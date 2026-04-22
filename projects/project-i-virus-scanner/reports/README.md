# Generated Reports

This folder keeps the current Rust-generated evidence artifacts for Project I.

| File | Purpose |
| --- | --- |
| [demo-report.json](demo-report.json) | Machine-readable scan result for the safe demo tree. |
| [demo-report.md](demo-report.md) | Instructor-friendly Markdown scan result. |
| [demo-evidence-manifest.json](demo-evidence-manifest.json) | Hashes, safety flags, inputs, report hashes, and reproduction commands. |

Regenerate from `projects/project-i-virus-scanner/`:

```bash
make rust-evidence
```

Keep only the current canonical Rust evidence files here. Do not store benchmark scratch output or duplicate language-specific report names unless the course requirement changes.
