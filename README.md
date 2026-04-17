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
| Official or third-party slides/PDFs | [handouts/README.md](handouts/README.md) | Raw course-material archive with normalized filenames |
| Lecture-date notes | [notes/README.md](notes/README.md) | Human-readable lecture routing and topic map |
| Compact handout summaries | [notes/handouts/index.md](notes/handouts/index.md) | One note per handout only when useful study content exists |
| Fast exam review | [midterm_notes/README.md](midterm_notes/README.md) | Plain definitions, intuition, examples, workflows, and recall cues |
| Long slide deep dives | [slide_notes/README.md](slide_notes/README.md) | Research-style extensions too large for compact handout notes |
| Homework preparation | [hw1/README.md](hw1/README.md) | Assignment-specific study sequence and evidence routing |
| Agenda-fit checks | [data/README.md](data/README.md) | Capacity inputs, goal metadata, commands, and response contract |
| Agent operating rules | [AGENTS.md](AGENTS.md) | Repo-specific routing, tone, and planning response contract |
| License boundaries | [LICENSE_SCOPE.md](LICENSE_SCOPE.md) | What is covered by the repo license and what is third-party material |

## Repository Map

| Path | Role | Detailed Index |
| --- | --- | --- |
| `handouts/` | Raw official or third-party course materials | [handouts/README.md](handouts/README.md) |
| `notes/` | Personal lecture notes and expanded explanations | [notes/README.md](notes/README.md) |
| `notes/handouts/` | Compact handout-aligned study notes | [notes/handouts/index.md](notes/handouts/index.md) |
| `midterm_notes/` | Exam-oriented recall and explanation notes | [midterm_notes/README.md](midterm_notes/README.md) |
| `slide_notes/` | Long-form slide deep dives or research extensions | [slide_notes/README.md](slide_notes/README.md) |
| `hwN/` | Assignment-specific notes, walkthroughs, and evidence | [hw1/README.md](hw1/README.md) |
| `data/capacity/`, `data/goals/` | Lightweight local planning inputs | [data/README.md](data/README.md) |
| `scripts/` | Standard-library Python 3 helpers | [capacity_check.py](scripts/capacity_check.py) |
| `tests/` | Unit tests for repo-local helpers | [test_capacity_check.py](tests/test_capacity_check.py) |

## Naming And Routing

- Raw handouts use lowercase kebab-case and keep their course prefix, such as `d5-dns-security.pdf`.
- Handout notes use lowercase snake_case and live in `notes/handouts/`, such as `c2_setuid.md`.
- Midterm notes use descriptive lowercase kebab-case topic names, such as `setuid-privileged-programs.md`.
- Slide deep dives use source-code-first names, such as `b1-malware-deep-dive.md`.
- Homework notes stay under the matching `hwN/` folder unless the concept is useful beyond that assignment.
- The root README is a routing map. Detailed tables belong in the nearest folder README or index.
- Use `python3` in commands and examples.

## Maintenance Checklist

When adding a new raw handout:

1. Put the raw file in `handouts/` with a normalized lowercase kebab-case filename.
2. Add the original course title and stored filename to [handouts/README.md](handouts/README.md).
3. Add or update the mapping in [notes/handouts/index.md](notes/handouts/index.md).
4. Create a `notes/handouts/*.md` note only when there is real study content to preserve.
5. Keep official handouts separate from personal notes because the repository license does not cover third-party course materials.

When adding study notes:

1. Put lecture-date notes in `notes/`.
2. Put compact slide-aligned summaries in `notes/handouts/`.
3. Put exam recall material in `midterm_notes/`.
4. Put large research-style extensions in `slide_notes/`.
5. Update the nearest folder README or index.

## Agenda Checks

This repo includes a tiny planning slice for course commitments only. It is not a replacement for the main planning repository.

Quick commands:

```bash
python3 scripts/capacity_check.py status
python3 scripts/capacity_check.py can-add --title "..." --domain course --priority secondary --deadline YYYY-MM-DD --blocks-7d 1 --blocks-14d 2 --flexibility movable
```

See [data/README.md](data/README.md) for the metadata files, response contract, and example verdicts.

## Scope And Limitations

- This repository is a study archive, not a web app, dashboard, or database.
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
