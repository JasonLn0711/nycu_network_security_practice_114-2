from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any


STATUS_ORDER = ("infected", "suspicious", "clean", "skipped", "error")


@dataclass
class FileResult:
    path: str
    status: str
    severity: str
    size_bytes: int | None = None
    md5: str | None = None
    sha256: str | None = None
    matches: list[dict[str, Any]] = field(default_factory=list)
    heuristics: list[dict[str, Any]] = field(default_factory=list)
    skip_reason: str | None = None
    error: str | None = None


def build_report(
    *,
    target: Path,
    started_at: str,
    finished_at: str,
    results: list[FileResult],
    signature_schema_version: str,
    scan_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    summary = {status: 0 for status in STATUS_ORDER}
    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1

    summary["files_scanned"] = len([result for result in results if result.status not in {"skipped", "error"}])
    summary["total_results"] = len(results)

    return {
        "tool": "Sentinel",
        "signature_schema_version": signature_schema_version,
        "started_at": started_at,
        "finished_at": finished_at,
        "target": str(target),
        "scan_metadata": scan_metadata or {},
        "summary": summary,
        "findings": [
            _result_to_dict(result)
            for result in results
            if result.status in {"infected", "suspicious", "skipped", "error"}
        ],
        "all_results": [_result_to_dict(result) for result in results],
    }


def write_json_report(report: dict[str, Any], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown_report(report: dict[str, Any], path: str | Path) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_markdown_report(report), encoding="utf-8")


def render_markdown_report(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        "# Sentinel Scan Report",
        "",
        "## Run Metadata",
        "",
        f"- Tool: `{_md(report.get('tool', 'Sentinel'))}`",
        f"- Target: `{_md(report.get('target', ''))}`",
        f"- Signature schema: `{_md(report.get('signature_schema_version', 'unknown'))}`",
        f"- Started: `{_md(report.get('started_at', ''))}`",
        f"- Finished: `{_md(report.get('finished_at', ''))}`",
        "",
        "## Scan Engine",
        "",
        f"- Pattern engine: `{_md(_scan_metadata(report, 'pattern_engine', 'unknown'))}`",
        f"- Pattern count: `{_md(_scan_metadata(report, 'pattern_count', 0))}`",
        f"- Automaton states: `{_md(_scan_metadata(report, 'automaton_states', 0))}`",
        f"- Chunk size bytes: `{_md(_scan_metadata(report, 'chunk_size_bytes', 0))}`",
        f"- Symlink policy: `{_md(_scan_metadata(report, 'symlink_policy', 'unknown'))}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Files scanned | {summary.get('files_scanned', 0)} |",
        f"| Infected | {summary.get('infected', 0)} |",
        f"| Suspicious | {summary.get('suspicious', 0)} |",
        f"| Clean | {summary.get('clean', 0)} |",
        f"| Skipped | {summary.get('skipped', 0)} |",
        f"| Errors | {summary.get('error', 0)} |",
        "",
        "## Findings",
        "",
    ]

    findings = report.get("findings", [])
    if not findings:
        lines.append("No infected, suspicious, skipped, or error results were found.")
    else:
        lines.extend(
            [
                "| Path | Status | Severity | Evidence |",
                "| --- | --- | --- | --- |",
            ]
        )
        for finding in findings:
            lines.append(
                "| "
                f"`{_md(finding.get('path', ''))}` | "
                f"{_md(finding.get('status', ''))} | "
                f"{_md(finding.get('severity', ''))} | "
                f"{_md(_finding_evidence(finding))} |"
            )

    lines.extend(["", "## All Results", ""])
    all_results = report.get("all_results", [])
    if not all_results:
        lines.append("No per-file results were recorded.")
    else:
        lines.extend(
            [
                "| Path | Status | Severity | Size | SHA-256 |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for result in all_results:
            lines.append(
                "| "
                f"`{_md(result.get('path', ''))}` | "
                f"{_md(result.get('status', ''))} | "
                f"{_md(result.get('severity', ''))} | "
                f"{result.get('size_bytes', '')} | "
                f"`{_md(result.get('sha256', ''))}` |"
            )

    return "\n".join(lines).rstrip() + "\n"


def _result_to_dict(result: FileResult) -> dict[str, Any]:
    payload = asdict(result)
    return {key: value for key, value in payload.items() if value not in (None, [], {})}


def _finding_evidence(finding: dict[str, Any]) -> str:
    matches = finding.get("matches", [])
    heuristics = finding.get("heuristics", [])
    skip_reason = finding.get("skip_reason")
    error = finding.get("error")

    evidence: list[str] = []
    for match in matches:
        evidence.append(
            _match_evidence(match)
        )
    for heuristic in heuristics:
        evidence.append(
            f"{heuristic.get('rule_id', 'heuristic')} ({heuristic.get('evidence', 'no evidence')})"
        )
    if skip_reason:
        evidence.append(f"skipped: {skip_reason}")
    if error:
        evidence.append(f"error: {error}")
    return "; ".join(evidence) if evidence else "-"


def _match_evidence(match: dict[str, Any]) -> str:
    evidence = f"{match.get('matcher', 'matcher')}:{match.get('signature_id', 'unknown-signature')}"
    if "pattern_offset" in match:
        evidence += f"@{match['pattern_offset']}"
    return evidence


def _scan_metadata(report: dict[str, Any], key: str, default: Any) -> Any:
    metadata = report.get("scan_metadata", {})
    if isinstance(metadata, dict):
        return metadata.get(key, default)
    return default


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")
