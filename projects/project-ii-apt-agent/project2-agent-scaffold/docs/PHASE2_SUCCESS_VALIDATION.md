# Phase II Success Validation Log

Date: 2026-05-13
Scope: supplied Project II Phase II IC (`server_2`) running from the official
local Docker lab bundle.

## Direct Result

**Not full-credit complete yet.** The latest EC candidate still does **not** make
the official IC create `/shared/success.txt`.

This file is intentionally explicit so a reader who did not see the live debug
session can tell what was tried, what was observed, and why the submission must
not claim Phase II success yet.

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

The latest status remains **not full-credit complete**.

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

The latest status remains **not full-credit complete**.

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

The latest status remains **not full-credit complete**.

## 2026-05-15 Multi-Line Non-Stack Staging Addendum

The multi-line non-stack staging probe is recorded in
`docs/PHASE2_MULTI_LINE_NON_STACK_STAGING_ATTEMPT_2026-05-15.md`.

Additional evidence from that pass:

- repeated `user_input=` keys can stage marker bytes around `0x405000`;
- a later short `user_input=` line resets the final global string before
  `log_message()` copies it;
- direct 6-byte ret-to-libc `system()` reached `__libc_system`, but `rdi` was
  not controlled command text;
- no official IC-side `/shared/success.txt` was produced.

The latest status remains **not full-credit complete**.

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
