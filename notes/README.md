# Notes

This folder contains personal lecture notes and expanded explanations for NYCU `Network Security Practice`.

Use these files when you want narrative explanations, mixed lecture context, examples, and study framing. Use [handouts/](handouts/) for compact slide-aligned notes, [../midterm_notes/](../midterm_notes/) for exam recall, and [../slide_notes/](../slide_notes/) for long-form slide deep dives.

## Course Overview

| File | Main Coverage | Notes |
| --- | --- | --- |
| [handouts/csic30094_syllabus.md](handouts/csic30094_syllabus.md) | Course facts, grading, references, and weekly dates from the syllabus | Compact source-aligned course overview |

## Lecture Notes

| File | Main Coverage | Notes |
| --- | --- | --- |
| [nsp_260225_w1.md](nsp_260225_w1.md) | Course introduction, malware, study framework, supporting reading strategy | Broad conceptual overview in English |
| [nsp_260304_w2-1.md](nsp_260304_w2-1.md) | Environment variables, process inheritance, linker abuse, external-program attacks | Chinese, focused on environment-variable attack surfaces |
| [nsp_260304_w2.md](nsp_260304_w2.md) | Environment variables, access control, Set-UID, service architecture, file permissions | Chinese, combines multiple week-2 topics in one file |
| [nsp_260311_w3.md](nsp_260311_w3.md) | Linux security basics, authentication, `/etc/passwd` and `/etc/shadow`, capabilities, Set-UID risks, secure design principles | Chinese, deeper host-security note |

## Layering Notes

- The two `2026-03-04` notes intentionally overlap: `nsp_260304_w2-1.md` is the focused environment-variable attack-surface slice, while `nsp_260304_w2.md` is the broader week-2 consolidation that connects environment variables to access control and Set-UID behavior.
- If this overlap becomes too noisy later, merge them into one curated lecture note rather than creating another parallel summary.
- Keep exam-only recall material in [../midterm_notes/](../midterm_notes/) so lecture notes do not become duplicate cram sheets.

## Handout-Aligned Notes

The handout-note index lives at [handouts/index.md](handouts/index.md).

These files should stay compact and mapped to raw files in [../handouts/](../handouts/). Create a new handout note only when there is real explanation, examples, workflows, or exam cues to preserve.

## Writing Rule

- Keep date-based lecture notes in this folder.
- Keep short slide-aligned summaries in `notes/handouts/`.
- Move exam-focused recall material to `midterm_notes/`.
- Move long research extensions to `slide_notes/`.
