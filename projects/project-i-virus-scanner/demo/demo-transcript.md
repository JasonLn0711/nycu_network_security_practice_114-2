# Sentinel Demo Transcript

## Purpose

This transcript records the Rust demo path for the Network Security Project I
virus scanner. It can be used as the base for a live demo script or short
recorded video.

## Safety Note

The current demo generates the official EICAR safe anti-malware test file in a
controlled local demo folder before scanning it. EICAR is not live malware. The
scanner is read-only: it does not execute, delete, quarantine, upload, or modify
scanned files. It skips symbolic links by default so the demo scan stays inside
the explicit target tree.

Final demo decision: because the instructor wording asks for a safe EICAR test
file, the Rust demo must generate and detect EICAR. The generated
`eicar.com.txt` file is ignored by Git and excluded from private-repo export.

## Commands

From `projects/project-i-virus-scanner/rust/`:

```bash
cargo fmt --check
```

Observed result:

```text
Finished successfully with no formatting diff.
```

Run the Rust test suite:

```bash
cargo test
```

Observed result:

```text
running 13 tests
test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Run the Rust lint gate:

```bash
cargo clippy --all-targets -- -D warnings
```

Observed result:

```text
Finished successfully with warnings denied.
```

Validate the signature database:

```bash
cargo run -- validate-signatures --signatures ../signatures/malware-signatures.json
```

Observed result:

```text
signature database ok: schema=1.0 signatures=1 hash_matchers=2 patterns=1
```

Prepare the official EICAR safe test file for the demo:

```bash
cargo run -- prepare-eicar-demo --target ../demo/demo-tree
```

Observed result:

```text
EICAR demo fixture written: ../demo/demo-tree/nested/level-1/level-2/eicar.com.txt bytes=68
```

Verify the expected Project I demo summary:

```bash
cargo run -- verify-demo \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json
```

Observed result:

```text
Rust demo verification passed: scanned=5 infected=1 suspicious=1 clean=3 skipped=0 errors=0
```

Generate the Rust JSON and Markdown reports:

```bash
cargo run -- scan \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --json ../reports/demo-report.json \
  --markdown ../reports/demo-report.md
```

Observed result:

```text
Sentinel v2 Rust scan complete: scanned=5 infected=1 suspicious=1 clean=3 errors=0 json=../reports/demo-report.json markdown=../reports/demo-report.md
```

The scan command returns exit code `1` because the generated EICAR safe test
file was intentionally detected.

Generate the Rust evidence manifest:

```bash
cargo run -- write-evidence \
  --target ../demo/demo-tree \
  --signatures ../signatures/malware-signatures.json \
  --report ../reports/demo-report.json \
  --report ../reports/demo-report.md \
  --output ../reports/demo-evidence-manifest.json
```

Observed result:

```text
Rust evidence manifest written: ../reports/demo-evidence-manifest.json
```

## Expected Demo Talking Points

1. Show the signature database and explain that it has MD5, SHA-256, and
   hex-pattern matchers.
2. Show the demo folder tree.
3. Run or summarize the Rust formatting, test, lint, signature-validation, and
   demo-verification commands.
4. Run the Rust scan command.
5. Explain the exit code: `1` means an infected file was intentionally detected.
6. Open `reports/demo-report.md`.
7. Open `reports/demo-evidence-manifest.json` and show the demo-tree
   hashes, report hashes, safety flags, and Rust reproduction commands.
8. Point out the `bloom-filter` hash pre-check metadata and the exact hash-map
   verification policy.
9. Point out the `aho-corasick-byte-automaton` pattern engine and explain that
   byte-pattern state is preserved across chunks.
10. Point out the heuristic rules recorded in scan metadata:
   `api-name-indicator`, `magic-mismatch`, and `high-entropy-sample`.
11. Open `docs/standards-alignment.md` and explain that EICAR, NIST, OWASP, and
    MITRE were used as external calibration references.
12. Point to the generated EICAR safe test file:
    `nested/level-1/level-2/eicar.com.txt`.
13. Point to the heuristic-only file:
    `suspicious/api-names-fixture.txt`.
14. Close by saying the scanner is educational and read-only, not production
    antivirus.

## Final Submission Fields

- Team members: `513559004` Jsaon Chia-Sheng Lin; `313264012` 陳靖中
  (Ching-Chung Chen)
- LMS submission: `final-report-513559004-313264012.pdf`, submitted for
  grading on `2026-04-22 17:30`.
- Private repository URL: not created or moved in this pass; keep the source
  package ready only if the instructor requests it after grading starts.
- Pre-commit local source-baseline observed before packaging commits:
  `fd945f850bca755bc3fe4ae90584c72a5fe443f9`
