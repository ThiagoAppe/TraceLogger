import logging
from logging.handlers import QueueListener
from typing import List, Optional, Union
from threading import Lock
from queue import Queue
from multiprocessing import Queue as MPQueue


_Listener: Optional[QueueListener] = None
_Lock: Lock = Lock()


def start_listener(
    queue: Union[Queue, MPQueue],
    handlers: List[logging.Handler],
) -> None:
    global _Listener

    if not handlers:
        raise ValueError("Cannot start listener without handlers")

    if _Listener is not None:
        return

    with _Lock:
        if _Listener is not None:
            return

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

        # Cleanup handlers (important for files/sockets)
        for handler in _Listener.handlers:
            try:
                handler.close()
            except Exception:
                pass

        _Listener = None