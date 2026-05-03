from queue import Queue
from multiprocessing import Queue as MPQueue
from typing import Union, Optional
from threading import Lock


_LogQueue: Optional[Union[Queue, MPQueue]] = None
_UseMultiprocessing: Optional[bool] = None
_InitLock: Lock = Lock()


def init_log_queue(use_multiprocessing: bool = False) -> None:
    global _LogQueue, _UseMultiprocessing

    if _LogQueue is not None:
        if _UseMultiprocessing != use_multiprocessing:
            raise RuntimeError(
                "Log queue already initialized with a different configuration"
            )
        return

    with _InitLock:
        if _LogQueue is not None:
            if _UseMultiprocessing != use_multiprocessing:
                raise RuntimeError(
                    "Log queue already initialized with a different configuration"
                )
            return

        if use_multiprocessing:
            _LogQueue = MPQueue(-1)
        else:
            _LogQueue = Queue(-1)

        _UseMultiprocessing = use_multiprocessing


def get_log_queue() -> Union[Queue, MPQueue]:
    if _LogQueue is None:
        raise RuntimeError(
            "Log queue not initialized. Call init_log_queue() first."
        )

    return _LogQueue


def is_multiprocessing() -> bool:
    if _UseMultiprocessing is None:
        raise RuntimeError(
            "Log queue not initialized. Call init_log_queue() first."
        )

    return _UseMultiprocessing