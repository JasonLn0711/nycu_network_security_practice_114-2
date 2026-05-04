# HW3 Taint Analysis Work Plan

## Assignment Contract

- Submit one zip named `513559004_taint_hw.zip`.
- Zip contents:
  - `taint_analysis.py`
  - `output.txt`
  - `report.pdf`
- Official due date: `2026-05-20 23:59`.
- Internal finish target: Friday `2026-05-08`.

## Ownership Boundary

- This file is the canonical detailed plan for HW3.
- Keep implementation gates, debug notes, report evidence, and packaging checks here in the Network Security repo.
- Keep `planning-everything-track` limited to capacity, deadline, and locator status.

## First-Principles Scope Decision

- The scarce resource is not calendar time; it is clean attention before the official due-date window closes.
- The shortest correct path is code correctness -> fresh output -> report -> zip. Report writing before a working analyzer risks fictional evidence.
- The assignment asks for three TODOs and a four-question report, not a reusable taint-analysis platform.
- Keep the original starter files unchanged so the modified solution can be compared against the official baseline.
- If capacity gets tight, preserve dependency verification, code correctness, and `output.txt`; cut polish and optional examples first.

## Current State Snapshot

- Official PDF and starter files are archived in this folder.
- Working files are staged in `solution/`.
- Local `.venv/` imports Triton and LIEF successfully.
- `solution/vuln.c` compiles into the ignored `solution/vuln` binary.
- Untouched starter run prints the assignment header and `Done.`, which means the remaining blocker is implementation, not environment setup.
- Next technical gate: complete TODO 1 and TODO 2 before trying to make the report look final.

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

## Detailed Execution Plan

### Gate 0 - Working Discipline

Purpose: make each run reproducible enough that `output.txt` can be trusted.

- Work only from `homeworks/hw03-taint-analysis/solution/`.
- Keep `starter/` unchanged for comparison.
- Use the local interpreter from the homework root:

```sh
cd /home/jnln3799/every_on_git_ubuntu/nycu_network_security_practice_114-2/homeworks/hw03-taint-analysis/solution
../.venv/bin/python taint_analysis.py
```

- Recompile `vuln` after any change to `vuln.c`, but do not edit `vuln.c` unless a compile or symbol issue proves it is necessary.
- Do not capture final `output.txt` until all three TODOs are complete and the terminal output visually matches the expected assignment shape.

### Gate 1 - TODO 1: `hook_strncpy`

Purpose: make the Python hook behave like the data movement that Triton cannot emulate through libc.

Implementation intent:

- Read `dest` from `rdi`, `src` from `rsi`, and `n` from `rdx`.
- Loop from byte `0` to `n - 1`.
- For each byte:
  - read the concrete byte at `src + i`
  - write it to `dest + i`
  - if `src + i` is tainted, taint `dest + i`
  - otherwise untaint `dest + i`
- Return `dest`, matching normal `strncpy` return behavior.

Verification signal:

- After TODO 1 alone, the script may still not show final success because source marking and sink reporting are incomplete.
- Do not debug TODO 1 in isolation for too long; complete TODO 2, then use the sink report to verify propagation.

Common mistakes to avoid:

- Copying bytes but forgetting taint propagation.
- Tainting the whole destination unconditionally.
- Forgetting to clear destination taint when the source byte is clean.
- Returning nothing from the hook when `strncpy` callers may expect the destination pointer in `rax`.

### Gate 2 - TODO 2: Mark Source Bytes

Purpose: define the trust boundary: the first `16` bytes of `user_input` are attacker-controlled.

Implementation intent:

- Before the emulation loop starts, loop over `track_length`.
- Call `ctx.taintMemory(source_addr + i)` for each source byte.
- Do not taint beyond `track_length`; the assignment is tracking the 16-byte path.

Verification signal:

- Once TODO 1 and TODO 2 are both in place, taint should flow from `user_input` through the XOR instructions into `processed`, then through hooked `strncpy` into `output_buf`.
- If the final result is less than `16 / 16`, inspect the hook first, then confirm `SOURCE_ADDR` and `TRACK_LEN` are being used exactly.

### Gate 3 - TODO 3: Check Sink Bytes

Purpose: produce the required evidence for `output.txt`.

Implementation intent:

- After emulation finishes, loop over `track_length` bytes starting at `sink_addr`.
- For each byte:
  - check `ctx.isMemoryTainted(sink_addr + i)`
  - print `[TAINTED] byte {i} at 0x{addr:x}` when tainted
  - print `[CLEAN] byte {i} at 0x{addr:x}` when clean
  - increment a tainted counter only for tainted bytes
- Print the summary line:

```text
Result: 16 / 16 bytes tainted at sink
```

Verification signal:

- All 16 sink bytes should be `[TAINTED]`.
- The actual addresses may differ from the PDF example; that is acceptable because the script resolves symbols dynamically.

### Gate 4 - First Full Run and Debug Pass

Run:

```sh
cd /home/jnln3799/every_on_git_ubuntu/nycu_network_security_practice_114-2/homeworks/hw03-taint-analysis/solution
../.venv/bin/python taint_analysis.py
```

Expected shape:

- Header prints source and sink addresses.
- 16 byte-status lines print for `output_buf`.
- Summary line says `Result: 16 / 16 bytes tainted at sink`.
- Final line says `Done.`.

If the run fails:

- Import error: reactivate/check `.venv`, then rerun the two import checks from the README.
- `lief.parse('./vuln')` fails: confirm `solution/vuln` exists and was compiled in the same folder.
- Source or sink symbol missing: confirm the binary was compiled from the provided `vuln.c` without stripping symbols.
- Fewer than 16 bytes tainted: check source marking, XOR propagation assumptions, and `hook_strncpy` taint copy.
- Infinite or long run: keep the existing instruction-count guard; do not remove it while debugging.

### Gate 5 - Capture `output.txt`

Only after the full run is correct:

```sh
cd /home/jnln3799/every_on_git_ubuntu/nycu_network_security_practice_114-2/homeworks/hw03-taint-analysis/solution
../.venv/bin/python taint_analysis.py | tee output.txt
```

Acceptance check:

- `output.txt` contains the full run, not only the summary line.
- It includes all 16 byte-status lines.
- It includes `Result: 16 / 16 bytes tainted at sink`.
- It includes `Done.`.

### Gate 6 - Report Draft

Write the report only after `output.txt` exists.

Use this evidence table:

| Report section | Evidence to cite | Keep it short |
| --- | --- | --- |
| Q1 propagation path | `vuln.c`, `output.txt`, `Result: 16 / 16` | Explain source -> XOR -> processed -> `strncpy` -> sink |
| Q2 hook necessity | `hook_strncpy` implementation | Explain that Triton cannot see inside Python hooks unless taint is manually copied |
| Q3 real-world scenario | one chosen source/sink/path | Use one concrete vulnerability, not three shallow ones |
| Q4 limitations | runtime path coverage and overhead, plus one more if useful | Pair each limitation with a complementary method |

Report quality bar:

- The report should be clear enough for grading, not publication-level.
- Include the observed result, but do not paste all terminal output into the report unless it helps.
- Explain XOR as "value changes, control/dependence remains."
- Keep each question answer focused: roughly 1-3 paragraphs per question is enough.

### Gate 7 - Build and Inspect Zip

Prepare staging from `solution/`:

```sh
cd /home/jnln3799/every_on_git_ubuntu/nycu_network_security_practice_114-2/homeworks/hw03-taint-analysis/solution
cp ../report/report.pdf ./report.pdf
zip 513559004_taint_hw.zip taint_analysis.py output.txt report.pdf
unzip -l 513559004_taint_hw.zip
```

Acceptance check:

- Zip filename is exactly `513559004_taint_hw.zip`.
- Zip contains exactly:
  - `taint_analysis.py`
  - `output.txt`
  - `report.pdf`
- Zip does not contain:
  - `vuln`
  - `vuln.c`
  - `.venv/`
  - `__pycache__/`
  - folder nesting

### Gate 8 - Fresh Final Verification

Before upload:

- Delete or move old `output.txt`, rerun the script, and regenerate it.
- Rebuild the zip after regenerating `output.txt`.
- Inspect `unzip -l`.
- Open `report.pdf` once to confirm it is readable and answers all four questions.
- If LMS upload cannot happen on Friday, leave a frozen package plus one note stating the exact blocker.

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

## Time-Boxed Block Plan

Use short blocks because this week also contains CYBERSEC delivery.

| Block | Target | Max time | Stop condition |
| --- | --- | ---: | --- |
| A | TODO 1 + TODO 2 | 45-60 min | source marking and hook logic written |
| B | first full run | 25-40 min | either `16 / 16` or one exact error captured |
| C | TODO 3 + `output.txt` | 45 min | byte-status report and clean output captured |
| D | report draft | 60-75 min | four questions answered from observed output |
| E | package check | 20 min | zip inspected and ready |

If Block A fails, do not start the report. Capture the error and resume at the code gate.
If Block D runs long, keep the answers direct and grader-facing; polish is secondary.

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
- Success target: source bytes are marked, `strncpy` copies taint, and any remaining issue is isolated to sink printing or final formatting.

### Wednesday 2026-05-06

- Complete TODO 3.
- Produce a clean `output.txt`.
- If CYBERSEC speech duty consumes the day, keep only a 25-minute verification block and move report drafting to Thursday.
- Success target: `output.txt` contains all 16 `[TAINTED]` lines and `Result: 16 / 16 bytes tainted at sink`.

### Thursday 2026-05-07

- Draft `report.pdf` from the four-question outline.
- Tie the explanation to the observed `16 / 16` output.
- Build a first submission zip and inspect its contents.
- Success target: first complete zip exists, even if final proofreading remains.

### Friday 2026-05-08

- Fresh-run verification from a clean shell.
- Rebuild `output.txt`, regenerate or proofread `report.pdf`, rebuild zip.
- Upload to LMS if everything is correct; otherwise freeze the package and write the exact remaining blocker.
- Success target: LMS upload complete, or a ready-to-submit package is frozen with one explicit upload blocker.

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
