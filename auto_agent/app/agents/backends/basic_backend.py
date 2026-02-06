"""
Basic Backend
Backend implementation with long-term memory support
"""

import os
from typing import Callable, Optional

from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from app.config import config


class BasicBackend:
    """Basic backend with long-term memory support"""

    def __init__(self):
        """
        Initialize basic backend
        """
        # Use InMemoryStore for all environments
        self.store = InMemoryStore()

        self.checkpointer = MemorySaver()

    def create_backend(self) -> Callable:
        """
        Create backend function for deepagents

        Returns:
            Backend creation function
        """

        def make_backend(runtime):
            return CompositeBackend(
                default=StateBackend(runtime),  # Ephemeral storage
                routes={"/memories/": StoreBackend(runtime)},  # Persistent storage
            )

        return make_backend

    def get_store(self) -> InMemoryStore:
        """
        Get the in-memory store

        Returns:
            InMemoryStore instance
        """
        return self.store

    def get_checkpointer(self) -> MemorySaver:
        """
        Get the memory saver checkpointer

        Returns:
            MemorySaver instance
        """
        return self.checkpointer

    def get_user_preferences_prompt(self) -> str:
        """
        Get system prompt for user preferences use case

        Returns:
            System prompt string
        """
        return """
        You are an assistant that remembers user preferences.
        
        When users tell you their preferences, save them to /memories/user_preferences.txt
        so you remember them in future conversations.
        
        Your persistent memory structure:
        - /memories/user_preferences.txt: User preferences and settings
        
        Always check this file at the start of conversations to understand user preferences.
        """

    def get_self_improving_instructions_prompt(self) -> str:
        """
        Get system prompt for self-improving instructions use case

        Returns:
            System prompt string
        """
        return """
        You are a self-improving assistant.
        
        You have a file at /memories/instructions.txt with additional instructions and preferences.
        
        Read this file at the start of conversations to understand user preferences.
        
        When users provide feedback like "please always do X" or "I prefer Y",
        update /memories/instructions.txt using the edit_file tool.
        
        Your persistent memory structure:
        - /memories/instructions.txt: Additional instructions and preferences
        
        Over time, the instructions file should accumulate user preferences, helping you improve.
        """

    def get_knowledge_base_prompt(self) -> str:
        """
        Get system prompt for knowledge base use case

        Returns:
            System prompt string
        """
        return """
        You are a knowledge base assistant.
        
        Build up knowledge over multiple conversations by saving information to:
        - /memories/knowledge/: Directory for knowledge base
        - /memories/knowledge/topics/: Directory for different topics
        - /memories/knowledge/facts.txt: General facts
        
        Your persistent memory structure:
        - /memories/knowledge/: Main knowledge directory
        - /memories/knowledge/topics/: Topic-specific knowledge
        - /memories/knowledge/facts.txt: General facts and information
        
        When users ask about topics you've discussed before, check your knowledge base first.
        """

    def get_research_projects_prompt(self) -> str:
        """
        Get system prompt for research projects use case

        Returns:
            System prompt string
        """
        return """
        You are a research assistant.
        
        Save your research progress to /memories/research/:
        - /memories/research/sources.txt - List of sources found
        - /memories/research/notes.txt - Key findings and notes
        - /memories/research/report.md - Final report draft
        
        Your persistent memory structure:
        - /memories/research/: Main research directory
        - /memories/research/sources.txt: Research sources
        - /memories/research/notes.txt: Research notes
        - /memories/research/report.md: Research report
        
        This allows research to continue across multiple sessions.
        """


# Global backend instance
basic_backend = BasicBackend()


def get_basic_backend() -> BasicBackend:
    """
    Get the global basic backend instance

    Returns:
        BasicBackend instance
    """
    return basic_backend


def create_backend_with_long_term_memory() -> tuple:
    """
    Create backend components with long-term memory support

    Returns:
        Tuple of (backend_function, store, checkpointer)
    """
    backend = basic_backend
    return (backend.create_backend(), backend.get_store(), backend.get_checkpointer())
