from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .heuristics import run_heuristics
from .matchers import PatternScanEngine, find_hash_matches, scan_file_content
from .reporting import FileResult, build_report
from .signatures import SEVERITY_RANK, SignatureDatabase


SYMLINK_SKIP_REASON = "Symbolic link skipped to keep scans inside the explicit target tree."


def scan_directory(target: str | Path, database: SignatureDatabase) -> dict:
    root = Path(target)
    started_at = _timestamp()
    results: list[FileResult] = []
    pattern_engine = PatternScanEngine(database.patterns)
    scan_metadata = {
        **database.hash_filter.metadata(),
        **pattern_engine.metadata(),
        "traversal_policy": "deterministic-rglob-files",
        "symlink_policy": "skip",
    }

    if root.is_symlink():
        finished_at = _timestamp()
        return build_report(
            target=root,
            started_at=started_at,
            finished_at=finished_at,
            results=[
                FileResult(
                    path=str(root),
                    status="skipped",
                    severity="info",
                    skip_reason=SYMLINK_SKIP_REASON,
                )
            ],
            signature_schema_version=database.schema_version,
            scan_metadata=scan_metadata,
        )

    if not root.exists():
        finished_at = _timestamp()
        return build_report(
            target=root,
            started_at=started_at,
            finished_at=finished_at,
            results=[
                FileResult(
                    path=str(root),
                    status="error",
                    severity="high",
                    error="Target path does not exist.",
                )
            ],
            signature_schema_version=database.schema_version,
            scan_metadata=scan_metadata,
        )

    if root.is_file():
        results.append(scan_file(root, root, database, pattern_engine))
    else:
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                results.append(
                    FileResult(
                        path=_display_path(path, root),
                        status="skipped",
                        severity="info",
                        skip_reason=SYMLINK_SKIP_REASON,
                    )
                )
            elif path.is_file():
                results.append(scan_file(path, root, database, pattern_engine))

    finished_at = _timestamp()
    return build_report(
        target=root,
        started_at=started_at,
        finished_at=finished_at,
        results=results,
        signature_schema_version=database.schema_version,
        scan_metadata=scan_metadata,
    )


def scan_file(
    path: Path,
    root: Path,
    database: SignatureDatabase,
    pattern_engine: PatternScanEngine | None = None,
) -> FileResult:
    display_path = _display_path(path, root)

    try:
        content = scan_file_content(path, database, pattern_engine=pattern_engine)
    except OSError as exc:
        return FileResult(path=display_path, status="error", severity="medium", error=str(exc))

    hash_matches = find_hash_matches(content.hashes, database)
    pattern_matches = content.pattern_matches
    heuristic_findings = run_heuristics(path, content.heuristic_sample)

    signature_matches = [
        {
            "signature_id": match.signature.id,
            "signature_name": match.signature.name,
            "category": match.signature.category,
            "severity": match.signature.severity,
            "matcher": match.matcher.type,
        }
        for match in hash_matches
    ]
    signature_matches.extend(
        {
            "signature_id": match.matcher.signature.id,
            "signature_name": match.matcher.signature.name,
            "category": match.matcher.signature.category,
            "severity": match.matcher.signature.severity,
            "matcher": match.matcher.matcher.type,
            "pattern_bytes": len(match.matcher.pattern),
            "pattern_offset": match.offset,
        }
        for match in pattern_matches
    )

    heuristics = [
        {
            "rule_id": finding.rule_id,
            "severity": finding.severity,
            "description": finding.description,
            "evidence": finding.evidence,
        }
        for finding in heuristic_findings
    ]

    if signature_matches:
        status = "infected"
        severity = _highest_severity([match["severity"] for match in signature_matches])
    elif heuristics:
        status = "suspicious"
        severity = _highest_severity([finding["severity"] for finding in heuristics])
    else:
        status = "clean"
        severity = "info"

    return FileResult(
        path=display_path,
        status=status,
        severity=severity,
        size_bytes=content.size_bytes,
        md5=content.hashes["md5"],
        sha256=content.hashes["sha256"],
        matches=signature_matches,
        heuristics=heuristics,
    )


def _highest_severity(values: list[str]) -> str:
    return max(values, key=lambda value: SEVERITY_RANK.get(value, -1), default="info")


def _display_path(path: Path, root: Path) -> str:
    try:
        base = root if root.is_dir() else root.parent
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
