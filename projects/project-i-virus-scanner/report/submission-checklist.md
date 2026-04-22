# Project I Submission Checklist

## Current State

| Area | State | Evidence |
| --- | --- | --- |
| Scanner core | Working locally | `src/sentinel/` |
| Signature database | Working locally | `signatures/malware-signatures.json` |
| Safe demo tree | Working locally | `demo/demo-tree/` |
| JSON report | Generated | `reports/demo-report.json` |
| Markdown report | Generated | `reports/demo-report.md` |
| Evidence manifest | Generated | `reports/demo-evidence-manifest.json` |
| Pattern benchmark | Generated | `reports/pattern-benchmark.json`, `reports/pattern-benchmark.md` |
| Unit tests | Passing locally; includes Aho-Corasick, overlapping-pattern, and chunk-boundary tests | `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v` |
| Report draft | Drafted | `report/report-draft.md` |
| Final report source | Drafted | `report/final-report.tex` |
| Final report PDF | Compiled | `report/final-report.pdf` |
| Demo transcript | Drafted | `demo/demo-transcript.md` |
| Demo runner | Working locally | `python3 demo/run_demo.py` |
| Release check | Passing locally | `python3 scripts/check_release.py` |
| Private repo handoff | Drafted | `report/private-repo-handoff.md` |
| Package metadata | Drafted | `pyproject.toml` |
| Version / changelog | Drafted | `VERSION`, `CHANGELOG.md` |

## Latest Verification Snapshot

- Date: `2026-04-22`
- Command: `python3 demo/run_demo.py`
- Result: `22` tests passed; demo reports, benchmark artifacts, and evidence manifest regenerated.
- Demo summary: `5` files scanned, `1` infected safe mock fixture, `1` suspicious heuristic fixture, `3` clean files, `0` skipped files, `0` errors.
- Algorithm checkpoint: `v0.2.0` uses `aho-corasick-byte-automaton`; current demo report records `1` pattern, `30` automaton states, and `symlink_policy: skip`.
- Standards checkpoint: `docs/standards-alignment.md` maps the project to EICAR, NIST SP 800-83 Rev. 1, NIST Cybersecurity Framework 2.0, OWASP File Upload Cheat Sheet, and MITRE ATT&CK T1055.002; EICAR reference validation uses hashes and in-memory bytes, not a stored EICAR file.
- Benchmark checkpoint: safe synthetic benchmark uses `128` patterns and records equal match sets versus the naive baseline; small-scale runtime is recorded without claiming production performance.
- Release gate: `python3 scripts/check_release.py` passes version, standards-alignment, EICAR reference-hash, demo, benchmark, evidence-manifest, and final-PDF checks.
- Report PDF: `report/final-report.pdf`, `6` pages.

## Before Final Submission

- [ ] Confirm whether Project I is required alongside Project II.
- [ ] Confirm team members.
- [ ] Create or choose the required private GitHub/GitLab repository.
- [ ] Move or mirror the implementation into that private repository.
- [ ] Record the private repository URL in `README.md`.
- [ ] Record the final commit hash used for the demo.
- [ ] Run `python3 -m pip install -e .` in the private repository.
- [ ] Run `python3 scripts/check_release.py` in the private repository.
- [ ] Confirm whether the final demo must use the literal EICAR test file.
- [ ] If EICAR is required, create it only in the controlled final demo environment.
- [ ] Run the full test command from a clean checkout.
- [ ] Confirm the chunked scan / boundary-pattern test still passes after moving to the private repo.
- [ ] Regenerate `reports/demo-report.json`.
- [ ] Regenerate `reports/demo-report.md`.
- [ ] Regenerate `reports/pattern-benchmark.json`.
- [ ] Regenerate `reports/pattern-benchmark.md`.
- [ ] Regenerate `reports/demo-evidence-manifest.json`.
- [ ] Recompile `report/final-report.pdf` after final team/repo/EICAR decisions.
- [ ] Record a short demo video or prepare the live-demo script.
- [ ] Ensure the final report references the same demo command, report files, evidence manifest, and commit hash.
- [ ] Ensure `VERSION`, `pyproject.toml`, `src/sentinel/version.py`, `CHANGELOG.md`, and final report version wording agree.

## Cut Rules

If time is short:

1. Keep the CLI scanner, signature database, JSON/Markdown report, and demo tree.
2. Keep the report explanation of data structures.
3. Cut UI polish first.
4. Cut Bloom filter discussion unless it is explicitly implemented.
5. Cut extra heuristics before cutting tests or demo reproducibility.
