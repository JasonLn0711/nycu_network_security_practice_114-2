"""Safety checks for the classroom-only scaffold.

This scaffold does not execute shell commands, connect to networks, tamper with
the grader, or access paths outside the configured lab/shared directory and the
repository itself.
"""

from __future__ import annotations

from pathlib import Path

from . import path_config


class SafetyError(RuntimeError):
    """Raised when a requested path or action violates the lab boundary."""


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def validate_lab_path(path: Path) -> None:
    """Require paths to stay under /shared, PROJECT2_SHARED_DIR, or repo root."""

    resolved = path.expanduser().resolve()
    allowed_roots = [path_config.SHARED_DIR.resolve(), path_config.PROJECT_ROOT.resolve()]
    if not any(_is_relative_to(resolved, root) for root in allowed_roots):
        raise SafetyError(f"path outside lab boundary: {resolved}")


def run_safety_checks() -> None:
    """Validate hard safety assumptions for the local scaffold.

    This function intentionally does not execute external commands or inspect
    networks. It documents and enforces the file boundary used by this scaffold.
    """

    for path in [
        path_config.SHARED_DIR,
        path_config.CONFIG_PATH,
        path_config.BLOGIC_COPY_PATH,
        path_config.BLOGIC_FALLBACK_PATH,
        path_config.EXPLOIT_DONE_PATH,
        path_config.COREDUMP_DIR,
        path_config.STATE_PATH,
        path_config.ROUND_LOG_PATH,
    ]:
        validate_lab_path(path)

