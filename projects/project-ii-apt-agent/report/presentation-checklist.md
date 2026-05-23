# Presentation Checklist

Use this checklist for the `2026-05-27 10:50` Project II report slot.

## Before Class

- [ ] Decide who is presenting Project II.
- [ ] Prepare a `9` slide deck from `slide-deck-outline.md`.
- [ ] Keep the deck under `10` minutes in rehearsal.
- [ ] Open these files in tabs before presenting:
  - [ ] `report/evidence/success.txt`
  - [ ] `report/evidence/exploit-log.txt`
  - [ ] `report/evidence/target_info.json`
  - [ ] `report/slide-deck-outline.md` or exported slides
- [ ] If using terminal demo, run the commands from
  `optional-demo-runbook.md` once before class.
- [ ] If using Docker live demo, pre-build images and rehearse the exact command
  sequence immediately before class.
- [ ] Keep evidence screenshots or saved files ready in case Docker is slow.
- [ ] Confirm the presentation slot: `2026-05-27 10:50`.
- [ ] Confirm time limit: `10` minutes.

## During The Report

- [ ] Start with the result and scope.
- [ ] Explain the EC/IC/shared-volume grading loop.
- [ ] Show `/exploit` and `/triage` roles.
- [ ] Explain analyzer output and discovered `execute_task`.
- [ ] Explain payload flow at a conceptual level.
- [ ] Show success evidence.
- [ ] Mention bounded lab-only safety boundary.
- [ ] Finish with one concise conclusion.

## If Asked About Division Of Work

Use this wording:

> 我們是兩人分組分工完成這份 Project II。報告會以本組最後 package 的系統功能、
> 系統特色與成功證據為主，細節包含 `/exploit`、`/triage`、target analysis、
> adaptive probing，以及 `/shared/success.txt`。

Use this only when the instructor asks about division of work; keep the main
report focused on system function and system features.

## If Asked Whether It Was A Live Run

Use this wording:

> The package contains saved success evidence and can be rerun in the course lab
> environment. For the in-class `10` minute report, I am showing the deterministic
> evidence and system flow first because a full Docker startup is not the core
> requirement and can waste presentation time.

## After Class

- [ ] Record any instructor feedback.
- [ ] Save final slide deck or exported PDF under this `report/` folder.
- [ ] If a live run was performed, save the terminal transcript.
- [ ] Confirm E3 report upload responsibility before `2026-06-07`.
