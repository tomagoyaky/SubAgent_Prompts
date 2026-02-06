"""
Basic Storage
Storage management base class
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BasicStorage(ABC):
    """Abstract base class for storage management"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the storage

        Args:
            name: Storage name
            description: Storage description
            **kwargs: Additional parameters
        """
        self.name = name
        self.description = description
        self.kwargs = kwargs

    @abstractmethod
    def save(self, path: str, data: Any, **kwargs) -> bool:
        """
        Save data to storage

        Args:
            path: Storage path
            data: Data to save
            **kwargs: Additional parameters

        Returns:
            Whether save was successful
        """
        pass

    @abstractmethod
    def load(self, path: str, **kwargs) -> Optional[Any]:
        """
        Load data from storage

        Args:
            path: Storage path
            **kwargs: Additional parameters

        Returns:
            Loaded data or None if not found
        """
        pass

    @abstractmethod
    def delete(self, path: str, **kwargs) -> bool:
        """
        Delete data from storage

        Args:
            path: Storage path
            **kwargs: Additional parameters

        Returns:
            Whether deletion was successful
        """
        pass

    @abstractmethod
    def exists(self, path: str, **kwargs) -> bool:
        """
        Check if path exists in storage

        Args:
            path: Storage path
            **kwargs: Additional parameters

        Returns:
            Whether path exists
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """
        Get storage information

        Returns:
            Storage information dictionary
        """
        return {"name": self.name, "description": self.description, **self.kwargs}
