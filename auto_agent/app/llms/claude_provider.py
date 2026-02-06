"""
Claude Provider
Implementation for Anthropic Claude models
"""

from typing import Any, Iterator

from langchain_anthropic import ChatAnthropic

from .basic_provider import BasicProvider


class ClaudeProvider(BasicProvider):
    """Claude LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get Claude chat model instance"""
        return ChatAnthropic(
            model=self.model_name,
            api_key=self.api_key,
            base_url=self.api_base or "https://api.anthropic.com/v1",
            **self.kwargs
        )

    def _prepare_messages(self, user_input: str, system_prompt: str, **kwargs) -> tuple:
        """Prepare messages for Claude chat model"""
        messages = [{"role": "user", "content": user_input}]
        kwargs["system"] = system_prompt
        return messages, kwargs
