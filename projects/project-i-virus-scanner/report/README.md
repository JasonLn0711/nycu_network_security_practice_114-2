# Report

This folder owns the Project I final report package.

| File | Purpose |
| --- | --- |
| [final-report.tex](final-report.tex) | Canonical LaTeX source for the Rust submission report. |
| `final-report.pdf` | Compiled report artifact generated from `final-report.tex`. |
| `final-report-513559004-313264012.pdf` | Submission-named copy of the compiled Rust report for course upload. |
| [submission-package.md](submission-package.md) | Last-mile submission checklist, private-repo handoff state, and verification record. |
| [evidence-screenshots/](evidence-screenshots/) | Screenshot evidence used by the final report and demo review. |

Build from this folder:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error final-report.tex
```

Only keep the current canonical report here. Superseded report variants belong in Git history, not as parallel live files.
