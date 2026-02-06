import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from app.agents.backends.basic_backend import (
    BasicBackend,
    basic_backend,
    create_backend_with_long_term_memory,
    get_basic_backend,
)


class TestBasicBackend(unittest.TestCase):
    """Test basic backend module"""

    @patch("app.agents.backends.basic_backend.config")
    def test_basic_backend_initialization_dev(self, mock_config):
        """Test BasicBackend initialization in dev environment"""
        # Set up mock config
        mock_config.get_environment.return_value = "dev"

        # Create backend
        backend = BasicBackend()

        # Check that store is InMemoryStore
        from langgraph.store.memory import InMemoryStore

        self.assertIsInstance(backend.store, InMemoryStore)

        # Check that checkpointer is MemorySaver
        from langgraph.checkpoint.memory import MemorySaver

        self.assertIsInstance(backend.checkpointer, MemorySaver)

    @patch("app.agents.backends.basic_backend.config")
    @patch("app.agents.backends.basic_backend.PostgresStore")
    def test_basic_backend_initialization_prod_success(
        self, mock_postgres_store, mock_config
    ):
        """Test BasicBackend initialization in prod environment with PostgresStore success"""
        # Set up mock config
        mock_config.get_environment.return_value = "prod"
        mock_config.get.return_value = (
            "postgresql://postgres:postgres@localhost:5432/auto_agent"
        )

        # Set up mock PostgresStore
        mock_store_ctx = MagicMock()
        mock_store = MagicMock()
        mock_store_ctx.__enter__.return_value = mock_store
        mock_postgres_store.from_conn_string.return_value = mock_store_ctx

        # Create backend
        backend = BasicBackend()

        # Check that store is the mock PostgresStore
        self.assertEqual(backend.store, mock_store)
        mock_store.setup.assert_called_once()

    @patch("app.agents.backends.basic_backend.config")
    @patch("app.agents.backends.basic_backend.PostgresStore")
    def test_basic_backend_initialization_prod_fallback(
        self, mock_postgres_store, mock_config
    ):
        """Test BasicBackend initialization in prod environment with fallback to InMemoryStore"""
        # Set up mock config
        mock_config.get_environment.return_value = "prod"
        mock_config.get.return_value = (
            "postgresql://postgres:postgres@localhost:5432/auto_agent"
        )

        # Set up mock PostgresStore to raise exception
        mock_postgres_store.from_conn_string.side_effect = Exception("Connection error")

        # Create backend
        backend = BasicBackend()

        # Check that store is InMemoryStore (fallback)
        from langgraph.store.memory import InMemoryStore

        self.assertIsInstance(backend.store, InMemoryStore)

    def test_create_backend(self):
        """Test create_backend method"""
        backend = BasicBackend()
        backend_func = backend.create_backend()

        # Check that it returns a callable
        self.assertCallable(backend_func)

    def test_get_store(self):
        """Test get_store method"""
        backend = BasicBackend()
        store = backend.get_store()
        self.assertEqual(store, backend.store)

    def test_get_checkpointer(self):
        """Test get_checkpointer method"""
        backend = BasicBackend()
        checkpointer = backend.get_checkpointer()
        self.assertEqual(checkpointer, backend.checkpointer)

    def test_get_user_preferences_prompt(self):
        """Test get_user_preferences_prompt method"""
        backend = BasicBackend()
        prompt = backend.get_user_preferences_prompt()

        self.assertIsInstance(prompt, str)
        self.assertIn("remembers user preferences", prompt)
        self.assertIn("/memories/user_preferences.txt", prompt)

    def test_get_self_improving_instructions_prompt(self):
        """Test get_self_improving_instructions_prompt method"""
        backend = BasicBackend()
        prompt = backend.get_self_improving_instructions_prompt()

        self.assertIsInstance(prompt, str)
        self.assertIn("self-improving assistant", prompt)
        self.assertIn("/memories/instructions.txt", prompt)

    def test_get_knowledge_base_prompt(self):
        """Test get_knowledge_base_prompt method"""
        backend = BasicBackend()
        prompt = backend.get_knowledge_base_prompt()

        self.assertIsInstance(prompt, str)
        self.assertIn("knowledge base assistant", prompt)
        self.assertIn("/memories/knowledge/", prompt)
        self.assertIn("/memories/knowledge/facts.txt", prompt)

    def test_get_research_projects_prompt(self):
        """Test get_research_projects_prompt method"""
        backend = BasicBackend()
        prompt = backend.get_research_projects_prompt()

        self.assertIsInstance(prompt, str)
        self.assertIn("research assistant", prompt)
        self.assertIn("/memories/research/", prompt)
        self.assertIn("/memories/research/sources.txt", prompt)
        self.assertIn("/memories/research/notes.txt", prompt)
        self.assertIn("/memories/research/report.md", prompt)

    def test_get_basic_backend(self):
        """Test get_basic_backend function"""
        backend = get_basic_backend()
        self.assertIsInstance(backend, BasicBackend)
        self.assertEqual(backend, basic_backend)

    def test_create_backend_with_long_term_memory(self):
        """Test create_backend_with_long_term_memory function"""
        result = create_backend_with_long_term_memory()

        # Check that it returns a tuple with 3 elements
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)

        # Check that first element is callable
        backend_func, store, checkpointer = result
        self.assertCallable(backend_func)

        # Check that store and checkpointer are not None
        self.assertIsNotNone(store)
        self.assertIsNotNone(checkpointer)

    def assertCallable(self, obj):
        """Helper method to check if object is callable"""
        self.assertTrue(callable(obj))


if __name__ == "__main__":
    unittest.main()
