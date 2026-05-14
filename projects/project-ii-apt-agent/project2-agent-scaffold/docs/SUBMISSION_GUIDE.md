# Project II Submission Guide

This guide records a conservative submission plan for the external container
side of Project II.

## Recommended Artifact

Submit a compressed source/build-context package containing this directory:

```text
project2-agent-scaffold/
```

The package should include:

- `Dockerfile`
- `/exploit` wrapper source (`exploit`)
- `/triage` wrapper source (`triage`)
- `src/`
- `scripts/`
- `docs/`
- `README.md`

The current honest submission posture is documented in:

- `docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md`
- `docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md`
- `docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md`
- `docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md`
- `docs/SUBMISSION_SPEC.md`
- `docs/SUBMISSION_SDD.md`
- `docs/PARTIAL_SUBMISSION_BRIEF.md`
- `docs/TA_CLARIFICATION_DRAFT.md`
- `docs/COMPLETION_AUDIT.md`
- `docs/PHASE2_SUCCESS_VALIDATION.md`

Do **not** include generated runtime state such as:

- `mock_shared/`
- `__pycache__/`
- `.pytest_cache/`
- local Docker layers or container exports unless the instructor explicitly asks
  for a prebuilt image.

## Build And Smoke-Test Commands

From this directory:

```sh
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
docker build -t project2-agent-submission .
```

The Dockerfile exposes exact container-root entrypoints:

```text
/exploit
/triage
```

The Docker image sets:

```text
PROJECT2_ENABLE_PHASE2_PROBE=1
```

so that grading uses the Phase II lab probe instead of the documentation-only
safe placeholder.

## Local Phase II Lab Check

If the supplied `lab.zip` has been extracted and Phase II IC is running, use:

```sh
PROJECT2_SHARED_DIR=/path/to/lab/shared \
  ./scripts/run_phase2_probe_against_shared.sh
```

Then check:

```sh
ls -l /path/to/lab/shared/config.data
ls -l /path/to/lab/shared/exploit_done
ls -l /path/to/lab/shared/success.txt
```

Full-credit evidence requires `success.txt` to be produced by IC-side
`/backdoor`, not by the EC.

## Current Honest Status

As of `2026-05-14`, the source package is a protocol-complete partial package.
The EC loop, state/logging, readiness gate, packaging scripts, and bounded Phase
II validation notes are present. Official IC-side `/shared/success.txt` has not
been observed.

Do not remove this limitation from the submission notes unless a new validation
run produces `/shared/success.txt` through the official IC path.

## Packaging Command

Use the helper:

```sh
./scripts/build_submission_package.sh
```

It writes a zip archive under `dist/` and excludes generated runtime files.

If the instructor wants a prebuilt Docker image instead of source, also run:

```sh
./scripts/build_submission_image.sh
```

This writes:

```text
dist/project2-agent-submission-image-phase2.tar.gz
```

The grader can load it with:

```sh
gzip -dc project2-agent-submission-image-phase2.tar.gz | docker load
```

## What To Say If Submitting Before Final Success

If the final Phase II success condition is still not observed, do not claim full
completion. State honestly:

> The EC interface, `/exploit`/`/triage` protocol, byte-exact config writer,
> readiness report, and bounded Phase II validation attempts are implemented.
> The remaining validation item is official IC-side `/backdoor` success
> evidence. The EC does not create `/shared/success.txt` directly.

Before asking the TA or uploading a partial package, review:

```text
docs/PARTIAL_SUBMISSION_BRIEF.md
docs/TA_CLARIFICATION_DRAFT.md
docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md
docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md
docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md
docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md
docs/SUBMISSION_SPEC.md
docs/SUBMISSION_SDD.md
```
