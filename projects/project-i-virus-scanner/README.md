# Project I - Virus Scanner

## Agent Search Summary

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title: `Project I. Virus Scanner`
- Opened: `2026-03-08 00:00`
- Due: `2026-06-07 23:59`
- Team size: `1-4`
- Status: active; Sentinel `v0.2.0` local package, EICAR reference-hash profile, standards-alignment note, Aho-Corasick byte-pattern engine, tests, safe mock demo, benchmark evidence, reports, evidence manifest, demo runner, and compiled report PDF exist; team and private repo still not locked
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

## Current Local Package

The local implementation is a Python 3 command-line scanner under `src/sentinel/`.

Install locally from this project folder:

```bash
python3 -m pip install -e .
```

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Validate signatures:

```bash
PYTHONPATH=src python3 -m sentinel validate-signatures signatures/malware-signatures.json
```

Run the safe local demo:

```bash
PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

Generate the instructor-friendly Markdown report:

```bash
PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.md \
  --format markdown
```

Generate the evidence manifest:

```bash
PYTHONPATH=src python3 -m sentinel write-evidence \
  --target demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --report reports/demo-report.md \
  --report reports/pattern-benchmark.json \
  --report reports/pattern-benchmark.md \
  --output reports/demo-evidence-manifest.json
```

Generate the safe synthetic pattern-matching benchmark:

```bash
PYTHONPATH=src python3 scripts/benchmark_patterns.py
```

Run the full local demo regeneration path:

```bash
python3 demo/run_demo.py
```

Run the release-readiness gate:

```bash
python3 scripts/check_release.py
```

Current observed demo summary: `5` files scanned, `1` infected safe mock fixture, `1` suspicious heuristic fixture, `3` clean files, `0` skipped files, and `0` errors. A detection run returns exit code `1` by design. The current test suite has `22` standard-library tests.

## 2026-04-22 Local Package Checkpoint

- Local implementation: working Python package with `sentinel` console entry point metadata.
- Scanner behavior: explicit target only, read-only, no live malware, no scanned-file execution, no delete/quarantine/upload/network action, and default symbolic-link skipping so a demo scan does not silently leave the target tree.
- Detection coverage: MD5, SHA-256, Aho-Corasick byte-pattern matching with stream/chunk-boundary tests, and heuristic-only suspicious flags.
- Demo evidence: `reports/demo-report.json`, `reports/demo-report.md`, `reports/pattern-benchmark.json`, `reports/pattern-benchmark.md`, `reports/demo-evidence-manifest.json`, and `demo/demo-transcript.md`.
- Report package: `report/final-report.tex` and compiled `report/final-report.pdf`.
- Handoff package: `report/private-repo-handoff.md` records what to move into the required private GitHub/GitLab repository.
- Remaining external decisions: team members, private repo URL, Project I vs Project II requirement relationship, and whether final demo must use literal EICAR.

## 2026-04-22 Algorithmic Hardening Checkpoint

- Version bumped to `0.2.0`.
- Added `VERSION`, `CHANGELOG.md`, `Makefile`, and `scripts/check_release.py` as release-readiness controls.
- Byte-pattern matching now uses an Aho-Corasick-style automaton (`aho-corasick-byte-automaton`) instead of checking each pattern independently.
- The automaton preserves state across streamed chunks, reports the first pattern offset, and records scan-engine metadata in JSON and Markdown reports.
- Tests cover overlapping patterns, stream state across chunks, chunk-boundary detection, version output, report metadata, and the existing scanner/demo behavior.
- `scripts/benchmark_patterns.py` generates safe synthetic benchmark artifacts; current evidence shows match-set equivalence with the naive baseline while noting that CPython's C-backed `bytes` search can be faster at small demo scale.

## 2026-04-22 Traversal Safety Checkpoint

- Scanner traversal now reports symbolic links as `skipped` by default instead of following them.
- JSON and Markdown reports include `symlink_policy: skip` in scan metadata.
- Skipped symbolic links include a `skip_reason` so the demo evidence is explicit and reviewable.
- Tests cover symbolic links inside a scanned directory and a symbolic link passed as the scan target.

## 2026-04-22 Standards Alignment Checkpoint

- Added `docs/standards-alignment.md` to map Sentinel against EICAR, NIST SP 800-83 Rev. 1, NIST Cybersecurity Framework 2.0, OWASP File Upload Cheat Sheet, and MITRE ATT&CK T1055.002.
- Added `signatures/eicar-reference-signature.json` with EICAR reference hashes only; the repository still does not store a literal EICAR test file.
- Added `tests/test_eicar_reference.py` to reconstruct the EICAR reference bytes in memory and verify the standard 68-byte length plus MD5/SHA-256 matches.
- Expanded `scripts/check_release.py` so standards alignment and EICAR reference checks are part of the release gate.

## First Useful Checkpoint

Before implementation, confirm:

- who is on the team
- whether Project I is still required if Project II is also listed
- programming language and private-repo location; default recommendation is a Python 3 CLI unless the team has a better reason
- minimum acceptable heuristic feature
- demo folder shape and safe mock-virus input

## File Map

| Path | Purpose |
| --- | --- |
| `project-spec.pdf` | Official project brief |
| `VERSION` | Single plain-text release version |
| `CHANGELOG.md` | Human-readable release history |
| `Makefile` | Shortcuts for tests, demo, benchmark, report, release-check, and cleanup |
| `pyproject.toml` | Python package metadata and `sentinel` console entry point |
| `README.md` | Local routing, objective, deliverables, and guardrails |
| `docs/standards-alignment.md` | EICAR, NIST, OWASP, and MITRE alignment notes |
| `requirements-traceability.md` | Requirement matrix, acceptance checks, evidence needs, open decisions, and completion gate |
| `technical-design.md` | Sentinel architecture, data structures, CLI, matching rules, report schema, tests, milestones, and team split |
| `demo-and-report-plan.md` | Safe mock-virus demo runbook, evidence checklist, submission package, and final report outline |
| `src/sentinel/` | Local Python 3 scanner package |
| `signatures/malware-signatures.json` | Safe mock-virus signature database |
| `signatures/eicar-reference-signature.json` | EICAR reference hash profile without storing the EICAR file |
| `demo/` | Safe local demo tree and fixture notes |
| `demo/run_demo.py` | Reproducible local demo runner for tests, reports, and evidence manifest |
| `scripts/benchmark_patterns.py` | Safe synthetic benchmark for pattern-matching evidence |
| `scripts/check_release.py` | Release-readiness gate for version, standards alignment, EICAR reference hashes, demo, benchmark, manifest, and PDF consistency |
| `reports/demo-report.json` | Generated demo JSON report |
| `reports/demo-report.md` | Generated instructor-friendly Markdown report |
| `reports/pattern-benchmark.json` | Generated synthetic pattern-matching benchmark |
| `reports/pattern-benchmark.md` | Instructor-readable benchmark summary |
| `reports/demo-evidence-manifest.json` | Reproducibility manifest with demo-tree, signature, and report hashes |
| `tests/` | Standard-library unit tests |
| `report/report-draft.md` | Submission report draft based on the current package |
| `report/final-report.tex` | LaTeX report source |
| `report/final-report.pdf` | Compiled 6-page report PDF |
| `report/submission-checklist.md` | Final packaging checklist and cut rules |
| `report/private-repo-handoff.md` | Files and verification steps for the required private GitHub/GitLab repo |

For final submission, mirror this package into the required private source repository and link the final private repository URL plus commit hash from this README.
