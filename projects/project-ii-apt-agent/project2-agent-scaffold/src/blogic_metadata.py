"""Safe metadata extraction for the Project II business-logic binary.

This module intentionally records only coarse, grading-useful metadata. It does
not disassemble the binary, does not derive offsets, and does not produce a
payload. The goal is to let /exploit, /triage, and readiness reports prove that
they observed the expected Phase II lab artifact without storing sensitive or
exploit-construction details.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ELF_MAGIC = b"\x7fELF"
PT_GNU_STACK = 0x6474E551
PF_X = 0x1

ELF_CLASS = {
    1: "ELF32",
    2: "ELF64",
}

ELF_ENDIAN_PREFIX = {
    1: "<",  # little endian
    2: ">",  # big endian
}

ELF_ENDIAN_LABEL = {
    1: "little",
    2: "big",
}

ELF_TYPE = {
    0: "NONE",
    1: "REL",
    2: "EXEC",
    3: "DYN",
    4: "CORE",
}

ELF_MACHINE = {
    0x03: "x86",
    0x3E: "x86_64",
    0xB7: "AArch64",
    0x28: "ARM",
    0xF3: "RISC-V",
}


@dataclass(frozen=True)
class BlogicMetadata:
    """Bounded metadata suitable for state files and grading reports."""

    exists: bool
    path: str
    size_bytes: int = 0
    sha256_prefix: str = ""
    file_kind: str = "missing"
    elf_class: str = ""
    endian: str = ""
    elf_type: str = ""
    machine: str = ""
    entrypoint_present: bool = False
    program_header_count: int = 0
    gnu_stack_executable: bool | None = None
    phase_hint: str = "unknown"
    parse_error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sha256_prefix(path: Path, *, bytes_to_read: int = 1024 * 1024) -> str:
    """Hash up to the first MiB so logs stay fast and bounded."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        remaining = bytes_to_read
        while remaining > 0:
            chunk = handle.read(min(65536, remaining))
            if not chunk:
                break
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()[:16]


def _parse_elf(path: Path, data: bytes) -> dict[str, Any]:
    if len(data) < 64 or not data.startswith(ELF_MAGIC):
        return {"file_kind": "non-elf"}

    class_id = data[4]
    endian_id = data[5]
    endian = ELF_ENDIAN_PREFIX.get(endian_id)
    if class_id != 2 or endian is None:
        return {
            "file_kind": "elf",
            "elf_class": ELF_CLASS.get(class_id, f"unknown-{class_id}"),
            "endian": ELF_ENDIAN_LABEL.get(endian_id, f"unknown-{endian_id}"),
            "parse_error": "unsupported ELF class or endian for bounded parser",
        }

    # ELF64 header layout after e_ident:
    # e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags,
    # e_ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx
    header = struct.unpack_from(f"{endian}HHIQQQIHHHHHH", data, 16)
    e_type = header[0]
    e_machine = header[1]
    e_entry = header[3]
    e_phoff = header[4]
    e_phentsize = header[8]
    e_phnum = header[9]

    gnu_stack_executable: bool | None = None
    with path.open("rb") as handle:
        for index in range(e_phnum):
            offset = e_phoff + index * e_phentsize
            handle.seek(offset)
            ph = handle.read(e_phentsize)
            if len(ph) < 8:
                continue
            p_type, p_flags = struct.unpack_from(f"{endian}II", ph, 0)
            if p_type == PT_GNU_STACK:
                gnu_stack_executable = bool(p_flags & PF_X)
                break

    elf_type = ELF_TYPE.get(e_type, f"unknown-{e_type}")
    phase_hint = "phase-ii-compatible" if elf_type == "EXEC" else "check-assumption"

    return {
        "file_kind": "elf",
        "elf_class": ELF_CLASS.get(class_id, f"unknown-{class_id}"),
        "endian": ELF_ENDIAN_LABEL.get(endian_id, f"unknown-{endian_id}"),
        "elf_type": elf_type,
        "machine": ELF_MACHINE.get(e_machine, f"unknown-{e_machine}"),
        "entrypoint_present": bool(e_entry),
        "program_header_count": int(e_phnum),
        "gnu_stack_executable": gnu_stack_executable,
        "phase_hint": phase_hint,
    }


def collect_blogic_metadata(path: Path) -> BlogicMetadata:
    """Collect safe metadata for a blogic copy or return a bounded error."""

    resolved = path.expanduser().resolve()
    if not resolved.exists():
        return BlogicMetadata(exists=False, path=str(resolved))
    if not resolved.is_file():
        return BlogicMetadata(
            exists=True,
            path=str(resolved),
            file_kind="not-file",
            parse_error="path exists but is not a regular file",
        )

    try:
        stat = resolved.stat()
        with resolved.open("rb") as handle:
            head = handle.read(64)
        parsed = _parse_elf(resolved, head)
        return BlogicMetadata(
            exists=True,
            path=str(resolved),
            size_bytes=stat.st_size,
            sha256_prefix=_sha256_prefix(resolved),
            **parsed,
        )
    except OSError as exc:
        return BlogicMetadata(
            exists=True,
            path=str(resolved),
            parse_error=f"metadata read failed: {exc}",
        )
