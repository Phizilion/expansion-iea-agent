from __future__ import annotations
import logging
import os

def setup_logging(level: str | int | None = None) -> None:
    """
    Configure root logger with a concise, developer-friendly format.

    Args:
        level: Optional log level. If None, read from env IEA_LOG_LEVEL or default to INFO.
    """
    lvl = level or os.getenv("IEA_LOG_LEVEL", "INFO")
    if isinstance(lvl, str):
        lvl = getattr(logging, lvl.upper(), logging.INFO)

    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(level=lvl, format=fmt, datefmt=datefmt)
