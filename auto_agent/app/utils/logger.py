"""
Logger Utility
Logging management functionality
"""

import logging
import os
from datetime import datetime


class Logger:
    """Logging utility class"""

    def __init__(self, name: str, log_file: str = None, level: int = logging.INFO):
        """
        Initialize logger

        Args:
            name: Logger name
            log_file: Optional log file path
            level: Logging level
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if log_file is provided
        if log_file:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, *args, **kwargs):
        """
        Log debug message

        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """
        Log info message

        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """
        Log warning message

        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """
        Log error message

        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """
        Log critical message

        Args:
            message: Log message
            *args: Additional arguments
            **kwargs: Additional keyword arguments
        """
        self.logger.critical(message, *args, **kwargs)


# Create default logger
def get_default_logger(name: str = "auto_agent") -> Logger:
    """
    Get default logger

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
    )
    log_file = os.path.join(
        log_dir, f"auto_agent_{datetime.now().strftime('%Y%m%d')}.log"
    )
    return Logger(name, log_file)


# Global logger instance
global_logger = get_default_logger()
