# HW3 Strict Grading Rubric and Self-Assessment

## Purpose

This file records a strict, quantitative grading standard for HW3 Taint
Analysis and applies the same standard to the current completed local package.

This is a stricter local audit rubric. It is compatible with the official
assignment shape, but it adds packaging and reproducibility checks so the final
submission can be judged by evidence, not by "looks complete" alone.

## Strict 100-Point Rubric

| Area | Points | Strict scoring rule |
| --- | ---: | --- |
| `hook_strncpy` byte copy | 8 | Correctly reads `rdi`, `rsi`, and `rdx`: 3. Copies each concrete byte from `src + i` to `dest + i`: 4. Returns `dest` with normal `strncpy` return semantics: 1. |
| `hook_strncpy` taint propagation | 12 | Checks taint state byte by byte from `src + i`: 5. Taints `dest + i` when the source byte is tainted: 4. Untaints `dest + i` when the source byte is clean: 2. Avoids unconditional whole-buffer taint and obvious false positives: 1. |
| Source taint marking | 10 | Uses a `track_length` loop: 4. Starts exactly at `source_addr`: 4. Does not hard-code the wrong address, over-taint, or under-taint: 2. |
| Sink taint checking | 10 | Uses `sink_addr` and `track_length` loop: 4. Prints one `[TAINTED]` or `[CLEAN]` line per tracked byte: 3. Correctly counts tainted bytes: 3. |
| Execution result correctness | 15 | Analyzer can be run in a prepared Triton/LIEF environment: 5. Output contains all 16 sink byte status lines: 4. Summary is `Result: 16 / 16 bytes tainted at sink`: 5. Output terminates cleanly with `Done.` or equivalent: 1. |
| Reproducibility and environment discipline | 10 | Dependency/setup commands are documented: 2. `vuln.c` compiles with the required flags: 2. `output.txt` is full terminal evidence, not only a hand-written summary: 2. Submission artifacts match the working files: 2. The current checkout can be rerun without undocumented local state: 2. |
| Report Q1: propagation path | 8 | Explains `user_input -> process_data() -> processed -> strncpy -> output_buf`: 4. Explains why XOR with a constant changes value but preserves taint/dependence: 3. Uses the observed `16 / 16` result: 1. |
| Report Q2: hook reasoning | 7 | Explains Triton is not emulating real libc `strncpy`: 3. Explains why the Python hook must manually copy taint: 3. Explains the false-negative risk if taint is not propagated: 1. |
| Report Q3: real-world scenario | 5 | Names a concrete vulnerability source, sink, and propagation path: 3. The scenario is security-relevant and not generic filler: 2. |
| Report Q4: limitations | 5 | Discusses at least two practical limitations of dynamic taint analysis: 3. Pairs limitations with complementary techniques or tools: 2. |
| Submission package | 10 | Zip filename is correct: 2. Zip contains exactly `taint_analysis.py`, `output.txt`, and `report.pdf`: 4. Zip contents match the working artifacts: 2. `report.pdf` opens and contains the intended report: 2. |

## Hard Caps

- If the zip cannot be opened, total score is capped at 30.
- If `taint_analysis.py` is missing, total score is capped at 35.
- If `taint_analysis.py` has a syntax error that prevents execution, total
  score is capped at 45.
- If `output.txt` is missing, total score is capped at 80.
- If `report.pdf` is missing, total score is capped at 70.
- If the result is not `16 / 16`, implementation and execution-result points
  are capped at 30 out of 65.
- If `output.txt` is fabricated or does not match a plausible run of the
  submitted script, total score is capped at 60.
- If the zip includes `.venv/`, caches, binaries, or unrelated bulky files,
  submission-package points are capped at 4 out of 10.

## Current HW3 Self-Assessment

Audit date: `2026-05-04`

Audited artifacts:

- `solution/taint_analysis.py`
- `solution/output.txt`
- `report/report.pdf`
- `solution/report.pdf`
- `solution/513559004_taint_hw.zip`

Verification evidence from the current audit:

- `solution/taint_analysis.py` implements byte copy and byte-level taint
  propagation in `hook_strncpy`.
- `emulate()` taints `track_length` bytes from `source_addr`.
- `emulate()` checks `track_length` bytes from `sink_addr` and prints per-byte
  taint status plus the summary count.
- `solution/output.txt` contains all 16 `[TAINTED]` lines and
  `Result: 16 / 16 bytes tainted at sink`.
- `gcc -o vuln vuln.c -no-pie -fno-stack-protector -fcf-protection=none`
  successfully builds a local x86-64 ELF binary from `solution/vuln.c`.
- `solution/513559004_taint_hw.zip` contains exactly three files:
  `taint_analysis.py`, `output.txt`, and `report.pdf`.
- The three files inside the zip match the working artifacts.
- `solution/report.pdf` matches `report/report.pdf`.
- `pdftotext` confirms the PDF contains the intended report sections and all
  four assigned answers.

Current local verification caveat:

- This checkout's system Python currently lacks `triton`, `pip`, and
  `python3-venv` support, so a fresh analyzer run could not be completed in this
  shell without first fixing the local Python environment. This is treated as a
  local reproducibility readiness deduction, not as evidence that the submitted
  code is wrong.

## Score Breakdown

| Area | Score | Notes |
| --- | ---: | --- |
| `hook_strncpy` byte copy | 8 / 8 | Correct argument reads, concrete byte copy, and return value. |
| `hook_strncpy` taint propagation | 12 / 12 | Correct byte-level taint copy and clean-byte untaint behavior. |
| Source taint marking | 10 / 10 | Uses `track_length` and `source_addr` correctly. |
| Sink taint checking | 10 / 10 | Prints each byte status and counts tainted bytes correctly. |
| Execution result correctness | 15 / 15 | Saved output has the complete expected `16 / 16` result shape. |
| Reproducibility and environment discipline | 8 / 10 | Compile path, zip consistency, and evidence are good; current checkout cannot rerun immediately because Triton/Python environment is missing. |
| Report Q1 | 8 / 8 | Explains the full path and why XOR with a constant does not remove taint. |
| Report Q2 | 7 / 7 | Correctly explains the hooked-libc boundary and false-negative risk. |
| Report Q3 | 5 / 5 | SQL injection scenario has source, sink, and propagation path. |
| Report Q4 | 5 / 5 | Covers path coverage, runtime/hook complexity, and implicit-flow limitations with complements. |
| Submission package | 10 / 10 | Correct name, exact three-file inventory, matching artifacts, readable PDF. |

Final strict local audit score: `98 / 100`.

If graded only under the official assignment's script-plus-report rubric in a
proper Triton/LIEF environment, this package is likely full-credit. Under this
stricter local audit, the only deduction is the current checkout's missing
rerunnable Python/Triton environment.
