# Phase II Current-RDI Argument Attempt - 2026-05-15

Scope: supplied Project II Phase II IC (`server_2`) in a fresh local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

Experiment ledger ID: `P2-EXP-014` in `docs/PHASE2_EXPERIMENT_LOG.md`.

## Direct Result

Project II is still **not full-credit complete**.

This pass intentionally moved away from the closed paths:

- no appended ROP chain after the saved return address;
- no preserved saved RBP assumption;
- no direct reuse of the post-logging `rax` value.

The bounded hypothesis was that `rdi` at `log_message()` return time might still
be a useful first argument. The candidate returned directly to `system@plt`
(`0x401250`) and let the current `rdi` stand as the command pointer.

## Environment

This pass used a fresh disposable local IC:

```text
container: IC_PHASE2_NEXT
image: ic_image
mount: /tmp/project2_phase2_next/lab/shared -> /shared
ASLR: 0
server_2 sha256: 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
libc sha256: d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
```

The IC loop was running under `/runserver.sh`. `/backdoor` was not invoked
manually, and the EC did not create `/shared/success.txt`.

## Pre-Probe Register Check

A marker crash at the `log_message()` epilogue showed the relevant register
state before choosing the candidate:

```text
rip = 0x40146f <log_message(char const*)+89>
rax = 0x404100              # copied std::cout object
rdi = 0x7ffff7d00710        # _IO_stdfile_1_lock
rsi = 0x0
rdx = 0x7ffff7faf310        # libstdc++ ostream vtable area
rcx = 0x7ffff7c175a4        # libc write() code
user_input = 0x404340
```

The pointed-to `rdi` bytes were zero:

```text
0x7ffff7d00710 <_IO_stdfile_1_lock>: ""
```

This made the hypothesis weak, but it was still a distinct first-argument setup
probe and did not depend on the previously closed `rax` route.

## Candidate

The source tree now preserves this bounded probe as:

```sh
PROJECT2_PHASE2_STRATEGY=current-rdi-system
```

with `PROJECT2_ENABLE_PHASE2_PROBE=1`.

The candidate writes a byte-exact `user_input=` line, pads to the observed
saved-return-address offset (`97` user-controlled bytes), and uses a non-PIE
partial return overwrite to `system@plt` (`0x401250`).

Validation command:

```sh
PROJECT2_SHARED_DIR=/tmp/project2_phase2_next/lab/shared \
  PROJECT2_ENABLE_PHASE2_PROBE=1 \
  PROJECT2_PHASE2_STRATEGY=current-rdi-system \
  python3 -m src.exploit_runner
```

## Observed Evidence

The IC consumed `/shared/exploit_done`.

Observed result:

```text
/shared/success.txt: absent
coredump: /shared/coredump/blogic-74.core
```

The coredump stopped inside libc `do_system()`:

```text
rip = 0x7ffff7b5343b <do_system+363>
line = 0x7ffff7d00710 <_IO_stdfile_1_lock> ""
```

The staged `/backdoor` text remained in `user_input`:

```text
0x404340 <user_input>: "/backdoor #..."
```

but `system()` did not receive that pointer. It received the empty libc lock
buffer from the current `rdi` register instead.

## Interpretation

Current-`rdi` reuse is not a full-credit route:

- `rdi` at the return point is not controlled by `user_input`;
- the candidate does not create `/shared/success.txt`;
- the crash is consistent with entering `system()` on an empty non-command
  pointer while the stack remains overflow-corrupted.

This closes the direct current-`rdi` first-argument setup. Future recovery needs
a different non-stack staging mechanism or a first-argument setup that makes a
controlled pointer reach the call target before the final C++ stream calls
clobber the argument registers.
