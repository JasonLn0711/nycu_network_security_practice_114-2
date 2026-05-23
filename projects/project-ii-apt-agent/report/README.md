# Project II Class Report Packet

Purpose: prepare the `10` minute in-class presentation for Project II -
Autonomous APT Agent.

The instructor notice says the report format is:

- in-class presentation;
- `10` minutes;
- Project I / Project II are separate presentations;
- required content:
  - system function demonstration;
  - system feature explanation.

This folder is the presentation/report packet for that classroom task. It is
separate from `../submissions/jingzhong-success/report/`, which preserves the
incoming Word report and extracted media from Chen Jingzhong's successful
package.

## Recommended Format

Use a slide deck with an optional short demo segment.

Time budget:

| Segment | Time | Purpose |
| --- | ---: | --- |
| Architecture, function, feature, and success evidence | `7` minutes | Explain what the system does and why it satisfies the project. |
| Optional short demo / evidence walkthrough | `2` minutes | Show success log, `success.txt`, payload flow, or a pre-verified run. |
| Conclusion and limitation | `1` minute | State bounded lab scope, result, and caveat. |

Do not rely on a full from-scratch Docker rebuild during class. The safest
classroom plan is:

1. present the architecture and feature slides;
2. show saved evidence from the successful package;
3. run only a very short pre-tested demo if the environment is already warm;
4. fall back to saved screenshots/logs immediately if anything is slow.

## File Map

| File | Role |
| --- | --- |
| `10-minute-presentation-plan.md` | Minute-by-minute plan and slide timing. |
| `slide-deck-outline.md` | Slide titles, visual suggestions, bullet content, and talk track. |
| `speaker-script.md` | A full Traditional Chinese speaker script that fits the `10` minute format. |
| `optional-demo-runbook.md` | Safe demo choices, commands/evidence to show, and fallback plan. |
| `presentation-checklist.md` | Before-class, during-class, and after-class checklist. |

## Source Evidence

Use these as the evidence base:

| Evidence | Path |
| --- | --- |
| Successful package | `../submissions/jingzhong-success/` |
| Saved success artifact | `../submissions/jingzhong-success/lab/shared/success.txt` |
| Saved exploit log | `../submissions/jingzhong-success/lab/shared/exploit-log.txt` |
| Saved target analysis | `../submissions/jingzhong-success/lab/shared/target_info.json` |
| Extracted report text | `../submissions/jingzhong-success/report/autonomous-apt-agent-report-extracted-text.txt` |
| Ownership and outcome boundary | `../OWNERSHIP_AND_OUTCOME.md` |
| Technical comparison | `../PROJECT_II_COMPARATIVE_ANALYSIS.md` |

## Presentation Stance

Present the successful Project II package, not Jason's failed recovery line.

Recommended wording:

> This Project II package implements a bounded autonomous exploit agent for the
> course lab. The successful package was completed by Chen Jingzhong; Jason's
> earlier scaffold/recovery line is preserved separately as a failed analysis
> branch and should not be presented as the successful result.

If time is tight, do not discuss the failure branch unless asked. The required
class content is system function demonstration and system feature explanation.

