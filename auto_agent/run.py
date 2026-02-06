#!/usr/bin/env python3

"""
Auto Agent Run Script
Main entry point for the Auto Agent system
"""

import sys
import os
import argparse
from app.main import main
from app.utils.logger import global_logger as logger

if __name__ == "__main__":
    try:
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
    except KeyboardInterrupt:
        logger.info("Auto Agent stopped by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running Auto Agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
