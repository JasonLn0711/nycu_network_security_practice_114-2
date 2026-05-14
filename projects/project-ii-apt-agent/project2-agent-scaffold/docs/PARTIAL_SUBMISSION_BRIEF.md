# Project II Partial Submission Brief

Date: 2026-05-14
Target: Project II / Phase II Medium external container
Status: protocol-complete partial package; official IC-side success not yet
observed

## Direct Status

This package should not be described as full-credit complete yet.

Implemented and verified:

- `/exploit` and `/triage` wrappers exist and are executable.
- Docker build context exposes container-root `/exploit` and `/triage`.
- `/exploit` writes `/shared/config.data` atomically and then creates
  `/shared/exploit_done`.
- `/triage` handles no-coredump and coredump-present feedback and updates
  `/shared/triage_state.json`.
- State and logs are JSON / JSONL and support round-by-round review.
- Runtime behavior is local to the controlled EC/IC Docker lab and `/shared`.
- The code does not create `/shared/success.txt` from EC.

Remaining full-credit gap:

- the official IC has not produced `/shared/success.txt` through its
  `/backdoor` path.

## Evidence Files

Use these files as the audit trail:

| Evidence file | Purpose |
| --- | --- |
| `docs/COMPLETION_AUDIT.md` | Current completion verdict and remaining gap. |
| `docs/PHASE2_SUCCESS_VALIDATION.md` | Chronological validation log for IC-side success attempts. |
| `docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md` | Deep sweep/NX pass and current boundary. |
| `docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md` | Saved-RBP / argument-control boundary. |
| `docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md` | Single-target and caller-stack staging boundary. |
| `docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md` | Heap/global-state feasibility boundary. |
| `docs/REQUIREMENTS_TRACEABILITY.md` | Requirement coverage and current grade risk. |
| `mock_shared/readiness_report.json` | Generated protocol-readiness report when `generate_readiness_report.sh` is run. |

Generated runtime files under `mock_shared/` are local evidence and are excluded
from the source submission zip by default.

## What This Package Claims

It is fair to claim:

```text
The EC interface, shared-volume protocol, state/logging loop, readiness report,
and bounded Phase II validation attempts are implemented and documented.
```

It is not fair to claim:

```text
Phase II success is complete.
The current candidate executes /backdoor.
The EC legitimately produced /shared/success.txt through the official IC flow.
```

## Latest Technical Boundary

The simple technical paths are narrowed:

- direct ret-to-maintenance did not produce success;
- direct stack shellcode is blocked by NX;
- broad one-shot text sweep found no success;
- saved-RBP maintenance-body entry is blocked by C-string/NUL-byte constraints;
- caller-stack staging is fixed, not attacker-controlled;
- direct heap/global-state adjacency reaches memory but crashes in `sprintf()`
  before producing a useful state change.

Further technical work should start only from a new concrete mechanism that
avoids the shared C-string constraint.

## Recommended Submission Posture

If the deadline or presentation gate arrives before IC-side success is observed,
submit as a protocol-complete partial package and state the gap plainly.

Recommended one-paragraph status:

```text
This submission provides a runnable EC scaffold for Project II Phase II. It
implements the required /exploit and /triage entry points, shared-volume writes,
exploit_done signaling, triage state, JSONL logs, readiness checks, and a
bounded set of Phase II validation attempts. The remaining gap is official
IC-side /shared/success.txt evidence; the package does not fabricate success
from the EC.
```

## Final Gate Before Upload

Run these from `project2-agent-scaffold/`:

```sh
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
./scripts/build_submission_package.sh
```

Optional, only if the instructor asks for a Docker image tarball:

```sh
./scripts/build_submission_image.sh
```

After packaging, inspect the zip listing and confirm it contains this brief,
the TA clarification draft, source files, wrappers, Dockerfile, and docs, but no
`mock_shared/`, `dist/`, `__pycache__/`, or coredumps.
