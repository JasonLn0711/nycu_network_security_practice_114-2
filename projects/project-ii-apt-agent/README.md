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


## Latest Engineering Checkpoint - 2026-05-13

FIRST PRINCIPLE status: the Project II deliverable is not a one-shot string; it
is a closed EC/IC grading loop. The EC must expose `/exploit` and `/triage`,
write `/shared/config.data`, signal `/shared/exploit_done`, learn from coredump
feedback, and eventually cause the IC-side `/backdoor` to create
`/shared/success.txt`.

Current course-repo state:

- protocol scaffolding, state/logging, static checks, readiness report, clean
  source packaging, and optional image export are implemented under
  `project2-agent-scaffold/`;
- the completion audit and traceability matrix explicitly state that official
  Phase II IC-side success has **not** been observed yet;
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
| `project2-agent-scaffold/docs/REQUIREMENTS_TRACEABILITY.md` | Requirement-by-requirement compliance matrix against the official brief and local rubric |
| `project2-agent-scaffold/docs/SUBMISSION_GUIDE.md` | Recommended packaging, build, smoke-test, and submission workflow |
| `project2-agent-scaffold/scripts/build_submission_package.sh` | Builds a clean zip submission package under `project2-agent-scaffold/dist/` while excluding generated runtime state |
| `SPEC.md` | Local audit-oriented requirements, deliverables, functional requirements, acceptance tests, and grading interface |
| `SDD.md` | Local audit-oriented software design document for the EC workflow, state files, logging, safety guards, and grader design |
| `project-brief.pdf` | Official project brief |
| `lab.zip` | Provided lab bundle |
| `lab-manifest.md` | Plain-text inventory of the lab bundle |
| `grading-rubric-phase-ii.md` | Strict local 100-point grading spec for Project II / Phase II Medium |
| `README.md` | Local routing, objective, deliverables, and guardrails |
