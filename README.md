# NYCU 114-2 Network Security Practices - Attack and Defense

This repository is the course workspace for NYCU 114-2 Network Security Practices. It organizes official handouts, lecture notes, labs, homework material, and security practice resources into a clean study path.

## Course Description

The course studies practical attack and defense across systems, networks, and applications. Students learn how vulnerabilities appear, how exploits abuse real mechanisms, and how defensive controls reduce risk.

Assessment:

- Homework: 70%
- Final report and demo: 30%

## Topics Covered

- Vulnerabilities and exploits
- Cryptographic primitives
- Network security
- Host security
- Code integrity
- Web security

## Repository Structure

```text
syllabus/    Course overview and grading facts
lectures/    Weekly topic modules with concepts and examples
handouts/    Curated study handouts plus raw official materials
labs/        Hands-on practice tasks and evidence guides
homeworks/   Assignment instructions, expected outputs, and notes
projects/    Term-project briefs, reports, demos, lab bundles, and source routing
datasets/    Packet captures, binaries, logs, and sample inputs
tools/       Small local helper scripts
misc/        Temporary parking only when no better folder fits
```

## Organization Principles

- Keep one live source of truth for each artifact.
- Keep raw official material separate from student notes.
- Keep current deliverables in the working tree; let Git history preserve superseded drafts and prototypes.
- Prefer folder-level `README.md` files over duplicate cross-references.
- Use generated folders such as `dist/`, `build/`, and `target/` only as rebuildable output.

## How To Use This Repo

1. Start with `syllabus/course-overview.md`.
2. Use `lectures/README.md` to choose the matching `lectures/weekXX-*/README.md`.
3. Use `key-concepts.md` for definitions and exam framing.
4. Use `examples.md` and `labs/` for practice.
5. Use `homeworks/` only for assignment-specific work.
6. Use `projects/` for term-report and final-demo work.
7. Check `handouts/raw/` when you need the original course files.

## Weekly Learning Path

| Week | Topic | Start Here |
| --- | --- | --- |
| 01 | Introduction | `lectures/week01-introduction/` |
| 02 | Vulnerabilities and Exploits | `lectures/week02-vulnerabilities-exploits/` |
| 03 | Cryptographic Primitives | `lectures/week03-crypto-primitives/` |
| 04 | Network Security | `lectures/week04-network-security/` |
| 05 | Host Security | `lectures/week05-host-security/` |
| 06 | Code Integrity | `lectures/week06-code-integrity/` |
| 07 | Web Security | `lectures/week07-web-security/` |

## Term Projects

| Project | Start Here | Current note |
| --- | --- | --- |
| Project I - Virus Scanner | `projects/project-i-virus-scanner/` | Build a signature-based scanner with source code, report, and demo. |
| Project II - Autonomous APT Agent | `projects/project-ii-apt-agent/` | Prepare the external-container `/exploit` and `/triage` grading artifact. |

The planning repository should track schedule, capacity, and next actions. This course repository owns the project briefs, lab bundles, implementation notes, report assets, and demo evidence.

## Tools Setup

Recommended tools:

- Wireshark for packet inspection
- Linux shell utilities for file, process, and permission practice
- Ghidra for binary analysis and reverse engineering
- Python 3 for helper scripts and small checks

Use `python3` in all commands.

## Raw Materials And License Boundary

Official and third-party materials are stored in `handouts/raw/`. They remain under their original terms and are not covered by the repository license. Curated Markdown explanations, indexes, homework notes, and lab guides are original study materials unless a file states otherwise.

## Maintenance Notes

- Add new official files to `handouts/raw/`.
- Add short curated handouts to `handouts/`.
- Add lecture-specific notes under the matching `lectures/weekXX-*` folder.
- Add assignment-specific material under `homeworks/`.
- Add term-project material under `projects/`.
- Add practice tasks under `labs/`, with expected evidence listed in the lab README.
- Remove or rename obsolete parallel artifacts instead of keeping multiple live copies with unclear authority.
