# Product Continuation

## Decision

On `2026-04-29`, the scanner product continuation was split out of the course
archive into:

```text
../../../sentinel-virus-scanner/
```

The shared cybersecurity product-family prefix is `sentinel-`.

The strategic product surface is `Sentinel Artifact Scanner`: a transparent
local artifact scanner and evidence generator, not another antivirus.

## Boundary

This course folder remains the canonical archive for Network Security Project I:

- official brief
- submitted report source and PDFs
- LMS submission notes
- course-specific evidence screenshots
- course demo reports
- grading follow-up

The product repo owns future product work:

- product README
- product spec and MVP spec
- target audience
- product roadmap
- CLI / config / rule / schema specs
- safety boundary
- Rust CLI evolution
- packaging and release work

Do not copy official course PDFs, LMS grading notes, or submission-only artifacts
into the product repo.
