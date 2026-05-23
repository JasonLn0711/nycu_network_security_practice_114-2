# Phase II BSS-Indirect Dispatch Feasibility - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) and the pinned Ubuntu 24.04
libc from a controlled local extraction of `lab.zip`.

Experiment ledger ID: `P2-EXP-017` in `docs/PHASE2_EXPERIMENT_LOG.md`.

Companion notes for the same dated session:

- `PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md`
  records `P2-EXP-015` (post-stream first-argument transfer check, with
  live IC core evidence) and `P2-EXP-016` (precise multi-line `.bss`
  staging boundary at `L=3264`).

This block is a deeper static slice of the same problem space: it focuses
specifically on whether a single-shot register-derived `rdi` setup can
land the first argument inside the multi-line `.bss` staging range while
the call/jmp tail still resolves to an exec-family symbol. It does not
rerun a live IC; it complements `P2-EXP-015` with the explicit gadget
tables that the live block did not enumerate.

## Why This Block Exists

The previous closed paths force the next hypothesis to start from a different
primitive. The full-credit recovery cannot keep using:

- the appended ROP path after saved RIP (caller-stack qwords are fixed);
- the preserved-saved-RBP path (the C-string copy embeds NUL bytes before saved
  RIP can be overwritten);
- direct reuse of post-`log_message` `rax` as a controlled command pointer
  (`rax` is forced to `0x404100` = `&std::cout`);
- direct reuse of post-`log_message` `rdi` as a controlled command pointer
  (`rdi` is forced to `0x7ffff7d00710` = `_IO_stdfile_1_lock`, an empty libc
  buffer);
- a simple backward stack pivot (no `sub rsp` / `add rsp, neg` / `mov rsp, reg`
  / `xchg rsp, reg` family member exists in the fresh `server_2` plus pinned
  libc).

This block treats the multi-line `.bss` staging primitive as the only available
non-stack data primitive (its safe boundary is now confirmed in `P2-EXP-016` at
`L=3264`, with allocator-state crashes beginning at `L>=3300`) and asks whether
any single-shot gadget can use it as a first-argument source.

## Hypothesis

After `log_message()` returns, the post-call register state is fixed (per the
`P2-EXP-014` register dump):

```text
rax = 0x404100              # copied std::cout object
rdi = 0x7ffff7d00710        # _IO_stdfile_1_lock (libc-mapped, EC-unwritable)
rsi = 0x0
rdx = 0x7ffff7faf310        # libstdc++ ostream vtable area (read-only)
rcx = 0x7ffff7c175a4        # libc write() text (read-only)
```

`rax` is the only register pointing at memory that the EC can also reach
through its writable primitive. The forward `strcpy()` from `parse_config()`
into global `user_input` (`0x404340`) plus the multi-line staging finding can
plant bytes in the writable `.bss`/page-tail range
`[0x404340 .. 0x404FFF]`.

The hypothesis is therefore:

> A single-shot binary or libc gadget exists that
>
> 1. sets `rdi` from `rax + small disp` (or from another register whose value
>    at `log_message` return can be steered to point at the `0x404340..0x404FFF`
>    multi-line staging range),
> 2. then transfers control (`jmp` / `call` / fall-through `ret`) to `system`,
>    `execve`, `execvp`, `posix_spawn`, or another libc routine that calls one
>    of those with `rdi` preserved,
> 3. without requiring an appended ROP chain after the saved RIP,
> 4. without requiring a preserved canonical saved RBP,
> 5. without requiring direct reuse of post-`log_message` `rax` or `rdi` as the
>    first argument value itself.

## Falsifiable Prediction

This hypothesis is supported only if the fresh `server_2` plus pinned
`libc.so.6` contains at least one such single-shot gadget reachable through the
existing partial saved-RIP overwrite (low-three-byte target inside
`0x401000..0x401a21` for the binary, or any address representable through the
same partial overwrite for libc).

The hypothesis is falsified if no such gadget exists in the tested artifact
set. In that case, no live EC candidate should be run for this hypothesis
because there is no concrete first-stage address to validate.

## Bounded Validation Contract

Run one static feasibility block:

1. Re-extract a fresh local `lab/` from `projects/project-ii-apt-agent/lab.zip`
   and confirm `server_2` SHA-256 matches the recorded hash.
2. Use the pinned libc copy that already matches the live container's libc
   (BuildID `8e9fd827446c24067541ac5390e6f527fb5947bb`).
3. Search both binaries for the candidate single-shot families:
   - `lea rdi, [rax+disp{8,32}]; (jmp|call) <system|execve|execvp|posix_spawn>`;
   - `mov rdi, [rax+disp{8,32}]; (jmp|call) <system|execve|execvp|posix_spawn>`;
   - `lea rdi, [rax+disp]; ret` followed by a single fixed return target that
     consumes pre-RIP bytes only (no appended ROP qword);
   - `mov rdi, r{bx,12,13,14,15}; (jmp|call) <system|execve-family>` where the
     source register is callee-saved through `log_message` and could plausibly
     be coerced into the staging range.
4. For each candidate, decode the call/jmp target and verify it resolves to one
   of the exec-family symbols.
5. If a candidate is found, document the exact `disp`, the resulting first-arg
   address, and the staged value layout. Stop the static block before any
   live-IC run; the live block becomes the next bounded experiment.
6. If no candidate is found, record the negative result and stop.

Do not broaden this into a general gadget search or another `.text` sweep.

## Environment

This pass used the in-tree extraction:

```text
host workspace: /home/jnclaw/every_on_git_jnclaw/phd-life-system/nycu_network_security_practice_114-2
extracted lab: /tmp/p2_explore/lab
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
pinned libc: /tmp/project2_pivot_static/libc.so.6
libc sha256: d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
libc executable file range: 0x28000 .. 0x1afd39
```

No live IC container was started for this static feasibility block. No
`/shared/success.txt` was created; no `/backdoor` was invoked manually.

## Result

Closed at the static feasibility stage.

The pinned libc and `server_2` searches found:

```text
lea rdi, [rax+disp32]; call rel32   total = 6   reaching exec-family = 0
lea rdi, [rax+disp8];  call rel32   total = 23  reaching exec-family = 0
lea rdi, [rax+disp];   jmp  rel32   total = 0
lea rdi, [rax+disp];   ret          total = 0
mov rdi, [rax+disp];   jmp  rel32   total = 0
mov rdi, [rax+disp];   call rel32   total = 0   (no qualifying tail)
mov rdi, [rax];        ret          total = 0
```

The six `lea rdi, [rax+disp32]; call rel32` matches in libc resolve to:

```text
off=0x2a02d  disp=+0xa30  -> __pthread_mutex_unlock
off=0xa5798  disp=+0x670  -> internal helper near gnu_get_libc_version (assert path)
off=0x183abb disp=+0xa08  -> internal helper
off=0x183c70 disp=+0xa08  -> internal helper
off=0x183ee7 disp=+0xa30  -> __pthread_mutex_unlock
off=0x184074 disp=+0xa30  -> __pthread_mutex_unlock
```

None of these reaches `system` (`0x58750`), `execve` (`0xeef30`), `execvp`
(`0xeefa0`), or `execvpe` (`0xeefc0`). Mutex helpers do not invoke the shell or
exec.

The 23 `lea rdi, [rax+disp8]; call rel32` matches all use `disp` in
`{0x1, 0x3}`, so `rax + disp` falls inside the `cout` object at `0x404100`,
not inside the EC-controllable `0x404340..0x404FFF` staging range.

The `server_2` text gadget search found:

```text
lea rdi, [rip+disp]   total = 0
mov rdi, [rip+disp]   total = 0
mov rdi, [rax]        total = 0
mov rdi, [rax+disp]   total = 0
mov rdi, [rsp+disp]   total = 0
pop rdi; ret          total = 0
```

The two reachable `mov edi, 0x4040d8; jmp rax` gadgets in the binary
(`0x401387` and `0x4013c9`) hardcode `rdi = 0x4040d8`. The address `0x4040d8`
is in `.data` *before* `user_input` at `0x404340`; the forward `strcpy()`
primitive cannot reach it. The two libc `mov edi, 0xe0; jmp rax` matches
(at libc offsets `0x85f7f` and `0x8604f`) hardcode a tiny constant that points
into unmapped low memory.

The exec-family direct-call sites in libc (`call execve` in `execvpe`,
`do_system`, etc.) are preceded by `mov rdi, rbx`, `mov rdi, r8`, or
`mov rdi, r15`. None of those source registers is pinned to a value that
points at the multi-line staging range at `log_message` return time, and no
secondary single-shot gadget was found that prepares one of them from `rax`
without an intermediate appended ROP qword.

## Interpretation

The single-shot register-derived first-argument route into the multi-line
`.bss` staging range is closed in the supplied Phase II main binary plus
pinned libc family.

This does not prove that every conceivable indirect dispatch is impossible. It
closes the narrow family that:

- can be reached from the partial saved-RIP overwrite,
- sets `rdi` from a register whose value at `log_message` return is either
  fixed at `0x404100` (`rax`) or settable by the gadget itself,
- reaches an exec-family call in one shot,
- falls within the multi-line staging address range.

Combined with the prior closed paths, the remaining technical recovery surface
now requires either:

- a fundamentally different writable primitive (heap-allocator manipulation
  that survives the `sprintf()` crash, file-descriptor or fopen hijack via a
  shared-volume race, or kernel-level escalation), or
- an unblock from the instructor on whether a protocol-complete partial
  package is acceptable when official IC-side `/shared/success.txt` is
  unreachable through the supplied surface.

## Updated Boundary

Add to the closed list:

- single-shot `lea/mov rdi, [rax+disp]; (jmp|call) exec-family` gadget reaching
  the multi-line `.bss` staging range in the supplied binary plus pinned libc;
- single-shot `mov rdi, r{bx,8,12,13,14,15}; (jmp|call) exec-family` gadget
  whose source register is provably steered into the staging range without
  appended ROP, preserved RBP, or direct `rax` reuse.

Both items are now treated as closed at static feasibility unless a new artifact
(different binary, different libc, or a newly written gadget) changes the search
surface.

## Decision

Do not run a live EC candidate for this hypothesis class. There is no concrete
single-shot first-stage address to validate.

The recommended next bounded blocks, in order of cost:

1. **Submission-track follow-through.** Use `docs/TA_CLARIFICATION_DRAFT.md`
   and `docs/PARTIAL_SUBMISSION_BRIEF.md` to confirm whether the
   protocol-complete partial package is the intended upload. This is the
   highest-value next move because it does not consume any new technical
   budget and resolves the grading posture.
2. **Heap-allocator state hypothesis.** A separate bounded block could ask
   whether the `tcache` corruption observed during the multi-line probe
   (`malloc(): unaligned tcache chunk detected`) can be turned into a
   controlled allocator side effect that supplies a first-argument pointer
   without crashing `sprintf()`. This would need its own falsifiable
   prediction and a fresh dated attempt note before any live IC run; it is
   explicitly out of scope for the current block.
3. **External-environment hypothesis.** A separate bounded block could ask
   whether a `/shared`-mounted file other than `config.data` can be used to
   inject state that the IC reads through a different code path. This must
   not invoke `/backdoor` directly and must produce `/shared/success.txt`
   only through the official IC side.

Until one of those new mechanisms is identified, the correct submission
posture remains:

```text
Protocol-complete partial package; official IC-side success evidence pending.
```
