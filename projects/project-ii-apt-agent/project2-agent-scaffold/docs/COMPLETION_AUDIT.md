# Project II Completion Audit

Date: 2026-05-13
Updated: 2026-05-14
Scope: Project II / Phase II Medium external-container submission under the supplied local Docker lab.

## Direct Verdict

The submission is **not yet full-credit complete** because Phase II success has
not been observed in the real IC grading loop. The missing item is the final
course-lab-specific candidate generation that makes the IC execute `/backdoor`.

All Phase II recovery experiments, including failures and positive primitives
that do not create `/shared/success.txt`, are indexed in
`docs/PHASE2_EXPERIMENT_LOG.md`.

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

## 2026-05-15 Multiline Staging Follow-Up

A further recovery pass tested the multi-line `parse_config()` behavior and is
recorded in `docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`.

Verified in that pass:

- earlier `user_input=` lines can stage controlled bytes beyond the final
  line's terminating NUL in global `user_input`;
- the final `user_input=` line can still be the stack-overflow trigger;
- a longer staging line can reach heap-adjacent state, but allocator hardening
  catches broad corruption;
- local libc one-gadget candidates spawn `/bin/sh`, not `/backdoor`, and do not
  satisfy the observed post-`log_message()` register/stack constraints.

The useful new primitive is preserved as
`PROJECT2_PHASE2_STRATEGY=multiline-staging`, but it does not yet provide the
missing first-stage pivot or first-argument setup. The completion verdict is
unchanged: protocol-complete partial, not full-credit complete.

## 2026-05-15 Register-Reuse Follow-Up

A bounded register-reuse pass tested whether `rax` after `log_message()` could
be reused as a controlled command pointer by returning directly into the
`maintenance_task()` tail sequence. The result is recorded in
`docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md`.

Verified in that pass:

- the selected EC candidate was written and IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` appeared;
- a coredump was produced at `maintenance_task+74` after the selected
  `system()` path returned;
- `system()` returned `0x7f00`, and the later crash was the expected corrupted
  saved-RBP epilogue crash;
- the direct `rax`-reuse route is therefore closed as a full-credit mechanism.

This does not change the completion verdict: protocol-complete partial, not
full-credit complete.

## 2026-05-15 Backward-Pivot Feasibility Follow-Up

A bounded first-stage pivot feasibility block tested whether the fresh Phase II
main binary or pinned libc contains a simple gadget that can move `rsp`
backwards from the post-return position into controlled pre-RIP stack bytes. The
result is recorded in
`docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md`.

Verified in that pass:

- a fresh disposable IC was started from the supplied `lab.zip`;
- the exact pinned libc was copied from the live IC;
- the checked pivot family was limited to `sub rsp, imm; ret`,
  negative `add rsp, imm; ret`, `lea rsp, [rsp-negative-imm]; ret`,
  `xchg rsp, reg; ret`, and `mov rsp, reg; ret`;
- no usable gadget in that family was found in the fresh binary set;
- no live EC candidate was run because the hypothesis produced no concrete
  first-stage pivot address.

This closes the simple backward-stack-pivot route. The completion verdict is
unchanged: protocol-complete partial, not full-credit complete.

## 2026-05-15 Current-RDI Argument Follow-Up

A bounded first-argument setup pass tested whether the current `rdi` register at
`log_message()` return time can be reused by returning directly to
`system@plt`. The result is recorded in
`docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md`.

Verified in that pass:

- a fresh local Phase II IC was started from the supplied `lab.zip`;
- the candidate did not use appended ROP, saved RBP, or direct `rax` reuse;
- IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` appeared;
- the coredump stopped inside libc `do_system()` with the command pointer set
  to the empty `_IO_stdfile_1_lock` buffer;
- the controlled `/backdoor` text remained in `user_input`, proving it did not
  reach the first argument.

This closes the direct current-`rdi` first-argument route. The completion
verdict is unchanged: protocol-complete partial, not full-credit complete.

## 2026-05-15 Post-Stream Argument / BSS Boundary Follow-Up

A bounded follow-up tested the next stricter route: not current-`rdi`, not
direct `rax`, not preserved saved RBP, and not appended ROP. The result is
recorded in
`docs/PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md`.

Verified in that pass:

- a marker crash at `log_message()` return preserved controlled data in
  `user_input` at `0x404340`;
- a stack/local slot at `[rsp-0x70]` still held `0x404340`, and a caller qword
  at `[rsp+0x08]` pointed into the controlled stack buffer;
- no fresh-binary or pinned-libc single-stage sequence was found that consumes
  either pointer into `rdi` and immediately calls `system()`/`execve()`;
- multi-line staging safely fills the data-page tail through first-line length
  `L=3264`;
- first-line lengths `L>=3300` cross into allocator/tcache state and crash
  before a useful final return point.

This closes the tested post-stream first-argument transfer family and preserves
only a bounded non-stack staging primitive. The completion verdict is unchanged:
protocol-complete partial, not full-credit complete.

## 2026-05-15 BSS-Indirect Dispatch Feasibility Follow-Up

A deeper static slice tested whether the bounded `.bss` staging range can be
used through a one-shot register-derived dispatch gadget. The result is
recorded in
`docs/PHASE2_BSS_INDIRECT_DISPATCH_FEASIBILITY_2026-05-15.md`.

Verified in that pass:

- no live IC candidate was run because no concrete first-stage address was
  found;
- `server_2` and the pinned libc were searched for single-shot
  `lea/mov rdi, [rax+disp]; (jmp|call) exec-family` and
  `mov rdi, r*; (jmp|call) exec-family` families;
- no candidate moved the first argument into the staged `.bss` range and then
  reached `system`/`execve`-family;
- hardcoded binary gadgets that set `rdi = 0x4040d8` target `.data` before
  `user_input`, which the forward `strcpy()` primitive cannot reach.

This closes the tested BSS-indirect dispatch route. The completion verdict is
unchanged: protocol-complete partial, not full-credit complete.

## 2026-05-15 Stack-Local First-Argument Feasibility Follow-Up

A final same-day static slice tested whether the preserved stack-local pointer
from the live post-stream core can be used directly by a stack-relative
first-argument setup gadget. The result is recorded in
`docs/PHASE2_STACK_LOCAL_FIRST_ARGUMENT_FEASIBILITY_2026-05-15.md`.

Verified in that pass:

- no live IC candidate was run because no concrete first-stage address survived
  static/manual review;
- `server_2` has zero stack-relative `mov/lea rdi, [rsp+disp]` setup patterns
  in its executable text;
- the apparent libc exec-family hits are not valid success candidates: two
  require `rbp`-relative state, and one `posix_spawn` path uses `rdi` as
  `pid_t *` while its executable path is fixed to `/bin/sh`;
- the preserved `[rsp-0x70] = 0x404340` pointer therefore does not provide a
  usable one-stage first-argument setup in this artifact set.

This closes the tested stack-local first-argument route. The completion verdict
is unchanged: protocol-complete partial, not full-credit complete.

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
