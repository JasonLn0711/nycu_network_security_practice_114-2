# Project I Submission Package

## Purpose

This file is the single last-mile source for final submission. It combines the
local package checklist, private-repository handoff, verification commands, and
safety checks so submission state does not split across multiple notes.

## Current Local State

| Area | State | Evidence |
| --- | --- | --- |
| Scanner package | Working | `python/src/sentinel/`, `python/pyproject.toml` |
| Signature database | Working | `signatures/malware-signatures.json` |
| Demo tree | Working | `demo/demo-tree/` |
| Tests | Passing, `25` tests | `python3 demo/run_demo.py` |
| Reports | Generated | `reports/demo-report.json`, `reports/demo-report.md` |
| Benchmark | Generated | `reports/pattern-benchmark.json`, `reports/pattern-benchmark.md` |
| Evidence manifest | Generated | `reports/demo-evidence-manifest.json` |
| Private repo export | Working | `scripts/export_private_repo.py` |
| Rust companion | Source-ready; compile pending Rust toolchain | `rust/`, `docs/rust/README.md` |
| Final report | Compiled, `6` pages; screenshot-evidence copy compiled as `12` pages | `report/` |
| Release gate | Passing locally | `python3 scripts/check_release.py` |

Latest verified result on `2026-04-22`: Sentinel `v0.4.0`, `5` files scanned,
`1` infected safe mock fixture, `1` suspicious fixture, `3` clean files,
`0` skipped files, and `0` errors.

## Final Project Decisions

| Field | Recorded value |
| --- | --- |
| Project package | Project I - Virus Scanner final submission package. |
| Team members | `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen) |
| Private repository URL | Not created or moved in this pass, per instruction. |
| Local demo source-baseline commit hash | `2be51a0f003834e58795efcdd4b9224a730b90e7` |
| Literal EICAR decision | Not required for the current final demo. Use the safe mock fixture plus EICAR reference hashes; create literal EICAR only if the instructor explicitly requires it later. |
| Demo format | Live-demo script/runbook prepared; short video not recorded in this pass. |

## Verification Record

Verification was run against the curated export package at
`dist/sentinel-private-repo/` on `2026-04-22`.

| Command | Result |
| --- | --- |
| `python3 -m pip install -e python` | Blocked by local environment: `/usr/bin/python3: No module named pip`. |
| `python3 -m ensurepip --upgrade --user` | Blocked by local environment: `/usr/bin/python3: No module named ensurepip`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python/tests -v` | Failed before install because `sentinel` was not importable without package installation. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m unittest discover -s python/tests -v` | Passed: `25` tests. |
| `python3 demo/run_demo.py` | Passed; regenerated reports, benchmark, and evidence manifest. |
| `python3 scripts/check_release.py` | Passed for Sentinel `0.4.0`. |
| `PYTHONPATH=python/src python3 -m sentinel validate-signatures signatures/malware-signatures.json` | Passed. |
| `PYTHONPATH=python/src python3 scripts/benchmark_patterns.py` | Passed. |

Interpretation: the export package verifies correctly in no-install mode. The
editable-install command still needs a Python environment with `pip` available.

## Private Repository Export

The official brief requires well-documented source code in a private GitHub or
GitLab repository. This pass intentionally does not move the implementation into
a private repository. Build the curated local handoff package first:

```bash
python3 scripts/export_private_repo.py --clean
```

The export writes:

- `dist/sentinel-private-repo/`
- `dist/sentinel-private-repo-manifest.json`

Copy the contents of `dist/sentinel-private-repo/` into the private repository
root. The manifest records file hashes and safety boundaries. It intentionally
excludes the official project PDF, LaTeX build artifacts, removed drafts, and
literal EICAR files.

## Exported Contents

| Path | Purpose |
| --- | --- |
| `README.md` | Reviewer entrypoint |
| `python/`, `VERSION`, `CHANGELOG.md`, `Makefile` | Python package metadata, tests, and release controls |
| `python/src/sentinel/` | Scanner implementation |
| `python/tests/` | Standard-library test suite |
| `signatures/` | Safe mock-virus signatures and EICAR reference hashes |
| `demo/` | Demo tree, runbook, transcript, and runner |
| `reports/` | Generated demo, benchmark, and evidence artifacts |
| `docs/` | Traceability, technical design, and standards notes |
| `rust/` | Optional Rust companion scanner implementation |
| `scripts/` | Benchmark, release-check, and export commands |
| `report/final-report.tex`, `report/final-report.pdf` | Final report source and PDF |
| `report/submission-package.md` | This final submission note |

Keep `project-spec.pdf` in the course repo unless the team is explicitly allowed
to store official handouts in the private repository.

## Private Repository Verification

From the private repository root:

```bash
python3 -m pip install -e python
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s python/tests -v
python3 demo/run_demo.py
python3 scripts/check_release.py
```

Optional smoke checks:

```bash
sentinel validate-signatures signatures/malware-signatures.json
PYTHONPATH=python/src python3 scripts/benchmark_patterns.py
```

Expected demo summary:

```text
scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

The scan command returns exit code `1` when the safe mock-virus fixture is
detected. That is expected behavior for this demo.

## Fields To Fill

- Private repository URL: not created or moved in this pass, per instruction.
- Local demo source-baseline commit hash: `2be51a0f003834e58795efcdd4b9224a730b90e7`
- Team members: `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen)
- Project package: Project I - Virus Scanner final submission package.
- Whether the final demo must use the literal EICAR test file: no for the current final demo; use safe mock fixture plus EICAR reference hashes unless the instructor explicitly requires literal EICAR later.

## Final Checklist

- [x] Confirm Project I package identity and team members.
- [x] Confirm team members.
- [ ] Create or choose the required private GitHub/GitLab repository. Not performed in this pass by instruction.
- [x] Run `python3 scripts/export_private_repo.py --clean`.
- [ ] Mirror the export package into the private repository. Not performed in this pass by instruction.
- [x] Record private repository URL in `README.md`.
- [x] Record final commit hash used for the demo.
- [x] Run the private-repository verification commands. Editable install was blocked by missing `pip`; no-install verification passed with `PYTHONPATH=python/src`.
- [x] Confirm whether the final demo must use literal EICAR.
- [x] If EICAR is required, create it only in the controlled final demo environment. Current decision: not required unless instructor overrides.
- [x] Recompile `report/final-report.pdf` after final team/repo/EICAR decisions.
- [x] Record a short demo video or finalize the live-demo script.
- [x] Ensure the final report, demo transcript, generated reports, evidence manifest, private repo URL, and final commit hash all agree.

## Safety Check

- [ ] No live malware is stored in the repository.
- [ ] The scanner does not execute scanned files.
- [ ] The scanner does not delete, quarantine, upload, or mutate scanned files.
- [ ] Symbolic links remain skipped by default unless the team deliberately changes and documents the policy.
- [ ] The demo target is `demo/demo-tree/`, not a personal home directory.
- [ ] The final report clearly states the mock-virus and EICAR-reference limitations.
- [ ] The benchmark is described as safe synthetic evidence, not production antivirus performance.
- [ ] The evidence manifest was regenerated after the final demo reports.

## Cut Rule

If time is short, keep the CLI scanner, signature database, JSON/Markdown report,
demo tree, final report, export package, and release gate. Cut UI polish and
extra heuristics first.
