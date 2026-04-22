# Project I - Virus Scanner

## Snapshot

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title: `Project I. Virus Scanner`
- Due: `2026-06-07 23:59`
- Official brief: `project-spec.pdf`
- Planning locator: `../../../planning-everything-track/data/projects/2026-06-network-security-virus-scanner.md`
- Current local package: Sentinel `v0.4.0`
- Status: scanner, tests, demo evidence, report source/PDF, export package, and live-demo script are working locally; team identity is recorded; private repo move is intentionally not performed in this pass.
- Team: `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen)
- Private repository URL: not created or moved in this pass, per instruction.
- Final local demo commit hash: `2be51a0f003834e58795efcdd4b9224a730b90e7`

## Deliverables

| Deliverable | Local state | Source of truth |
| --- | --- | --- |
| Source code | Python 3 CLI package under `src/sentinel/` | `src/sentinel/`, `pyproject.toml` |
| Signature database | Safe JSON signatures with MD5, SHA-256, and hex-pattern matchers | `signatures/malware-signatures.json` |
| Report | LaTeX source, compiled PDF, and screenshot-evidence copy | `report/final-report.tex`, `report/final-report.pdf`, `report/final-report-v2.tex`, `report/final-report-v2.pdf` |
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

## Final Submission State

- Private GitHub/GitLab move: not performed in this pass by instruction.
- Literal EICAR: not required for the current final demo; use the safe mock fixture plus EICAR reference hashes unless the instructor explicitly requires literal EICAR later.
- Demo format: live-demo script/runbook prepared; short video not recorded in this pass.
- Export verification: `dist/sentinel-private-repo/` passed no-install verification with `PYTHONPATH=src`; editable install was blocked on this machine because `/usr/bin/python3` has no `pip` or `ensurepip`.
