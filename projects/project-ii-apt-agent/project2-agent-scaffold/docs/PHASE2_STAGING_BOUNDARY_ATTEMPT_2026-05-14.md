# Phase II Staging Boundary Attempt - 2026-05-14

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

## Direct Result

Project II is still **not full-credit complete**.

This pass tested the next boundary after the saved-RBP argument-control attempt:
whether a first return target can use existing `rsp` / caller-stack state as a
second-stage path without needing a normal appended chain after saved RIP.

The bounded result is:

- no `/shared/success.txt` was created;
- the IC-side `/backdoor` was not invoked manually;
- the main binary still has no useful `pop rdi; ret`;
- the only visible `system@plt` call path still depends on either stale `rdi`
  or a valid `maintenance_task()` frame;
- the clean caller-stack probe reached a fixed no-success path and produced no
  coredump, confirming that the untouched caller stack does not become a
  controllable second-stage chain by itself.

## Environment

This pass used a fresh local extraction:

```text
/tmp/phase2_stage/lab
```

The isolated IC was started as:

```text
docker context: default
container: IC_PHASE2_STAGE
image: ic_image_phase2_stage
mount: /tmp/phase2_stage/lab/shared -> /shared
ASLR: 0
processes: /bin/bash /runserver.sh and /blogic
success artifact before probe: absent
```

The live Phase II binary matched the previously recorded `server_2` hash:

```text
155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

## Static Staging Check

The following first targets are representable by the same three-byte partial
overwrite model used in earlier attempts:

| Candidate target | Address | Why it is not enough |
| --- | ---: | --- |
| `system@plt` | `0x401250` | Uses stale `rdi`, not `user_input`. |
| `maintenance_task+5` | `0x401475` | Reaches the function body setup, but `rdi` is stale. |
| `maintenance_task+22` | `0x401486` | Needs a valid saved RBP frame, which the C-string path cannot preserve while also overwriting saved RIP. |
| `run_server` user-input setup | `0x4016bb` | Sets `rdi = user_input`, but calls `log_message`, not `system` or `maintenance_task`. |
| `main` user-input setup | `0x401707` | Sets up `user_input` for `memset`, not a success path. |
| `maintenance_task` `mov rdi, rax; call system` | `0x4014b1` | Uses `rax` from the post-logging state, which points to `std::cout`, not controlled command text. |
| caller-stack `pop rbp; ret` | `0x4016cb` | Consumes untouched caller-stack qwords and returns to the fixed main epilogue path. |

Useful negative facts:

- no `pop rdi; ret` was found in the main binary text range;
- no main-binary sequence was found that both sets `rdi = user_input` and calls
  `system@plt` or `maintenance_task()`;
- the writable GOT is before `user_input`, so the forward `strcpy()` write from
  `user_input` does not provide a simple GOT overwrite path;
- `.bss` can hold bytes, but no current first-stage pivot can set `rsp` or `rbp`
  to a `.bss` address without hitting the same NUL-byte termination problem.

## Live Probe - Caller-Stack Pop

The live probe targeted the caller-stack `pop rbp; ret` sequence at
`0x4016cb`.

Observed result:

```text
strategy=caller-stack-pop-rbp-ret-probe
target=0x4016cb
success_exists=no
coredumps=
new /blogic process continued under /runserver.sh
```

Interpretation:

- the first target is reachable;
- consuming the untouched caller stack does not crash;
- the untouched next return path is fixed by the original call chain and returns
  toward the main epilogue;
- because the partial overwrite terminates the C string inside the saved-RIP
  qword, the probe cannot also write a controlled second-stage qword after saved
  RIP.

This closes the simple caller-stack staging idea. It is not a full exploit path.

## Updated Boundary

The current blockers are now narrower:

1. Single-target reuse in the main binary does not provide
   `rdi = user_input` followed by `system` or `/backdoor`.
2. Saved-RBP-based maintenance entry is blocked by the C-string/NUL-byte
   constraint.
3. Caller-stack staging after the partial saved-RIP overwrite is fixed, not
   attacker-controlled.
4. Libc gadgets remain theoretically attractive because ASLR is disabled, but a
   first-stage pivot or argument setup is still missing.

## Next Direction

The next useful block should move away from simple stack staging and inspect
whether the earlier `.bss` to heap-adjacency note can provide a legitimate
course-lab-specific state change before `log_message()` returns.

Recommended next bounded question:

```text
Can the unbounded strcpy() into user_input create a stable, observable heap or
global-state effect that changes a later call target or argument source before
the stack overflow epilogue?
```

Stop after one of these outcomes:

- a concrete writable target is identified with an address, lifetime, and
  validation plan;
- the heap/global-state route is ruled out for this binary and runtime;
- `/shared/success.txt` appears through the official IC path.
