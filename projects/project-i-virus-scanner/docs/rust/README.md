# Rust v2 Companion Implementation

## Purpose

`rust/` is a companion implementation of the Project I scanner in Rust. It
does not replace the Python Sentinel package used by the release gate and final
report. Its purpose is to show that the same signature-scanner design can be
implemented in a systems language if the instructor or team later wants that
direction.

## Current Local Status

- Rust source and Cargo metadata have been added under `rust/`.
- The implementation mirrors the Python scanner's core behavior:
  - JSON signature loading and validation
  - MD5 and SHA-256 matching
  - Bloom-filter pre-check with exact hash-map verification
  - Aho-Corasick byte-pattern matching
  - deterministic directory traversal
  - symbolic-link skipping
  - heuristic-only suspicious API-name findings
  - JSON and Markdown report output
- This machine currently does not have `rustc` or `cargo` installed, so the Rust
  version was not compiled locally in this pass.

## Verification Commands

Run these from `rust/` on a Rust-capable machine:

```bash
cargo test
cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json
cargo run -- scan \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --json ../reports/demo-report-rust.json \
  --markdown ../reports/demo-report-rust.md
```

Expected scan result:

```text
scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

The scan command returns exit code `1` when the safe mock-virus fixture is found.
That is expected and matches the Python implementation's demo behavior.

## Submission Guidance

Keep Python as the primary submission path unless the instructor explicitly asks
for C++/Rust or the team chooses to present this as an optional companion
implementation. The official Project I brief focuses on scanner behavior,
signature database design, data structures, report, and demo. The Rust version is
therefore useful as an extra implementation artifact, not a reason to reset the
already verified Python package.
