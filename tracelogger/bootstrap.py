import logging
from logging.handlers import QueueHandler
from typing import List, Optional
import atexit


from .core.queue import init_log_queue, get_log_queue
from .core.listener import start_listener, stop_listener
from .handlers.console import create_console_handler
from .handlers.file import create_file_handler
from .formatters.simple import SimpleFormatter
from .config import (
    log_level,
    log_console,
    log_file,
)


_IsInitialized = False


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
    # Formatters
    # =========================

    formatter = SimpleFormatter()

    # =========================
    # Handlers
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

    start_listener(handlers)
    atexit.register(stop_listener)

    # =========================
    # Root logger
    # =========================

    root_logger = logging.getLogger()

    root_logger.handlers.clear()
    root_logger.setLevel(level)

    queue_handler = QueueHandler(queue)
    root_logger.addHandler(queue_handler)

    root_logger.propagate = False

    _IsInitialized = True