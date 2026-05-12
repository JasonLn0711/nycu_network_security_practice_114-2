# Project II Student Checklist

Use this checklist before submitting the Project II / Phase II Medium external
container. It checks interfaces, reproducibility, logs, documentation, and the
course-lab safety boundary. It does not require writing exploit details into the
documentation.

## 1. Container Readiness

- [ ] The submitted EC can be built, loaded, or started using documented steps.
- [ ] The EC does not require internet access during grading.
- [ ] All runtime dependencies are declared in the Dockerfile or README.
- [ ] The EC does not depend on a student-local absolute path.
- [ ] The EC works with the course `/shared` mount.
- [ ] The EC does not modify the grader, IC image, host filesystem, or Docker daemon.
- [ ] Runtime output is bounded and does not fill `/shared`.

## 2. `/exploit` Readiness

- [ ] `/exploit` exists at the container root.
- [ ] `/exploit` has executable permission.
- [ ] `/exploit` runs without interactive input.
- [ ] `/exploit` checks `/shared/config.data`.
- [ ] `/exploit` handles missing `config.data` with a clear error.
- [ ] `/exploit` checks `/shared/blogic.copy` when available.
- [ ] `/exploit` does not modify `/shared/blogic.copy`.
- [ ] `/exploit` writes a candidate config to `/shared/config.data`.
- [ ] A hash or log shows that `config.data` changed when expected.
- [ ] `/exploit` writes config safely before signaling.
- [ ] `/exploit` creates exactly `/shared/exploit_done`.
- [ ] `/exploit` does not create `exploit_done` before config write completion.
- [ ] `/exploit` exits cleanly per round.
- [ ] `/exploit` returns meaningful exit codes.

## 3. `/triage` Readiness

- [ ] `/triage` exists at the container root.
- [ ] `/triage` has executable permission.
- [ ] `/triage` runs without interactive input.
- [ ] `/triage` handles an empty `/shared/coredump/` directory.
- [ ] `/triage` detects files under `/shared/coredump/*` when present.
- [ ] `/triage` selects a coredump by a deterministic rule.
- [ ] `/triage` logs which evidence file was considered.
- [ ] `/triage` writes or updates `/shared/triage_state.json`.
- [ ] `/triage` exits cleanly even when evidence is missing or malformed.
- [ ] `/triage` does not require external services or manual analysis during grading.

## 4. State And Log Readiness

- [ ] `/shared/triage_state.json` is valid JSON.
- [ ] State includes `schema_version`.
- [ ] State includes `project` and `phase`.
- [ ] State includes a round number or clear round status.
- [ ] State includes last evidence status.
- [ ] State includes a next strategy identifier.
- [ ] State uses safe placeholders or high-level summaries.
- [ ] State does not include secrets.
- [ ] State does not include external target data.
- [ ] `/exploit` reads the state file when present.
- [ ] Round logs include round, component, event, result, and timestamp.
- [ ] Logs include exit codes when relevant.
- [ ] Logs include safe hashes when useful.
- [ ] Logs are bounded in size.
- [ ] Logs do not copy raw coredump content.

## 5. Report Readiness

- [ ] README explains how to build the EC.
- [ ] README explains how to run or verify the EC locally.
- [ ] README identifies `/exploit` and `/triage` responsibilities.
- [ ] README states the Project II / Phase II Medium assumptions.
- [ ] README explains the shared-volume workflow.
- [ ] README lists dependencies.
- [ ] README explains expected logs and state files.
- [ ] README lists known limitations and failure cases.
- [ ] A sample run log is included.
- [ ] The report avoids payload details, shellcode, chains, or real-world attack instructions.
- [ ] The report states that the project is for the course Docker lab only.

## 6. Safety Readiness

- [ ] No external network connection is required during grading.
- [ ] No external callback, scan, or download is performed.
- [ ] No host paths are modified.
- [ ] No Docker daemon or socket access is used.
- [ ] No grader files are modified.
- [ ] No IC image files are modified outside the expected lab procedure.
- [ ] No fake success signal is produced.
- [ ] No unrelated student or system data is read.
- [ ] No unbounded process spawning occurs.
- [ ] No unbounded disk output occurs.
- [ ] Documentation uses safe wording such as `candidate config`, `triage evidence`, and `state update`.
- [ ] Documentation avoids unsafe wording such as real-world targets, command servers, or weaponized chains.

## 7. Final Pre-Submission Test

- [ ] Start from a clean EC container.
- [ ] Start from a clean `/shared` volume.
- [ ] Confirm `test -f /exploit && test -x /exploit`.
- [ ] Confirm `test -f /triage && test -x /triage`.
- [ ] Run `/exploit` with no stdin and confirm it exits.
- [ ] Confirm `/shared/config.data` changes when a candidate config is written.
- [ ] Confirm `/shared/exploit_done` appears after the config write.
- [ ] Run `/triage` with no coredump and confirm it exits cleanly.
- [ ] Run `/triage` with available safe placeholder evidence and confirm state updates.
- [ ] Parse `/shared/triage_state.json` as JSON.
- [ ] Inspect `/shared/round_log.jsonl` for required fields.
- [ ] Run with external network disabled if possible.
- [ ] Confirm no host files, grader files, or unrelated files are modified.
- [ ] Save sample build and run evidence.

