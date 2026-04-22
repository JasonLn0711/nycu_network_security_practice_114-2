# Sentinel v2 Rust

This folder is a Rust companion implementation for Project I. The Python
implementation remains the primary submission path because it is already covered
by the release gate and final report. The Rust version exists to demonstrate the
same scanner design in a systems language without moving the project goalposts.

## Scope

Implemented in this v2 Rust prototype:

- JSON signature loading and validation.
- MD5 and SHA-256 signature matching.
- Bloom-filter hash pre-check followed by exact hash-map verification.
- Aho-Corasick byte-pattern matching.
- Deterministic recursive directory traversal.
- Symbolic-link skipping.
- Heuristic-only suspicious finding for process-injection API names.
- JSON and Markdown report generation.

Still intentionally out of scope:

- Live malware handling.
- Quarantine, deletion, upload, or file mutation.
- Whole-machine scanning.
- Production antivirus claims.

## Commands

From this folder:

```bash
cargo run -- scan \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --json ../reports/demo-report-rust.json \
  --markdown ../reports/demo-report-rust.md
```

Expected demo summary:

```text
Sentinel v2 Rust scan complete: scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

The scan command returns exit code `1` when the safe mock-virus fixture is
detected. That mirrors the Python scanner behavior and is expected for the demo.

Validate the signature database only:

```bash
cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json
```

Run Rust tests:

```bash
cargo test
```

## Toolchain Note

This workspace currently does not have `rustc` or `cargo` installed, so the Rust
implementation is scaffolded and ready for a Rust-capable environment but was not
compiled locally in this pass.
