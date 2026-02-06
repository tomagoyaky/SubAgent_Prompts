"""
Basic LLM Provider
Abstract base class for all LLM providers
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, Optional


class BasicProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(
        self,
        model_name: str,
        api_key: str,
        api_base: Optional[str] = None,
        stream_mode: bool = False,
        thinking_mode: bool = False,
        **kwargs
    ):
        """
        Initialize the provider

        Args:
            model_name: Name of the model to use
            api_key: API key for the model
            api_base: Optional API base URL
            stream_mode: Whether to use streaming mode
            thinking_mode: Whether to use thinking mode
            **kwargs: Additional parameters
        """
        self.model_name = model_name
        self.api_key = api_key
        self.api_base = api_base
        self.stream_mode = stream_mode
        self.thinking_mode = thinking_mode
        self.kwargs = kwargs
        self.llm = self._create_llm()
        # Add profile attribute for compatibility with deepagents library
        self.profile = {
            "model_name": model_name,
            "api_base": api_base,
            "stream_mode": stream_mode,
            "thinking_mode": thinking_mode
        }

    def _create_llm(self) -> Any:
        """
        Create the LLM instance

        Returns:
            LLM instance
        """
        return self._get_chat_model()

    def _generate(self, user_input: str, system_prompt: str, **kwargs) -> str:
        """
        Generate a response

        Args:
            user_input: User input text
            system_prompt: System prompt text
            **kwargs: Additional parameters

        Returns:
            Generated response
        """
        messages, invoke_kwargs = self._prepare_messages(
            user_input, system_prompt, **kwargs
        )
        response = self.llm.invoke(messages, **invoke_kwargs)
        return response.content

    def _stream(self, user_input: str, system_prompt: str, **kwargs) -> Iterator[str]:
        """
        Stream a response

        Args:
            user_input: User input text
            system_prompt: System prompt text
            **kwargs: Additional parameters

        Returns:
            Iterator yielding response chunks
        """
        messages, stream_kwargs = self._prepare_messages(
            user_input, system_prompt, **kwargs
        )
        for chunk in self.llm.stream(messages, **stream_kwargs):
            if chunk.content:
                yield chunk.content

    @abstractmethod
    def _get_chat_model(self) -> Any:
        """
        Get the chat model instance

        Returns:
            Chat model instance
        """
        pass

    def _prepare_messages(self, user_input: str, system_prompt: str, **kwargs) -> tuple:
        """
        Prepare messages for the chat model

        Args:
            user_input: User input text
            system_prompt: System prompt text
            **kwargs: Additional parameters

        Returns:
            Tuple of (messages, invoke_kwargs)
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
        return messages, kwargs

    def chat(self, user_input: str, system_prompt: str, **kwargs) -> str:
        """
        Chat with the LLM

        Args:
            user_input: User input text
            system_prompt: System prompt text
            **kwargs: Additional parameters

        Returns:
            Response text or streaming iterator
        """
        if self.stream_mode:
            return self._stream(user_input, system_prompt, **kwargs)
        else:
            return self._generate(user_input, system_prompt, **kwargs)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information

        Returns:
            Model information dictionary
        """
        return {
            "model_name": self.model_name,
            "api_base": self.api_base,
            "stream_mode": self.stream_mode,
            "thinking_mode": self.thinking_mode,
            "kwargs": self.kwargs,
        }

    def _llm_type(self) -> str:
        """
        Get LLM type for compatibility with deepagents library

        Returns:
            LLM type string
        """
        return "chat_openai"

    def invoke(self, messages, **kwargs):
        """
        Invoke method for compatibility with deepagents library

        Args:
            messages: Messages to send
            **kwargs: Additional parameters

        Returns:
            Response
        """
        if hasattr(self.llm, "invoke"):
            return self.llm.invoke(messages, **kwargs)
        # Fallback implementation
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Extract system prompt and user message
        system_prompt = ""
        user_input = ""
        
        for message in messages:
            if message.get("role") == "system":
                system_prompt = message.get("content", "")
            elif message.get("role") == "user":
                user_input = message.get("content", "")
        
        # Use existing chat method
        result = self.chat(user_input, system_prompt, **kwargs)
        
        # Return in expected format
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(result)

    def stream(self, messages, **kwargs):
        """
        Stream method for compatibility with deepagents library

        Args:
            messages: Messages to send
            **kwargs: Additional parameters

        Returns:
            Streaming response
        """
        if hasattr(self.llm, "stream"):
            return self.llm.stream(messages, **kwargs)
        # Fallback implementation
        from langchain_core.messages import HumanMessage, SystemMessage
        
        # Extract system prompt and user message
        system_prompt = ""
        user_input = ""
        
        for message in messages:
            if message.get("role") == "system":
                system_prompt = message.get("content", "")
            elif message.get("role") == "user":
                user_input = message.get("content", "")
        
        # Use existing chat method with streaming
        self.stream_mode = True
        return self.chat(user_input, system_prompt, **kwargs)

    def bind_tools(self, tools, **kwargs):
        """
        Bind tools to the model for compatibility with deepagents library

        Args:
            tools: Tools to bind
            **kwargs: Additional parameters

        Returns:
            Model with bound tools
        """
        if hasattr(self.llm, "bind_tools"):
            return self.llm.bind_tools(tools, **kwargs)
        # Fallback implementation
        return self
