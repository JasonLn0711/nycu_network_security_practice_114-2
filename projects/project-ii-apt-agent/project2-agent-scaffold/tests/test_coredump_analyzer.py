from src.coredump_analyzer import decide_next_action
from src.state_manager import default_state, update_after_exploit


def test_no_coredump_increases_placeholder_length():
    state = default_state()
    state = update_after_exploit(
        state,
        "baseline-observation",
        "sha256:placeholder",
        {"field_name": "candidate_field", "length": 16},
    )

    decision = decide_next_action(
        state,
        coredump_found=False,
        selected_coredump="",
        evidence_summary="No coredump evidence available.",
    )

    assert decision["next_action"]["strategy_id"] == "length-sweep-placeholder"
    assert decision["next_action"]["parameters"]["candidate_length"] == 32
    assert decision["search_state"]["last_safe_length"] == 16


def test_coredump_sets_crash_bound_without_payload_details():
    state = default_state()
    state = update_after_exploit(
        state,
        "length-sweep-placeholder",
        "sha256:placeholder",
        {"field_name": "candidate_field", "length": 64},
    )
    state["search_state"]["last_safe_length"] = 32

    decision = decide_next_action(
        state,
        coredump_found=True,
        selected_coredump="/shared/coredump/core.placeholder",
        evidence_summary="Safe high-level coredump evidence summary only.",
    )

    assert decision["search_state"]["first_crash_length"] == 64
    assert decision["next_action"]["strategy_id"] in {
        "boundary-search-placeholder",
        "stability-check-placeholder",
    }
    assert "payload" not in str(decision).lower()
