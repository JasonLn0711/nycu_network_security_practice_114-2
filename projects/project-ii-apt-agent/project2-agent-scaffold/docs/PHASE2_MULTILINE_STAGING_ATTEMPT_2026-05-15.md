# Phase II Multiline Staging Attempt - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger IDs: `P2-EXP-009`, `P2-EXP-010`, `P2-EXP-011` in
`docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

Project II is still **not full-credit complete**.

This pass tested a more professional recovery route that was not fully captured
in the earlier notes: `parse_config()` processes multiple `user_input=` lines.
That means an earlier line can stage bytes past the final line's terminating
NUL in global `user_input`, while the final line can remain the stack-overflow
trigger.

The bounded result is:

- the multi-line staging primitive is real and reproducible;
- no `/shared/success.txt` was created;
- the IC-side `/backdoor` was not invoked manually;
- the primitive does not by itself solve the remaining pivot or first-argument
  control problem.

## Environment

This pass used the local Linux Docker engine:

```text
container: IC_PHASE2_LOCAL
image: ic_image_phase2_local
mount: /tmp/project2_phase2_run/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

Tooling used inside the disposable IC container:

```text
gdb 15.1
ltrace
one_gadget 1.10.0 on Ubuntu glibc 2.39
```

## Static Recheck

The Phase II binary still has the same blockers:

- no useful main-binary `pop rdi; ret`;
- no main-binary gadget that sets `rdi = user_input` and then calls
  `system@plt` or `maintenance_task()`;
- GOT and copied iostream globals are before `user_input`, so the forward global
  `strcpy()` cannot directly overwrite them;
- libc one-gadgets found for the local glibc spawn `/bin/sh`, not `/backdoor`,
  and their register/stack constraints do not match the post-`log_message()`
  state.

## Multiline Staging Finding

The tested config shape was:

```text
user_input=<long staging bytes>
user_input=FINAL
```

A breakpoint after `parse_config()` and before `run_server()` showed:

```text
0x404340 <user_input>: "FINAL"
0x404340: 0x5353004c414e4946 0x5353535353535353
0x404350: 0x5353535353535353 0x5353535353535353
...
```

Interpretation:

- the final short line controls the visible C string used by `sprintf()`;
- bytes beyond the final line's terminating NUL remain from the earlier staging
  line;
- this creates a real staged-data primitive in `.bss` / the adjacent writable
  page.

`src/phase2_payload.py` now preserves this as:

```text
PROJECT2_PHASE2_STRATEGY=multiline-staging
```

when `PROJECT2_ENABLE_PHASE2_PROBE=1` is set.

## Heap Boundary Check

A longer multi-line test also confirmed that the forward `strcpy()` can corrupt
heap-adjacent state while a later short final line avoids the earlier direct
`sprintf()` crash. However, later same-size C++ string allocation can abort with
allocator consistency checks such as:

```text
malloc(): unaligned tcache chunk detected
```

This is useful evidence, but not yet a stable exploit route. A legitimate heap
route would need a precise allocator plan, not a broad overwrite.

## Why This Still Does Not Complete Phase II

The staged bytes are data, not execution:

- NX still blocks direct execution from stack/heap/global writable memory;
- the first return target still must provide a pivot or first-argument setup;
- saved RBP cannot be made a canonical `.bss`, heap, or stack pointer while the
  same C string continues far enough to overwrite saved RIP;
- no validated first-stage gadget currently pivots to the staged bytes or turns
  them into `system("/backdoor")`.

## Current Professional Posture

The repo now has:

- a protocol-complete EC scaffold;
- byte-exact Phase II candidate writing;
- a selectable multi-line staging probe;
- reproducible negative evidence for the closed simple routes;
- an honest partial-submission package path.

Do not mark full-credit complete until the official IC creates
`/shared/success.txt` through `/backdoor`.
