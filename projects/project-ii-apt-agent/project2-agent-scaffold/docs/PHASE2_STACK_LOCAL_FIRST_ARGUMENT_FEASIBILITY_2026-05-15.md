# Phase II Stack-Local First-Argument Feasibility - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) and the pinned Ubuntu 24.04
libc from the controlled local Phase II lab.

Experiment ledger ID: `P2-EXP-018` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Why This Block Exists

`P2-EXP-015` left one important gap to close before moving to a heavier heap
hypothesis. The live post-stream core showed that controlled pointers still
exist near the `log_message()` return boundary:

```text
rsp = 0x7fffffffec48
[rsp-0x70] = 0x0000000000404340  # preserved local slot pointing at user_input
[rsp+0x08] = 0x00007fffffffec00  # caller qword pointing into controlled stack bytes
```

That suggests a first-argument setup route distinct from the already-closed
paths:

- it does not append a ROP chain after saved RIP;
- it does not require saved RBP to be canonical;
- it does not directly reuse post-stream `rax` as the command pointer;
- it does not rely on `.bss` dispatch from `rax + disp` as tested in
  `P2-EXP-017`.

The remaining question for this family is whether a first-stage target can
consume a preserved stack-local pointer and immediately reach a success-relevant
call.

## Hypothesis

A reachable main-binary or libc sequence exists that performs one of these
first-argument setup operations from the current `rsp` region:

```text
mov rdi, [rsp + signed_disp]
lea rdi, [rsp + signed_disp]
```

and then directly calls or jumps to one of:

```text
system, execv, execve, execvp, execvpe, posix_spawn, posix_spawnp
```

without requiring:

- a second appended qword after the overwritten saved RIP;
- a valid saved RBP frame;
- direct `rax` reuse;
- a broad heap overwrite.

A qualifying candidate would need to land `rdi` on either:

- the preserved pointer at `[rsp-0x70]` (`0x404340`, pointing at staged
  `user_input`), or
- the controlled stack bytes reachable from the caller qword at `[rsp+0x08]`,
  if using `lea rdi, [rsp+disp]` directly.

## Bounded Validation Contract

Run one static feasibility block only:

1. Re-extract a fresh `server_2` from `projects/project-ii-apt-agent/lab.zip`.
2. Use the pinned libc already copied from the local IC.
3. Resolve libc offsets for `system`, `execv`, `execve`, `execvp`, `execvpe`,
   `posix_spawn`, and `posix_spawnp`.
4. Search `server_2` and libc executable ranges for stack-relative first-arg
   setup patterns followed by direct `call rel32`, `jmp rel32`, or binary
   `call/jmp [system@GOT]` tails.
5. Record `rbp`-relative hits only as non-viable sanity checks, because the
   saved-RBP route is already closed.
6. Manually disassemble any apparent hit before promoting it to a live IC
   candidate.

No live IC run should occur unless a concrete candidate survives static and
manual-disassembly review.

## Environment

```text
extracted lab: /tmp/p2_exp018/lab
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
pinned libc: /tmp/project2_pivot_static/libc.so.6
libc sha256: d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
libc targets:
  system      0x58750
  execv       0xeef10
  execve      0xeef30
  execvp      0xeefa0
  execvpe     0xeefc0
  posix_spawn 0x10ecd0
  posix_spawnp 0x10fef0
```

The scanner was a one-off local Python byte scan over executable PT_LOAD ranges
for:

```text
48 8b 7c 24 xx          mov rdi, [rsp+disp8]
48 8d 7c 24 xx          lea rdi, [rsp+disp8]
48 8b bc 24 xx xx xx xx mov rdi, [rsp+disp32]
48 8d bc 24 xx xx xx xx lea rdi, [rsp+disp32]
```

plus non-viable `rbp` analogues for comparison. For every direct exec-family
call/jump tail, the scan checked the preceding 48 bytes for these patterns.

No `/backdoor` invocation occurred. No live IC candidate was run for this block.

## Result

Closed at static feasibility.

### Main binary result

`server_2` contains no stack-relative or `rbp`-relative `rdi` setup pattern in
its executable text:

```text
mov rdi, [rsp+disp8]   0
lea rdi, [rsp+disp8]   0
mov rdi, [rsp+disp32]  0
lea rdi, [rsp+disp32]  0
mov rdi, [rbp+disp8]   0
lea rdi, [rbp+disp8]   0
```

The scanner observed two `system` tails in the main binary family (the normal
`maintenance_task()` call path and the `system@plt` indirect jump), but neither
has a stack-relative `rdi` setup before it.

### libc result

The pinned libc does contain stack-relative setup instructions in general:

```text
mov rdi, [rsp+disp8]   43
lea rdi, [rsp+disp8]   25
mov rdi, [rsp+disp32]  7
lea rdi, [rsp+disp32]  13
```

However, direct exec-family/system tails with a nearby first-argument setup
reduce to only three apparent hits:

```text
0xef2b8: mov rdi, [rbp-0x60]; call execve
0xef752: mov rdi, [rbp-0x48]; call execve
0x1111e7: lea rdi, [rsp+0x64]; call posix_spawn
```

Manual disassembly rejects all three as candidates:

1. `0xef2b8` and `0xef752` are `rbp`-relative `execvpe()` internal paths. They
   need a valid libc frame and meaningful `rbp-0x60` / `rbp-0x48` contents.
   That reintroduces the preserved-saved-RBP dependency that this block is not
   allowed to assume.
2. `0x1111e7` is an internal `__waitpid()` path:

   ```text
   0x1111e7: lea rdi,[rsp+0x64]
   0x1111ec: lea r8,[rsp+0x70]
   0x1111f1: xor ecx,ecx
   0x1111f3: lea rsi,[rip+0xba235]  # "/bin/sh"
   0x1111fa: call posix_spawn
   ```

   For `posix_spawn(pid_t *pid, const char *path, ...)`, `rdi` is the output
   `pid_t *`, not the executable path. The executable path is `rsi`, fixed to
   libc's `"/bin/sh"`, not `/backdoor` or controlled `user_input`. This does
   not create `/shared/success.txt` and does not meet the assignment success
   condition.

A raw byte scan also produced one apparent `lea rdi, [rsp+0xe0]` ret-style hit
inside `__waitpid()`, but manual disassembly showed the `c3` byte belonged to a
`call` displacement, not a real `ret` instruction. It is a scanner false
positive and is not a gadget.

## Interpretation

The stack-local first-argument setup family is closed for the supplied artifact
set:

- no main-binary stack-relative `rdi` setup exists;
- libc stack-relative setup exists but does not lead to `system`/`execve` with a
  controlled first argument;
- the only stack-relative `posix_spawn` hit controls the wrong argument and
  points at `/bin/sh`, not `/backdoor`;
- `rbp`-relative `execve` hits are invalid because the saved-RBP route is
  already blocked by the C-string/NUL-byte constraint.

This matters because it removes the most plausible non-appended-ROP way to use
the preserved `[rsp-0x70] = 0x404340` pointer observed in the live core.

## Decision

Do not run a live EC candidate for this hypothesis class. There is no surviving
first-stage address that consumes the stack-local pointer into a success-relevant
first argument.

The next technical block should not be another register/stack-local gadget
search unless a new binary/libc artifact changes the search surface. The only
technical route still worth a bounded experiment is a **precise heap-allocator
state hypothesis** that explains how the `L>=3300` allocator boundary can become
a controlled primitive instead of a crash. If no such heap invariant plan is
available, switch to submission-track follow-through and TA clarification.
