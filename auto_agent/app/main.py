"""
Main
Main application entry point
"""

import os
import sys
from typing import Any, Optional

from .agents.basic_agent import BasicAgent
from .config import config
from .llms.initializer import initialize_llm_provider
from .utils.logger import global_logger as logger
from .core.dependency_injector import register_dependency, register_factory


def cli_chat(default_user_input=None):
    """
    CLI chat function for interactive terminal interaction
    
    Args:
        default_user_input: Default user input to process automatically
    """
    from .core.dependency_injector import get_dependency
    
    # Get agent from dependency injector
    basic_agent = get_dependency("agent")
    
    if not basic_agent:
        logger.error("Failed to get agent for CLI chat")
        return
    
    # Call the chat method from BasicAgent
    basic_agent.chat(default_user_input=default_user_input)


def main(cli_mode=False, default_user_input=None):
    """
    Main function
    
    Args:
        cli_mode: Whether to start in CLI chat mode
        default_user_input: Default user input for non-CLI mode
    """
    # Initialize application
    logger.info("Initializing Auto Agent...")

    # Create necessary directories
    os.makedirs(config.get("directories.workspace", "./workspace"), exist_ok=True)
    os.makedirs("./logs", exist_ok=True)

    # Initialize LLM provider
    default_model = config.get("llm.default_model", "ollama/llama3")
    logger.info(f"Initializing LLM provider for model: {default_model}")

    llm_provider = initialize_llm_provider(
        model_name=default_model,
        stream_mode=config.get("llm.stream_mode", False),
        thinking_mode=config.get("llm.thinking_mode", False),
        temperature=config.get("llm.temperature", 0.7),
        top_p=config.get("llm.top_p", 0.9),
        max_tokens=config.get("llm.max_tokens", 2000),
    )

    if not llm_provider:
        logger.error("Failed to initialize LLM provider")
        sys.exit(1)

    # Register dependencies with dependency injector
    register_dependency("config", config)
    register_dependency("llm_provider", llm_provider)
    
    # Register factory for agent creation
    def create_agent_factory():
        return BasicAgent(
            name="AutoAgent",
            description="A professional AI assistant that can help with various tasks",
            llm_provider=llm_provider,
            config=config,
        )
    register_factory("agent", create_agent_factory)

    # Create and start agent using dependency injector
    from .core.dependency_injector import get_dependency
    basic_agent = get_dependency("agent")
    
    if basic_agent:
        if cli_mode:
            # Start CLI chat mode with default user input
            cli_chat(default_user_input=default_user_input)
        else:
            # Use default user input if provided, otherwise use "你好"
            user_input = default_user_input or "你好"
            
            # Start with initial input
            basic_agent.start(
                user_input=user_input,
                prompt={"system_prompt": "你是一个专业的助手", "user_prompt": user_input},
            )

            # Application initialized successfully
            logger.info("Auto Agent initialized successfully")

            # Wait for the agent thread to complete
            import time

            while basic_agent.is_alive():
                time.sleep(1)
            print("\n=======================================")
            print("        Auto Agent System")
            print("=======================================")
            print("System initialized successfully!")
            print("=======================================")
    else:
        logger.error("Failed to create agent")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description="Auto Agent System")
    
    # Add CLI mode argument
    parser.add_argument(
        "--cli",
        "-c",
        action="store_true",
        help="Start in CLI chat mode for interactive terminal interaction"
    )
    
    # Add default user input argument
    parser.add_argument(
        "--default_user_input",
        type=str,
        help="Default user input for non-CLI mode"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Start main function with CLI mode flag and default user input
    main(cli_mode=args.cli, default_user_input=args.default_user_input)
