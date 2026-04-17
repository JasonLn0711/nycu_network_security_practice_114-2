# NYCU Network Security Practice 114-2

Study repository for the NYCU `Network Security Practice` course. This is the canonical local home for raw class handouts, lecture notes, homework-prep notes, exam-review notes, and a small agenda-fit checker.

The companion planning repository may track deadlines or promote distilled concepts, but raw network-security course materials should live here first.

## Author

Jason Chia-Sheng Lin  
PhD Student, Institute of Biophotonics, National Yang Ming Chiao Tung University (NYCU)

## Start Here

| Need | Go To | Why |
| --- | --- | --- |
| Course syllabus | [csic30094_syllabus.md](notes/handouts/csic30094_syllabus.md) | Course facts, grading, references, and weekly dates |
| Official or third-party slides/PDFs | [handouts/](handouts/) | Raw course-material archive with normalized filenames |
| Lecture-date notes | [notes/README.md](notes/README.md) | Human-readable lecture routing and topic map |
| Compact handout summaries | [notes/handouts/index.md](notes/handouts/index.md) | One note per handout only when useful study content exists |
| Fast exam review | [midterm_notes/README.md](midterm_notes/README.md) | Plain definitions, intuition, examples, workflows, and recall cues |
| Long slide deep dives | [slide_notes/README.md](slide_notes/README.md) | Research-style extensions too large for compact handout notes |
| Homework preparation | [hw1/README.md](hw1/README.md) | Assignment-specific study sequence and evidence routing |
| Agenda-fit checks | [data/capacity/current.md](data/capacity/current.md), [data/goals/](data/goals/), [scripts/capacity_check.py](scripts/capacity_check.py) | Lightweight local planning inputs and checker |
| Agent operating rules | [AGENTS.md](AGENTS.md) | Repo-specific routing, tone, and planning response contract |
| License boundaries | [LICENSE_SCOPE.md](LICENSE_SCOPE.md) | What is covered by the repo license and what is third-party material |

## Repository Roles

- `handouts/`: raw official or third-party course materials. Use lowercase kebab-case filenames and keep the original course title visible in indexes.
- `notes/`: personal lecture notes and expanded explanations.
- `notes/handouts/`: compact handout-aligned summaries. Do not create empty placeholder notes.
- `midterm_notes/`: exam-oriented notes named by topic, not by capture order.
- `slide_notes/`: long-form slide deep dives or research extensions.
- `hwN/`: assignment-specific plans, walkthrough notes, and evidence.
- `data/capacity/` and `data/goals/`: small planning inputs for near-term capacity checks.
- `scripts/`: standard-library Python 3 helpers.

## Handout Archive

When adding or renaming a raw handout, update this table and [notes/handouts/index.md](notes/handouts/index.md).

| Stored File | Original Title | Topic | Compact Note |
| --- | --- | --- | --- |
| [csic30094-syllabus.docx](handouts/csic30094-syllabus.docx) | `1142_535607syllabus.docx` / `Syllabus` | Course syllabus, grading, references, weekly dates | [csic30094_syllabus.md](notes/handouts/csic30094_syllabus.md) |
| [a-introduction.pdf](handouts/a-introduction.pdf) | `A. Introduction.pdf` | Course introduction | [a_introduction.md](notes/handouts/a_introduction.md) |
| [b1-malware.pdf](handouts/b1-malware.pdf) | `B1. Malware.pdf` | Malware | [b1_malware.md](notes/handouts/b1_malware.md) |
| [b2-environment-variables.pptx](handouts/b2-environment-variables.pptx) | `B2. Environment_Variables.pptx` | Environment variables and related attacks | [b2_environment_variables.md](notes/handouts/b2_environment_variables.md) |
| [c1-linux-security-basics.pdf](handouts/c1-linux-security-basics.pdf) | `C1. Linux_Security_Basics.pdf` | Linux security basics | [c1_linux_security_basics.md](notes/handouts/c1_linux_security_basics.md) |
| [c2-setuid.pdf](handouts/c2-setuid.pdf) | `C2. SetUID.pdf` | Set-UID / privileged programs | [c2_setuid.md](notes/handouts/c2_setuid.md) |
| [c3-access-control-models.pdf](handouts/c3-access-control-models.pdf) | `C3. Access Control Models.pdf` | Access control models | [c3_access_control_models.md](notes/handouts/c3_access_control_models.md) |
| [c4-bell-lapadula.pdf](handouts/c4-bell-lapadula.pdf) | `C4. Bell-LaPadula.pdf` | Bell-LaPadula model | [c4_bell_lapadula.md](notes/handouts/c4_bell_lapadula.md) |
| [c5-selinux.pdf](handouts/c5-selinux.pdf) | `C5. SELinux.pdf` | SELinux | [c5_selinux.md](notes/handouts/c5_selinux.md) |
| [c6-windows-access-control.pdf](handouts/c6-windows-access-control.pdf) | `C6. Windows Access Control.pdf` | Windows access control | [c6_windows_access_control.md](notes/handouts/c6_windows_access_control.md) |
| [d1-tcpip.pdf](handouts/d1-tcpip.pdf) | `D1. TCPIP.pdf` | TCP/IP | Not yet created |
| [d2-end-to-end-encryption.pdf](handouts/d2-end-to-end-encryption.pdf) | `D2. End-to-End Encryption.pdf` | End-to-end encryption | Not yet created |
| [d3-crypto-primitives.pdf](handouts/d3-crypto-primitives.pdf) | `D3. Crypto Primitives.pdf` | Crypto primitives | Not yet created |
| [d4-hash-and-message-authentication-code.pdf](handouts/d4-hash-and-message-authentication-code.pdf) | `D4. Hash and Message Authentication Code.pdf` | Hash and message authentication code | Not yet created |
| [d5-dns-security.pdf](handouts/d5-dns-security.pdf) | `D5. DNS Security.pdf` | DNS security | Not yet created |
| [d6-reconnaissance-vulnerability-scanning.pdf](handouts/d6-reconnaissance-vulnerability-scanning.pdf) | `D6. Reconnaissance - Vulnerability Scanning.pdf` | Reconnaissance and vulnerability scanning | Not yet created |

## Study Indexes

| Area | Index | Current Coverage |
| --- | --- | --- |
| Lecture notes | [notes/README.md](notes/README.md) | Course introduction, malware, environment variables, Linux security basics, access control, Set-UID |
| Handout notes | [notes/handouts/index.md](notes/handouts/index.md) | Syllabus and A through C6 expanded; D1 through D6 archived but pending compact notes |
| Homework 1 | [hw1/README.md](hw1/README.md) | Five-week path from basic computing concepts to beginner Ghidra workflows |
| Exam review | [midterm_notes/README.md](midterm_notes/README.md) | Malware, environment variables, Set-UID, access control, Bell-LaPadula |
| Slide deep dives | [slide_notes/README.md](slide_notes/README.md) | Malware long-form slide/research expansion |

## Naming Conventions

- `handouts/<code>-<topic>.<ext>`: raw course material with normalized lowercase kebab-case names.
- `notes/nsp_YYMMDD_wN.md`: lecture note for a specific date and course week.
- `notes/handouts/<code>_<topic>.md`: compact handout-aligned study note keyed to the bundled handout filename.
- `midterm_notes/<topic>.md`: exam-oriented plain-language note named by topic.
- `slide_notes/<code>-<topic>-deep-dive.md`: long-form slide expansion or research note.
- `hwN/notes/notes_week_N.md`: homework-preparation note grouped by study week.

## Maintenance Rules

- Keep official handouts in `handouts/`; keep personal notes outside `handouts/`.
- Rename raw handouts to lowercase kebab-case and keep original course titles visible in indexes.
- Create a handout note only when it contains useful study content.
- Keep compact handout summaries in `notes/handouts/`, exam recall material in `midterm_notes/`, and large research-style expansions in `slide_notes/`.
- When renaming midterm or slide notes, update the matching folder `README.md` and this root README.
- Use `python3` in commands and examples.

## Agenda And Capacity Checks

This repo includes a tiny planning slice for course commitments only. It is not a replacement for the main planning repository.

1. Update [data/capacity/current.md](data/capacity/current.md) when your real `7`-day or `14`-day sustainable block budget changes.
2. Copy [data/goals/_template.md](data/goals/_template.md) into a new goal file under `data/goals/` and fill its machine-readable metadata.
3. Run `python3 scripts/capacity_check.py status` to diagnose the current agenda.
4. Run `python3 scripts/capacity_check.py can-add --title ... --domain ... --priority ... --deadline ... --blocks-7d ... --blocks-14d ... --flexibility ...` before accepting a new commitment.
5. Answer planning questions in this order: verdict, why, recommendations.

Allowed verdicts are `fit`, `tight`, and `does not fit`.

Example `does not fit` response:

```text
Verdict: does not fit
Why: the next 7 days would require 8.5 blocks against a capacity of 8.0; making it fit would pressure protected domains such as family, health
Recommendations:
- Defer `Journal fit revision` to its next checkpoint instead of stacking more work into this horizon.
- Replace an existing primary lane before accepting this new primary commitment.
- Set a later checkpoint or explicit defer date instead of forcing this into the next 7 to 14 days.
```

Example `tight` response:

```text
Verdict: tight
Why: the task is technically possible, but it would leave little or no safe buffer for drift
Recommendations:
- Shrink `Security midterm readiness` from 4.0 to 2.5 blocks in the next 7 days.
- If you keep this, remove or downgrade one lower-value commitment rather than borrowing from protected life domains.
- Consider shrinking `New workshop abstract` to a smaller first milestone before you try to fit the full request.
```

## Scope And Limitations

- This repository is a study archive, not a web app, dashboard, or database.
- The planning layer is intentionally small: Markdown inputs plus one Python checker.
- Markdown files are study notes, not official transcripts.
- Some notes simplify, reorganize, or expand on lecture material for learning.
- Raw handouts and other third-party materials are not covered by the repository license.

## Suggested Next Improvements

- Expand compact handout notes for D1 through D6 when those topics become active study targets.
- Add `labs/` if later assignments include commands, packet captures, exploit demos, or evidence files.
- Add `REFERENCES.md` if you want one place to collect cited textbooks, papers, slide decks, and URLs.
- Add per-topic indexes only if the note set grows enough that folder-level indexes stop being clear.

## License

Original notes and documentation in this repository are licensed under `CC BY-NC 4.0`.

- The full legal text is in [LICENSE](LICENSE).
- The repository-specific coverage and exclusions are described in [LICENSE_SCOPE.md](LICENSE_SCOPE.md).
- `handouts/` and other third-party materials are not covered by the repository license.

## Disclaimer

This repository is best treated as a personal or team study archive for coursework. Official course policies, grading rules, and source teaching materials should always take precedence over these notes.
