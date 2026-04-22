# Project I - Virus Scanner

## Snapshot

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Project title: `Project I. Virus Scanner`
- Due: `2026-06-07 23:59`
- Official brief: `project-spec.pdf`
- Planning locator: `../../../planning-everything-track/data/projects/2026-06-network-security-virus-scanner.md`
- Current local package: Sentinel `v0.4.0`
- Status: LMS submission uploaded and marked `Submitted for grading`; scanner, tests, demo evidence, report source/PDF, export package, and live-demo script are working locally.
- Team: `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen)
- LMS submission: `final-report-513559004-313264012.pdf`, last modified `Wednesday, 22 April 2026, 5:30 PM`; grading status `Not graded`.
- Private repository URL: not created or moved in this pass; keep source package ready if the instructor requests it after LMS submission.
- Pre-commit local source-baseline observed before packaging commits: `fd945f850bca755bc3fe4ae90584c72a5fe443f9`

## Deliverables

| Deliverable | Local state | Source of truth |
| --- | --- | --- |
| Source code | Rust scanner implementation; builds and tests locally | `rust/`, `docs/rust/README.md` |
| Signature database | Safe JSON signatures with MD5, SHA-256, and hex-pattern matchers | `signatures/malware-signatures.json` |
| Report | Canonical LaTeX source/PDF for the Rust submission | `report/final-report.tex`, `report/final-report.pdf` |
| Demo evidence | Rust JSON/Markdown scan reports, Rust evidence manifest, and screenshots | `reports/demo-report.*`, `reports/demo-evidence-manifest.json`, `report/evidence-screenshots/` |
| Submission gate | Rust verification passes | `make rust-verify`, `cargo run -- verify-demo ...` |
| Private repo export | Curated handoff package and manifest, generated only when needed | `scripts/export_private_repo.py`, `dist/sentinel-private-repo/` |
| Submission package | Final checklist plus private repo handoff | `report/submission-package.md` |

## Current Implementation

Sentinel is intentionally safe and read-only. It scans only the explicit target path, does not execute scanned files, does not delete/quarantine/upload files, does not use live malware, and skips symbolic links by default.

Implemented detection and evidence paths:

- MD5 and SHA-256 exact signature matching.
- Bloom-filter hash pre-check followed by exact hash-map verification.
- Aho-Corasick byte-pattern matching with streamed chunk state.
- Heuristic-only suspicious findings for weak signals.
- JSON and Markdown reports with scan metadata.
- Rust `verify-demo` gate for the expected Project I demo summary.
- Rust `write-evidence` command for reproducibility hashes and safety flags.
- Rust `prepare-eicar-demo` command that materializes the official 68-byte
  EICAR safe anti-malware test file in the nested demo tree before scanning.
- Private-repository export dry-run and local package builder.
- Git history preserves the older Python prototype; the live working tree now keeps only the Rust submission path.

Rust implementation path:

- `rust/` implements the scanner design in Rust with JSON signatures, MD5/SHA-256 matching, Bloom-filter pre-checks, Aho-Corasick byte-pattern matching, heuristic-only suspicious findings, and JSON/Markdown reports.
- The Rust path now builds with `rustc 1.95.0` / `cargo 1.95.0`, passes `cargo fmt --check`, passes `cargo test` with `13` tests, passes `cargo clippy --all-targets -- -D warnings`, matches the demo summary through `cargo run -- verify-demo`, and writes the Rust evidence manifest through `cargo run -- write-evidence`.
- The Rust heuristic layer includes process-injection API names, executable-magic/file-extension mismatch, and high-entropy byte-sample rules.

Current verified Rust demo result: `5` files scanned, `1` infected EICAR safe test file, `1` suspicious heuristic fixture, `3` clean files, `0` skipped files, and `0` errors.

## Commands

Run the Rust verification gate:

```bash
make rust-verify
```

Regenerate demo artifacts:

```bash
make rust-evidence
```

Run the Rust checks:

```bash
make rust-verify
make rust-test
make rust-lint
```

Run the Rust scanner manually:

```bash
cd rust
cargo run -- prepare-eicar-demo --target ../demo/demo-tree
cargo run -- scan \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --json ../reports/demo-report.json \
  --markdown ../reports/demo-report.md
```

The scan command returns exit code `1` when the generated EICAR safe test file
is detected. That is expected for the demo.

## File Routing

| Need | File |
| --- | --- |
| Requirement coverage | `docs/requirements-traceability.md` |
| Rust architecture and data structures | `docs/rust/README.md` |
| Demo runbook | `demo/runbook.md` |
| Terminal/live-demo transcript | `demo/demo-transcript.md` |
| External standards notes | `docs/standards-alignment.md` |
| Final report source | `report/final-report.tex` |
| Final report PDF | `report/final-report.pdf` |
| Submission package and private repo handoff | `report/submission-package.md` |
| Private repo export tool | `scripts/export_private_repo.py` |
| Release history | `CHANGELOG.md` |

## Final Submission State

- LMS submission: completed on `2026-04-22 17:30`, status `Submitted for grading`, file `final-report-513559004-313264012.pdf`, submitted `46 days 6 hours` early.
- Private GitHub/GitLab move: not performed in this pass; treat as a follow-up only if the instructor requests source URL verification after grading starts.
- EICAR demo: required for the final demo. The literal EICAR file is generated
  by the Rust `prepare-eicar-demo` command at demo time, scanned by Sentinel,
  and excluded from Git/private-repo export to avoid antivirus quarantine and
  repository hygiene problems.
- Demo format: live-demo script/runbook prepared; short video not recorded in this pass.
- Export verification: run `make private-export` when the handoff package is needed. The generated `dist/` folder is ignored and not part of the canonical course archive.
