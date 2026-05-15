# Project II Requirements Traceability Matrix

Date: 2026-05-13
Updated: 2026-05-15
Target: Project II - Autonomous APT Agent, Phase II / Medium

This matrix checks the submission against the official brief and the local rubric.
It separates **implemented**, **verified**, and **remaining risk** so the final
package is honest and auditable.

## Official Requirement Coverage

| Brief requirement | Evidence in this repo | Current status | Verification command / note |
| --- | --- | --- | --- |
| Student prepares the external container (EC). | `Dockerfile` in this directory. | Implemented | `docker build -t project2-agent-scaffold-readiness .` passed locally. |
| `/exploit` exists at container root. | Dockerfile creates `ln -sf ... /exploit`; wrapper file `exploit`. | Implemented | `scripts/run_static_checks.sh` checks wrapper. |
| `/triage` exists at container root. | Dockerfile creates `ln -sf ... /triage`; wrapper file `triage`. | Implemented | `scripts/run_static_checks.sh` checks wrapper. |
| `/exploit` modifies `/shared/config.data`. | `src/exploit_runner.py` atomic byte writer. | Implemented | Mock readiness and real shared smoke test changed config hash/content. |
| `/exploit` creates `/shared/exploit_done`. | `src/exploit_runner.py`. | Implemented | Mock readiness and real shared smoke test. |
| Uses shared volume `/shared`. | `src/path_config.py`; override via `PROJECT2_SHARED_DIR` for tests. | Implemented | Static checks and mock grader. |
| Can examine `blogic.copy`. | `resolve_blogic_path()` accepts `blogic.copy` and supplied-lab `blogic`. | Implemented | Real lab metadata smoke test found `/shared/blogic`. |
| `/triage` reads coredump feedback. | `src/coredump_scanner.py`, `src/coredump_analyzer.py`, `src/triage_runner.py`. | Implemented | Mock grader creates fake coredumps and state updates. |
| Phase II Medium target: non-PIE, ASLR disabled, NX stack. | `src/phase2_payload.py` uses non-PIE partial text-address probe; Docker image enables probe mode. | Partially implemented | Control-flow probe written; IC-side `/backdoor` success not yet observed. |
| Score depends on time to execute `/backdoor`. | `docs/COMPLETION_AUDIT.md` records that final success is not observed yet. | Remaining gap | Need official IC `/shared/success.txt` evidence. |
| Completion evidence is reproducible. | `docs/PHASE2_EXPERIMENT_LOG.md`; `docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`; `docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`; `docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`; `docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`; `docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md`; `docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md`; `docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md`; `docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md`; `docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md`; `scripts/run_phase2_one_shot_sweep.py`. | Partially implemented | Every recorded experiment is indexed; success evidence is still missing. |
| Partial submission posture is explicit. | `docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md`; `docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md`; `docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md`; `docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md`; `docs/SUBMISSION_SPEC.md`; `docs/SUBMISSION_SDD.md`; `docs/PARTIAL_SUBMISSION_BRIEF.md`; `docs/TA_CLARIFICATION_DRAFT.md`; `docs/SUBMISSION_GUIDE.md`. | Implemented | Package can be submitted honestly as protocol-complete partial if full success is not reached before the gate. |
| No external network runtime dependency. | Python-only local code; no network calls. | Implemented | Readiness report scans for obvious runtime network tokens. |
| No grader bypass / fake success. | Code does not write `/shared/success.txt`; docs forbid doing so. | Implemented | Reviewed `src/`; only IC-side `/backdoor` should create success. |

## Current Honest Grade-Risk Summary

- Strong coverage: container interface, `/exploit` and `/triage` protocol,
  state/logging, controlled-lab path handling, buildability, documentation.
- Main grade risk: the current Phase II work has **not** produced IC-side
  `/shared/success.txt`, so full C-section success points are not yet earned.
- The package is therefore a high-quality partial implementation unless the
  final Phase II candidate is completed and validated before submission.
- The latest bounded attempts narrow the simple routes: direct maintenance,
  stack shellcode, broad text sweep, saved-RBP argument control, caller-stack
  staging, direct heap/global-state adjacency, multi-line staging without a
  pivot, direct `rax` register reuse, the simple backward-pivot family, and
  direct current-`rdi` argument reuse have not produced success.

## Commands Used For Current Verification

```sh
python3 -m compileall -q src
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
docker build -t project2-agent-scaffold-readiness .
python3 scripts/run_phase2_one_shot_sweep.py --start 0x401470 --stop 0x401476
git diff --check
```

The full 2026-05-14 one-shot sweep was run inside the supplied IC container
against `/blogic` and `/shared`; the short command above is a syntax/smoke shape
for the harness, not a replacement for the full IC validation pass.

## Required Before Claiming Full Completion

1. Run the EC image with the official Phase II IC.
2. Confirm that `/shared/success.txt` is created by IC-side `/backdoor`.
3. Save the grader log and `mock_shared/readiness_report.json` or equivalent
   real-run report.
4. Re-run this traceability matrix and update the remaining gap to complete.

## Required Before Honest Partial Upload

If full completion is not reached before the gate:

1. Run `./scripts/run_static_checks.sh`.
2. Run `./scripts/generate_readiness_report.sh`.
3. Run `./scripts/build_submission_package.sh`.
4. Review `docs/PARTIAL_SUBMISSION_BRIEF.md`.
5. Review `docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md`,
   `docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md`,
   `docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md`,
   `docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md`,
   `docs/SUBMISSION_SPEC.md`, and `docs/SUBMISSION_SDD.md`.
6. Send or adapt `docs/TA_CLARIFICATION_DRAFT.md` if TA clarification is needed.
7. Confirm the zip does not contain `mock_shared/`, `dist/`, `__pycache__/`, or
   coredumps.
