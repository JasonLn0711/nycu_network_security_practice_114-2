# Project II Agent Scaffold

This is a classroom-safe scaffold for NYCU Network Security Project II / Phase
II Medium. It demonstrates the autonomous workflow structure expected by the
assignment without implementing a real exploit.

It includes:

- `/exploit` wrapper;
- `/triage` wrapper;
- shared-volume protocol;
- JSON state management;
- JSONL logging;
- safety guard;
- classroom-only mock grader;
- pytest tests;
- student-facing documentation.

This scaffold does not solve Project II. It does not execute `/backdoor`, does
not generate shellcode, does not build ROP chains, does not bypass the grader,
and does not connect to external networks.

## Safety Boundary

Use this scaffold only inside the controlled course Docker lab or the local
mock shared directory. Do not use it against real systems, external networks,
host machines, or third-party targets.

By default the candidate config is a safe placeholder:

```text
PROJECT2_SAFE_PLACEHOLDER_CONFIG
round=X
strategy=safe-placeholder
```

For controlled local Phase II lab experiments, `PROJECT2_ENABLE_PHASE2_PROBE=1`
enables the current byte-exact probe writer. That mode is **not** a completion
claim: it still requires official IC-side `/backdoor` validation and must not
fabricate `/shared/success.txt` from the EC.

## Repository Structure

```text
project2-agent-scaffold/
|-- README.md
|-- Dockerfile
|-- exploit
|-- triage
|-- src/
|   |-- path_config.py
|   |-- logger.py
|   |-- safety_guard.py
|   |-- state_manager.py
|   |-- environment_checker.py
|   |-- config_planner.py
|   |-- exploit_runner.py
|   |-- coredump_scanner.py
|   |-- coredump_analyzer.py
|   |-- triage_runner.py
|   `-- mock_grader.py
|-- scripts/
|   |-- run_mock_grader.sh
|   |-- run_static_checks.sh
|   |-- run_phase2_probe_against_shared.sh
|   |-- run_phase2_one_shot_sweep.py
|   `-- clean_shared.sh
|-- tests/
`-- docs/
    |-- CORE_WORKFLOW.md
    |-- TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md
    |-- PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md
    |-- PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md
    |-- PROJECT_II_ANALYSIS_REPORT_2026-05-14.md
    |-- COMPLETION_AUDIT.md
    |-- PHASE2_SUCCESS_VALIDATION.md
    |-- PHASE2_COMPLETION_ATTEMPT_2026-05-14.md
    |-- PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md
    |-- PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md
    |-- PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md
    |-- PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md
    |-- PARTIAL_SUBMISSION_BRIEF.md
    |-- TA_CLARIFICATION_DRAFT.md
    |-- SUBMISSION_SPEC.md
    |-- SUBMISSION_SDD.md
    |-- SPEC.md
    |-- SDD.md
    |-- STUDENT_CHECKLIST.md
    `-- SAFETY_BOUNDARY.md
```

Start with [docs/CORE_WORKFLOW.md](docs/CORE_WORKFLOW.md) for the step-by-step
feedback-loop view of the real assignment core.

## How `/exploit` Works

`/exploit` calls `python3 -m src.exploit_runner`.

It:

1. logs start;
2. runs safety checks;
3. checks `/shared` and the observable `blogic` artifact
   (`blogic.copy` from the brief or `blogic` from the supplied lab script);
4. loads `/shared/triage_state.json` if present;
5. increments the round;
6. calls the state-driven config planner;
7. writes `/shared/config.data` through a temp file and rename;
8. computes a SHA-256 hash;
9. updates and saves state;
10. creates `/shared/exploit_done`;
11. exits with a meaningful status.

The default planner demonstrates baseline, length-sweep, boundary-search, and
stability-check states with safe placeholder content. Phase II probe mode writes
byte-exact lab candidate bytes but is still an unfinished validation step until
IC-side `/shared/success.txt` is observed.

## How `/triage` Works

`/triage` calls `python3 -m src.triage_runner`.

It:

1. logs start;
2. runs safety checks;
3. ensures `/shared/coredump/` exists;
4. loads state;
5. scans `/shared/coredump/*`;
6. handles the no-coredump case;
7. selects the latest coredump deterministically when files exist;
8. records a safe high-level evidence summary;
9. updates `/shared/triage_state.json`;
10. exits with a meaningful status.

It does not provide exploit guidance.

## Run Static Checks

```sh
./scripts/run_static_checks.sh
```

This verifies wrappers, executable bits, docs, and Python imports.

## Run The Classroom Mock Grader

The real assignment grader uses `/shared`. For classroom demonstration, this
script defaults to a local `./mock_shared` directory:

```sh
./scripts/run_mock_grader.sh
```

Optional:

```sh
PROJECT2_SHARED_DIR=./mock_shared ./scripts/run_mock_grader.sh --rounds 3
```

The mock grader prints:

```text
MOCK GRADER ONLY - no real exploit or backdoor execution.
```

It creates mock `config.data`, mock `blogic.copy`, fake text coredumps, state,
and JSONL logs. It never executes `/backdoor` and never claims real success.

## Run Tests

If `pytest` is available:

```sh
pytest -q
```

The tests use temporary shared directories and do not require the real lab
binary.

## Docker Usage

Build locally:

```sh
docker build -t project2-agent-scaffold .
```

The image exposes:

```text
/exploit
/triage
```

The Dockerfile does not install unnecessary packages and does not require
runtime network access.


## Generate A Readiness Report

Before replacing the candidate-generation hook, run a protocol-readiness gate:

```sh
./scripts/generate_readiness_report.sh
```

This starts from a clean mock shared directory, runs two safe mock rounds, runs
static checks, and writes:

```text
mock_shared/readiness_report.json
```

The report verifies wrapper executability, required docs/modules, parseable
state, round logs, external-network safety state, and safe metadata for the
observable `blogic` artifact. It supports both names seen in the course material:
`/shared/blogic.copy` from the brief and `/shared/blogic` from the supplied lab
script. The report is a protocol-readiness check only; it does not claim exploit
success.


## Phase II Probe Mode

The scaffold now supports byte-exact candidate writing for controlled local lab
experiments. To run the current Phase II control-flow probe against a shared
volume:

```sh
PROJECT2_SHARED_DIR=/path/to/lab/shared \
  PROJECT2_ENABLE_PHASE2_PROBE=1 \
  ./scripts/run_phase2_probe_against_shared.sh
```

The current probe is not a success claim. It is a lab-only candidate-generation
step that keeps the EC protocol honest: it writes `config.data`, signals
`exploit_done`, and does not fabricate `/shared/success.txt`. See
`docs/COMPLETION_AUDIT.md` and `docs/PHASE2_SUCCESS_VALIDATION.md` for the
current missing full-credit item and the latest official-IC validation evidence.

The latest deep validation pass is recorded in
`docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`. That pass reproduced the Phase
II IC in an x86_64 Colima Docker VM, confirmed the current ret-to-maintenance
candidate still does not trigger IC-side `/backdoor`, confirmed stack shellcode
is blocked by NX, and preserved the bounded one-shot text sweep as:

```sh
python3 scripts/run_phase2_one_shot_sweep.py
```

Run that sweep only inside the supplied course IC container. It does not create
`/shared/success.txt` and does not invoke `/backdoor`; it only checks whether a
candidate caused the official IC-side success artifact to appear.

Later bounded attempts are recorded in:

- `docs/PHASE2_EXPERIMENT_LOG.md`
- `docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`
- `docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`
- `docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`
- `docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md`
- `docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`
- `docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md`
- `docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md`
- `docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md`

`docs/PHASE2_EXPERIMENT_LOG.md` is now the canonical ledger. Every new
full-credit recovery experiment, successful or failed, must add a stable
experiment ID, hypothesis, environment, procedure, observation, verdict, and
evidence link there before the next experiment starts.

The 2026-05-15 pass adds a selectable multi-line staging probe:

```sh
PROJECT2_SHARED_DIR=/path/to/lab/shared \
  PROJECT2_ENABLE_PHASE2_PROBE=1 \
  PROJECT2_PHASE2_STRATEGY=multiline-staging \
  ./scripts/run_phase2_probe_against_shared.sh
```

This confirms a useful parser primitive but remains a bounded recovery probe,
not a completion claim.

The later 2026-05-15 register-reuse block tested
`PROJECT2_PHASE2_STRATEGY=register-reuse-system-rax`. It reached the selected
`system()` tail path, produced no `/shared/success.txt`, and is now closed as a
direct full-credit route.

The next 2026-05-15 backward-pivot feasibility block checked the fresh Phase II
main binary plus pinned libc for a narrow first-stage pivot family that could
move `rsp` back into controlled pre-RIP stack bytes. No usable gadget in that
family was found, so no live EC candidate exists for that hypothesis.

The later 2026-05-15 current-`rdi` argument block tested
`PROJECT2_PHASE2_STRATEGY=current-rdi-system`. It returned directly to
`system@plt` without appended ROP, saved RBP, or direct `rax` reuse. The IC
produced no `/shared/success.txt`; the core showed `system()` received an empty
libc lock pointer, not controlled `user_input`.

The current submission posture is summarized in
`docs/PARTIAL_SUBMISSION_BRIEF.md`. A concise TA-facing clarification draft is
available in `docs/TA_CLARIFICATION_DRAFT.md`.

The next executable action is tracked in
`docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md`. Use that runbook to choose
between TA clarification, partial upload, Docker image fallback, and bounded
full-credit recovery.

The concrete upload/TA message packet is
`docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md`.

The direct teacher-requirements completion verdict is
`docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md`.

For a fuller decision-grade view, read
`docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md`,
`docs/SUBMISSION_SPEC.md`, and `docs/SUBMISSION_SDD.md`.

## What Students Must Implement

Students must finish or replace the candidate-generation hook with
instructor-approved course-lab-specific logic:

```text
src/config_planner.py
```

The safe default path deliberately keeps this TODO boundary visible:

```text
TODO: Student implements course-lab-specific candidate generation here. Do not
use this scaffold outside the controlled Docker lab.
```

Do not add general-purpose exploitation guidance to the docs. Keep reports
focused on interfaces, state, logs, reproducibility, the lab-only boundary, and
whether the official IC-side success condition has actually been observed.


## Submission Packaging

Before submission, read:

- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/SUBMISSION_GUIDE.md`
- `docs/COMPLETION_AUDIT.md`
- `docs/PHASE2_SUCCESS_VALIDATION.md`

Build a clean source package with:

```sh
./scripts/build_submission_package.sh
# Optional if a prebuilt Docker image is required:
./scripts/build_submission_image.sh
```

The package helper excludes generated runtime state such as `mock_shared/` and writes a
zip archive under `dist/`. The image helper writes a gzipped `docker save` tarball
under `dist/`.

## Grading Readiness Checklist

- [ ] `/exploit` exists and is executable in the EC.
- [ ] `/triage` exists and is executable in the EC.
- [ ] Both wrappers are noninteractive.
- [ ] `/exploit` writes `/shared/config.data`.
- [ ] `/exploit` creates `/shared/exploit_done` after config write completion.
- [ ] `/triage` handles no-coredump and coredump cases.
- [ ] `/triage` writes valid `/shared/triage_state.json`.
- [ ] Logs are written to `/shared/round_log.jsonl`.
- [ ] No external network dependency exists during grading.
- [ ] No host, grader, or IC image tampering exists.
- [ ] Official IC-side `/backdoor` creates `/shared/success.txt` before any
      full-credit completion claim is made.
