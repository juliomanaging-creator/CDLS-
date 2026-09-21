"""Shared logger setup for all agents."""

import logging
import sys
from datetime import datetime


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Create a consistently formatted logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(name)-20s] %(levelname)-8s %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Also log to file
        file_handler = logging.FileHandler(
            f"anthropic_kb_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger
