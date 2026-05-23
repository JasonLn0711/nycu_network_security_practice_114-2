# Phase II Post-Stream Argument And BSS Boundary Attempt - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in an isolated local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger IDs: `P2-EXP-015`, `P2-EXP-016` in
`docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

Project II is still **not full-credit complete**.

This pass did not use the already closed direct current-`rdi` route. It tested
two narrower questions:

- after the final C++ stream call in `log_message()`, is there still a controlled
  pointer that a single first-stage sequence can move into the first argument and
  immediately use for a success-relevant call?
- can multi-line non-stack staging be bounded more precisely than the earlier
  broad heap/global check?

The result is mixed:

- post-stream controlled data still exists in stack/local and `.bss` memory;
- no usable single-stage `rdi` setup plus `system`/`execve` call sequence was
  found in the fresh main binary plus pinned libc;
- `.bss` staging is precise up to the end of the data page;
- crossing into allocator state is reproducibly unstable and not a full-credit
  route by itself;
- no official IC-side `/shared/success.txt` appeared.

## Environment

```text
container: IC_PHASE2_P15
image: ic_image
mount: /tmp/project2_phase2_p15/lab/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
libc sha256: d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
```

The disposable container was removed after evidence capture. The local evidence
directory was:

```text
/tmp/project2_phase2_p15/
```

## P2-EXP-015 - Post-Stream First-Argument Transfer Check

### Hypothesis

The final C++ stream calls clobber direct `rdi`, but a controlled pointer may
still survive in a fixed stack/local slot or original caller-stack qword, and a
single reachable sequence may move that pointer into the first argument and call
`system()` or `execve()` without appended ROP.

### Procedure

1. Create a marker config that reaches `log_message()` return and forces a core
   at the `ret` boundary:

   ```text
   user_input=RMAP-P2-EXP015;AAAA...BBBBBBBB
   ```

2. Trigger the official IC loop by writing `/shared/exploit_done`.
3. Confirm no `/shared/success.txt`.
4. Inspect `/tmp/project2_phase2_p15/lab/shared/coredump/blogic-30.core`.
5. Byte-scan the pinned libc and the fresh main binary for exact first-stage
   sequences that set `rdi` from post-stream stack/register state and make a
   success-relevant call without a second appended qword.

### Core Evidence

At the crash boundary:

```text
rip = 0x40146f              # log_message ret
rsp = 0x7fffffffec48
rbp = 0x4141414141414141
rax = 0x404100              # std::cout copy object, not a function pointer
rdi = 0x7ffff7d00710        # _IO_stdfile_1_lock, zero bytes
rsi = 0x0
rdx = 0x7ffff7faf310
```

Useful controlled data still existed, but not in a directly callable first
argument:

```text
$rsp-0x70 = 0x0000000000404340  # preserved local slot pointing to user_input
$rsp+0x08 = 0x00007fffffffec00  # original caller qword pointing into controlled stack buffer
0x404340 = "RMAP-P2-EXP015;AAAA..."
```

### Static Scan Result

The fresh libc contains direct `execve` call sites, but the bounded byte-offset
scan found:

```text
direct_system_or_execve_calls: 10
rdi_setup_to_system_or_execve_gadgets: 0
pop_rdi_call_rax_gadgets: 1
```

The one `pop rdi; call rax` sequence is not useful for this state:

```text
offset: 0x129a61
absolute low six bytes: 61 4a c2 f7 ff 7f
sequence: pop rdi; call rax
post-stream rax: 0x404100
```

`rax = 0x404100` is the copied `std::cout` object in writable data, not
`system()` or another executable success path.

### Verdict

Closed for the tested single-stage first-argument family.

This does not prove that all libc or heap routes are impossible. It does prove
that the current post-stream state does not give a simple single-stage gadget
that loads a controlled pointer into `rdi` and immediately calls
`system()`/`execve()` without appended ROP.

## P2-EXP-016 - Precise BSS Non-Stack Staging Boundary

### Hypothesis

Multi-line `user_input=` staging can safely fill the `.bss`/data-page tail up to
the allocator boundary, but crossing into heap/tcache state is not stable unless
a precise allocator plan exists.

### Procedure

For each stage length, write:

```text
user_input=STAGELENNNNN;SSSS...
user_input=P15-FINAL;AAAA...BBBBBBBB
```

The final line is intentionally short enough to leave prior staged bytes after
its terminating NUL, while still forcing a core if `log_message()` is reached.

Tested first-line stage lengths:

```text
2048, 3000, 3200, 3264, 3300, 3400, 3500, 3600, 3700, 3800, 4000
```

### Boundary Results

```text
L=3200 -> reached log_message ret, SIGSEGV at 0x40146f, no success
L=3264 -> reached log_message ret, SIGSEGV at 0x40146f, no success
L=3300 -> crashed in libc tcache_get_n before final log_message ret, no success
L=3400 -> crashed in libc tcache_get_n before final log_message ret, no success
L>=3500 -> SIGABRT in allocator path, no success
```

The `L=3264` core showed the precise safe staging boundary:

```text
0x404340 <user_input>: "P15-FINAL;AAAA..."
0x4043a0: final-line tail, terminating NUL, then staged 'S' bytes
0x404ff0: staged 'S' bytes still present at the end of the data page
0x405000: allocator state still intact
0x405008: 0x0000000000000291
```

The `L=3300` and longer attempts cross the boundary into allocator/tcache state
and crash before a usable control-flow point.

### Verdict

Positive primitive only.

This improves the previous multi-line staging result: the safe non-stack staging
window is now bounded as data-page staging through `0x404fff`, while the next
page begins allocator-sensitive state. It still does not call `/backdoor`,
because no first-stage pivot or first-argument setup has been proven.

## Updated Recovery Rule

Do not repeat direct current-`rdi`, direct `rax`, saved-RBP, normal appended ROP,
or broad heap-overwrite assumptions.

The next technical block must choose one of:

- a first-stage sequence that consumes the preserved post-stream stack/local
  pointer and internally reaches a success-relevant call without requiring a
  second appended qword;
- a heap plan that preserves allocator invariants and turns the `3300+` boundary
  into a controlled write rather than allocator abort;
- TA/instructor clarification or honest partial-submission route.

