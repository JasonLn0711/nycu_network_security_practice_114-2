#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


COMMANDS = [
    [
        PYTHON,
        "-m",
        "unittest",
        "discover",
        "-s",
        "python/tests",
        "-v",
    ],
    [
        PYTHON,
        "-m",
        "sentinel",
        "validate-signatures",
        "signatures/malware-signatures.json",
    ],
    [
        PYTHON,
        "-m",
        "sentinel",
        "validate-signatures",
        "signatures/eicar-reference-signature.json",
    ],
    [
        PYTHON,
        "-m",
        "sentinel",
        "scan",
        "demo/demo-tree",
        "--signatures",
        "signatures/malware-signatures.json",
        "--report",
        "reports/demo-report.json",
        "--format",
        "json",
    ],
    [
        PYTHON,
        "-m",
        "sentinel",
        "scan",
        "demo/demo-tree",
        "--signatures",
        "signatures/malware-signatures.json",
        "--report",
        "reports/demo-report.md",
        "--format",
        "markdown",
    ],
    [
        PYTHON,
        "scripts/benchmark_patterns.py",
        "--json-output",
        "reports/pattern-benchmark.json",
        "--markdown-output",
        "reports/pattern-benchmark.md",
    ],
    [
        PYTHON,
        "-m",
        "sentinel",
        "write-evidence",
        "--target",
        "demo/demo-tree",
        "--signatures",
        "signatures/malware-signatures.json",
        "--report",
        "reports/demo-report.json",
        "--report",
        "reports/demo-report.md",
        "--report",
        "reports/pattern-benchmark.json",
        "--report",
        "reports/pattern-benchmark.md",
        "--output",
        "reports/demo-evidence-manifest.json",
    ],
]


def main() -> int:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = "python/src"

    for command in COMMANDS:
        print()
        print("$ " + " ".join(command), flush=True)
        completed = subprocess.run(command, cwd=PROJECT_ROOT, env=env, check=False)
        if _allowed_detection_exit(command, completed.returncode):
            print("note: scan returned 1 because the safe mock-virus fixture was detected.")
            continue
        if completed.returncode != 0:
            return completed.returncode

    print()
    print("Demo artifacts regenerated:")
    print("- reports/demo-report.json")
    print("- reports/demo-report.md")
    print("- reports/pattern-benchmark.json")
    print("- reports/pattern-benchmark.md")
    print("- reports/demo-evidence-manifest.json")
    return 0


def _allowed_detection_exit(command: list[str], returncode: int) -> bool:
    return "scan" in command and returncode == 1


if __name__ == "__main__":
    raise SystemExit(main())
