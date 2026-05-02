import logging


def create_console_handler(formatter: logging.Formatter) -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler