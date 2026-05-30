# Submission Staging

Use this directory for final upload staging and dry-run package checks.

The official PDF labels the assignment as HW4 but describes the ZIP root folder
as `HW6_{student_ID}`. This repo preserves that source wording. Confirm the
final upload folder name in E3 before the real submission.

## Dry Run

```bash
scripts/build_submission_dry_run.sh 513559004
```

The dry run creates an ignored package under `submission/dry-run/`, then checks:

- root folder name
- `Extension/manifest.json`
- `Extension/background.js`
- `{student_ID}_report.pdf`
- PDF header
- absence of `.git`, `.DS_Store`, `raw-local`, and cache artifacts

The generated dry-run PDF is a placeholder for package validation only. Replace
it with the final evidence-backed report PDF before upload.

## Final Package

The current final package is:

```text
submission/final/HW6_513559004.zip
```

It follows the directory structure written in the official PDF:

```text
HW6_513559004/
├── Extension/
│   ├── manifest.json
│   └── background.js
└── 513559004_report.pdf
```

The course platform labels the assignment as HW4 while the PDF specifies
`HW6_{student_ID}` for the ZIP root. The local final package preserves the PDF
structure and keeps this discrepancy documented for the upload check.
