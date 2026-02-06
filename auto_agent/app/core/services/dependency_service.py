"""
Dependency Service
Service for handling dependency injection-related business logic
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Callable
from app.core.dependency_injector import dependency_injector, register_dependency, register_factory, get_dependency
from app.utils.logger import global_logger as logger


class DependencyService(ABC):
    """
    Abstract base class for dependency service
    """

    @abstractmethod
    def register_dependency(self, name: str, dependency: Any) -> bool:
        """
        Register a dependency

        Args:
            name: Dependency name
            dependency: Dependency instance

        Returns:
            Whether dependency was successfully registered
        """
        pass

    @abstractmethod
    def register_factory(self, name: str, factory: Callable) -> bool:
        """
        Register a dependency factory

        Args:
            name: Dependency name
            factory: Factory function that creates the dependency

        Returns:
            Whether factory was successfully registered
        """
        pass

    @abstractmethod
    def get_dependency(self, name: str) -> Optional[Any]:
        """
        Get a dependency by name

        Args:
            name: Dependency name

        Returns:
            Dependency instance or None if not found
        """
        pass

    @abstractmethod
    def get_all_dependencies(self) -> Dict[str, Any]:
        """
        Get all registered dependencies

        Returns:
            Dictionary of all dependencies
        """
        pass

    @abstractmethod
    def unregister_dependency(self, name: str) -> bool:
        """
        Unregister a dependency

        Args:
            name: Dependency name

        Returns:
            Whether dependency was successfully unregistered
        """
        pass

    @abstractmethod
    def clear_dependencies(self) -> bool:
        """
        Clear all dependencies

        Returns:
            Whether dependencies were successfully cleared
        """
        pass

    @abstractmethod
    def inject_dependencies(self, func: Callable, **kwargs) -> Callable:
        """
        Inject dependencies into a function

        Args:
            func: Function to inject dependencies into
            **kwargs: Additional keyword arguments

        Returns:
            Function with injected dependencies
        """
        pass


class DependencyServiceImpl(DependencyService):
    """
    Implementation of dependency service
    """

    def register_dependency(self, name: str, dependency: Any) -> bool:
        """
        Register a dependency

        Args:
            name: Dependency name
            dependency: Dependency instance

        Returns:
            Whether dependency was successfully registered
        """
        try:
            register_dependency(name, dependency)
            return True
        except Exception as e:
            logger.error(f"Error registering dependency {name}: {e}")
            return False

    def register_factory(self, name: str, factory: Callable) -> bool:
        """
        Register a dependency factory

        Args:
            name: Dependency name
            factory: Factory function that creates the dependency

        Returns:
            Whether factory was successfully registered
        """
        try:
            register_factory(name, factory)
            return True
        except Exception as e:
            logger.error(f"Error registering factory {name}: {e}")
            return False

    def get_dependency(self, name: str) -> Optional[Any]:
        """
        Get a dependency by name

        Args:
            name: Dependency name

        Returns:
            Dependency instance or None if not found
        """
        try:
            return get_dependency(name)
        except Exception as e:
            logger.error(f"Error getting dependency {name}: {e}")
            return None

    def get_all_dependencies(self) -> Dict[str, Any]:
        """
        Get all registered dependencies

        Returns:
            Dictionary of all dependencies
        """
        try:
            return dependency_injector.get_all()
        except Exception as e:
            logger.error(f"Error getting all dependencies: {e}")
            return {}

    def unregister_dependency(self, name: str) -> bool:
        """
        Unregister a dependency

        Args:
            name: Dependency name

        Returns:
            Whether dependency was successfully unregistered
        """
        try:
            return dependency_injector.unregister(name)
        except Exception as e:
            logger.error(f"Error unregistering dependency {name}: {e}")
            return False

    def clear_dependencies(self) -> bool:
        """
        Clear all dependencies

        Returns:
            Whether dependencies were successfully cleared
        """
        try:
            dependency_injector.clear()
            return True
        except Exception as e:
            logger.error(f"Error clearing dependencies: {e}")
            return False

    def inject_dependencies(self, func: Callable, **kwargs) -> Callable:
        """
        Inject dependencies into a function

        Args:
            func: Function to inject dependencies into
            **kwargs: Additional keyword arguments

        Returns:
            Function with injected dependencies
        """
        try:
            def wrapper(*args, **wrap_kwargs):
                # Combine kwargs
                combined_kwargs = {**kwargs, **wrap_kwargs}
                
                # Inject dependencies
                for name, _ in combined_kwargs.items():
                    dependency = get_dependency(name)
                    if dependency:
                        combined_kwargs[name] = dependency
                
                return func(*args, **combined_kwargs)
            
            return wrapper
        except Exception as e:
            logger.error(f"Error injecting dependencies: {e}")
            return func


# Global dependency service instance
dependency_service = DependencyServiceImpl()
