"""
Config
Configuration management
"""

import os
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from .utils.logger import global_logger as logger


class Config:
    """Configuration management class"""

    def __init__(self):
        """
        Initialize configuration
        """
        # Load environment variables
        load_dotenv()

        # Load YAML configuration
        self.config_data = self._load_config()

        # Get current environment
        self.current_env = self.config_data.get('environment', 'dev')

        # Load environment-specific configuration
        self.env_config = self.config_data.get('environments', {}).get(self.current_env, {})

        # Merge with environment variables
        self._merge_with_env()
        
        # Initialize configuration cache
        self._cache = {}

    def clear_cache(self):
        """
        Clear configuration cache
        """
        self._cache.clear()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file

        Returns:
            Configuration data
        """
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config.yaml"
        )
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logger.warning(
                f"Configuration file not found at {config_path}, using default configuration"
            )
            return {}
        except yaml.YAMLError as e:
            logger.warning(
                f"Error parsing YAML configuration: {e}, using default configuration"
            )
            return {}
        except Exception as e:
            logger.warning(
                f"Unexpected error loading configuration: {e}, using default configuration"
            )
            return {}

    def _merge_with_env(self):
        """
        Merge configuration with environment variables
        """
        # LLM API keys
        llm_config = self.config_data.get("llm", {})

        # Update API keys from environment
        api_keys = {
            "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY"),
            "glm_api_key": os.getenv("GLM_API_KEY"),
            "qwen_api_key": os.getenv("QWEN_API_KEY"),
            "doubao_api_key": os.getenv("DOUBAO_API_KEY"),
            "kimi_api_key": os.getenv("KIMI_API_KEY"),
            "minipro_api_key": os.getenv("MINIPRO_API_KEY"),
            "gpt_api_key": os.getenv("GPT_API_KEY"),
            "claude_api_key": os.getenv("CLAUDE_API_KEY"),
        }

        # Update API bases from environment
        api_bases = {
            "deepseek_api_base": os.getenv("DEEPSEEK_API_BASE"),
            "glm_api_base": os.getenv("GLM_API_BASE"),
            "qwen_api_base": os.getenv("QWEN_API_BASE"),
            "doubao_api_base": os.getenv("DOUBAO_API_BASE"),
            "kimi_api_base": os.getenv("KIMI_API_BASE"),
            "minipro_api_base": os.getenv("MINIPRO_API_BASE"),
            "gpt_api_base": os.getenv("GPT_API_BASE"),
            "claude_api_base": os.getenv("CLAUDE_API_BASE"),
        }

        # Update configuration
        for key, value in api_keys.items():
            if value:
                llm_config[key] = value

        for key, value in api_bases.items():
            if value:
                llm_config[key] = value

        # Update default model
        default_model = os.getenv("DEFAULT_MODEL")
        if default_model:
            llm_config["default_model"] = default_model

        # Update log level
        log_level = os.getenv("LOG_LEVEL")
        if log_level:
            log_config = self.config_data.get("log", {})
            log_config["level"] = log_level
            self.config_data["log"] = log_config

        # Update workspace directory
        workspace_dir = os.getenv("WORKSPACE_DIR")
        if workspace_dir:
            dir_config = self.config_data.get("directories", {})
            dir_config["workspace"] = workspace_dir
            self.config_data["directories"] = dir_config

        self.config_data["llm"] = llm_config

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            path: Configuration path (e.g., "llm.default_model")
            default: Default value if not found

        Returns:
            Configuration value
        """
        # Check cache first
        cache_key = f"{path}:{default}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        parts = path.split(".")

        # First check environment-specific configuration
        result = self.env_config
        for part in parts:
            if isinstance(result, dict) and part in result:
                result = result[part]
            else:
                # Fallback to general configuration
                result = self.config_data
                for part in parts:
                    if isinstance(result, dict) and part in result:
                        result = result[part]
                    else:
                        # Cache the default value
                        self._cache[cache_key] = default
                        return default
                # Cache the result
                self._cache[cache_key] = result
                return result

        # Cache the result
        self._cache[cache_key] = result
        return result

    def set(self, path: str, value: Any) -> bool:
        """
        Set configuration value

        Args:
            path: Configuration path (e.g., "llm.default_model")
            value: Value to set

        Returns:
            Whether set was successful
        """
        try:
            if not path or not isinstance(path, str):
                logger.error("Configuration path must be a non-empty string")
                return False

            parts = path.split(".")
            if not parts:
                logger.error("Configuration path is empty")
                return False

            result = self.config_data

            for part in parts[:-1]:
                if part not in result:
                    result[part] = {}
                elif not isinstance(result[part], dict):
                    logger.error(
                        f"Cannot set nested configuration at '{part}' - it is not a dictionary"
                    )
                    return False
                result = result[part]

            result[parts[-1]] = value
            # Clear cache to ensure fresh values are returned
            self.clear_cache()
            return True
        except ValueError as e:
            logger.error(f"Invalid value for configuration: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error setting configuration: {e}")
            return False

    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration

        Returns:
            LLM configuration
        """
        return self.env_config.get("llm", self.config_data.get("llm", {}))

    def get_agent_config(self) -> Dict[str, Any]:
        """
        Get agent configuration

        Returns:
            Agent configuration
        """
        return self.env_config.get("agent", self.config_data.get("agent", {}))

    def get_log_config(self) -> Dict[str, Any]:
        """
        Get log configuration

        Returns:
            Log configuration
        """
        return self.env_config.get("log", self.config_data.get("log", {}))

    def get_directory_config(self) -> Dict[str, Any]:
        """
        Get directory configuration

        Returns:
            Directory configuration
        """
        return self.env_config.get(
            "directories", self.config_data.get("directories", {})
        )

    def get_api_config(self) -> Dict[str, Any]:
        """
        Get API configuration

        Returns:
            API configuration
        """
        return self.env_config.get("api", self.config_data.get("api", {}))

    def get_environment(self) -> str:
        """
        Get current environment

        Returns:
            Current environment name
        """
        return self.current_env

    def save(self, file_path: Optional[str] = None) -> bool:
        """
        Save configuration to file

        Args:
            file_path: File path to save to

        Returns:
            Whether save was successful
        """
        if file_path is None:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "config.yaml"
            )

        try:
            # Ensure directory exists
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.config_data, f, default_flow_style=False, allow_unicode=True
                )
            return True
        except FileNotFoundError:
            logger.error(
                f"Directory not found for configuration file: {os.path.dirname(file_path)}"
            )
            return False
        except PermissionError:
            logger.error(f"Permission denied when saving configuration to {file_path}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error saving configuration: {e}")
            return False


# Global config instance
config = Config()
