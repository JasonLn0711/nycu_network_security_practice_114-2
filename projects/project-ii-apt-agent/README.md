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
| `project-brief.pdf` | Official project brief |
| `lab.zip` | Provided lab bundle |
| `lab-manifest.md` | Plain-text inventory of the lab bundle |
| `README.md` | Local routing, objective, deliverables, and guardrails |
