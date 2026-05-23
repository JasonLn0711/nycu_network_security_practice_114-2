# 10-Minute Presentation Plan

Audience: instructor / classmates in Network Security Practice.

Goal: explain the successful Project II package clearly, show the system
function and system features, and leave evidence that `/backdoor` was triggered
inside the bounded lab.

## Timing Overview

| Time | Slide / segment | Main point |
| ---: | --- | --- |
| `0:00-0:30` | 1. Title and result | This is an Autonomous APT Agent for the course lab; final package succeeds. |
| `0:30-1:20` | 2. Assignment interface | EC must provide `/exploit` and `/triage`, modify `/shared/config.data`, and signal `/shared/exploit_done`. |
| `1:20-2:20` | 3. System architecture | EC, IC, and `/shared` form a closed grading loop. |
| `2:20-3:25` | 4. Analyzer function | Agent reads `blogic`, extracts ELF metadata, symbols, gadgets, and risk clues. |
| `3:25-4:45` | 5. Exploit generation | Agent selects `execute_task`, ret gadget, and offset, then writes payload config. |
| `4:45-5:45` | 6. Triage and adaptive probing | `/triage` updates state after success/crash/no-success; adaptive mode demonstrates autonomous retry. |
| `5:45-6:50` | 7. System features | Analysis-driven, state-driven, bounded lab-only, fast mode and adaptive mode. |
| `6:50-7:30` | 8. Success evidence | Show `success.txt`, exploit log, and payload flow. |
| `7:30-9:20` | Optional demo | Evidence walkthrough is recommended; warm live demo only if already tested. |
| `9:20-10:00` | 9. Conclusion and limitation | Satisfies assignment interface in this package; bounded to course lab; binary-version caveat. |

## Narrative Arc

The presentation should answer four questions in order:

1. **What did the project need?**
   - Build the external-container side.
   - Provide `/exploit` and `/triage`.
   - Interact through `/shared`.
   - Trigger IC-side `/backdoor`.

2. **What did the system do?**
   - Analyze target binary.
   - Generate a payload based on discovered symbols and gadgets.
   - Signal the IC.
   - Observe outcome and update state.

3. **Why did it work?**
   - The successful package contains `execute_task()`.
   - `execute_task()` calls `maintenance_task(user_input)`.
   - The payload places `/backdoor` in `user_input` and returns to
     `execute_task`.

4. **What is the evidence?**
   - Saved `success.txt`.
   - Saved exploit log selecting `execute_task = 0x401415`,
     `ret_gadget = 0x401414`, and `offset_to_ret = 104`.
   - Reported fast mode and adaptive mode behavior.

## Slide Count

Use `8-9` slides. This keeps the pace under control:

1. Title / result
2. Assignment grading loop
3. Architecture
4. Target analyzer
5. Exploit generation / payload flow
6. Triage and adaptive probing
7. System features
8. Demo / evidence
9. Conclusion / limitation

If the instructor is strict about `10` minutes, skip a detailed live run and use
Slide 8 as an evidence walkthrough.

## What To Avoid

- Do not start from a clean Docker build during the report.
- Do not spend time explaining Jason's failed branch unless asked.
- Do not overclaim that this proves the earlier `lab.zip` binary also succeeds.
- Do not present the package as a general offensive tool.
- Do not show external targets, network scans, or non-course systems.

## One-Sentence Thesis

> This system is a bounded autonomous exploit agent for the course lab: it
> analyzes the provided target, generates a shared-volume payload, uses triage
> state for feedback, and in the successful package triggers `/backdoor` through
> the discovered `execute_task()` path.

