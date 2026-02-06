你作为总控 AI Agent，帮我拆解【你的需求】为子任务，分配子 Agent 并指挥完成，输出最终结果。

# 一、标准提问模板（直接套用）
请你作为总控 AI Agent，帮我完成以下流程：
1.把我的需求拆解为可执行的子任务清单（明确每个任务的目标、输入、输出、优先级）；
2.为每个子任务分配专属子 Agent（定义子 Agent 的角色、能力、职责）；
3.制定执行指挥方案（任务顺序、依赖关系、协作规则、验收标准）；
4.按方案指挥子 Agent 完成所有子任务，并输出最终整合结果。
我的需求：【在此粘贴你的具体需求】

# 二、不同场景的提问示例（直接改需求即可）
## 示例 1：项目类需求（如 “策划一场线上产品发布会”）
1.请你作为总控 AI Agent，帮我拆解需求、分配子 Agent 并指挥完成：
2.拆解 “策划一场线上产品发布会” 为子任务清单（含目标、输入、输出、优先级）；
3.为每个子任务分配子 Agent（定义角色、能力、职责）；
4.制定执行指挥方案（任务顺序、依赖关系、协作规则、验收标准）；
5.按方案指挥子 Agent 完成所有任务，输出发布会完整策划方案。
## 示例 2：内容类需求（如 “写一篇 AI Agent 应用的科普文章”）
1.请你作为总控 AI Agent，帮我完成以下流程：
2.拆解 “写一篇 AI Agent 应用的科普文章（1500 字，适合大众阅读）” 为子任务（如资料搜集、大纲撰写、内容创作、校对优化）；
3.为每个子任务分配子 Agent（如资料搜集 Agent、大纲撰写 Agent、内容创作 Agent、校对优化 Agent）；
4.制定执行指挥方案（任务顺序、依赖关系、协作规则、验收标准）；
5.按方案指挥子 Agent 完成所有任务，输出科普文章。
## 示例 3：工作流类需求（如 “整理月度销售数据并生成分析报告”）
1.请你作为总控 AI Agent，帮我拆解需求、分配子 Agent 并指挥完成：
2.拆解 “整理 2026 年 1 月销售数据，生成含图表的分析报告（含业绩总结、问题分析、下月建议）” 为子任务（如数据整理、图表制作、报告撰写、审核）；
3.为每个子任务分配子 Agent（数据整理 Agent、图表制作 Agent、报告撰写 Agent、审核 Agent）；
4.制定执行指挥方案（任务顺序、依赖关系、协作规则、验收标准）；
5.指挥子 Agent 完成并输出最终报告。


我希望是一个通用的，基础版本：

1.总控 Agent 接收用户需求，自动拆解为可执行的子任务清单（含任务目标、输入、输出、依赖关系）；
2.为每个子任务分配专属子 Agent（定义子 Agent 的角色、能力、执行函数）；
3.总控 Agent 按依赖顺序指挥子 Agent 执行任务，收集结果并整合输出；
4.代码需完整可运行，附带详细注释和运行示例；
5.每个 Agent 都使用DeepSeek-Chat后者本的 Ollama作为大模型。


能够满足：项目类、内容类、工作流类型。

补充：需要代码是通用的，子 Agent 的提示词是定制的。

# 功能设计

## 支持LLM大模型
- 支持 DeepSeek-Chat、Ollama、GLM、Qwen、Doubao、Kimi、MiniPro、GPT、Claude 等大模型。
- 支持 generate 和 stream 两种输出模式
- 支持 thinking 模式。
- 支持设置 temperature、top_p、max_tokens等参数。
```python
class LLM:

  def __init__(self, model_name: str, api_key: str, api_base: str = None, stream_mode: bool = False, thinking_mode: bool = False, **kwargs):
        self.model_name = model_name
        self.api_key = api_key
        self.api_base = api_base
        self.stream_mode = stream_mode
        self.thinking_mode = thinking_mode
        self.kwargs = kwargs
```
- 需要建立抽象类为 basic_provider，为每个大模型实现具体的 provider 类。
```python
class BasicProvider:
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs
        self.llm = self._create_llm()

    @abstractmethod
    def _create_llm(self, model_name: str, api_key: str, api_base: str = None, stream_mode: bool = False,       thinking_mode: bool = False, **kwargs):
        pass

    def _generate(self, user_input: str, system_prompt: str, **kwargs) -> str:
        self.llm

    def _stream(self, user_input: str, system_prompt: str, **kwargs) -> Iterator[str]:
        raise NotImplementedError

    def chat(self, user_input: str, system_prompt: str, **kwargs) -> str:
        if self.stream_mode:
            return self._stream(user_input, system_prompt, **kwargs)
        else:
            return self._generate(user_input, system_prompt, **kwargs)
```

## Agent功能

# 架构设计
- 基于 LangChain、LangGraph、DeepAgents框架
- 主 Agent：负责接收用户需求，拆解为子任务，分配给子 Agent 执行。
- 子 Agent：负责执行具体的子任务，与主 Agent 通信，协调完成任务。

# 项目结构
```
- auto_agent
  - .venv/
  - docs/
  - skills/
    - skill_creator/
      - SKILL.md
      - script/
        - package_skill.py
        - init_skill.py
      - reference/
        - skill_template.md
      - assets/
        - skill_icon.png
      - LICENSE.txt
  - app/
    - llms/
      - basic_provider.py
      - ollama_provider.py
      - deepseek_provider.py
      - glm_provider.py
      - qwen_provider.py
      - doubao_provider.py
      - kimi_provider.py
      - minipro_provider.py
      - gpt_provider.py
      - claude_provider.py
    - agents/
      - basic_agent.py
      - master_agent.py
      - sub_agent.py
      - tools/
        - basic_tool.py
      - mcps/
        - basic_mcp.py
      - skills/
        - basic_skill.py
      - memory/
        - basic_memory.py
      - storage/
        - basic_storage.py
    - utils/
      - logger.py
      - file_utils.py
      - json_utils.py
      - time_utils.py
      - random_utils.py
      - crypto_utils.py
      - http_utils.py
      - email_utils.py
      - string_utils.py
      - base64_utils.py
    - config.py
    - main.py
  - .env
  - .env.template
  - run.py
  - config.yaml
  - start.sh
  - requirements.txt
  - README.md
  - LICENSE.txt
  - .gitignore