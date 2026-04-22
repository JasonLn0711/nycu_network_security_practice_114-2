# Changelog

## 0.4.0 - 2026-04-22

- Added a private-repository export tool that builds a curated handoff package for the required private GitHub/GitLab submission repo.
- Added export-manifest safety checks so the package excludes the official project PDF, LaTeX build artifacts, the removed report draft, and any literal EICAR file.
- Added standard-library tests for the export dry-run and copy path.
- Expanded the release-readiness gate to verify the private-repo export plan.
- Reorganized project docs around first-principle deliverables: source, report, demo, evidence, and submission package.
- Moved durable design notes into `docs/`, moved the demo runbook into `demo/`, and merged the private-repo handoff plus checklist into `report/submission-package.md`.

## 0.3.0 - 2026-04-22

- Added a standard-library Bloom filter for hash-signature membership pre-checks.
- Kept exact MD5/SHA-256 hash-map verification after the Bloom pre-check so Bloom false positives cannot create infected findings.
- Added Bloom-filter metadata to JSON and Markdown scan reports.
- Expanded tests and release checks to cover Bloom-filter construction, hash matching, report metadata, and release evidence.
- Updated the report package to describe the implemented hash map, Bloom filter, and Aho-Corasick data structures.

## 0.2.0 - 2026-04-22

- Added Aho-Corasick byte-pattern matching with stream state across chunks.
- Added scan-engine metadata to JSON and Markdown reports.
- Added safe synthetic pattern benchmark artifacts.
- Added release controls: `VERSION`, `Makefile`, and `scripts/check_release.py`.
- Added explicit symbolic-link skipping with scan metadata and skipped-result evidence.
- Added standards alignment notes and EICAR reference-hash tests without storing an EICAR file.
- Expanded the standard-library test suite to cover overlapping patterns, streamed boundary matching, report metadata, and CLI version output.
- Updated the safe mock-virus signature hashes so the demo fixture matches MD5, SHA-256, and hex-pattern evidence.
- Updated report, demo, handoff, and planning documentation for the algorithmic-hardening checkpoint.

## 0.1.0 - 2026-04-22

- Built the initial safe Sentinel scanner package.
- Added signature loading, MD5/SHA-256 matching, chunked hex-pattern matching, heuristic suspicious flags, JSON/Markdown reporting, safe demo tree, evidence manifest, and report package.
