# Project I Requirements Traceability

## Purpose

This file turns the official Virus Scanner brief into implementation-ready requirements.
Use it to decide whether the scanner, report, and demo are complete enough for submission.

## Source Facts

- Course project: `[2026 NS] Project - Virus Scanner`
- Tool name in brief: `Sentinel`
- Due date tracked in planning: `2026-06-07 23:59`
- Team members: `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen)
- Required output: functional signature-based virus scanner, source code, report, and demo
- Safety input: safe mock virus such as the EICAR test file

## Requirement Matrix

| ID | Requirement | Source phase / deliverable | Minimum acceptance check | Evidence to keep |
| --- | --- | --- | --- | --- |
| R1 | Scan a directory tree of files. | Phase II - Scanning Engine | CLI accepts a directory, visits nested regular files deterministically, and reports symbolic links as skipped by default. | Demo command, tree listing, test result |
| R2 | Maintain a structured malware-signature repository. | Phase I - Database Design | JSON or CSV signature database stores at least name, severity, hash type/value, and optional byte or hex pattern. | Signature file, schema note |
| R3 | Compare scanned files against known signatures. | Phase II - Scanning Engine | Known safe mock-virus fixture is detected by exact hash or pattern match. | Unit test, demo report |
| R4 | Implement bitwise or byte-pattern comparison. | Phase II - Scanning Engine | Hex or byte patterns are converted to bytes and searched inside target files with stream-safe matching. | Matcher test, report metadata, benchmark evidence |
| R5 | Add basic heuristic analysis. | Phase III - Heuristic Analysis | At least one documented low-risk heuristic flags a safe suspicious fixture without claiming it is confirmed malware. | Heuristic rules table, sample report row |
| R6 | Generate a security report. | Phase IV - Reporting and UI | Report includes scanned paths, infected or suspicious paths, threat names, severity, match reason, and timestamps. | JSON or Markdown report artifact |
| R7 | Host well-documented source code in a private GitHub or GitLab repository. | Deliverable 1 | Private repo exists, README explains setup/run/test, and final source has no live malware or secrets. | Private repo URL, commit hash |
| R8 | Write a project report explaining data-structure choices. | Deliverable 2 | Report explains the implemented hash map, Bloom filter, and Aho-Corasick structures without production-antivirus claims. | Report source/PDF, screenshot-evidence report copy |
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

- Bloom filter pre-check before hash-map lookup. `Implemented locally in v0.3.0 with exact hash-map verification after the filter.`
- Chunked pattern scanning for large files. `Implemented locally with an Aho-Corasick byte-pattern engine.`
- Multiple report formats such as JSON plus Markdown. `Implemented locally.`
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
| Team members | `513559004` Jsaon Chia-Sheng Lin and `313264012` 陳靖中 (Ching-Chung Chen) are recorded. | Recorded |
| Language | Python 3 CLI is the current local implementation; team can override only with a strong reason. | Local default chosen; team confirmation open |
| Private repo location | Do not move the implementation into a private GitHub/GitLab repository in this pass. | Explicitly deferred by instruction |
| Minimum heuristic | Current local implementation uses safe suspicious API-name indicators as suspicious-only findings. | Implemented locally; final acceptance open |

## Completion Gate

Before submission, every row in the requirement matrix should have:

- one implementation artifact
- one evidence artifact
- one report paragraph or table entry

## Current Local Package Snapshot

As of `2026-04-22`, the local course-repo package covers the scanner core, evidence artifacts, report package, export package, and live-demo script. The private-repo move is intentionally not performed in this pass.

| Requirement | Prototype state | Evidence |
| --- | --- | --- |
| R1 | Implemented locally | `src/sentinel/scanner.py`, `tests/test_scanner.py`; symlink-skip tests cover links inside the target tree and a symlink target path |
| R2 | Implemented locally | `signatures/malware-signatures.json`, `signatures/eicar-reference-signature.json`, `tests/test_signatures.py` |
| R3 | Implemented locally | safe mock-virus fixture detected in `reports/demo-report.json`; Bloom-filter hash pre-check plus exact hash-map verification tested in `tests/test_matchers.py`; EICAR reference hashes validated in memory by `tests/test_eicar_reference.py` |
| R4 | Implemented locally | Aho-Corasick `hex_pattern` matcher in `src/sentinel/matchers.py`; overlapping-pattern, stream-boundary, and chunk-boundary tests in `tests/test_matchers.py`; benchmark artifacts in `reports/pattern-benchmark.*` |
| R5 | Implemented locally | `src/sentinel/heuristics.py`, suspicious fixture in demo report |
| R6 | Implemented locally | `src/sentinel/reporting.py`, scan metadata in reports, `reports/demo-report.json`, `reports/demo-report.md`, `reports/demo-evidence-manifest.json` |
| R7 | Export package implemented; private remote not moved by instruction | `scripts/export_private_repo.py`, `report/submission-package.md`; private repository URL recorded as not created/moved in this pass |
| R8 | Drafted and compiled locally | `report/final-report.tex`, `report/final-report.pdf` |
| R9 | Live-demo script prepared | local demo works, `demo/runbook.md` and `demo/demo-transcript.md` exist, `demo/run_demo.py` regenerates evidence, and `reports/demo-evidence-manifest.json` captures reproducibility evidence |

## Release-Readiness Gate

`scripts/check_release.py` is the local submission-candidate gate. It checks:

- `VERSION`, `pyproject.toml`, `src/sentinel/version.py`, and `sentinel --version` agree on `0.4.0`
- `docs/standards-alignment.md` and EICAR reference hashes are present
- the full demo regeneration path passes
- the JSON report has the expected safe-demo summary, Bloom-filter metadata, Aho-Corasick metadata, and `symlink_policy: skip`
- the safe synthetic benchmark has equal match sets versus the naive baseline
- the evidence manifest has safe flags and the expected report artifacts
- the private-repo export dry-run includes the curated package and excludes the official brief, LaTeX build artifacts, removed draft, and literal EICAR files
- `report/final-report.pdf` exists and has at least `5` pages when `pdfinfo` is available; the current compiled report is `6` pages
