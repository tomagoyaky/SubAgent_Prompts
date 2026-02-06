import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.agents.interrupt.basic_interrupt import BasicInterrupt


class TestBasicInterrupt(unittest.TestCase):
    """Test basic interrupt module"""

    def setUp(self):
        """Set up test fixtures"""
        self.interrupt = BasicInterrupt()

    def test_should_interrupt_delete_file(self):
        """Test should_interrupt for delete_file operation"""
        state = {
            "tool_calls": [
                {"name": "delete_file", "arguments": {"file_path": "/path/to/file.txt"}}
            ]
        }
        self.assertTrue(self.interrupt.should_interrupt(state))

    def test_should_interrupt_delete_directory(self):
        """Test should_interrupt for delete_directory operation"""
        state = {
            "tool_calls": [
                {
                    "name": "delete_directory",
                    "arguments": {"directory": "/path/to/directory"},
                }
            ]
        }
        self.assertTrue(self.interrupt.should_interrupt(state))

    def test_should_interrupt_persistent_memory(self):
        """Test should_interrupt for operations on persistent memory"""
        state = {
            "tool_calls": [
                {
                    "name": "delete_file",
                    "arguments": {"file_path": "/memories/data.txt"},
                }
            ]
        }
        self.assertTrue(self.interrupt.should_interrupt(state))

    def test_should_not_interrupt_safe_operation(self):
        """Test should_interrupt for safe operations"""
        state = {
            "tool_calls": [
                {"name": "read_file", "arguments": {"file_path": "/path/to/file.txt"}}
            ]
        }
        self.assertFalse(self.interrupt.should_interrupt(state))

    def test_should_not_interrupt_no_tool_calls(self):
        """Test should_interrupt when there are no tool calls"""
        state = {}
        self.assertFalse(self.interrupt.should_interrupt(state))

    @patch("app.agents.interrupt.basic_interrupt.config")
    def test_get_interrupt_message_delete_file(self, mock_config):
        """Test get_interrupt_message for delete_file operation"""
        # Set up mock config
        mock_config.get_environment.return_value = "dev"

        state = {
            "tool_calls": [
                {"name": "delete_file", "arguments": {"file_path": "/path/to/file.txt"}}
            ]
        }

        message = self.interrupt.get_interrupt_message(state)
        self.assertIn(
            "Warning: You are about to perform dangerous operations in dev environment",
            message,
        )
        self.assertIn("Delete file: /path/to/file.txt", message)
        self.assertIn("Do you want to continue? (y/n)", message)

    @patch("app.agents.interrupt.basic_interrupt.config")
    def test_get_interrupt_message_delete_directory(self, mock_config):
        """Test get_interrupt_message for delete_directory operation"""
        # Set up mock config
        mock_config.get_environment.return_value = "prod"

        state = {
            "tool_calls": [
                {
                    "name": "delete_directory",
                    "arguments": {"directory": "/path/to/directory"},
                }
            ]
        }

        message = self.interrupt.get_interrupt_message(state)
        self.assertIn(
            "Warning: You are about to perform dangerous operations in prod environment",
            message,
        )
        self.assertIn("Delete directory: /path/to/directory", message)
        self.assertIn("Do you want to continue? (y/n)", message)

    @patch("app.agents.interrupt.basic_interrupt.config")
    def test_get_interrupt_message_persistent_memory(self, mock_config):
        """Test get_interrupt_message for operations on persistent memory"""
        # Set up mock config
        mock_config.get_environment.return_value = "dev"

        state = {
            "tool_calls": [
                {
                    "name": "delete_file",
                    "arguments": {"file_path": "/memories/data.txt"},
                }
            ]
        }

        message = self.interrupt.get_interrupt_message(state)
        self.assertIn("Delete persistent file: /memories/data.txt", message)

    def test_get_interrupt_message_no_tool_calls(self):
        """Test get_interrupt_message when there are no tool calls"""
        state = {}
        message = self.interrupt.get_interrupt_message(state)
        self.assertIn(
            "Warning: You are about to perform a dangerous operation", message
        )
        self.assertIn("Do you want to continue? (y/n)", message)

    def test_handle_user_response_yes(self):
        """Test handle_user_response with yes"""
        state = {}
        response = self.interrupt.handle_user_response(state, "y")
        self.assertTrue(response["allow_operation"])
        self.assertIn("Operation approved by user", response["message"])

    def test_handle_user_response_yes_variations(self):
        """Test handle_user_response with yes variations"""
        state = {}
        # Test different variations of "yes"
        variations = ["Y", "yes", "YES", "  Yes  "]
        for variation in variations:
            response = self.interrupt.handle_user_response(state, variation)
            self.assertTrue(response["allow_operation"])

    def test_handle_user_response_no(self):
        """Test handle_user_response with no"""
        state = {}
        response = self.interrupt.handle_user_response(state, "n")
        self.assertFalse(response["allow_operation"])
        self.assertIn("Operation cancelled by user", response["message"])

    def test_handle_user_response_no_variations(self):
        """Test handle_user_response with no variations"""
        state = {}
        # Test different variations of "no"
        variations = ["N", "no", "NO", "  No  ", "cancel"]
        for variation in variations:
            response = self.interrupt.handle_user_response(state, variation)
            self.assertFalse(response["allow_operation"])


if __name__ == "__main__":
    unittest.main()
