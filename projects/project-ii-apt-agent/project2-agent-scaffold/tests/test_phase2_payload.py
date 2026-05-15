from src.phase2_payload import (
    LOG_MESSAGE_RET_OFFSET,
    CURRENT_RDI_COMMAND_PREFIX,
    DIRECT_SYSTEM_COMMAND_PREFIX,
    MAINTENANCE_COMMAND_PREFIX,
    MAINTENANCE_TASK_FRAME_BODY_ENTRY,
    MAINTENANCE_TASK_SYSTEM_RAX_ENTRY,
    MAINTENANCE_TASK_ALIGNED_ENTRY,
    MULTILINE_STAGE_LENGTH,
    SYSTEM_PLT_ENTRY,
    build_phase2_candidate,
    build_control_flow_probe,
    build_current_rdi_system_probe,
    build_multiline_staging_probe,
    build_register_reuse_system_rax_probe,
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


def test_phase2_multiline_staging_probe_shape():
    candidate = build_multiline_staging_probe()

    assert candidate.content.count(b"user_input=") == 2
    assert candidate.content.startswith(b"user_input=PHASE2-MULTILINE-STAGE;")
    assert b"\x00" not in candidate.content
    assert candidate.input_profile["line_count"] == 2
    assert candidate.input_profile["stage_length"] == MULTILINE_STAGE_LENGTH
    assert candidate.input_profile["ret_offset"] == LOG_MESSAGE_RET_OFFSET
    assert candidate.input_profile["partial_target"] == hex(MAINTENANCE_TASK_FRAME_BODY_ENTRY)
    assert candidate.input_profile["binary_safe"] is True
    assert candidate.input_profile["placeholder_only"] is False


def test_phase2_register_reuse_system_rax_probe_shape():
    candidate = build_register_reuse_system_rax_probe()

    assert candidate.content.startswith(b"user_input=" + DIRECT_SYSTEM_COMMAND_PREFIX)
    assert candidate.content.endswith(b"\n")
    assert b"\x00" not in candidate.content
    assert candidate.input_profile["ret_offset"] == LOG_MESSAGE_RET_OFFSET
    assert candidate.input_profile["partial_target"] == hex(MAINTENANCE_TASK_SYSTEM_RAX_ENTRY)
    assert candidate.input_profile["binary_safe"] is True
    assert candidate.input_profile["placeholder_only"] is False


def test_phase2_current_rdi_system_probe_shape():
    candidate = build_current_rdi_system_probe()

    assert candidate.content.startswith(b"user_input=" + CURRENT_RDI_COMMAND_PREFIX)
    assert candidate.content.endswith(b"\n")
    assert b"\x00" not in candidate.content
    assert candidate.input_profile["ret_offset"] == LOG_MESSAGE_RET_OFFSET
    assert candidate.input_profile["partial_target"] == hex(SYSTEM_PLT_ENTRY)
    assert candidate.input_profile["binary_safe"] is True
    assert candidate.input_profile["placeholder_only"] is False


def test_phase2_candidate_selector():
    assert build_phase2_candidate("control-flow").strategy_id == (
        "phase2-medium-control-flow-probe"
    )
    assert build_phase2_candidate("multiline-staging").strategy_id == (
        "phase2-medium-multiline-staging-probe"
    )
    assert build_phase2_candidate("register-reuse-system-rax").strategy_id == (
        "phase2-medium-register-reuse-system-rax-probe"
    )
    assert build_phase2_candidate("current-rdi-system").strategy_id == (
        "phase2-medium-current-rdi-system-probe"
    )
