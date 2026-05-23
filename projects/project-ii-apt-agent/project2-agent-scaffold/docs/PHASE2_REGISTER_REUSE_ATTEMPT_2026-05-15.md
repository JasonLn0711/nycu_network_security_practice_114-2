# Phase II Register-Reuse Attempt - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger ID: `P2-EXP-012` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Hypothesis

After `log_message()` completes its final C++ stream call, `rax` may still point
at a controlled string buffer. If so, a single partial return to the existing
`maintenance_task()` sequence:

```text
0x4014b1: mov rdi, rax
0x4014b4: call system@plt
```

could call `system()` with controlled command text and legitimately reach the
IC-side `/backdoor` path.

This avoids the already closed paths:

- it does not require preserving saved RBP;
- it does not depend on stale `rdi`;
- it does not append a NUL-bearing ROP chain after the partial return address;
- it does not execute stack shellcode;
- it does not create `/shared/success.txt` from EC code.

## Falsifiable Prediction

The hypothesis is supported only if the official IC creates:

```text
/shared/success.txt
```

after EC writes the candidate and IC consumes `/shared/exploit_done`.

The hypothesis is falsified if either:

- `/shared/success.txt` does not appear and coredump/register evidence shows
  `rax` is not a controlled command-string pointer at the selected path; or
- the candidate returns/crashes without any IC-side success artifact.

## Bounded Validation Contract

Run exactly one candidate class:

```sh
PROJECT2_SHARED_DIR=/tmp/project2_register_reuse/shared \
  PROJECT2_ENABLE_PHASE2_PROBE=1 \
  PROJECT2_PHASE2_STRATEGY=register-reuse-system-rax \
  python3 -m src.exploit_runner
```

Then wait for IC to consume `/shared/exploit_done`, check
`/shared/success.txt`, and inspect at most the resulting coredump/register state.

Stop after that result. Do not broaden this into another `.text` sweep.

## Result

Falsified.

## Environment

This pass used a fresh local Docker reproduction:

```text
container: IC_PHASE2_REGISTER_REUSE
image: ic_image_register_reuse
mount: /tmp/project2_register_reuse/lab/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

The container was removed after the validation block finished.

## Observed Evidence

The EC probe wrote the selected candidate through `src.exploit_runner`.

```text
PROJECT2_PHASE2_STRATEGY=register-reuse-system-rax
config_size=112
config_sha256=8ebed8ecef6d5d915df53a26e99ff72667ce252c12ca03c9a22eb32197cde5d9
```

After the run:

```text
exploit_done=absent
success=absent
coredumps=blogic-30.core
```

This means IC consumed `/shared/exploit_done`, but the official success artifact
did not appear.

## Core Evidence

The resulting coredump showed the candidate reached the intended
`maintenance_task()` tail path and then crashed at the expected corrupted-frame
epilogue:

```text
signal: SIGBUS
rip = 0x4014ba <maintenance_task(char const*)+74>
rbp = 0x5252525252525252
rax = 0x7f00
rdi = 0x2
```

Interpretation:

- execution reached the `system@plt` tail path and returned;
- `rax = 0x7f00` is the `system()` return status, not a controlled pointer;
- no `/shared/success.txt` was created before the crash;
- the later crash at `leave` is expected because saved RBP was marker-controlled.

The controlled global value was present:

```text
0x404340 <user_input>: "x; /backdoor; #", 'R' <repeats 82 times>, "\\261\\024@"
```

Therefore the selected `rax` reuse path did not pass a controlled command string
to `system()`.

## Decision

Do not continue this same `rax`-reuse path. It is now closed as a direct
full-credit route.

The remaining unsolved class is still a reliable first-stage pivot or
first-argument setup under the shared C-string constraints. Further recovery
work needs a different written hypothesis before another candidate is run.
