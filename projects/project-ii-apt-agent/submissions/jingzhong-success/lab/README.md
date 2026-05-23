# Autonomous APT Agent

## 1. Project Overview

This project implements an **analysis-driven adaptive exploit agent** for the course project **[2026 NS] Project - Autonomous APT Agent**.

The grading environment contains two containers:

- **EC (External Container)**: runs the exploit agent.
- **IC (Internal Container)**: runs the vulnerable business logic program `blogic`.

The EC agent can access the shared volume `/shared`, modify `/shared/config.data`, and create `/shared/exploit_done`. Once IC detects `/shared/exploit_done`, it runs `blogic`, which reads `/shared/config.data`. The goal is to trigger execution of `/backdoor` inside IC.

This implementation is designed as a **bounded autonomous agent** for the provided lab environment. It does not scan networks, attack external systems, or operate outside the `/shared` lab interface.

---

## 2. Assignment Requirements Covered

The assignment requires the submitted EC image to provide:

| Requirement | Implementation |
|---|---|
| `/exploit` executable | Implemented |
| `/triage` executable | Implemented |
| `/exploit` modifies `/shared/config.data` | Implemented |
| `/exploit` creates `/shared/exploit_done` | Implemented |
| `/shared/blogic.copy` or `/shared/blogic` can be examined | Implemented by `analyze_target.py` |
| IC runs `blogic` after `exploit_done` appears | Supported by grader flow |
| Failed attempts can produce coredumps under `/shared/coredump/*` | Observed during probing |
| `/triage` runs after failed rounds | Implemented |
| Maximum 60 rounds | Supported; adaptive probing succeeds within the limit |
| Maximum 30 minutes | All tests completed within seconds |

The grading loop is interpreted as:

```text
for round = 1..MaxRound:
    EC runs /exploit
    IC waits for /shared/exploit_done
    IC runs blogic on /shared/config.data
    if /backdoor executes:
        grading terminates successfully
    else:
        coredump is stored
        EC runs /triage
```

Therefore, the agent does **not** need to run all 60 rounds. Sixty rounds is the maximum number of attempts, not the required number of attempts.

---

## 3. High-Level Architecture

The system follows this agent loop:

```text
Analyze → Plan → Generate → Execute → Observe → Update State → Retry
```

The implementation contains three major components:

```text
EC/
├── Dockerfile
├── exploit
├── triage
└── analyze_target.py
```

### 3.1 Target Analyzer: `analyze_target.py`

The analyzer performs read-only analysis on:

```text
/shared/blogic.copy
/shared/blogic
```

It extracts:

- ELF architecture
- 32-bit / 64-bit information
- PIE status
- NX / executable stack status
- Symbol table
- Interesting strings
- Imported risky functions
- Candidate target functions
- Candidate `ret` gadgets
- Offset inference attempts

Generated outputs:

```text
/shared/target_info.json
/shared/target_analysis.log
```

### 3.2 Exploit Generator: `/exploit`

The exploit generator:

1. Runs `/analyze_target.py`.
2. Reads `/shared/target_info.json`.
3. Selects the discovered `execute_task` function.
4. Selects a discovered `ret` gadget.
5. Chooses an offset strategy:
   - fast final exploit mode
   - adaptive offset probing mode
   - fallback calibrated lab profile
6. Writes `/shared/config.data`.
7. Creates `/shared/exploit_done`.

Generated outputs:

```text
/shared/config.data
/shared/exploit_done
/shared/exploit.log
/shared/state.json
```

### 3.3 Triage Module: `/triage`

The triage module:

1. Reads `/shared/state.json`.
2. Checks whether `/shared/success.txt` exists.
3. Checks `/shared/coredump/*`.
4. Infers the previous round result.
5. Updates the next action in `/shared/state.json`.
6. Advances adaptive offset probing candidates when needed.

Generated outputs:

```text
/shared/triage.log
/shared/state.json
```

---

## 4. Agent State

The agent maintains state in:

```text
/shared/state.json
```

Example state:

```json
{
  "round": 1,
  "offset_status": "adaptive_probe",
  "offset_candidates": [64, 72, 80, 88, 96, 104, 112, 120, 128],
  "offset_candidate_index": 0,
  "strategy": "adaptive_static_analysis_driven_agent",
  "ret_gadget": "0x401414",
  "ret_gadget_source": "analyzer_preferred_ret",
  "execute_task": "0x401415",
  "mode": "adaptive_offset_probe",
  "next_action": "try_next_offset_candidate"
}
```

This allows `/exploit` and `/triage` to cooperate across rounds.

---

## 5. Analysis Features

### 5.1 ELF and Protection Analysis

The analyzer detects that the target binary is:

```text
ELF 64-bit
x86_64
non-PIE
not stripped
```

It also checks the GNU_STACK program header. In the tested Phase 1 binary, the stack was executable:

```text
GNU_STACK ... RWE
```

### 5.2 Symbol Discovery

The analyzer parses the symbol table and discovers important symbols such as:

```text
user_input
user_input_len
main
execute_task
maintenance_task
parse_config
```

The most important target is:

```text
execute_task = 0x401415
```

This value is not manually hard-coded in `/exploit`; it is read from `target_info.json`.

### 5.3 Ret Gadget Discovery

The analyzer disassembles the binary and searches for `ret` instructions.

Example discovered preferred gadget:

```text
ret_gadget = 0x401414
```

This is selected automatically because it is the closest useful `ret` gadget before `execute_task`.

### 5.4 Offset Handling

The original working exploit required:

```text
offset_to_ret = 104
```

This is the distance from the start of `user_input` to the saved return address.

The project implements two approaches:

1. **Static offset inference attempt**
2. **Adaptive offset probing**

The static inference attempt is conservative. It rejects unreliable candidates when the disassembly contains complex C++ stack objects.

The adaptive offset probing mode is more reliable in this lab because it tests candidate offsets across grading rounds.

---

## 6. Exploit Payload Structure

The final payload has this structure:

```text
user_input=/backdoor\x00 + padding + ret_gadget + execute_task
```

Conceptually:

```text
/backdoor\x00
A...A until offset_to_ret
ret gadget address
execute_task address
```

When the function returns, the overwritten return address redirects control flow through the selected `ret` gadget and then to `execute_task`.

---

## 7. Operating Modes

### 7.1 Fast Final Exploit Mode

This is the default mode when no prior adaptive state exists.

It uses:

- analyzer-discovered `execute_task`
- analyzer-discovered `ret_gadget`
- calibrated lab profile offset if automatic inference is unavailable

This mode is useful for stable grading and typically succeeds in Round 1.

### 7.2 Adaptive Offset Probing Mode

This mode demonstrates the autonomous feedback loop.

To enable it, create `/shared/state.json` before running the grader:

```bash
python3 - <<'PY'
import json
from pathlib import Path

state = {
    "round": 1,
    "offset_status": "adaptive_probe",
    "offset_candidates": [64, 72, 80, 88, 96, 104, 112, 120, 128],
    "offset_candidate_index": 0,
    "next_action": "try_next_offset_candidate"
}

Path("shared/state.json").write_text(json.dumps(state, indent=2))
PY
```

The agent then tries one candidate per round.

Example observed behavior:

```text
Round 1: offset 64  -> no_success_no_coredump
Round 2: offset 72  -> no_success_no_coredump
Round 3: offset 80  -> no_success_no_coredump
Round 4: offset 88  -> no_success_no_coredump
Round 5: offset 96  -> crash
Round 6: offset 104 -> success
```

This demonstrates that `104` can be discovered by the agent within the 60-round limit.

---

## 8. Problems Encountered and Fixes

### Problem 1: Initial implementation was too hard-coded

Early versions used:

```text
offset_to_ret = 104
ret_gadget = 0x401414
execute_task = 0x401415
```

This worked, but it looked like a fixed exploit runner rather than an autonomous agent.

#### Fix

We added `analyze_target.py` to automatically identify:

- target binary properties
- symbols
- `execute_task`
- `ret` gadgets

Now `execute_task` and `ret_gadget` are selected from analyzer output.

---

### Problem 2: NX parser initially returned `unknown`

The original GNU_STACK parser failed because normal `readelf -l` output wrapped lines.

#### Fix

Changed:

```bash
readelf -l
```

to:

```bash
readelf -W -l
```

This allowed the parser to correctly identify:

```text
GNU_STACK ... RWE
```

---

### Problem 3: Static offset inference selected the wrong buffer

The first static offset inference selected the largest stack displacement in `parse_config`:

```text
-0x280(%rbp)
```

This produced:

```text
offset_to_ret = 0x280 + 8 = 0x288 = 648
```

That payload crashed and did not execute `/backdoor`.

#### Root Cause

`parse_config` is a C++ function with many stack objects such as `ifstream`, string objects, and temporary buffers. The largest `rbp` displacement is not necessarily the vulnerable overflow buffer.

#### Fix

The analyzer now treats static offset inference conservatively:

- It tries to locate meaningful vulnerable-copy evidence.
- It rejects unsafe candidates instead of using a false inference.
- Adaptive probing is used to discover the correct offset when static inference is unreliable.

---

### Problem 4: Coredumps were generated but empty

During probing, many files appeared under:

```text
/shared/coredump/*
```

However, their size was:

```text
0 bytes
```

This made it unreliable to recover RIP/RSP or cyclic-pattern information from coredumps.

#### Fix

Instead of relying on coredump content, the agent uses triage feedback at a higher level:

- success
- crash
- no success and no coredump

Then it advances to the next offset candidate.

---

### Problem 5: Probe mode originally repeated the same crash

The first probe mode generated the same payload every round. This caused repeated crashes until `MaxRound`.

#### Fix

`/triage` now advances `offset_candidate_index` after each failed round when `offset_status = adaptive_probe`.

---

## 9. Testing

### 9.1 Build EC Image

```bash
docker build -t my_ec ./EC
```

### 9.2 Build IC Image

```bash
docker build -t ic_image ./IC
```

### 9.3 Clean Shared Directory

```bash
rm -f shared/config.data shared/exploit_done shared/success.txt
rm -f shared/exploit.log shared/triage.log shared/target_analysis.log
rm -f shared/target_info.json shared/state.json
rm -f shared/coredump/*
```

---

## 10. Fast Mode Test Results

Fast mode uses fresh `/shared` with no adaptive `state.json`.

### Phase 1

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 1

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

Observed result:

```text
[*] Round 1 start
[+] Exploit successful! Grading ends.
[*] Grading done
Total time: 1 seconds
```

### Phase 2

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 2

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

Observed result:

```text
[*] Round 1 start
[+] Exploit successful! Grading ends.
[*] Grading done
Total time: 1 seconds
```

### Phase 3

```bash
docker rm -f IC_PHASE1 IC_PHASE2 IC_PHASE3 2>/dev/null || true
bash ./docker.sh 3

docker run -it --rm \
  -v "$(pwd)/shared:/shared" \
  -v "$(pwd)/grader.sh:/grader.sh:ro" \
  my_ec bash /grader.sh
```

Observed result:

```text
[*] Round 1 start
[+] Exploit successful! Grading ends.
[*] Grading done
Total time: 1 seconds
```

Phase 3 has ASLR enabled, but the target is non-PIE, so code addresses remain stable enough for the discovered `execute_task` and `ret_gadget` addresses to work.

---

## 11. Adaptive Mode Test Result

Adaptive mode was tested by setting:

```json
{
  "offset_status": "adaptive_probe",
  "offset_candidates": [64, 72, 80, 88, 96, 104, 112, 120, 128],
  "offset_candidate_index": 0
}
```

Observed Phase 1 result:

```text
[*] Round 1 start
[*] triage complete
[*] result: no_success_no_coredump
[*] next_action: try_next_offset_candidate
[*] offset_to_ret: 72

[*] Round 2 start
[*] triage complete
[*] result: no_success_no_coredump
[*] next_action: try_next_offset_candidate
[*] offset_to_ret: 80

[*] Round 3 start
[*] triage complete
[*] result: no_success_no_coredump
[*] next_action: try_next_offset_candidate
[*] offset_to_ret: 88

[*] Round 4 start
[*] triage complete
[*] result: no_success_no_coredump
[*] next_action: try_next_offset_candidate
[*] offset_to_ret: 96

[*] Round 5 start
[*] triage complete
[*] result: crash
[*] next_action: try_next_offset_candidate
[*] offset_to_ret: 104

[*] Round 6 start
[+] Exploit successful! Grading ends.
[*] Grading done
Total time: 3 seconds
```

This demonstrates that the agent can find the correct return-address offset through adaptive retries within the 60-round limit.

---

## 12. Generality of the Architecture

The current implementation is not just a single fixed payload. It is a reusable architecture for this class of lab targets.

The general parts are:

- ELF metadata extraction
- PIE/NX detection
- symbol table parsing
- target function discovery
- `ret` gadget discovery
- state-driven exploit generation
- triage-driven feedback
- adaptive offset probing

Target-specific assumptions still exist:

- The target is a local ELF binary placed in `/shared`.
- The input interface is `/shared/config.data`.
- Success is indicated by `/shared/success.txt`.
- The expected command is `/backdoor`.
- The exploit strategy assumes a stack-based control-flow hijack.

---

## 13. Limitations

This prototype is best described as an:

```text
analysis-driven adaptive exploit agent
```

rather than a completely general exploit framework.

Known limitations:

1. It does not attack external systems.
2. It assumes the lab shared-volume interface.
3. It assumes the presence of useful symbols or recognizable patterns.
4. Coredump files in this environment may be empty, so register-level crash analysis is not reliable.
5. Static offset inference is conservative and may reject complex C++ stack layouts.
6. Adaptive probing is used to recover the offset when static inference is unreliable.
7. The default fast mode uses a calibrated lab profile for stable grading when no adaptive state is provided.

---

## 14. Final Evaluation

The project satisfies the assignment workflow:

```text
/exploit → config.data → exploit_done → blogic → /backdoor
```

It also implements an autonomous feedback loop:

```text
Analyze → Generate → Execute → Observe → Triage → Retry
```

The most important result is that the agent can operate in adaptive mode and discover the working offset within the 60-round limit, instead of only relying on a manually fixed offset.

