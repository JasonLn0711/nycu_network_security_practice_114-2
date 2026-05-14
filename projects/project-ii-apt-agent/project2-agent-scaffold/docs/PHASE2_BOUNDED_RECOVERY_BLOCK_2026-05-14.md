# Phase II Bounded Recovery Block - 2026-05-14

Scope: supplied Project II Phase II IC (`server_2`) in a fresh local Docker
container, using the official `/blogic` and `/backdoor` files from `lab.zip`.

## Direct Result

Project II is still **not full-credit complete**.

This block followed the handoff rule: choose one falsifiable technical check,
run it inside the controlled course lab, and stop after the result.

The result:

- no `/shared/success.txt` was created;
- `/shared/exploit_done` was consumed by the IC;
- no coredump appeared for this candidate;
- the `/blogic` process remained running under `/runserver.sh`;
- `/backdoor` was not invoked manually;
- the EC did not create `/shared/success.txt`.

## Bounded Hypothesis

Hypothesis:

```text
If execution can be redirected to the existing user-input setup point in
run_server(), then the process may re-enter the logging path with controlled
data and either reach the success path or produce a new observable artifact.
```

Why this was worth one bounded check:

- it avoids relying on preserved saved RBP;
- it avoids an appended ROP chain after saved RIP;
- it is a single-target check, not a broad sweep;
- it has a clean success signal: official IC-side `/shared/success.txt`.

Falsification criteria:

- IC consumes `/shared/exploit_done`;
- `/shared/success.txt` does not appear;
- no new control artifact appears.

## Environment

Fresh extraction:

```text
/tmp/project2_bounded_recovery/lab
```

Container:

```text
container: IC_PHASE2_BOUND
image: ic_image_phase2_bound
mount: /tmp/project2_bounded_recovery/lab/shared -> /shared
ASLR: 0
processes: /bin/bash /runserver.sh and /blogic
success artifact before probe: absent
```

Binary hash:

```text
server_2 sha256 = 155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

## Pre-Check

The live IC state before the candidate:

```text
/runserver.sh running
/blogic running
/proc/sys/kernel/randomize_va_space = 0
/shared/success.txt absent
/shared/coredump/ empty
```

Static re-check:

- the main binary still has no useful direct `pop rdi; ret` path;
- the success-relevant single-target paths remain constrained by stale argument
  state or corrupted saved frame state;
- the selected target was the existing user-input setup point already visible
  in `run_server()`.

## Candidate Result

Observed after the candidate:

```text
candidate=run-server-user-input-setup-boundary
success_exists=no
exploit_done=no
coredumps=none
/blogic still running
```

Interpretation:

- the IC did consume the exploit marker;
- the candidate did not cause official IC-side `/backdoor` execution;
- absence of a coredump means this target returned into a stable no-success path
  rather than creating a new crash artifact;
- this closes the simple "re-enter user-input setup" idea as a direct
  full-credit route.

## What This Does Not Prove

This does not prove that all pivot or libc/libstdc++ paths are impossible.

It only proves that this single bounded user-input setup boundary check did not
produce the official success artifact.

## Updated Boundary

Do not repeat these without a new mechanism:

- direct ret-to-maintenance;
- broad `.text` sweep;
- direct stack execution;
- saved-RBP maintenance-body entry;
- caller-stack staging with fixed original qwords;
- direct heap/global-state adjacency;
- direct re-entry to the user-input setup point as a success route.

## Next Technical Gate

Only continue technical recovery if a new written hypothesis identifies a
different mechanism that:

1. avoids the C-string/NUL-byte limitation;
2. does not need preserved saved RBP;
3. does not need an appended post-RIP chain;
4. has one observable success or failure signal;
5. remains inside the supplied course lab.

Until then, the correct submission posture remains:

```text
Protocol-complete partial package; official IC-side success evidence pending.
```
