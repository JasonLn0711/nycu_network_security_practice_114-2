# Project II Scaffold Safety Boundary

This scaffold is for controlled coursework only. It demonstrates interfaces,
state, logs, and a mock grading loop. It is not an exploit and must not be used
outside the NYCU Network Security Project II Docker lab.

## Allowed Behavior

| Allowed | Boundary |
| --- | --- |
| Write placeholder `config.data` | Only under `/shared` or `PROJECT2_SHARED_DIR`. |
| Create `exploit_done` | Only after config write. |
| Read `blogic.copy` metadata | Do not modify it. |
| Read coredump filenames/metadata | Do not copy raw content into reports. |
| Write `triage_state.json` | Safe summaries only. |
| Run mock grader | Classroom-only; no `/backdoor` execution. |

## Forbidden Behavior

- Real exploit payloads.
- Shellcode.
- ROP chains.
- Instructions to execute `/backdoor`.
- Grader bypass.
- External network connections.
- Host file modification.
- Docker daemon tampering.
- Real-world target instructions.

## Safe Wording

Use:

- candidate config;
- controlled lab input;
- triage evidence;
- state update;
- mock grader;
- safe placeholder.

Avoid:

- real target;
- command server;
- stealth persistence;
- weaponized chain;
- real-world payload;
- fake success.

## Self-Check

- [ ] Does the code stay under the lab/shared paths?
- [ ] Does the mock grader avoid `/backdoor`?
- [ ] Do docs avoid exploit construction details?
- [ ] Do logs avoid secrets and raw evidence dumps?
- [ ] Does the TODO clearly mark where student lab-specific work belongs?

