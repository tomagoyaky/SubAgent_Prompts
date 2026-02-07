"""
DeepSeek Provider
Implementation for DeepSeek models
"""

from typing import Any, Iterator

from langchain_openai import ChatOpenAI

from .basic_provider import BasicProvider


class DeepSeekProvider(BasicProvider):
    """DeepSeek LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get DeepSeek chat model instance"""
        # Add streaming parameter
        chat_kwargs = {
            "model": self.model_name,
            "api_key": self.api_key,
            "base_url": self.api_base or "https://api.deepseek.com/v1",
            "streaming": self.stream_mode,
            **self.kwargs
        }
        return ChatOpenAI(**chat_kwargs)
