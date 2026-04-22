# Sentinel Demo Transcript

## Purpose

This transcript records the current local demo path for the Network Security Project I virus scanner.
It can be used as the base for a live demo script or a short recorded video.

## Safety Note

The current demo uses a local safe mock-virus fixture. It is not live malware and does not contain the literal EICAR string.
The scanner is read-only: it does not execute, delete, quarantine, upload, or modify scanned files. It skips symbolic links by default so the demo scan stays inside the explicit target tree.

## Commands

From `projects/project-i-virus-scanner/`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Observed result:

```text
Ran 25 tests in 0.071s

OK
```

Validate the signature database:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel validate-signatures signatures/malware-signatures.json
```

Validate the EICAR reference-hash profile:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel validate-signatures signatures/eicar-reference-signature.json
```

Observed result:

```text
Signature database valid: schema=1.0 signatures=1 patterns=1
Signature database valid: schema=1.0 signatures=1 patterns=0
```

Generate the JSON report:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --format json
```

Observed result:

```text
Sentinel scan complete: scanned=5 infected=1 suspicious=1 clean=3 errors=0 report=reports/demo-report.json
```

The command returns exit code `1` because an infected safe mock-virus fixture was intentionally detected.

Generate the Markdown report:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel scan demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.md \
  --format markdown
```

Observed result:

```text
Sentinel scan complete: scanned=5 infected=1 suspicious=1 clean=3 errors=0 report=reports/demo-report.md
```

Summarize the JSON report:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel summarize-report reports/demo-report.json
```

Observed result:

```text
Sentinel report summary: scanned=5 infected=1 suspicious=1 clean=3 errors=0
```

Generate the evidence manifest:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel write-evidence \
  --target demo/demo-tree \
  --signatures signatures/malware-signatures.json \
  --report reports/demo-report.json \
  --report reports/demo-report.md \
  --report reports/pattern-benchmark.json \
  --report reports/pattern-benchmark.md \
  --output reports/demo-evidence-manifest.json
```

Observed result:

```text
Evidence manifest written: files=5 reports=4 output=reports/demo-evidence-manifest.json
```

Generate the safe synthetic pattern benchmark:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/benchmark_patterns.py
```

Observed result:

```text
Pattern benchmark complete: patterns=128 payload_size=524288
```

Validate the private-repo export package without copying files:

```bash
python3 scripts/export_private_repo.py --dry-run
```

Observed result:

```text
"manifest_type": "private-repo-export"
"file_count": 50
```

Run the release-readiness gate:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 scripts/check_release.py
```

Observed result:

```text
[ ok ] version files agree
[ ok ] standards alignment is present
[ ok ] EICAR reference hashes are consistent
[ ok ] demo regeneration passes
[ ok ] demo report is consistent
[ ok ] benchmark evidence is consistent
[ ok ] evidence manifest is consistent
[ ok ] private repo export plan is consistent
[ ok ] final report PDF exists

Release check passed for Sentinel 0.4.0.
```

## Expected Demo Talking Points

1. Show the signature database and explain that it has MD5, SHA-256, and hex-pattern matchers.
2. Show the demo folder tree.
3. Run the tests briefly or state that the 25-test suite passed.
4. Run the JSON or Markdown scan command.
5. Explain the exit code: `1` means an infected file was intentionally detected.
6. Open `reports/demo-report.md`.
7. Point out the `bloom-filter` hash pre-check metadata and the exact hash-map verification policy.
8. Open `reports/pattern-benchmark.md` and explain that the Aho-Corasick matcher has the same match set as the naive baseline on safe synthetic data.
9. Open `docs/standards-alignment.md` and explain that EICAR, NIST, OWASP, and MITRE were used as external calibration references.
10. Run or show `scripts/check_release.py` as the final consistency gate.
11. Open `reports/demo-evidence-manifest.json` and show that the demo tree, signature database, reports, and benchmark artifacts have SHA-256 hashes.
12. Run or show `scripts/export_private_repo.py --dry-run` and explain that this is the package checklist for the required private repo.
13. Point to the safe mock-virus fixture:
   - path: `nested/level-1/level-2/sentinel-safe-mock-virus.txt`
   - status: `infected`
   - evidence: MD5, SHA-256, and hex-pattern match
14. Point to the heuristic-only file:
   - path: `suspicious/api-names-fixture.txt`
   - status: `suspicious`
   - evidence: suspicious API-name strings
15. Close by saying the scanner is educational and read-only, not production antivirus.
