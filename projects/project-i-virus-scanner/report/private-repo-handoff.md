# Private Repository Handoff

## Purpose

The official project brief requires well-documented source code hosted in a private GitHub or GitLab repository. This handoff note records what should move into that private repository and how to verify it after transfer.

## Recommended Repository Contents

Copy these paths into the private source repository:

| Path | Reason |
| --- | --- |
| `VERSION` | Plain-text release version |
| `CHANGELOG.md` | Release history for reviewer/team handoff |
| `Makefile` | Shortcuts for verification and cleanup |
| `pyproject.toml` | Python package metadata and `sentinel` console entry point |
| `README.md` | Setup, run, demo, and routing instructions |
| `docs/standards-alignment.md` | EICAR, NIST, OWASP, and MITRE alignment notes |
| `src/sentinel/` | Scanner implementation |
| `tests/` | Standard-library test suite |
| `signatures/malware-signatures.json` | Safe mock-virus signature database |
| `signatures/eicar-reference-signature.json` | EICAR reference hash profile without storing an EICAR file |
| `demo/` | Safe demo tree, transcript, and demo runner |
| `reports/demo-report.json` | Machine-readable demo report |
| `reports/demo-report.md` | Instructor-friendly demo report |
| `reports/pattern-benchmark.json` | Safe synthetic benchmark evidence |
| `reports/pattern-benchmark.md` | Instructor-friendly benchmark summary |
| `reports/demo-evidence-manifest.json` | Reproducibility hashes and commands |
| `scripts/benchmark_patterns.py` | Benchmark regeneration command |
| `scripts/check_release.py` | Final local release-readiness gate |
| `report/final-report.tex` | Final report source |
| `report/final-report.pdf` | Compiled final report |
| `report/submission-checklist.md` | Last-mile submission checklist |

Keep `project-spec.pdf` in the course repo unless the team is allowed to store official handouts in the private repository.

## Local Verification After Transfer

From the private repository root:

```bash
python3 -m pip install -e .
```

Run the tests:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Run the full demo:

```bash
python3 demo/run_demo.py
```

Run the release-readiness gate:

```bash
python3 scripts/check_release.py
```

Optional installed-command smoke test:

```bash
sentinel validate-signatures signatures/malware-signatures.json
```

Optional benchmark regeneration:

```bash
PYTHONPATH=src python3 scripts/benchmark_patterns.py
```

Expected demo result:

```text
scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

The scan command should return exit code `1` when the safe mock-virus fixture is detected. That is expected behavior, not a failure.

## Final Fields To Fill

- Private repository URL:
- Final demo commit hash:
- Team members:
- Whether Project I is required alongside Project II:
- Whether the final demo must use the literal EICAR test file:

## Safety Check Before Submission

- [ ] No live malware is stored in the repository.
- [ ] The scanner does not execute scanned files.
- [ ] The scanner does not delete, quarantine, upload, or mutate scanned files.
- [ ] Symbolic links remain skipped by default unless the team deliberately changes and documents the policy.
- [ ] The demo target is `demo/demo-tree/`, not a personal home directory.
- [ ] The final report clearly states the mock-virus and EICAR-reference limitations.
- [ ] The benchmark is described as safe synthetic evidence, not production antivirus performance.
- [ ] The evidence manifest was regenerated after the final demo reports.
