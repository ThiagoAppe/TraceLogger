import os
from enum import Enum
from typing import Optional


# =========================
# Helpers
# =========================

def _ensure_log_folder(path: str) -> str:
    """
    Ensure that the log folder exists. Create it if missing.
    """
    os.makedirs(path, exist_ok=True)
    return path


def _get_str(key: str, default: str) -> str:
    return os.getenv(key, default)


def _get_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


def _get_bool(key: str, default: bool) -> bool:
    value: Optional[str] = os.getenv(key)

    if value is None:
        return default

    return value.lower() in ("true", "1", "yes", "y", "on")



# =========================
# Paths
# =========================

log_folder = _ensure_log_folder(
    _get_str("LOG_FOLDER", "logging")
)

log_history_folder = _ensure_log_folder(
    _get_str("LOG_HISTORY_FOLDER", "logging/history")
)


# =========================
# Core config
# =========================

log_level = _get_int("LOG_LEVEL", 10)

log_console = _get_bool("LOG_CONSOLE", True)
log_file = _get_bool("LOG_FILE", True)
log_json = _get_bool("LOG_JSON", False)


# =========================
# Rotation config
# =========================

log_rotate_daily = _get_bool("LOG_ROTATE_DAILY", False)
log_rotate_size = _get_int("LOG_ROTATE_SIZE", 5_000_000)

log_daily_backup = _get_int("LOG_DAILY_BACKUP", 7)
log_size_backup = _get_int("LOG_SIZE_BACKUP", 5)


# =========================
# Advanced / future
# =========================

log_encrypt = _get_bool("LOG_ENCRYPT", False)