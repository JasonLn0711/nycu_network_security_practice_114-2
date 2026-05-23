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
- Ownership split currently recorded:
  - Project I - Virus Scanner: built/completed by Jason for the two-person group.
  - Project II - Autonomous APT Agent: Jason's local scaffold/recovery attempt
    did not meet the success gate; Chen Jingzhong's package under
    `project-ii-apt-agent/submissions/jingzhong-success/` is the successful
    Project II result.

## Current Project Briefs

| Project | Due | Canonical folder | Current objective | Status |
| --- | --- | --- | --- | --- |
| Project I - Virus Scanner | `2026-06-07 23:59` | `project-i-virus-scanner/` | Build a functional signature-based virus scanner with source code, report, and demo. | LMS PDF submitted for grading on `2026-04-22 17:30`; Rust `v0.4.0` package/report/demo evidence preserved; Project I was completed by Jason for the two-person group; product continuation split to `../../sentinel-virus-scanner/` |
| Project II - Autonomous APT Agent | `2026-06-07 23:59` | `project-ii-apt-agent/` | Preserve the successful external-container package and keep Jason's unsuccessful recovery attempt separate. | Ownership-separated archive: Jason's `project2-agent-scaffold/` is a protocol-complete partial without success; Chen Jingzhong's `project-ii-apt-agent/submissions/jingzhong-success/` package is the successful Project II result; Doodle booked for `2026-05-27 10:50` |

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
