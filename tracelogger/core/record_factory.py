import logging
from typing import Any

from .context import build_context


_OriginalFactory = logging.getLogRecordFactory()


def record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
    record = _OriginalFactory(*args, **kwargs)

    context = build_context()

    for key, value in context.items():
        setattr(record, key, value)

    return record


def setup_record_factory() -> None:
    logging.setLogRecordFactory(record_factory)