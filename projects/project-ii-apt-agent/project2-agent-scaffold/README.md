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

The only candidate config generated here is a safe placeholder:

```text
PROJECT2_SAFE_PLACEHOLDER_CONFIG
round=X
strategy=safe-placeholder
```

The course-lab-specific candidate generation hook is intentionally left as a
TODO in `src/config_planner.py`.

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
|   `-- clean_shared.sh
|-- tests/
`-- docs/
    |-- CORE_WORKFLOW.md
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
3. checks `/shared/config.data` and `/shared/blogic.copy`;
4. loads `/shared/triage_state.json` if present;
5. increments the round;
6. calls the state-driven safe placeholder config planner;
7. writes `/shared/config.data` through a temp file and rename;
8. computes a SHA-256 hash;
9. updates and saves state;
10. creates `/shared/exploit_done`;
11. exits with a meaningful status.

It does not contain real exploit logic. The planner demonstrates baseline,
length-sweep, boundary-search, and stability-check states with safe placeholder
content only.

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

## What Students Must Implement

Students must replace only the safe candidate-generation hook with
course-lab-specific logic allowed by the instructor:

```text
src/config_planner.py
```

The scaffold deliberately leaves this TODO:

```text
TODO: Student implements course-lab-specific candidate generation here. Do not
use this scaffold outside the controlled Docker lab.
```

Do not add payload details to the docs. Keep reports focused on interfaces,
state, logs, reproducibility, and lab-only safety.

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
