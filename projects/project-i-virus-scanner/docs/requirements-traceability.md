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
- Safety input: official EICAR safe anti-malware test file generated for the demo

## Requirement Matrix

| ID | Requirement | Source phase / deliverable | Minimum acceptance check | Evidence to keep |
| --- | --- | --- | --- | --- |
| R1 | Scan a directory tree of files. | Phase II - Scanning Engine | CLI accepts a directory, visits nested regular files deterministically, and reports symbolic links as skipped by default. | Demo command, tree listing, test result |
| R2 | Maintain a structured malware-signature repository. | Phase I - Database Design | JSON or CSV signature database stores at least name, severity, hash type/value, and byte or hex pattern evidence. | Signature file, schema note |
| R3 | Compare scanned files against known signatures. | Phase II - Scanning Engine | The generated official EICAR safe test file is detected by exact hash or pattern match. | Unit test, demo report |
| R4 | Implement bitwise or byte-pattern comparison. | Phase II - Scanning Engine | Hex or byte patterns are converted to bytes and searched inside target files with stream-safe matching. | Matcher test and report metadata |
| R5 | Add basic heuristic analysis. | Phase III - Heuristic Analysis | At least one documented low-risk heuristic flags a safe suspicious fixture without claiming it is confirmed malware. | Heuristic rules table, sample report row |
| R6 | Generate a security report. | Phase IV - Reporting and UI | Report includes scanned paths, infected or suspicious paths, threat names, severity, match reason, and timestamps. | JSON or Markdown report artifact |
| R7 | Host well-documented source code in a private GitHub or GitLab repository. | Deliverable 1 | Private repo exists, README explains setup/run/test, and final source has no live malware or secrets. | Private repo URL, commit hash |
| R8 | Write a project report explaining data-structure choices. | Deliverable 2 | Report explains the implemented hash map, Bloom filter, and Aho-Corasick structures without production-antivirus claims. | Report source/PDF |
| R9 | Demonstrate detection inside a complex folder structure. | Deliverable 3 | Demo tree contains clean files plus a nested generated EICAR safe test file; scanner finds EICAR and leaves clean files clean. | Video or live-demo script, demo report |

## Minimal Valid Scope

The minimum project that satisfies the brief is:

1. A command-line scanner.
2. A JSON or CSV signature database.
3. Exact hash matching using MD5 and SHA-256.
4. Byte or hex pattern matching for the EICAR safe test signature.
5. A small heuristic layer that produces suspicious, not infected, findings.
6. A timestamped report.
7. A demo folder with clean files and a generated EICAR safe test fixture.
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
- Exploitation, detonation, or malware reverse engineering beyond the EICAR safe test fixture and benign local fixtures.
- Broad UI polish before the scanner core, report, and demo are complete.

## Open Decisions

| Decision | Default recommendation | Owner / status |
| --- | --- | --- |
| Team members | `513559004` Jsaon Chia-Sheng Lin and `313264012` 陳靖中 (Ching-Chung Chen) are recorded. | Recorded |
| Language | Rust CLI is the current submission implementation. | Rust path chosen |
| Private repo location | LMS PDF submission is complete; keep the source package ready if the instructor asks for private-repo URL verification later. | Follow-up only if requested |
| Minimum heuristic | Current local implementation uses safe suspicious API-name indicators as suspicious-only findings. | Implemented locally; final acceptance open |

## Completion Gate

Before submission, every row in the requirement matrix should have:

- one implementation artifact
- one evidence artifact
- one report paragraph or table entry

## Current Local Package Snapshot

As of `2026-04-22`, the local course-repo package covers the scanner core, evidence artifacts, report package, export package, and live-demo script. LMS shows `Submitted for grading` with `final-report-513559004-313264012.pdf` uploaded at `2026-04-22 17:30`; private-repo mirroring remains a follow-up only if requested.

| Requirement | Prototype state | Evidence |
| --- | --- | --- |
| R1 | Implemented locally | `rust/src/scanner.rs`, `cargo test`; symlink-skip policy is recorded in Rust scan metadata |
| R2 | Implemented locally | `signatures/malware-signatures.json`, `signatures/eicar-reference-signature.json`, `rust/src/signatures.rs` |
| R3 | Implemented locally | generated EICAR safe test file detected in `reports/demo-report.json`; Bloom-filter hash pre-check plus exact hash-map verification implemented in `rust/src/bloom.rs` and `rust/src/scanner.rs` |
| R4 | Implemented locally | Aho-Corasick `hex_pattern` matcher in `rust/src/patterns.rs`; stream-boundary tests in `cargo test` |
| R5 | Implemented locally | heuristic rules in `rust/src/scanner.rs`, suspicious fixture in Rust demo report |
| R6 | Implemented locally | `rust/src/reporting.rs`, scan metadata in `reports/demo-report.json` and `reports/demo-report.md`, reproducibility evidence in `reports/demo-evidence-manifest.json` |
| R7 | Export package implemented; private remote follow-up only if requested | `scripts/export_private_repo.py`, `report/submission-package.md`; LMS submission completed without a private URL field shown in the captured submission screen |
| R8 | Drafted, compiled, and submitted to LMS | `report/final-report.tex`, `report/final-report.pdf`, `report/final-report-513559004-313264012.pdf` |
| R9 | Live-demo script prepared | local Rust demo works, `demo/runbook.md` and `demo/demo-transcript.md` exist, and `reports/demo-report.*` captures scan evidence |

The Rust implementation now builds, passes its test suite, passes Clippy, and
matches the safe demo summary through `cargo run -- verify-demo`.

## Release-Readiness Gate

The Rust submission-candidate gate is:

```bash
cd rust
cargo fmt --check
cargo test
cargo clippy --all-targets -- -D warnings
cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json
cargo run -- verify-demo \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json
cargo run -- scan \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --json ../reports/demo-report.json \
  --markdown ../reports/demo-report.md
cargo run -- write-evidence \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --report ../reports/demo-report.json \
  --report ../reports/demo-report.md \
  --output ../reports/demo-evidence-manifest.json
```

It checks:

- Rust formatting, tests, and linting
- JSON signature loading and validation
- the expected safe-demo summary
- Bloom-filter metadata, Aho-Corasick metadata, heuristic-rule metadata, and
  `symlink_policy: skip`
- generated Rust JSON, Markdown, and evidence-manifest artifacts
- compiled Rust report PDF under `report/`
