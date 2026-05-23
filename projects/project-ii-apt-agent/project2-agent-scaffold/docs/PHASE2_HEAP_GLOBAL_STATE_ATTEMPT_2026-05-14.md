# Phase II Heap And Global-State Attempt - 2026-05-14

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger ID: `P2-EXP-007` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

Project II is still **not full-credit complete**.

This pass tested the next remaining direction from the staging-boundary note:
whether the unbounded `strcpy()` into global `user_input` can create a useful
heap or global-state effect before `log_message()` reaches its stack-overflow
return path.

The bounded result is:

- no `/shared/success.txt` was created;
- the IC-side `/backdoor` was not invoked manually;
- a long `user_input` value did reach the memory immediately beyond the main
  binary's `.bss` page and into the next heap-adjacent region;
- the same long C string then caused `sprintf()` to copy thousands of bytes into
  the small stack buffer and crash inside libc before a useful epilogue or
  second-stage path was reached.

This route is therefore not a direct shortcut. It would need a separate staging
idea that can make the forward global/heap write useful without letting the same
long C string immediately cause an uncontrolled stack copy.

## Environment

This pass reused the isolated local setup:

```text
/tmp/phase2_stage/lab
container: IC_PHASE2_STAGE
mount: /tmp/phase2_stage/lab/shared -> /shared
ASLR: 0
```

The live Phase II binary matched the known `server_2` hash:

```text
155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

## Static Boundary

Relevant writable layout:

```text
std::cout      = 0x404100
std::cerr      = 0x404220
completed.0    = 0x404330
user_input     = 0x404340
_end           = 0x404380
page boundary  = 0x405000
```

Important constraints:

- `strcpy(user_input, value.c_str())` writes forward from `0x404340`.
- The forward write cannot reach the GOT, `std::cout`, `std::cerr`, or
  `completed.0` because those are before `user_input`.
- A value long enough to reach the page boundary or heap-adjacent region is also
  long enough for the later `sprintf(local_buffer, "[LOG]: %s", user_input)` to
  copy far beyond saved RIP.
- Adding an embedded NUL would stop the later `sprintf()`, but the same NUL
  would also stop the earlier `strcpy()` before the forward heap/global-state
  write happens.

## Live Probe

The probe wrote a long marker value to `user_input` and then let the official IC
process the round normally.

Observed result:

```text
strategy=bss-to-heap-adjacency-feasibility-probe
value_len=3474
success_exists=no
core=/shared/coredump/blogic-45.core
```

The core showed:

```text
signal=SIGSEGV
rip=__memcpy_avx_unaligned_erms
call path=__sprintf -> log_message(char const*)
copy_count=3474
source=0x404340 <user_input>
sample at 0x404ff0=marker bytes
sample at 0x405000=marker bytes
```

Interpretation:

- the forward `strcpy()` write did reach the heap-adjacent region;
- the process did not turn that write into a success-relevant control-flow
  change;
- the later `sprintf()` copy crashed first because it attempted to copy the same
  long C string into the small stack buffer.

## Updated Boundary

The direct heap/global-state route is now narrowed:

1. Forward global overflow from `user_input` cannot overwrite the GOT or copied
   iostream globals because they are at lower addresses.
2. Heap-adjacent bytes can be reached, but the same string then drives an
   uncontrolled stack copy before a useful return path.
3. A NUL separator would stop the stack copy, but it would also stop `strcpy()`
   before reaching the heap-adjacent region.
4. A useful heap route would require a separate mechanism, such as a later read
   from the overwritten region or a way to make the long write affect a live
   object before `sprintf()` copies the whole string. No such object/path was
   identified in this pass.

## Next Direction

At this point, the simple routes have been narrowed:

- direct ret-to-maintenance: insufficient;
- direct stack shellcode: blocked by NX;
- broad one-shot text sweep: no success;
- saved-RBP maintenance-body entry: blocked by C-string/NUL-byte constraints;
- caller-stack staging: fixed, not controllable;
- direct heap/global-state adjacency: reaches memory but crashes in `sprintf()`
  before producing a useful state change.

The next useful work is no longer another candidate probe. It should be a
decision point:

1. Ask the TA/instructor whether a high-quality protocol-complete partial
   package is acceptable if Phase II success is not reached before the
   presentation/submission gate.
2. In parallel, prepare the submission/report honestly as partial, with the
   above negative evidence and no fake success claim.
3. If continuing technical work, only pursue a new route after identifying a
   concrete mechanism that avoids the shared C-string constraint. Do not repeat
   the already-closed direct paths.

## 2026-05-15 Follow-Up Boundary

A later bounded pass found one such separate mechanism:
`docs/PHASE2_MULTI_LINE_NON_STACK_STAGING_ATTEMPT_2026-05-15.md`.

The updated boundary is:

- the single-line long heap-adjacency route still crashes through `sprintf()`;
- repeated `user_input=` keys can stage bytes around `0x405000` first, then
  reset the final `user_input` to a short string before `log_message()`;
- this proves a non-stack staging primitive exists, but it still does not prove
  first-argument control, a pivot, or official IC-side success.
