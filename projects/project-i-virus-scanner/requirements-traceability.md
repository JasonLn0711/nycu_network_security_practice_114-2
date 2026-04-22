# Project I Requirements Traceability

## Purpose

This file turns the official Virus Scanner brief into implementation-ready requirements.
Use it to decide whether the scanner, report, and demo are complete enough for submission.

## Source Facts

- Course project: `[2026 NS] Project - Virus Scanner`
- Tool name in brief: `Sentinel`
- Due date tracked in planning: `2026-06-07 23:59`
- Team size tracked in planning: `1-4`
- Required output: functional signature-based virus scanner, source code, report, and demo
- Safety input: safe mock virus such as the EICAR test file

## Requirement Matrix

| ID | Requirement | Source phase / deliverable | Minimum acceptance check | Evidence to keep |
| --- | --- | --- | --- | --- |
| R1 | Scan a directory tree of files. | Phase II - Scanning Engine | CLI accepts a directory and visits nested files deterministically. | Demo command, tree listing, test result |
| R2 | Maintain a structured malware-signature repository. | Phase I - Database Design | JSON or CSV signature database stores at least name, severity, hash type/value, and optional byte or hex pattern. | Signature file, schema note |
| R3 | Compare scanned files against known signatures. | Phase II - Scanning Engine | Known safe mock-virus fixture is detected by exact hash or pattern match. | Unit test, demo report |
| R4 | Implement bitwise or byte-pattern comparison. | Phase II - Scanning Engine | Hex or byte patterns are converted to bytes and searched inside target files. | Matcher test, code comments where useful |
| R5 | Add basic heuristic analysis. | Phase III - Heuristic Analysis | At least one documented low-risk heuristic flags a safe suspicious fixture without claiming it is confirmed malware. | Heuristic rules table, sample report row |
| R6 | Generate a security report. | Phase IV - Reporting and UI | Report includes scanned paths, infected or suspicious paths, threat names, severity, match reason, and timestamps. | JSON or Markdown report artifact |
| R7 | Host well-documented source code in a private GitHub or GitLab repository. | Deliverable 1 | Private repo exists, README explains setup/run/test, and final source has no live malware or secrets. | Private repo URL, commit hash |
| R8 | Write a project report explaining data-structure choices. | Deliverable 2 | Report explains why hash maps, pattern lists, and any optional Bloom filter were or were not used. | Report source/PDF |
| R9 | Demonstrate detection inside a complex folder structure. | Deliverable 3 | Demo tree contains clean files plus a hidden safe mock-virus file; scanner finds the mock virus and leaves clean files clean. | Video or live-demo script, demo report |

## Minimal Valid Scope

The minimum project that satisfies the brief is:

1. A command-line scanner.
2. A JSON or CSV signature database.
3. Exact hash matching using MD5 and SHA-256.
4. Byte or hex pattern matching for at least one safe mock-virus signature.
5. A small heuristic layer that produces suspicious, not infected, findings.
6. A timestamped report.
7. A demo folder with clean files and a safe mock-virus fixture.
8. A report that explains the data structures honestly.

## Stretch Scope

Only add these after the minimum project works:

- Bloom filter pre-check before hash-map lookup.
- Chunked pattern scanning for large files.
- Multiple report formats such as JSON plus Markdown.
- A small text UI or web UI for demonstration only.
- Performance measurements across larger synthetic folder trees.

## Out Of Scope

- Live malware handling.
- Production antivirus claims.
- Scanning personal home directories or third-party files for the demo.
- Network scanning.
- Exploitation, detonation, or malware reverse engineering beyond safe fixtures.
- Broad UI polish before the scanner core, report, and demo are complete.

## Open Decisions

| Decision | Default recommendation | Owner / status |
| --- | --- | --- |
| Team members | Confirm early, then assign source, report, and demo owners. | Open |
| Language | Python 3 CLI is the current local implementation; team can override only with a strong reason. | Local default chosen; team confirmation open |
| Private repo location | Create private GitHub or GitLab repo and link it from this folder. | Open |
| Project I vs Project II relationship | Ask instructor or E3 whether both briefs are required. | Open |
| Minimum heuristic | Current local implementation uses safe suspicious API-name indicators as suspicious-only findings. | Implemented locally; final acceptance open |

## Completion Gate

Before submission, every row in the requirement matrix should have:

- one implementation artifact
- one evidence artifact
- one report paragraph or table entry

## Current Local Package Snapshot

As of `2026-04-22`, the local course-repo package covers the scanner core, evidence artifacts, and report package. It does not yet satisfy the final private-repo/video or live-demo submission gate.

| Requirement | Prototype state | Evidence |
| --- | --- | --- |
| R1 | Implemented locally | `src/sentinel/scanner.py`, `tests/test_scanner.py` |
| R2 | Implemented locally | `signatures/malware-signatures.json`, `tests/test_signatures.py` |
| R3 | Implemented locally | safe mock-virus fixture detected in `reports/demo-report.json` |
| R4 | Implemented locally | chunked `hex_pattern` matcher in `src/sentinel/signatures.py` and `src/sentinel/matchers.py`; chunk-boundary test in `tests/test_matchers.py` |
| R5 | Implemented locally | `src/sentinel/heuristics.py`, suspicious fixture in demo report |
| R6 | Implemented locally | `src/sentinel/reporting.py`, `reports/demo-report.json`, `reports/demo-report.md`, `reports/demo-evidence-manifest.json` |
| R7 | Pending | private GitHub/GitLab repo not chosen |
| R8 | Drafted and compiled locally | `report/report-draft.md`, `report/final-report.tex`, `report/final-report.pdf` |
| R9 | Locally reproducible; final recording/live demo pending | local demo works, `demo/demo-transcript.md` exists, `demo/run_demo.py` regenerates evidence, and `reports/demo-evidence-manifest.json` captures reproducibility evidence |
