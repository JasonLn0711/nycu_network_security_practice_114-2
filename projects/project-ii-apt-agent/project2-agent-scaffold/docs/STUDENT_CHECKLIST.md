# Project II Scaffold Student Checklist

## Container Readiness

- [ ] EC builds or loads using documented steps.
- [ ] `/exploit` exists in the container.
- [ ] `/triage` exists in the container.
- [ ] No runtime internet dependency exists.
- [ ] Dependencies are declared.

## `/exploit` Readiness

- [ ] Wrapper is executable.
- [ ] Wrapper calls `python3 -m src.exploit_runner`.
- [ ] It checks `config.data`.
- [ ] It checks `blogic.copy` or supplied-lab `blogic`.
- [ ] It writes safe placeholder config by default.
- [ ] If Phase II probe mode is enabled, it is labeled as a lab-only candidate
      and not a completion claim.
- [ ] It creates `exploit_done` after config write.
- [ ] It logs events.
- [ ] It exits with meaningful status.

## `/triage` Readiness

- [ ] Wrapper is executable.
- [ ] Wrapper calls `python3 -m src.triage_runner`.
- [ ] It handles no coredump.
- [ ] It detects fake or real lab coredump files.
- [ ] It selects latest coredump deterministically.
- [ ] It writes safe state updates.
- [ ] It logs events.

## State And Log Readiness

- [ ] `triage_state.json` is valid JSON.
- [ ] `round_log.jsonl` is JSONL.
- [ ] State uses safe placeholders and summaries.
- [ ] `next_action.strategy_id` changes based on coredump/no-coredump evidence.
- [ ] `last_exploit.input_profile` records the candidate profile used.
- [ ] `search_state.avoid_repeating_hashes` or equivalent logic prevents repeated identical candidates.
- [ ] Logs do not include secrets or payload details.

## Report Readiness

- [ ] README says this scaffold is not a solution.
- [ ] README explains mock grader.
- [ ] README explains tests.
- [ ] README explains the TODO hook.
- [ ] `docs/COMPLETION_AUDIT.md` states that IC-side success is not observed
      unless `/shared/success.txt` has actually appeared.
- [ ] `docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md` has been
      reviewed before claiming teacher requirements are complete.
- [ ] `docs/PARTIAL_SUBMISSION_BRIEF.md` is reviewed before any partial upload.
- [ ] `docs/TA_CLARIFICATION_DRAFT.md` is ready if TA clarification is needed.
- [ ] `docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md` has been used
      for the TA message or LMS upload wording.
- [ ] `docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md` has been used to choose
      the next route.
- [ ] Negative Phase II evidence is linked rather than hidden.

## Safety Readiness

- [ ] No shellcode.
- [ ] No ROP chains.
- [ ] No `/backdoor` execution.
- [ ] No external network callbacks.
- [ ] No grader tampering.
- [ ] No host modification.

## Final Test

- [ ] `./scripts/run_static_checks.sh` passes.
- [ ] `pytest -q` passes if pytest is installed.
- [ ] `./scripts/run_mock_grader.sh` demonstrates the workflow.
- [ ] `./scripts/generate_readiness_report.sh` reports
      `ready-for-protocol-demo`.
- [ ] `./scripts/build_submission_package.sh` creates a zip with no
      `mock_shared/`, `dist/`, `__pycache__/`, or coredumps.
