# Phase II Success Validation Log

Date: 2026-05-13
Scope: supplied Project II Phase II IC (`server_2`) running from the official
local Docker lab bundle.

Experiment ledger IDs: `P2-EXP-000`, `P2-EXP-001` in
`docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

**Not full-credit complete yet.** The latest EC candidate still does **not** make
the official IC create `/shared/success.txt`.

This file is intentionally explicit so a reader who did not see the live debug
session can tell what was tried, what was observed, and why the submission must
not claim Phase II success yet.

The canonical index of all Phase II experiments is
`docs/PHASE2_EXPERIMENT_LOG.md`. Each success, failure, static infeasibility
check, and positive primitive should have a row there.

## Candidate Under Test

The current Phase II probe in `src/phase2_payload.py` writes a byte-exact
`user_input=` line with:

- a lab-only command-injection-shaped prefix: `'; /backdoor; #`
- padding to the observed `log_message` saved-return-address offset (`97`
  bytes of `user_input` value)
- a non-PIE partial return overwrite to `maintenance_task+5` (`0x401475`)

The candidate keeps the EC protocol correct: it writes `/shared/config.data`,
then creates `/shared/exploit_done`, and it does not create
`/shared/success.txt` from the EC.

## Official IC Validation Command

Executed from the scaffold directory with the official Phase II IC already
running and the lab shared directory mounted:

```sh
PROJECT2_SHARED_DIR=/tmp/p2lab2/lab/shared \
  PROJECT2_ENABLE_PHASE2_PROBE=1 \
  python3 -m src.exploit_runner
```

Then the runner waited for IC to consume `/shared/exploit_done` and checked the
shared directory.

## Observed Evidence

Latest observed result:

```text
success_exists=no
coredumps=
server_log_tail= |  |  |  |
```

Interpretation:

- IC consumed `/shared/exploit_done`.
- No `/shared/success.txt` appeared.
- No new coredump appeared for this candidate.
- The maintenance path appears to run only the empty `echo '' >> /tmp/server.log`
  form, not the intended `/backdoor` command.

## Debug Findings

A crash probe with a long marker string confirmed the vulnerable return-address
control point and register state at the end of `log_message`:

```text
rip = 0x40146f <log_message(char const*)+89>
rsp = 0x7fffffffec48
rbp = marker-controlled bytes
rdi = 0x7ffff7d00710 (_IO_stdfile_1_lock, zero bytes)
user_input = 0x404340
```

This explains why simply returning to `maintenance_task+5` is not enough in the
validated Ubuntu 24.04 IC: by the time `log_message` returns, the `rdi` register
no longer points at `user_input`; it points at a glibc stdout lock area whose
bytes are zero. As a result, `maintenance_task` formats and runs an empty echo
instead of the intended command-injection value.

A bounded sweep over observed instruction-start addresses in `server_2` did not
find a text-section partial-return target that created `/shared/success.txt`.
The sweep used the same `'; /backdoor; #` prefix and did not create the success
file from the EC.

## Current Blocker

The remaining blocker is a Phase II control-flow target that both:

1. survives NX / non-executable stack constraints, and
2. makes the IC execute `/backdoor` or otherwise legitimately reach the official
   success condition from IC-side control flow.

Do **not** mark this assignment complete until `/shared/success.txt` is observed
from the official IC flow. Do **not** create `/shared/success.txt` from `/exploit`.

## 2026-05-14 Addendum

The next deep validation pass is recorded in
`docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`.

Additional evidence from that pass:

- the local IC was rebuilt and run in a verified x86_64 Colima Docker profile;
- the current candidate again produced `success_exists=no`;
- a direct stack-shellcode probe reached `rip = 0x7fffffffeb97` but faulted
  under NX;
- a text-section one-shot sweep tried `10328` candidates across
  `0x401000..0x401a20` and found no `/shared/success.txt`.

The latest status is still **not full-credit complete**.

## 2026-05-14 Argument-Control Addendum

The follow-up argument-control probe is recorded in
`docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`.

Additional evidence from that pass:

- a candidate reached `maintenance_task+22` (`0x401486`);
- no `/shared/success.txt` was created;
- the crash core showed `rbp` contained marker bytes, so the maintenance body
  could not read a valid argument pointer from `[rbp-0x88]`;
- the apparently useful preserved stack slot holding `0x404340` cannot be used
  by this direct path because saved RBP and saved RIP cannot both be encoded
  through the current C-string copy path.

## 2026-05-14 Staging-Boundary Addendum

The follow-up staging probe is recorded in
`docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`.

Additional evidence from that pass:

- single-target reuse in the main binary did not reveal a path that both sets
  `rdi = user_input` and calls the success-relevant function path;
- the caller-stack `pop rbp; ret` probe reached a no-success/no-coredump path;
- the untouched qwords after saved RIP are fixed by the original call chain and
  cannot act as a controlled appended chain under the current C-string
  overwrite model.

## 2026-05-14 Heap / Global-State Addendum

The heap/global-state feasibility probe is recorded in
`docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`.

Additional evidence from that pass:

- a long `user_input` value reached memory around `0x405000`;
- no `/shared/success.txt` was created;
- the process crashed inside libc `sprintf()` / copy handling before a useful
  control-flow epilogue was reached;
- this makes the direct heap-adjacency route insufficient without a new staging
  mechanism.

## 2026-05-14 Bounded Recovery Block Addendum

The next bounded recovery block is recorded in
`docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md`.

Additional evidence from that block:

- a fresh Phase II IC container was started from the supplied `lab.zip`;
- ASLR was confirmed disabled inside the container;
- `/shared/success.txt` was absent before the candidate;
- the IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` was created;
- no coredump appeared for the candidate;
- `/blogic` remained running under `/runserver.sh`;
- the checked user-input setup boundary is therefore a stable no-success path,
  not a full-credit route.

The latest status remains **not full-credit complete**.

## 2026-05-15 Register-Reuse Addendum

The bounded register-reuse probe is recorded in
`docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md`.

Additional evidence from that pass:

- a fresh Phase II IC container was started from the supplied `lab.zip`;
- ASLR was confirmed disabled inside the container;
- the EC candidate used
  `PROJECT2_PHASE2_STRATEGY=register-reuse-system-rax`;
- IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` was created;
- a coredump appeared at `maintenance_task+74` after the selected `system()`
  tail path returned;
- `system()` returned `0x7f00`, so direct `rax` reuse is not a full-credit
  route.

The latest status remains **not full-credit complete**.

## 2026-05-15 Current-RDI Argument Addendum

The bounded current-`rdi` first-argument probe is recorded in
`docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md`.

Additional evidence from that pass:

- a fresh local Phase II IC container was started from the supplied `lab.zip`;
- a marker crash confirmed `rdi = 0x7ffff7d00710`, the empty
  `_IO_stdfile_1_lock` buffer, at `log_message()` return time;
- the EC candidate used `PROJECT2_PHASE2_STRATEGY=current-rdi-system`;
- IC consumed `/shared/exploit_done`;
- no `/shared/success.txt` was created;
- the coredump stopped inside libc `do_system()` with
  `line = 0x7ffff7d00710 ""`, while controlled `/backdoor` text remained in
  `user_input`.

The direct current-`rdi` route is therefore closed as a full-credit mechanism.
The latest status remains **not full-credit complete**.

## 2026-05-15 Post-Stream Argument / BSS Boundary Addendum

The next bounded recovery block is recorded in
`docs/PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md`.

Additional evidence from that block:

- the probe did not reuse direct current-`rdi`, direct `rax`, preserved saved
  RBP, or appended ROP;
- a marker crash at `log_message()` return showed controlled data still
  survived at `0x404340`, with a preserved local slot
  `[rsp-0x70] = 0x404340` and a caller qword `[rsp+0x08]` pointing into the
  controlled stack buffer;
- the same crash showed `rax = 0x404100` and
  `rdi = 0x7ffff7d00710`, so neither register was already the needed first
  argument;
- a fresh main-binary plus pinned-libc scan found no single-stage sequence that
  moves those preserved pointers into `rdi` and immediately calls
  `system()`/`execve()`;
- multi-line staging is safe through the data-page tail at first-line length
  `L=3264`, but `L>=3300` crosses into allocator/tcache state and crashes
  before a useful final return point.

The post-stream pointer-transfer route is closed in the tested single-stage
family. The `.bss` staging boundary is a positive primitive only, not a
full-credit mechanism.

## 2026-05-15 BSS-Indirect Dispatch Feasibility Addendum

The follow-up static dispatch check is recorded in
`docs/PHASE2_BSS_INDIRECT_DISPATCH_FEASIBILITY_2026-05-15.md`.

Additional evidence from that block:

- no live IC candidate was run because the static search produced no concrete
  first-stage address;
- `server_2` and the pinned libc were searched for single-shot
  `lea/mov rdi, [rax+disp]; (jmp|call) exec-family` and
  `mov rdi, r*; (jmp|call) exec-family` families;
- no candidate both landed in the staged `.bss` range and transferred to
  `system`/`execve`-family;
- the binary's hardcoded `mov edi, 0x4040d8; jmp rax` gadgets point before
  `user_input`, outside the forward `strcpy()` staging surface.

The BSS-indirect dispatch route is closed in the tested artifact set. The
latest status remains **not full-credit complete**.

## 2026-05-15 Stack-Local First-Argument Feasibility Addendum

The follow-up stack-local first-argument check is recorded in
`docs/PHASE2_STACK_LOCAL_FIRST_ARGUMENT_FEASIBILITY_2026-05-15.md`.

Additional evidence from that block:

- no live IC candidate was run because the static/manual review produced no
  concrete first-stage address;
- `server_2` contains no stack-relative `mov/lea rdi, [rsp+disp]` setup pattern
  in its executable text;
- the only apparent libc exec-family hits are invalid for this problem: two
  `rbp`-relative `execve` paths require the saved-RBP route that is already
  closed, and one `posix_spawn` path puts the stack address in `rdi` as
  `pid_t *` while the executable path is fixed in `rsi` to `/bin/sh`;
- no tested stack-local path consumes `[rsp-0x70] = 0x404340` or controlled
  caller-stack bytes into a success-relevant first argument.

The stack-local first-argument setup route is closed in the tested artifact set.
The latest status remains **not full-credit complete**.
