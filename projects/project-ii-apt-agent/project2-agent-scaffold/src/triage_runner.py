"""Classroom-safe /triage runner for the Project II scaffold."""

from __future__ import annotations

import sys

from .coredump_scanner import (
    list_coredumps,
    select_latest_coredump,
    summarize_coredump_safely,
)
from .coredump_analyzer import decide_next_action
from .environment_checker import EnvironmentCheckError, check_required_paths_for_triage
from .logger import log_event
from .safety_guard import SafetyError, run_safety_checks
from .state_manager import load_state, save_state, update_after_triage


def main() -> int:
    try:
        log_event("triage", "start", True)
        run_safety_checks()
        status = check_required_paths_for_triage()
        log_event("triage", "environment_checked", True, status.__dict__)

        state = load_state()
        coredumps = list_coredumps()
        log_event("triage", "coredumps_scanned", True, {"count": len(coredumps)})

        if not coredumps:
            summary = "No coredump evidence available."
            decision = decide_next_action(
                state,
                coredump_found=False,
                selected_coredump="",
                evidence_summary=summary,
            )
            state = update_after_triage(
                state,
                coredump_found=False,
                selected_coredump="",
                summary=summary,
                next_action=decision["next_action"],
                search_state=decision["search_state"],
            )
            log_event(
                "triage",
                "no_coredump",
                True,
                {
                    "summary": summary,
                    "next_action": decision["next_action"],
                },
            )
        else:
            selected = select_latest_coredump(coredumps)
            assert selected is not None
            evidence = summarize_coredump_safely(selected)
            decision = decide_next_action(
                state,
                coredump_found=True,
                selected_coredump=str(selected),
                evidence_summary=evidence["summary"],
            )
            state = update_after_triage(
                state,
                coredump_found=True,
                selected_coredump=str(selected),
                summary=evidence["summary"],
                next_action=decision["next_action"],
                search_state=decision["search_state"],
            )
            log_event(
                "triage",
                "coredump_selected",
                True,
                {
                    **evidence,
                    "next_action": decision["next_action"],
                },
            )

        save_state(state)
        log_event("triage", "state_saved", True, {"round": state.get("round")})
        log_event("triage", "success", True, {"exit_code": 0})
        return 0
    except (EnvironmentCheckError, SafetyError, OSError, ValueError) as exc:
        log_event("triage", "error", False, {"error": str(exc), "exit_code": 1})
        print(f"/triage scaffold error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
