"""
Tool Service
Service for handling tool-related business logic
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Callable
from app.core.tool_registry import tool_registry, register_tool
from app.agents.tools.basic_tool import get_all_tools
from app.utils.logger import global_logger as logger


class ToolService(ABC):
    """
    Abstract base class for tool service
    """

    @abstractmethod
    def register_tool(self, name: str, func: Callable, description: str, **kwargs) -> bool:
        """
        Register a tool

        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            **kwargs: Additional tool information

        Returns:
            Whether tool was successfully registered
        """
        pass

    @abstractmethod
    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get tool by name

        Args:
            name: Tool name

        Returns:
            Tool function or None if not found
        """
        pass

    @abstractmethod
    def get_all_tools(self) -> List[Callable]:
        """
        Get all registered tools

        Returns:
            List of tool functions
        """
        pass

    @abstractmethod
    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool information

        Args:
            name: Tool name

        Returns:
            Tool information dictionary or None if not found
        """
        pass

    @abstractmethod
    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool

        Args:
            name: Tool name

        Returns:
            Whether tool was successfully unregistered
        """
        pass

    @abstractmethod
    async def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """
        Execute a tool

        Args:
            tool_name: Tool name
            *args: Tool arguments
            **kwargs: Tool keyword arguments

        Returns:
            Tool execution result
        """
        pass


class ToolServiceImpl(ToolService):
    """
    Implementation of tool service
    """

    def register_tool(self, name: str, func: Callable, description: str, **kwargs) -> bool:
        """
        Register a tool

        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            **kwargs: Additional tool information

        Returns:
            Whether tool was successfully registered
        """
        try:
            tool_registry.register_tool(name, func, description, **kwargs)
            return True
        except Exception as e:
            logger.error(f"Error registering tool {name}: {e}")
            return False

    def get_tool(self, name: str) -> Optional[Callable]:
        """
        Get tool by name

        Args:
            name: Tool name

        Returns:
            Tool function or None if not found
        """
        try:
            tool = tool_registry.get_tool(name)
            if not tool:
                logger.warning(f"Tool not found: {name}")
            return tool
        except Exception as e:
            logger.error(f"Error getting tool {name}: {e}")
            return None

    def get_all_tools(self) -> List[Callable]:
        """
        Get all registered tools

        Returns:
            List of tool functions
        """
        try:
            # First try to get tools from registry
            registry_tools = tool_registry.get_all_tools()
            if registry_tools:
                return registry_tools
            # Fallback to get_all_tools function
            return get_all_tools()
        except Exception as e:
            logger.error(f"Error getting all tools: {e}")
            return []

    def get_tool_info(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get tool information

        Args:
            name: Tool name

        Returns:
            Tool information dictionary or None if not found
        """
        try:
            info = tool_registry.get_tool_info(name)
            if not info:
                logger.warning(f"Tool info not found: {name}")
            return info
        except Exception as e:
            logger.error(f"Error getting tool info {name}: {e}")
            return None

    def unregister_tool(self, name: str) -> bool:
        """
        Unregister a tool

        Args:
            name: Tool name

        Returns:
            Whether tool was successfully unregistered
        """
        try:
            return tool_registry.unregister_tool(name)
        except Exception as e:
            logger.error(f"Error unregistering tool {name}: {e}")
            return False

    async def execute_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """
        Execute a tool

        Args:
            tool_name: Tool name
            *args: Tool arguments
            **kwargs: Tool keyword arguments

        Returns:
            Tool execution result
        """
        try:
            # Validate tool name
            if not tool_name or not isinstance(tool_name, str):
                return "Error: Invalid tool name"
            
            tool = self.get_tool(tool_name)
            if not tool:
                return f"Error: Tool '{tool_name}' not found"
            
            # Validate tool is callable
            if not callable(tool):
                return f"Error: Tool '{tool_name}' is not callable"
            
            result = await tool(*args, **kwargs)
            return result
        except TypeError as e:
            logger.error(f"Type error executing tool {tool_name}: {e}")
            return f"Error executing tool {tool_name}: Invalid arguments - {str(e)}"
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return f"Error executing tool {tool_name}: {str(e)}"


# Global tool service instance
tool_service = ToolServiceImpl()
