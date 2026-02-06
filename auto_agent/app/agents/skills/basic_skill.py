"""
Basic Skill
Skill base class for deepagents integration
"""

import os
from typing import Any, Dict, List, Optional

from app.config import config


class BasicSkill:
    """Base class for skills"""

    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the skill

        Args:
            name: Skill name
            description: Skill description
            **kwargs: Additional parameters
        """
        self.name = name
        self.description = description
        self.kwargs = kwargs

    @staticmethod
    def get_skill_directory() -> str:
        """
        Get the default skill directory

        Returns:
            Path to skill directory
        """
        # Try to get from config first
        skill_dir = config.get("directories.skills")
        if skill_dir:
            return skill_dir
        # Fallback to current directory
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_default_skills() -> List[str]:
        """
        Get default skills for deepagents

        Returns:
            List of skill paths
        """
        skill_dir = BasicSkill.get_skill_directory()
        return [skill_dir]
