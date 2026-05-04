# Network Security HW3 - Taint Analysis

## Agent Search Summary

- Course: `114-spring-535607-network-security-practice-attack-and-defense`
- Assignment: `HW3. Taint Analysis`
- Name: `Jason Chia-Sheng Lin`
- Student ID: `513559004`
- Organization: `Institute of Biophotonics, NYCU`
- Opened: `2026-05-01 00:00`
- Due: `2026-05-20 23:59`
- Internal finish target: Friday `2026-05-08`
- Status: intake archived; local environment verified; implementation not started
- Submission file target: `513559004_taint_hw.zip`
- Planning/project locator from the course repo root: `../planning-everything-track/data/projects/2026-05-network-security-hw3-taint-analysis.md`

## What This Project Must Prove

This homework uses Triton to emulate a compiled Linux binary and track whether tainted data flows from `user_input` to `output_buf`.

The final submission must prove:

- `hook_strncpy` copies bytes from `src` to `dest` and propagates taint byte by byte.
- `emulate()` marks `track_length` bytes from `source_addr` as tainted.
- `emulate()` checks `track_length` bytes at `sink_addr` and reports each byte as `[TAINTED]` or `[CLEAN]`.
- Running `python3 taint_analysis.py` shows `16 / 16` tainted bytes at the sink.
- `report.pdf` answers the four assigned report questions.

## Folder Map

| Path | Purpose | Git policy |
| --- | --- | --- |
| `hw3-taint-analysis-spec.pdf` | Official assignment PDF copied from Downloads | tracked source asset |
| `starter/taint_analysis.py` | Original starter script with TODOs | tracked source asset |
| `starter/vuln.c` | Original target C program | tracked source asset |
| `work-plan.md` | Friday-finish execution plan and report outline | tracked |
| `report/` | Report notes, draft, and final PDF when produced | tracked for source and final submission PDF |
| `solution/` | Modified script, compiled-run output, and submission staging once implementation begins | tracked for allowed homework deliverables |

## Required Commands

Install and verify dependencies:

```sh
sudo apt update && sudo apt install -y gcc python3 python3-pip
pip install triton-library lief
python3 -c "from triton import *; print('Triton OK')"
python3 -c "import lief; print('LIEF OK')"
```

Current local setup uses the ignored virtual environment at `.venv/`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install triton-library lief
```

Compile the target binary from the working solution folder:

```sh
gcc -o vuln vuln.c -no-pie -fno-stack-protector -fcf-protection=none
```

Run and capture output:

```sh
python3 taint_analysis.py | tee output.txt
```

Build the final submission zip:

```sh
zip 513559004_taint_hw.zip taint_analysis.py output.txt report.pdf
```

## Friday Finish Definition

By Friday `2026-05-08`, the project is done if:

- `solution/taint_analysis.py` contains completed TODO 1, TODO 2, and TODO 3.
- `solution/output.txt` is generated from a fresh run and shows `16 / 16 bytes tainted at sink`.
- `report/report.pdf` answers all four report questions and uses the observed output rather than invented results.
- `solution/513559004_taint_hw.zip` contains exactly `taint_analysis.py`, `output.txt`, and `report.pdf`.
- The LMS submission page shows the zip uploaded; if not submitted Friday, the folder is frozen and ready to submit well before `2026-05-20 23:59`.

## Safety Rules

- Keep the official starter files unchanged under `starter/`.
- Do implementation in `solution/` so the original handout remains recoverable.
- Do not commit local virtual environments, caches, compiled binaries, or exploratory package folders.
- Do not overbuild the analyzer. The assignment asks for the three TODOs, one output file, and a short report.
- If dependency installation fails, capture the exact error and switch to the smallest Linux environment that can run Triton.

## Next Action

Implement TODO 1 and TODO 2 in `solution/taint_analysis.py`, then rerun with:

```sh
../.venv/bin/python taint_analysis.py
```

Baseline check on `2026-05-04`: Triton and LIEF import successfully in `.venv/`, `solution/vuln.c` compiles, and the untouched starter script runs but prints no sink taint report yet because TODO 3 is still empty.
