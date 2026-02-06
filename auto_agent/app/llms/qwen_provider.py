"""
Qwen Provider
Implementation for Qwen models
"""

from typing import Any, Iterator

from langchain_openai import ChatOpenAI

from .basic_provider import BasicProvider


class QwenProvider(BasicProvider):
    """Qwen LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get Qwen chat model instance"""
        return ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.api_base or "https://ark.cn-beijing.volces.com/api/v3",
            **self.kwargs
        )
