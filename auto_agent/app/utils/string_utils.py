"""
String Utils
String operation utilities
"""

import re
from typing import List, Optional


class StringUtils:
    """String utility class"""

    @staticmethod
    def capitalize(text: str) -> str:
        """
        Capitalize string

        Args:
            text: Text to capitalize

        Returns:
            Capitalized text
        """
        return text.capitalize()

    @staticmethod
    def title(text: str) -> str:
        """
        Title case string

        Args:
            text: Text to title case

        Returns:
            Title case text
        """
        return text.title()

    @staticmethod
    def upper(text: str) -> str:
        """
        Uppercase string

        Args:
            text: Text to uppercase

        Returns:
            Uppercase text
        """
        return text.upper()

    @staticmethod
    def lower(text: str) -> str:
        """
        Lowercase string

        Args:
            text: Text to lowercase

        Returns:
            Lowercase text
        """
        return text.lower()

    @staticmethod
    def strip(text: str, chars: Optional[str] = None) -> str:
        """
        Strip whitespace or characters from string

        Args:
            text: Text to strip
            chars: Characters to strip

        Returns:
            Stripped text
        """
        return text.strip(chars)

    @staticmethod
    def lstrip(text: str, chars: Optional[str] = None) -> str:
        """
        Strip whitespace or characters from left of string

        Args:
            text: Text to strip
            chars: Characters to strip

        Returns:
            Left-stripped text
        """
        return text.lstrip(chars)

    @staticmethod
    def rstrip(text: str, chars: Optional[str] = None) -> str:
        """
        Strip whitespace or characters from right of string

        Args:
            text: Text to strip
            chars: Characters to strip

        Returns:
            Right-stripped text
        """
        return text.rstrip(chars)

    @staticmethod
    def split(text: str, sep: Optional[str] = None, maxsplit: int = -1) -> List[str]:
        """
        Split string

        Args:
            text: Text to split
            sep: Separator
            maxsplit: Maximum splits

        Returns:
            List of split parts
        """
        return text.split(sep, maxsplit)

    @staticmethod
    def join(parts: List[str], sep: str = "") -> str:
        """
        Join list of strings

        Args:
            parts: List of strings to join
            sep: Separator

        Returns:
            Joined string
        """
        return sep.join(parts)

    @staticmethod
    def replace(text: str, old: str, new: str, count: int = -1) -> str:
        """
        Replace substring

        Args:
            text: Text to modify
            old: Old substring
            new: New substring
            count: Maximum replacements

        Returns:
            Modified text
        """
        return text.replace(old, new, count)

    @staticmethod
    def find(text: str, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Find substring

        Args:
            text: Text to search
            sub: Substring to find
            start: Start index
            end: End index

        Returns:
            Index of substring or -1 if not found
        """
        return text.find(sub, start, end)

    @staticmethod
    def rfind(text: str, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Reverse find substring

        Args:
            text: Text to search
            sub: Substring to find
            start: Start index
            end: End index

        Returns:
            Last index of substring or -1 if not found
        """
        return text.rfind(sub, start, end)

    @staticmethod
    def contains(text: str, sub: str) -> bool:
        """
        Check if string contains substring

        Args:
            text: Text to check
            sub: Substring to check for

        Returns:
            Whether substring is present
        """
        return sub in text

    @staticmethod
    def starts_with(
        text: str, prefix: str, start: int = 0, end: Optional[int] = None
    ) -> bool:
        """
        Check if string starts with prefix

        Args:
            text: Text to check
            prefix: Prefix to check for
            start: Start index
            end: End index

        Returns:
            Whether string starts with prefix
        """
        return text.startswith(prefix, start, end)

    @staticmethod
    def ends_with(
        text: str, suffix: str, start: int = 0, end: Optional[int] = None
    ) -> bool:
        """
        Check if string ends with suffix

        Args:
            text: Text to check
            suffix: Suffix to check for
            start: Start index
            end: End index

        Returns:
            Whether string ends with suffix
        """
        return text.endswith(suffix, start, end)

    @staticmethod
    def count(text: str, sub: str, start: int = 0, end: Optional[int] = None) -> int:
        """
        Count occurrences of substring

        Args:
            text: Text to search
            sub: Substring to count
            start: Start index
            end: End index

        Returns:
            Number of occurrences
        """
        return text.count(sub, start, end)

    @staticmethod
    def is_alpha(text: str) -> bool:
        """
        Check if string is alphabetic

        Args:
            text: Text to check

        Returns:
            Whether string is alphabetic
        """
        return text.isalpha()

    @staticmethod
    def is_numeric(text: str) -> bool:
        """
        Check if string is numeric

        Args:
            text: Text to check

        Returns:
            Whether string is numeric
        """
        return text.isnumeric()

    @staticmethod
    def is_alphanumeric(text: str) -> bool:
        """
        Check if string is alphanumeric

        Args:
            text: Text to check

        Returns:
            Whether string is alphanumeric
        """
        return text.isalnum()

    @staticmethod
    def is_space(text: str) -> bool:
        """
        Check if string is whitespace

        Args:
            text: Text to check

        Returns:
            Whether string is whitespace
        """
        return text.isspace()

    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate string

        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix for truncated text

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[: max_length - len(suffix)] + suffix

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace

        Args:
            text: Text to normalize

        Returns:
            Text with normalized whitespace
        """
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def slugify(text: str) -> str:
        """
        Slugify string

        Args:
            text: Text to slugify

        Returns:
            Slugified text
        """
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        text = re.sub(r"-+", "-", text)
        return text.strip("-")


# Global instance
string_utils = StringUtils()
