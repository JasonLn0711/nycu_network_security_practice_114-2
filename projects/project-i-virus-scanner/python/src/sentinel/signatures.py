from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .bloom import HashBloomFilter


SUPPORTED_HASH_TYPES = {"md5": 32, "sha256": 64}
SUPPORTED_MATCHER_TYPES = {*SUPPORTED_HASH_TYPES, "hex_pattern"}
SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
HEX_RE = re.compile(r"^[0-9a-fA-F]+$")


class SignatureError(ValueError):
    """Raised when a signature database is malformed."""


@dataclass(frozen=True)
class Matcher:
    type: str
    value: str


@dataclass(frozen=True)
class Signature:
    id: str
    name: str
    category: str
    severity: str
    matchers: tuple[Matcher, ...]
    notes: str = ""


@dataclass(frozen=True)
class HashMatcher:
    signature: Signature
    matcher: Matcher


@dataclass(frozen=True)
class PatternMatcher:
    signature: Signature
    matcher: Matcher
    pattern: bytes


@dataclass(frozen=True)
class SignatureDatabase:
    schema_version: str
    signatures: tuple[Signature, ...]
    hash_index: dict[str, dict[str, tuple[HashMatcher, ...]]]
    hash_filter: HashBloomFilter
    patterns: tuple[PatternMatcher, ...]


def load_signature_database(path: str | Path) -> SignatureDatabase:
    """Load and validate a JSON signature database."""
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SignatureError(f"Invalid JSON in signature database: {exc}") from exc
    except OSError as exc:
        raise SignatureError(f"Could not read signature database {source}: {exc}") from exc

    return parse_signature_database(payload)


def parse_signature_database(payload: dict[str, Any]) -> SignatureDatabase:
    if not isinstance(payload, dict):
        raise SignatureError("Signature database must be a JSON object.")

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version:
        raise SignatureError("Signature database requires a non-empty schema_version.")

    raw_signatures = payload.get("signatures")
    if not isinstance(raw_signatures, list) or not raw_signatures:
        raise SignatureError("Signature database requires a non-empty signatures list.")

    signatures: list[Signature] = []
    seen_ids: set[str] = set()
    hash_index: dict[str, dict[str, list[HashMatcher]]] = {key: {} for key in SUPPORTED_HASH_TYPES}
    patterns: list[PatternMatcher] = []

    for raw_signature in raw_signatures:
        signature = _parse_signature(raw_signature, seen_ids)
        signatures.append(signature)

        for matcher in signature.matchers:
            if matcher.type in SUPPORTED_HASH_TYPES:
                hash_index[matcher.type].setdefault(matcher.value, []).append(
                    HashMatcher(signature=signature, matcher=matcher)
                )
            elif matcher.type == "hex_pattern":
                try:
                    pattern = bytes.fromhex(matcher.value)
                except ValueError as exc:
                    raise SignatureError(f"Signature {signature.id} has invalid hex_pattern.") from exc
                patterns.append(PatternMatcher(signature=signature, matcher=matcher, pattern=pattern))

    frozen_hash_index = {
        algorithm: {digest: tuple(matchers) for digest, matchers in digest_map.items()}
        for algorithm, digest_map in hash_index.items()
    }
    hash_filter = HashBloomFilter.from_matchers(
        (algorithm, digest)
        for algorithm, digest_map in frozen_hash_index.items()
        for digest in digest_map
    )

    return SignatureDatabase(
        schema_version=schema_version,
        signatures=tuple(signatures),
        hash_index=frozen_hash_index,
        hash_filter=hash_filter,
        patterns=tuple(patterns),
    )


def _parse_signature(payload: Any, seen_ids: set[str]) -> Signature:
    if not isinstance(payload, dict):
        raise SignatureError("Each signature must be a JSON object.")

    signature_id = _required_string(payload, "id")
    if signature_id in seen_ids:
        raise SignatureError(f"Duplicate signature id: {signature_id}")
    seen_ids.add(signature_id)

    name = _required_string(payload, "name")
    category = _required_string(payload, "category")
    severity = _required_string(payload, "severity").lower()
    if severity not in SEVERITY_RANK:
        raise SignatureError(
            f"Signature {signature_id} has invalid severity {severity!r}; "
            f"use one of {', '.join(SEVERITY_RANK)}."
        )

    raw_matchers = payload.get("matchers")
    if not isinstance(raw_matchers, list) or not raw_matchers:
        raise SignatureError(f"Signature {signature_id} requires a non-empty matchers list.")

    matchers = tuple(_parse_matcher(signature_id, raw_matcher) for raw_matcher in raw_matchers)
    notes = payload.get("notes", "")
    if not isinstance(notes, str):
        raise SignatureError(f"Signature {signature_id} notes must be a string.")

    return Signature(
        id=signature_id,
        name=name,
        category=category,
        severity=severity,
        matchers=matchers,
        notes=notes,
    )


def _parse_matcher(signature_id: str, payload: Any) -> Matcher:
    if not isinstance(payload, dict):
        raise SignatureError(f"Signature {signature_id} matcher must be a JSON object.")

    matcher_type = _required_string(payload, "type").lower()
    if matcher_type not in SUPPORTED_MATCHER_TYPES:
        raise SignatureError(
            f"Signature {signature_id} has unsupported matcher type {matcher_type!r}; "
            f"use one of {', '.join(sorted(SUPPORTED_MATCHER_TYPES))}."
        )

    value = _required_string(payload, "value").lower()
    if matcher_type in SUPPORTED_HASH_TYPES:
        expected_len = SUPPORTED_HASH_TYPES[matcher_type]
        if len(value) != expected_len or not HEX_RE.match(value):
            raise SignatureError(
                f"Signature {signature_id} {matcher_type} value must be {expected_len} hex characters."
            )
    elif matcher_type == "hex_pattern":
        compact = value.replace(" ", "")
        if len(compact) < 4 or len(compact) % 2 != 0 or not HEX_RE.match(compact):
            raise SignatureError(
                f"Signature {signature_id} hex_pattern must be even-length hex with at least 2 bytes."
            )
        value = compact

    return Matcher(type=matcher_type, value=value)


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SignatureError(f"Missing or empty required field: {key}")
    return value.strip()
