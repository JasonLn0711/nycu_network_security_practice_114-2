# Phase II Argument-Control Attempt - 2026-05-14

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

## Direct Result

Project II is still **not full-credit complete**.

This pass tested the recommended next handoff direction: whether the current
pre-return stack/register state can be turned into a controlled first argument
for the existing `maintenance_task()` path, instead of repeating the already
failed direct ret-to-`maintenance_task+5` or broad `.text` sweep.

The bounded result is:

- no `/shared/success.txt` was created;
- the IC-side `/backdoor` was not invoked manually;
- a maintenance-body entry candidate reached `maintenance_task+22`
  (`0x401486`) and stopped at that instruction because `rbp` was not a valid
  frame pointer;
- the run confirms an important constraint: the original saved frame pointer
  would have made an attractive argument-control path, but the `strcpy` /
  `sprintf` C-string path prevents preserving that canonical pointer while also
  overwriting saved RIP.

## Environment

This pass used a fresh local extraction:

```text
/tmp/phase2_next/lab
```

The isolated IC was started as:

```text
docker context: default
container: IC_PHASE2_NEXT
image: ic_image_phase2_next
mount: /tmp/phase2_next/lab/shared -> /shared
ASLR: 0
processes: /bin/bash /runserver.sh and /blogic
success artifact before probe: absent
```

The live Phase II binary matched the previously recorded `server_2` hash:

```text
155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

## Static Facts Rechecked

Relevant symbols:

```text
log_message(char const*)      = 0x401416
maintenance_task(char const*) = 0x401470
maintenance_task+22           = 0x401486
run_server()                  = 0x401688
user_input (.bss)             = 0x404340
```

Relevant code behavior:

- `run_server()` passes `user_input` to `log_message()`.
- `log_message()` stores that pointer at `[rbp-0x68]`, then formats
  `"[LOG]: %s"` into a local stack buffer.
- Saved RBP begins after `89` bytes of the `user_input` value.
- Saved RIP begins after `97` bytes of the `user_input` value.
- At `maintenance_task+22`, the function expects a valid frame pointer and
  reads its would-be argument from `[rbp-0x88]`.

## Probe 1 - Layout Confirmation

A marker run confirmed the live stack layout:

```text
rip = 0x40146f <log_message(char const*)+89>
rsp = 0x7fffffffec48
rbp = marker-controlled bytes
rdi = 0x7ffff7d00710
rax = 0x404100
```

Important stack slots from the same core:

```text
local_buffer begins around 0x7fffffffebe0
user bytes begin at local_buffer + 7
stored original log_message argument at 0x7fffffffebd8 = 0x404340
saved RBP slot at 0x7fffffffec40
saved RIP slot at 0x7fffffffec48
untouched caller stack after short overwrite:
  0x7fffffffec50 = 0x00007fffffffec60
  0x7fffffffec58 = 0x00000000004017f0
```

This explains why the argument-control path looked promising: if execution
entered `maintenance_task+22` with `rbp = 0x7fffffffec60`, then
`[rbp-0x88]` would read the preserved `0x404340` pointer to `user_input`.

## Probe 2 - Maintenance Body Entry

The next candidate used the same lab-only command-shaped `user_input` prefix,
then targeted `maintenance_task+22` (`0x401486`) instead of
`maintenance_task+5`.

Observed result:

```text
success_exists=no
core=/shared/coredump/blogic-58.core
signal=SIGBUS
rip=0x401486 <maintenance_task(char const*)+22>
rsp=0x7fffffffec50
rbp=0x2154534554504252
rdi=0x7ffff7d00710
```

The candidate reached the intended maintenance-body instruction, but `rbp`
contained the marker bytes from the saved-RBP slot. The instruction at
`0x401486` then tried to dereference `[rbp-0x88]`, which is not a valid mapped
address.

## Constraint Proven By This Pass

The candidate needs two things at once:

1. saved RBP must remain or become a canonical stack pointer such as
   `0x00007fffffffec60`;
2. saved RIP must be partially overwritten to a useful text address such as
   `0x401486`.

The input path blocks that direct combination:

- bytes `89..96` of `user_input` overwrite saved RBP;
- bytes `97..` overwrite saved RIP;
- a useful stack pointer needs high bytes `00 00`;
- embedded NUL bytes terminate `strcpy` / `sprintf`;
- if the string terminates while preserving saved RBP, it cannot continue to
  overwrite saved RIP;
- if the string continues to saved RIP, saved RBP's high bytes are polluted and
  become non-canonical.

Therefore, "enter `maintenance_task+22` and use preserved original RBP" is not a
complete path under the current input model.

## Do Not Repeat

Do not repeat these as open possibilities without a new encoding or staging
idea:

- direct ret-to-`maintenance_task+5`;
- broad one-shot `.text` sweep with the already tested prefixes;
- direct stack shellcode;
- direct entry to `maintenance_task+22` while assuming saved RBP can stay
  canonical.

## Next Direction

The next useful block should search for a path that avoids needing both a
canonical saved RBP and a saved RIP overwrite in the same C string.

Best bounded directions:

1. Find a target that sets its own frame from `rsp`, does not need the corrupted
   saved RBP, and still derives the first argument from a preserved stack slot
   or the `user_input` global.
2. Investigate whether untouched caller-stack qwords after the short partial RIP
   overwrite can be used as a one-step staging source, without needing a normal
   appended ROP chain.
3. Only revisit libc or libstdc++ gadgets after proving where a canonical
   next-address qword can be staged under the C-string/NUL-byte constraint.

Stop condition for the next block remains the same: one candidate path should
end with either `/shared/success.txt`, a core/register artifact explaining
failure, or a documented infeasibility reason.
