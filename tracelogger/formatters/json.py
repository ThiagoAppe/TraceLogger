import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict


_RESERVED_ATTRS = {
    "name", "msg", "args", "levelname", "levelno",
    "pathname", "filename", "module", "exc_info",
    "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread",
    "threadName", "processName", "process"
}


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log_record = self._build_base(record)

        # =========================
        # Structured payload
        # =========================

        data = getattr(record, "data", None)

        if isinstance(data, dict):
            log_record["data"] = data

        # =========================
        # Exception handling
        # =========================

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False, default=str)

    # =========================
    # Helpers
    # =========================

    def _build_base(self, record: logging.LogRecord) -> Dict[str, Any]:
        base: Dict[str, Any] = {
            "@timestamp": self._format_time(record.created),
            "level": record.levelname,
            "status": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }

        context = self._extract_context(record)

        if context:
            base["context"] = context
            self._flatten_context(base, context)

        return base

    def _extract_context(self, record: logging.LogRecord) -> Dict[str, Any]:
        context: Dict[str, Any] = {}

        for key, value in record.__dict__.items():

            # excluir internos de logging
            if key in _RESERVED_ATTRS:
                continue

            # excluir campos controlados por el formatter
            if key in ("message", "asctime", "data"):
                continue

            # evitar valores inútiles
            if value is None:
                continue

            context[key] = value

        return context

    def _flatten_context(
        self,
        base: Dict[str, Any],
        context: Dict[str, Any]
    ) -> None:
        # Campos seguros para indexación (baja cardinalidad)
        for key in ("request_id", "process_id", "thread_id"):
            if key in context:
                base[key] = context[key]

    def _format_time(self, timestamp: float) -> str:
        return (
            datetime
            .fromtimestamp(timestamp, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )