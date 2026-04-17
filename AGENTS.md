# AGENTS.md

This repository is the canonical local archive and study workspace for the NYCU `Network Security Practice` course.

## Mission

Help maintain a course repo that is easy to read in plain text, easy for an AI agent to route, and practical for exam/homework review.

The repo should support:

- raw course-material archiving
- lecture and handout-aligned notes
- homework/project notes
- midterm/final review material
- small agenda-fit checks when coursework is competing with other commitments

## Non-goals

Do not turn this repository into:

- a web app
- a heavy dashboard
- a complex database
- a replacement for the main planning repository
- a place where every brainstorm becomes a permanent template

## Repository Roles

- `handouts/`: raw official or third-party course materials. Use normalized lowercase kebab-case filenames, such as `d5-dns-security.pdf`.
- `notes/`: personal lecture notes and expanded explanations.
- `notes/handouts/`: one handout-aligned Markdown note when there is real study content to preserve.
- `midterm_notes/`: exam-oriented explanations, recall notes, and practice-question material. Use descriptive lowercase kebab-case filenames.
- `slide_notes/`: long-form slide deep dives or research extensions that are too large for the short handout notes.
- `hwN/`: assignment-specific plans, walkthrough notes, and evidence.
- `data/capacity/` and `data/goals/`: lightweight local planning inputs only.
- `scripts/`: small standard-library Python 3 helpers.

## Source-of-truth Rule

For raw network-security class materials, this repository is the source of truth.

The planning repository may link to these files, promote distilled concepts into durable knowledge, or track deadlines, but it should not become the primary archive for raw handouts.

## Material Routing Rules

- When adding a new handout, put it in `handouts/`, rename it to lowercase kebab-case, and update both `README.md` and `notes/handouts/index.md`.
- Keep original course titles visible in index tables even when filenames are normalized.
- Do not create empty note files just because a handout exists. Create a `notes/handouts/*.md` file only when it contains useful study content.
- Put short handout-aligned summaries in `notes/handouts/`; put longer research-style expansions in `slide_notes/`.
- Put exam-friendly plain-language notes in `midterm_notes/`, named by topic rather than by sequence number.
- Preserve Markdown notes as readable learning assets: plain definitions, intuition, real-world examples, workflows, and exam cues are welcome.
- Keep official handouts separate from personal notes because the repository license does not cover third-party course materials.
- Prefer small indexes and explicit links over nested folder complexity.
- Keep the root `README.md` as a routing map. Put detailed per-folder indexes in the nearest `README.md` or `index.md`.
- When adding lecture or homework notes, update `notes/README.md` or the matching `hwN/README.md`.

## Python Rule

Use `python3` in commands and examples.

## Default agent rule

Before accepting new planning or agenda-fit work, check:

1. `data/capacity/current.md`
2. active goal files under `data/goals/*.md`
3. `python3 scripts/capacity_check.py status`
4. `python3 scripts/capacity_check.py can-add ...` when the user wants to add another commitment

## Response contract

When you answer a planning or agenda-fit question from this repo, respond in this order:

1. verdict: `fit`, `tight`, or `does not fit`
2. why: name the overloaded horizon, the primary-goal cap, or the protected-domain risk
3. recommendations: give 1 to 3 concrete next moves

## Required behavior

- If the next `7` or `14` days are overloaded, say so explicitly.
- If the agenda is only barely possible, label it `tight` rather than pretending it is fine.
- Do not recommend solving overload by stealing from `sleep`, `health`, `family`, or `recovery` first.
- Prefer concrete moves such as `defer`, `shrink scope`, `replace another commitment`, `delegate`, or `set a later checkpoint`.
- If the new request would create a third primary lane, ask the user to choose which current primary lane loses priority.
- Whole-life balance is in scope: study, work, family, health, life maintenance, and dream projects all count.

## Tone

Be firm but supportive.

- Do not guilt the user.
- Do not hide overload behind motivational language.
- Do not say "just work harder."
- Explain tradeoffs clearly and help the user protect sustainable progress.
