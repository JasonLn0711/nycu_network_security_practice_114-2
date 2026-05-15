# Phase II Experiment Log

Date: 2026-05-15
Scope: NYCU Project II Phase II controlled local IC lab.

## Purpose

This is the canonical experiment ledger for Phase II recovery work.

Every technical experiment must be recorded here, whether it succeeds, fails,
or only narrows the search space. A separate dated attempt note may hold deeper
evidence, but this ledger must remain the single index that lets the next reader
answer:

- what was tested;
- what prior blocker it was meant to avoid;
- what exact environment or command family was used;
- what was observed;
- whether `/shared/success.txt` appeared;
- what route is now open or closed.

Do not run another full-credit recovery experiment without updating this file in
the same work block.

## Record Contract

Every new experiment record must include:

| Field | Requirement |
| --- | --- |
| ID | Stable ID such as `P2-EXP-015`. |
| Date | Local date of the experiment. |
| Hypothesis | One falsifiable sentence. |
| Prior blocker avoided | Name the old route this does not depend on. |
| Environment | Container, binary hash, ASLR, and relevant shared path if applicable. |
| Procedure | Exact command or bounded procedure at the level needed for reproduction inside the controlled lab. |
| Expected observation | What result would count as progress. |
| Observed result | Artifact, coredump/register state, static-search result, or no-success result. |
| Success artifact | Whether IC-side `/shared/success.txt` appeared. |
| Verdict | `open`, `closed`, `positive primitive only`, or `full-credit success`. |
| Next action | One concrete follow-up or stop rule. |
| Evidence files | Link the dated attempt note, validation note, or coredump path if preserved. |

## Status Legend

| Status | Meaning |
| --- | --- |
| full-credit success | IC-side `/backdoor` created `/shared/success.txt`. |
| positive primitive only | The experiment found a useful primitive but did not create `/shared/success.txt`. |
| closed | The tested route did not work and should not be repeated without a new mechanism. |
| open | Static or planning result leaves a bounded follow-up, but no candidate has proven success. |

## Summary Ledger

| ID | Date | Track | Short result | Status | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| P2-EXP-000 | 2026-05-13 | Baseline overflow | Marker input confirmed stack control and saved RIP offset `97`; no success. | positive primitive only | `PHASE2_SUCCESS_VALIDATION.md`, `HANDOFF_PHASE2.md` |
| P2-EXP-001 | 2026-05-13 | Direct maintenance entry | Ret-to-`maintenance_task+5` did not pass controlled `user_input` as first argument. | closed | `PHASE2_SUCCESS_VALIDATION.md` |
| P2-EXP-002 | 2026-05-14 | NX check | Direct stack execution reached the intended stack address but faulted under NX. | closed | `PHASE2_COMPLETION_ATTEMPT_2026-05-14.md` |
| P2-EXP-003 | 2026-05-14 | Text sweep | One-shot partial-return sweep tried `10328` candidates and found no `/shared/success.txt`. | closed | `PHASE2_COMPLETION_ATTEMPT_2026-05-14.md` |
| P2-EXP-004 | 2026-05-14 | Saved-RBP argument control | `maintenance_task+22` was reachable, but saved RBP was non-canonical marker data. | closed | `PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md` |
| P2-EXP-005 | 2026-05-14 | Main-binary call-path scan | No main-binary path was found that sets `rdi = user_input` and calls the success path. | closed | `PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md` |
| P2-EXP-006 | 2026-05-14 | Caller-stack staging | `pop rbp; ret` consumed fixed caller-stack qwords, not a controlled second stage. | closed | `PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md` |
| P2-EXP-007 | 2026-05-14 | Heap/global forward write | Long `user_input` reached heap-adjacent memory but crashed before useful control flow. | closed | `PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md` |
| P2-EXP-008 | 2026-05-14 | User-input setup boundary | Fresh IC consumed the candidate, produced no success, no coredump, and kept `/blogic` running. | closed | `PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md` |
| P2-EXP-009 | 2026-05-15 | Multiline staging | Earlier `user_input=` lines can stage bytes past the final line's NUL. | positive primitive only | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md` |
| P2-EXP-010 | 2026-05-15 | Multiline heap boundary | Longer staged data can touch heap-adjacent state, but allocator checks can abort. | positive primitive only | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md` |
| P2-EXP-011 | 2026-05-15 | One-gadget feasibility | Local libc one-gadget candidates did not match the needed `/backdoor` path or constraints. | closed | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md` |
| P2-EXP-012 | 2026-05-15 | Direct `rax` reuse | Returned into the `mov rdi, rax; call system` path, but no success and `system()` returned `0x7f00`. | closed | `PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md` |
| P2-EXP-013 | 2026-05-15 | Backward pivot feasibility | Fresh main binary plus pinned libc had no usable simple backward `rsp` pivot in the tested family. | closed | `PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md` |
| P2-EXP-014 | 2026-05-15 | Current-`rdi` argument reuse | Direct `system@plt` received an empty libc lock pointer, not controlled `user_input`. | closed | `PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md` |

## Detailed Records

### P2-EXP-000 - Baseline Overflow And Offset Discovery

| Field | Record |
| --- | --- |
| Date | 2026-05-13 |
| Hypothesis | A long `user_input` can corrupt `log_message()` saved control data. |
| Prior blocker avoided | Not applicable; this establishes the baseline primitive. |
| Environment | Supplied Phase II `server_2`, ASLR disabled, official shared-volume workflow. |
| Procedure | Write a marker `user_input` through the EC/IC flow and inspect the resulting coredump. |
| Expected observation | Saved RIP/RBP contain marker bytes and the return offset can be measured. |
| Observed result | Coredump showed crash at `0x40146f`, marker-controlled RBP, and saved RIP overwrite after `97` user bytes. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | positive primitive only. |
| Next action | Use offset `97` only inside bounded controlled-lab probes. |
| Evidence files | `PHASE2_SUCCESS_VALIDATION.md`, `HANDOFF_PHASE2.md`. |

### P2-EXP-001 - Direct Maintenance Entry

| Field | Record |
| --- | --- |
| Date | 2026-05-13 |
| Hypothesis | Returning to `maintenance_task+5` may reuse a controlled first argument. |
| Prior blocker avoided | Avoids needing a main-binary `pop rdi; ret`. |
| Environment | Official Phase II IC loop, `server_2`, ASLR disabled. |
| Procedure | Enable the Phase II control-flow probe and let IC consume `/shared/exploit_done`. |
| Expected observation | IC-side `/backdoor` executes through the maintenance command path. |
| Observed result | IC consumed the signal, but no success appeared; debug state showed `rdi` pointed to an empty stdout-lock area. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Do not repeat direct ret-to-maintenance unless a new first-argument setup is proven. |
| Evidence files | `PHASE2_SUCCESS_VALIDATION.md`. |

### P2-EXP-002 - NX Stack Execution Check

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | Direct stack execution might still be viable if the stack mapping is executable. |
| Prior blocker avoided | Tests whether a pivot/call-path solution is necessary. |
| Environment | Reproduced x86_64 IC, `server_2`, ASLR disabled, NX checked from program headers and runtime fault. |
| Procedure | Use a bounded stack-address control probe inside the controlled lab and inspect the fault. |
| Expected observation | Progress only if the stack executes. |
| Observed result | Control reached the intended stack address, but execution faulted because the stack is non-executable. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Treat NX as active; do not pursue direct stack execution. |
| Evidence files | `PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`. |

### P2-EXP-003 - One-Shot Text Partial-Return Sweep

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | Some reachable text address might accidentally set up the success path without a normal ROP chain. |
| Prior blocker avoided | Avoids appended ROP and explicit first-argument gadgets. |
| Environment | Reproduced Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Run the bounded lab-only one-shot sweep over `0x401000..0x401a20` with four command-prefix families. |
| Expected observation | `/shared/success.txt` appears for at least one target. |
| Observed result | `10328` candidates tried; no success artifact appeared. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed for this sweep range and candidate family. |
| Next action | Do not repeat broad text sweeps without a narrower written hypothesis. |
| Evidence files | `PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`, `scripts/run_phase2_one_shot_sweep.py`. |

### P2-EXP-004 - Saved-RBP Argument Control

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | Entering `maintenance_task+22` could read the preserved `user_input` pointer through the expected frame slot. |
| Prior blocker avoided | Avoids relying on stale `rdi` at `log_message()` return. |
| Environment | Phase II IC, `server_2`, ASLR disabled, coredump analysis. |
| Procedure | Return to the maintenance body boundary and inspect the resulting frame/register state. |
| Expected observation | RBP names a canonical frame where `[rbp-0x88]` resolves to `user_input`. |
| Observed result | Target was reached, but RBP was marker-controlled and non-canonical. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed for direct saved-RBP use. |
| Next action | Only revisit if a separate staging mechanism can preserve a canonical frame pointer while still controlling RIP. |
| Evidence files | `PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`. |

### P2-EXP-005 - Main-Binary Call-Path Scan

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | A main-binary sequence may set `rdi = user_input` and then call `system()` or `maintenance_task()`. |
| Prior blocker avoided | Avoids saved RBP, appended ROP, and libc gadget address encoding. |
| Environment | Static analysis of fresh `server_2`. |
| Procedure | Inspect main-binary instruction starts and call paths around relevant symbols. |
| Expected observation | A reachable sequence performs first-argument setup and calls a success-relevant function. |
| Observed result | No useful sequence was found; main binary also lacks a useful `pop rdi; ret`. |
| Success artifact | No candidate run; static route not found. |
| Verdict | closed for the searched main-binary path family. |
| Next action | Look outside this direct main-binary call-path family. |
| Evidence files | `PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`. |

### P2-EXP-006 - Caller-Stack Staging

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | Returning to `pop rbp; ret` may use untouched caller-stack qwords as a second-stage chain. |
| Prior blocker avoided | Avoids embedding a normal post-RIP ROP chain in the C string. |
| Environment | Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Target the caller-stack staging boundary and observe success/coredump behavior. |
| Expected observation | Control continues through attacker-controlled staged qwords. |
| Observed result | No success and no useful coredump; path consumed fixed original caller-stack qwords. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Do not treat untouched caller-stack qwords as controlled. |
| Evidence files | `PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`. |

### P2-EXP-007 - Heap/Global Forward Write

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | The unbounded `strcpy()` into `user_input` can change heap/global state before the stack overflow returns. |
| Prior blocker avoided | Avoids stack staging and saved-RBP dependence. |
| Environment | Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Use a long controlled `user_input` value and inspect memory/state after the copy path. |
| Expected observation | A useful global or heap target changes and survives until control flow can use it. |
| Observed result | The write reached around `0x405000`, but the same long string crashed in libc copy handling through `sprintf()` before useful control flow. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed for direct long-string heap adjacency. |
| Next action | Only revisit with a separate mechanism that avoids the same `sprintf()` crash. |
| Evidence files | `PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`. |

### P2-EXP-008 - User-Input Setup Boundary

| Field | Record |
| --- | --- |
| Date | 2026-05-14 |
| Hypothesis | Re-entering the user-input setup boundary may reload controlled data into the right argument path. |
| Prior blocker avoided | Avoids using stale post-logging argument registers directly. |
| Environment | Fresh Phase II IC from `lab.zip`, ASLR disabled. |
| Procedure | Run one bounded setup-boundary candidate after rechecking IC state. |
| Expected observation | IC-side `/backdoor` execution or a coredump proving progress. |
| Observed result | IC consumed `/shared/exploit_done`, produced no success, produced no coredump, and `/blogic` remained running. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Do not repeat simple setup-boundary re-entry as a direct route. |
| Evidence files | `PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md`. |

### P2-EXP-009 - Multiline Staging Primitive

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | Multiple `user_input=` lines let an earlier line stage bytes beyond the final line's terminating NUL. |
| Prior blocker avoided | Avoids requiring all staged bytes to appear in the final overflowing C string. |
| Environment | Fresh local Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Use a long first `user_input=` line and a shorter final `user_input=` line, then inspect `user_input` after parsing. |
| Expected observation | Visible final string is short, but bytes beyond its NUL remain from the earlier staging line. |
| Observed result | Staged bytes remained beyond the final line's NUL in `.bss`. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | positive primitive only. |
| Next action | Needs a separate first-stage pivot or first-argument setup before it can help full-credit success. |
| Evidence files | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`. |

### P2-EXP-010 - Multiline Heap Boundary

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | Multiline staging can safely reach heap-adjacent state while a short final line avoids the earlier direct `sprintf()` crash. |
| Prior blocker avoided | Avoids copying the long staged string through the final `sprintf()` path. |
| Environment | Fresh local Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Combine long staging with a shorter final trigger and inspect allocator/runtime behavior. |
| Expected observation | Heap-adjacent mutation survives and remains usable. |
| Observed result | Heap-adjacent state can be touched, but allocator consistency checks can abort on broad corruption. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | positive primitive only. |
| Next action | Heap work needs a precise allocator plan; broad overwrite is not a route. |
| Evidence files | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`. |

### P2-EXP-011 - One-Gadget Feasibility

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | Local libc one-gadget constraints may fit the post-`log_message()` state. |
| Prior blocker avoided | Avoids first-argument setup for `system("/backdoor")`. |
| Environment | Pinned Ubuntu 24.04 libc from the Phase II IC. |
| Procedure | Check local one-gadget feasibility against observed register/stack state and required success artifact. |
| Expected observation | A candidate both matches constraints and can reach the course success condition. |
| Observed result | Candidates are shell-oriented, do not directly run `/backdoor`, and constraints do not match observed state. |
| Success artifact | No candidate run; static route not found. |
| Verdict | closed. |
| Next action | Do not rely on one-gadget as the full-credit mechanism. |
| Evidence files | `PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`. |

### P2-EXP-012 - Direct RAX Reuse

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | The post-logging `rax` value may still point at controlled command text and can be moved into `rdi` by an existing tail sequence. |
| Prior blocker avoided | Avoids appended ROP and preserved saved RBP. |
| Environment | Fresh Phase II IC, `server_2`, ASLR disabled. |
| Procedure | Use `PROJECT2_PHASE2_STRATEGY=register-reuse-system-rax` and inspect the coredump. |
| Expected observation | `system()` receives controlled `/backdoor` command text. |
| Observed result | Selected path was reached, but no success appeared; `system()` returned `0x7f00` and the later crash was at the corrupted-frame epilogue. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Do not continue direct `rax` reuse. |
| Evidence files | `PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md`. |

### P2-EXP-013 - Backward Pivot Feasibility

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | A first-stage gadget can move `rsp` backward into controlled pre-RIP stack bytes. |
| Prior blocker avoided | Avoids appended post-RIP ROP bytes and saved RBP. |
| Environment | Fresh `server_2` plus pinned Ubuntu 24.04 libc from a disposable IC. |
| Procedure | Search the bounded pivot family: `sub rsp, imm; ret`, negative `add rsp, imm; ret`, `lea rsp, [rsp-negative-imm]; ret`, `xchg rsp, reg; ret`, and `mov rsp, reg; ret`. |
| Expected observation | At least one reachable first-stage pivot exists. |
| Observed result | No usable gadget in the tested family was found in the fresh binary set. |
| Success artifact | No live candidate run; no concrete first-stage address existed. |
| Verdict | closed for this pivot family. |
| Next action | Future pivot work must use a genuinely different mechanism. |
| Evidence files | `PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md`. |

### P2-EXP-014 - Current-RDI Argument Reuse

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | Returning directly to `system@plt` can reuse current `rdi` as a useful command pointer. |
| Prior blocker avoided | Avoids appended ROP, saved RBP, and direct `rax` reuse. |
| Environment | Fresh disposable IC `IC_PHASE2_NEXT`, `server_2` SHA-256 `155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c`, ASLR disabled, shared path `/tmp/project2_phase2_next/lab/shared`. |
| Procedure | Run `PROJECT2_SHARED_DIR=/tmp/project2_phase2_next/lab/shared PROJECT2_ENABLE_PHASE2_PROBE=1 PROJECT2_PHASE2_STRATEGY=current-rdi-system python3 -m src.exploit_runner`, then inspect success and coredump state. |
| Expected observation | `system()` receives controlled `/backdoor` text from `user_input`. |
| Observed result | IC consumed `/shared/exploit_done`; coredump `blogic-74.core` stopped in libc `do_system()` with `line = 0x7ffff7d00710 ""`; controlled `/backdoor` text remained in `user_input`. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed. |
| Next action | Do not reuse current `rdi` directly; find a different non-stack staging or first-argument setup mechanism. |
| Evidence files | `PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md`; preserved local coredump path `/tmp/project2_phase2_next/lab/shared/coredump/blogic-74.core` if not cleaned. |

## Future Entry Template

Use this template for `P2-EXP-015` and later:

```markdown
### P2-EXP-XXX - Short Title

| Field | Record |
| --- | --- |
| Date | YYYY-MM-DD |
| Hypothesis |  |
| Prior blocker avoided |  |
| Environment |  |
| Procedure |  |
| Expected observation |  |
| Observed result |  |
| Success artifact |  |
| Verdict |  |
| Next action |  |
| Evidence files |  |
```
