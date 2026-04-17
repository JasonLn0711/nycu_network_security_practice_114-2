# AGENTS.md

This repository is the canonical local archive and study workspace for NYCU `Network Security Practice`.

## Mission

Help maintain a course repo that is easy to read in plain text, easy for an AI agent to route, and practical for exam, homework, lab, and final-demo review.

The repo should support:

- raw course-material archiving
- student-facing lecture modules
- curated handout notes
- homework and lab practice material
- security practice resources
- small agenda-fit checks when coursework is competing with other commitments

## Non-goals

Do not turn this repository into:

- a web app
- a heavy dashboard
- a complex database
- a replacement for the main planning repository
- a place where every brainstorm becomes a permanent template

## Repository Roles

- `syllabus/`: course overview, grading facts, weekly dates, and syllabus-derived routing.
- `lectures/`: weekly topic modules. Each week should include `README.md`, `key-concepts.md`, and `examples.md`; add deeper notes only when they preserve real study value.
- `handouts/`: curated Markdown handouts for students.
- `handouts/raw/`: raw official or third-party course materials. Use normalized lowercase kebab-case filenames, such as `d5-dns-security.pdf`.
- `labs/`: hands-on practice guides and expected evidence.
- `homeworks/`: assignment-specific instructions, expected outputs, notes, and optional solutions when real solution material exists.
- `datasets/`: packet captures, binaries, logs, and sample inputs.
- `tools/`: small local helpers. The capacity checker lives in `tools/capacity-check/`.
- `misc/`: temporary parking only when no better folder fits.

## Source-of-truth Rule

For raw network-security class materials, this repository is the source of truth.

The planning repository may link to these files, promote distilled concepts into durable knowledge, or track deadlines, but it should not become the primary archive for raw handouts.

## Material Routing Rules

- When adding a new official handout, put the raw file in `handouts/raw/`, rename it to lowercase kebab-case, and update `handouts/README.md`.
- Update the root `README.md` only when the repository routing map itself changes.
- Keep original course titles visible in index tables even when filenames are normalized.
- Do not create empty note files just because a handout exists. Create curated Markdown only when it contains useful study content.
- Put short handout-aligned summaries in `handouts/`.
- Put lecture notes, exam-review notes, and long-form deep dives under the most relevant `lectures/weekXX-*` folder.
- Put assignment-specific plans, walkthrough notes, and evidence under `homeworks/`.
- Preserve Markdown notes as readable learning assets: plain definitions, intuition, real-world examples, workflows, and exam cues are welcome.
- Keep official handouts separate from personal notes because the repository license does not cover third-party course materials.
- Prefer small indexes and explicit links over nested folder complexity.
- Keep folder depth to three levels for student-facing material.

## Python Rule

Use `python3` in commands and examples.

## Default Agent Rule

Before accepting new planning or agenda-fit work, check:

1. `tools/capacity-check/capacity/current.md`
2. active goal files under `tools/capacity-check/goals/*.md`
3. `python3 tools/capacity-check/capacity_check.py status`
4. `python3 tools/capacity-check/capacity_check.py can-add ...` when the user wants to add another commitment

## Response Contract

When you answer a planning or agenda-fit question from this repo, respond in this order:

1. verdict: `fit`, `tight`, or `does not fit`
2. why: name the overloaded horizon, the primary-goal cap, or the protected-domain risk
3. recommendations: give 1 to 3 concrete next moves

## Required Behavior

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
