# NYCU Network Security Practice 114-2

Study repository for the NYCU `Network Security Practice` course. This repository currently serves as a course-material archive and note-taking workspace rather than a software project: it contains lecture notes, homework-prep notes, and bundled handouts/slides used for study.

## Author

Jason Chia-Sheng Lin  
PhD Student, Institute of Biophotonics, National Yang Ming Chiao Tung University (NYCU)

## What This Repository Contains

- `notes/`
  - Weekly lecture notes and expanded summaries tied to class dates.
  - Focus areas currently include introduction, malware, environment variables, access control, Linux security basics, and Set-UID / privileged programs.
- `hw1/notes/`
  - A structured five-week self-study track for Homework 1.
  - The sequence starts from fundamentals and gradually moves toward Linux command-line usage, basic C reading, executable structure, and beginner Ghidra workflows.
- `handouts/`
  - Bundled reference material such as PDFs and slides related to the course topics.
  - These appear to be official course or third-party teaching materials and are not covered by the repository's documentation license.

## Repository Layout

```text
.
├── handouts/
│   ├── A. Introduction.pdf
│   ├── B1. Malware.pdf
│   ├── B2. Environment_Variables.pptx
│   ├── C1. Linux_Security_Basics.pdf
│   ├── C2. SetUID.pdf
│   ├── C3. Access Control Models.pdf
│   ├── C4. Bell-LaPadula.pdf
│   ├── C5. SELinux.pdf
│   └── C6. Windows Access Control.pdf
├── hw1/
│   └── notes/
│       ├── notes_week_1.md
│       ├── notes_week_2.md
│       ├── notes_week_3.md
│       ├── notes_week_4.md
│       └── notes_week_5.md
└── notes/
    ├── nsp_260225_w1.md
    ├── nsp_260304_w2-1.md
    ├── nsp_260304_w2.md
    └── nsp_260311_w3.md
```

## Content Index

### Lecture Notes

| File | Main Coverage | Notes |
| --- | --- | --- |
| `notes/nsp_260225_w1.md` | Course introduction, malware, study framework, supporting reading strategy | Broad conceptual overview in English |
| `notes/nsp_260304_w2-1.md` | Environment variables, process inheritance, linker abuse, external-program attacks | Chinese, focused on environment-variable attack surfaces |
| `notes/nsp_260304_w2.md` | Environment variables, access control, Set-UID, service architecture, file permissions | Chinese, combines multiple week-2 topics in one file |
| `notes/nsp_260311_w3.md` | Linux security basics, authentication, `/etc/passwd` and `/etc/shadow`, capabilities, Set-UID risks, secure design principles | Chinese, deeper host-security note |

### Homework 1 Study Track

| File | Main Coverage | Intended Outcome |
| --- | --- | --- |
| `hw1/notes/notes_week_1.md` | Programs, binaries, operating systems, files, paths, executables, command line | Build core mental models from zero |
| `hw1/notes/notes_week_2.md` | Linux basics, navigation, file operations, reading output, permissions, running programs | Gain hands-on terminal fluency |
| `hw1/notes/notes_week_3.md` | Basic C concepts: variables, control flow, functions, strings, input/output | Read decompiler-like C without panic |
| `hw1/notes/notes_week_4.md` | Build pipeline, ELF files, assembly intuition, stack/register basics, decompiler limitations | Bridge source code and binary form |
| `hw1/notes/notes_week_5.md` | Ghidra projects, auto-analysis, navigation, functions, strings, xrefs, decompiler usage | Start practical reverse-engineering workflow |

### Reference Handouts

| File | Topic |
| --- | --- |
| `handouts/A. Introduction.pdf` | Course introduction |
| `handouts/B1. Malware.pdf` | Malware |
| `handouts/B2. Environment_Variables.pptx` | Environment variables and related attacks |
| `handouts/C1. Linux_Security_Basics.pdf` | Linux security basics |
| `handouts/C2. SetUID.pdf` | Set-UID / privileged programs |
| `handouts/C3. Access Control Models.pdf` | Access control models |
| `handouts/C4. Bell-LaPadula.pdf` | Bell-LaPadula model |
| `handouts/C5. SELinux.pdf` | SELinux |
| `handouts/C6. Windows Access Control.pdf` | Windows access control |

## Naming Conventions

- `notes/nsp_YYMMDD_wN.md`
  - Course note for a specific lecture date and week number.
  - Example: `nsp_260311_w3.md` corresponds to a note associated with `2026-03-11`, week 3.
- `hw1/notes/notes_week_N.md`
  - Homework-preparation note grouped by study week rather than lecture date.

## How To Use This Repository

### For Review Before or After Class

1. Start with the relevant file in `handouts/` to see the official topic framing.
2. Read the matching file in `notes/` for expanded explanations and study-oriented organization.
3. Add your own clarifications, examples, command snippets, or diagrams directly into the Markdown notes.

### For Homework 1 Preparation

Recommended order:

1. `hw1/notes/notes_week_1.md`
2. `hw1/notes/notes_week_2.md`
3. `hw1/notes/notes_week_3.md`
4. `hw1/notes/notes_week_4.md`
5. `hw1/notes/notes_week_5.md`

That sequence moves from basic computing concepts to beginner reverse-engineering tooling. It is a better fit for a new learner than jumping straight into Ghidra or binary inspection.

### For Repository Maintenance

- Keep official handouts in `handouts/`.
- Keep your own lecture summaries in `notes/`.
- Keep assignment-specific study plans and walkthrough notes under `hw1/`, `hw2/`, and so on as the course progresses.
- Prefer Markdown for personal notes so diffs stay readable in Git.

## Current Scope And Limitations

- This repository does not currently contain executable labs, code samples beyond note snippets, or automation scripts.
- Some notes mix direct course topics with broader study guidance, supplementary examples, and outside references.
- The Markdown files are study notes, not official transcripts; they may simplify, reorganize, or expand on lecture content for learning purposes.
- Several notes reference external images, books, slides, or online materials. Those references do not imply those assets are relicensed here.

## Suggested Next Improvements

- Add a top-level `syllabus/` or `schedule.md` if you want a semester timeline.
- Add `labs/` if later assignments include commands, exploits, packet captures, or demo code.
- Add per-topic index pages such as `topics/setuid.md` or `topics/access-control.md` if the note set grows.
- Add `REFERENCES.md` if you want one place to collect textbooks, papers, slide decks, and URLs cited across the notes.

## License

Original notes and documentation in this repository are licensed under `CC BY-NC 4.0`.

- The full legal text is in [LICENSE](LICENSE).
- The repository-specific coverage and exclusions are described in [LICENSE_SCOPE.md](LICENSE_SCOPE.md).
- `handouts/` and other third-party materials are not covered by the repository license.

## Disclaimer

This repository is best treated as a personal or team study archive for coursework. Official course policies, grading rules, and source teaching materials should always take precedence over these notes.
