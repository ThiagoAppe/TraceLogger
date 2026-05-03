import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def create_file_handler(filename: str, formatter: logging.Formatter) -> logging.Handler:
    Path("logs").mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        f"logs/{filename}.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )

    handler.setFormatter(formatter)
    return handler