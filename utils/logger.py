"""Logging utility for AI Web Signal Hunter."""

import logging
import sys
from typing import Optional

def setup_logger(name: str = "signal_hunter", level: int = logging.INFO) -> logging.Logger:
    """Configures a standardized logger avoiding credential leakage."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger

logger = setup_logger()

