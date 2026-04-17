# NYCU Network Security Practice 114-2

Study repository for the NYCU `Network Security Practice` course. This repository is the canonical local home for raw class handouts, lecture notes, homework-prep notes, exam-review notes, and a lightweight planning/governance slice for agenda-fit checks.

The companion planning repository may track deadlines or promote durable concepts, but raw network-security course materials should live here first.

## Author

Jason Chia-Sheng Lin  
PhD Student, Institute of Biophotonics, National Yang Ming Chiao Tung University (NYCU)

## What This Repository Contains

- `notes/`
  - Weekly lecture notes and expanded summaries tied to class dates.
  - Handout-aligned study notes under `notes/handouts/`, with one Markdown note only when there is real study content to preserve.
  - Focus areas currently include system security, access control, network foundations, DNS, crypto, reconnaissance, and vulnerability scanning.
- `midterm_notes/`
  - Exam-oriented plain-language explanations and recall material.
- `hw1/notes/`
  - A structured five-week self-study track for Homework 1.
  - The sequence starts from fundamentals and gradually moves toward Linux command-line usage, basic C reading, executable structure, and beginner Ghidra workflows.
- `handouts/`
  - Raw reference material such as PDFs and slides related to the course topics.
  - Filenames are normalized to lowercase kebab-case for stable links and easy shell use.
  - These appear to be official course or third-party teaching materials and are not covered by the repository's documentation license.
- `data/capacity/` and `data/goals/`
  - Structured Markdown inputs for near-term capacity and active goals.
  - These files let an agent or CLI checker decide whether another commitment fits the current `7`-day and `14`-day agenda.
- `scripts/`
  - Small Python helpers for repo-local planning checks.
  - `scripts/capacity_check.py` reports whether the agenda is `fit`, `tight`, or overloaded/reject-worthy before you add more work.

## Repository Layout

```text
.
├── handouts/
│   ├── a-introduction.pdf
│   ├── b1-malware.pdf
│   ├── b2-environment-variables.pptx
│   ├── c1-linux-security-basics.pdf
│   ├── c2-setuid.pdf
│   ├── c3-access-control-models.pdf
│   ├── c4-bell-lapadula.pdf
│   ├── c5-selinux.pdf
│   ├── c6-windows-access-control.pdf
│   ├── d1-tcpip.pdf
│   ├── d2-end-to-end-encryption.pdf
│   ├── d3-crypto-primitives.pdf
│   ├── d4-hash-and-message-authentication-code.pdf
│   ├── d5-dns-security.pdf
│   └── d6-reconnaissance-vulnerability-scanning.pdf
├── data/
│   ├── capacity/
│   │   └── current.md
│   └── goals/
│       └── _template.md
├── hw1/
│   └── notes/
│       ├── notes_week_1.md
│       ├── notes_week_2.md
│       ├── notes_week_3.md
│       ├── notes_week_4.md
│       └── notes_week_5.md
├── midterm_notes/
│   ├── note_1.md
│   ├── note_2.md
│   ├── note_3.md
│   └── note_4.md
├── scripts/
│   └── capacity_check.py
├── slide_notes/
│   └── B1_malware.md
└── notes/
    ├── handouts/
    │   ├── a_introduction.md
    │   ├── b1_malware.md
    │   ├── b2_environment_variables.md
    │   ├── c1_linux_security_basics.md
    │   ├── c2_setuid.md
    │   ├── c3_access_control_models.md
    │   ├── c4_bell_lapadula.md
    │   ├── c5_selinux.md
    │   ├── c6_windows_access_control.md
    │   └── index.md
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

### Handout Notes

| File | Tied Handout | Status / Coverage |
| --- | --- | --- |
| `notes/handouts/a_introduction.md` | `handouts/a-introduction.pdf` | Course structure, prerequisites, grading, and topic map |
| `notes/handouts/b1_malware.md` | `handouts/b1-malware.pdf` | Malware history, taxonomy, propagation, concealment, and detection mindset |
| `notes/handouts/b2_environment_variables.md` | `handouts/b2-environment-variables.pptx` | Process environments, inheritance, attack surfaces, and safer invocation patterns |
| `notes/handouts/c1_linux_security_basics.md` | `handouts/c1-linux-security-basics.pdf` | Linux identities, permissions, ACLs, privilege mechanisms, and authentication basics |
| `notes/handouts/c2_setuid.md` | `handouts/c2-setuid.pdf` | Set-UID mechanics, attack surfaces, capability leaks, and least-privilege design |
| `notes/handouts/c3_access_control_models.md` | `handouts/c3-access-control-models.pdf` | Policy vs model, access matrix, ACLs vs capabilities, DAC/MAC, and later models |
| `notes/handouts/c4_bell_lapadula.md` | `handouts/c4-bell-lapadula.pdf` | Confidentiality lattice, simple security condition, `*-property`, and model limitations |
| `notes/handouts/c5_selinux.md` | `handouts/c5-selinux.pdf` | SELinux contexts, type enforcement, transitions, policy modules, and audit-driven debugging |
| `notes/handouts/c6_windows_access_control.md` | `handouts/c6-windows-access-control.pdf` | Windows tokens, descriptors, integrity levels, UI isolation, and UAC |
| Not yet created | `handouts/d1-tcpip.pdf` | Pending handout note |
| Not yet created | `handouts/d2-end-to-end-encryption.pdf` | Pending handout note |
| Not yet created | `handouts/d3-crypto-primitives.pdf` | Pending handout note |
| Not yet created | `handouts/d4-hash-and-message-authentication-code.pdf` | Pending handout note |
| Not yet created | `handouts/d5-dns-security.pdf` | Pending handout note |
| Not yet created | `handouts/d6-reconnaissance-vulnerability-scanning.pdf` | Pending handout note |
| `notes/handouts/index.md` | All handouts | Directory index and recommended reading order |

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
| `handouts/a-introduction.pdf` | Course introduction |
| `handouts/b1-malware.pdf` | Malware |
| `handouts/b2-environment-variables.pptx` | Environment variables and related attacks |
| `handouts/c1-linux-security-basics.pdf` | Linux security basics |
| `handouts/c2-setuid.pdf` | Set-UID / privileged programs |
| `handouts/c3-access-control-models.pdf` | Access control models |
| `handouts/c4-bell-lapadula.pdf` | Bell-LaPadula model |
| `handouts/c5-selinux.pdf` | SELinux |
| `handouts/c6-windows-access-control.pdf` | Windows access control |
| `handouts/d1-tcpip.pdf` | TCP/IP |
| `handouts/d2-end-to-end-encryption.pdf` | End-to-end encryption |
| `handouts/d3-crypto-primitives.pdf` | Crypto primitives |
| `handouts/d4-hash-and-message-authentication-code.pdf` | Hash and message authentication code |
| `handouts/d5-dns-security.pdf` | DNS security |
| `handouts/d6-reconnaissance-vulnerability-scanning.pdf` | Reconnaissance and vulnerability scanning |

## Naming Conventions

- `notes/nsp_YYMMDD_wN.md`
  - Course note for a specific lecture date and week number.
  - Example: `nsp_260311_w3.md` corresponds to a note associated with `2026-03-11`, week 3.
- `notes/handouts/<code>_<topic>.md`
  - Handout-aligned summary note keyed to the bundled slide filename.
  - Example: `c2_setuid.md` matches `handouts/c2-setuid.pdf`.
- `handouts/<code>-<topic>.<ext>`
  - Raw course material with normalized lowercase kebab-case names.
  - Keep the course code prefix, such as `d6`, so ordering remains obvious.
- `hw1/notes/notes_week_N.md`
  - Homework-preparation note grouped by study week rather than lecture date.

## How To Use This Repository

### For Review Before or After Class

1. Start with the relevant file in `handouts/` to see the official topic framing.
2. Read the matching file in `notes/handouts/` for a handout-specific concept map and review checklist.
3. Read the matching file in `notes/` for expanded explanations, mixed-language lecture detail, or broader study framing.
4. Add your own clarifications, examples, command snippets, or diagrams directly into the Markdown notes.

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
- Rename handouts to lowercase kebab-case and keep the original course title visible in index tables.
- Keep your own lecture summaries in `notes/`.
- Keep exam-specific explanations in `midterm_notes/`.
- Keep assignment-specific study plans and walkthrough notes under `hw1/`, `hw2/`, and so on as the course progresses.
- Prefer Markdown for personal notes so diffs stay readable in Git.
- When adding or renaming a handout, update both this README and `notes/handouts/index.md`.
- Create a handout note only when it contains useful study content; do not add empty placeholder notes.

### For Agenda And Capacity Checks

1. Update [data/capacity/current.md](data/capacity/current.md) when your real `7`-day or `14`-day sustainable block budget changes.
2. Copy [data/goals/_template.md](data/goals/_template.md) into a new goal file under `data/goals/` and fill its machine-readable metadata.
3. Run `python3 scripts/capacity_check.py status` to diagnose the current agenda.
4. Run `python3 scripts/capacity_check.py can-add --title ... --domain ... --priority ... --deadline ... --blocks-7d ... --blocks-14d ... --flexibility ...` before accepting a new commitment.
5. Let an agent use the checker result as the first response layer: verdict first, reason second, recommendations third.

Example supportive rejection:

```text
Verdict: reject
Why: the next 7 days would require 8.5 blocks against a capacity of 8.0; making it fit would pressure protected domains such as family, health
Recommendations:
- Defer `Journal fit revision` to its next checkpoint instead of stacking more work into this horizon.
- Replace an existing primary lane before accepting this new primary commitment.
- Set a later checkpoint or explicit defer date instead of forcing this into the next 7 to 14 days.
```

Example `tight` but still possible recommendation:

```text
Verdict: tight
Why: the task is technically possible, but it would leave little or no safe buffer for drift
Recommendations:
- Shrink `Security midterm readiness` from 4.0 to 2.5 blocks in the next 7 days.
- If you keep this, remove or downgrade one lower-value commitment rather than borrowing from protected life domains.
- Consider shrinking `New workshop abstract` to a smaller first milestone before you try to fit the full request.
```

## Current Scope And Limitations

- This repository still does not contain executable labs or a full planning application.
- The planning layer is intentionally small: plain Markdown inputs plus one Python checker, not a dashboard or database product.
- Some notes mix direct course topics with broader study guidance, supplementary examples, and outside references.
- The Markdown files are study notes, not official transcripts; they may simplify, reorganize, or expand on lecture content for learning purposes.
- Several notes reference external images, books, slides, or online materials. Those references do not imply those assets are relicensed here.
- Handout notes for D1 through D6 have not been expanded yet; the raw handouts are archived and indexed.

## Suggested Next Improvements

- Add a top-level `syllabus/` or `schedule.md` if you want a semester timeline.
- Expand handout notes for D1 through D6 when those topics become active study targets.
- Add `labs/` if later assignments include commands, exploits, packet captures, or demo code.
- Add per-topic index pages such as `topics/setuid.md` or `topics/access-control.md` if the note set grows.
- Add `REFERENCES.md` if you want one place to collect textbooks, papers, slide decks, and URLs cited across the notes.
- Extend the planning slice with weekly review or metrics only if the lightweight checker stops being enough.

## License

Original notes and documentation in this repository are licensed under `CC BY-NC 4.0`.

- The full legal text is in [LICENSE](LICENSE).
- The repository-specific coverage and exclusions are described in [LICENSE_SCOPE.md](LICENSE_SCOPE.md).
- `handouts/` and other third-party materials are not covered by the repository license.

## Disclaimer

This repository is best treated as a personal or team study archive for coursework. Official course policies, grading rules, and source teaching materials should always take precedence over these notes.
