"""Safe feedback-loop analysis for the Project II scaffold.

This module does not parse exploit-relevant internals. It turns high-level
round evidence into the next safe placeholder strategy so students can see the
closed-loop engineering pattern.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


DEFAULT_STEP = 16
DEFAULT_MAX_DEMO_LENGTH = 256


def _last_candidate_length(state: dict[str, Any]) -> int:
    profile = state.get("last_exploit", {}).get("input_profile", {})
    if isinstance(profile, dict) and "length" in profile:
        return int(profile.get("length", 0))
    params = state.get("next_action", {}).get("parameters", {})
    if isinstance(params, dict):
        return int(params.get("candidate_length", DEFAULT_STEP))
    return DEFAULT_STEP


def _bounded_length(value: int, max_length: int) -> int:
    return max(0, min(int(value), int(max_length)))


def decide_next_action(
    state: dict[str, Any],
    *,
    coredump_found: bool,
    selected_coredump: str,
    evidence_summary: str,
) -> dict[str, Any]:
    """Decide the next safe placeholder action from high-level evidence.

    The decision model demonstrates:
    observe -> update hypothesis -> choose next candidate length.

    It intentionally avoids payload construction and uses only safe metadata:
    whether a coredump exists, which round produced it, and the last placeholder
    input length.
    """

    search_state = deepcopy(state.get("search_state", {}))
    max_demo_length = int(search_state.get("max_demo_length", DEFAULT_MAX_DEMO_LENGTH))
    step = int(state.get("next_action", {}).get("parameters", {}).get("step", DEFAULT_STEP))
    last_length = _last_candidate_length(state)
    last_safe = int(search_state.get("last_safe_length", 0) or 0)
    first_crash = search_state.get("first_crash_length")

    if coredump_found:
        search_state["first_crash_length"] = (
            last_length
            if first_crash is None
            else min(int(first_crash), last_length)
        )
        search_state["last_result"] = "coredump-observed"
    else:
        search_state["last_safe_length"] = max(last_safe, last_length)
        search_state["last_result"] = "no-coredump-observed"

    last_safe = int(search_state.get("last_safe_length", 0) or 0)
    first_crash = search_state.get("first_crash_length")

    if first_crash is None:
        strategy_id = "length-sweep-placeholder"
        next_length = _bounded_length(max(last_length + step, step), max_demo_length)
        confidence = 0.1
    else:
        first_crash_int = int(first_crash)
        gap = max(0, first_crash_int - last_safe)
        if gap <= step:
            strategy_id = "stability-check-placeholder"
            next_length = _bounded_length(max(last_safe, step), max_demo_length)
            confidence = 0.5
        else:
            strategy_id = "boundary-search-placeholder"
            next_length = _bounded_length((last_safe + first_crash_int) // 2, max_demo_length)
            confidence = 0.35

    next_action = {
        "strategy_id": strategy_id,
        "parameters": {
            "candidate_field": "candidate_field",
            "candidate_length": next_length,
            "step": step,
            "selected_coredump": selected_coredump,
            "evidence_summary": evidence_summary,
        },
        "confidence": confidence,
    }

    return {
        "next_action": next_action,
        "search_state": search_state,
    }
