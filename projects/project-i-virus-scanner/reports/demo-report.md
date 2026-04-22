# Sentinel Scan Report

## Run Metadata

- Tool: `Sentinel`
- Target: `demo/demo-tree`
- Signature schema: `1.0`
- Started: `2026-04-22T05:21:49+00:00`
- Finished: `2026-04-22T05:21:49+00:00`

## Scan Engine

- Pattern engine: `aho-corasick-byte-automaton`
- Pattern count: `1`
- Automaton states: `30`
- Chunk size bytes: `1048576`
- Symlink policy: `skip`

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
| `nested/level-1/level-2/sentinel-safe-mock-virus.txt` | infected | critical | md5:sig-sentinel-safe-mock-virus; sha256:sig-sentinel-safe-mock-virus; hex_pattern:sig-sentinel-safe-mock-virus@109 |
| `suspicious/api-names-fixture.txt` | suspicious | medium | api-name-indicator (CreateRemoteThread, VirtualAllocEx, WriteProcessMemory) |

## All Results

| Path | Status | Severity | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| `clean/image-placeholder.bin` | clean | info | 56 | `2d878a97c4fb1d6cabcf0b6e6aa52eb01ec6a7bf064de55b5d4c893e27673bbe` |
| `clean/notes.txt` | clean | info | 105 | `e74722e0fe162678153f68b7ebca5d363a5175f7dc317c1cff65208ad912ff4c` |
| `ignored-or-empty/empty.txt` | clean | info | 1 | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` |
| `nested/level-1/level-2/sentinel-safe-mock-virus.txt` | infected | critical | 139 | `569f58884e12c423aa9442c7b220c2814ea0febb66278e61f4b8b0bd35dad122` |
| `suspicious/api-names-fixture.txt` | suspicious | medium | 149 | `e82d86354c2d35e16ba25417d042a6d8633fe390118bcfa0767f7370352b3f2e` |
