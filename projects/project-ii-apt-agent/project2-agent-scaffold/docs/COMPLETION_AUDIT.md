# Project II Completion Audit

Date: 2026-05-13
Updated: 2026-05-14
Scope: Project II / Phase II Medium external-container submission under the supplied local Docker lab.

## Direct Verdict

The submission is **not yet full-credit complete** because Phase II success has
not been observed in the real IC grading loop. The missing item is the final
course-lab-specific candidate generation that makes the IC execute `/backdoor`.

Everything around the grading protocol is now implemented or scaffolded:

- `/exploit` wrapper exists and is executable.
- `/triage` wrapper exists and is executable.
- `/exploit` writes `/shared/config.data` atomically and then creates
  `/shared/exploit_done`.
- `/triage` reads coredump/no-coredump evidence and updates
  `/shared/triage_state.json`.
- State and logs are parseable JSON/JSONL.
- The scaffold handles both `/shared/blogic.copy` from the brief and
  `/shared/blogic` from the supplied `docker.sh`.
- A readiness report can be generated with `scripts/generate_readiness_report.sh`.
- Byte-exact `config.data` writing is supported for Phase II lab candidates.

## What Was Missing Before This Pass

| Gap | Status after this pass |
| --- | --- |
| No explicit readiness report gate | Fixed: `src/readiness_report.py` and `scripts/generate_readiness_report.sh`. |
| No safe metadata check for the observable blogic artifact | Fixed: `src/blogic_metadata.py`. |
| Brief says `blogic.copy`, supplied lab uses `blogic` | Fixed: `resolve_blogic_path()` supports both. |
| Text-only config writer would be fragile for byte-exact lab candidates | Fixed: `/exploit` now writes bytes safely when `content_bytes` is provided. |
| No isolated Phase II candidate builder | Added: `src/phase2_payload.py`. |
| No script to run the Phase II probe against a shared volume | Added: `scripts/run_phase2_probe_against_shared.sh`. |

## Current Phase II Probe Status

The current lab-specific probe is enabled with:

```sh
PROJECT2_ENABLE_PHASE2_PROBE=1 /exploit
```

or from the source tree:

```sh
PROJECT2_SHARED_DIR=/path/to/lab/shared \
  ./scripts/run_phase2_probe_against_shared.sh
```

Observed against the local Phase II IC lab:

- `config.data` is written as a byte-exact `user_input=` line.
- `exploit_done` is created and consumed by IC.
- No fake `success.txt` is created by EC.
- No official `/backdoor` success has been observed yet.

Therefore this probe is useful evidence for protocol and control-flow work, but
it is **not** a final success claim.


## 2026-05-13 Final Phase II Validation Pass

A final validation pass was run against the official local Phase II IC. The EC
probe wrote the intended ret-to-maintenance candidate and IC consumed
`/shared/exploit_done`, but `/shared/success.txt` did not appear. The result is
recorded in `docs/PHASE2_SUCCESS_VALIDATION.md`.

The submission therefore remains **not full-credit complete**. The honest final
state is a protocol-complete scaffold plus an unsuccessful Phase II candidate; no
EC-side fake success file was created.

## 2026-05-14 Deep Completion Attempt

A follow-up pass reproduced the Phase II IC inside an x86_64 Colima Docker VM
and added stronger negative evidence. The result is recorded in
`docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`.

Verified in that pass:

- the current ret-to-`maintenance_task+5` candidate still does not create
  `/shared/success.txt`;
- direct stack shellcode reaches the intended stack address but faults under NX;
- a bounded one-shot partial-return sweep across `0x401000..0x401a20` with four
  command prefixes found no target that triggered IC-side `/backdoor`;
- the reusable lab-only sweep harness is now preserved as
  `scripts/run_phase2_one_shot_sweep.py`.

This improves the audit trail, but it does not change the completion verdict:
Project II / Phase II remains a high-quality partial submission until the
official IC creates `/shared/success.txt`.

## 2026-05-14 First-Principles Next Gate

The next planning artifact is
`docs/PHASE2_FIRST_PRINCIPLES_NEXT_GATE_2026-05-14.md`.

It narrows the next block to one falsifiable question: whether the
post-`log_message()` state can be turned into controlled first-argument state or
a reliable pivot under the input path constraints. It also keeps instructor
clarification as a valid bounded track if the intended Phase II route or binary
assumption is different from the local reading.

Do not spend the next block on another broad `.text` sweep, direct stack
shellcode, or the same direct ret-to-maintenance attempt unless new evidence
changes the premise.

## Remaining Work For A Full-Credit Submission

1. Finish the instructor-approved Phase II candidate-generation logic in
   `src/phase2_payload.py` / `src/config_planner.py`.
2. Validate the candidate in the supplied Phase II IC loop until
   `/shared/success.txt` is created by the IC-side `/backdoor`.
3. Save the grader output and generated readiness report as submission evidence.
4. Build the final EC image and verify `/exploit` and `/triage` at container
   root.

## Honesty Boundary

Do **not** mark this project as complete by creating `/shared/success.txt` from
the EC. The official success condition is IC-side `/backdoor` execution. Creating
the success file directly from the EC would be a grading bypass rather than a
valid Project II solution.
