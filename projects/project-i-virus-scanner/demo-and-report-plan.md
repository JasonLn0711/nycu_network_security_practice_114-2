# Demo And Report Plan

## Demo Objective

Show that Sentinel can scan a directory tree, detect a safe mock-virus file, produce a clear report, and distinguish exact signature detections from weaker heuristic warnings.

The demo should be boring in the best way: deterministic, safe, repeatable, and easy for the instructor to understand.

Current local checkpoint as of `2026-04-22`: `python3 demo/run_demo.py` passes `22` tests and regenerates the JSON report, Markdown report, pattern benchmark, and evidence manifest. The demo result is `5` files scanned, `1` infected safe mock fixture, `1` suspicious heuristic fixture, `3` clean files, `0` skipped files, and `0` errors.

## Demo Safety Rules

- Use only safe fixtures, such as EICAR if required by the instructor or locally created dummy files.
- Do not download, store, execute, or analyze live malware.
- Do not scan personal directories in the demo.
- Keep the target folder small enough to explain on screen.
- Make the scanner read-only: no deletion, quarantine, upload, or network action.
- Keep symbolic links skipped by default so the scan does not silently leave the explicit demo tree.

## Demo Tree Shape

```text
demo/demo-tree/
  clean/
    notes.txt
    image-placeholder.bin
  nested/
    level-1/
      level-2/
        sentinel-safe-mock-virus.txt
  suspicious/
    api-names-fixture.txt
  ignored-or-empty/
    empty.txt
```

Expected result:

| Path | Expected status | Why |
| --- | --- | --- |
| `clean/notes.txt` | clean | Normal text file with no signature or heuristic signal. |
| `clean/image-placeholder.bin` | clean | Binary-like file with no known signature. |
| `nested/level-1/level-2/sentinel-safe-mock-virus.txt` | infected | Exact safe mock-virus signature match. |
| `suspicious/api-names-fixture.txt` | suspicious | Safe fixture containing suspicious API-name strings for the heuristic demo. |
| `ignored-or-empty/empty.txt` | clean | Empty file should not break the scanner. |

## Demo Script

1. Show the official requirement summary:
   - signature database
   - directory scan
   - bitwise or pattern matching
   - heuristic rules
   - report with paths, threat level, and timestamp
2. Show the signature database.
3. Show the demo folder tree.
4. Run the scanner:

```bash
python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

5. Show the terminal summary:
   - total files scanned
   - infected count
   - suspicious count
   - clean count
   - report path
6. Open the JSON or Markdown report.
7. Point to the nested safe mock-virus finding.
8. Point to the heuristic-only suspicious fixture and explain that it is not a confirmed malware detection.
9. Close with limitations:
   - only known-signature detection
   - no live malware
   - no production antivirus claim
   - safe educational demo only

## Demo Evidence Checklist

- [ ] Private source repo URL recorded.
- [ ] Commit hash used for demo recorded.
- [x] Signature database created locally.
- [x] Demo tree created locally.
- [x] Scanner command recorded.
- [x] JSON report saved under `reports/demo-report.json`.
- [x] Markdown report saved under `reports/demo-report.md`.
- [x] Pattern benchmark saved under `reports/pattern-benchmark.json` and `reports/pattern-benchmark.md`.
- [x] Evidence manifest saved under `reports/demo-evidence-manifest.json`.
- [x] Terminal transcript drafted under `demo/demo-transcript.md`.
- [ ] Screenshot captured.
- [ ] Short demo video or final live-demo script prepared.
- [x] Report draft references the same evidence.
- [x] Final report PDF references the same evidence.
- [x] Release-readiness gate passes via `python3 scripts/check_release.py`.

## Report Outline

### 1. Introduction

- Problem: detecting known threats in a directory without executing files.
- Goal: build Sentinel, a functional signature-based scanner.
- Safety stance: safe mock-virus fixture only, no live malware.

### 2. Requirement Summary

Map the official brief to implemented features:

| Brief item | Sentinel feature |
| --- | --- |
| Signature database | JSON database with hashes and patterns |
| File traversal | Recursive directory walker |
| Bitwise comparison | Byte/hex pattern matcher |
| Heuristic analysis | Suspicious-rule layer |
| Report/UI | JSON or Markdown security report |

### 3. Signature Database Design

Explain:

- schema fields
- why JSON or CSV was chosen
- how signatures are validated
- how MD5/SHA-256 values are indexed
- why exact hash matching is fast and deterministic

Data-structure paragraph:

- Hash map for exact digest lookup.
- Aho-Corasick byte-pattern automaton for multi-pattern matching.
- Optional Bloom filter only if implemented and measured.

### 4. Scanning Engine

Explain:

- directory traversal
- symbolic-link skipping and skipped-result reporting
- file read error handling
- MD5/SHA-256 computation
- Aho-Corasick chunked pattern matching with streamed automaton state
- result aggregation
- exit codes

### 5. Heuristic Analysis

Explain the difference between:

- `infected`: confirmed signature match
- `suspicious`: heuristic signal only
- `clean`: no detection
- `skipped`: symbolic link or other unsupported file intentionally not scanned

Example heuristic table:

| Heuristic | Rationale | Limitation |
| --- | --- | --- |
| Suspicious API-name indicator | Some malware uses process or memory APIs. | String presence alone is not proof. |
| Extension/magic mismatch | File disguise can be suspicious. | Many benign files can be mislabeled. |
| High entropy | Packing/encryption can raise entropy. | Compressed benign files may also trigger. |

### 6. Reporting

Include:

- report schema
- timestamps
- counts
- finding fields
- sample result table

### 7. Evaluation

Minimum evaluation table:

| Test case | Expected | Result |
| --- | --- | --- |
| Clean text file | clean | Pass in local demo report |
| Empty file | clean | Pass in local demo report |
| Nested Sentinel safe mock-virus fixture | infected | Pass in local demo report |
| Suspicious API-name fixture | suspicious | Pass in local demo report |
| Symbolic link inside target tree | skipped | Pass in unit tests |
| EICAR reference bytes | MD5/SHA-256 match standard reference | Pass in unit tests without storing an EICAR file |
| Malformed signature database | clear error | Pass in unit tests |
| Overlapping byte patterns | all expected matches | Pass in unit tests |
| Streamed pattern split across chunks | infected | Pass in unit tests |
| Synthetic pattern benchmark | match sets equal to naive baseline | Pass in `reports/pattern-benchmark.json` |

### 8. Limitations And Ethics

State clearly:

- Sentinel is educational, not production antivirus.
- It detects only known signatures and simple heuristic indicators.
- It does not execute or detonate files.
- It avoids live malware and real-world target scanning.

### 9. Conclusion

Summarize what was built, what data structures were used, and how the demo proves the course requirements.

## Submission Package

Expected final package:

- private GitHub or GitLab source repository
- report PDF: local draft exists at `report/final-report.pdf`
- demo video or live-demo readiness: final capture still pending
- generated report artifact: local draft exists at `reports/demo-report.json`
- generated Markdown report artifact: local draft exists at `reports/demo-report.md`
- generated benchmark artifacts: local drafts exist at `reports/pattern-benchmark.json` and `reports/pattern-benchmark.md`
- generated evidence manifest: local draft exists at `reports/demo-evidence-manifest.json`
- short README with install, run, test, and safety notes: local README exists; private-repo URL and commit hash still pending
- release-readiness check: local `scripts/check_release.py` exists and passes; rerun after private-repo mirroring
