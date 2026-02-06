"""
GPT Provider
Implementation for OpenAI GPT models
"""

from typing import Any, Iterator

from langchain_openai import ChatOpenAI

from .basic_provider import BasicProvider


class GPTProvider(BasicProvider):
    """GPT LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get GPT chat model instance"""
        return ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.api_base or "https://api.openai.com/v1",
            **self.kwargs
        )
