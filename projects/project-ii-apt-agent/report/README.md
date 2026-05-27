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

This folder is the presentation/report packet for that classroom task. It uses
the team's successful Project II package as the presentation evidence base and
keeps classroom-facing wording focused on the two-person group result.

## Recommended Format

Use a slide deck with an optional short demo segment.

Time budget:

| Segment | Time | Purpose |
| --- | ---: | --- |
| Architecture, function, feature, and success evidence | `7` minutes | Explain what the system does and why it satisfies the project. |
| Optional short demo / evidence walkthrough | `2` minutes | Show success log, `success.txt`, payload flow, or a pre-verified run. |
| Conclusion and limitation | `1` minute | State bounded lab scope, result, and caveat. |

Use saved evidence as the default classroom demonstration. The safest classroom
plan is:

1. present the architecture and feature slides;
2. show saved evidence from the successful package;
3. run only a very short pre-tested demo if the environment is already warm;
4. fall back to saved screenshots/logs immediately if anything is slow.

## File Map

| File | Role |
| --- | --- |
| `10-minute-presentation-plan.md` | Minute-by-minute plan and slide timing. |
| `presentation-full-10-minute-zh.md` | Complete Traditional Chinese 10-minute presentation deck with actual saved lab evidence, experimental data, and Mermaid diagrams. |
| `presentation-full-10-minute-english.md` | Complete English 10-minute presentation deck with actual saved lab evidence, experimental data, and Mermaid diagrams. |
| `presentation-part-1-lab-overview.md` | Markdown presentation for the first lab-overview section, including architecture and process Mermaid diagrams. |
| `presentation-part-2-vulnerability-source.md` | Markdown presentation continuing the walkthrough with `server.cpp` data flow, buffer overflow source, and a Mermaid process diagram. |
| `presentation-part-3-exploit-payload-stack.md` | Markdown presentation continuing the walkthrough with `EC/exploit`, payload layout, stack frames, offset, GDB, and a Mermaid process diagram. |
| `presentation-part-4-address-elf-protections.md` | Markdown presentation continuing the walkthrough with little-endian address packing, ELF binary analysis, Linux protections, and a Mermaid process diagram. |
| `slide-deck-outline.md` | Slide titles, visual suggestions, bullet content, and talk track. |
| `speaker-script.md` | A full Traditional Chinese speaker script that fits the `10` minute format. |
| `speaker-script-full-10-minute-zh.md` | Full Traditional Chinese word-for-word script aligned to `presentation-full-10-minute-zh.md`. |
| `optional-demo-runbook.md` | Safe demo choices, commands/evidence to show, and fallback plan. |
| `presentation-checklist.md` | Before-class, during-class, and after-class checklist. |
| `evidence/` | Team-facing copies of the saved evidence files to open during class. |

## Source Evidence

Use these as the evidence base:

| Evidence | Path |
| --- | --- |
| Classroom evidence folder | `evidence/` |
| Saved success artifact | `evidence/success.txt` |
| Saved exploit log | `evidence/exploit-log.txt` |
| Saved target analysis | `evidence/target_info.json` |
| Saved state | `evidence/state.json` |

Internal audit references stay outside the classroom flow:

- `../OWNERSHIP_AND_OUTCOME.md`
- `../PROJECT_II_COMPARATIVE_ANALYSIS.md`

Teammate-provided presentation source note:

- `../submissions/jingzhong-success/report/autonomous-apt-agent-technical-report-jingzhong-reference-2026-05-26.md`

Use this Markdown note for presentation preparation when a fuller technical
explanation is needed. Keep the classroom packet concise and use the archived
evidence files as the demonstration source.

## Presentation Stance

Present Project II as a two-person team deliverable with clear system function,
system features, and saved success evidence.

Recommended wording:

> Our team implemented a bounded autonomous exploit agent for the course lab.
> The system provides `/exploit` and `/triage`, uses the shared-volume grading
> loop, and preserves success evidence showing `/shared/success.txt`.

Use the class time for the required system function demonstration and system
feature explanation. Keep internal development history outside the main talk.
