import os
import sys
import threading
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.agents.basic_agent import BasicAgent


class TestBasicAgent(unittest.TestCase):
    """Test basic agent module"""

    def setUp(self):
        """Set up test fixtures"""

        # Create a subclass of BasicAgent for testing
        class TestAgent(BasicAgent):
            def process(self, task, context=None, **kwargs):
                return {"task": task, "context": context}

        self.TestAgent = TestAgent

    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = self.TestAgent("Test Agent", "A test agent")
        self.assertIsInstance(agent, BasicAgent)
        self.assertEqual(agent.name, "Test Agent")
        self.assertEqual(agent.description, "A test agent")

    def test_get_thread_id(self):
        """Test get_thread_id method"""
        agent = self.TestAgent("Test Agent", "A test agent")
        thread_id = agent.get_thread_id()
        self.assertIsInstance(thread_id, str)
        self.assertTrue(len(thread_id) > 0)

    def test_validate_input(self):
        """Test validate_input method"""
        agent = self.TestAgent("Test Agent", "A test agent")

        # Test valid input
        self.assertTrue(agent.validate_input("Valid task"))
        self.assertTrue(agent.validate_input("Valid task", {"key": "value"}))

        # Test invalid input
        self.assertFalse(agent.validate_input(None))
        self.assertFalse(agent.validate_input(123))  # Not a string
        self.assertFalse(
            agent.validate_input("Valid task", "Not a dict")
        )  # Context not a dict

    def test_get_info(self):
        """Test get_info method"""
        agent = self.TestAgent("Test Agent", "A test agent")
        info = agent.get_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info["name"], "Test Agent")
        self.assertEqual(info["description"], "A test agent")
        self.assertIn("thread_id", info)

    @patch("app.agents.basic_agent.create_deep_agent")
    def test_invoke_deep_agent(self, mock_create_deep_agent):
        """Test invoke_deep_agent method"""
        # Set up mock
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"response": "Test response"}
        mock_create_deep_agent.return_value = mock_agent

        agent = self.TestAgent("Test Agent", "A test agent")
        result = agent.invoke_deep_agent("Test task")

        self.assertEqual(result, {"response": "Test response"})
        mock_agent.invoke.assert_called_once()

    @patch("app.agents.basic_agent.create_deep_agent")
    def test_run_method(self, mock_create_deep_agent):
        """Test run method"""
        # Set up mock
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"response": "Test response"}
        mock_create_deep_agent.return_value = mock_agent

        agent = self.TestAgent("Test Agent", "A test agent", task="Test task")

        # Run in a thread to avoid blocking
        thread = threading.Thread(target=agent.run)
        thread.start()
        thread.join(timeout=1)

        mock_agent.invoke.assert_called_once()

    @patch("app.agents.basic_agent.create_deep_agent")
    def test_start_method(self, mock_create_deep_agent):
        """Test start method"""
        # Set up mock
        mock_agent = MagicMock()
        mock_agent.invoke.return_value = {"response": "Test response"}
        mock_create_deep_agent.return_value = mock_agent

        agent = self.TestAgent("Test Agent", "A test agent")
        agent.start(task="Test task")

        # Wait for the thread to complete
        agent.join(timeout=1)

        mock_agent.invoke.assert_called_once()

    def test_process_method(self):
        """Test process method"""
        agent = self.TestAgent("Test Agent", "A test agent")
        result = agent.process("Test task", {"key": "value"})
        self.assertEqual(result["task"], "Test task")
        self.assertEqual(result["context"], {"key": "value"})


if __name__ == "__main__":
    unittest.main()
