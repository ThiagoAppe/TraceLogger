import os
import threading
from contextvars import ContextVar, Token
from typing import Dict, Any, Optional


_Context: ContextVar[Dict[str, Any]] = ContextVar(
    "log_context",
    default={}
)


# =========================
# Public API
# =========================

def set_context(**kwargs: Any) -> None:
    current = _Context.get().copy()
    current.update(kwargs)
    _Context.set(current)


def get_context() -> Dict[str, Any]:
    return _Context.get()


def clear_context() -> None:
    _Context.set({})


# =========================
# Scoped context (CRÍTICO)
# =========================

class ContextScope:
    def __init__(self, **kwargs: Any) -> None:
        self._kwargs = kwargs
        self._token: Optional[Token] = None

    def __enter__(self) -> None:
        current = _Context.get().copy()
        current.update(self._kwargs)
        self._token = _Context.set(current)

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._token is not None:
            _Context.reset(self._token)


def context_scope(**kwargs: Any) -> ContextScope:
    return ContextScope(**kwargs)


# =========================
# Base context (automático)
# =========================

def _get_base_context() -> Dict[str, Any]:
    return {
        "process_id": os.getpid(),
        "thread_id": threading.get_ident(),
    }


# =========================
# Builder (usado por logging)
# =========================

def build_context() -> Dict[str, Any]:
    base = _get_base_context()
    user = _Context.get()

    if not user:
        return base

    merged = base.copy()
    merged.update(user)
    return merged