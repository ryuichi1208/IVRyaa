"""Logging module"""

import logging
import sys

from rich.console import Console
from rich.logging import RichHandler

from ivryaa.utils.config import settings

console = Console()


def setup_logger(name: str = "ivryaa") -> logging.Logger:
    """Set up and configure the logger"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    return logger


logger = setup_logger()
