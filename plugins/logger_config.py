"""
Centralized logging configuration for the grtnr.com project.
Provides standardized logging format with colored output.
"""

import logging
import sys
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for different log levels."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        """Format the log record with colors and standardized format."""
        # Get the color for the log level
        color = self.COLORS.get(record.levelname, "")

        # Format timestamp as "2025-05-28 21:63"
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M")

        # Create the formatted message
        log_message = f"{color}{timestamp} {record.levelname:<8}{self.RESET} {record.getMessage()}"

        # Add exception info if present
        if record.exc_info:
            log_message += "\n" + self.formatException(record.exc_info)

        return log_message


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a configured logger with colored output.

    Args:
        name: Logger name (typically __name__ or plugin name)
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Set log level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)

    # Set the colored formatter
    formatter = ColoredFormatter()
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    # Prevent propagation to avoid duplicate messages
    logger.propagate = False

    return logger


def setup_pelican_logging(level: str = "INFO"):
    """
    Setup logging for the entire Pelican project.
    Call this once during Pelican initialization.

    Args:
        level: Global log level for the project
    """
    # Configure root logger for any uncaught logging calls
    root_logger = logging.getLogger()

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set up with our colored formatter
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter()
    handler.setFormatter(formatter)

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)
    handler.setLevel(numeric_level)

    root_logger.addHandler(handler)


# Convenience function for quick logger access
def log(level: str, message: str, logger_name: str = "grtnr"):
    """
    Quick logging function for one-off messages.

    Args:
        level: Log level ('debug', 'info', 'warning', 'error', 'critical')
        message: Message to log
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)
    getattr(logger, level.lower())(message)


# Module-level logger for this file
logger = get_logger(__name__)
