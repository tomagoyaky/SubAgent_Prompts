"""
LLM Initializer
Responsible for initializing LLM providers
"""

from typing import Any, Optional

from ..config import config
from ..utils.logger import global_logger as logger
from .provider_factory import ProviderFactory


def initialize_llm_provider(model_name: str, **kwargs) -> Optional[Any]:
    """
    Initialize LLM provider

    Args:
        model_name: Model name
        **kwargs: Additional parameters

    Returns:
        LLM provider instance or None if error
    """
    try:
        # Extract provider name from model name
        provider_name = model_name

        # Handle special cases
        if model_name.startswith("ollama/"):
            provider_name = "ollama"
            kwargs["model_name"] = model_name.split("/")[1]
        elif model_name.startswith("gpt") or model_name.startswith("openai"):
            provider_name = "gpt"
        elif "-" in model_name:
            provider_name = model_name.split("-")[0]

        # Get API configuration based on provider
        api_key_key = f"llm.{provider_name}_api_key"
        api_base_key = f"llm.{provider_name}_api_base"

        # Add API credentials to kwargs if not provided
        if "api_key" not in kwargs:
            kwargs["api_key"] = config.get(api_key_key)
        if "api_base" not in kwargs:
            kwargs["api_base"] = config.get(api_base_key)

        # Add model name to kwargs if not already set
        if "model_name" not in kwargs:
            kwargs["model_name"] = model_name

        # Use ProviderFactory to create the provider
        return ProviderFactory.create_provider(provider_name, **kwargs)
    except Exception as e:
        logger.error(f"Error initializing LLM provider: {e}")
        return None
