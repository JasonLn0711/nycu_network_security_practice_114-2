# Project II Safety Boundary

This project is for controlled coursework only. The assignment environment is a
closed Docker lab with a student-submitted external container (`EC`), a
course-provided internal container (`IC`), and a shared volume at `/shared`.

The documentation and implementation must stay focused on software interfaces,
state management, logging, reproducibility, and safe educational constraints.
Do not include payload code, shellcode, ROP chains, real-world attack
instructions, or instructions for attacking systems outside the course lab.

## Allowed Lab-Only Behavior

Allowed behavior is limited to the expected Project II workflow:

| Allowed behavior | Boundary |
| --- | --- |
| Run `/exploit` inside EC | Must be noninteractive and bounded. |
| Run `/triage` inside EC | Must be noninteractive and bounded. |
| Read `/shared/config.data` | Only for the controlled lab workflow. |
| Write `/shared/config.data` | Only as the candidate lab config for the current round. |
| Read `/shared/blogic.copy` | Safe metadata and lab analysis only; do not modify it. |
| Create `/shared/exploit_done` | Only after `config.data` write completion. |
| Read `/shared/coredump/*` | Only for safe high-level triage evidence. |
| Write `/shared/triage_state.json` | Machine-readable state for the next round. |
| Write `/shared/round_log.jsonl` | Bounded audit logs with no secrets or weaponized details. |
| Document Phase II assumptions | Keep at high-level assignment terms. |

## Forbidden Behavior

The following behavior is outside the assignment and must not be implemented,
documented as an instruction, or rewarded:

```text
attacking the host machine
attacking Docker daemon or Docker socket
modifying the grader
modifying the IC image outside the expected lab flow
forging success signals
connecting to external servers
calling external APIs during grading
downloading runtime payloads
scanning networks
reading unrelated host files
reading other students' data
writing outside lab paths
creating unbounded logs or files
spawning unbounded processes
including shellcode, ROP chains, or payload recipes in docs
providing real-world attack instructions
```

## Safe Wording Examples

Use wording that describes interfaces and evidence without operational attack
details:

| Safe wording | Why it is safe |
| --- | --- |
| `candidate config` | Describes lab input without payload details. |
| `controlled lab input` | Limits scope to the course environment. |
| `triage evidence` | Describes feedback without exploit construction. |
| `state update` | Describes workflow evolution safely. |
| `round-based feedback` | Describes the grading loop. |
| `safe high-level summary` | Avoids weaponized details. |
| `Phase II assumptions` | Uses assignment-level terms. |
| `IC/EC Docker lab` | Keeps scope local and controlled. |

## Unsafe Wording Examples

Avoid wording that implies real-world misuse or operational offensive detail:

| Unsafe wording | Why to avoid it |
| --- | --- |
| `real target` | Suggests use outside the course lab. |
| `C2` | Implies external command infrastructure. |
| `stealth persistence` | Suggests real-world intrusion behavior. |
| `weaponized chain` | Implies operational exploit construction. |
| `real-world payload` | Goes beyond assignment documentation. |
| `external victim` | Violates lab-only boundary. |
| `bypass the grader` | Cheating and not part of the workflow. |
| `fake success` | Violates academic integrity. |

## Student Self-Check

Before submission, answer these questions:

- [ ] Does every runtime action stay inside EC, IC, or `/shared`?
- [ ] Does the implementation avoid external network calls during grading?
- [ ] Does the implementation avoid modifying host files?
- [ ] Does the implementation avoid Docker daemon access?
- [ ] Does the implementation avoid modifying the grader?
- [ ] Does the implementation avoid modifying IC artifacts outside the expected lab flow?
- [ ] Does `/exploit` signal only through `/shared/exploit_done`?
- [ ] Does `/triage` use coredump evidence only for safe state updates?
- [ ] Do logs avoid secrets and raw unrelated data?
- [ ] Do docs avoid shellcode, ROP chains, payload recipes, and real-world attack steps?
- [ ] Does the README clearly say this is course Docker lab only?

If any answer is no, fix the issue before submission.

## Required Safety Statement

Every README or report should include a statement equivalent to:

```text
This Project II artifact is intended only for the NYCU Network Security
Practice controlled Docker lab. It should not be used against real systems,
external networks, host machines, or third-party targets. The implementation is
limited to the EC/IC lab workflow and the shared volume paths required by the
assignment.
```

## Handling Uncertainty

If the official grading script or TA instruction is unclear:

- keep behavior bounded to the documented lab paths;
- document assumptions in the README;
- prefer a safe failure over an unsafe workaround;
- ask the instructor or TA instead of adding grader-bypass behavior;
- do not add external network dependencies to compensate for missing local
  information.

