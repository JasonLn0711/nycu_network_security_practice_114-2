# Sentinel Technical Design

## Design Goal

Build a small, explainable, safe signature-based virus scanner that satisfies the course brief without pretending to be production antivirus software.

The strongest default implementation is a Python 3 command-line tool because it is easy to run, easy to review, and enough for the required scanner/report/demo workflow. The team can still choose another language before implementation starts.

## System Boundary

Sentinel should scan only explicit demo or test directories passed by the user.

It should not:

- scan the whole machine by default
- modify, quarantine, delete, or upload files
- execute unknown files
- fetch remote signatures automatically
- process live malware

## Proposed CLI

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

Optional commands after the core works:

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

## Proposed Repository Layout

```text
project-i-virus-scanner/
  README.md
  project-spec.pdf
  requirements-traceability.md
  technical-design.md
  demo-and-report-plan.md
  src/
    sentinel/
      __init__.py
      __main__.py
      cli.py
      evidence.py
      scanner.py
      signatures.py
      matchers.py
      heuristics.py
      reporting.py
  signatures/
    malware-signatures.json
  demo/
    README.md
    demo-tree/
  reports/
    .gitkeep
  tests/
    test_signatures.py
    test_matchers.py
    test_scanner.py
    test_reporting.py
```

If the deliverable source must live in a separate private repository, keep this folder as the course-repo index and link to the private repo, final report, demo evidence, and submission package.

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
          "value": "3c02151fde3384bab4474e6a2f619157e1c0d51a14b711d226e9d750d31d9b54"
        },
        {
          "type": "hex_pattern",
          "value": "safe-fixture-pattern-as-hex"
        }
      ],
      "notes": "Safe local demo signature only; not live malware."
    }
  ]
}
```

Recommended in-memory structures:

| Structure | Use | Why |
| --- | --- | --- |
| `dict[str, Signature]` | Signature lookup by ID. | Stable report references and simple validation. |
| `dict[str, list[SignatureMatcher]]` | Hash lookup by algorithm and digest. | Exact hash checks become constant-time dictionary lookups. |
| `tuple[PatternMatcher, ...]` | Byte or hex pattern scan. | Validated once and reused during chunked file scans. |
| `list[HeuristicRule]` | Suspicious-file rules. | Keeps confirmed malware signatures separate from weaker signals. |

Optional report-only discussion:

- A Bloom filter can reduce unnecessary hash-map lookups when the signature set is large.
- Do not claim a Bloom filter was used unless it is actually implemented and tested.
- For this course project, a hash map is enough for a small signature database and is easier to verify.

## Scan Pipeline

1. Parse CLI arguments.
2. Load and validate the signature database.
3. Walk the target directory with a deterministic ordering.
4. For each regular file:
   - record file path, size, and read status
   - read file content in chunks
   - compute MD5 and SHA-256 incrementally
   - check hash signatures through lookup maps
   - scan chunks for configured hex or byte patterns
   - preserve enough overlap between chunks to catch split patterns
   - run heuristic rules against a bounded sample
   - append clean, suspicious, infected, skipped, or error result
5. Aggregate counts and severity.
6. Write a timestamped JSON or Markdown report.
7. Return an exit code:
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
- Search file bytes for the pattern during the chunked scan.
- Report pattern length and signature ID, but do not print large binary blobs.
- Preserve overlap between chunks so a pattern split across two chunks is still detectable.
- Test this with a safe fixture whose `ABCDE` marker crosses a small artificial chunk boundary.

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
- JSON report summary copied from `reports/demo-report.json`
- reproducibility commands for tests, signature validation, JSON scan, and Markdown scan

## Test Plan

| Test | Purpose |
| --- | --- |
| Valid signature file loads. | Prevent demo failure from malformed JSON. |
| Invalid signature file fails clearly. | Make configuration errors easy to debug. |
| Clean file remains clean. | Avoid false positive in the simplest case. |
| Safe mock-virus file is detected. | Prove the core requirement. |
| Nested folder scan finds hidden fixture. | Prove directory traversal. |
| Pattern split case across chunk boundary. | Prove bitwise comparison is not only whole-file search. |
| Suspicious fixture produces heuristic-only finding. | Prove Phase III without overclaiming. |
| Report contains required fields. | Protect report/demo stability. |
| Evidence manifest records demo tree and report hashes. | Keep the final demo reproducible. |

## Milestone Plan

| Milestone | Output | Done when |
| --- | --- | --- |
| M0 - Team and repo lock | Team members, language, private repo URL, Project I/II status | README open decisions are resolved or explicitly deferred. |
| M1 - Signature database | JSON schema and safe mock-virus fixture signature | Signature validation and hash-match test pass. |
| M2 - Scanner core | Directory traversal, hash match, pattern match | Nested safe fixture is detected from CLI. |
| M3 - Heuristic and report | Suspicious rules plus JSON report | Demo report has infected, suspicious, and clean examples. |
| M4 - Demo package | Demo tree, run script, captured report | A teammate can reproduce the demo from README commands. |
| M5 - Final report | PDF/report source | Report explains data structures and limitations honestly. |

Current local status as of `2026-04-22`: M1-M5 are locally implemented or drafted in the course repo, including chunked hashing, chunk-boundary pattern matching, reproducible demo reports, evidence manifest, demo runner, report source, and compiled PDF. M0 is still open because team/private repo/Project I-vs-II status is not locked; final submission still needs the private repo URL, final commit hash, and demo video or live-demo decision.

## Team Split

For a team of four:

| Owner | Workstream |
| --- | --- |
| A | Scanner CLI, traversal, and exit codes |
| B | Signature schema, hash/pattern matchers, validation |
| C | Heuristic rules, report schema, demo evidence |
| D | Final report, video/live-demo script, submission checklist |

For a solo version, implement M1-M3 first and keep the report/demo short.
