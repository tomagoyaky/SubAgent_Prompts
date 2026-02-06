"""
Basic Memory
Memory management base class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BasicMemory(ABC):
    """Abstract base class for memory management"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the memory

        Args:
            name: Memory name
            description: Memory description
            **kwargs: Additional parameters
        """
        self.name = name
        self.description = description
        self.kwargs = kwargs

    @abstractmethod
    def store(self, key: str, value: Any, **kwargs) -> bool:
        """
        Store data in memory

        Args:
            key: Storage key
            value: Data to store
            **kwargs: Additional parameters

        Returns:
            Whether storage was successful
        """
        pass

    @abstractmethod
    def retrieve(self, key: str, **kwargs) -> Optional[Any]:
        """
        Retrieve data from memory

        Args:
            key: Storage key
            **kwargs: Additional parameters

        Returns:
            Retrieved data or None if not found
        """
        pass

    @abstractmethod
    def delete(self, key: str, **kwargs) -> bool:
        """
        Delete data from memory

        Args:
            key: Storage key
            **kwargs: Additional parameters

        Returns:
            Whether deletion was successful
        """
        pass

    @abstractmethod
    def clear(self, **kwargs) -> bool:
        """
        Clear all data from memory

        Args:
            **kwargs: Additional parameters

        Returns:
            Whether clearing was successful
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get memory information

        Returns:
            Memory information dictionary
        """
        return {"name": self.name, "description": self.description, **self.kwargs}
