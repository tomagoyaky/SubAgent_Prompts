"""
LLM Service
Service for handling LLM-related business logic
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, AsyncGenerator
from app.llms.initializer import initialize_llm_provider
from app.core.dependency_injector import get_dependency
from app.utils.logger import global_logger as logger


class LLMService(ABC):
    """
    Abstract base class for LLM service
    """

    @abstractmethod
    def get_llm_provider(self, model_name: str, **kwargs) -> Optional[Any]:
        """
        Get LLM provider for specified model

        Args:
            model_name: Model name
            **kwargs: Additional model parameters

        Returns:
            LLM provider instance or None if failed
        """
        pass

    @abstractmethod
    async def generate(self, model: Any, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate text using LLM

        Args:
            model: LLM provider instance
            prompt: Prompt text
            **kwargs: Additional generation parameters

        Returns:
            Generated text or None if failed
        """
        pass

    @abstractmethod
    async def stream(self, model: Any, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream text generation using LLM

        Args:
            model: LLM provider instance
            prompt: Prompt text
            **kwargs: Additional generation parameters

        Yields:
            Generated text chunks
        """
        pass

    @abstractmethod
    def get_model_info(self, model: Any) -> Dict[str, Any]:
        """
        Get model information

        Args:
            model: LLM provider instance

        Returns:
            Model information dictionary
        """
        pass


class LLMServiceImpl(LLMService):
    """
    Implementation of LLM service
    """

    def get_llm_provider(self, model_name: str, **kwargs) -> Optional[Any]:
        """
        Get LLM provider for specified model

        Args:
            model_name: Model name
            **kwargs: Additional model parameters

        Returns:
            LLM provider instance or None if failed
        """
        try:
            logger.info(f"Initializing LLM provider for model: {model_name}")
            
            # Get config from dependency injector if available
            config = get_dependency("config")
            if config:
                llm_config = config.get_llm_config()
                # Merge config parameters with kwargs
                merged_kwargs = {
                    "temperature": llm_config.get("temperature", 0.7),
                    "top_p": llm_config.get("top_p", 0.9),
                    "max_tokens": llm_config.get("max_tokens", 2000),
                    "stream_mode": llm_config.get("stream_mode", False),
                    "thinking_mode": llm_config.get("thinking_mode", False),
                    **kwargs
                }
            else:
                merged_kwargs = kwargs
            
            provider = initialize_llm_provider(model_name=model_name, **merged_kwargs)
            
            if provider:
                logger.info(f"Successfully initialized LLM provider for model: {model_name}")
            else:
                logger.error(f"Failed to initialize LLM provider for model: {model_name}")
            
            return provider
        except Exception as e:
            logger.error(f"Error initializing LLM provider: {e}")
            return None

    async def generate(self, model: Any, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate text using LLM

        Args:
            model: LLM provider instance
            prompt: Prompt text
            **kwargs: Additional generation parameters

        Returns:
            Generated text or None if failed
        """
        try:
            if hasattr(model, "generate"):
                result = await model.generate(prompt, **kwargs)
                return result
            elif hasattr(model, "invoke"):
                result = await model.invoke(prompt, **kwargs)
                return result
            else:
                logger.error("Model does not have generate or invoke method")
                return None
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None

    async def stream(self, model: Any, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream text generation using LLM

        Args:
            model: LLM provider instance
            prompt: Prompt text
            **kwargs: Additional generation parameters

        Yields:
            Generated text chunks
        """
        try:
            if hasattr(model, "stream"):
                async for chunk in model.stream(prompt, **kwargs):
                    yield chunk
            else:
                logger.error("Model does not have stream method")
                # Fallback to generate if stream not available
                result = await self.generate(model, prompt, **kwargs)
                if result:
                    yield result
        except Exception as e:
            logger.error(f"Error streaming text: {e}")

    def get_model_info(self, model: Any) -> Dict[str, Any]:
        """
        Get model information

        Args:
            model: LLM provider instance

        Returns:
            Model information dictionary
        """
        try:
            info = {
                "type": type(model).__name__,
                "has_generate": hasattr(model, "generate"),
                "has_stream": hasattr(model, "stream"),
                "has_invoke": hasattr(model, "invoke"),
            }
            
            # Add model-specific information if available
            if hasattr(model, "model_name"):
                info["model_name"] = model.model_name
            elif hasattr(model, "name"):
                info["model_name"] = model.name
            
            return info
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}


# Global LLM service instance
llm_service = LLMServiceImpl()
