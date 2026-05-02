import logging
from logging.handlers import QueueListener
from typing import List

from .queue import get_log_queue


_Listener: QueueListener | None = None


def start_listener(handlers: List[logging.Handler], use_multiprocessing: bool = False) -> None:
    global _Listener

    if _Listener is not None:
        return

    queue = get_log_queue(use_multiprocessing)

    _Listener = QueueListener(queue, *handlers, respect_handler_level=True)
    _Listener.start()


def stop_listener() -> None:
    global _Listener

    if _Listener:
        _Listener.stop()
        _Listener = None