import logging
from logging.handlers import QueueHandler
from typing import List, Optional
import atexit
from threading import Lock

from .core.queue import init_log_queue, get_log_queue
from .core.listener import start_listener, stop_listener
from .core.record_factory import setup_record_factory
from .handlers.console import create_console_handler
from .handlers.file import create_file_handler
from .formatters.json import JsonFormatter

from .config import (
    log_level,
    log_console,
    log_file,
)


_IsInitialized = False
_InitLock: Lock = Lock()


def init_logging(
    level: Optional[int] = None,
    use_console: Optional[bool] = None,
    use_file: Optional[bool] = None,
    use_multiprocessing: bool = False,
    extra_handlers: Optional[List[logging.Handler]] = None,
) -> None:
    global _IsInitialized

    if _IsInitialized:
        return

    with _InitLock:
        if _IsInitialized:
            return

        # =========================
        # Resolve config
        # =========================

        level = level if level is not None else log_level
        use_console = use_console if use_console is not None else log_console
        use_file = use_file if use_file is not None else log_file

        # =========================
        # Queue init
        # =========================

        init_log_queue(use_multiprocessing)
        queue = get_log_queue()

        # =========================
        # Record factory (context injection)
        # =========================

        setup_record_factory()


        # =========================
        # Formatters
        # =========================

        formatter = JsonFormatter()

        # =========================
        # Handlers (consumer side)
        # =========================

        handlers: List[logging.Handler] = []

        if use_console:
            handlers.append(create_console_handler(formatter))

        if use_file:
            handlers.append(create_file_handler("app", formatter))

        if extra_handlers:
            handlers.extend(extra_handlers)

        # =========================
        # Listener
        # =========================

        start_listener(queue, handlers)
        atexit.register(stop_listener)

        # =========================
        # Root logger (producer side)
        # =========================

        root_logger = logging.getLogger()

        root_logger.handlers.clear()
        root_logger.setLevel(level)

        queue_handler = QueueHandler(queue)
        root_logger.addHandler(queue_handler)

        _IsInitialized = True