import os
import sys
import unittest
from unittest.mock import patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.agents.middleware.basic_middleware import BasicMiddleware
from app.agents.tools.basic_tool import get_all_tools


class TestBasicMiddleware(unittest.TestCase):
    """Test basic middleware module"""

    def test_basic_middleware_initialization(self):
        """Test BasicMiddleware initialization"""
        middleware = BasicMiddleware()
        self.assertIsInstance(middleware, BasicMiddleware)

    def test_basic_middleware_tools(self):
        """Test BasicMiddleware tools property"""
        # Get all tools from basic_tool.py
        expected_tools = get_all_tools()

        # Check that BasicMiddleware.tools contains all expected tools
        self.assertEqual(len(BasicMiddleware.tools), len(expected_tools))

        # Check that all tool names match
        expected_tool_names = [tool.name for tool in expected_tools]
        actual_tool_names = [tool.name for tool in BasicMiddleware.tools]

        for expected_name in expected_tool_names:
            self.assertIn(expected_name, actual_tool_names)

    @patch("app.agents.middleware.basic_middleware.get_all_tools")
    def test_basic_middleware_tools_injection(self, mock_get_all_tools):
        """Test BasicMiddleware tools injection"""
        # Set up mock
        mock_tools = [lambda x: x, lambda y: y]
        mock_get_all_tools.return_value = mock_tools

        # Clear the module cache to reimport with mocked get_all_tools
        if "app.agents.middleware.basic_middleware" in sys.modules:
            del sys.modules["app.agents.middleware.basic_middleware"]

        # Reimport the module
        from app.agents.middleware.basic_middleware import BasicMiddleware

        # Check that tools were injected correctly
        self.assertEqual(BasicMiddleware.tools, mock_tools)
        mock_get_all_tools.assert_called_once()


if __name__ == "__main__":
    unittest.main()
