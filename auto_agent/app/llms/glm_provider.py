"""
GLM Provider
Implementation for GLM models
"""

from typing import Any, Iterator

from langchain_openai import ChatOpenAI

from .basic_provider import BasicProvider


class GLMProvider(BasicProvider):
    """GLM LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get GLM chat model instance"""
        return ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.api_base or "https://open.bigmodel.cn/api/messages",
            **self.kwargs
        )
