# Sentinel Python Implementation

This folder contains the primary, release-gated Sentinel implementation for
Project I.

## Contents

| Path | Purpose |
| --- | --- |
| `src/sentinel/` | Python scanner package and CLI implementation. |
| `tests/` | Standard-library unit tests for signatures, matching, scanning, reports, evidence, CLI, and export boundaries. |
| `pyproject.toml` | Editable-install package metadata for the Python implementation. |

## Commands

From the project root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m unittest discover -s python/tests -v
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m sentinel scan demo/demo-tree --signatures signatures/malware-signatures.json --report reports/demo-report.json --format json
```

Editable install from the project root:

```bash
python3 -m pip install -e python
```
