# Phase II Completion Attempt - 2026-05-14

Scope: supplied Project II Phase II IC (`server_2`) in an x86_64 Colima Docker
VM, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger IDs: `P2-EXP-002`, `P2-EXP-003` in
`docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

Project II is still **not full-credit complete**.

The 2026-05-14 pass reproduced the official Phase II lab locally and ruled out
the main one-shot paths that were still plausible after the 2026-05-13 handoff:

- the existing ret-to-`maintenance_task+5` candidate does not create
  `/shared/success.txt`;
- stack-resident shellcode reaches the intended stack address but faults under
  NX before executing;
- a bounded text-section partial-return sweep over `0x401000..0x401a20` with
  four command prefixes found no target that created `/shared/success.txt`.

The honest state is therefore a protocol-complete, well-documented partial
submission plus stronger negative evidence. Do not mark the assignment complete
until the official IC creates `/shared/success.txt` through `/backdoor`.

## Environment

The local macOS host did not have a working Docker engine at the start of this
pass. A disposable headless validation path was built:

```sh
brew install qemu colima docker lima-additional-guestagents
colima start --profile phase2 --arch x86_64 --vm-type qemu --cpu 2 --memory 4 --disk 20 --mount-type 9p
docker context use colima-phase2
```

The IC image was built from the official lab bundle:

```sh
docker build --platform linux/amd64 -t ic_image /Users/iKev/.cache/codex-phase2-complete/lab/IC
```

The live IC was started manually to avoid `docker.sh` interactive `-it`
assumptions:

```sh
docker run -dit --name IC_PHASE2 --platform linux/amd64 --privileged \
  -v /Users/iKev/.cache/codex-phase2-complete/lab/shared:/shared \
  ic_image bash
docker cp /Users/iKev/.cache/codex-phase2-complete/lab/IC/server_2 IC_PHASE2:/blogic
docker cp /Users/iKev/.cache/codex-phase2-complete/lab/IC/server_2 IC_PHASE2:/shared/blogic
docker cp /Users/iKev/.cache/codex-phase2-complete/lab/IC/backdoor IC_PHASE2:/backdoor
docker cp /Users/iKev/.cache/codex-phase2-complete/lab/IC/runserver.sh IC_PHASE2:/runserver.sh
docker exec IC_PHASE2 chmod +x /blogic /runserver.sh /backdoor
docker exec IC_PHASE2 sysctl -w kernel.randomize_va_space=0
docker exec -d IC_PHASE2 /runserver.sh
```

Verified runtime facts:

```text
glibc: ldd (Ubuntu GLIBC 2.39-0ubuntu8.7) 2.39
ASLR: 0
live libc base observed in /blogic maps: 0x7ffff7afc000
blogic text: 0x401000..0x402000
blogic writable segment: 0x404000..0x405000
heap immediately follows: 0x405000..0x426000
```

## Baseline Candidate

The existing scaffold candidate wrote:

```text
user_input='; /backdoor; # + padding to 97 user bytes + 0x401475 low 3 bytes
```

Observed result:

```text
success_exists=no
coredumps=
config_size=112
server_log_tail=|
```

This reproduces the previous result: returning to `maintenance_task+5` is
reachable, but the stale `rdi` value is not the controlled `user_input` pointer.

## Register State At The Overflow

Under `gdb`, a marker crash at the return from `log_message` showed:

```text
rip = 0x4242424242424242
rsp = 0x7fffffffec00
rbp = 0x4242424242424242
rax = 0x404100
rdi = 0x7ffff7d01710 (_IO_stdfile_1_lock, zero bytes)
rsi = 0x0
rdx = 0x7ffff7fb0310 (_ZTVSo+24)
rcx = 0x7ffff7c185a4
r8  = 0x73
```

The controlled stack bytes begin at the `log_message` local buffer:

```text
local_buffer = 0x7fffffffeb90
user bytes begin at local_buffer + 7 = 0x7fffffffeb97
saved RIP slot = 0x7fffffffebf8
```

With the short partial-return candidate, bytes after the saved RIP are not
controlled because the C string terminates at the high zero byte of the target:

```text
0x7fffffffebf8: 0x0000000000401475
0x7fffffffec00: 0x00007fffffffec10
0x7fffffffec08: 0x00000000004017f0
```

This is why a normal ROP chain cannot simply be appended after the first
partial return address.

## NX Check

A null-free stack shellcode probe was placed at the controlled stack value start
and the saved return address was partially overwritten to `0x7fffffffeb97`.

Observed under `gdb`:

```text
Program received signal SIGSEGV
rip = 0x7fffffffeb97
=> 0x7fffffffeb97: xor %edx,%edx
```

Interpretation: control reaches the shellcode address, but the stack is not
executable. This confirms the Phase II NX constraint in the live runtime.

## One-Shot Text Sweep

The pass then tested all representable byte offsets in the executable text
range with four command prefixes:

```text
range: 0x401000..0x401a20
prefixes:
  b"'; /backdoor; #"
  b"x'; /backdoor; #"
  b"; /backdoor; #"
  b"/backdoor #"
ret offset: 97 user bytes
timeout: 0.35s per /blogic process
```

Result:

```json
{
  "status": "no_success",
  "tried": 10328,
  "elapsed_seconds": 545.3
}
```

This sweep is preserved as `scripts/run_phase2_one_shot_sweep.py` so future
agents can reproduce or extend it without rewriting the harness.

## Current Boundary

The remaining solution probably cannot be a simple one-shot partial return into
`server_2` text, direct stack shellcode, or direct ret-to-maintenance. The next
credible route must solve at least one of these constraints:

1. create an argument-control path despite `rdi` being clobbered by the final
   C++ stream call;
2. find a pivot that does not require appending a normal NUL-bearing ROP chain
   after the partial return address;
3. use the `.bss` to heap overflow adjacency in a controlled way, without
   relying on a grader bypass;
4. identify a libc or libstdc++ one-shot gadget that uses current registers or
   already-controlled pre-return stack bytes to call a command interpreter with
   a controlled command string.

## Do Not Repeat

Do not spend more time on these as if they are untested:

- direct ret-to-`maintenance_task+5`;
- direct stack shellcode;
- one-shot partial returns to all byte offsets in `0x401000..0x401a20` with the
  four prefixes above.

The project should remain marked partial until an IC-side `/shared/success.txt`
is observed.

## Next Agent Direction

The next Codex run should start from `../../../../HANDOFF_PHASE2.md`, not from a
fresh binary survey.

Immediate start checks:

1. Verify `docker context show` is still `colima-phase2`.
2. Verify `IC_PHASE2` still has `/runserver.sh` and `/blogic` running.
3. Verify `/proc/sys/kernel/randomize_va_space` is still `0`.
4. Verify `/shared/success.txt` is still absent before trying a new candidate.
5. Re-check `/proc/<blogic-pid>/maps` if using libc or libstdc++ addresses.

Best next direction:

- Focus on argument control or stack pivot feasibility under C-string/NUL-byte
  constraints.
- Do not run another broad `.text` sweep unless the prefix set, offset model, or
  success condition changes.
- Treat libc/libstdc++ gadget work as useful only after a pivot or first-argument
  setup is clearly specified.

Stop condition for the next block:

- one candidate path has a clear result, either a new IC-side
  `/shared/success.txt`, a register/core artifact that explains failure, or a
  documented reason that the path is infeasible.
