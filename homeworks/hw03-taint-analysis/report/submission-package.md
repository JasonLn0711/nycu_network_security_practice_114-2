# HW3 Submission Package

## Purpose

This file records the last-mile HW3 package state in the same spirit as the
Project I virus-scanner submission notes: implementation, evidence, report, and
zip inventory should agree before upload.

## Current Local State

| Area | State | Evidence |
| --- | --- | --- |
| Analyzer implementation | Complete | `solution/taint_analysis.py` |
| Target binary | Compiled locally | `solution/vuln` |
| Run evidence | Complete | `solution/output.txt` |
| Report | Compiled | `report/report.pdf` |
| Submission zip | Built | `solution/513559004_taint_hw.zip` |

## Verification Record

| Command | Expected result |
| --- | --- |
| `cd solution && ../.venv/bin/python taint_analysis.py` | Prints all 16 sink bytes as `[TAINTED]`. |
| `cd solution && ../.venv/bin/python taint_analysis.py \| tee output.txt` | Regenerates full terminal output. |
| `cd report && latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex` | Builds `report/report.pdf`. |
| `cd solution && zip 513559004_taint_hw.zip taint_analysis.py output.txt report.pdf` | Builds final submission zip. |
| `cd solution && unzip -l 513559004_taint_hw.zip` | Shows exactly the three required files. |

## Final Pre-Upload Audit

Audit date: `2026-05-04`

| Check | Result |
| --- | --- |
| Fresh analyzer run matches saved `solution/output.txt` | pass |
| Zip `taint_analysis.py` matches `solution/taint_analysis.py` | pass |
| Zip `output.txt` matches `solution/output.txt` | pass |
| Zip `report.pdf` matches `solution/report.pdf` | pass |
| `solution/report.pdf` matches canonical `report/report.pdf` | pass |
| Zip inventory contains only the three required files | pass |

Zip inventory:

```text
taint_analysis.py
output.txt
report.pdf
```

Checksums:

| File | SHA-256 |
| --- | --- |
| `solution/513559004_taint_hw.zip` | `3c2d94836794fe08d39dcf319c0c602af58fed6a7ffa5dcbf2504a507a120910` |
| `solution/taint_analysis.py` | `67932c220ff9964ec02b50919362ef7da0b2c3421e60364ea792d800ee709edc` |
| `solution/output.txt` | `240c690944c99b71a1a6ea1b7b094601bcca90387f3fab265e54c53889a9920c` |
| `solution/report.pdf` | `1c7c983a0d2dab1f7bc8d70085b649447658694d171f52f4684720d7fb7f978c` |
| `report/report.pdf` | `1c7c983a0d2dab1f7bc8d70085b649447658694d171f52f4684720d7fb7f978c` |

## Final Checklist

- [x] Implement TODO 1: byte copy and taint propagation in `hook_strncpy`.
- [x] Implement TODO 2: mark 16 source bytes as tainted.
- [x] Implement TODO 3: print sink-byte taint status and total count.
- [x] Capture `output.txt` from a fresh run.
- [x] Confirm `Result: 16 / 16 bytes tainted at sink`.
- [x] Answer all four report questions.
- [x] Compile `report.pdf`.
- [x] Build `513559004_taint_hw.zip`.
- [x] Inspect zip inventory.
- [x] Complete byte-for-byte pre-upload audit.

## Upload Note

Upload `solution/513559004_taint_hw.zip` to the course LMS. Keep this folder as
the local archive of the implementation and evidence.

Current LMS status: `upload pending`

Detailed upload steps:

1. Open the LMS assignment page for `HW3. Taint Analysis`.
2. Upload `solution/513559004_taint_hw.zip`.
3. Confirm the displayed filename is exactly `513559004_taint_hw.zip`.
4. Submit, then verify the LMS status changed from draft/uploaded to submitted.
5. If the LMS shows a timestamp or receipt, capture that in this file or the
   planning locator after submission.

## Snapshot Policy

Snapshots are not required by the HW3 spec and must not be added to the
submission zip. They are useful as local audit evidence, especially because the
course LMS is the final source of submission status.

Recommended snapshots:

| Snapshot | When | Why |
| --- | --- | --- |
| Zip inventory / checksum | Already captured in this file | Proves the local package had exactly the required three files. |
| LMS upload confirmation before submit | After selecting the zip but before final submit | Proves the displayed upload filename is `513559004_taint_hw.zip`. |
| LMS submitted receipt/status | After final submit | Proves the assignment moved from pending/draft to submitted. |

Store optional local screenshots under `report/snapshots/`. Do not duplicate
them inside `solution/` or the final zip.

## Receipt Slot

Fill this after LMS submission:

| Field | Value |
| --- | --- |
| LMS status | `pending` |
| Submitted file shown by LMS | `pending` |
| Submission timestamp | `pending` |
| Grading status | `pending` |
| Notes | `pending` |
