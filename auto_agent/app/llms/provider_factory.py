"""
Provider Factory
Factory class for creating LLM providers
"""

from typing import Any, Dict, Optional

from app.llms.basic_provider import BasicProvider
from app.llms.claude_provider import ClaudeProvider
from app.llms.deepseek_provider import DeepSeekProvider
from app.llms.doubao_provider import DoubaoProvider
from app.llms.glm_provider import GLMProvider
from app.llms.gpt_provider import GPTProvider
from app.llms.kimi_provider import KimiProvider
from app.llms.minipro_provider import MiniProProvider
from app.llms.ollama_provider import OllamaProvider
from app.llms.qwen_provider import QwenProvider


class ProviderFactory:
    """
    Factory class for creating LLM providers
    """

    # Mapping of provider names to their respective classes
    PROVIDERS = {
        "basic": BasicProvider,
        "gpt": GPTProvider,
        "claude": ClaudeProvider,
        "deepseek": DeepSeekProvider,
        "doubao": DoubaoProvider,
        "glm": GLMProvider,
        "kimi": KimiProvider,
        "minipro": MiniProProvider,
        "ollama": OllamaProvider,
        "qwen": QwenProvider,
    }

    @classmethod
    def create_provider(cls, provider_name: str, **kwargs) -> Optional[BasicProvider]:
        """
        Create a provider instance based on the provider name

        Args:
            provider_name: Name of the provider to create
            **kwargs: Additional parameters for the provider

        Returns:
            An instance of the requested provider, or None if the provider doesn't exist
        """
        # Normalize provider name
        normalized_name = provider_name.lower()

        # Handle model names like "deepseek-chat" by extracting the provider part
        if "-" in normalized_name:
            normalized_name = normalized_name.split("-")[0]

        provider_class = cls.PROVIDERS.get(normalized_name)
        if provider_class:
            return provider_class(**kwargs)
        return None

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of available provider names

        Returns:
            List of available provider names
        """
        return list(cls.PROVIDERS.keys())

    @classmethod
    def is_provider_available(cls, provider_name: str) -> bool:
        """
        Check if a provider is available

        Args:
            provider_name: Name of the provider to check

        Returns:
            True if the provider is available, False otherwise
        """
        return provider_name.lower() in cls.PROVIDERS
