"""
Tool Registry
Centralized tool registration and management system
"""

from typing import Callable, Dict, List, Any, Optional
from langchain_core.tools import tool
from ..utils.logger import global_logger as logger


class ToolRegistry:
    """
    Centralized tool registration and management class
    """

    def __init__(self):
        """
        Initialize tool registry
        """
        self._tools: Dict[str, Callable] = {}
        self._tool_info: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, func: Callable, description: str, **kwargs):
        """
        Register a tool

        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            **kwargs: Additional tool information
        """
        # Create tool wrapper with langchain tool decorator
        @tool
        async def tool_wrapper(*args, **kwargs):
            """Tool wrapper function"""
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return f"Error executing tool {name}: {str(e)}"

        # Update function metadata
        tool_wrapper.__name__ = name
        tool_wrapper.__doc__ = description

        # Register tool
        self._tools[name] = tool_wrapper
        self._tool_info[name] = {
            "description": description,
            **kwargs
        }

        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get tool by name

        Args:
            name: Tool name

        Returns:
            Tool function or None if not found
        """
        return self._tools.get(name)

    def get_all_tools(self) -> List[Callable]:
        """
        Get all registered tools

        Returns:
            List of tool functions
        """
        return list(self._tools.values())

    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool information

        Args:
            name: Tool name

        Returns:
            Tool information or None if not found
        """
        return self._tool_info.get(name)

    def get_all_tool_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information for all tools

        Returns:
            Dictionary of tool information
        """
        return self._tool_info

    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool

        Args:
            name: Tool name

        Returns:
            Whether tool was successfully unregistered
        """
        if name in self._tools:
            del self._tools[name]
            del self._tool_info[name]
            logger.info(f"Unregistered tool: {name}")
            return True
        return False

    def clear_tools(self):
        """
        Clear all registered tools
        """
        self._tools.clear()
        self._tool_info.clear()
        logger.info("Cleared all registered tools")


# Global tool registry instance
tool_registry = ToolRegistry()


# Helper function for easy tool registration
def register_tool(name: str, description: str, **kwargs):
    """
    Decorator for tool registration

    Args:
        name: Tool name
        description: Tool description
        **kwargs: Additional tool information

    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        tool_registry.register_tool(name, func, description, **kwargs)
        return func
    return decorator
