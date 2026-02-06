"""
Crypto Utils
Cryptography utilities
"""

import base64
import hashlib
from typing import Optional


class CryptoUtils:
    """Cryptography utility class"""

    @staticmethod
    def md5_hash(data: str) -> str:
        """
        Generate MD5 hash

        Args:
            data: Data to hash

        Returns:
            MD5 hash string
        """
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    @staticmethod
    def sha1_hash(data: str) -> str:
        """
        Generate SHA1 hash

        Args:
            data: Data to hash

        Returns:
            SHA1 hash string
        """
        return hashlib.sha1(data.encode("utf-8")).hexdigest()

    @staticmethod
    def sha256_hash(data: str) -> str:
        """
        Generate SHA256 hash

        Args:
            data: Data to hash

        Returns:
            SHA256 hash string
        """
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def sha512_hash(data: str) -> str:
        """
        Generate SHA512 hash

        Args:
            data: Data to hash

        Returns:
            SHA512 hash string
        """
        return hashlib.sha512(data.encode("utf-8")).hexdigest()

    @staticmethod
    def base64_encode(data: str) -> str:
        """
        Base64 encode string

        Args:
            data: Data to encode

        Returns:
            Base64 encoded string
        """
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    @staticmethod
    def base64_decode(data: str) -> Optional[str]:
        """
        Base64 decode string

        Args:
            data: Base64 encoded string

        Returns:
            Decoded string or None if error
        """
        try:
            return base64.b64decode(data).decode("utf-8")
        except Exception:
            return None

    @staticmethod
    def get_random_key(length: int = 32) -> str:
        """
        Get random key

        Args:
            length: Key length

        Returns:
            Random key
        """
        import os

        return base64.b64encode(os.urandom(length)).decode("utf-8")[:length]

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> str:
        """
        Hash password with salt

        Args:
            password: Password to hash
            salt: Optional salt

        Returns:
            Hashed password
        """
        if salt is None:
            salt = CryptoUtils.get_random_key(16)
        combined = password + salt
        hash_value = hashlib.sha256(combined.encode("utf-8")).hexdigest()
        return f"{salt}:{hash_value}"

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify password against hash

        Args:
            password: Password to verify
            hashed_password: Hashed password

        Returns:
            Whether password is correct
        """
        try:
            salt, hash_value = hashed_password.split(":", 1)
            combined = password + salt
            new_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
            return new_hash == hash_value
        except Exception:
            return False


# Global instance
crypto_utils = CryptoUtils()
