# Sentinel Virus Scanner Report Draft

## 1. Introduction

Sentinel is a functional signature-based virus scanner built for the Network Security Practice final project. Its goal is to scan an explicit target directory, compare files against a known-signature database, flag safe mock-virus fixtures, and produce a readable security report.

This implementation is intentionally read-only. It does not execute scanned files, delete files, quarantine files, upload files, or scan the whole machine by default. The current demo uses a local safe mock-virus fixture instead of live malware or the literal EICAR string. If the instructor requires the exact EICAR test file, it should be created only in the final controlled demo environment and documented separately.

## 2. Requirement Summary

| Official requirement | Sentinel implementation |
| --- | --- |
| Structured malware-signature repository | `signatures/malware-signatures.json` with MD5, SHA-256, and hex-pattern matchers |
| File traversal and comparison | `sentinel.scanner` recursively walks the explicit target directory and scans regular files |
| Bitwise or pattern comparison | `hex_pattern` signatures are converted to bytes and searched in file content |
| Heuristic analysis | `sentinel.heuristics` flags suspicious API-name strings and other low-confidence signals |
| Security report | `sentinel.reporting` writes timestamped JSON and Markdown reports with summary counts, findings, hashes, paths, and severities |
| Demonstration | `demo/demo-tree/` contains clean files, one safe mock-virus fixture, and one heuristic-only suspicious fixture |

## 3. Signature Database Design

The signature database uses JSON because it is easy to read, easy to validate with the Python standard library, and flexible enough to store multiple matcher types per signature.

Each signature contains:

- `id`: stable internal identifier
- `name`: human-readable threat or fixture name
- `category`: classification such as `safe-mock-virus`
- `severity`: one of `info`, `low`, `medium`, `high`, or `critical`
- `matchers`: one or more detection methods
- `notes`: safety and interpretation notes

The current safe mock-virus signature has three matchers:

| Matcher | Purpose |
| --- | --- |
| `md5` | Fast exact-file detection for the known demo fixture |
| `sha256` | Stronger exact-file detection for the same fixture |
| `hex_pattern` | Byte-pattern matching to satisfy the bitwise comparison requirement |

### Data Structures

Sentinel loads the JSON database into a `SignatureDatabase` object with:

| Structure | Purpose | Reason |
| --- | --- | --- |
| `tuple[Signature, ...]` | Preserve validated signature records | Immutable enough for the scan run and easy to inspect |
| `dict[str, dict[str, tuple[HashMatcher, ...]]]` | Lookup hash matches by algorithm and digest | Exact hash detection becomes constant-time dictionary lookup |
| `tuple[PatternMatcher, ...]` | Store validated byte patterns | Validated once and reused during chunked file scans |

A Bloom filter is not currently implemented. It would only be useful if the signature database became large enough that avoiding unnecessary dictionary checks mattered. For this course project, direct hash-map lookup is simpler, testable, and honest.

## 4. Scanning Engine

The scanner workflow is:

1. Parse the CLI command.
2. Load and validate the signature database.
3. Walk the explicit target directory in sorted order.
4. Read each regular file in chunks.
5. Compute MD5 and SHA-256 incrementally.
6. Check exact hash matches.
7. Search configured byte patterns while preserving chunk overlap.
8. Run heuristic rules against a bounded content sample.
9. Assign file status:
   - `infected` when an exact signature or configured pattern matches
   - `suspicious` when only heuristics trigger
   - `clean` when no detection triggers
   - `error` when a file or target cannot be read
10. Write a JSON or Markdown report.

The scanner returns exit code `1` when infected files are found. This makes detections visible in scripts while still keeping the scan read-only.

The chunked scan avoids loading full files into memory for hash and pattern matching. For pattern matching, the scanner keeps a short tail from the previous chunk so that a signature split across two chunks is still detected. This behavior is covered by the `test_chunked_scan_finds_pattern_across_chunk_boundary` unit test.

## 5. Heuristic Analysis

Heuristics are weaker than signatures, so Sentinel keeps them separate. A heuristic-only hit is marked `suspicious`, not `infected`.

Current heuristic rules:

| Rule | Signal | Severity | Limitation |
| --- | --- | --- | --- |
| `api-name-indicator` | Safe fixture mentions names such as `CreateRemoteThread`, `VirtualAllocEx`, and `WriteProcessMemory` | medium | String presence alone does not prove malware |
| `extension-magic-mismatch` | A `.txt` file begins with executable-like `MZ` bytes | low | Benign mislabeled files can exist |
| `high-entropy-small-binary` | Small binary-like file has high entropy | low | Compressed benign files can also trigger |

The current demo uses `api-name-indicator` to create one suspicious but not infected finding.

## 6. Report Format

The JSON report contains:

- tool name
- signature schema version
- start and finish timestamps
- target path
- summary counts
- findings for infected, suspicious, skipped, or error results
- all per-file results, including hashes and statuses

The generated JSON demo report is stored at `reports/demo-report.json`.

The Markdown report is stored at `reports/demo-report.md`. It is easier to show during a live demo because it has a summary table, findings table, and all-results table.

The evidence manifest is stored at `reports/demo-evidence-manifest.json`. It records SHA-256 hashes for the demo tree, signature database, and generated reports, plus the exact commands needed to reproduce the current demo evidence.

## 7. Current Evaluation

Command used:

```bash
PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

Observed summary:

| Metric | Result |
| --- | --- |
| Files scanned | 5 |
| Infected | 1 |
| Suspicious | 1 |
| Clean | 3 |
| Errors | 0 |

Markdown report command:

```bash
PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.md \
  --format markdown
```

Evidence manifest command:

```bash
PYTHONPATH=src python3 -m sentinel write-evidence \
  --target demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --report reports/demo-report.md \
  --output reports/demo-evidence-manifest.json
```

Test command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Observed result:

| Test area | Status |
| --- | --- |
| Signature parsing and validation | pass |
| Hash and pattern matching | pass |
| Chunk-boundary pattern matching | pass |
| Directory scan and missing-target handling | pass |
| Report construction and JSON writing | pass |
| Evidence manifest generation | pass |
| CLI scan and signature validation commands | pass |

## 8. Limitations And Ethics

Sentinel is an educational scanner, not production antivirus software. It detects only signatures and simple heuristic indicators that are present in the configured database or rules. It does not execute files, detonate samples, collect telemetry, or handle live malware.

The current mock-virus fixture is a local safe string marker. The report should be clear that this demonstrates the scanner mechanism rather than real-world malware coverage.

## 9. Next Work

Before final submission:

1. Confirm whether Project I is still required alongside Project II.
2. Confirm team members and source-code private repository.
3. Move or mirror the implementation into the required private GitHub/GitLab repository.
4. Decide whether the final demo must use the literal EICAR string.
5. Capture a final demo video or live-demo script.
6. Convert this draft into the required report format.
