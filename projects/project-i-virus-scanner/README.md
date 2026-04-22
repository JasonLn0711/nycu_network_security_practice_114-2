# Project I - Virus Scanner

## Snapshot

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title: `Project I. Virus Scanner`
- Due: `2026-06-07 23:59`
- Official brief: `project-spec.pdf`
- Planning locator: `../../../planning-everything-track/data/projects/2026-06-network-security-virus-scanner.md`
- Current local package: Sentinel `v0.4.0`
- Status: scanner, tests, demo evidence, report source/PDF, and submission package are working locally; team, private repo, Project I/II relationship, and final demo format remain open.

## Deliverables

| Deliverable | Local state | Source of truth |
| --- | --- | --- |
| Source code | Python 3 CLI package under `src/sentinel/` | `src/sentinel/`, `pyproject.toml` |
| Signature database | Safe JSON signatures with MD5, SHA-256, and hex-pattern matchers | `signatures/malware-signatures.json` |
| Report | LaTeX source and compiled PDF | `report/final-report.tex`, `report/final-report.pdf` |
| Demo evidence | Regenerated JSON/Markdown reports, benchmark, and manifest | `reports/`, `demo/demo-transcript.md` |
| Submission gate | Local release check passes | `scripts/check_release.py` |
| Private repo export | Curated handoff package and manifest | `scripts/export_private_repo.py`, `dist/sentinel-private-repo/` |
| Submission package | Final checklist plus private repo handoff | `report/submission-package.md` |

## Current Implementation

Sentinel is intentionally safe and read-only. It scans only the explicit target path, does not execute scanned files, does not delete/quarantine/upload files, does not use live malware, and skips symbolic links by default.

Implemented detection and evidence paths:

- MD5 and SHA-256 exact signature matching.
- Bloom-filter hash pre-check followed by exact hash-map verification.
- Aho-Corasick byte-pattern matching with streamed chunk state.
- Heuristic-only suspicious findings for weak signals.
- JSON and Markdown reports with scan metadata.
- Safe synthetic pattern benchmark.
- Evidence manifest with file/report hashes and safety flags.
- Private-repository export dry-run and local package builder.

Current verified demo result: `5` files scanned, `1` infected safe mock fixture, `1` suspicious heuristic fixture, `3` clean files, `0` skipped files, and `0` errors. The test suite currently has `25` standard-library tests.

## Commands

Run the full local release gate:

```bash
python3 scripts/check_release.py
```

Regenerate demo artifacts:

```bash
python3 demo/run_demo.py
```

Build the private-repo export package:

```bash
python3 scripts/export_private_repo.py --clean
```

Run the scanner manually:

```bash
PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

The scan command returns exit code `1` when the safe mock-virus fixture is detected. That is expected for the demo.

## File Routing

| Need | File |
| --- | --- |
| Requirement coverage | `docs/requirements-traceability.md` |
| Architecture and data structures | `docs/technical-design.md` |
| Demo runbook | `demo/runbook.md` |
| Terminal/live-demo transcript | `demo/demo-transcript.md` |
| External standards notes | `docs/standards-alignment.md` |
| Final report source | `report/final-report.tex` |
| Final report PDF | `report/final-report.pdf` |
| Submission package and private repo handoff | `report/submission-package.md` |
| Private repo export tool | `scripts/export_private_repo.py` |
| Release history | `CHANGELOG.md` |

## Remaining Decisions

- Confirm whether Project I is required alongside Project II.
- Confirm team members and final ownership split.
- Create or choose the required private GitHub/GitLab repository and copy the export package into it.
- Record final private repo URL and commit hash.
- Confirm whether the final demo must use the literal EICAR test file.
- Record a short demo video or prepare the live-demo script.
