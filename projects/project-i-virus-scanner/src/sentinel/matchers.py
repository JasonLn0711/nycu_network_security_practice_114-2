from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .signatures import HashMatcher, PatternMatcher, SignatureDatabase


CHUNK_SIZE = 1024 * 1024
HEURISTIC_SAMPLE_LIMIT = 1024 * 1024


@dataclass(frozen=True)
class FileScanContent:
    size_bytes: int
    hashes: dict[str, str]
    pattern_matches: tuple[PatternMatcher, ...]
    heuristic_sample: bytes


def read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def compute_hashes(data: bytes) -> dict[str, str]:
    return {
        "md5": hashlib.md5(data).hexdigest(),  # nosec: course signature matching, not security auth
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def find_hash_matches(hashes: dict[str, str], database: SignatureDatabase) -> list[HashMatcher]:
    matches: list[HashMatcher] = []
    for algorithm, digest in hashes.items():
        matches.extend(database.hash_index.get(algorithm, {}).get(digest, ()))
    return matches


def find_pattern_matches(data: bytes, database: SignatureDatabase) -> list[PatternMatcher]:
    return [pattern_matcher for pattern_matcher in database.patterns if pattern_matcher.pattern in data]


def scan_file_content(
    path: Path,
    database: SignatureDatabase,
    *,
    chunk_size: int = CHUNK_SIZE,
    heuristic_sample_limit: int = HEURISTIC_SAMPLE_LIMIT,
) -> FileScanContent:
    """Read a file once while hashing, matching patterns, and keeping a heuristic sample."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")
    if heuristic_sample_limit < 0:
        raise ValueError("heuristic_sample_limit cannot be negative.")

    md5 = hashlib.md5()  # nosec: course signature matching, not security auth
    sha256 = hashlib.sha256()
    size_bytes = 0
    sample_parts: list[bytes] = []
    sample_bytes = 0
    pattern_matches: list[PatternMatcher] = []
    seen_patterns: set[tuple[str, str, str]] = set()
    max_pattern_len = max((len(pattern.pattern) for pattern in database.patterns), default=0)
    tail = b""

    with path.open("rb") as source:
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break

            size_bytes += len(chunk)
            md5.update(chunk)
            sha256.update(chunk)
            if sample_bytes < heuristic_sample_limit:
                needed = heuristic_sample_limit - sample_bytes
                sample = chunk[:needed]
                sample_parts.append(sample)
                sample_bytes += len(sample)

            search_window = tail + chunk
            for pattern in database.patterns:
                key = (pattern.signature.id, pattern.matcher.type, pattern.matcher.value)
                if key in seen_patterns:
                    continue
                if pattern.pattern in search_window:
                    pattern_matches.append(pattern)
                    seen_patterns.add(key)

            if max_pattern_len > 1:
                tail = search_window[-(max_pattern_len - 1) :]
            else:
                tail = b""

    return FileScanContent(
        size_bytes=size_bytes,
        hashes={"md5": md5.hexdigest(), "sha256": sha256.hexdigest()},
        pattern_matches=tuple(pattern_matches),
        heuristic_sample=b"".join(sample_parts),
    )
