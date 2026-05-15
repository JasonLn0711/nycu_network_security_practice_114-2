# Project II - Autonomous APT Agent

## Agent Search Summary

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title in attachment: `Project II. Autonmous APT Agent`
- PDF title metadata: `Project - Automous APT Agent`
- Opened: `2026-04-13 00:00`
- Due: `2026-06-07 23:59`
- Status: active, relationship to Project I not yet clarified
- Planning locator: `../../../planning-everything-track/data/projects/2026-06-network-security-project-ii-apt-agent.md`
- Official brief: `project-brief.pdf`
- Provided lab bundle: `lab.zip`
- Lab manifest: `lab-manifest.md`
- Presentation scheduling evidence: `../report-scheduling/`
- Presentation intent: Jason presents this or the other non-Project-I item while 陳靖中 presents Project I.
- Booked presentation slot: `2026-05-27 10:50`
- Travel logistics: paid HSR tickets are booked for same-day Taipei <-> Hsinchu
  travel; see `../report-scheduling/2026-05-12-hsr-booking-2026-05-27.md`.


## Latest Engineering Checkpoint - 2026-05-14

FIRST PRINCIPLE status: the Project II deliverable is not a one-shot string; it
is a closed EC/IC grading loop. The EC must expose `/exploit` and `/triage`,
write `/shared/config.data`, signal `/shared/exploit_done`, learn from coredump
feedback, and eventually cause the IC-side `/backdoor` to create
`/shared/success.txt`.

Current course-repo state:

- protocol scaffolding, state/logging, static checks, readiness report, clean
  source packaging, and optional image export are implemented under
  `project2-agent-scaffold/`;
- machine-handoff state for continuation is compressed in
  `../../HANDOFF_PHASE2.md`; start there before any new Phase II continuation
  run so verified facts, dead ends, and theory do not get mixed;
- the latest deep sweep/NX attempt is recorded in
  `project2-agent-scaffold/docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`;
- the latest bounded argument-control attempt is recorded in
  `project2-agent-scaffold/docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md`;
- the latest staging-boundary attempt is recorded in
  `project2-agent-scaffold/docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md`;
- the latest heap/global-state attempt is recorded in
  `project2-agent-scaffold/docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md`;
- the next executable action is now defined in
  `project2-agent-scaffold/docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md`;
- the completion audit, success-validation log, and traceability matrix
  explicitly state that official Phase II IC-side success has **not** been
  observed yet;
- the current honest submission mode is therefore a protocol-ready/partial
  package unless the final IC-side `/backdoor` success evidence is produced
  before upload;
- generated runtime/package outputs stay out of git (`mock_shared/`, `dist/`,
  `__pycache__/`).

## Objective

Prepare the external-container side of the Autonomous APT Agent grading setup. The required artifact must provide runnable `/exploit` and `/triage` paths, interact with the shared volume, and match the provided grading flow.

This project should be treated as a controlled course lab. Keep all exploit, triage, and backdoor-related work inside the supplied local lab environment.

## Environment Model

| Component | Role |
| --- | --- |
| External container (EC) | Student-prepared container that runs `/exploit` and `/triage` |
| Internal container (IC) | Provided environment with the business-logic program and preinstalled `/backdoor` |
| Shared volume | Mounted at `/shared` in both EC and IC |
| `/shared/config.data` | Data file modified by the exploit path and processed by the business-logic program |
| `/shared/exploit_done` | Marker file created by `/exploit` to trigger IC processing |
| `/shared/coredump/*` | Crash outputs made available for triage |

## Required Behavior

| Path | Expected role |
| --- | --- |
| `/exploit` | Modify `/shared/config.data` and create `/shared/exploit_done` for the grading loop |
| `/triage` | Analyze feedback such as coredumps and prepare the next attempt |

The score depends on total penetration time in the grading procedure, not on building a general red-team framework.

## Project Phases

| Phase | Difficulty | Brief summary |
| --- | --- | --- |
| I | Easy | Stack-based buffer issue, executable stack, non-PIE executable, ASLR disabled |
| II | Medium | Stack-based buffer issue, non-PIE executable, ASLR disabled |
| III | Hard | Stack-based buffer issue, non-PIE executable, ASLR enabled |

## Scope Guardrails

In scope:

- understanding the supplied lab bundle
- reproducing the local grading model
- building EC behavior that fits the provided `/exploit` and `/triage` requirements
- keeping notes on exact assumptions and test results

Out of scope:

- applying techniques to non-course systems
- persistence outside the provided containers
- credential collection, network pivoting, or real third-party targets
- expanding the lab into a general offensive toolkit

## First Useful Checkpoint

Before implementation, confirm:

- whether Project II replaces Project I or both are required
- exact submission format for the external container
- whether a written report or demo is required in addition to runnable EC behavior
- team ownership of exploit, triage, report, and demo tasks

## File Map

| Path | Purpose |
| --- | --- |
| `docs/SPEC.md` | Student-facing assignment specification, deliverables, FR/NFR, test cases, and grading-readiness guidance |
| `docs/SDD.md` | Student-facing software design document for the EC workflow, components, state, logs, error handling, and safety |
| `docs/STUDENT_CHECKLIST.md` | Pre-submission checklist for container, entry points, state/logs, report, and safety |
| `docs/SAFETY_BOUNDARY.md` | Lab-only safety boundary, forbidden behavior, safe wording, and self-checks |
| `project2-agent-scaffold/` | Runnable classroom-safe EC scaffold with `/exploit`, `/triage`, mock grader, tests, state/logging, and docs; does not implement a real exploit |
| `project2-agent-scaffold/docs/CORE_WORKFLOW.md` | Step-by-step explanation of the safe round-based feedback loop: action, execution, evidence, triage, state update, next action |
| `project2-agent-scaffold/docs/COMPLETION_AUDIT.md` | Honest completion audit: implemented protocol pieces, current Phase II probe status, and remaining full-credit success evidence gap |
| `project2-agent-scaffold/docs/PHASE2_SUCCESS_VALIDATION.md` | Latest official-IC validation log for the current Phase II candidate; records observed non-success without fabricating `/shared/success.txt` |
| `project2-agent-scaffold/docs/PHASE2_EXPERIMENT_LOG.md` | Canonical Phase II experiment ledger: every success, failure, and positive primitive must be indexed here |
| `project2-agent-scaffold/docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md` | Deep follow-up validation pass: x86_64 Colima IC setup, baseline non-success, NX shellcode check, one-shot text sweep, and current boundary |
| `project2-agent-scaffold/docs/PHASE2_FIRST_PRINCIPLES_NEXT_GATE_2026-05-14.md` | First-principles next-gate note: choose one bounded argument-control, pivot, or instructor-clarification block before more candidate testing |
| `project2-agent-scaffold/docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md` | Bounded argument-control follow-up: maintenance-body entry reached, no success, saved-RBP/C-string constraint documented |
| `project2-agent-scaffold/docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md` | Bounded staging follow-up: single-target and caller-stack staging checked, no success, next route narrowed to heap/global-state feasibility |
| `project2-agent-scaffold/docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md` | Bounded heap/global-state follow-up: forward write reaches heap-adjacent memory but crashes in `sprintf()` before a useful state change |
| `project2-agent-scaffold/docs/PHASE2_BOUNDED_RECOVERY_BLOCK_2026-05-14.md` | Bounded full-credit recovery block: fresh IC drift check plus one user-input setup-boundary candidate, no official success artifact |
| `project2-agent-scaffold/docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md` | Bounded multiline staging follow-up: parser leaves staged bytes beyond the final `user_input` NUL, but no pivot or first-argument setup yet |
| `project2-agent-scaffold/docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md` | Bounded register-reuse follow-up: direct post-logging `rax` reuse reaches `system()` but does not create `/shared/success.txt` |
| `project2-agent-scaffold/docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md` | Bounded backward-pivot feasibility check: no usable simple first-stage pivot found in the fresh binary set |
| `project2-agent-scaffold/docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md` | Bounded current-`rdi` argument follow-up: direct `system@plt` receives an empty libc lock pointer, not controlled `user_input` |
| `project2-agent-scaffold/docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md` | Complete current-state analysis: done, not done, and what is required to finish |
| `project2-agent-scaffold/docs/TEACHER_REQUIREMENTS_COMPLETION_VERDICT_2026-05-14.md` | Direct verdict on which teacher requirements are complete and which full-credit items remain incomplete |
| `project2-agent-scaffold/docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md` | Concrete TA clarification / LMS upload action packet for the current protocol-complete partial posture |
| `project2-agent-scaffold/docs/PROJECT_II_NEXT_STEP_RUNBOOK_2026-05-14.md` | Detailed next-step runbook for TA clarification, partial upload, Docker image fallback, and bounded full-credit recovery |
| `project2-agent-scaffold/docs/SUBMISSION_SPEC.md` | Submission-facing SPEC for protocol-complete partial versus full-credit complete states |
| `project2-agent-scaffold/docs/SUBMISSION_SDD.md` | Submission-facing SDD for EC architecture, evidence design, and packaging |
| `project2-agent-scaffold/docs/PARTIAL_SUBMISSION_BRIEF.md` | Honest protocol-complete partial submission brief and final gate checklist |
| `project2-agent-scaffold/docs/TA_CLARIFICATION_DRAFT.md` | Short TA-facing clarification draft for source/image format and partial-status handling |
| `project2-agent-scaffold/docs/REQUIREMENTS_TRACEABILITY.md` | Requirement-by-requirement compliance matrix against the official brief and local rubric |
| `project2-agent-scaffold/docs/SUBMISSION_GUIDE.md` | Recommended packaging, build, smoke-test, and submission workflow |
| `project2-agent-scaffold/scripts/build_submission_package.sh` | Builds a clean zip submission package under `project2-agent-scaffold/dist/` while excluding generated runtime state |
| `project2-agent-scaffold/scripts/run_phase2_one_shot_sweep.py` | Lab-only reproducibility harness for the bounded one-shot partial-return sweep; does not create `/shared/success.txt` |
| `../../HANDOFF_PHASE2.md` | Machine handoff for the next Phase II agent: objective, verified facts, important symbols, failed/explored paths, current hypothesis, exact environment, useful commands, and FACT/THEORY separation |
| `SPEC.md` | Local audit-oriented requirements, deliverables, functional requirements, acceptance tests, and grading interface |
| `SDD.md` | Local audit-oriented software design document for the EC workflow, state files, logging, safety guards, and grader design |
| `project-brief.pdf` | Official project brief |
| `lab.zip` | Provided lab bundle |
| `lab-manifest.md` | Plain-text inventory of the lab bundle |
| `grading-rubric-phase-ii.md` | Strict local 100-point grading spec for Project II / Phase II Medium |
| `README.md` | Local routing, objective, deliverables, and guardrails |
