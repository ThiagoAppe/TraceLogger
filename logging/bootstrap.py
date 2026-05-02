import logging
from logging.handlers import QueueHandler

from .core.queue import get_log_queue
from .core.listener import start_listener
from .handlers.console import create_console_handler
from .handlers.file import create_file_handler
from .formatters.simple import SimpleFormatter


_IsInitialized = False


def init_logging(
    level: int = logging.INFO,
    use_console: bool = True,
    use_file: bool = False,
    use_multiprocessing: bool = False
) -> None:
    global _IsInitialized

    if _IsInitialized:
        return

    queue = get_log_queue(use_multiprocessing)

    formatter = SimpleFormatter()

    handlers = []

    if use_console:
        handlers.append(create_console_handler(formatter))

    if use_file:
        handlers.append(create_file_handler("app", formatter))

    start_listener(handlers, use_multiprocessing)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    queue_handler = QueueHandler(queue)
    root_logger.addHandler(queue_handler)

    _IsInitialized = True