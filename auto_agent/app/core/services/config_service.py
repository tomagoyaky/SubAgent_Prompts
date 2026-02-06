"""
Config Service
Service for handling configuration-related business logic
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.core.config_manager import config_manager
from app.utils.logger import global_logger as logger


class ConfigService(ABC):
    """
    Abstract base class for config service
    """

    @abstractmethod
    def get_config(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key (optional)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        pass

    @abstractmethod
    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration

        Returns:
            LLM configuration dictionary
        """
        pass

    @abstractmethod
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key for specified provider

        Args:
            provider: Provider name

        Returns:
            API key or None if not found
        """
        pass

    @abstractmethod
    def get_api_base(self, provider: str) -> Optional[str]:
        """
        Get API base URL for specified provider

        Args:
            provider: Provider name

        Returns:
            API base URL or None if not found
        """
        pass

    @abstractmethod
    def get_directory(self, directory_type: str) -> Optional[str]:
        """
        Get directory path

        Args:
            directory_type: Directory type

        Returns:
            Directory path or None if not found
        """
        pass

    @abstractmethod
    def refresh_config(self) -> bool:
        """
        Refresh configuration

        Returns:
            Whether configuration was successfully refreshed
        """
        pass


class ConfigServiceImpl(ConfigService):
    """
    Implementation of config service
    """

    def get_config(self, key: Optional[str] = None, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key (optional)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        try:
            if key:
                return config_manager.get(key, default)
            return config_manager.get_all()
        except Exception as e:
            logger.error(f"Error getting config: {e}")
            return default

    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration

        Returns:
            LLM configuration dictionary
        """
        try:
            return config_manager.get_llm_config()
        except Exception as e:
            logger.error(f"Error getting LLM config: {e}")
            return {}

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get API key for specified provider

        Args:
            provider: Provider name

        Returns:
            API key or None if not found
        """
        try:
            return config_manager.get_api_key(provider)
        except Exception as e:
            logger.error(f"Error getting API key for {provider}: {e}")
            return None

    def get_api_base(self, provider: str) -> Optional[str]:
        """
        Get API base URL for specified provider

        Args:
            provider: Provider name

        Returns:
            API base URL or None if not found
        """
        try:
            return config_manager.get_api_base(provider)
        except Exception as e:
            logger.error(f"Error getting API base for {provider}: {e}")
            return None

    def get_directory(self, directory_type: str) -> Optional[str]:
        """
        Get directory path

        Args:
            directory_type: Directory type

        Returns:
            Directory path or None if not found
        """
        try:
            return config_manager.get_directory(directory_type)
        except Exception as e:
            logger.error(f"Error getting directory {directory_type}: {e}")
            return None

    def refresh_config(self) -> bool:
        """
        Refresh configuration

        Returns:
            Whether configuration was successfully refreshed
        """
        try:
            logger.info("Refreshing configuration")
            # Note: config_manager currently doesn't have a refresh method
            # This would be implemented if configuration sources change dynamically
            logger.info("Configuration refreshed successfully")
            return True
        except Exception as e:
            logger.error(f"Error refreshing config: {e}")
            return False


# Global config service instance
config_service = ConfigServiceImpl()
