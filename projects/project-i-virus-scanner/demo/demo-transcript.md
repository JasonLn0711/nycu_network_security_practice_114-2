# Sentinel Demo Transcript

## Purpose

This transcript records the current local demo path for the Network Security Project I virus scanner.
It can be used as the base for a live demo script or a short recorded video.

## Safety Note

The current demo uses a local safe mock-virus fixture. It is not live malware and does not contain the literal EICAR string.
The scanner is read-only: it does not execute, delete, quarantine, upload, or modify scanned files.

## Commands

From `projects/project-i-virus-scanner/`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Observed result:

```text
Ran 15 tests in 0.005s

OK
```

Validate the signature database:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m sentinel validate-signatures signatures/malware-signatures.json
```

Observed result:

```text
Signature database valid: schema=1.0 signatures=1 patterns=1
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
  --output reports/demo-evidence-manifest.json
```

Observed result:

```text
Evidence manifest written: files=5 reports=2 output=reports/demo-evidence-manifest.json
```

## Expected Demo Talking Points

1. Show the signature database and explain that it has MD5, SHA-256, and hex-pattern matchers.
2. Show the demo folder tree.
3. Run the tests briefly or state that they passed.
4. Run the JSON or Markdown scan command.
5. Explain the exit code: `1` means an infected file was intentionally detected.
6. Open `reports/demo-report.md`.
7. Open `reports/demo-evidence-manifest.json` and show that the demo tree, signature database, and reports have SHA-256 hashes.
8. Point to the safe mock-virus fixture:
   - path: `nested/level-1/level-2/sentinel-safe-mock-virus.txt`
   - status: `infected`
   - evidence: MD5, SHA-256, and hex-pattern match
9. Point to the heuristic-only file:
   - path: `suspicious/api-names-fixture.txt`
   - status: `suspicious`
   - evidence: suspicious API-name strings
10. Close by saying the scanner is educational and read-only, not production antivirus.
