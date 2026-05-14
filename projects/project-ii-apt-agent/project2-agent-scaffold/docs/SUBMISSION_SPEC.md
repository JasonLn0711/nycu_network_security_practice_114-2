# Project II Submission SPEC

Date: 2026-05-14
Scope: Project II / Phase II Medium EC submission package
Status: protocol-complete partial package unless IC-side success is later
observed

## 1. Purpose

This SPEC defines the current submission target for the Project II external
container (`EC`) package.

The submission has two possible states:

| State | Meaning |
| --- | --- |
| Protocol-complete partial | EC interfaces, shared-volume workflow, state/logging, safety, readiness, and packaging are complete, but `/shared/success.txt` has not appeared through the official IC. |
| Full-credit complete | Everything in protocol-complete partial plus official IC-side `/shared/success.txt` evidence. |

The current state is **protocol-complete partial**.

## 2. Actors And Systems

| Actor/System | Responsibility |
| --- | --- |
| Student EC | Provides `/exploit` and `/triage`. |
| Official IC | Runs the supplied Phase II `/blogic` and owns `/backdoor`. |
| Shared volume | Provides `/shared/config.data`, `/shared/exploit_done`, `/shared/coredump/`, state, and logs. |
| Grader | Repeatedly runs EC entry points and checks for official success. |
| TA / instructor | Confirms final submission format and grading expectations. |

## 3. Submission Package Requirements

### R-001: Source Build Context

The source package must include:

- `Dockerfile`;
- `exploit`;
- `triage`;
- `src/`;
- `scripts/`;
- `docs/`;
- `README.md`.

Acceptance:

```sh
./scripts/build_submission_package.sh
```

must create a zip containing the required source files and docs.

### R-002: Container Entry Points

The Docker image must expose:

```text
/exploit
/triage
```

Acceptance:

```sh
./scripts/run_static_checks.sh
docker build -t project2-agent-submission .
```

### R-003: `/exploit` Protocol

`/exploit` must:

- run without interactive input;
- check required `/shared` paths;
- write `/shared/config.data`;
- write the config before signaling;
- create `/shared/exploit_done`;
- update state and logs;
- exit cleanly or fail with a meaningful nonzero status.

Acceptance evidence:

- `round_log.jsonl`;
- `triage_state.json`;
- readiness report;
- mock grader run.

### R-004: `/triage` Protocol

`/triage` must:

- run without interactive input;
- tolerate no coredump;
- detect coredump files when present;
- select evidence deterministically;
- write safe state updates;
- avoid raw coredump dumps in logs;
- exit cleanly or fail with a meaningful nonzero status.

Acceptance evidence:

- state update after no-coredump case;
- state update after fake-coredump mock case;
- readiness report.

### R-005: State And Logs

The package must use:

```text
/shared/triage_state.json
/shared/round_log.jsonl
```

State must be parseable JSON. Logs must be JSONL.

Acceptance:

```sh
./scripts/generate_readiness_report.sh
```

must report:

```text
ready-for-protocol-demo
```

### R-006: Safety Boundary

The package must not:

- create `/shared/success.txt` from EC;
- manually invoke `/backdoor`;
- modify grader or IC images;
- require external network access;
- modify host paths;
- include real-world attack instructions.

Acceptance evidence:

- `docs/SAFETY_BOUNDARY.md`;
- `docs/COMPLETION_AUDIT.md`;
- `docs/PARTIAL_SUBMISSION_BRIEF.md`;
- readiness report with no hard failures.

### R-007: Completion Honesty

If `/shared/success.txt` has not appeared through the official IC flow, docs and
submission notes must state the remaining gap.

Acceptance evidence:

- `docs/PARTIAL_SUBMISSION_BRIEF.md`;
- `docs/TA_CLARIFICATION_DRAFT.md`;
- `docs/PHASE2_SUCCESS_VALIDATION.md`;
- `docs/REQUIREMENTS_TRACEABILITY.md`.

## 4. Full-Credit Acceptance Criteria

Full-credit completion requires:

1. EC builds or loads in the expected grading environment.
2. `/exploit` and `/triage` run under the official grader.
3. IC consumes `/shared/exploit_done`.
4. IC-side `/backdoor` creates `/shared/success.txt`.
5. EC does not fabricate success.
6. The result is repeatable enough for grading.
7. Evidence is saved and docs are updated.

Until item 4 is true, the package remains protocol-complete partial.

## 5. Current Evidence Matrix

| Requirement | Current status | Evidence |
| --- | --- | --- |
| EC wrappers | Complete | `exploit`, `triage`, static checks |
| Docker build context | Complete | `Dockerfile`, package zip |
| Shared protocol | Complete | readiness report, mock grader |
| State/logging | Complete | `triage_state.json`, `round_log.jsonl` |
| Safety boundary | Complete | safety docs, no fake success |
| Phase II success | Not complete | no IC-side `/shared/success.txt` |
| Submission brief | Complete | `PARTIAL_SUBMISSION_BRIEF.md` |
| TA clarification draft | Complete | `TA_CLARIFICATION_DRAFT.md` |

## 6. Final Gate Commands

Run from `project2-agent-scaffold/`:

```sh
git diff --check
./scripts/run_static_checks.sh
python3 -m compileall -q src
./scripts/generate_readiness_report.sh
./scripts/build_submission_package.sh
```

Optional image package:

```sh
./scripts/build_submission_image.sh
```

## 7. Change Rule

Do not change the completion state from protocol-complete partial to full-credit
complete unless a new official IC validation run creates `/shared/success.txt`
without EC-side fabrication.
