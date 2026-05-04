# HW3 Taint Analysis Work Plan

## Assignment Contract

- Submit one zip named `513559004_taint_hw.zip`.
- Zip contents:
  - `taint_analysis.py`
  - `output.txt`
  - `report.pdf`
- Official due date: `2026-05-20 23:59`.
- Internal finish target: Friday `2026-05-08`.

## First-Principles Scope Decision

- The scarce resource is not calendar time; it is clean attention before the official due-date window closes.
- The shortest correct path is code correctness -> fresh output -> report -> zip. Report writing before a working analyzer risks fictional evidence.
- The assignment asks for three TODOs and a four-question report, not a reusable taint-analysis platform.
- Keep the original starter files unchanged so the modified solution can be compared against the official baseline.
- If capacity gets tight, preserve dependency verification, code correctness, and `output.txt`; cut polish and optional examples first.

## Implementation Checklist

- [x] Copy `starter/taint_analysis.py` and `starter/vuln.c` into `solution/`.
- [x] Verify Linux dependency path: `gcc`, `triton-library`, and `lief`.
- [x] Compile `vuln.c` with `gcc -o vuln vuln.c -no-pie -fno-stack-protector -fcf-protection=none`.
- [ ] TODO 1: implement `hook_strncpy(dest, src, n)` byte copying plus taint propagation.
- [ ] TODO 2: mark `track_length` bytes starting at `source_addr` as tainted.
- [ ] TODO 3: inspect `track_length` bytes at `sink_addr`, print each byte status, and print total tainted count.
- [ ] Run `python3 taint_analysis.py`.
- [ ] Save fresh terminal output to `solution/output.txt`.
- [ ] Confirm output says `Result: 16 / 16 bytes tainted at sink`.
- [ ] Package final zip with only the three required files.

## Report Outline

### Q1 - Propagation Path

Explain `user_input -> process_data() -> processed -> strncpy -> output_buf`.

Key point: XOR with a constant changes the concrete byte value, but it does not change who controls the byte. If attacker-controlled input determines the result, the result remains tainted.

### Q2 - Hooked `strncpy`

Explain that Triton tracks taint through emulated instructions. A Python hook is outside the emulated instruction stream, so the hook must manually copy both concrete bytes and taint state.

If taint is not propagated in the hook, `output_buf` can look clean even though attacker-controlled data reached it.

### Q3 - Real Vulnerability Scenario

Use one concrete scenario:

- Source: HTTP request parameter, form field, cookie, uploaded file, or socket input.
- Sink: SQL query execution, shell command, HTML response, file path, or fixed-size buffer copy.
- Path: parsing and transformations that preserve attacker control until the sink.

### Q4 - Dynamic Taint Limitations

Cover at least two:

- Only observes paths that actually execute.
- Runtime overhead can be high.
- Environment/input coverage matters.
- Library hooks and implicit flows are difficult.
- Path explosion and multi-process systems complicate tracking.

Pair with complementary techniques:

- Static analysis.
- Fuzzing.
- Unit/integration tests with security assertions.
- Sanitizer or runtime instrumentation.
- Manual code review for trust-boundary design.

## Day-by-Day Finish Plan

### Monday 2026-05-04

- Archive official files and create the project locator.
- Read the PDF once for exact deliverables.
- Prepare the working folder and first-run checklist.
- Set up ignored `.venv/` and verify Triton/LIEF imports.
- Compile `solution/vuln.c`.
- Baseline run result: the untouched starter prints the assignment header and `Done.`, but no sink-byte report yet.
- Stop after setup unless there is a clean 30-minute implementation window.

### Tuesday 2026-05-05

- Complete TODO 1 and TODO 2.
- Run the script and capture the first meaningful failure or partial output.
- Do not write the report before the analyzer behavior is understood.

### Wednesday 2026-05-06

- Complete TODO 3.
- Produce a clean `output.txt`.
- If CYBERSEC speech duty consumes the day, keep only a 25-minute verification block and move report drafting to Thursday.

### Thursday 2026-05-07

- Draft `report.pdf` from the four-question outline.
- Tie the explanation to the observed `16 / 16` output.
- Build a first submission zip and inspect its contents.

### Friday 2026-05-08

- Fresh-run verification from a clean shell.
- Rebuild `output.txt`, regenerate or proofread `report.pdf`, rebuild zip.
- Upload to LMS if everything is correct; otherwise freeze the package and write the exact remaining blocker.

## Cut Rules

- Cut optional OpenClaw/personal-agent implementation before cutting HW3.
- Cut report polish before cutting code correctness and fresh output.
- Do not cut sleep/recovery to make room for optional lanes; use the official due-date buffer if Friday becomes blocked by fixed commitments.

## First Debug Questions

- Does `python3 -c "from triton import *"` pass?
- Does `python3 -c "import lief"` pass?
- Does `gcc` produce a non-PIE `vuln` binary?
- Does the script resolve `user_input` and `output_buf` symbols?
- Does the final output show all 16 sink bytes as tainted?
