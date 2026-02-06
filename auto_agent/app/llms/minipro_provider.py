"""
MiniPro Provider
Implementation for MiniPro models
"""

from typing import Any, Iterator

from langchain_openai import ChatOpenAI

from .basic_provider import BasicProvider


class MiniProProvider(BasicProvider):
    """MiniPro LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get MiniPro chat model instance"""
        return ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.api_base or "https://api.minipro.ai/v1",
            **self.kwargs
        )
