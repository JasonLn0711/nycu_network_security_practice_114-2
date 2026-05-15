# Phase II Backward Pivot Feasibility - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) and the pinned Ubuntu 24.04
libc from an isolated local Docker reproduction of `lab.zip`.

Experiment ledger ID: `P2-EXP-013` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Hypothesis

The current C-string constraint prevents appending a normal ROP chain after the
partial saved-RIP overwrite. However, the controlled `log_message()` stack bytes
exist before the saved RIP slot. If a first-stage gadget can move `rsp`
backwards from the fixed post-return position into that controlled local buffer,
then the pre-RIP bytes could become the next-stage control surface.

The useful candidate family is deliberately narrow:

```text
sub rsp, imm; ret
add rsp, negative-imm; ret
lea rsp, [rsp-negative-imm]; ret
xchg rsp, reg; ret
mov rsp, reg; ret
```

A useful target must also be reachable through the current C-string copy path:
its first return address must be encodable without an embedded NUL before the
overwrite completes.

## Falsifiable Prediction

This hypothesis is supported only if the main binary or pinned libc contains at
least one reachable first-stage pivot from the family above.

It is falsified if the fresh IC binary set has no such gadget. In that case, no
live EC candidate should be run for this hypothesis because there is no concrete
first-stage address to validate.

## Bounded Validation Contract

Run one static feasibility block against the fresh Phase II IC artifacts:

1. Rebuild a fresh local IC from `lab.zip`.
2. Confirm the live libc mapping and copy that exact libc.
3. Search only the narrow pivot family above in `server_2` and the copied libc.
4. Stop after the gadget-family result.

Do not broaden this into a general gadget search or another partial-return
sweep.

## Environment

This pass used a fresh disposable local Docker reproduction:

```text
container: IC_PHASE2_PIVOT_STATIC
image: ic_image_pivot_static
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
libc sha256: d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
libc executable mapping: 0x7ffff7b23000-0x7ffff7cab000
```

The disposable container was removed after the static validation block.

## Result

Falsified for this gadget family.

The pinned libc search found:

```text
sub rsp, imm8; ret: 0
sub rsp, imm32; ret: 0
lea rsp,[rsp-imm8]; ret: 0
add rsp, neg-imm8; ret: 0
xchg rsp, rax; ret: 0
xchg rsp, rdi; ret: 0
mov rsp, rax; ret: 0
mov rsp, rdi; ret: 0
```

The main binary had already been checked for the same simple pivot family; it
has `leave; ret` and `pop rbp; ret` style sequences, but those depend on saved
RBP or untouched caller-stack qwords that prior attempts have already closed.

## Interpretation

The simple backward-stack-pivot route is not available in the fresh Phase II
binary set. This matters because it removes a plausible way to turn pre-saved-RIP
controlled bytes into a normal second-stage ROP surface under the C-string
constraint.

This does not prove that every pivot is impossible. It closes only the narrow
first-stage family tested here. Future recovery work needs a different concrete
mechanism, such as a non-stack staging primitive or an instruction sequence that
sets the first argument without relying on appended ROP bytes, preserved saved
RBP, direct `rax` reuse, or this backward-pivot family.
