"""State management for the Project II scaffold."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import path_config


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_state() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project": "project2",
        "phase": "II",
        "round": 0,
        "last_exploit": {
            "config_hash": "",
            "strategy_id": "",
            "timestamp": "",
            "input_profile": {},
        },
        "last_triage": {
            "coredump_found": False,
            "selected_coredump": "",
            "analysis_status": "none",
            "summary": "",
        },
        "next_action": {
            "strategy_id": "baseline-observation",
            "parameters": {
                "candidate_field": "candidate_field",
                "candidate_length": 16,
                "step": 16,
            },
            "confidence": 0.0,
        },
        "search_state": {
            "strategy_family": "safe-placeholder-feedback-loop",
            "current_field": "",
            "current_length": 0,
            "last_safe_length": 0,
            "first_crash_length": None,
            "max_demo_length": 256,
            "last_result": "not-run",
            "avoid_repeating_hashes": [],
        },
        "safety": {
            "lab_only": True,
            "external_network": False,
        },
    }


def load_state() -> dict[str, Any]:
    if not path_config.STATE_PATH.exists():
        return default_state()
    try:
        with path_config.STATE_PATH.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return default_state()
    state = default_state()
    if isinstance(loaded, dict):
        state.update(loaded)
    return state


def save_state(state: dict[str, Any]) -> None:
    path_config.STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = Path(str(path_config.STATE_PATH) + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path_config.STATE_PATH)


def increment_round(state: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(state)
    updated["round"] = int(updated.get("round", 0)) + 1
    return updated


def update_after_exploit(
    state: dict[str, Any],
    strategy_id: str,
    config_hash: str,
    input_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = deepcopy(state)
    updated["last_exploit"] = {
        "config_hash": config_hash,
        "strategy_id": strategy_id,
        "timestamp": _now(),
        "input_profile": input_profile or {},
    }
    search_state = updated.setdefault("search_state", {})
    if input_profile:
        search_state["current_field"] = str(input_profile.get("field_name", ""))
        search_state["current_length"] = int(input_profile.get("length", 0) or 0)
    seen_hashes = search_state.setdefault("avoid_repeating_hashes", [])
    if config_hash and config_hash not in seen_hashes:
        seen_hashes.append(config_hash)
    search_state["avoid_repeating_hashes"] = seen_hashes[-20:]
    updated.setdefault("next_action", {})
    updated["next_action"]["strategy_id"] = strategy_id
    return updated


def update_after_triage(
    state: dict[str, Any],
    coredump_found: bool,
    selected_coredump: str,
    summary: str,
    next_action: dict[str, Any] | None = None,
    search_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = deepcopy(state)
    updated["last_triage"] = {
        "coredump_found": bool(coredump_found),
        "selected_coredump": selected_coredump,
        "analysis_status": "parsed" if coredump_found else "no-evidence",
        "summary": summary,
    }
    if next_action is not None:
        updated["next_action"] = next_action
    else:
        updated["next_action"] = {
            "strategy_id": (
                "safe-placeholder-after-coredump"
                if coredump_found
                else "safe-placeholder-no-coredump"
            ),
            "parameters": {},
            "confidence": 0.25 if coredump_found else 0.0,
        }
    if search_state is not None:
        updated["search_state"] = search_state
    return updated
