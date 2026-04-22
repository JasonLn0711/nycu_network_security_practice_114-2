# Sentinel Scan Report

## Run Metadata

- Tool: `Sentinel`
- Target: `demo/demo-tree`
- Signature schema: `1.0`
- Started: `2026-04-22T04:26:54+00:00`
- Finished: `2026-04-22T04:26:54+00:00`

## Summary

| Metric | Count |
| --- | ---: |
| Files scanned | 5 |
| Infected | 1 |
| Suspicious | 1 |
| Clean | 3 |
| Skipped | 0 |
| Errors | 0 |

## Findings

| Path | Status | Severity | Evidence |
| --- | --- | --- | --- |
| `nested/level-1/level-2/sentinel-safe-mock-virus.txt` | infected | critical | md5:sig-sentinel-safe-mock-virus; sha256:sig-sentinel-safe-mock-virus; hex_pattern:sig-sentinel-safe-mock-virus |
| `suspicious/api-names-fixture.txt` | suspicious | medium | api-name-indicator (CreateRemoteThread, VirtualAllocEx, WriteProcessMemory) |

## All Results

| Path | Status | Severity | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| `clean/image-placeholder.bin` | clean | info | 57 | `7f4f12bf857a1f5d3ada9afe9489605bc5f4e8d55a15abd82675dde5bd488ee7` |
| `clean/notes.txt` | clean | info | 106 | `2f5d4f23920fc8aa80b4e63d175b23a26c1f2b201bc7f8a07bcb05770c59d11c` |
| `ignored-or-empty/empty.txt` | clean | info | 1 | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` |
| `nested/level-1/level-2/sentinel-safe-mock-virus.txt` | infected | critical | 140 | `3c02151fde3384bab4474e6a2f619157e1c0d51a14b711d226e9d750d31d9b54` |
| `suspicious/api-names-fixture.txt` | suspicious | medium | 150 | `2b8bc14462bbb16f771ea073728786ea462fdddfab54af6ff547381dd6db56e1` |
