from src.phase2_payload import (
    LOG_MESSAGE_RET_OFFSET,
    MAINTENANCE_COMMAND_PREFIX,
    MAINTENANCE_TASK_ALIGNED_ENTRY,
    build_control_flow_probe,
)


def test_phase2_control_flow_probe_shape():
    candidate = build_control_flow_probe()

    assert candidate.content.startswith(b"user_input=" + MAINTENANCE_COMMAND_PREFIX)
    assert candidate.content.endswith(b"\n")
    assert b"\x00" not in candidate.content
    assert candidate.input_profile["ret_offset"] == LOG_MESSAGE_RET_OFFSET
    assert candidate.input_profile["partial_target"] == hex(MAINTENANCE_TASK_ALIGNED_ENTRY)
    assert candidate.input_profile["binary_safe"] is True
    assert candidate.input_profile["placeholder_only"] is False
