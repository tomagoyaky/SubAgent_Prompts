import os
import sys
import unittest
from unittest.mock import patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.agents.skills.basic_skill import BasicSkill


class TestBasicSkill(unittest.TestCase):
    """Test basic skill module"""

    def test_basic_skill_initialization(self):
        """Test BasicSkill initialization"""
        skill = BasicSkill("Test Skill", "A test skill", param1="value1")
        self.assertIsInstance(skill, BasicSkill)
        self.assertEqual(skill.name, "Test Skill")
        self.assertEqual(skill.description, "A test skill")
        self.assertEqual(skill.kwargs["param1"], "value1")

    @patch("app.agents.skills.basic_skill.config")
    def test_get_skill_directory_from_config(self, mock_config):
        """Test get_skill_directory method with config value"""
        # Set up mock config
        expected_dir = "/path/to/skills"
        mock_config.get.return_value = expected_dir

        # Test the method
        skill_dir = BasicSkill.get_skill_directory()
        self.assertEqual(skill_dir, expected_dir)
        mock_config.get.assert_called_once_with("directories.skills")

    @patch("app.agents.skills.basic_skill.config")
    def test_get_skill_directory_fallback(self, mock_config):
        """Test get_skill_directory method with fallback"""
        # Set up mock config to return None
        mock_config.get.return_value = None

        # Test the method
        skill_dir = BasicSkill.get_skill_directory()
        # Should return the directory containing basic_skill.py
        expected_dir = os.path.dirname(os.path.abspath(__file__))
        expected_dir = os.path.dirname(expected_dir)  # Go up to tests directory
        expected_dir = os.path.join(
            expected_dir, "agents", "skills"
        )  # Go to skills directory
        self.assertEqual(skill_dir, expected_dir)
        mock_config.get.assert_called_once_with("directories.skills")

    @patch("app.agents.skills.basic_skill.BasicSkill.get_skill_directory")
    def test_get_default_skills(self, mock_get_skill_directory):
        """Test get_default_skills method"""
        # Set up mock
        expected_dir = "/path/to/skills"
        mock_get_skill_directory.return_value = expected_dir

        # Test the method
        default_skills = BasicSkill.get_default_skills()
        self.assertIsInstance(default_skills, list)
        self.assertEqual(len(default_skills), 1)
        self.assertEqual(default_skills[0], expected_dir)
        mock_get_skill_directory.assert_called_once()


if __name__ == "__main__":
    unittest.main()
