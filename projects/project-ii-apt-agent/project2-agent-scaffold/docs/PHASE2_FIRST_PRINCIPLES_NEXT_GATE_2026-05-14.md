# Phase II First-Principles Next Gate

Date: 2026-05-14
Scope: Project II / Phase II Medium continuation after the verified non-success
validation pass.

## First Principle

The assignment is not asking for more interesting candidate strings. It is
asking for a valid EC/IC grading-loop outcome:

1. EC `/exploit` writes `/shared/config.data`.
2. EC `/exploit` creates `/shared/exploit_done`.
3. IC `blogic` consumes the input.
4. IC-side control flow legitimately reaches `/backdoor`.
5. `/backdoor` creates `/shared/success.txt`.

Everything else is support evidence. A candidate is useful only if it increases
confidence in one of those five steps without faking the success artifact.

## Current Proven Boundary

The useful facts are now narrow:

- the EC protocol and scaffold are implemented;
- the overflow is reachable;
- saved control data can be corrupted;
- direct ret-to-`maintenance_task+5` was not enough because the first argument
  was not controlled at return time;
- direct stack execution is blocked by NX;
- the broad one-shot text sweep did not find a working target;
- official IC-side `/shared/success.txt` has not appeared.

Therefore the next scarce proof is not "can we overwrite RIP?" The next scarce
proof is:

> Can the post-`log_message()` state be turned into controlled first-argument
> state or a reliable pivot under the C-string constraints?

## Next Block Contract

Before running another candidate, choose exactly one bounded track:

| Track | Question | Stop condition |
| --- | --- | --- |
| Argument-control | Is there a return target or short sequence that makes the first argument point at controlled data after the final C++ stream call? | One verified register-state result, success or failure. |
| Pivot | Is there a reliable pivot to already-controlled bytes without depending on a normal NUL-bearing appended ROP chain? | One verified pivot-state result, success or failure. |
| Instructor clarification | Is the intended Phase II route or binary assumption different from the local reading? | One TA/instructor answer or one documented no-response checkpoint. |

Do not spend the next block on another broad `.text` sweep, direct stack
shellcode, or the same direct ret-to-maintenance attempt unless new evidence
changes the premise.

## Evidence To Record

For the chosen block, record:

- exact environment state before the run;
- candidate class, not just the raw bytes;
- exact command;
- whether IC consumed `/shared/exploit_done`;
- whether `/shared/success.txt` appeared;
- coredump path or explicit no-coredump observation;
- the register or stack fact that answers the track question;
- decision: continue same track, switch track, or ask instructor.

## Planning Boundary

Planning should track this as a blocked proof-artifact lane, not as a hidden
success. The planning repo should hold only status, next gate, capacity impact,
and open questions. Course-repo technical evidence remains here and in
`../../../../HANDOFF_PHASE2.md`.
