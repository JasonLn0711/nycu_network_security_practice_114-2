"""Environment checks for the Project II scaffold."""

from __future__ import annotations

from dataclasses import dataclass

from . import path_config


class EnvironmentCheckError(RuntimeError):
    """Raised when a required scaffold path is missing or unusable."""


@dataclass(frozen=True)
class EnvironmentStatus:
    shared_exists: bool
    config_exists: bool
    blogic_copy_exists: bool
    coredump_dir_exists: bool
    shared_writable: bool


def check_shared_dir() -> None:
    if not path_config.SHARED_DIR.exists():
        raise EnvironmentCheckError(f"missing shared directory: {path_config.SHARED_DIR}")
    if not path_config.SHARED_DIR.is_dir():
        raise EnvironmentCheckError(f"shared path is not a directory: {path_config.SHARED_DIR}")


def ensure_coredump_dir() -> None:
    path_config.COREDUMP_DIR.mkdir(parents=True, exist_ok=True)


def check_required_paths_for_exploit() -> EnvironmentStatus:
    check_shared_dir()
    missing: list[str] = []
    if not path_config.CONFIG_PATH.exists():
        missing.append(str(path_config.CONFIG_PATH))
    if not path_config.BLOGIC_COPY_PATH.exists():
        missing.append(str(path_config.BLOGIC_COPY_PATH))
    if missing:
        raise EnvironmentCheckError("missing required exploit path(s): " + ", ".join(missing))
    ensure_coredump_dir()
    return EnvironmentStatus(
        shared_exists=True,
        config_exists=True,
        blogic_copy_exists=True,
        coredump_dir_exists=path_config.COREDUMP_DIR.exists(),
        shared_writable=True,
    )


def check_required_paths_for_triage() -> EnvironmentStatus:
    check_shared_dir()
    ensure_coredump_dir()
    return EnvironmentStatus(
        shared_exists=True,
        config_exists=path_config.CONFIG_PATH.exists(),
        blogic_copy_exists=path_config.BLOGIC_COPY_PATH.exists(),
        coredump_dir_exists=path_config.COREDUMP_DIR.exists(),
        shared_writable=True,
    )

