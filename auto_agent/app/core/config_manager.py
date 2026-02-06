"""
Config Manager
Centralized configuration management module
"""

from typing import Any, Dict, Optional
from ..config import config
from ..utils.logger import global_logger as logger


class ConfigManager:
    """
    Centralized configuration management class
    """

    # Configuration sections
    SECTIONS = {
        "LLM": "llm",
        "AGENT": "agent",
        "LOG": "log",
        "DIRECTORIES": "directories",
        "API": "api"
    }

    # Common configuration keys
    LLM_KEYS = {
        "DEFAULT_MODEL": "default_model",
        "STREAM_MODE": "stream_mode",
        "THINKING_MODE": "thinking_mode",
        "TEMPERATURE": "temperature",
        "TOP_P": "top_p",
        "MAX_TOKENS": "max_tokens",
        "API_KEYS": {
            "DEEPSEEK": "deepseek_api_key",
            "GLM": "glm_api_key",
            "QWEN": "qwen_api_key",
            "DOUBAO": "doubao_api_key",
            "KIMI": "kimi_api_key",
            "MINIPRO": "minipro_api_key",
            "GPT": "gpt_api_key",
            "CLAUDE": "claude_api_key"
        },
        "API_BASES": {
            "DEEPSEEK": "deepseek_api_base",
            "GLM": "glm_api_base",
            "QWEN": "qwen_api_base",
            "DOUBAO": "doubao_api_base",
            "KIMI": "kimi_api_base",
            "MINIPRO": "minipro_api_base",
            "GPT": "gpt_api_base",
            "CLAUDE": "claude_api_base"
        }
    }

    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """
        Get LLM configuration

        Returns:
            LLM configuration dictionary
        """
        return config.get_llm_config()

    @classmethod
    def get_agent_config(cls) -> Dict[str, Any]:
        """
        Get agent configuration

        Returns:
            Agent configuration dictionary
        """
        return config.get_agent_config()

    @classmethod
    def get_log_config(cls) -> Dict[str, Any]:
        """
        Get log configuration

        Returns:
            Log configuration dictionary
        """
        return config.get_log_config()

    @classmethod
    def get_directory_config(cls) -> Dict[str, Any]:
        """
        Get directory configuration

        Returns:
            Directory configuration dictionary
        """
        return config.get_directory_config()

    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """
        Get API configuration

        Returns:
            API configuration dictionary
        """
        return config.get_api_config()

    @classmethod
    def get_llm_setting(cls, key: str, default: Any = None) -> Any:
        """
        Get specific LLM setting

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value
        """
        llm_config = cls.get_llm_config()
        return llm_config.get(key, default)

    @classmethod
    def get_directory_path(cls, key: str, default: str = ".") -> str:
        """
        Get directory path

        Args:
            key: Directory key
            default: Default path if not found

        Returns:
            Directory path
        """
        dir_config = cls.get_directory_config()
        return dir_config.get(key, default)

    @classmethod
    def get_api_key(cls, provider: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get API key for specific provider

        Args:
            provider: Provider name
            default: Default value if not found

        Returns:
            API key
        """
        api_key_key = cls.LLM_KEYS["API_KEYS"].get(provider.upper())
        if not api_key_key:
            logger.warning(f"Unknown provider: {provider}")
            return default
        return config.get(f"llm.{api_key_key}", default)

    @classmethod
    def get_api_base(cls, provider: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get API base URL for specific provider

        Args:
            provider: Provider name
            default: Default value if not found

        Returns:
            API base URL
        """
        api_base_key = cls.LLM_KEYS["API_BASES"].get(provider.upper())
        if not api_base_key:
            logger.warning(f"Unknown provider: {provider}")
            return default
        return config.get(f"llm.{api_base_key}", default)

    @classmethod
    def get_environment(cls) -> str:
        """
        Get current environment

        Returns:
            Environment name
        """
        return config.get_environment()

    @classmethod
    def set_config(cls, path: str, value: Any) -> bool:
        """
        Set configuration value

        Args:
            path: Configuration path
            value: Value to set

        Returns:
            Whether set was successful
        """
        return config.set(path, value)

    @classmethod
    def save_config(cls, file_path: Optional[str] = None) -> bool:
        """
        Save configuration to file

        Args:
            file_path: File path to save to

        Returns:
            Whether save was successful
        """
        return config.save(file_path)


# Global config manager instance
config_manager = ConfigManager()
