"""Safe coredump evidence helpers for the Project II scaffold."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import path_config


def list_coredumps() -> list[Path]:
    if not path_config.COREDUMP_DIR.exists():
        return []
    candidates = [path for path in path_config.COREDUMP_DIR.iterdir() if path.is_file()]
    return sorted(candidates, key=lambda path: (path.stat().st_mtime, path.name))


def select_latest_coredump(coredumps: list[Path] | None = None) -> Path | None:
    files = list_coredumps() if coredumps is None else coredumps
    if not files:
        return None
    return max(files, key=lambda path: (path.stat().st_mtime, path.name))


def summarize_coredump_safely(path: Path) -> dict[str, Any]:
    stat = path.stat()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
    return {
        "exists": path.exists(),
        "path": str(path),
        "size_bytes": stat.st_size,
        "modified_time": modified,
        "sha256_prefix": digest[:16],
        "summary": "Safe high-level coredump evidence summary only.",
    }

