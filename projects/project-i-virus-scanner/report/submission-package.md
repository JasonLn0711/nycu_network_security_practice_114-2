# Project I Submission Package

## Purpose

This file is the last-mile source for the Rust Project I submission. It records
the package checklist, private-repository handoff status, verification commands,
and safety checks so the final state is easy to review.

## Current Local State

| Area | State | Evidence |
| --- | --- | --- |
| Scanner package | Working Rust CLI | `rust/`, `rust/Cargo.toml`, `rust/Cargo.lock` |
| Signature database | Working | `signatures/malware-signatures.json` |
| Demo tree | Working | `demo/demo-tree/` |
| Tests | Passing, `13` Rust tests | `cd rust && cargo test` |
| Reports | Generated | `reports/demo-report.json`, `reports/demo-report.md` |
| Evidence manifest | Generated | `reports/demo-evidence-manifest.json` |
| Rust verification | Passing | `cd rust && cargo run -- verify-demo ...` |
| Final report | Compiled canonical Rust report | `report/final-report.pdf` |
| Demo script | Prepared | `demo/runbook.md`, `demo/demo-transcript.md` |

Latest verified Rust result on `2026-04-22`: Sentinel `v0.4.0`, `5` files
scanned, `1` infected generated EICAR safe test file, `1` suspicious fixture,
`3` clean files, `0` skipped files, and `0` errors.

## Final Project Decisions

| Field | Recorded value |
| --- | --- |
| Project package | Project I - Virus Scanner final submission package. |
| Team members | `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中 (Ching-Chung Chen) |
| LMS submission status | `Submitted for grading`; grading status `Not graded`. |
| LMS submission file | `final-report-513559004-313264012.pdf`, last modified `Wednesday, 22 April 2026, 5:30 PM`; submitted `46 days 6 hours` early. |
| Private repository URL | Not created or moved in this pass; keep source package ready if the instructor requests it after LMS submission. |
| Pre-commit local source-baseline observed before packaging commits | `fd945f850bca755bc3fe4ae90584c72a5fe443f9` |
| EICAR demo decision | Required for the final demo. The Rust `prepare-eicar-demo` command generates the official 68-byte EICAR safe anti-malware test file at demo time; the generated file is not committed or exported. |
| Demo format | Live-demo script/runbook prepared; short video not recorded in this pass. |

## Verification Record

| Command | Result |
| --- | --- |
| `cd rust && cargo fmt --check` | Passed. |
| `cd rust && cargo test` | Passed: `13` tests. |
| `cd rust && cargo clippy --all-targets -- -D warnings` | Passed. |
| `cd rust && cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json` | Passed with schema `1.0`, `1` signature, `2` hash matchers, and `1` pattern. |
| `cd rust && cargo run -- verify-demo --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json` | Passed with summary `scanned=5 infected=1 suspicious=1 clean=3 skipped=0 errors=0`. |
| `cd rust && cargo run -- scan --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json --json ../reports/demo-report.json --markdown ../reports/demo-report.md` | Passed with expected detection exit code `1` and regenerated Rust reports. |
| `cd rust && cargo run -- write-evidence --target ../demo/demo-tree --signatures ../signatures/malware-signatures.json --report ../reports/demo-report.json --report ../reports/demo-report.md --output ../reports/demo-evidence-manifest.json` | Passed; regenerated the Rust evidence manifest. |
| `cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error final-report.tex` | Passed; compiled `report/final-report.pdf`. |

## Private Repository Handoff

The LMS submission is complete with the compiled report PDF. The official brief
also mentions well-documented source code in a private GitHub or GitLab
repository, so keep this Rust source package ready if the instructor requests
source URL verification after grading starts. For handoff, include these Rust
submission artifacts:

| Path | Purpose |
| --- | --- |
| `README.md` | Reviewer entrypoint. |
| `rust/` | Rust scanner implementation and Cargo lockfile. |
| `signatures/` | EICAR demo signatures and EICAR reference hashes. |
| `demo/` | Demo tree, runbook, and transcript. |
| `reports/demo-report.json` | Machine-readable Rust scan evidence. |
| `reports/demo-report.md` | Instructor-friendly Rust scan evidence. |
| `reports/demo-evidence-manifest.json` | Rust-generated hashes, safety flags, and reproduction commands. |
| `docs/rust/README.md` | Rust architecture and verification notes. |
| `docs/requirements-traceability.md` | Mapping from official requirements to artifacts. |
| `docs/standards-alignment.md` | Safety and standards calibration. |
| `report/final-report.tex`, `report/final-report.pdf` | Canonical report source and PDF. |
| `report/evidence-screenshots/` | Rust command, validation, scan, report, and package screenshots. |
| `report/submission-package.md` | This final submission note. |

Keep `project-spec.pdf` in the course repo unless the team is explicitly allowed
to store official handouts in the private repository.

## Private Repository Verification

From the private repository root:

```bash
cd rust
cargo fmt --check
cargo test
cargo clippy --all-targets -- -D warnings
cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json
cargo run -- prepare-eicar-demo --target ../demo/demo-tree
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

Expected demo summary:

```text
scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

The scan command returns exit code `1` when the generated EICAR safe test file
is detected. That is expected behavior for this demo.

## Final Checklist

- [x] Confirm Project I package identity and team members.
- [x] Confirm team members.
- [x] Upload `final-report-513559004-313264012.pdf` to LMS.
- [x] Confirm LMS status is `Submitted for grading`.
- [ ] Create or choose the private GitHub/GitLab repository only if the
  instructor requests source URL verification after LMS submission.
- [ ] Mirror the Rust submission artifacts into the private repository only if
  requested after LMS submission.
- [x] Record private repository URL state in `README.md`.
- [x] Record final commit hash used for the demo.
- [x] Run Rust formatting, tests, linting, signature validation, demo
  verification, demo scan, and Rust evidence-manifest generation.
- [x] Confirm whether the final demo must use EICAR.
- [x] Generate the EICAR safe test file with Rust at demo time and exclude the
  generated literal file from Git/private-repo export.
- [x] Recompile the Rust report.
- [x] Finalize the live-demo script.
- [x] Ensure the Rust report, demo transcript, generated Rust reports, private
  repo URL state, and final commit hash all agree.

## Safety Check

- [x] No live malware is stored in the repository.
- [x] The scanner does not execute scanned files.
- [x] The scanner does not delete, quarantine, upload, or mutate scanned files.
- [x] Symbolic links remain skipped by default unless the team deliberately
  changes and documents the policy.
- [x] The demo target is `demo/demo-tree/`, not a personal home directory.
- [x] The final report clearly states that the demo generates and detects the
  official EICAR safe test file without using live malware.
- [x] The report is described as safe educational evidence, not production
  antivirus performance.

## Cut Rule

If time is short, keep the Rust CLI scanner, signature database, JSON/Markdown
Rust report, demo tree, final report, and Cargo verification gate. Cut UI polish
and extra heuristics first.
