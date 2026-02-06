"""
Random Utils
Random number and string utilities
"""

import random
import string
from typing import Any, List, Optional


class RandomUtils:
    """Random utility class"""

    @staticmethod
    def get_random_int(min_val: int = 0, max_val: int = 100) -> int:
        """
        Get random integer

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random integer
        """
        return random.randint(min_val, max_val)

    @staticmethod
    def get_random_float(min_val: float = 0.0, max_val: float = 1.0) -> float:
        """
        Get random float

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random float
        """
        return random.uniform(min_val, max_val)

    @staticmethod
    def get_random_choice(choices: List[Any]) -> Any:
        """
        Get random choice from list

        Args:
            choices: List of choices

        Returns:
            Random choice
        """
        if not choices:
            return None
        return random.choice(choices)

    @staticmethod
    def get_random_sample(population: List[Any], k: int) -> List[Any]:
        """
        Get random sample from population

        Args:
            population: Population to sample from
            k: Sample size

        Returns:
            Random sample
        """
        if not population:
            return []
        k = min(k, len(population))
        return random.sample(population, k)

    @staticmethod
    def get_random_string(
        length: int = 8,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        special: bool = False,
    ) -> str:
        """
        Get random string

        Args:
            length: String length
            uppercase: Include uppercase letters
            lowercase: Include lowercase letters
            digits: Include digits
            special: Include special characters

        Returns:
            Random string
        """
        chars = ""
        if uppercase:
            chars += string.ascii_uppercase
        if lowercase:
            chars += string.ascii_lowercase
        if digits:
            chars += string.digits
        if special:
            chars += string.punctuation

        if not chars:
            chars = string.ascii_letters

        return "".join(random.choice(chars) for _ in range(length))

    @staticmethod
    def get_random_hex(length: int = 8) -> str:
        """
        Get random hex string

        Args:
            length: String length

        Returns:
            Random hex string
        """
        return "".join(random.choice("0123456789abcdef") for _ in range(length))

    @staticmethod
    def get_random_bool(probability: float = 0.5) -> bool:
        """
        Get random boolean

        Args:
            probability: Probability of returning True

        Returns:
            Random boolean
        """
        return random.random() < probability

    @staticmethod
    def shuffle_list(items: List[Any]) -> List[Any]:
        """
        Shuffle list

        Args:
            items: List to shuffle

        Returns:
            Shuffled list
        """
        shuffled = items.copy()
        random.shuffle(shuffled)
        return shuffled

    @staticmethod
    def get_random_uuid() -> str:
        """
        Get random UUID

        Returns:
            Random UUID string
        """
        import uuid

        return str(uuid.uuid4())

    @staticmethod
    def seed_random(seed: Optional[int] = None):
        """
        Seed random number generator

        Args:
            seed: Seed value
        """
        random.seed(seed)


# Global instance
random_utils = RandomUtils()
