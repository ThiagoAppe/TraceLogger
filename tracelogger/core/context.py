import os
import threading
from contextvars import ContextVar
from typing import Dict, Any


_Context: ContextVar[Dict[str, Any]] = ContextVar(
    "log_context",
    default={}
)


def set_context(**kwargs: Any) -> None:
    current = _Context.get().copy()
    current.update(kwargs)
    _Context.set(current)


def get_context() -> Dict[str, Any]:
    return _Context.get()


def clear_context() -> None:
    _Context.set({})


def _get_base_context() -> Dict[str, Any]:
    return {
        "process_id": os.getpid(),
        "thread_id": threading.get_ident(),
    }


def build_context() -> Dict[str, Any]:
    base = _get_base_context()
    user = _Context.get()

    if not user:
        return base

    merged = base.copy()
    merged.update(user)
    return merged