# Phase II Tcache Count-Gate Staging - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in a disposable local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger ID: `P2-EXP-019` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Why This Block Exists

The previous recovery blocks closed the direct register routes after the final
C++ stream clobber:

- direct current-`rdi` reaches `system()`, but the command pointer is the empty
  libc `_IO_stdfile_1_lock` buffer;
- post-stream stack/local pointers survive, but no single-stage gadget consumes
  them into `rdi` plus `system`/`execve`;
- `.bss`-indirect `rax + disp` dispatch has no qualifying exec-family tail;
- stack-local `mov/lea rdi, [rsp+disp]` has no viable success tail.

This block therefore switches to the other allowed direction: **more precise
non-stack staging**. The goal is not to assume that heap/tcache corruption is
usable. The goal is to identify the exact C++/glibc allocator gate that separates
safe staging from early allocator death, then decide whether there is a credible
next heap primitive.

## Hypothesis

The earlier `L>=3300` allocator crashes are not merely "heap corruption is
unstable". They should correspond to a specific glibc tcache field being
corrupted by the forward `strcpy()` from global `user_input`.

If the first long `user_input=` line is sized so that its terminating NUL lands
on the relevant tcache count field, then the IC may continue past the allocator
call and reach the final `log_message()` return point even after writing beyond
`0x405000`.

This would be a positive primitive only: it would extend the safe non-stack
staging window, but it would not by itself create `/shared/success.txt`.

## C++ / allocator model

`parse_config()` processes each line approximately as:

```text
getline(config_file, line)
pos = line.find('=')
key   = line.substr(0, pos)
value = line.substr(pos + 1)
if (key == "user_input") strcpy(user_input, value.c_str())
```

Important consequences:

1. Every `user_input=` line writes from the fixed destination `0x404340`.
2. `strcpy()` copies non-NUL bytes and then writes exactly one NUL terminator at
   `0x404340 + len(value)`.
3. The next `std::string::substr()` allocation happens before a later
   `user_input=` line can repair corrupted allocator state.
4. Therefore any staging beyond the allocator boundary must leave the next
   allocator request internally consistent immediately after that same line's
   `strcpy()`.

The live cores show the first glibc heap/tcache structure begins immediately
after the executable data page:

```text
user_input = 0x404340
0x405000   = start of adjacent allocator/tcache memory
0x405010   = tcache counts array / per-thread tcache user area
```

The relevant allocation after the staged line is a `std::string::substr()`
allocation of `106` bytes. In glibc 2.39 this uses tcache bin index `6`.
`tcache_get_n()` reads the count at:

```text
count[6] = *(uint16_t *)(0x405010 + 6*2) = *(uint16_t *)0x40501c
```

If this count is non-zero while the corresponding entry pointer is NULL or
invalid, glibc crashes before the final `log_message()` call.

## Bounded Validation Contract

Run one live IC block in a disposable container, without invoking `/backdoor`
manually and without creating `/shared/success.txt` from EC/host code.

Each candidate writes two `user_input=` lines:

```text
user_input=<stage value of exact length L>
user_input=<short final overflow marker that reaches log_message ret>
```

The final line is intentionally only a crash marker; it is not a success claim.
A successful primitive observation is "IC reaches `log_message()` ret" rather
than "allocator crashes in `tcache_get_n()`".

Tested stage lengths:

```text
3278, 3280, 3288, 3290, 3291, 3292, 3293, 3294, 3300
```

## Environment

```text
container: IC_PHASE2_P19
image: ic_image
mount: /tmp/project2_phase2_p19/lab/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
local evidence dir: /tmp/project2_phase2_p19/
```

The IC loop was started from the official `runserver.sh`. The experiment only
wrote `/shared/config.data` and `/shared/exploit_done`, then inspected official
IC coredumps and `/shared/success.txt` state.

## Result

Positive primitive only; no full-credit success.

Observed outcomes:

| Stage length `L` | Result | Core site | `/shared/success.txt` |
| ---: | --- | --- | --- |
| 3278 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3280 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3288 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3290 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3291 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3292 | IC consumed marker; reached final crash marker | `log_message` ret `0x40146f` | absent |
| 3293 | IC consumed marker; allocator crash before final log | `tcache_get_n` / `malloc(106)` | absent |
| 3294 | IC consumed marker; allocator crash before final log | `tcache_get_n` / `malloc(106)` | absent |
| 3300 | IC consumed marker; allocator crash before final log | `tcache_get_n` / `malloc(106)` | absent |

The decisive boundary is `L=3292` vs `L=3293`.

## Core evidence

### `L=3292` reaches the final return point

`/tmp/project2_phase2_p19/P19-L3292-blogic-107.core`:

```text
rip = 0x40146f <log_message(char const*)+89>
rsp = 0x7fffffffec48
rbp = 0x4141414141414141
rax = 0x404100
rdi = 0x7ffff7d00710
```

Allocator/tcache bytes at the boundary:

```text
0x405000: 0x5353535353535353 0x5353535353535353
0x405010: 0x5353535353535353 0x0000000153535353
```

As halfwords:

```text
0x405010: 5353 5353 5353 5353 5353 5353 0001 0000
```

`count[6]` is the halfword at `0x40501c`; with `L=3292`, the `strcpy()`
terminating NUL lands at `0x40501c`. The next byte remains zero, so the value
is effectively zero / non-tcache-taking for the following `malloc(106)` path,
and the process survives to the final `log_message()` overflow.

### `L=3293` crashes in `tcache_get_n`

`/tmp/project2_phase2_p19/P19-L3293-blogic-119.core`:

```text
rip = 0x7ffff7ba87e1 <__GI___libc_malloc+369>
#0 tcache_get_n
#1 tcache_get
#2 __GI___libc_malloc(bytes=106)
#3 operator new(unsigned long)
#4 std::__cxx11::basic_string<...>::_M_construct(...)
#5 std::__cxx11::basic_string<...>::substr(...)
#6 parse_config()
```

Registers at the crash:

```text
rdx = 0x405010        # tcache struct / counts base
r12 = 0x6             # tc_idx 6
rax = 0x0             # entries[6] is NULL
rcx = 0x52            # count[6] is non-zero
```

Relevant memory:

```text
0x405010: 5353 5353 5353 5353 5353 5353 0053 0000
```

With `L=3293`, `count[6]` becomes non-zero (`0x0053`) while the tcache entry is
NULL. glibc follows the tcache fast path and crashes when it tries to decode the
NULL entry.

## Interpretation

This is a more precise non-stack staging result than the earlier broad
`L=3264` boundary:

- The largest allocator-tolerated first-line stage length observed in this
  block is `L=3292`.
- `L=3292` deliberately corrupts the adjacent allocator/tcache region but uses
  the `strcpy()` terminator as a **count-gate NUL** at `count[6]`.
- `L>=3293` is not merely "unstable"; it corrupts `count[6]` into a non-zero
  value before a required C++ `std::string` allocation, so the process dies in
  `tcache_get_n()` before final `log_message()`.
- A later `user_input=` line cannot repair this, because the allocator call that
  crashes occurs before the parser reaches any later line.

This also explains why a naive multi-line NUL-stitch plan cannot extend past
`3292`: any line long enough to write beyond `0x40501c` must first write a
non-NUL byte into `count[6]`, and `strcpy()` cannot embed an interior NUL to keep
that count zero.

## Decision

No live success candidate exists for this heap/tcache count-gate hypothesis.
The primitive is useful evidence, not a full exploit route.

The non-stack staging boundary is now:

```text
safe data-page staging:                  up to L=3264
allocator-tolerated count-gated staging: up to L=3292
allocator crash before final log:        L>=3293
```

Do not repeat broad `L>=3300` heap overwrites. Future heap work would need a
specific plan that both:

1. keeps `count[6]` zero or supplies a valid safe-linked `entries[6]` pointer
   before `malloc(106)`; and
2. uses the staged state to create a real first-argument setup or call target.

Without both properties, the correct next technical conclusion is still:

```text
Protocol-complete partial package; official IC-side success evidence pending.
```
