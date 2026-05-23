# Phase II Safe-Linked Entry Feasibility - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in a disposable local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger ID: `P2-EXP-020` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Why This Block Exists

`P2-EXP-019` made the non-stack staging boundary more precise, but it also left
a tempting next idea:

```text
If L>=3293 crashes because count[6] is non-zero while entries[6] is NULL,
can we write a plausible safe-linked entries[6] pointer before malloc(106)?
```

This block is a critical review of that idea. It intentionally does **not** use
current-`rdi`, direct `rax`, appended ROP, preserved saved RBP, or the already
closed stack-local/BSS gadget families.

The bounded question is narrower:

> Can the forward `strcpy(user_input, value.c_str())` staging primitive build a
> valid enough tcache `entries[6]` state to cross beyond the `L=3292` count-gate
> and still reach final `log_message()`?

## Correction to the previous mental model

`P2-EXP-019` correctly found the decisive `L=3292` vs `L=3293` boundary, but the
simple phrasing "`L=3292` keeps `count[6]` zero" is too coarse when read from
the final coredump.

In the final `L=3292` core, after subsequent allocations/frees have already
run, the tcache state includes:

```text
0x4050c0: 0x000000000041b1a0  # entries[6] in the final core
0x41b190: 0x0000000000002d00 0x0000000000000080
0x41b1a0: 0x000000000000041b ...
```

So the important fact is not simply "count is zero forever." The important
fact is that `L=3292` avoids the **early** `tcache_get_n()` crash during the
next `malloc(106)` and eventually reaches the final overflow marker.

For `L=3293`, the crash occurs during that next allocation:

```text
rip = __GI___libc_malloc+369 / tcache_get_n
rdx = 0x405010        # tcache-per-thread base
r12 = 0x6             # tc_idx 6 for malloc(106)
rax = 0x0             # entries[6] loaded as NULL
rcx = 0x52            # count[6] after decrement from non-zero
```

That means the next useful hypothesis must make `entries[6]` valid **at the
moment of the first post-stage `malloc(106)`**, not merely in the later final
core.

## Hypothesis

A staged long `user_input=` line can write both:

```text
count[6]   at 0x40501c
entries[6] at 0x4050c0
```

so that the following `malloc(106)` can pop a safe-linked tcache entry and let
parsing continue to the final overflow marker.

A candidate entry must satisfy at least these allocator-side properties:

1. `entries[6]` is non-NULL and 16-byte aligned (`test al, 0xf` passes).
2. `entries[6]` points to readable/writable memory for the safe-link decode:

   ```text
   next = *(uint64_t *)entry ^ (entry >> 12)
   ```

3. The returned pointer later survives `std::string` use and destructor/free.
   In practice that means `entry - 0x10` must look like a real glibc chunk
   header, not just any writable address.

## Candidate design

The most tempting deterministic pointer from the `L=3292` final core is:

```text
entries[6] candidate = 0x000000000041b1a0
encoded bytes        = a0 b1 41 00 00 00 00 00
```

This is encodable through the current C-string path as a partial qword:

- write bytes `a0 b1 41` at `entries[6]` (`0x4050c0`);
- let the `strcpy()` terminator write the fourth byte as `0x00`;
- leave the high bytes zero.

The staged line therefore used:

```text
entries[6] offset from user_input = 0x4050c0 - 0x404340 = 3456
stage length = 3459  # terminator lands at entries[6]+3
count[6] bytes = 0x01 0x01  # non-zero without interior NUL
entries[6] low bytes = a0 b1 41
```

This deliberately tests whether the observed `0x41b1a0` is a reusable valid
tcache entry rather than a final-state artifact.

## Bounded Validation Contract

Run one disposable IC block with two candidates:

1. `baseline-3292`: re-confirm the known count-gated staging reaches final
   `log_message()` return.
2. `safe-entry6-41b1a0`: write `count[6]` and partial `entries[6] = 0x41b1a0`,
   then use the same short final overflow marker.

Stop after the first concrete allocator result. Do not broaden into a heap
spray or blind pointer sweep.

## Environment

```text
container: IC_PHASE2_P20
image: ic_image
mount: /tmp/project2_phase2_p20/lab/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
local evidence dir: /tmp/project2_phase2_p20/
```

The container was removed after the run. `/backdoor` was not invoked manually,
and no EC/host code created `/shared/success.txt`.

## Result

Falsified for this safe-linked entry candidate class.

### Baseline re-check

`baseline-3292` reproduced the known positive primitive:

```text
stage_len=3292
success=False
core=blogic-29.core
rip=0x40146f <log_message(char const*)+89>
entries[6] final-core value at 0x4050c0 = 0x41b1a0
```

The final core also showed why `0x41b1a0` looked attractive:

```text
0x41b190: 0x0000000000002d00 0x0000000000000080
0x41b1a0: 0x000000000000041b ...
```

At this final-state moment, it looks like a plausible small-bin/tcache-sized
chunk user pointer.

### Safe-entry candidate

`safe-entry6-41b1a0` did **not** reach the final overflow marker and did not
produce `/shared/success.txt`:

```text
stage_len=3459
success=False
signal=SIGABRT
abort reason=double free or corruption (out)
#7 _int_free_merge_chunk(..., p=0x41b190, size=6004234345560363776)
#8 __GI___libc_free(mem=0x41b1a0)
#9 parse_config()
```

Relevant memory in the abort core:

```text
0x41b190: 0x0153535353535353 0x5353535353535301
0x41b1a0: "safe-entry6-41b1a0;AAAA..."
```

Interpretation:

- The candidate successfully made the allocator return/use `0x41b1a0` for the
  next C++ string buffer.
- But at this point in the run, `0x41b1a0` is not a valid chunk with a valid
  header at `0x41b190`; it lies inside the large staged string region / corrupted
  heap payload created by the same long line.
- When the C++ string destructor frees that pointer, glibc correctly aborts on
  the bogus chunk header.

## Why this closes the naive safe-linked-entry path

A valid safe-linked `entries[6]` route has to solve two independent constraints:

1. **Pointer encoding under `strcpy()`**
   - Low heap/main-binary pointers can sometimes be partially written by using
     the terminating NUL as byte 3.
   - But any pointer whose earlier bytes contain NUL is impossible before the
     required `entries[6]` offset.

2. **Valid chunk header at `entry - 0x10`**
   - A `.bss` fake chunk such as `entry = 0x405020` would need a sane size field
     like `0x81` at `0x405018`.
   - That header lies **before** `entries[6]`. A single long `strcpy()` line that
     continues to `entries[6]` cannot place the required zero bytes in the size
     field; it must use non-NUL bytes until the final terminator.
   - A later shorter line cannot repair the header before the post-stage
     `malloc(106)`, because the allocator call happens before the parser reaches
     a later repair line.

The tested `0x41b1a0` pointer demonstrates the timing pitfall: an address that
is a plausible `entries[6]` value in the final `L=3292` core is not necessarily
a valid freeable chunk at the earlier post-stage allocation point.

## Decision

Do not continue with naive `entries[6] = 0x41b1a0` or `.bss` fake-chunk tcache
poisoning. This route can make the allocator use a staged pointer, but it dies
in C++ string destruction before `log_message()` and before any success-relevant
call path.

Remaining heap work would need a new written mechanism that identifies a real
free chunk pointer available **before** the post-stage `malloc(106)`, and whose
chunk header remains valid after the long `strcpy()` staging line. Without that,
non-stack staging remains a positive primitive only, not a full-credit path.
