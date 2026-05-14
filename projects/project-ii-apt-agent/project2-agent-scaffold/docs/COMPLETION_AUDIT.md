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

The later follow-up attempts below answer this gate further. They narrow the
practical next move toward submission/report hardening or instructor
clarification unless a new staging idea changes the technical premise.

## 2026-05-14 Argument-Control Follow-Up

A bounded follow-up tested the handoff's recommended argument-control direction.
The result is recorded in
`docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`.

Verified in that pass:

- a maintenance-body entry candidate reached `maintenance_task+22`
  (`0x401486`);
- no `/shared/success.txt` appeared;
- the IC-side `/backdoor` was not invoked manually;
- the candidate stopped because `rbp` was marker-controlled instead of a valid
  frame pointer;
- the useful original frame-pointer path is blocked by the C-string/NUL-byte
  constraint: preserving canonical saved RBP prevents continuing to overwrite
  saved RIP, while continuing to saved RIP corrupts saved RBP.

This narrows the next step: do not keep trying maintenance-body entry unless a
new staging or encoding path can preserve a canonical frame pointer while still
controlling the return target.

## 2026-05-14 Staging-Boundary Follow-Up

A second bounded follow-up tested whether simple single-target reuse or
untouched caller-stack staging can replace the missing saved-RBP path. The
result is recorded in
`docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`.

Verified in that pass:

- the main binary still has no useful `pop rdi; ret`;
- no main-binary sequence was found that both sets `rdi = user_input` and calls
  `system@plt` or `maintenance_task()`;
- the clean caller-stack `pop rbp; ret` probe produced no success and no
  coredump;
- the untouched caller-stack qwords after the partial saved-RIP overwrite return
  to the fixed main epilogue path, not to a controllable second-stage chain.

This narrows the next practical direction to the remaining heap/global-state
question around the unbounded `strcpy()` into `user_input`, or to a new staging
idea that is not just saved-RBP or caller-stack reuse.

## 2026-05-14 Heap / Global-State Follow-Up

A final bounded follow-up tested whether the forward `strcpy()` overflow from
global `user_input` can create a useful heap or global-state effect before
`log_message()` returns. The result is recorded in
`docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`.

Verified in that pass:

- the forward write can reach memory around `0x405000`, beyond the main
  binary's `.bss` page boundary;
- no `/shared/success.txt` appeared;
- the later `sprintf()` copied the same long string into the small stack buffer
  and crashed inside libc before a useful epilogue path was reached;
- the forward write cannot directly hit the GOT or copied iostream globals
  because those live before `user_input`.

This leaves the project in an honest high-quality partial state. The next
practical work should be submission/report hardening and, if needed, a TA-facing
question about whether the protocol-complete package plus negative Phase II
evidence is acceptable before the final gate.

## 2026-05-14 Bounded Recovery Follow-Up

A bounded full-credit recovery block tested one additional user-input setup
boundary after rechecking a fresh official Phase II IC. The result is recorded
in `docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md`.

Verified in that pass:

- the IC container was rebuilt from the supplied lab bundle;
- ASLR was disabled;
- `/shared/success.txt` was absent before the candidate;
- IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` appeared;
- no coredump appeared;
- `/blogic` continued running under `/runserver.sh`.

This closes the simple "re-enter user-input setup" boundary as a direct success
route. The completion verdict is unchanged: protocol-complete partial, not
full-credit complete.

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
