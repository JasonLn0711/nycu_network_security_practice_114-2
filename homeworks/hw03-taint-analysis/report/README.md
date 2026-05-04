# HW3 Report

This folder owns the HW3 report package.

| File | Purpose |
| --- | --- |
| [report.tex](report.tex) | Canonical LaTeX source for the four report questions. |
| `report.pdf` | Compiled report artifact for the final zip. |
| [submission-package.md](submission-package.md) | Last-mile checklist, verification commands, and zip inventory. |

Build from this folder:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error report.tex
```

The final upload zip is built from `solution/`, because the official submission
requires `taint_analysis.py`, `output.txt`, and `report.pdf` at zip root.
