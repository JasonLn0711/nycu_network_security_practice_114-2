# HW04 - Pi Memory Transfer Note

HW04 Pi Memory now belongs to the AIASE course repository. This network-security
archive keeps a concise transfer note so future agents can route the material
to the correct course workspace.

## Canonical Location

- Repository: `../nycu-114-2-taica-ncku-aiase/`
- Homework entry: `TAICA_AIASE2026/homeworks/HW4.md`
- Full package: `TAICA_AIASE2026/homeworks/HW4-pi-memory/`
- Original GitHub Classroom remote:
  `https://github.com/Netdb-NCKU/hw4-pi-memory-JasonLn0711.git`
- Assignment deadline from the bundled spec: `2026-06-09 23:59`; course
  announcements remain the final deadline source.

## Transfer Scope

The AIASE repository now owns the ordinary-file archive and working copy for
HW4 Pi Memory. The transferred package includes the assignment spec,
implementation, tests, benchmark corpus, demo notes, validation documents,
GitHub Classroom CI files, and experiment logs.

Nested Git metadata, local virtual environments, pytest caches, and other
machine-local runtime state stay outside the archive scope.

## Working Commands

```bash
cd ../nycu-114-2-taica-ncku-aiase/TAICA_AIASE2026/homeworks/HW4-pi-memory
python3 -m pytest -q
python3 benchmark/run_benchmark.py --k 5 --per-query
```
