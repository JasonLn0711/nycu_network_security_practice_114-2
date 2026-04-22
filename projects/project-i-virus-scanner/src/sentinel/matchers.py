from __future__ import annotations

from collections import deque
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
    pattern_matches: tuple["PatternScanMatch", ...]
    heuristic_sample: bytes


@dataclass(frozen=True)
class PatternScanMatch:
    matcher: PatternMatcher
    offset: int


@dataclass
class _AutomatonNode:
    transitions: dict[int, int]
    failure: int
    outputs: list[PatternMatcher]


class PatternScanEngine:
    """Aho-Corasick byte-pattern scanner for many signatures in one pass."""

    def __init__(self, patterns: tuple[PatternMatcher, ...]):
        self.patterns = patterns
        self._nodes = [_AutomatonNode(transitions={}, failure=0, outputs=[])]
        self._build_trie(patterns)
        self._build_failure_links()

    @property
    def state_count(self) -> int:
        return len(self._nodes)

    def metadata(self) -> dict[str, int | str]:
        return {
            "pattern_engine": "aho-corasick-byte-automaton",
            "pattern_count": len(self.patterns),
            "automaton_states": self.state_count,
            "chunk_size_bytes": CHUNK_SIZE,
            "heuristic_sample_limit_bytes": HEURISTIC_SAMPLE_LIMIT,
        }

    def stream(self) -> "PatternStreamScanner":
        return PatternStreamScanner(self)

    def scan(self, data: bytes) -> tuple[PatternScanMatch, ...]:
        scanner = self.stream()
        scanner.feed(data)
        return scanner.finish()

    def _build_trie(self, patterns: tuple[PatternMatcher, ...]) -> None:
        for pattern_matcher in patterns:
            state = 0
            for byte in pattern_matcher.pattern:
                next_state = self._nodes[state].transitions.get(byte)
                if next_state is None:
                    next_state = len(self._nodes)
                    self._nodes[state].transitions[byte] = next_state
                    self._nodes.append(_AutomatonNode(transitions={}, failure=0, outputs=[]))
                state = next_state
            self._nodes[state].outputs.append(pattern_matcher)

    def _build_failure_links(self) -> None:
        queue: deque[int] = deque()
        for next_state in self._nodes[0].transitions.values():
            self._nodes[next_state].failure = 0
            queue.append(next_state)

        while queue:
            state = queue.popleft()
            for byte, next_state in self._nodes[state].transitions.items():
                queue.append(next_state)
                fallback = self._nodes[state].failure
                while fallback and byte not in self._nodes[fallback].transitions:
                    fallback = self._nodes[fallback].failure
                self._nodes[next_state].failure = self._nodes[fallback].transitions.get(byte, 0)
                self._nodes[next_state].outputs.extend(self._nodes[self._nodes[next_state].failure].outputs)


class PatternStreamScanner:
    def __init__(self, engine: PatternScanEngine):
        self._engine = engine
        self._state = 0
        self._position = 0
        self._seen: set[tuple[str, str, str]] = set()
        self._matches: list[PatternScanMatch] = []

    def feed(self, data: bytes) -> None:
        for byte in data:
            while self._state and byte not in self._engine._nodes[self._state].transitions:
                self._state = self._engine._nodes[self._state].failure
            self._state = self._engine._nodes[self._state].transitions.get(byte, 0)

            for pattern_matcher in self._engine._nodes[self._state].outputs:
                key = _pattern_key(pattern_matcher)
                if key in self._seen:
                    continue
                self._seen.add(key)
                offset = self._position - len(pattern_matcher.pattern) + 1
                self._matches.append(PatternScanMatch(matcher=pattern_matcher, offset=offset))

            self._position += 1

    def finish(self) -> tuple[PatternScanMatch, ...]:
        return tuple(self._matches)


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
        if not database.hash_filter.might_contain(algorithm, digest):
            continue
        matches.extend(database.hash_index.get(algorithm, {}).get(digest, ()))
    return matches


def find_pattern_matches(data: bytes, database: SignatureDatabase) -> list[PatternMatcher]:
    engine = PatternScanEngine(database.patterns)
    return [match.matcher for match in engine.scan(data)]


def scan_file_content(
    path: Path,
    database: SignatureDatabase,
    *,
    pattern_engine: PatternScanEngine | None = None,
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
    engine = pattern_engine or PatternScanEngine(database.patterns)
    pattern_scanner = engine.stream()

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

            pattern_scanner.feed(chunk)

    return FileScanContent(
        size_bytes=size_bytes,
        hashes={"md5": md5.hexdigest(), "sha256": sha256.hexdigest()},
        pattern_matches=pattern_scanner.finish(),
        heuristic_sample=b"".join(sample_parts),
    )


def _pattern_key(pattern_matcher: PatternMatcher) -> tuple[str, str, str]:
    return (
        pattern_matcher.signature.id,
        pattern_matcher.matcher.type,
        pattern_matcher.matcher.value,
    )
