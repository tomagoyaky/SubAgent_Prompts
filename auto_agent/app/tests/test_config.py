import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.config import Config


class TestConfig(unittest.TestCase):
    """Test config module"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary config.yaml file for testing
        self.temp_config = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        self.temp_config.write("""
environment: dev

environments:
  dev:
    llm:
      default_model: ollama/llama3
    directories:
      workspace: ./workspace
  prod:
    llm:
      default_model: anthropic:claude-sonnet-4-5-20250929
    directories:
      workspace: ./workspace
""")
        self.temp_config.close()

        # Patch the config path
        self.original_config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config.yaml"
        )
        if os.path.exists(self.original_config_path):
            self.original_config_content = open(self.original_config_path, "r").read()
            os.rename(self.original_config_path, self.original_config_path + ".backup")

        # Copy temp config to project root
        with open(self.original_config_path, "w") as f:
            f.write(open(self.temp_config.name, "r").read())

    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temp files
        os.unlink(self.temp_config.name)

        # Restore original config
        if hasattr(self, "original_config_content"):
            with open(self.original_config_path, "w") as f:
                f.write(self.original_config_content)
            os.unlink(self.original_config_path + ".backup")
        else:
            if os.path.exists(self.original_config_path):
                os.unlink(self.original_config_path)

    def test_config_initialization(self):
        """Test config initialization"""
        config = Config()
        self.assertIsInstance(config, Config)

    def test_get_method(self):
        """Test get method"""
        config = Config()

        # Test getting existing value
        self.assertEqual(config.get("llm.default_model"), "ollama/llama3")

        # Test getting non-existent value with default
        self.assertEqual(config.get("non_existent", "default_value"), "default_value")

        # Test getting non-existent value without default
        self.assertIsNone(config.get("non_existent"))

    def test_get_llm_config(self):
        """Test get_llm_config method"""
        config = Config()
        llm_config = config.get_llm_config()
        self.assertIsInstance(llm_config, dict)
        self.assertIn("default_model", llm_config)

    def test_get_directory_config(self):
        """Test get_directory_config method"""
        config = Config()
        dir_config = config.get_directory_config()
        self.assertIsInstance(dir_config, dict)
        self.assertIn("workspace", dir_config)

    def test_get_environment(self):
        """Test get_environment method"""
        config = Config()
        self.assertEqual(config.get_environment(), "dev")

    def test_set_method(self):
        """Test set method"""
        config = Config()

        # Test setting a value
        config.set("test.key", "test_value")
        self.assertEqual(config.get("test.key"), "test_value")

    def test_save_method(self):
        """Test save method"""
        config = Config()

        # Test saving to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        ) as temp_file:
            temp_file_path = temp_file.name

        try:
            result = config.save(temp_file_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_file_path))
            self.assertTrue(os.path.getsize(temp_file_path) > 0)
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)


if __name__ == "__main__":
    unittest.main()
