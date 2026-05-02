from queue import Queue
from multiprocessing import Queue as MPQueue
from typing import Union


_LogQueue: Union[Queue, MPQueue, None] = None


def get_log_queue(use_multiprocessing: bool = False) -> Union[Queue, MPQueue]:
    global _LogQueue

    if _LogQueue is None:
        if use_multiprocessing:
            _LogQueue = MPQueue(-1)
        else:
            _LogQueue = Queue(-1)

    return _LogQueue