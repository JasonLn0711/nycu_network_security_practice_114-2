from __future__ import annotations

from dataclasses import dataclass
from math import log2
from pathlib import Path


SUSPICIOUS_API_MARKERS = (
    b"CreateRemoteThread",
    b"VirtualAllocEx",
    b"WriteProcessMemory",
    b"SetWindowsHookEx",
)


@dataclass(frozen=True)
class HeuristicFinding:
    rule_id: str
    severity: str
    description: str
    evidence: str


def run_heuristics(path: Path, data: bytes) -> list[HeuristicFinding]:
    findings: list[HeuristicFinding] = []
    findings.extend(_api_name_indicator(data))
    findings.extend(_extension_magic_mismatch(path, data))
    findings.extend(_high_entropy_small_binary(path, data))
    return findings


def _api_name_indicator(data: bytes) -> list[HeuristicFinding]:
    hits = [marker.decode("ascii") for marker in SUSPICIOUS_API_MARKERS if marker in data]
    if not hits:
        return []

    return [
        HeuristicFinding(
            rule_id="api-name-indicator",
            severity="medium",
            description="Suspicious API-name strings appear in the file.",
            evidence=", ".join(hits),
        )
    ]


def _extension_magic_mismatch(path: Path, data: bytes) -> list[HeuristicFinding]:
    suffix = path.suffix.lower()
    if suffix == ".txt" and data.startswith(b"MZ"):
        return [
            HeuristicFinding(
                rule_id="extension-magic-mismatch",
                severity="low",
                description="File extension suggests text, but file header looks executable-like.",
                evidence="suffix=.txt, magic=MZ",
            )
        ]
    return []


def _high_entropy_small_binary(path: Path, data: bytes) -> list[HeuristicFinding]:
    if not data or len(data) > 4096:
        return []
    if path.suffix.lower() in {".txt", ".md", ".json", ".csv"}:
        return []

    entropy = _shannon_entropy(data)
    if entropy < 7.4:
        return []

    return [
        HeuristicFinding(
            rule_id="high-entropy-small-binary",
            severity="low",
            description="Small binary-like file has high byte entropy.",
            evidence=f"entropy={entropy:.2f}",
        )
    ]


def _shannon_entropy(data: bytes) -> float:
    counts = [0] * 256
    for byte in data:
        counts[byte] += 1

    entropy = 0.0
    length = len(data)
    for count in counts:
        if count == 0:
            continue
        probability = count / length
        entropy -= probability * log2(probability)
    return entropy
