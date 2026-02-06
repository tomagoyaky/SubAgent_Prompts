"""
Base64 Utils
Base64 encoding and decoding utilities
"""

import base64
from typing import Optional


class Base64Utils:
    """Base64 utility class"""

    @staticmethod
    def encode_string(text: str) -> str:
        """
        Base64 encode string

        Args:
            text: String to encode

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_string(encoded_text: str) -> Optional[str]:
        """
        Base64 decode string

        Args:
            encoded_text: Base64 encoded string

        Returns:
            Decoded string or None if error
        """
        try:
            return base64.b64decode(encoded_text).decode("utf-8")
        except Exception:
            return None

    @staticmethod
    def encode_bytes(data: bytes) -> str:
        """
        Base64 encode bytes

        Args:
            data: Bytes to encode

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def decode_bytes(encoded_text: str) -> Optional[bytes]:
        """
        Base64 decode to bytes

        Args:
            encoded_text: Base64 encoded string

        Returns:
            Decoded bytes or None if error
        """
        try:
            return base64.b64decode(encoded_text)
        except Exception:
            return None

    @staticmethod
    def encode_urlsafe_string(text: str) -> str:
        """
        URL-safe Base64 encode string

        Args:
            text: String to encode

        Returns:
            URL-safe Base64 encoded string
        """
        return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def decode_urlsafe_string(encoded_text: str) -> Optional[str]:
        """
        URL-safe Base64 decode string

        Args:
            encoded_text: URL-safe Base64 encoded string

        Returns:
            Decoded string or None if error
        """
        try:
            return base64.urlsafe_b64decode(encoded_text).decode("utf-8")
        except Exception:
            return None

    @staticmethod
    def encode_file(file_path: str) -> Optional[str]:
        """
        Base64 encode file

        Args:
            file_path: File path

        Returns:
            Base64 encoded string or None if error
        """
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return None

    @staticmethod
    def decode_file(encoded_text: str, output_path: str) -> bool:
        """
        Base64 decode to file

        Args:
            encoded_text: Base64 encoded string
            output_path: Output file path

        Returns:
            Whether decode was successful
        """
        try:
            # Ensure directory exists
            import os

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(encoded_text))
            return True
        except Exception:
            return False


# Global instance
base64_utils = Base64Utils()
