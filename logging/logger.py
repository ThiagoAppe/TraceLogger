import logging

from .config import LogArea, LogCategory, log_level


def get_logger(area: LogArea, category: LogCategory) -> logging.Logger:
    if not isinstance(area, LogArea):
        raise TypeError("area must be an instance of LogArea enum")

    if not isinstance(category, LogCategory):
        raise TypeError("category must be an instance of LogCategory enum")

    logger_name = f"{area.value}.{category.value}"
    logger = logging.getLogger(logger_name)

    logger.setLevel(int(log_level))

    return logger