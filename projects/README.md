# Network Security Projects

This folder is the canonical course-repo home for Network Security term-project and final-demo material.

Use this folder for project briefs, provided lab bundles, implementation notes, report assets, demo evidence, and submission packaging. Keep daily scheduling, capacity decisions, and carry-forward planning in `../../planning-everything-track/`.

## Presentation Scheduling

- Report scheduling archive: `report-scheduling/`
- Instructor notice captured from E3/Gmail on `2026-05-12`.
- Confirmed Doodle booking: `2026-05-27 10:50`.
- Earlier preferred slot from teammate coordination: `2026-05-27 10:40`.
- Travel logistics: paid HSR student tickets are booked for Taipei `09:11` ->
  Hsinchu `09:45`, return Hsinchu `14:08` -> Taipei `14:39`.
- Presentation format: in-class presentation, `10` minutes; Project I / II are separate reports.
- Presenter split currently recorded:
  - Project I - Virus Scanner: 陳靖中 presents the already-built Sentinel package.
  - Project II / other project item: Jason presents, unless the instructor's final registration flow changes the split.

## Current Project Briefs

| Project | Due | Canonical folder | Current objective | Status |
| --- | --- | --- | --- | --- |
| Project I - Virus Scanner | `2026-06-07 23:59` | `project-i-virus-scanner/` | Build a functional signature-based virus scanner with source code, report, and demo. | LMS PDF submitted for grading on `2026-04-22 17:30`; Rust `v0.4.0` package/report/demo evidence preserved; 陳靖中 should present Project I; product continuation split to `../../sentinel-virus-scanner/` |
| Project II - Autonomous APT Agent | `2026-06-07 23:59` | `project-ii-apt-agent/` | Prepare an external-container grading artifact with runnable `/exploit` and `/triage` paths. | Active; student-facing docs live in `project-ii-apt-agent/docs/`, local SPEC/SDD/rubric are drafted, and a classroom-safe runnable scaffold lives in `project-ii-apt-agent/project2-agent-scaffold/`; Jason should present the other project item; Doodle booked for `2026-05-27 10:50` |

## Routing Rule

| Material | Keep here | Keep in planning repo |
| --- | --- | --- |
| Official project PDFs | Yes | Link only |
| Instructor presentation notices and teammate coordination | Yes | Status/date link only |
| Lab bundles and supplied challenge files | Yes | Link only |
| Source code, scripts, reports, demo assets | Yes | Status link only |
| Weekly and daily next actions | No | Yes |
| Capacity tradeoffs and cut rules | No | Yes |
| Distilled reusable concepts | Promote only when useful | `data/knowledge/` |
| Productized continuation | No, link only | Status / capacity locator only |

## Active Ambiguity

Both saved project briefs currently point to the same course and the same deadline. Until the instructor or E3 clarifies whether Project II replaces Project I or both are required, keep both visible and treat `2026-06-07` as blocked by Network Security project work.

## Safety Boundary

Project work must stay inside the provided course lab, local test files, or explicit safe demo inputs. Do not aim project code, exploit logic, scanner tests, or backdoor behavior at real systems, personal files, third-party networks, or live malware.

## Product Continuation

Project I is frozen here as a submitted course artifact. Future product work for
the scanner lives in `../../sentinel-virus-scanner/` under the Sentinel product
family prefix. Keep official course PDFs, LMS status, grading notes, and
submission evidence in this course repo; keep product roadmap, target audience,
and product implementation evolution in the product repo.
