# Sentinel Technical Design

## Design Goal

Build a small, explainable, safe signature-based virus scanner that satisfies the course brief without pretending to be production antivirus software.

The primary implementation is a Python 3 command-line tool because it is easy to run, easy to review, and enough for the required scanner/report/demo workflow.

An optional Rust companion implementation now lives in `../../rust/`. It mirrors
the same scanner boundaries and data structures for a systems-language path, but
it is not the primary release-gated submission artifact until it can be compiled
and tested on a machine with `rustc` / `cargo` installed.

## System Boundary

Sentinel should scan only explicit demo or test directories passed by the user.

It should not:

- scan the whole machine by default
- modify, quarantine, delete, or upload files
- execute unknown files
- fetch remote signatures automatically
- process live malware

## Core Commands

```bash
python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

Markdown report output is also supported for the final demo:

```bash
python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.md \
  --format markdown
```

Supporting commands:

```bash
python3 -m sentinel validate-signatures signatures/malware-signatures.json
python3 -m sentinel summarize-report reports/demo-report.json
python3 -m sentinel write-evidence \
  --target demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --report reports/demo-report.md \
  --output reports/demo-evidence-manifest.json
```

## Data Model

Use JSON first. It is readable, easy to validate with the standard library, and can express multiple signature types cleanly.

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-06-01T00:00:00+08:00",
  "signatures": [
    {
      "id": "sig-sentinel-safe-mock-virus",
      "name": "Sentinel Safe Mock Virus Fixture",
      "category": "safe-mock-virus",
      "severity": "critical",
      "matchers": [
        {
          "type": "sha256",
          "value": "569f58884e12c423aa9442c7b220c2814ea0febb66278e61f4b8b0bd35dad122"
        },
        {
          "type": "hex_pattern",
          "value": "534146455f4d4f434b5f4d41524b4552"
        }
      ],
      "notes": "Safe local demo signature only; not live malware."
    }
  ]
}
```

Implemented in-memory structures:

| Structure | Use | Why |
| --- | --- | --- |
| `dict[str, Signature]` | Signature lookup by ID. | Stable report references and simple validation. |
| `dict[str, list[SignatureMatcher]]` | Hash lookup by algorithm and digest. | Exact hash checks become constant-time dictionary lookups. |
| `HashBloomFilter` | Hash-signature membership pre-check. | Gives a reportable scalable data structure while preserving exact hash-map verification. |
| `PatternScanEngine` | Byte or hex pattern scan. | Builds an Aho-Corasick automaton once per scan run and reuses it for streamed file scans. |
| `PatternStreamScanner` | Per-file byte-pattern scan state. | Preserves automaton state across chunks without loading the whole file. |
| `list[HeuristicRule]` | Suspicious-file rules. | Keeps confirmed malware signatures separate from weaker signals. |

The Bloom filter stores normalized `algorithm:digest` keys for configured hash
matchers. During scanning it answers only "might contain"; every possible hit is
then confirmed against the exact hash index. This keeps the usual Bloom-filter
false-positive limitation from producing infected findings.

## Scan Pipeline

1. Parse CLI arguments.
2. Load and validate the signature database.
3. Walk the target directory with a deterministic ordering.
4. Report symbolic links as `skipped` so the scanner does not silently leave the explicit target tree.
5. For each regular file:
   - record file path, size, and read status
   - read file content in chunks
   - compute MD5 and SHA-256 incrementally
   - pre-check hash signatures through the Bloom filter
   - confirm possible hash hits through lookup maps
   - scan chunks with the Aho-Corasick byte-pattern automaton
   - preserve automaton state across chunks to catch split patterns
   - run heuristic rules against a bounded sample
   - append clean, suspicious, infected, skipped, or error result
6. Aggregate counts and severity.
7. Write a timestamped JSON or Markdown report.
8. Return an exit code:
   - `0` when no infected files are found
   - `1` when infected files are found
   - `2` for configuration or scanner errors

## Matching Rules

### Hash Matching

Hash matching is the primary exact-detection path.

Acceptance behavior:

- If a scanned file digest equals a known signature digest, mark the file `infected`.
- Include algorithm, signature ID, signature name, and digest in the report.
- If multiple signatures match, report all of them.

### Pattern Matching

Pattern matching supports the brief's bitwise-comparison requirement.

Acceptance behavior:

- Convert each configured hex pattern into bytes at load time.
- Build a trie with failure links from all configured byte patterns.
- Search streamed file chunks with one automaton state machine instead of one independent search per pattern.
- Report pattern length, first matched offset, and signature ID, but do not print large binary blobs.
- Preserve automaton state across chunks so a pattern split across two chunks is still detectable.
- Test overlapping patterns, stream chunk boundaries, and a safe fixture whose `ABCDE` marker crosses a small artificial chunk boundary.

The current implementation is intentionally standard-library Python. The synthetic benchmark records both the Aho-Corasick automaton and a naive per-pattern `bytes` search. For small demo-scale inputs, CPython's C-backed `bytes` search can be faster; the reason to keep the automaton is explainable multi-pattern behavior and better algorithmic scaling as signature count grows.

### Heuristic Rules

Heuristics should never be presented as confirmed malware on their own.

Suggested rules:

| Rule | Signal | Report severity |
| --- | --- | --- |
| `api-name-indicator` | Safe fixture contains suspicious Windows API strings such as process-injection API names. | medium |
| `extension-magic-mismatch` | File extension and magic bytes disagree in a safe demo fixture. | low |
| `high-entropy-small-binary` | Small binary-like fixture has unusually high entropy. | low |

Heuristic output should use wording such as `suspicious` or `review`, not `infected`, unless an exact signature also matches.

## Report Schema

```json
{
  "tool": "Sentinel",
  "started_at": "2026-06-01T10:00:00+08:00",
  "finished_at": "2026-06-01T10:00:02+08:00",
  "target": "demo/demo-tree",
  "summary": {
    "files_scanned": 12,
    "infected": 1,
    "suspicious": 1,
    "clean": 10,
    "skipped": 0,
    "errors": 0
  },
  "findings": [
    {
      "path": "demo/demo-tree/nested/level-1/level-2/sentinel-safe-mock-virus.txt",
      "status": "infected",
      "severity": "critical",
      "matches": [
        {
          "signature_id": "sig-sentinel-safe-mock-virus",
          "signature_name": "Sentinel Safe Mock Virus Fixture",
          "matcher": "sha256"
        }
      ]
    }
  ]
}
```

## Evidence Manifest

`write-evidence` produces `reports/demo-evidence-manifest.json`, which records:

- safety flags: read-only scanner, no live malware, no scanned-file execution, no network action
- SHA-256 and size for the signature database
- SHA-256 and size for each demo-tree file
- SHA-256 and size for the generated JSON and Markdown reports
- SHA-256 and size for the generated pattern benchmark artifacts
- JSON report summary copied from `reports/demo-report.json`
- reproducibility commands for tests, signature validation, JSON scan, and Markdown scan

## Release Gate

`scripts/check_release.py` is the local submission-candidate gate. It runs the full demo regeneration path, then validates version consistency, standards alignment, EICAR reference hashes, expected demo counts, Bloom-filter scan metadata, Aho-Corasick scan metadata, symbolic-link traversal policy, benchmark equivalence, evidence-manifest safety flags, private-repo export boundaries, and final-report PDF presence. Use it before mirroring the project into the required private repository and again after the private-repo move.

## Test Plan

| Test | Purpose |
| --- | --- |
| Valid signature file loads. | Prevent demo failure from malformed JSON. |
| Invalid signature file fails clearly. | Make configuration errors easy to debug. |
| Clean file remains clean. | Avoid false positive in the simplest case. |
| Safe mock-virus file is detected. | Prove the core requirement. |
| EICAR reference hashes match in memory. | Use an international anti-malware test reference without storing the test file. |
| Bloom-filter pre-check still uses exact hash-map verification. | Prove the scalable data structure does not create infected false positives. |
| Nested folder scan finds hidden fixture. | Prove directory traversal. |
| Symbolic links are skipped by default. | Keep scans inside the explicit target tree unless the policy is deliberately changed. |
| Pattern split case across chunk boundary. | Prove bitwise comparison is not only whole-file search. |
| Overlapping pattern matches are both reported. | Prove the automaton handles failure-link outputs correctly. |
| Streamed chunks preserve pattern state. | Prove the matcher does not rely on whole-file reads or manual overlap buffers. |
| Suspicious fixture produces heuristic-only finding. | Prove Phase III without overclaiming. |
| Report contains required fields. | Protect report/demo stability. |
| Evidence manifest records demo tree and report hashes. | Keep the final demo reproducible. |
| Pattern benchmark matches naive baseline. | Keep algorithmic-hardening evidence honest and reproducible. |
| Private-repo export excludes official brief, LaTeX build files, removed drafts, and literal EICAR files. | Make the required private repository handoff repeatable before the remote exists. |

## Current Status

As of `2026-04-22`, scanner core, report generation, demo evidence, synthetic benchmark evidence, standards notes, private-repo export tooling, release gate, and compiled report are implemented locally. Final submission still needs team confirmation, private repository URL, final commit hash, and demo video or live-demo decision.
