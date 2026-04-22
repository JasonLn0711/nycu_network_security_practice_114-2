# Sentinel Pattern-Matching Benchmark

## Scope

Safe synthetic benchmark only. No live malware, no network activity, and no scanned-file execution.

## Configuration

| Setting | Value |
| --- | ---: |
| Pattern count | 128 |
| Payload size bytes | 524288 |
| Repetitions | 5 |
| Inserted pattern count | 8 |
| Automaton states | 1001 |

## Results

| Matcher | Best ms | Matches |
| --- | ---: | ---: |
| Aho-Corasick byte automaton | 42.826 | 8 |
| Naive per-pattern bytes search | 18.788 | 8 |

- Match sets equal: `True`
- Interpretation: Aho-Corasick scans the payload once with automaton state carried across bytes. For small Python-only demos, CPython's C-backed bytes search may remain competitive; the professional value here is deterministic multi-pattern behavior and explainable scaling.
