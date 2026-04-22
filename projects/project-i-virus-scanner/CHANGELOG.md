# Changelog

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
