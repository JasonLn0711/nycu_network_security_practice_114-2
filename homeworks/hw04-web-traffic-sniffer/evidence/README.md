# HW04 Evidence Handling

This folder separates local raw evidence from submission-safe evidence.

## Evidence Layers

| Path | Commit status | Purpose |
| --- | --- | --- |
| `raw-local/` | ignored | Temporary local captures, raw screenshots, browser profile notes, and unredacted logs |
| `screenshots/` | allowed | Redacted screenshots suitable for the report |
| `traffic-observations.md` | allowed | Sanitized written observations tied to screenshot numbers |

## Controlled Capture Rule

Capture traffic only in the clean test browser profile described in
`docs/clean-browser-profile.md`. The evidence should support the assignment
questions while preserving personal-data boundaries.

## Redaction Rule

Apply `docs/redaction-rules.md` before moving any file from `raw-local/` into
`screenshots/` or report assets.
