"""State-driven placeholder config planning for the Project II scaffold."""

from __future__ import annotations

import os
from typing import Any

from .phase2_payload import build_phase2_candidate


MAX_PLACEHOLDER_FIELD_LENGTH = 256


def plan_candidate_config(state: dict[str, Any]) -> dict[str, Any]:
    """Return a safe, state-driven placeholder config for the current round.

    This is not an exploit. This only demonstrates writing config.data and
    signaling IC in the Project II shared-volume protocol. The candidate field
    length is used only to demonstrate an auditable feedback loop.

    TODO: Student implements course-lab-specific candidate generation here. Do
    not use this scaffold outside the controlled Docker lab.
    """

    if os.environ.get("PROJECT2_ENABLE_PHASE2_PROBE") == "1":
        strategy = os.environ.get("PROJECT2_PHASE2_STRATEGY", "control-flow")
        candidate = build_phase2_candidate(strategy)
        return {
            "strategy_id": candidate.strategy_id,
            "content_bytes": candidate.content,
            "input_profile": candidate.input_profile,
        }

    round_number = int(state.get("round", 0))
    next_action = state.get("next_action", {})
    parameters = next_action.get("parameters", {}) if isinstance(next_action, dict) else {}
    candidate_field = str(parameters.get("candidate_field", "candidate_field"))
    requested_length = int(parameters.get("candidate_length", 16))
    candidate_length = max(0, min(requested_length, MAX_PLACEHOLDER_FIELD_LENGTH))
    strategy_id = str(next_action.get("strategy_id", f"safe-placeholder-round-{round_number}"))
    placeholder_value = "P" * candidate_length
    content = (
        "PROJECT2_SAFE_PLACEHOLDER_CONFIG\n"
        f"round={round_number}\n"
        f"strategy={strategy_id}\n"
        f"{candidate_field}={placeholder_value}\n"
        f"{candidate_field}_length={candidate_length}\n"
        "notes=placeholder-only-no-payload\n"
    )
    return {
        "strategy_id": strategy_id,
        "content": content,
        "input_profile": {
            "field_name": candidate_field,
            "length": candidate_length,
            "requested_length": requested_length,
            "placeholder_only": True,
        },
    }
