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
| P2-EXP-015 | 2026-05-15 | Post-stream first-argument transfer | Controlled pointers survived in stack/local slots, but no single-stage `rdi` setup plus success call was found. | closed | `PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md` |
| P2-EXP-016 | 2026-05-15 | Precise BSS staging boundary | `3264` staged bytes safely fill the data-page tail; `3300+` crosses into allocator state and crashes. | positive primitive only | `PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md` |
| P2-EXP-017 | 2026-05-15 | BSS-indirect dispatch feasibility | Static search found no single-shot gadget that moves staged `.bss` data into first argument and reaches exec-family. | closed | `PHASE2_BSS_INDIRECT_DISPATCH_FEASIBILITY_2026-05-15.md` |

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

### P2-EXP-015 - Post-Stream First-Argument Transfer Check

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | After the final C++ stream call in `log_message()`, a controlled pointer may still survive in a fixed stack/local slot or original caller-stack qword, and a single reachable sequence may move that pointer into the first argument and call `system()` or `execve()` without appended ROP. |
| Prior blocker avoided | Avoids appended ROP, preserved saved RBP, direct `rax` reuse, and direct current-`rdi` reuse. |
| Environment | Disposable IC `IC_PHASE2_P15`, `server_2` SHA-256 `155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c`, libc SHA-256 `d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75`, ASLR disabled, evidence dir `/tmp/project2_phase2_p15/`. |
| Procedure | Write a marker `user_input=` line that reaches `log_message()` return; trigger the IC loop; capture `blogic-30.core` at the `ret` boundary; byte-scan the pinned libc and main binary for first-stage `rdi`-setup-to-`system`/`execve` sequences. |
| Expected observation | A reachable single-stage gadget that loads a controlled pointer into `rdi` and immediately calls `system()` or `execve()` without appended ROP. |
| Observed result | Core showed `rip = 0x40146f`, `rax = 0x404100`, `rdi = 0x7ffff7d00710`; controlled data preserved at `[$rsp-0x70] = 0x404340` and `[$rsp+0x08] = 0x00007fffffffec00`; static scan found 10 direct `system`/`execve` call sites in libc but `rdi_setup_to_system_or_execve_gadgets = 0`; the only `pop rdi; call rax` sequence at libc offset `0x129a61` is unusable because post-stream `rax = 0x404100` is the writable `cout` object, not an executable success path. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | closed for the tested single-stage first-argument family. |
| Next action | Do not re-run a single-stage post-stream `rdi`-setup probe; the next block must use a different mechanism. |
| Evidence files | `PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md`. |

### P2-EXP-016 - Precise BSS Non-Stack Staging Boundary

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | Multi-line `user_input=` staging can safely fill the `.bss`/data-page tail up to the allocator boundary, but crossing into heap/tcache state is not stable unless a precise allocator plan exists. |
| Prior blocker avoided | Avoids the broad heap-overwrite assumption from `P2-EXP-009`. |
| Environment | Same disposable IC as `P2-EXP-015`. |
| Procedure | For a sweep of first-line lengths `L` in `{2048, 3000, 3200, 3264, 3300, 3400, 3500, 3600, 3700, 3800, 4000}`, write `user_input=STAGELEN<L>;...` followed by a short `user_input=P15-FINAL;...` line; trigger the IC; record where the IC reaches `log_message()` return cleanly versus where it crashes in libc allocator paths. |
| Expected observation | A precise length boundary separating safe `.bss`/data-page staging from allocator-state corruption. |
| Observed result | `L=3200` and `L=3264` reached `log_message()` ret cleanly with staged 'S' bytes still present at `0x404ff0` and allocator state intact at `0x405000`; `L=3300` and `L=3400` crashed in `tcache_get_n` before the final `log_message()` ret; `L>=3500` reproduced `SIGABRT` in the allocator path. |
| Success artifact | No `/shared/success.txt`. |
| Verdict | positive primitive only (safe non-stack staging window bounded at `L=3264`). |
| Next action | Treat `0x404340..0x404FFF` as the safe multi-line staging address range; do not rely on `L>=3300` heap overwrites unless a separate precise allocator plan is written first. |
| Evidence files | `PHASE2_POST_STREAM_ARGUMENT_AND_BSS_BOUNDARY_2026-05-15.md`. |

### P2-EXP-017 - BSS-Indirect Dispatch Feasibility (deeper static slice)

| Field | Record |
| --- | --- |
| Date | 2026-05-15 |
| Hypothesis | A single-shot binary or libc gadget exists that sets `rdi` from `rax + small disp` (or another callee-preserved register) into the multi-line `.bss` staging range and transfers control to `system`/`execve`-family in one shot. |
| Prior blocker avoided | Avoids appended ROP after saved RIP, preserved saved RBP, direct `rax` reuse, direct current-`rdi` reuse, and the simple backward stack-pivot family. |
| Environment | Local in-tree extraction `/tmp/p2_explore/lab`, `server_2` SHA-256 `155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c`, pinned libc `/tmp/project2_pivot_static/libc.so.6` SHA-256 `d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75`, libc executable file range `0x28000..0x1afd39`. No live IC was started. |
| Procedure | Static byte-scan over `server_2` text and the pinned libc executable segment for the candidate single-shot families (`lea rdi, [rax+disp]; (jmp|call) <exec-family>`, `mov rdi, [rax+disp]; (jmp|call) <exec-family>`, `mov rdi, r{bx,8,12,13,14,15}; (jmp|call) <exec-family>`); decode each candidate's call/jmp target and verify it resolves to `system`/`execve`/`execvp`/`execvpe`/`posix_spawn`. |
| Expected observation | At least one matching gadget with a decoded target inside the exec-family symbols and a `disp` that lands `rax + disp` inside `0x404340..0x404FFF`. |
| Observed result | Six libc `lea rdi, [rax+disp32]; call rel32` matches all resolve to `__pthread_mutex_unlock` or internal assert helpers; 23 `lea rdi, [rax+disp8]; call rel32` matches use `disp` of `0x1` or `0x3` and target the `cout` object, not the staging range; `server_2` text has zero `lea rdi, [rip+disp]`, `mov rdi, [rax]`, `mov rdi, [rax+disp]`, `mov rdi, [rsp+disp]`, or `pop rdi; ret` matches; the only binary `mov edi, imm; jmp rax` gadgets at `0x401387` and `0x4013c9` hardcode `rdi = 0x4040d8` (in `.data`, before `user_input`, unreachable through forward `strcpy`). The exec-family direct-call sites in libc are preceded by `mov rdi, rbx` / `mov rdi, r8` / `mov rdi, r15`, none of which is pinned to a value inside the staging range at `log_message` return time. |
| Success artifact | No `/shared/success.txt`; no live IC run was performed. |
| Verdict | closed. |
| Next action | Do not run a live EC candidate for this hypothesis class; pivot to submission-track follow-through (`docs/TA_CLARIFICATION_DRAFT.md`, `docs/PARTIAL_SUBMISSION_BRIEF.md`) or open a new bounded block with a fundamentally different writable primitive (heap-allocator state, shared-volume file, or kernel-level escalation). |
| Evidence files | `PHASE2_BSS_INDIRECT_DISPATCH_FEASIBILITY_2026-05-15.md`. |

## Future Entry Template

Use this template for `P2-EXP-018` and later:

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
