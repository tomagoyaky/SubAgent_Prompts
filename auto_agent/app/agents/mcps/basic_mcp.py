"""
Basic MCP
Master Control Program base class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BasicMCP(ABC):
    """Abstract base class for Master Control Program"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the MCP

        Args:
            name: MCP name
            description: MCP description
            **kwargs: Additional parameters
        """
        self.name = name
        self.description = description
        self.kwargs = kwargs

    @abstractmethod
    def control(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Control function

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Control result
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get MCP information

        Returns:
            MCP information dictionary
        """
        return {"name": self.name, "description": self.description, **self.kwargs}
