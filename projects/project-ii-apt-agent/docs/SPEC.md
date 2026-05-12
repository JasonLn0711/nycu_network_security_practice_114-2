# Project II SPEC - Autonomous Agent Workflow for Controlled Lab Evaluation

## 1. Purpose

Project II is a controlled Docker lab assignment. The student designs an
autonomous workflow inside the submitted external container, abbreviated `EC`.
The goal is not to submit a single one-shot script. The goal is to submit a
reproducible round-based workflow:

- `/exploit` acts in each round.
- The internal container, abbreviated `IC`, runs `blogic` after
  `/shared/exploit_done` appears.
- If the round fails, coredump evidence appears under `/shared/coredump/*`.
- `/triage` reviews available evidence and updates state for the next round.
- The next `/exploit` invocation uses that state to choose the next candidate
  configuration.

This project is lab-only. All behavior must stay inside the course Docker
environment. This specification does not authorize real-world offensive use,
external network activity, host modification, or attack activity outside the
provided assignment setup.

The documentation in this folder is intended to help students build a clean,
auditable, reproducible workflow without including exploit payload code,
shellcode, ROP chains, or step-by-step attack instructions.

## 2. Scope

| Area | In scope | Out of scope |
| --- | --- | --- |
| Entry points | `/exploit`, `/triage` | Any hidden or undocumented manual entry point |
| Shared files | `/shared/config.data`, `/shared/blogic.copy`, `/shared/exploit_done`, `/shared/coredump/*` | Files outside the course lab paths |
| State | `triage_state.json`, local round state | Secrets, external host data, unrelated system data |
| Logs | local logs, `/shared/project2_agent.log`, `/shared/round_log.jsonl` | Massive logs, raw unrelated data, sensitive data |
| Container | Docker container compatibility for EC | Host machine modification or Docker daemon interference |
| Grading flow | Course-provided EC/IC interaction | Grader modification or grading-logic bypass |
| Safety | Lab-only, bounded behavior | External servers, external scanning, fake success signals, destructive behavior |

Explicitly forbidden behavior:

```text
attacking the host machine
attacking network services
connecting to external servers
modifying the grader
modifying the IC image outside the expected lab flow
bypassing grading logic
creating fake success signals
deleting or corrupting lab artifacts
causing resource exhaustion
```

## 3. Assignment Environment

| Term | Meaning |
| --- | --- |
| `EC` | External container prepared and submitted by the student. |
| `IC` | Internal container supplied by the lab; it runs the business logic program. |
| `/shared` | Shared volume mounted by both EC and IC. |
| `blogic` | Business logic program running in IC. |
| `/backdoor` | Preinstalled program in IC; successful execution is detected by the grader. |
| `/exploit` | EC entry point that writes a candidate `/shared/config.data` and creates `/shared/exploit_done`. |
| `/triage` | EC entry point that reviews feedback and updates next-round state. |

```mermaid
flowchart LR
    subgraph EC[EC - student submitted container]
        X[/exploit/]
        T[/triage/]
        LS[local state and logs]
    end

    subgraph SHARED[/shared]
        C[config.data]
        B[blogic.copy]
        D[exploit_done]
        CD[coredump/*]
        ST[triage_state.json]
    end

    subgraph IC[IC - course lab container]
        BL[blogic]
        BD[/backdoor]
    end

    ST --> X
    B --> X
    X --> C
    X --> D
    C --> BL
    D --> BL
    BL --> BD
    BL --> CD
    CD --> T
    T --> ST
    T --> LS
    X --> LS
```

## 4. Required Deliverables

### Container-Level Deliverables

| Path | Purpose | Required | Acceptance criteria |
| --- | --- | --- | --- |
| `/exploit` | Per-round action entry point. Writes candidate config and signals completion. | Must have | `test -f /exploit` and `test -x /exploit` pass; runs without interactive input. |
| `/triage` | Per-round feedback entry point. Reads evidence and updates state. | Must have | `test -f /triage` and `test -x /triage` pass; runs without interactive input. |

### Repository-Level Recommended Deliverables

| Path | Purpose | Required | Acceptance criteria |
| --- | --- | --- | --- |
| `Dockerfile` | Defines the EC runtime environment. | Should have unless another official format is required | Build instructions are reproducible; dependencies are declared. |
| `README.md` | Student-facing build/run summary. | Should have | Explains build, run, entry points, assumptions, and safety boundary. |
| `src/` | Source code for the EC tools. | Should have for maintainability | Source is organized by responsibility; no hidden manual steps. |
| `docs/SPEC.md` | Assignment and interface specification. | Must have in this repo | Requirements are testable and lab-bounded. |
| `docs/SDD.md` | Software design document. | Must have in this repo | Component responsibilities and data contracts are clear. |
| `docs/STUDENT_CHECKLIST.md` | Pre-submission checklist. | Must have in this repo | Covers container, entry points, state, logs, report, and safety. |
| `docs/SAFETY_BOUNDARY.md` | Course-lab safety document. | Must have in this repo | States allowed and forbidden behavior. |
| `logs/sample_run.log` | Example evidence from a safe local run. | Should have | Includes round, component, event, result, and timestamp; no dangerous details. |

## 5. Functional Requirements

### FR-001: `/exploit` must exist at root path

Requirement: the EC must provide an executable file at `/exploit`.

Acceptance:

```sh
test -f /exploit
test -x /exploit
```

Failure cases:

- File exists at `/home/student/exploit` but not `/exploit`.
- File exists but lacks executable permission.
- File requires manual compilation during grading.

### FR-002: `/triage` must exist at root path

Requirement: the EC must provide an executable file at `/triage`.

Acceptance:

```sh
test -f /triage
test -x /triage
```

Failure cases:

- File exists only under a source directory.
- File requires a working directory change before execution.
- File cannot run in the EC environment.

### FR-003: `/exploit` must be non-interactive

Requirement: `/exploit` must not ask the grader or student for input.

Acceptance:

- `/exploit` exits without stdin input.
- No prompt asks for offsets, filenames, phase numbers, or strategy choices.
- The command has a bounded runtime and meaningful exit code.

Failure cases:

- Blocks waiting for keyboard input.
- Requires manual file copy or manual config editing.

### FR-004: `/exploit` must check `/shared/config.data`

Requirement: `/exploit` must verify that the expected config file is present
and writable before writing a candidate config.

Acceptance:

- Logs whether `/shared/config.data` exists.
- Handles a missing file gracefully.
- Does not silently create unrelated replacement paths.

Failure cases:

- Crashes without a clear message.
- Waits forever for the file.
- Writes to a different path.

### FR-005: `/exploit` must check `/shared/blogic.copy`

Requirement: `/exploit` must safely confirm the presence of the supplied
`blogic.copy` artifact and record safe metadata if useful.

Acceptance:

- Confirms `/shared/blogic.copy` exists when provided.
- Records safe metadata such as file size, hash, or high-level file type.
- Does not modify `/shared/blogic.copy`.

Failure cases:

- Modifies or deletes `blogic.copy`.
- Requires dangerous or external analysis tools during grading.
- Stores weaponized details in documentation or logs.

### FR-006: `/exploit` must modify `/shared/config.data`

Requirement: `/exploit` must write a candidate controlled-lab config to
`/shared/config.data`.

Acceptance:

- Hash before and after differs when a new candidate config is written.
- The file remains readable by IC.
- The file is not deleted or permanently renamed.
- The write is logged without exposing dangerous details.

Failure cases:

- Only touches the file timestamp.
- Writes to a temporary file but never replaces `config.data`.
- Breaks file permissions.

### FR-007: `/exploit` must create `/shared/exploit_done`

Requirement: `/exploit` must create the exact marker file after finishing the
`config.data` write.

Acceptance:

- `/shared/exploit_done` exists after config write completion.
- Marker is created at the correct path.
- Marker is not created before `config.data` is fully written.

Failure cases:

- Creates `/tmp/exploit_done`.
- Creates `/shared/exploit.done`.
- Signals before finishing the write, causing a race condition.

### FR-008: `/exploit` must terminate per round

Requirement: each `/exploit` invocation must complete one round action and exit.

Acceptance:

- No long-running foreground loop.
- Exits within the expected timeout.
- Returns a meaningful exit code.

Failure cases:

- Runs as an unbounded daemon.
- Starts background processes that interfere with grading.
- Hides errors behind exit code `0`.

### FR-009: `/triage` must be non-interactive

Requirement: `/triage` must not require manual coredump selection or user input.

Acceptance:

- `/triage` exits without stdin input.
- Selection rules are deterministic.
- Logs enough to show what evidence was considered.

Failure cases:

- Prompts for a coredump filename.
- Requires manual copying from `/shared/coredump`.

### FR-010: `/triage` must handle no-coredump case

Requirement: `/triage` must behave safely when no coredump exists.

Acceptance:

- Does not crash.
- Creates initial state or logs `no evidence available`.
- Exits cleanly with a documented status.

Failure cases:

- Crashes on empty directory.
- Treats missing coredump as success.
- Loops forever waiting for a file.

### FR-011: `/triage` must inspect `/shared/coredump/*` when available

Requirement: `/triage` must detect and consider available coredump files.

Acceptance:

- Detects available coredump files.
- Selects the newest or most relevant coredump by deterministic rule.
- Logs which coredump was considered.

Failure cases:

- Ignores all coredumps.
- Uses an arbitrary file without logging the selection.
- Requires external network services to analyze evidence.

### FR-012: `/triage` must update machine-readable state

Requirement: `/triage` should write state that `/exploit` can read next round.

Recommended path:

```text
/shared/triage_state.json
```

Acceptance:

- JSON is valid.
- Includes round number.
- Includes last evidence status.
- Includes next strategy identifier.
- Includes safe notes.
- Contains no secrets or external target data.

Failure cases:

- Writes malformed JSON.
- Writes only human prose that `/exploit` cannot parse.
- Stores dangerous details in the state file.

### FR-013: `/exploit` must consume triage state

Requirement: `/exploit` should read the state written by `/triage` when present.

Acceptance:

- Reads `/shared/triage_state.json` when present.
- Records which strategy state was used.
- Next-round behavior can be explained from the state and logs.

Failure cases:

- Ignores triage state entirely.
- Reads stale state without checking round or timestamp.
- Cannot explain why the next candidate changed.

### FR-014: System must be repeatable

Requirement: the workflow must run from a clean EC and a clean `/shared` volume.

Acceptance:

- Clean `/shared` volume run works.
- Clean container run works.
- Old state does not corrupt a new grading run.
- Previous coredumps are not required for a fresh attempt.

Failure cases:

- Success depends on manually preserved files.
- Run fails if old logs are absent.
- Run only works on a student's laptop path.

### FR-015: System must stay lab-only

Requirement: every action must remain within the course Docker lab boundary.

Acceptance:

- No external network connections.
- No host path modification.
- No grader tampering.
- No fake success signal.
- Logs and docs avoid operational offensive details.

Failure cases:

- Runtime download from the internet.
- External callback.
- Docker socket access.
- Modifying grader or IC image to fake success.

## 6. Non-Functional Requirements

| ID | Requirement | Description | Reason | Acceptance criteria |
| --- | --- | --- | --- | --- |
| NFR-001 | Reproducibility | Same submitted files should run in a clean EC and clean `/shared`. | Grading must not depend on local residue. | Clean run produces bounded logs and valid state. |
| NFR-002 | Deterministic behavior where possible | File selection, state naming, and log format should be stable. | Auditors need to reproduce decisions. | Coredump selection rule and state schema are documented. |
| NFR-003 | Clear logging | Each round should record component, event, result, and timestamp. | Grading needs evidence. | JSONL logs are parseable and bounded. |
| NFR-004 | Bounded runtime | Commands must finish within expected round time. | Grader has a 30-minute total limit. | `/exploit` and `/triage` do not hang. |
| NFR-005 | Bounded disk usage | Logs and state must not fill `/shared`. | Resource exhaustion is unsafe and unfair. | Logs are compact; raw dumps are not duplicated. |
| NFR-006 | No external grading dependency | Runtime must not require internet access. | Grading should be offline and repeatable. | Network-off test does not break expected local behavior. |
| NFR-007 | Readable error handling | Errors should produce clear messages and meaningful exit codes. | Debugging should not require guessing. | Missing files produce bounded failures. |
| NFR-008 | Safe failure | Failure must not modify host, grader, or unrelated files. | Protects the lab environment. | Failure stays inside `/shared` and EC-owned files. |
| NFR-009 | No host impact | The EC must not affect the host or Docker daemon. | Required safety boundary. | No host path writes, daemon access, or destructive commands. |

## 7. Runtime Workflow

```mermaid
flowchart TD
    A[Start round] --> B[Grader runs /exploit]
    B --> C[/exploit writes candidate config.data]
    C --> D[/exploit creates /shared/exploit_done]
    D --> E[IC detects exploit_done]
    E --> F[IC runs blogic with config.data]
    F --> G{Backdoor success recorded by grader?}
    G -- Yes --> H[Stop and record success time]
    G -- No --> I[IC places coredump under /shared/coredump]
    I --> J[Grader runs /triage]
    J --> K[/triage updates triage_state.json]
    K --> L{Under 60 rounds and 30 minutes?}
    L -- Yes --> A
    L -- No --> M[Stop and record bounded failure evidence]
```

Round responsibilities:

| Step | Owner | Required evidence |
| --- | --- | --- |
| Run `/exploit` | Grader/EC | exit code, timestamp |
| Write config | `/exploit` | hash before/after, log event |
| Signal done | `/exploit` | marker path, ordering evidence |
| Process config | IC | grader or IC log |
| Store failure feedback | IC | coredump count/path |
| Run `/triage` | Grader/EC | exit code, state update |
| Next round | `/exploit` | state read event |

## 8. State File Specification

Recommended path:

```text
/shared/triage_state.json
```

Example:

```json
{
  "schema_version": "1.0",
  "project": "project2",
  "phase": "II",
  "round": 3,
  "last_exploit": {
    "config_hash": "placeholder",
    "strategy_id": "candidate-v3",
    "timestamp": "ISO-8601"
  },
  "last_triage": {
    "coredump_found": true,
    "selected_coredump": "/shared/coredump/core.placeholder",
    "analysis_status": "parsed",
    "summary": "Safe high-level summary only"
  },
  "next_action": {
    "strategy_id": "candidate-v4",
    "parameters": {
      "safe_placeholder": "value"
    },
    "confidence": 0.65
  },
  "safety": {
    "lab_only": true,
    "external_network": false
  }
}
```

Rules:

- Do not include weaponized details in docs or state examples.
- Do not include secrets.
- Do not include external host data.
- Use strategy identifiers and safe placeholders instead of offensive details.
- Store hashes or summaries when raw content is unnecessary.

## 9. Logging Specification

Recommended paths:

```text
/shared/project2_agent.log
/shared/round_log.jsonl
```

Preferred structured log format: JSONL, one event per line.

Each round log should include:

| Field | Meaning |
| --- | --- |
| `round` | Current round number if known. |
| `component` | `exploit`, `triage`, or `safety`. |
| `event` | Short event name. |
| `success` | Boolean result. |
| `timestamp` | ISO-8601 timestamp. |
| `config_hash` | Safe hash when relevant. |
| `coredump_count` | Number of coredumps seen when relevant. |
| `state_version` | State schema version. |
| `exit_code` | Component exit code when relevant. |

Example JSONL:

```json
{"round":1,"component":"exploit","event":"environment_checked","success":true,"timestamp":"ISO-8601","exit_code":0}
{"round":1,"component":"exploit","event":"config_written","success":true,"timestamp":"ISO-8601","config_hash":"sha256:placeholder"}
{"round":1,"component":"exploit","event":"exploit_done_created","success":true,"timestamp":"ISO-8601"}
{"round":1,"component":"triage","event":"coredumps_scanned","success":true,"timestamp":"ISO-8601","coredump_count":1}
{"round":1,"component":"triage","event":"state_written","success":true,"timestamp":"ISO-8601","state_version":"1.0"}
```

Logging rules:

- Keep logs bounded.
- Do not store secrets.
- Do not copy raw coredump content into logs.
- Do not include external targets.
- Log enough for grading without exposing operational offensive details.

## 10. Testing Specification

| Test ID | Purpose | Setup | Command | Expected result | Evidence |
| --- | --- | --- | --- | --- | --- |
| TC-001 | Path test | EC is running | `test -f /exploit && test -f /triage` | Both paths exist | shell exit code |
| TC-002 | Permission test | EC is running | `test -x /exploit && test -x /triage` | Both executable | shell exit code |
| TC-003 | Exploit no-stdin test | `/shared` mounted | `timeout 30s /exploit </dev/null` | Exits without prompt | exit code, log |
| TC-004 | Config modification test | Record `config.data` hash before run | `timeout 30s /exploit </dev/null` | Hash changes when candidate config is written | before/after hash |
| TC-005 | `exploit_done` ordering test | Clean marker before run | `timeout 30s /exploit </dev/null` | Marker exists after config write event | timestamps/log sequence |
| TC-006 | No-coredump triage test | Empty `/shared/coredump/` | `timeout 30s /triage </dev/null` | No crash; state or log created | exit code, state/log |
| TC-007 | Coredump detection test | Place safe placeholder evidence file under coredump dir if allowed by test harness | `timeout 30s /triage </dev/null` | Triage logs selected evidence by deterministic rule | log event |
| TC-008 | State update test | Triage has run | inspect `/shared/triage_state.json` | Valid JSON with round/evidence/next action | JSON parser result |
| TC-009 | Clean run test | Fresh EC and fresh `/shared` | run official or local safe grading loop | No dependency on old files | run log |
| TC-010 | Safety boundary test | Runtime network disabled; review paths | run local checks | No external network dependency or host writes | network-off result, review |

These tests validate interfaces and evidence. They do not require documenting
payload details.

## 11. Student Checklist

- [ ] `/exploit` exists at container root.
- [ ] `/triage` exists at container root.
- [ ] Both files are executable.
- [ ] Neither entry point requires interactive input.
- [ ] `/exploit` checks `/shared/config.data`.
- [ ] `/exploit` checks `/shared/blogic.copy` without modifying it.
- [ ] `/exploit` modifies `/shared/config.data`.
- [ ] `/exploit` creates `/shared/exploit_done` only after config write.
- [ ] `/exploit` exits cleanly per round.
- [ ] `/triage` handles an empty coredump directory.
- [ ] `/triage` detects available coredumps.
- [ ] `/triage` writes valid `/shared/triage_state.json`.
- [ ] `/exploit` reads `/shared/triage_state.json` when present.
- [ ] Logs include round, component, event, result, and timestamp.
- [ ] No external network dependency exists during grading.
- [ ] No host files or grader files are modified.
- [ ] README explains build/run commands.
- [ ] Sample log is included.
- [ ] Safety statement is included.

## 12. Grading Readiness

Prepare evidence that helps the grader verify behavior without needing exploit
details:

| Evidence | Purpose |
| --- | --- |
| Build log | Shows EC can be built or loaded. |
| Sample run log | Shows round-level behavior and exit codes. |
| `triage_state.json` example | Shows state schema and safe next-round state. |
| Config hash sequence | Shows config changed between relevant steps. |
| Known limitations | Explains bounded failure cases without hiding issues. |
| Optional screenshots | Useful only if they show official grader status or build output. |

Do not submit or describe weaponized payload details in the documentation.
Focus on reproducibility, interfaces, logging, and safe lab behavior.

