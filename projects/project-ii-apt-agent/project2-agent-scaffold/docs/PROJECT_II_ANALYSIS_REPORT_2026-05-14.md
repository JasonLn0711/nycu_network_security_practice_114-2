# Project II Analysis Report - Current State

Date: 2026-05-14
Target: NYCU Network Security Practice Project II / Phase II Medium
Repository area: `projects/project-ii-apt-agent/project2-agent-scaffold/`

## Executive Verdict

The project is currently a **protocol-complete partial submission**, not a
full-credit Phase II completion.

We have built and verified the external-container (`EC`) interface expected by
the assignment:

- runnable `/exploit`;
- runnable `/triage`;
- shared-volume protocol;
- state and JSONL logging;
- coredump/no-coredump feedback loop;
- Docker build context;
- readiness report;
- clean source-package builder;
- safety boundary and audit notes.

The remaining full-credit gap is specific and measurable:

```text
The official internal container has not produced /shared/success.txt through
its /backdoor path.
```

Until that artifact appears through the official IC flow, the submission must
not claim Phase II success.

## What We Have Completed

### 1. Course Artifact Routing

Completed:

- preserved the official `lab.zip` and `project-brief.pdf`;
- created a searchable lab manifest;
- kept Project II material under `projects/project-ii-apt-agent/`;
- kept generated runtime files out of git.

Important files:

| File | Role |
| --- | --- |
| `../project-brief.pdf` | Official brief. |
| `../lab.zip` | Official lab bundle. |
| `../lab-manifest.md` | Searchable inventory of the lab bundle. |
| `../../README.md` | Project-level routing and current checkpoint. |

### 2. EC Protocol Scaffold

Completed:

- `/exploit` wrapper exists and is executable;
- `/triage` wrapper exists and is executable;
- Dockerfile exposes container-root `/exploit` and `/triage`;
- `/exploit` writes `/shared/config.data`;
- `/exploit` creates `/shared/exploit_done` after the config write;
- `/triage` reads feedback from `/shared/coredump/`;
- `/triage` updates `/shared/triage_state.json`;
- both paths write structured JSONL events.

Key files:

| File | Role |
| --- | --- |
| `exploit` | Container-root `/exploit` wrapper source. |
| `triage` | Container-root `/triage` wrapper source. |
| `src/exploit_runner.py` | One-round exploit protocol coordinator. |
| `src/triage_runner.py` | One-round triage protocol coordinator. |
| `src/state_manager.py` | State schema and state updates. |
| `src/logger.py` | Round-level JSONL logging. |

### 3. Safety Boundary

Completed:

- no EC-side fake `/shared/success.txt`;
- no manual `/backdoor` invocation in the EC;
- no external network dependency;
- no host modification;
- no general-purpose offensive toolkit behavior;
- documentation states the lab-only boundary.

Key files:

| File | Role |
| --- | --- |
| `docs/SAFETY_BOUNDARY.md` | Required lab-only boundary. |
| `docs/PARTIAL_SUBMISSION_BRIEF.md` | Honest partial-submission posture. |
| `docs/TA_CLARIFICATION_DRAFT.md` | TA-facing clarification draft. |

### 4. Readiness And Packaging

Completed:

- static checks pass;
- Python source compiles;
- readiness report generates successfully;
- source zip builds successfully;
- source zip includes required docs and excludes generated runtime state.

Latest verified commands:

```sh
git diff --check
./scripts/run_static_checks.sh
python3 -m compileall -q src
./scripts/generate_readiness_report.sh
./scripts/build_submission_package.sh
```

Latest readiness status:

```text
ready-for-protocol-demo
```

Latest source package produced locally:

```text
dist/project2-agent-scaffold-20260514T040627Z.zip
```

The zip inspection showed:

```text
missing required files: none
forbidden generated files: none
```

### 5. Phase II Technical Investigation

Completed:

- reproduced the official Phase II binary state;
- confirmed the current candidate does not produce IC-side success;
- confirmed direct stack shellcode is blocked by NX;
- preserved a bounded one-shot sweep harness;
- tested argument-control feasibility;
- tested caller-stack staging feasibility;
- tested heap/global-state adjacency feasibility.

Evidence files:

| File | What it proves |
| --- | --- |
| `docs/PHASE2_SUCCESS_VALIDATION.md` | Latest status remains not full-credit complete. |
| `docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md` | Direct ret-to-maintenance, NX, and text-sweep evidence. |
| `docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md` | Saved-RBP argument-control route is blocked. |
| `docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md` | Caller-stack staging is not controllable by itself. |
| `docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md` | Direct heap/global-state adjacency is not a shortcut. |

## What We Have Not Completed

### 1. Official IC-Side Success

Not completed:

```text
/shared/success.txt has not appeared through the official IC-side /backdoor path.
```

This is the main full-credit gap.

### 2. Final Candidate-Generation Logic

Not completed:

- no validated Phase II candidate produces the official success artifact;
- `src/phase2_payload.py` remains a lab-specific probe, not a success claim;
- `src/config_planner.py` still preserves the explicit TODO boundary for
  instructor-approved course-lab-specific logic.

### 3. Full Grader Evidence

Not completed:

- no successful official grader transcript;
- no timing score;
- no successful repeatability evidence;
- no final full-credit proof package.

### 4. TA / Instructor Confirmation

Not completed:

- no confirmed answer yet on whether to submit source, Docker image tarball, or
  both;
- no confirmed answer yet on whether audit notes should be included in the
  official upload;
- no confirmed grading posture for a protocol-complete partial package.

## Why The Full-Credit Path Is Still Blocked

The current block is not the EC protocol. The protocol works.

The block is candidate generation under the supplied Phase II binary's runtime
constraints:

- the input path is C-string based;
- embedded NUL bytes stop the copy path;
- NX blocks direct stack execution;
- the main binary has limited useful gadget quality;
- the direct first-argument path is stale by the time control is redirected;
- simple caller-stack and heap-adjacent staging paths did not produce a useful
  success route.

The practical meaning:

```text
We can control the lab protocol and record evidence, but we do not yet have a
validated IC-side success mechanism.
```

## What It Would Take To Finish Full Credit

A full-credit completion requires all of the following:

1. Identify a new concrete candidate mechanism that avoids the shared C-string
   constraint.
2. Implement that mechanism only inside the controlled course-lab boundary.
3. Run it through the official IC loop.
4. Observe `/shared/success.txt` created by IC-side `/backdoor`.
5. Save the successful grader transcript and runtime evidence.
6. Update `COMPLETION_AUDIT.md`, `PHASE2_SUCCESS_VALIDATION.md`,
   `REQUIREMENTS_TRACEABILITY.md`, and `PARTIAL_SUBMISSION_BRIEF.md`.
7. Rebuild the source package and, if requested, the Docker image tarball.

Without step 4, do not claim full completion.

## Recommended Next Action

The next action should be submission-oriented:

1. Send or adapt `docs/TA_CLARIFICATION_DRAFT.md`.
2. Ask whether the TA wants source/build context, Docker image tarball, or both.
3. Ask whether the audit notes should be included in the official upload.
4. Keep the current package ready as a protocol-complete partial submission.

Continue technical research only if a new mechanism is identified. Do not spend
more time repeating the already closed direct paths.

## Submission Decision Record

If submitting now:

| Decision point | Current answer |
| --- | --- |
| Claim full Phase II success? | No. |
| Claim protocol-complete EC? | Yes. |
| Include safety/audit notes? | Yes, unless TA says upload only EC source. |
| Include generated `mock_shared/`? | No. |
| Include generated `dist/` in zip? | No. |
| Include coredumps? | No. |
| Mention remaining gap? | Yes. |

Recommended upload posture:

```text
This is a runnable Project II Phase II EC package with the required entry
points, shared-volume protocol, state/logging loop, readiness checks, and
documented Phase II validation attempts. The remaining gap is official IC-side
/shared/success.txt evidence.
```
