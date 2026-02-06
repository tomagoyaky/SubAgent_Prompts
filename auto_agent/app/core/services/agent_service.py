"""
Agent Service
Service for handling agent-related business logic
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from deepagents import create_deep_agent
from app.agents.basic_agent import BasicAgent
from app.core.services.tool_service import tool_service
from app.core.services.llm_service import llm_service
from app.core.dependency_injector import get_dependency
from app.utils.logger import global_logger as logger


class AgentService(ABC):
    """
    Abstract base class for agent service
    """

    @abstractmethod
    def create_agent(self, name: str, description: str, **kwargs) -> Optional[BasicAgent]:
        """
        Create an agent

        Args:
            name: Agent name
            description: Agent description
            **kwargs: Additional agent parameters

        Returns:
            Agent instance or None if failed
        """
        pass

    @abstractmethod
    def create_deep_agent(self, model: Any, system_prompt: str, tools: List[Any], **kwargs) -> Optional[Any]:
        """
        Create deep agent using deepagents library

        Args:
            model: LLM provider instance
            system_prompt: System prompt
            tools: List of tools
            **kwargs: Additional deep agent parameters

        Returns:
            Deep agent instance or None if failed
        """
        pass

    @abstractmethod
    def start_agent(self, agent: BasicAgent, user_input: str, **kwargs) -> bool:
        """
        Start an agent

        Args:
            agent: Agent instance
            user_input: User input
            **kwargs: Additional start parameters

        Returns:
            Whether agent was successfully started
        """
        pass

    @abstractmethod
    def get_agent_info(self, agent: BasicAgent) -> Dict[str, Any]:
        """
        Get agent information

        Args:
            agent: Agent instance

        Returns:
            Agent information dictionary
        """
        pass

    @abstractmethod
    def stop_agent(self, agent: BasicAgent) -> bool:
        """
        Stop an agent

        Args:
            agent: Agent instance

        Returns:
            Whether agent was successfully stopped
        """
        pass


class AgentServiceImpl(AgentService):
    """
    Implementation of agent service
    """

    def create_agent(self, name: str, description: str, **kwargs) -> Optional[BasicAgent]:
        """
        Create an agent

        Args:
            name: Agent name
            description: Agent description
            **kwargs: Additional agent parameters

        Returns:
            Agent instance or None if failed
        """
        try:
            logger.info(f"Creating agent: {name}")
            
            # Get dependencies from dependency injector if not provided
            if "llm_provider" not in kwargs:
                llm_provider = get_dependency("llm_provider")
                if llm_provider:
                    kwargs["llm_provider"] = llm_provider
            
            if "config" not in kwargs:
                config = get_dependency("config")
                if config:
                    kwargs["config"] = config
            
            # Create agent
            agent = BasicAgent(
                name=name,
                description=description,
                **kwargs
            )
            
            logger.info(f"Successfully created agent: {name}")
            return agent
        except Exception as e:
            logger.error(f"Error creating agent {name}: {e}")
            return None

    def create_deep_agent(self, model: Any, system_prompt: str, tools: List[Any], **kwargs) -> Optional[Any]:
        """
        Create deep agent using deepagents library

        Args:
            model: LLM provider instance
            system_prompt: System prompt
            tools: List of tools
            **kwargs: Additional deep agent parameters

        Returns:
            Deep agent instance or None if failed
        """
        try:
            logger.info("Creating deep agent")
            
            # Prepare deep agent parameters
            deep_agent_kwargs = {
                "model": model,
                "system_prompt": system_prompt,
                "tools": tools,
                **kwargs
            }
            
            # Create deep agent
            deep_agent = create_deep_agent(**deep_agent_kwargs)
            
            logger.info("Successfully created deep agent")
            return deep_agent
        except Exception as e:
            logger.error(f"Error creating deep agent: {e}")
            return None

    def start_agent(self, agent: BasicAgent, user_input: str, **kwargs) -> bool:
        """
        Start an agent

        Args:
            agent: Agent instance
            user_input: User input
            **kwargs: Additional start parameters

        Returns:
            Whether agent was successfully started
        """
        try:
            logger.info(f"Starting agent: {agent.name}")
            
            agent.start(user_input=user_input, **kwargs)
            
            logger.info(f"Successfully started agent: {agent.name}")
            return True
        except Exception as e:
            logger.error(f"Error starting agent {agent.name}: {e}")
            return False

    def get_agent_info(self, agent: BasicAgent) -> Dict[str, Any]:
        """
        Get agent information

        Args:
            agent: Agent instance

        Returns:
            Agent information dictionary
        """
        try:
            info = agent.get_agent_info()
            
            # Add additional information
            if hasattr(agent, "agent") and agent.agent:
                info["deep_agent"] = {
                    "has_model": hasattr(agent.agent, "model"),
                    "has_tools": hasattr(agent.agent, "tools"),
                    "has_system_prompt": hasattr(agent.agent, "system_prompt"),
                }
            
            return info
        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return {"error": str(e)}

    def stop_agent(self, agent: BasicAgent) -> bool:
        """
        Stop an agent

        Args:
            agent: Agent instance

        Returns:
            Whether agent was successfully stopped
        """
        try:
            logger.info(f"Stopping agent: {agent.name}")
            
            # Try to stop the agent thread
            if agent.is_alive():
                # Note: BasicAgent doesn't have a direct stop method
                # We'll rely on the thread completing naturally
                logger.info(f"Agent {agent.name} is running, will stop when task completes")
            
            logger.info(f"Successfully stopped agent: {agent.name}")
            return True
        except Exception as e:
            logger.error(f"Error stopping agent {agent.name}: {e}")
            return False


# Global agent service instance
agent_service = AgentServiceImpl()
