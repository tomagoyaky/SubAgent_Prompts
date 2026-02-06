"""
Basic Agent
Abstract base class for all agents
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
from app.core.dependency_injector import get_dependency


class BasicAgent(ABC, threading.Thread):
    """Abstract base class for agents that runs in a thread"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the agent

        Args:
            name: Agent name
            description: Agent description
            **kwargs: Additional parameters
        """
        # Initialize threading.Thread
        threading.Thread.__init__(self, name=name)

        self.name = name
        self.description = description
        self.kwargs = kwargs
        self.agent = self._create_deep_agent()
        self.task_id = None

    def _create_deep_agent(self):
        """
        Create deep agent using deepagents library

        Returns:
            Deep agent instance
        """
        # Extract parameters for deep agent creation
        # Use only parameters that are relevant for create_deep_agent
        deep_agent_kwargs = {}

        # Set model - use llm_provider from kwargs if provided
        model = self.kwargs.get("llm_provider") or self.kwargs.get("model")

        # If no model provided, create one from config
        if not model:
            # Get config from dependency injector
            config = get_dependency("config") or self.kwargs.get("config")
            
            if config:
                # Get LLM configuration from config
                llm_config = config.get_llm_config()

                # Required parameters
                default_model = llm_config.get("default_model")

                # Extract model configuration parameters
                model_kwargs = {
                    "temperature": llm_config.get("temperature"),
                    "top_p": llm_config.get("top_p"),
                    "max_tokens": llm_config.get("max_tokens"),
                }

                # Use initialize_llm_provider from llms.initializer to create model provider
                from app.llms.initializer import initialize_llm_provider

                model = initialize_llm_provider(model_name=default_model, **model_kwargs)
            else:
                logger.error("No config available for LLM initialization")
                return None

        deep_agent_kwargs["model"] = model

        # Set system prompt
        system_prompt = (
            self.kwargs.get("system_prompt")
            or f"You are {self.name}. {self.description}"
        )
        deep_agent_kwargs["system_prompt"] = system_prompt

        # Set tools
        tools = self.kwargs.get("tools") or get_all_tools()
        deep_agent_kwargs["tools"] = tools

        # Set subagents
        subagents = self.kwargs.get("subagents") or []
        deep_agent_kwargs["subagents"] = subagents

        # Set middleware
        middleware = self.kwargs.get("middleware") or [BasicMiddleware()]
        deep_agent_kwargs["middleware"] = middleware

        # Set interrupt handler
        interrupt_on = self.kwargs.get("interrupt_on") or {}
        deep_agent_kwargs["interrupt_on"] = interrupt_on

        # Set skills
        skills = self.kwargs.get("skills") or BasicSkill.get_default_skills()
        deep_agent_kwargs["skills"] = skills

        # Add long-term memory support if enabled
        long_term_memory = self.kwargs.get("long_term_memory")
        if long_term_memory:
            backend, store, checkpointer = create_backend_with_long_term_memory()
            deep_agent_kwargs["backend"] = backend
            deep_agent_kwargs["store"] = store
            deep_agent_kwargs["checkpointer"] = checkpointer

        # Optional parameters that create_deep_agent accepts
        optional_params = ["memory"]
        for param in optional_params:
            if param in self.kwargs:
                deep_agent_kwargs[param] = self.kwargs[param]

        # Create deep agent with the extracted parameters
        agent = create_deep_agent(**deep_agent_kwargs)

        return agent

    def get_thread_id(self) -> str:
        """
        Get the thread ID for the current thread

        Returns:
            Thread ID string
        """
        return str(threading.get_ident())

    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information

        Returns:
            Agent information dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "thread_id": self.get_thread_id(),
        }

    def get_llm_info(self) -> Dict[str, Any]:
        """
        Get LLM information

        Returns:
            LLM information dictionary
        """
        if self.agent:
            try:
                return {"model": getattr(self.agent, "model", None), "system_prompt": getattr(self.agent, "system_prompt", None)}
            except Exception as e:
                logger.error(f"Error getting LLM info: {e}")
                return {"model": None, "system_prompt": None}
        return {"model": None, "system_prompt": None}

    def start(
        self, user_input: Optional[str] = None, prompt: Optional[Dict[str, Any]] = None
    ):
        """
        Start the agent thread

        Args:
            user_input: Optional user input description
            prompt: Optional prompt information
        """
        # Update user_input and prompt if provided
        if user_input:
            self.kwargs["user_input"] = user_input
        if prompt:
            self.kwargs["prompt"] = prompt

        # Call parent class start method to start the thread
        threading.Thread.start(self)

    def run(self):
        """
        Run method for the thread
        This method calls the agent with the provided user_input
        """
        if "user_input" in self.kwargs:
            user_input = self.kwargs["user_input"]
            prompt = self.kwargs.get("prompt")
            try:
                if self.agent:
                    # Use stream method instead of invoke to avoid sync invocation issues
                    for chunk in self.agent.stream(
                        {"user_input": user_input, "prompt": prompt}
                    ):
                        # Process each chunk as it arrives
                        pass
                    # Log success message
                    logger.info(f"Agent {self.name} execution completed successfully")
                else:
                    logger.error(f"Agent {self.name} has no underlying agent instance")
            except Exception as e:
                logger.error(f"Agent {self.name} execution failed: {e}")
        else:
            logger.warning(f"Agent {self.name} started but no user_input provided")

    def run_with_thread_pool(self):
        """
        Run agent using thread pool

        Returns:
            Task ID
        """
        self.task_id = thread_pool_manager.submit_task(self.run)
        return self.task_id

    def validate_input(
        self, user_input: str, prompt: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Validate input

        Args:
            user_input: User input description
            prompt: Optional prompt information

        Returns:
            Whether input is valid
        """
        if not user_input or not isinstance(user_input, str):
            return False
        if prompt is not None and not isinstance(prompt, dict):
            return False
        return True

    def _process_message(self, user_input: str):
        """
        Process a single user message and display the response

        Args:
            user_input: User input text
        """
        # Create messages for agent invocation
        messages = [
            {"role": "system", "content": "你是一个专业的助手"},
            {"role": "user", "content": user_input}
        ]
        
        try:
            if not self.agent:
                print("Auto-Agent: Agent not initialized.")
                return
            
            # Check if agent supports streaming
            if hasattr(self.agent, "model") and hasattr(self.agent.model, "stream"):
                self._handle_streaming_response(messages)
            else:
                self._handle_non_streaming_response(messages)
        except Exception as e:
            logger.error(f"Error invoking agent: {e}")
            print("Auto-Agent: An error occurred while processing your request.")

    def _handle_streaming_response(self, messages: list):
        """
        Handle streaming response from agent

        Args:
            messages: List of messages to send to agent
        """
        print("\nAuto-Agent: ", end="", flush=True)
        full_response = []
        try:
            for chunk in self.agent.stream({"messages": messages}):
                if chunk:
                    # Parse chunk to extract content
                    if isinstance(chunk, dict):
                        # If chunk is a dict, extract content field
                        content = chunk.get("content", "")
                        if content:
                            print(content, end="", flush=True)
                            full_response.append(content)
                    else:
                        # If chunk is not a dict, print as is
                        print(chunk, end="", flush=True)
                        full_response.append(str(chunk))
            print()  # New line after streaming complete
            if not full_response:
                print("No response received.")
        except Exception as e:
            logger.error(f"Error streaming agent response: {e}")
            print("\nAuto-Agent: An error occurred during streaming.")

    def _handle_non_streaming_response(self, messages: list):
        """
        Handle non-streaming response from agent

        Args:
            messages: List of messages to send to agent
        """
        result = self.agent.invoke({"messages": messages})
        # Display the result
        if result:
            print(f"\nAuto-Agent: {result}")
        else:
            print("\nAuto-Agent: No response received.")

    def chat(self, default_user_input: Optional[str] = None):
        """
        Interactive chat function for terminal interaction

        Args:
            default_user_input: Optional default user input to start with
        """
        print("\n=======================================")
        print("        Auto Agent Chat")
        print("=======================================")
        print("Type 'exit' or 'quit' to end the chat")
        print("=======================================")
        
        # Process default user input if provided
        if default_user_input:
            print(f"\nYou: {default_user_input}")
            
            if self.validate_input(default_user_input):
                self._process_message(default_user_input)
            else:
                print("Auto-Agent: Invalid input, please try again.")
        
        # Chat loop
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ")
                
                # Check if user wants to exit
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("\nAuto-Agent: Goodbye!")
                    print("=======================================")
                    break
                
                # Validate input
                if not self.validate_input(user_input):
                    print("Auto-Agent: Invalid input, please try again.")
                    continue
                
                # Process the message
                self._process_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\nAuto-Agent: Chat interrupted.")
                print("=======================================")
                break
            except Exception as e:
                logger.error(f"Chat error: {e}")
                print("Auto-Agent: An error occurred, please try again.")
