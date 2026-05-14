"""Generate a bounded Project II grading-readiness report.

The report is meant to answer: can this external-container scaffold expose the
right entry points, write/read the shared-volume protocol, and leave auditable
state? It does not attempt to prove exploit success and does not inspect payload
internals.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import path_config
from .blogic_metadata import collect_blogic_metadata


REQUIRED_DOCS = [
    "README.md",
    "Dockerfile",
    "docs/SPEC.md",
    "docs/SDD.md",
    "docs/STUDENT_CHECKLIST.md",
    "docs/SAFETY_BOUNDARY.md",
    "docs/CORE_WORKFLOW.md",
    "docs/COMPLETION_AUDIT.md",
    "docs/PHASE2_SUCCESS_VALIDATION.md",
    "docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md",
    "docs/REQUIREMENTS_TRACEABILITY.md",
    "docs/SUBMISSION_GUIDE.md",
    "docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md",
    "docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md",
    "docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md",
    "docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md",
    "docs/SUBMISSION_SPEC.md",
    "docs/SUBMISSION_SDD.md",
    "docs/PARTIAL_SUBMISSION_BRIEF.md",
    "docs/TA_CLARIFICATION_DRAFT.md",
]

REQUIRED_MODULES = [
    "src/path_config.py",
    "src/logger.py",
    "src/safety_guard.py",
    "src/state_manager.py",
    "src/environment_checker.py",
    "src/blogic_metadata.py",
    "src/phase2_payload.py",
    "src/config_planner.py",
    "src/exploit_runner.py",
    "src/coredump_scanner.py",
    "src/coredump_analyzer.py",
    "src/triage_runner.py",
    "src/mock_grader.py",
    "src/readiness_report.py",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_executable(path: Path) -> bool:
    try:
        mode = path.stat().st_mode
    except OSError:
        return False
    return bool(mode & stat.S_IXUSR)


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _count_jsonl(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for line in handle if line.strip())
    except OSError:
        return 0


def _grep_external_network_dependency(root: Path) -> list[str]:
    """Return suspicious runtime network strings from source/docs.

    This is intentionally a simple heuristic. It does not read generated shared
    outputs and it does not fail the build by itself; the report flags it for
    review.
    """

    suspicious: list[str] = []
    tokens = ("curl ", "wget ", "nc ", "ncat ", "ssh ", "http://", "https://")
    for rel in [*REQUIRED_DOCS, *REQUIRED_MODULES, "exploit", "triage"]:
        # Avoid self-reporting the token list used by this heuristic.
        if rel == "src/readiness_report.py":
            continue
        path = root / rel
        if not path.exists() or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in tokens:
            if token in text:
                suspicious.append(f"{rel}: contains {token.strip()}")
    return suspicious


def _run_static_checks(root: Path) -> dict[str, Any]:
    script = root / "scripts" / "run_static_checks.sh"
    if not script.exists():
        return {"ran": False, "ok": False, "reason": "missing scripts/run_static_checks.sh"}
    result = subprocess.run(
        [str(script)],
        cwd=root,
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    return {
        "ran": True,
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-5:],
        "stderr_tail": result.stderr.strip().splitlines()[-5:],
    }


def build_report(*, run_static: bool = False) -> dict[str, Any]:
    root = path_config.PROJECT_ROOT
    shared = path_config.SHARED_DIR
    state = _read_json(path_config.STATE_PATH)
    round_log_events = _count_jsonl(path_config.ROUND_LOG_PATH)

    wrappers = {
        name: {
            "exists": (root / name).is_file(),
            "executable": _is_executable(root / name),
            "container_path": f"/{name}",
        }
        for name in ["exploit", "triage"]
    }
    docs = {rel: (root / rel).is_file() for rel in REQUIRED_DOCS}
    modules = {rel: (root / rel).is_file() for rel in REQUIRED_MODULES}

    protocol_checks = {
        "shared_dir_exists": shared.is_dir(),
        "config_exists": path_config.CONFIG_PATH.is_file(),
        "blogic_copy_exists": path_config.resolve_blogic_path().is_file(),
        "blogic_path": str(path_config.resolve_blogic_path()),
        "exploit_done_exists_now": path_config.EXPLOIT_DONE_PATH.exists(),
        "coredump_dir_exists": path_config.COREDUMP_DIR.is_dir(),
        "state_json_exists": path_config.STATE_PATH.is_file(),
        "state_json_parseable": state is not None,
        "round_log_exists": path_config.ROUND_LOG_PATH.is_file(),
        "round_log_events": round_log_events,
    }

    latest_state_summary: dict[str, Any] = {}
    if state:
        latest_state_summary = {
            "schema_version": state.get("schema_version"),
            "project": state.get("project"),
            "phase": state.get("phase"),
            "round": state.get("round"),
            "last_exploit_strategy": state.get("last_exploit", {}).get("strategy_id"),
            "last_triage_status": state.get("last_triage", {}).get("analysis_status"),
            "next_strategy": state.get("next_action", {}).get("strategy_id"),
            "external_network": state.get("safety", {}).get("external_network"),
            "lab_only": state.get("safety", {}).get("lab_only"),
        }

    hard_failures: list[str] = []
    warnings: list[str] = []

    for name, info in wrappers.items():
        if not info["exists"]:
            hard_failures.append(f"/{name} wrapper missing from build context")
        elif not info["executable"]:
            hard_failures.append(f"/{name} wrapper is not executable")

    for rel, present in docs.items():
        if not present:
            warnings.append(f"missing documentation artifact: {rel}")
    for rel, present in modules.items():
        if not present:
            hard_failures.append(f"missing source module: {rel}")

    if protocol_checks["state_json_exists"] and not protocol_checks["state_json_parseable"]:
        hard_failures.append("triage_state.json exists but is not valid JSON")
    if state and latest_state_summary.get("external_network") is not False:
        hard_failures.append("state does not assert external_network=false")
    if state and latest_state_summary.get("lab_only") is not True:
        warnings.append("state does not assert lab_only=true")

    suspicious_network = _grep_external_network_dependency(root)
    if suspicious_network:
        warnings.extend([f"review network dependency: {item}" for item in suspicious_network])

    static_checks = _run_static_checks(root) if run_static else {"ran": False}
    if static_checks.get("ran") and not static_checks.get("ok"):
        hard_failures.append("static checks failed")

    status = "ready-for-protocol-demo"
    if hard_failures:
        status = "blocked"
    elif warnings:
        status = "needs-review"

    return {
        "generated_at": _utc_now(),
        "status": status,
        "scope": "Project II Phase II EC protocol readiness; not exploit success",
        "project_root": str(root),
        "shared_dir": str(shared),
        "wrappers": wrappers,
        "docs": docs,
        "modules": modules,
        "protocol_checks": protocol_checks,
        "latest_state_summary": latest_state_summary,
        "blogic_metadata": collect_blogic_metadata(path_config.resolve_blogic_path()).to_dict(),
        "static_checks": static_checks,
        "hard_failures": hard_failures,
        "warnings": warnings,
        "next_step_after_this_report": (
            "Use this report to keep /exploit and /triage packaging stable, then replace "
            "src/config_planner.py with instructor-approved Phase II lab logic inside the Docker lab."
        ),
    }


def write_report(report: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(output) + ".tmp")
    tmp.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Project II readiness report")
    parser.add_argument(
        "--output",
        type=Path,
        default=path_config.SHARED_DIR / "readiness_report.json",
        help="report output path; defaults to shared/readiness_report.json",
    )
    parser.add_argument(
        "--run-static",
        action="store_true",
        help="also run scripts/run_static_checks.sh",
    )
    args = parser.parse_args(argv)

    report = build_report(run_static=args.run_static)
    write_report(report, args.output)
    print(f"readiness_report={args.output}")
    print(f"status={report['status']}")
    if report["hard_failures"]:
        print("hard_failures:", file=sys.stderr)
        for item in report["hard_failures"]:
            print(f"- {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
