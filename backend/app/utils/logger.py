"""Logging configuration."""
import logging
import sys
from ..config import get_settings

settings = get_settings()


def setup_logger() -> logging.Logger:
    """Configure and return the root logger."""
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    # Add handler
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
