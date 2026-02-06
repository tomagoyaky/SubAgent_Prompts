import requests
import json
import time
from typing import List, Dict, Optional, Generator
from skills_loader import list_skills, format_skills_system_prompt, get_skill_content, match_skills_by_tags, SkillMetadata

# ===================== 全局配置 =====================
# 模型配置（支持切换DeepSeek/Ollama）
MODEL_TYPE = "deepseek"  # 可选 "ollama" 或 "deepseek"
# MODEL_TYPE = "ollama"  # 可选 "ollama" 或 "deepseek"
DEFAULT_STREAM = True  # 默认开启流式输出，False则为非流式

# DeepSeek-Chat API配置（替换为你的有效API Key）
DEEPSEEK_API_KEY = "sk-8209e046f7234a128ecf9220030dd718"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
DEEPSEEK_HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

# Ollama配置（本地启动Ollama服务后使用）
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3:8b"

# ===================== 工具类：大模型调用封装（支持流式+非流式） =====================
class LLMClient:
    """所有Agent统一调用大模型的封装类，支持本地Ollama和远程DeepSeek，兼容流式/非流式输出"""
    @staticmethod
    def chat(messages: List[Dict], temperature: float = 0.7, stream: bool = DEFAULT_STREAM) -> str | Generator[str, None, None]:
        """
        统一调用入口：stream=True返回生成器（流式），stream=False返回字符串（非流式）
        :param messages: 对话消息列表
        :param temperature: 生成随机性
        :param stream: 是否开启流式输出
        :return: 字符串（非流式）或生成器（流式）
        """
        if MODEL_TYPE == "deepseek":
            return LLMClient._chat_deepseek(messages, temperature, stream)
        elif MODEL_TYPE == "ollama":
            return LLMClient._chat_ollama(messages, temperature, stream)
        else:
            return f"不支持的模型类型：{MODEL_TYPE}"
    
    @staticmethod
    def _chat_deepseek(messages: List[Dict], temperature: float = 0.7, stream: bool = False) -> str | Generator[str, None, None]:
        """DeepSeek 流式/非流式调用（SSE 格式响应）"""
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "temperature": temperature,
            "stream": stream  # 关键：控制是否流式
        }
        try:
            # 流式请求需设置 stream=True，逐行接收响应
            response = requests.post(DEEPSEEK_API_URL, headers=DEEPSEEK_HEADERS, json=payload, stream=stream, timeout=60)
            response.raise_for_status()

            # 非流式：直接返回完整结果
            if not stream:
                return response.json()["choices"][0]["message"]["content"].strip()
            
            # 流式：逐行解析 SSE 响应，返回生成器
            def generate():
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        # 解析 SSE 格式：data: {...}
                        line_str = line.decode("utf-8").strip()
                        if line_str.startswith("data: ") and line_str != "data: [DONE]":
                            chunk_data = json.loads(line_str[6:])  # 去掉 "data: " 前缀
                            chunk_content = chunk_data["choices"][0]["delta"].get("content", "")
                            if chunk_content:
                                full_content += chunk_content
                                yield chunk_content  # 逐块返回内容
                return full_content
            return generate()

        except Exception as e:
            error_msg = f"DeepSeek调用失败：{str(e)}"
            if stream:
                # 流式场景下，错误信息作为生成器返回
                def error_gen():
                    yield error_msg
                return error_gen()
            return error_msg
    
    @staticmethod
    def _chat_ollama(messages: List[Dict], temperature: float = 0.7, stream: bool = False) -> str | Generator[str, None, None]:
        """Ollama 流式/非流式调用（逐行 JSON 响应）"""
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "temperature": temperature,
            "stream": stream  # 关键：控制是否流式
        }
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, stream=stream, timeout=60)
            response.raise_for_status()

            # 非流式：直接返回完整结果
            if not stream:
                return response.json()["message"]["content"].strip()
            
            # 流式：逐行解析 JSON 响应，返回生成器
            def generate():
                full_content = ""
                for line in response.iter_lines():
                    if line:
                        chunk_data = json.loads(line.decode("utf-8"))
                        chunk_content = chunk_data["message"].get("content", "")
                        if chunk_content:
                            full_content += chunk_content
                            yield chunk_content  # 逐块返回内容
                return full_content
            return generate()

        except Exception as e:
            error_msg = f"Ollama调用失败：{str(e)}"
            if stream:
                def error_gen():
                    yield error_msg
                return error_gen()
            return error_msg

# ===================== 子Agent类（支持流式执行） =====================
class SubAgent:
    """
    子Agent：支持专属Prompt定制，兼容流式/非流式任务执行
    :param agent_id: 子Agent唯一标识
    :param role: 子Agent角色
    :param ability_tags: 能力标签
    :param prompt_template: 定制化Prompt模板
    :param skills: 该Agent可用的技能列表
    """
    def __init__(self, agent_id: str, role: str, ability_tags: List[str], prompt_template: str, skills: Optional[List[SkillMetadata]] = None):
        self.agent_id = agent_id
        self.role = role
        self.ability_tags = ability_tags
        self.prompt_template = prompt_template
        self.skills = skills or []
        self.llm = LLMClient()

    def execute_task(self, task: Dict, stream: bool = DEFAULT_STREAM) -> str:
        """
        执行子任务：支持流式输出（实时打印），返回完整结果
        :param task: 子任务字典
        :param stream: 是否开启流式输出
        :return: 子任务完整执行结果
        """
        # 替换Prompt模板变量
        final_prompt = self.prompt_template.format(
            task_name=task["name"],
            task_goal=task["goal"],
            task_input=task["input"],
            task_output=task["output"]
        )
        
        # 添加技能系统提示
        skills_prompt = ""
        if self.skills:
            skills_prompt = format_skills_system_prompt(self.skills)
            final_prompt = skills_prompt + "\n" + final_prompt
        
        messages = [{"role": "user", "content": final_prompt}]
        
        # 调用大模型（流式/非流式）
        result_gen = self.llm.chat(messages, temperature=0.6, stream=stream)
        
        # 处理流式输出：实时打印 + 收集完整结果
        full_result = ""
        if stream:
            print("子任务输出：", end="", flush=True)
            for chunk in result_gen:
                print(chunk, end="", flush=True)
                full_result += chunk
            print()
        else:
            full_result = result_gen
            print(f"子任务输出：{full_result[:60]}...")
        
        return full_result.strip()

# ===================== 总控Agent类（适配流式输出） =====================
class MasterAgent:
    """总控Agent：通用需求拆解、动态生成子Agent、任务调度、结果整合（支持流式）"""
    def __init__(self, skills_sources: Optional[List[str]] = None):
        self.llm = LLMClient()
        self.sub_agents: Dict[str, SubAgent] = {}
        self.task_results: Dict[str, str] = {}
        self.skills_sources = skills_sources or []
        self.all_skills: Dict[str, SkillMetadata] = {}
        
        # 加载所有 skills
        if self.skills_sources:
            self._load_skills()

    def register_sub_agent(self, sub_agent: SubAgent):
        """注册子Agent（动态生成后自动调用）"""
        self.sub_agents[sub_agent.agent_id] = sub_agent

    def _load_skills(self):
        """加载所有技能"""
        print("\n===== 加载 Skills =====")
        self.all_skills = list_skills(self.skills_sources)
        print(f"✅ 成功加载 {len(self.all_skills)} 个技能：")
        for skill_name, skill in self.all_skills.items():
            print(f"  - {skill_name}: {skill['description']}")

    def _parse_requirement(self, requirement: str) -> List[Dict]:
        """增强需求拆解：返回子任务+角色+能力+核心要求"""
        parse_prompt = f"""
        你是专业需求拆解师，将用户需求拆解为【可执行、带依赖】的子任务，仅返回JSON数组，无其他文字。
        子任务字段要求：
        1. task_id：唯一标识（如T001）
        2. name：任务名（简洁明确）
        3. goal：任务目标（核心目的）
        4. input：任务输入（所需数据/信息）
        5. output：输出要求（格式、内容规范）
        6. dependencies：依赖任务ID（无依赖则为空数组[]）
        7. tags：任务标签（匹配能力，如["数据处理"]）
        8. role：执行该任务的专属子Agent角色（如"资深数据分析师"）
        9. core_requirements：该任务的核心执行要求（如"数据精准、输出可视化描述"）
        
        示例：[{{
            "task_id":"T001",
            "name":"数据采集",
            "goal":"获取2026年1月销售原始数据",
            "input":"销售Excel文件地址",
            "output":"清洗后的结构化数据集",
            "dependencies":[],
            "tags":["数据处理"],
            "role":"数据采集专员",
            "core_requirements":"确保数据完整无缺失，清洗重复值和异常值"
        }}]
        
        用户需求：{requirement}
        """
        messages = [{"role": "user", "content": parse_prompt}]
        parse_result = self.llm.chat(messages, temperature=0.3, stream=False)  # 拆解需求固定非流式，保证结构化
        try:
            return json.loads(parse_result)
        except:
            return [{
                "task_id":"T000",
                "name":"拆解失败",
                "goal":"无",
                "input":"无",
                "output":"无",
                "dependencies":[],
                "tags":["通用"],
                "role":"通用执行专家",
                "core_requirements":"按要求完成基础任务，输出简洁准确"
            }]

    def _generate_dynamic_agent_prompt(self, task: Dict) -> str:
        """自动为子任务生成专属Prompt模板"""
        prompt_template = f"""
        你是{task['role']}，专业能力：{', '.join(task['tags'])}。
        核心执行要求：{task['core_requirements']}。
  请执行子任务：{{task_name}}，任务目标：{{task_goal}}。
  输入信息：{{task_input}}，输出要求：{{task_output}}。
  要求：严格遵循核心执行要求，输出精准、符合规范，无冗余内容。
        """
        return prompt_template.strip()

    def _generate_dynamic_agents(self, tasks: List[Dict]):
        """动态创建子Agent并自动注册（同类任务复用）"""
        print("\n===== 动态生成子Agent =====")
        generated_agent_keys = set()
        
        for task in tasks:
            agent_key = f"{task['role']}_{'_'.join(task['tags'])}"
            if agent_key in generated_agent_keys:
                continue
            
            dynamic_prompt = self._generate_dynamic_agent_prompt(task)
            agent_id = f"A_{task['role'][:2].upper()}_{len(generated_agent_keys)+1:03d}"
            
            # 根据任务标签匹配 skills
            matched_skills = match_skills_by_tags(task["tags"], self.all_skills)
            
            dynamic_agent = SubAgent(
                agent_id=agent_id,
                role=task['role'],
                ability_tags=task['tags'],
                prompt_template=dynamic_prompt,
                skills=matched_skills
            )
            self.register_sub_agent(dynamic_agent)
            generated_agent_keys.add(agent_key)
            
            skills_info = f"，包含 {len(matched_skills)} 个技能" if matched_skills else ""
            print(f"✅ 生成子Agent：{agent_id} - {task['role']}（标签：{task['tags']}{skills_info}）")

    def _assign_agent_for_task(self, task: Dict) -> Optional[SubAgent]:
        """基于标签匹配子Agent"""
        for agent in self.sub_agents.values():
            if any(tag in agent.ability_tags for tag in task["tags"]):
                return agent
        for agent in self.sub_agents.values():
            if "通用" in agent.ability_tags:
                return agent
        return None

    def _schedule_tasks(self, tasks: List[Dict], stream: bool = DEFAULT_STREAM) -> Dict[str, str]:
        """按依赖顺序执行任务（支持流式输出）"""
        remaining_tasks = tasks.copy()
        executed_tasks = set()
        results = {}

        print("\n===== 按依赖顺序执行子任务 =====")
        while remaining_tasks:
            executable_tasks = [t for t in remaining_tasks if all(dep in executed_tasks for dep in t["dependencies"])]
            if not executable_tasks:
                print("警告：存在循环依赖，调度终止！")
                break

            for task in executable_tasks:
                print(f"\n📌 执行任务：{task['task_id']} - {task['name']}")
                agent = self._assign_agent_for_task(task)
                if not agent:
                    result = "无可用子Agent"
                    print(f"子任务输出：{result}")
                else:
                    print(f"🤖 分配子Agent：{agent.agent_id} - {agent.role}")
                    result = agent.execute_task(task, stream=stream)  # 流式执行子任务
                results[task["task_id"]] = result
                executed_tasks.add(task["task_id"])
                time.sleep(0.5)  # 短延时，提升交互体验

            remaining_tasks = [t for t in remaining_tasks if t["task_id"] not in executed_tasks]
        return results

    def _integrate_results(self, requirement: str, tasks: List[Dict], results: Dict[str, str], stream: bool = DEFAULT_STREAM) -> str:
        """结果整合（支持流式输出最终结果）"""
        task_details = "\n".join([f"任务{t['task_id']}：{t['name']}\n结果：{results[t['task_id']]}" for t in tasks])
        integrate_prompt = f"""
        你是结果整合专家，根据原始需求和子任务结果，生成完整、连贯的最终输出，直接输出结果，无额外解释。
        原始需求：{requirement}
        子任务结果：{task_details}
        """
        messages = [{"role": "user", "content": integrate_prompt}]
        
        # 流式输出最终结果
        print("\n===== 整合所有结果（流式输出） =====")
        result_gen = self.llm.chat(messages, temperature=0.5, stream=stream)
        
        full_final_result = ""
        if stream:
            print("最终结果：", end="", flush=True)
            for chunk in result_gen:
                print(chunk, end="", flush=True)
                full_final_result += chunk
            print()
        else:
            full_final_result = result_gen
            print(f"最终结果：{full_final_result}")
        
        return full_final_result.strip()

    def run(self, requirement: str, stream: bool = DEFAULT_STREAM) -> str:
        """总控主流程（支持流式）"""
        print(f"===== 总控接收需求：{requirement} =====")
        # 1. 拆解需求
        tasks = self._parse_requirement(requirement)
        if tasks[0]["task_id"] == "T000":
            return "需求拆解失败"
        print(f"拆解完成，共{len(tasks)}个子任务：")
        for t in tasks:
            print(f"- {t['task_id']}：{t['name']}（角色：{t['role']}，依赖：{t['dependencies']}）")

        # 2. 动态生成子Agent
        self._generate_dynamic_agents(tasks)

        # 3. 调度执行子任务（流式）
        self.task_results = self._schedule_tasks(tasks, stream=stream)

        # 4. 整合结果（流式）
        final_result = self._integrate_results(requirement, tasks, self.task_results, stream=stream)
        return final_result

# ===================== 运行示例 =====================
if __name__ == "__main__":
    # 配置 skills 源目录
    skills_sources = [
        "./skills",  # 项目级 skills
        # "~/.deepagents/skills",  # 用户级 skills（可选）
    ]
    
    # 初始化总控（传入 skills_sources）
    master = MasterAgent(skills_sources=skills_sources)

    # 选择需求类型
    print("请选择需求类型：")
    print("1. 项目类：策划一场线上产品发布会（面向年轻用户，含宣传、流程、预算）")
    print("2. 内容类：写一篇AI Agent科普文章（1500字，大众阅读，含定义、场景、趋势）")
    print("3. 工作流类：整理2026年1月销售数据，生成含图表的分析报告（业绩+问题+建议）")
    choice = input("输入选择（1/2/3）：")

    if choice == "1":
        req = "策划一场线上产品发布会，面向年轻用户群体，突出产品核心功能，包含宣传方案、执行流程、预算核算、风险预案"
    elif choice == "2":
        req = "写一篇AI Agent应用的科普文章，1500字左右，适合大众阅读，通俗易懂，覆盖定义、实际应用场景、未来发展趋势"
    elif choice == "3":
        req = "整理2026年1月销售数据（Excel格式），生成含可视化图表的分析报告，包含业绩总结、问题分析、下月优化建议，输出PDF格式"
    else:
        req = "写一篇AI Agent应用的科普文章（1500字，大众阅读）"

    # 执行总控（默认流式输出，可手动改为stream=False关闭）
    final_output = master.run(req, stream=DEFAULT_STREAM)