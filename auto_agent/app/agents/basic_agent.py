"""
基础代理
所有代理的抽象基类
"""

import threading
from abc import ABC
from typing import Dict, Any, Optional
from deepagents import create_deep_agent
from app.agents.tools.basic_tool import get_all_tools
from app.agents.middleware.basic_middleware import BasicMiddleware
from app.agents.skills.basic_skill import BasicSkill
from app.agents.backends.basic_backend import create_backend_with_long_term_memory
from app.utils.logger import global_logger as logger
from app.utils.thread_pool import thread_pool_manager
from app.utils.msg_utils import process_message
from app.core.dependency_injector import get_dependency


class BasicAgent(ABC, threading.Thread):
    """所有代理的抽象基类，运行在一个线程中"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        初始化代理

        参数:
            name: 代理名称
            description: 代理描述
            **kwargs: 其他参数
        """
        # 初始化 threading.Thread
        threading.Thread.__init__(self, name=name)

        self.name = name
        self.description = description
        self.kwargs = kwargs
        self.agent = self._create_deep_agent()
        self.task_id = None

    def _create_deep_agent(self):
        """
        使用 deepagents 库创建深度代理

        返回:
            深度代理实例
        """
        # 提取深度代理创建的参数
        # 只使用与 create_deep_agent 相关的参数
        deep_agent_kwargs = {}

        # 设置模型 - 如果提供了 llm_provider，则使用它
        model = self.kwargs.get("llm_provider") or self.kwargs.get("model")

        # 如果没有提供模型，则从配置创建
        if not model:
            # 从依赖注入器获取配置
            config = get_dependency("config") or self.kwargs.get("config")
            
            if config:
                # 从配置获取 LLM 配置
                llm_config = config.get_llm_config()

                # 必需参数
                default_model = llm_config.get("default_model")

                # 提取模型配置参数
                model_kwargs = {
                    "temperature": llm_config.get("temperature"),
                    "top_p": llm_config.get("top_p"),
                    "max_tokens": llm_config.get("max_tokens"),
                    "stream_mode": llm_config.get("stream_mode", True),
                    "thinking_mode": llm_config.get("thinking_mode"),
                }

                # 使用 llms.initializer 中的 initialize_llm_provider 创建模型提供商
                from app.llms.initializer import initialize_llm_provider

                model = initialize_llm_provider(model_name=default_model, **model_kwargs)
            else:
                logger.error("没有可用的配置用于 LLM 初始化")
                return None

        deep_agent_kwargs["model"] = model

        # 设置系统提示
        system_prompt = (
            self.kwargs.get("system_prompt")
            or f"你是 {self.name}。 {self.description}"
        )
        deep_agent_kwargs["system_prompt"] = system_prompt

        # 设置工具
        tools = self.kwargs.get("tools") or get_all_tools()
        deep_agent_kwargs["tools"] = tools

        # 设置子代理
        subagents = self.kwargs.get("subagents") or []
        deep_agent_kwargs["subagents"] = subagents

        # 设置中间件
        middleware = self.kwargs.get("middleware") or [BasicMiddleware()]
        deep_agent_kwargs["middleware"] = middleware

        # 设置中断处理程序
        interrupt_on = self.kwargs.get("interrupt_on") or {}
        deep_agent_kwargs["interrupt_on"] = interrupt_on

        # 设置技能
        skills = self.kwargs.get("skills") or BasicSkill.get_default_skills()
        deep_agent_kwargs["skills"] = skills

        # 如果启用，添加长期记忆支持
        long_term_memory = self.kwargs.get("long_term_memory")
        if long_term_memory:
            backend, store, checkpointer = create_backend_with_long_term_memory()
            deep_agent_kwargs["backend"] = backend
            deep_agent_kwargs["store"] = store
            deep_agent_kwargs["checkpointer"] = checkpointer

        # create_deep_agent 接受的可选参数
        optional_params = ["memory"]
        for param in optional_params:
            if param in self.kwargs:
                deep_agent_kwargs[param] = self.kwargs[param]

        # 使用提取的参数创建深度代理
        agent = create_deep_agent(**deep_agent_kwargs)

        return agent

    def get_thread_id(self) -> str:
        """
        获取当前线程的线程 ID

        返回:
            线程 ID 字符串
        """
        return str(threading.get_ident())

    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取代理信息

        返回:
            代理信息字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "thread_id": self.get_thread_id(),
        }

    def get_llm_info(self) -> Dict[str, Any]:
        """
        获取 LLM 信息

        返回:
            LLM 信息字典
        """
        if self.agent:
            try:
                return {"model": getattr(self.agent, "model", None), "system_prompt": getattr(self.agent, "system_prompt", None)}
            except Exception as e:
                logger.error(f"获取 LLM 信息时出错: {e}")
                return {"model": None, "system_prompt": None}
        return {"model": None, "system_prompt": None}

    def start(
        self, user_input: Optional[str] = None, prompt: Optional[Dict[str, Any]] = None
    ):
        """
        启动代理线程

        参数:
            user_input: 可选的用户输入描述
            prompt: 可选的提示信息
        """
        # 如果提供，更新 user_input 和 prompt
        if user_input:
            self.kwargs["user_input"] = user_input
        if prompt:
            self.kwargs["prompt"] = prompt

        # 调用父类的 start 方法启动线程
        threading.Thread.start(self)

    def run(self):
        """
        线程的运行方法
        此方法使用提供的 user_input 调用代理
        """
        if "user_input" in self.kwargs:
            user_input = self.kwargs["user_input"]
            prompt = self.kwargs.get("prompt")
            try:
                if self.agent:
                    # 使用 stream 方法而不是 invoke 以避免同步调用问题
                    for chunk in self.agent.stream(
                        {"user_input": user_input, "prompt": prompt}
                    ):
                        # 处理每个到达的块
                        pass
                    # 记录成功消息
                    logger.info(f"代理 {self.name} 执行成功完成")
                else:
                    logger.error(f"代理 {self.name} 没有底层代理实例")
            except Exception as e:
                logger.error(f"代理 {self.name} 执行失败: {e}")
        else:
            logger.warning(f"代理 {self.name} 启动但未提供 user_input")

    def run_with_thread_pool(self):
        """
        使用线程池运行代理

        返回:
            任务 ID
        """
        self.task_id = thread_pool_manager.submit_task(self.run)
        return self.task_id

    def validate_input(
        self, user_input: str, prompt: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        验证输入

        参数:
            user_input: 用户输入描述
            prompt: 可选的提示信息

        返回:
            输入是否有效
        """
        if not user_input or not isinstance(user_input, str):
            return False
        if prompt is not None and not isinstance(prompt, dict):
            return False
        return True



    def chat(self, default_user_input: Optional[str] = None):
        """
        用于终端交互的交互式聊天功能

        参数:
            default_user_input: 可选的默认用户输入，用于启动聊天
        """
        print("\n=======================================")
        print("        Auto Agent Chat")
        print("=======================================")
        print("Type 'exit' or 'quit' to end the chat")
        print("=======================================")
        
        # 如果提供，处理默认用户输入
        if default_user_input:
            print(f"\nYou: {default_user_input}")
            
            if self.validate_input(default_user_input):
                process_message(self.agent, default_user_input)
            else:
                print("Auto-Agent: 无效输入，请重试。")
        
        # 聊天循环
        while True:
            try:
                # 获取用户输入
                user_input = input("\nYou: ")
                
                # 检查用户是否要退出
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\nAuto-Agent: Goodbye!")
                    print("=======================================")
                    break
                
                # 验证输入
                if not self.validate_input(user_input):
                    print("Auto-Agent: 无效输入，请重试。")
                    continue
                
                # 处理消息
                process_message(self.agent, user_input)
                
            except KeyboardInterrupt:
                print("\n\nAuto-Agent: Chat interrupted.")
                print("=======================================")
                break
            except Exception as e:
                logger.error(f"聊天错误: {e}")
                print("Auto-Agent: 发生错误，请重试。")
