# Project I - Virus Scanner

## Agent Search Summary

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title: `Project I. Virus Scanner`
- Opened: `2026-03-08 00:00`
- Due: `2026-06-07 23:59`
- Team size: `1-4`
- Status: active, team and minimum scope not locked
- Planning locator: `../../../planning-everything-track/data/projects/2026-06-network-security-virus-scanner.md`
- Official brief: `project-spec.pdf`

## Objective

Build a functional signature-based virus scanner named in the brief as the "Sentinel" scanner. The scanner should scan a directory tree, compare files against a known-malware signature database, and produce a clear security report.

## Required Deliverables

| Deliverable | Requirement |
| --- | --- |
| Source code | Well-documented code hosted in a private GitHub or GitLab repository |
| Project report | Explain the scanner design, especially the signature database data structure |
| Demo | Show the scanner detecting a safe mock virus, such as the EICAR test file, hidden inside a folder tree |

## Project Phases

| Phase | Milestone | Objective |
| --- | --- | --- |
| I | Database design | Create a structured malware-signature repository, such as JSON or CSV, with MD5/SHA-256 hashes and hex patterns. |
| II | Scanning engine | Implement file traversal and comparison logic. |
| III | Heuristic analysis | Add a small ruleset for suspicious file behaviors, such as suspicious API-call indicators when available from the test data. |
| IV | Reporting and UI | Generate a log/report with infected paths, threat levels, and timestamps. |

## Scope Guardrails

In scope:

- signature database in JSON or CSV
- hash and pattern matching
- folder traversal
- basic heuristic flags
- report/log output
- safe demo using mock malware only

Out of scope:

- production antivirus behavior
- live malware handling
- broad malware reverse engineering that is not required by the brief
- UI polish before the scanner core and demo path work

## First Useful Checkpoint

Before implementation, confirm:

- who is on the team
- whether Project I is still required if Project II is also listed
- programming language and private-repo location
- minimum acceptable heuristic feature
- demo folder shape and safe mock-virus input

## File Map

| Path | Purpose |
| --- | --- |
| `project-spec.pdf` | Official project brief |
| `README.md` | Local routing, objective, deliverables, and guardrails |

When implementation begins, keep the project source, report draft, and demo notes here or link to the required private source repository from this README.
