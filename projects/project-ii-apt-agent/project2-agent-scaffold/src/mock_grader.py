"""Classroom-only mock grader for the Project II scaffold.

This module simulates the assignment's round structure without executing any
real exploit payload and without executing /backdoor.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone

from . import path_config


def _write_if_missing(path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def prepare_mock_shared() -> None:
    path_config.SHARED_DIR.mkdir(parents=True, exist_ok=True)
    path_config.COREDUMP_DIR.mkdir(parents=True, exist_ok=True)
    _write_if_missing(path_config.CONFIG_PATH, "INITIAL_MOCK_CONFIG\n")
    _write_if_missing(path_config.BLOGIC_COPY_PATH, "MOCK_BLOGIC_COPY\n")


def _run_wrapper(name: str) -> subprocess.CompletedProcess[str]:
    wrapper = path_config.PROJECT_ROOT / name
    env = os.environ.copy()
    env["PROJECT2_SHARED_DIR"] = str(path_config.SHARED_DIR)
    return subprocess.run(
        [str(wrapper)],
        cwd=path_config.PROJECT_ROOT,
        env=env,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def _fake_coredump(round_number: int) -> None:
    path = path_config.COREDUMP_DIR / f"core.mock-round-{round_number}.txt"
    timestamp = datetime.now(timezone.utc).isoformat()
    path.write_text(
        "MOCK COREDUMP PLACEHOLDER\n"
        f"round={round_number}\n"
        f"timestamp={timestamp}\n"
        "This is classroom-only evidence. It is not a real coredump.\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Project II mock grader.")
    parser.add_argument("--rounds", type=int, default=3, help="number of mock rounds")
    args = parser.parse_args(argv)

    print("MOCK GRADER ONLY - no real exploit or backdoor execution.")
    print(f"shared_dir={path_config.SHARED_DIR}")
    prepare_mock_shared()

    for round_number in range(1, args.rounds + 1):
        print(f"\n[mock] round {round_number}: running /exploit wrapper")
        exploit_result = _run_wrapper("exploit")
        print(f"[mock] /exploit exit={exploit_result.returncode}")
        if exploit_result.stderr:
            print(exploit_result.stderr.strip(), file=sys.stderr)
        if exploit_result.returncode != 0:
            return exploit_result.returncode

        if not path_config.EXPLOIT_DONE_PATH.exists():
            print("[mock] missing exploit_done marker", file=sys.stderr)
            return 2

        print("[mock] simulating IC blogic failure with fake coredump")
        _fake_coredump(round_number)
        path_config.EXPLOIT_DONE_PATH.unlink(missing_ok=True)

        print("[mock] running /triage wrapper")
        triage_result = _run_wrapper("triage")
        print(f"[mock] /triage exit={triage_result.returncode}")
        if triage_result.stderr:
            print(triage_result.stderr.strip(), file=sys.stderr)
        if triage_result.returncode != 0:
            return triage_result.returncode

    print("\n[mock] completed mock rounds without real success claim.")
    print("[mock] inspect mock_shared/round_log.jsonl and mock_shared/triage_state.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

