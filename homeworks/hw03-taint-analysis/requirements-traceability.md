# HW3 Requirements Traceability

## Purpose

This file mirrors the Project I virus-scanner habit: turn the official brief
into a compact acceptance matrix before treating the homework as done.

## Source Facts

- Course assignment: `[2026 NS] Taint Analysis`
- Required submission: `513559004_taint_hw.zip`
- Required zip contents: `taint_analysis.py`, `output.txt`, `report.pdf`
- Official due date: `2026-05-20 23:59`
- Internal finish target: `2026-05-08`
- Target result: all `16 / 16` tracked bytes in `output_buf` are tainted.

## Requirement Matrix

| ID | Requirement | Minimum acceptance check | Evidence to keep |
| --- | --- | --- | --- |
| R1 | Implement `hook_strncpy` byte copy. | `dest[i]` receives the concrete byte from `src[i]` for each copied byte. | `solution/taint_analysis.py` |
| R2 | Propagate taint through `hook_strncpy`. | Each destination byte receives the source byte's taint state. | `solution/taint_analysis.py`, `solution/output.txt` |
| R3 | Mark source bytes as tainted. | `track_length` bytes from `user_input` are tainted before emulation. | `solution/taint_analysis.py` |
| R4 | Check sink bytes. | The script prints one status line per tracked byte at `output_buf`. | `solution/output.txt` |
| R5 | Produce correct run evidence. | Output says `Result: 16 / 16 bytes tainted at sink`. | `solution/output.txt` |
| R6 | Answer four report questions. | Report covers propagation path, hook reasoning, one real scenario, and at least two limitations. | `report/report.tex`, `report/report.pdf` |
| R7 | Build clean submission zip. | Zip contains exactly `taint_analysis.py`, `output.txt`, and `report.pdf`. | `solution/513559004_taint_hw.zip`, `report/submission-package.md` |

## Completion Gate

The homework is ready to upload when every row above has a concrete artifact and
`unzip -l solution/513559004_taint_hw.zip` shows only the three required files.
