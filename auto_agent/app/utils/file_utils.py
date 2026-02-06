"""
File Utils
File operation utilities
"""

import os
import shutil
from typing import Any, List, Optional


class FileUtils:
    """File utility class"""

    @staticmethod
    def read_file(file_path: str, encoding: str = "utf-8") -> Optional[str]:
        """
        Read file content

        Args:
            file_path: File path
            encoding: File encoding

        Returns:
            File content or None if file not found
        """
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except Exception:
            return None

    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Write content to file

        Args:
            file_path: File path
            content: Content to write
            encoding: File encoding

        Returns:
            Whether write was successful
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except Exception:
            return False

    @staticmethod
    def append_file(file_path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Append content to file

        Args:
            file_path: File path
            content: Content to append
            encoding: File encoding

        Returns:
            Whether append was successful
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "a", encoding=encoding) as f:
                f.write(content)
            return True
        except Exception:
            return False

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete file

        Args:
            file_path: File path

        Returns:
            Whether deletion was successful
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False

    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """
        List files in directory

        Args:
            directory: Directory path
            pattern: File pattern

        Returns:
            List of file paths
        """
        try:
            import glob

            search_path = os.path.join(directory, pattern)
            return glob.glob(search_path)
        except Exception:
            return []

    @staticmethod
    def copy_file(src: str, dst: str) -> bool:
        """
        Copy file

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            Whether copy was successful
        """
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            return True
        except Exception:
            return False

    @staticmethod
    def move_file(src: str, dst: str) -> bool:
        """
        Move file

        Args:
            src: Source file path
            dst: Destination file path

        Returns:
            Whether move was successful
        """
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            return True
        except Exception:
            return False

    @staticmethod
    def exists(file_path: str) -> bool:
        """
        Check if file exists

        Args:
            file_path: File path

        Returns:
            Whether file exists
        """
        return os.path.exists(file_path)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size

        Args:
            file_path: File path

        Returns:
            File size in bytes
        """
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0

    @staticmethod
    def get_file_modified_time(file_path: str) -> float:
        """
        Get file modified time

        Args:
            file_path: File path

        Returns:
            Modified time timestamp
        """
        try:
            return os.path.getmtime(file_path)
        except Exception:
            return 0.0


# Global instance
file_utils = FileUtils()
