# HW04 - Pi Memory Locator

HW04 owns its implementation history in a separate Git repository. This course
archive tracks the assignment route, local path, and operating rules, while the
code, experiments, report work, and submission commits stay inside the
GitHub Classroom repository.

## Canonical Repository

- Local path: `homeworks/hw4-pi-memory-JasonLn0711/`
- Remote: `https://github.com/Netdb-NCKU/hw4-pi-memory-JasonLn0711.git`
- Nested branch observed locally: `main`
- Assignment deadline from the bundled spec: `2026-06-09 23:59`; course
  announcements remain the final deadline source.

## Git Routing Rule

- Commit and push HW04 implementation work from
  `homeworks/hw4-pi-memory-JasonLn0711/`.
- Keep this outer course repo as the locator and study archive layer.
- The outer `.gitignore` intentionally ignores
  `homeworks/hw4-pi-memory-JasonLn0711/` so the nested `.git` directory and its
  working tree stay under the HW04 repository's own history.
- If the course archive later needs a static submission copy, create an explicit
  snapshot without `.git` after submission and document that snapshot as an
  archive artifact.

## Working Commands

```bash
cd homeworks/hw4-pi-memory-JasonLn0711
git status --short --branch
.venv/bin/python -m pytest -q
git push origin main
```

Update this locator only when the repository route, deadline, or submission
status changes.
