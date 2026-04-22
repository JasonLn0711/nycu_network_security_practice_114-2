from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable


DEFAULT_HASH_FUNCTIONS = 3
MIN_BIT_COUNT = 128


@dataclass(frozen=True)
class HashBloomFilter:
    """Small Bloom filter for signature-hash membership pre-checks."""

    bit_count: int
    hash_function_count: int
    item_count: int
    bits: int

    @classmethod
    def from_matchers(
        cls,
        matcher_keys: Iterable[tuple[str, str]],
        *,
        hash_function_count: int = DEFAULT_HASH_FUNCTIONS,
    ) -> "HashBloomFilter":
        keys = tuple(_normalize_key(algorithm, digest) for algorithm, digest in matcher_keys)
        bit_count = _choose_bit_count(len(keys))
        bits = 0
        for key in keys:
            for position in _positions(key, bit_count, hash_function_count):
                bits |= 1 << position
        return cls(
            bit_count=bit_count,
            hash_function_count=hash_function_count,
            item_count=len(keys),
            bits=bits,
        )

    def might_contain(self, algorithm: str, digest: str) -> bool:
        if self.item_count == 0:
            return False
        key = _normalize_key(algorithm, digest)
        return all(self.bits & (1 << position) for position in _positions(key, self.bit_count, self.hash_function_count))

    def metadata(self) -> dict[str, int | str]:
        return {
            "hash_filter": "bloom-filter",
            "hash_filter_items": self.item_count,
            "hash_filter_bits": self.bit_count,
            "hash_filter_hash_functions": self.hash_function_count,
            "hash_filter_policy": "precheck-then-exact-hash-map",
        }


def _choose_bit_count(item_count: int) -> int:
    if item_count <= 0:
        return MIN_BIT_COUNT
    return max(MIN_BIT_COUNT, item_count * 16)


def _positions(key: str, bit_count: int, hash_function_count: int) -> tuple[int, ...]:
    positions: list[int] = []
    for salt in range(hash_function_count):
        digest = hashlib.sha256(f"{salt}:{key}".encode("utf-8")).digest()
        positions.append(int.from_bytes(digest[:8], "big") % bit_count)
    return tuple(positions)


def _normalize_key(algorithm: str, digest: str) -> str:
    return f"{algorithm.lower()}:{digest.lower()}"
