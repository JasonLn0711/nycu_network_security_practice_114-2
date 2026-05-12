# Project II SPEC - Autonomous APT Agent Phase II Medium

## Purpose

This document defines the best local specification for Project II - Autonomous
APT Agent, Phase II Medium. It is intended for three audiences:

- students, to understand the expected deliverables;
- graders, to judge behavior from evidence instead of intuition;
- AI or automation tools, to check the assignment without inventing missing
  facts.

This specification is derived from `project-brief.pdf`, `lab.zip`, and the
local 100-point rubric in `grading-rubric-phase-ii.md`. The instructor's
official grading script and announcements remain authoritative if they differ
from this local specification.

This is a controlled course-lab specification. It does not define or authorize
use against real systems, external networks, host machines, or third-party
targets.

Student-facing companion documents are in `docs/`:

| Path | Role |
| --- | --- |
| `docs/SPEC.md` | Student-facing assignment specification and testable requirements |
| `docs/SDD.md` | Student-facing software design document |
| `docs/STUDENT_CHECKLIST.md` | Pre-submission checklist |
| `docs/SAFETY_BOUNDARY.md` | Course-lab safety boundary |

## Project Identity

| Field | Value |
| --- | --- |
| Project | Project II - Autonomous APT Agent |
| Phase | II / Medium |
| Course | Network Security Practice - Attack and Defense |
| Target OS from brief | Ubuntu Linux LTS `24.04.3` x86_64 |
| Student-owned side | External container, abbreviated `EC` |
| Provided target side | Internal container, abbreviated `IC` |
| Required EC entrypoints | `/exploit`, `/triage` |
| Shared volume | `/shared` |
| Time bound | `30` minutes |
| Round bound | `60` rounds |

## Grading Goal

The goal is not to reward a dangerous general-purpose tool. The goal is to
evaluate whether a student can build a closed-lab autonomous workflow that:

1. runs inside the supplied Docker lab;
2. understands the expected EC/IC shared-volume protocol;
3. produces a modified `/shared/config.data`;
4. signals the IC through `/shared/exploit_done`;
5. observes crash feedback under `/shared/coredump/*`;
6. updates next-round behavior through `/triage`;
7. reaches the Phase II success condition when possible;
8. remains reproducible, auditable, and bounded to the course environment.

## System Boundary

### In Scope

Only these resources are in scope for Project II grading:

```text
EC container
IC container business-logic flow
/exploit
/triage
/shared/config.data
/shared/blogic.copy
/shared/exploit_done
/shared/coredump/*
grader.sh and the course-provided grading loop
```

### Out Of Scope

The following behavior is not part of the project and must not receive credit:

```text
attacking the host machine
attacking Docker daemon or runtime
scanning external networks
connecting to an external command server
downloading runtime payloads from the internet
modifying the grader
modifying the IC image outside the expected lab flow
forging the success signal instead of using the specified workflow
reading other students' data
causing resource exhaustion
using the artifact outside the course lab
```

## Student Deliverables

The recommended submitted source package should be organized as:

```text
project2_submission/
|-- Dockerfile
|-- README.md
|-- exploit
|-- triage
|-- src/
|   |-- exploit_main.*
|   |-- triage_main.*
|   `-- utils.*
|-- logs/
|   `-- sample_run.log
`-- report/
    `-- project2_report.md
```

The actual running EC container must expose:

```text
/exploit
/triage
```

Both entrypoints must:

- execute directly;
- require no interactive input;
- run without external network access during grading;
- avoid student-local absolute path dependencies;
- stay within the course lab boundary;
- produce bounded logs and clear exit status.

If the instructor requires a different packaging format later, keep these
runtime invariants and adapt only the outer package shape.

## Functional Requirements

### FR-1: `/exploit` Direct Execution

`/exploit` must run directly in the EC:

```sh
/exploit
```

Required behavior:

1. Check that `/shared/config.data` exists.
2. Check that `/shared/blogic.copy` exists when the lab provides it.
3. Load current round state if state exists.
4. Produce the next `config.data` content for the current round.
5. Write `/shared/config.data`.
6. Confirm the write is complete.
7. Create `/shared/exploit_done`.
8. Exit cleanly for this round.

Acceptance criteria:

| Criterion | Required |
| --- | --- |
| `/exploit` exists | Yes |
| `/exploit` is executable | Yes |
| No interactive input | Yes |
| Reads or checks `/shared/config.data` | Yes |
| Reads or checks `/shared/blogic.copy` when available | Yes |
| Modifies `/shared/config.data` content | Yes |
| Creates `/shared/exploit_done` | Yes |
| Creates signal after config write completes | Yes |
| Terminates per invocation | Yes |
| Exit code is meaningful | Yes |

### FR-2: `/triage` Direct Execution

`/triage` must run directly in the EC:

```sh
/triage
```

Required behavior:

1. Check `/shared/coredump/*`.
2. If no coredump exists, produce initial or default triage state.
3. If coredumps exist, choose the newest or most relevant coredump by a clear
   rule.
4. Analyze crash feedback at the metadata/state level needed for the next
   round.
5. Optionally inspect `/shared/blogic.copy` metadata.
6. Update a machine-readable state file.
7. Exit cleanly.

Acceptance criteria:

| Criterion | Required |
| --- | --- |
| `/triage` exists | Yes |
| `/triage` is executable | Yes |
| No interactive input | Yes |
| Handles no-coredump case | Yes |
| Reads `/shared/coredump/*` when present | Yes |
| Produces next-round state | Yes |
| Exit code is meaningful | Yes |

### FR-3: Shared-Volume Protocol

The EC must follow the course grading sequence:

```mermaid
flowchart TD
    A[Grader starts round] --> B[EC runs /exploit]
    B --> C[/exploit writes /shared/config.data]
    C --> D[/exploit creates /shared/exploit_done]
    D --> E[IC detects exploit_done]
    E --> F[IC runs blogic with config.data]
    F --> G{Backdoor executed?}
    G -- Yes --> H[Record success time and terminate]
    G -- No --> I[IC writes coredump under /shared/coredump]
    I --> J[EC runs /triage]
    J --> K[/triage updates triage state]
    K --> A
```

Protocol requirements:

- `/exploit` must not delete or move `/shared/config.data`.
- `/exploit` must not signal before `config.data` is fully written.
- `/exploit` must use exactly `/shared/exploit_done`.
- `/triage` must not require manual movement of coredumps.
- Both tools must tolerate a fresh `/shared` volume.

### FR-4: Triage State Contract

The recommended state file is:

```text
/shared/triage_state.json
```

The state file should be machine-readable JSON. It must avoid secrets and avoid
recording unrelated host data.

Minimal schema:

```json
{
  "schema_version": "1.0",
  "project": "project2",
  "phase": "II",
  "round": 0,
  "last_exploit": {
    "config_hash": "",
    "strategy_id": "",
    "timestamp": ""
  },
  "last_triage": {
    "coredump_found": false,
    "coredump_path": "",
    "analysis_status": "none",
    "summary": ""
  },
  "next_action": {
    "strategy_id": "initial",
    "parameters": {},
    "confidence": 0.0
  },
  "safety": {
    "lab_only": true,
    "external_network": false
  }
}
```

This file is not required to expose dangerous implementation details. It exists
so the workflow can be audited and so `/exploit` can consume `/triage` output.

### FR-5: Round Logging

Each round should produce bounded, append-only evidence. Recommended file:

```text
/shared/round_log.jsonl
```

Example events:

```json
{"round":1,"component":"exploit","event":"config_written","success":true,"timestamp":"..."}
{"round":1,"component":"exploit","event":"exploit_done_created","success":true,"timestamp":"..."}
{"round":1,"component":"triage","event":"coredump_scanned","success":true,"timestamp":"..."}
{"round":1,"component":"triage","event":"state_written","success":true,"timestamp":"..."}
```

Logs must be useful for grading but bounded in size.

### FR-6: Phase II Medium Assumption Handling

The submitted artifact must target Phase II Medium:

```text
stack-based buffer without boundary check
non-PIE executable
ASLR disabled
```

The README/report must explicitly state this target. The implementation must
not depend on Phase I-only executable-stack assumptions or Phase III-only
ASLR-enabled assumptions.

### FR-7: Report And Audit Evidence

The submission should include a README or report with:

1. build/run instructions;
2. `/exploit` responsibility;
3. `/triage` responsibility;
4. Phase II Medium assumptions;
5. sample run log with round/time/result;
6. known limitations and failure modes;
7. safety statement: course Docker lab only.

### FR-8: Grading Output Contract

The recommended grading report format is:

```json
{
  "student_id": "string",
  "project": "Project II",
  "phase": "Medium",
  "total_score": 0,
  "score_breakdown": {
    "A_submission_environment": 0,
    "B_exploit_protocol": 0,
    "C_success_performance": 0,
    "D_triage": 0,
    "E_automation_stability": 0,
    "F_code_quality": 0,
    "G_report_auditability": 0,
    "H_safety_integrity": 0
  },
  "success": false,
  "success_time_sec": null,
  "success_round": null,
  "caps_applied": [],
  "critical_errors": [],
  "evidence": {
    "exploit_exists": false,
    "triage_exists": false,
    "config_modified": false,
    "exploit_done_created": false,
    "coredump_seen": false,
    "triage_state_updated": false
  },
  "notes": []
}
```

## Non-Functional Requirements

### NFR-1: Reproducibility

The submission must be runnable from:

```text
clean EC container
clean /shared volume
same Project II grader
no internet
same submitted files
```

### NFR-2: Deterministic Evidence

Every round should make it possible to answer:

```text
Which round was this?
Did /exploit exit?
Did config.data change?
Was exploit_done created?
Did IC produce a coredump?
Did /triage exit?
Did triage state change?
```

### NFR-3: Safety

Forbidden behavior:

```text
external socket callbacks
external scanning
runtime payload download
host escape
privilege escalation outside the EC/IC lab
grader tampering
resource exhaustion
unbounded output
```

### NFR-4: Timeout Discipline

Recommended command bounds:

| Command | Maximum runtime |
| --- | ---: |
| `/exploit` single invocation | 30 seconds |
| `/triage` single invocation | 30 seconds |
| Full grading loop | 30 minutes |
| Full grading rounds | 60 rounds |

### NFR-5: Dependency Discipline

All dependencies must be declared in the Dockerfile or README. The grader should
not need to discover missing packages manually. Runtime network installation is
not acceptable unless the instructor explicitly permits it.

### NFR-6: Observability Without Over-Disclosure

Logs and reports must support grading and debugging. They do not need to reveal
dangerous implementation details such as payload internals. They must not store
secrets, unrelated host data, or external target information.

## 100-Point Scoring Interface

The detailed scoring standard is `grading-rubric-phase-ii.md`. The top-level
weighting is:

| Category | Points |
| --- | ---: |
| A. Submission and environment | 12 |
| B. Exploit shared-volume protocol | 18 |
| C. Project II success and performance | 25 |
| D. Triage and iterative learning | 15 |
| E. Automation and stability | 10 |
| F. Code quality and maintainability | 8 |
| G. Report and auditability | 7 |
| H. Safety and integrity | 5 |
| Total | 100 |

This SPEC defines what the system must do. The rubric defines exactly how
points, caps, and direct-zero rules are applied.

## Acceptance Test Cases

### TC-1: Basic Structure Test

Input: submitted EC image or build context.

Expected:

```text
/exploit exists
/triage exists
both are executable
EC can start
```

### TC-2: No Manual Input Test

Run:

```sh
/exploit
/triage
```

Expected:

```text
both terminate
neither reads from stdin interactively
exit status is meaningful
```

### TC-3: Config Modification Test

Given:

```text
/shared/config.data hash = H1
```

Run:

```sh
/exploit
```

Expected:

```text
/shared/config.data hash = H2
H1 != H2
/shared/exploit_done exists
```

### TC-4: Missing Coredump Test

Given:

```text
/shared/coredump/ is empty
```

Run:

```sh
/triage
```

Expected:

```text
no crash
bounded runtime
state file is created or log explains no coredump
```

### TC-5: Full Phase II Run

Given:

```text
Phase II IC and clean /shared
```

Run:

```text
course grading loop
```

Expected:

```text
success within 30 minutes / 60 rounds, or partial score from observable evidence
```

### TC-6: Repeatability Test

Run the same submission three times from clean state.

Expected:

```text
stable behavior
no dependency on previous shared-volume residue
no dependency on stale EC filesystem state
```

### TC-7: Network-Off Test

Run grading with external network disabled.

Expected:

```text
runtime does not require external connectivity
no outbound attack or callback behavior appears
```

## Traceability Matrix

| Requirement | Rubric area | Acceptance tests |
| --- | --- | --- |
| EC starts and paths exist | A | TC-1 |
| `/exploit` modifies config and signals | B | TC-2, TC-3, TC-5 |
| Phase II success and speed | C | TC-5, TC-6 |
| `/triage` handles coredumps and state | D | TC-4, TC-5 |
| No manual intervention | E | TC-2, TC-5 |
| Clear code/dependency discipline | F | TC-1, review |
| Report/audit trail present | G | review |
| Lab-only safety boundary | H | TC-7, review |

## Final Design Principle

The submitted artifact is not just an exploit. It is a bounded, observable,
repeatable, and auditable autonomous exploitation workflow inside a course lab.
