"""
JSON Utils
JSON operation utilities
"""

import json
from typing import Any, Dict, List, Optional


class JSONUtils:
    """JSON utility class"""

    @staticmethod
    def load_json(file_path: str) -> Optional[Any]:
        """
        Load JSON from file

        Args:
            file_path: File path

        Returns:
            JSON data or None if error
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    @staticmethod
    def dump_json(file_path: str, data: Any, indent: int = 2) -> bool:
        """
        Dump JSON to file

        Args:
            file_path: File path
            data: Data to dump
            indent: Indentation level

        Returns:
            Whether dump was successful
        """
        try:
            # Ensure directory exists
            import os

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception:
            return False

    @staticmethod
    def loads_json(json_str: str) -> Optional[Any]:
        """
        Load JSON from string

        Args:
            json_str: JSON string

        Returns:
            JSON data or None if error
        """
        try:
            return json.loads(json_str)
        except Exception:
            return None

    @staticmethod
    def dumps_json(data: Any, indent: int = 2) -> Optional[str]:
        """
        Dump JSON to string

        Args:
            data: Data to dump
            indent: Indentation level

        Returns:
            JSON string or None if error
        """
        try:
            return json.dumps(data, indent=indent, ensure_ascii=False)
        except Exception:
            return None

    @staticmethod
    def validate_json(json_str: str) -> bool:
        """
        Validate JSON string

        Args:
            json_str: JSON string

        Returns:
            Whether JSON is valid
        """
        try:
            json.loads(json_str)
            return True
        except Exception:
            return False

    @staticmethod
    def get_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
        """
        Get nested value from JSON data

        Args:
            data: JSON data
            path: Path to value (e.g., "a.b.c")
            default: Default value if not found

        Returns:
            Retrieved value or default
        """
        try:
            parts = path.split(".")
            result = data
            for part in parts:
                result = result[part]
            return result
        except Exception:
            return default

    @staticmethod
    def set_nested_value(data: Dict[str, Any], path: str, value: Any) -> bool:
        """
        Set nested value in JSON data

        Args:
            data: JSON data
            path: Path to value (e.g., "a.b.c")
            value: Value to set

        Returns:
            Whether set was successful
        """
        try:
            parts = path.split(".")
            result = data
            for part in parts[:-1]:
                if part not in result:
                    result[part] = {}
                result = result[part]
            result[parts[-1]] = value
            return True
        except Exception:
            return False

    @staticmethod
    def merge_json(data1: Dict[str, Any], data2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two JSON objects

        Args:
            data1: First JSON object
            data2: Second JSON object

        Returns:
            Merged JSON object
        """
        try:
            result = data1.copy()
            for key, value in data2.items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(value, dict)
                ):
                    result[key] = JSONUtils.merge_json(result[key], value)
                else:
                    result[key] = value
            return result
        except Exception:
            return data1


# Global instance
json_utils = JSONUtils()
