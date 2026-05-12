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
- [ ] It checks `blogic.copy`.
- [ ] It writes only safe placeholder config until student logic is added.
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
