"""
Dependency Injector
Centralized dependency management system
"""

from typing import Dict, Any, Optional, Callable
from app.utils.logger import global_logger as logger


class DependencyInjector:
    """
    Dependency injection container for managing and providing dependencies
    """

    def __init__(self):
        """
        Initialize dependency injector
        """
        self._dependencies: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}

    def register(self, name: str, dependency: Any):
        """
        Register a dependency

        Args:
            name: Dependency name
            dependency: Dependency instance
        """
        self._dependencies[name] = dependency
        logger.info(f"Registered dependency: {name}")

    def register_factory(self, name: str, factory: Callable):
        """
        Register a dependency factory

        Args:
            name: Dependency name
            factory: Factory function that creates the dependency
        """
        self._factories[name] = factory
        logger.info(f"Registered dependency factory: {name}")

    def get(self, name: str) -> Optional[Any]:
        """
        Get a dependency by name

        Args:
            name: Dependency name

        Returns:
            Dependency instance or None if not found
        """
        # First check if dependency is already registered
        if name in self._dependencies:
            return self._dependencies[name]

        # If not found, check if there's a factory
        if name in self._factories:
            try:
                dependency = self._factories[name]()
                self._dependencies[name] = dependency
                logger.info(f"Created dependency from factory: {name}")
                return dependency
            except Exception as e:
                logger.error(f"Error creating dependency {name}: {e}")
                return None

        logger.warning(f"Dependency not found: {name}")
        return None

    def get_all(self) -> Dict[str, Any]:
        """
        Get all registered dependencies

        Returns:
            Dictionary of all dependencies
        """
        return self._dependencies

    def unregister(self, name: str) -> bool:
        """
        Unregister a dependency

        Args:
            name: Dependency name

        Returns:
            Whether dependency was successfully unregistered
        """
        if name in self._dependencies:
            del self._dependencies[name]
            logger.info(f"Unregistered dependency: {name}")
            return True
        if name in self._factories:
            del self._factories[name]
            logger.info(f"Unregistered dependency factory: {name}")
            return True
        return False

    def clear(self):
        """
        Clear all dependencies
        """
        self._dependencies.clear()
        self._factories.clear()
        logger.info("Cleared all dependencies")


# Global dependency injector instance
dependency_injector = DependencyInjector()


# Helper functions for easy dependency management
def register_dependency(name: str, dependency: Any):
    """
    Register a dependency

    Args:
        name: Dependency name
        dependency: Dependency instance
    """
    dependency_injector.register(name, dependency)


def register_factory(name: str, factory: Callable):
    """
    Register a dependency factory

    Args:
        name: Dependency name
        factory: Factory function that creates the dependency
    """
    dependency_injector.register_factory(name, factory)


def get_dependency(name: str) -> Optional[Any]:
    """
    Get a dependency by name

    Args:
        name: Dependency name

    Returns:
        Dependency instance or None if not found
    """
    return dependency_injector.get(name)


def inject_dependency(name: str):
    """
    Decorator for dependency injection

    Args:
        name: Dependency name

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        import asyncio
        if asyncio.iscoroutinefunction(func):
            async def async_wrapper(*args, **kwargs):
                dependency = get_dependency(name)
                if dependency:
                    kwargs[name] = dependency
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            def sync_wrapper(*args, **kwargs):
                dependency = get_dependency(name)
                if dependency:
                    kwargs[name] = dependency
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator
