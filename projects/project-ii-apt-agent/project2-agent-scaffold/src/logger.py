"""Structured JSONL logging for the Project II scaffold."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from . import path_config


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(
    component: str,
    event: str,
    success: bool,
    details: dict[str, Any] | None = None,
) -> None:
    """Append one bounded JSON event to /shared/round_log.jsonl."""

    path_config.ROUND_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": utc_now(),
        "component": component,
        "event": event,
        "success": bool(success),
        "details": details or {},
    }
    with path_config.ROUND_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")

