import logging
from logging.handlers import QueueListener
from typing import List, Optional
from threading import Lock

from .queue import get_log_queue


_Listener: Optional[QueueListener] = None
_Lock: Lock = Lock()


def start_listener(handlers: List[logging.Handler]) -> None:
    global _Listener

    if not handlers:
        raise ValueError("Cannot start listener without handlers")

    if _Listener is not None:
        return

    with _Lock:
        if _Listener is not None:
            return

        queue = get_log_queue()

        _Listener = QueueListener(
            queue,
            *handlers,
            respect_handler_level=True
        )

        _Listener.start()


def stop_listener() -> None:
    global _Listener

    if _Listener is None:
        return

    with _Lock:
        if _Listener is None:
            return

        _Listener.stop()
        _Listener = None