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
> readiness report, and Phase II control-flow probe are implemented. The
> remaining validation item is official IC-side `/backdoor` success evidence.
