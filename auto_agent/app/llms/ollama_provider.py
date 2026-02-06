"""
Ollama Provider
Implementation for Ollama local models
"""

from typing import Any, Iterator

from langchain_ollama import ChatOllama

from .basic_provider import BasicProvider


class OllamaProvider(BasicProvider):
    """Ollama LLM provider"""

    def _get_chat_model(self) -> Any:
        """Get Ollama chat model instance"""
        return ChatOllama(
            model=self.model_name,
            base_url=self.api_base or "http://localhost:11434",
            **self.kwargs
        )
