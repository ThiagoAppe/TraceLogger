import logging
from enum import Enum
from typing import Union


def _resolve(value: Union[str, Enum]) -> str:
    """
    Normalize input value to string.

    Supports:
    - str
    - Enum
    """
    if isinstance(value, Enum):
        return value.value

    return str(value)


def get_logger(area: Union[str, Enum], category: Union[str, Enum]) -> logging.Logger:
    """
    Create and return a logger bound to area and category.

    Parameters:
        area: str | Enum
        category: str | Enum

    Returns:
        logging.Logger
    """

    area_str = _resolve(area)
    category_str = _resolve(category)

    logger_name = f"{area_str}.{category_str}"
    logger = logging.getLogger(logger_name)

    return logger