#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from time import perf_counter
from typing import Any

from sentinel.matchers import PatternScanEngine
from sentinel.signatures import parse_signature_database


DEFAULT_PATTERN_COUNT = 128
DEFAULT_PAYLOAD_SIZE = 512 * 1024
DEFAULT_REPETITIONS = 5
SEED = 20260422


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a safe synthetic benchmark for Sentinel pattern matching.",
    )
    parser.add_argument("--patterns", type=int, default=DEFAULT_PATTERN_COUNT)
    parser.add_argument("--payload-size", type=int, default=DEFAULT_PAYLOAD_SIZE)
    parser.add_argument("--repetitions", type=int, default=DEFAULT_REPETITIONS)
    parser.add_argument("--json-output", default="reports/pattern-benchmark.json")
    parser.add_argument("--markdown-output", default="reports/pattern-benchmark.md")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = run_benchmark(
        pattern_count=args.patterns,
        payload_size=args.payload_size,
        repetitions=args.repetitions,
    )
    write_json(result, Path(args.json_output))
    write_markdown(result, Path(args.markdown_output))
    print(
        "Pattern benchmark complete: "
        f"patterns={result['config']['pattern_count']} "
        f"payload_size={result['config']['payload_size_bytes']} "
        f"aho_best_ms={result['results']['aho_corasick_best_ms']:.3f} "
        f"naive_best_ms={result['results']['naive_best_ms']:.3f}"
    )
    return 0


def run_benchmark(*, pattern_count: int, payload_size: int, repetitions: int) -> dict[str, Any]:
    if pattern_count <= 0:
        raise ValueError("pattern_count must be positive.")
    if payload_size < 1024:
        raise ValueError("payload_size must be at least 1024 bytes.")
    if repetitions <= 0:
        raise ValueError("repetitions must be positive.")

    rng = random.Random(SEED)
    pattern_bytes = _generate_patterns(rng, pattern_count)
    payload = _generate_payload(rng, payload_size, pattern_bytes[: min(8, pattern_count)])
    database = parse_signature_database(_signature_payload(pattern_bytes))
    engine = PatternScanEngine(database.patterns)

    aho_runs = [_time_call(lambda: engine.scan(payload)) for _ in range(repetitions)]
    naive_runs = [_time_call(lambda: _naive_scan(payload, database.patterns)) for _ in range(repetitions)]

    aho_matches = engine.scan(payload)
    naive_matches = _naive_scan(payload, database.patterns)
    aho_ids = sorted(match.matcher.signature.id for match in aho_matches)
    naive_ids = sorted(match.signature.id for match in naive_matches)

    return {
        "tool": "Sentinel",
        "benchmark": "safe-synthetic-pattern-matching",
        "config": {
            "seed": SEED,
            "pattern_count": pattern_count,
            "payload_size_bytes": payload_size,
            "repetitions": repetitions,
            "inserted_pattern_count": min(8, pattern_count),
            "live_malware_used": False,
        },
        "results": {
            "aho_corasick_best_ms": min(aho_runs) * 1000,
            "aho_corasick_runs_ms": [round(value * 1000, 3) for value in aho_runs],
            "naive_best_ms": min(naive_runs) * 1000,
            "naive_runs_ms": [round(value * 1000, 3) for value in naive_runs],
            "aho_corasick_matches": len(aho_matches),
            "naive_matches": len(naive_matches),
            "match_sets_equal": aho_ids == naive_ids,
            "automaton_states": engine.state_count,
        },
        "interpretation": (
            "Aho-Corasick scans the payload once with automaton state carried across bytes. "
            "For small Python-only demos, CPython's C-backed bytes search may remain competitive; "
            "the professional value here is deterministic multi-pattern behavior and explainable scaling."
        ),
    }


def write_json(result: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(result: dict[str, Any], path: Path) -> None:
    config = result["config"]
    output = result["results"]
    lines = [
        "# Sentinel Pattern-Matching Benchmark",
        "",
        "## Scope",
        "",
        "Safe synthetic benchmark only. No live malware, no network activity, and no scanned-file execution.",
        "",
        "## Configuration",
        "",
        "| Setting | Value |",
        "| --- | ---: |",
        f"| Pattern count | {config['pattern_count']} |",
        f"| Payload size bytes | {config['payload_size_bytes']} |",
        f"| Repetitions | {config['repetitions']} |",
        f"| Inserted pattern count | {config['inserted_pattern_count']} |",
        f"| Automaton states | {output['automaton_states']} |",
        "",
        "## Results",
        "",
        "| Matcher | Best ms | Matches |",
        "| --- | ---: | ---: |",
        f"| Aho-Corasick byte automaton | {output['aho_corasick_best_ms']:.3f} | {output['aho_corasick_matches']} |",
        f"| Naive per-pattern bytes search | {output['naive_best_ms']:.3f} | {output['naive_matches']} |",
        "",
        f"- Match sets equal: `{output['match_sets_equal']}`",
        f"- Interpretation: {result['interpretation']}",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def _generate_patterns(rng: random.Random, pattern_count: int) -> list[bytes]:
    patterns: set[bytes] = set()
    while len(patterns) < pattern_count:
        patterns.add(bytes(rng.getrandbits(8) for _ in range(8)))
    return sorted(patterns)


def _generate_payload(rng: random.Random, payload_size: int, inserted_patterns: list[bytes]) -> bytes:
    payload = bytearray(rng.getrandbits(8) for _ in range(payload_size))
    spacing = max(payload_size // (len(inserted_patterns) + 1), 16)
    for index, pattern in enumerate(inserted_patterns, start=1):
        start = min(index * spacing, payload_size - len(pattern))
        payload[start : start + len(pattern)] = pattern
    return bytes(payload)


def _signature_payload(patterns: list[bytes]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "signatures": [
            {
                "id": f"sig-benchmark-{index:03d}",
                "name": f"Benchmark Pattern {index:03d}",
                "category": "safe-synthetic-benchmark",
                "severity": "medium",
                "matchers": [{"type": "hex_pattern", "value": pattern.hex()}],
            }
            for index, pattern in enumerate(patterns)
        ],
    }


def _time_call(callback) -> float:
    started = perf_counter()
    callback()
    return perf_counter() - started


def _naive_scan(payload: bytes, patterns) -> list:
    return [pattern for pattern in patterns if pattern.pattern in payload]


if __name__ == "__main__":
    raise SystemExit(main())
