# Phase II Multi-Line Non-Stack Staging Attempt - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

## Direct Result

Project II is still **not full-credit complete**.

This block did find a new useful primitive:

```text
multi-line user_input can stage bytes past .bss into heap-adjacent memory, then
reset the final global user_input before run_server() reaches log_message().
```

This is materially different from the earlier single-line heap/global-state
probe. The earlier probe proved that one very long `user_input` line reaches
heap-adjacent memory but then crashes when `sprintf()` copies that same long
C string into the small stack buffer. This pass proved that `parse_config()`
processes multiple `user_input=` lines, so a first long line can perform the
forward write and a later short line can make the final `log_message()` input
short again.

No `/shared/success.txt` was produced, and `/backdoor` was not invoked manually.

## Environment

Isolated recovery extraction:

```text
/tmp/phase2_recovery_next/lab
```

Container:

```text
container: IC_PHASE2_RECOVERY
base image: ic_image_phase2_tools
mount: /tmp/phase2_recovery_next/lab/shared -> /shared
ASLR: 0
```

Binary hash:

```text
server_2 sha256 = 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

The analysis container was separate from the live
`/Users/iKev/.cache/codex-phase2-complete/lab/shared` runtime state.

## Probe A - Direct Libc System First-Argument Check

Before testing the new non-stack staging idea, this pass checked whether a
6-byte libc partial return to `system()` could avoid appended ROP.

Result under `gdb`:

```text
target = __libc_system
system address = 0x7ffff7b54750
rdi = 0x7ffff7d01710 <_IO_stdfile_1_lock> ""
rsi = 0x0
rdx = 0x7ffff7fb0310
rax = 0x404100
rbp = 0x4141414141414141
rsp = 0x7fffffffec00
success_exists = no
```

Interpretation:

- a 6-byte libc return target is writable through the C-string path because the
  first six address bytes are non-NUL;
- the first NUL still terminates the string before any post-RIP stack chain can
  be staged;
- direct `system()` receives a stale libc/internal pointer, not controlled
  command text;
- this closes direct libc `system()` as a no-chain first-argument setup.

## Probe B - Multi-Line Non-Stack Staging

Hypothesis:

```text
If parse_config() accepts repeated user_input keys, a first long value can stage
bytes beyond user_input into heap-adjacent memory, and a second short value can
reset user_input before log_message() copies it.
```

Observed at the `run_server()` breakpoint:

```text
long first value length = 3474
second value = SHORT-RESET
rip = 0x401688 <run_server()>
user_input = "SHORT-RESET"
0x404ff0 = staged marker bytes
0x405000 = staged marker bytes
```

The program then continued through `run_server()` and exited normally:

```text
[+] Running server...
[LOG]: SHORT-RESET
program exited normally
success_exists = no
```

Interpretation:

- the long first line performed the forward non-stack write;
- the short second line reset the global C string used by `log_message()`;
- the prior "long heap write necessarily crashes in `sprintf()`" conclusion is
  now too broad for multi-line config input;
- this is a staging primitive, not a full exploit route.

## Updated Boundary

Validated:

1. A non-stack staging primitive exists for this lab binary:
   repeated `user_input=` lines can leave attacker-chosen bytes around
   `0x405000` while keeping the final `user_input` short.
2. Direct libc `system()` without an argument setup is still blocked:
   `rdi` is not controlled at the hijacked return.
3. A libc first target still cannot carry a normal post-RIP chain because the
   six-byte target write is followed by the C-string terminator.

Still not solved:

1. No path has yet made `rdi` point at the staged non-stack bytes.
2. No verified pivot points `rsp` at the staged non-stack bytes.
3. The staged address range around `0x405000` contains NUL bytes in its pointer
   representation, so it cannot simply be embedded as a full pointer in the
   same C-string path.
4. A quick libc/libstdc++ motif scan did not identify an immediate
   `rsp`-relative single gadget that points the first argument back to the
   overflow buffer and then calls `system()` or `execve()`.

## Next Technical Gate

Continue only from the new multi-line primitive. Do not repeat the single-line
heap crash probe.

The next useful bounded check is:

```text
Identify whether any live object, pointer, or later call path reads from the
staged 0x405000-region bytes after parse_config() but before or during the
hijacked control-flow point.
```

Concrete next checks:

1. Map the heap contents before and after the first long line to see whether the
   staged region overlaps a live allocator chunk, stream buffer, or C++ runtime
   object.
2. Search for a single-hop target that sets `rdi` from a non-stack source
   reachable from the staged region.
3. If no reader/path exists, treat the multi-line primitive as useful evidence
   but not a full-credit route.

