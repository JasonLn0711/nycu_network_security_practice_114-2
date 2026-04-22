from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .evidence import build_evidence_manifest, write_evidence_manifest
from .reporting import write_json_report, write_markdown_report
from .scanner import scan_directory
from .signatures import SignatureError, load_signature_database
from .version import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="Sentinel safe signature-based scanner for the network security project.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan an explicit file or directory.")
    scan_parser.add_argument("target", help="File or directory to scan.")
    scan_parser.add_argument(
        "--signatures",
        required=True,
        help="Path to JSON signature database.",
    )
    scan_parser.add_argument(
        "--report",
        required=True,
        help="Path to write JSON report.",
    )
    scan_parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Report format.",
    )
    scan_parser.set_defaults(handler=_scan)

    validate_parser = subparsers.add_parser("validate-signatures", help="Validate a JSON signature database.")
    validate_parser.add_argument("signatures", help="Path to JSON signature database.")
    validate_parser.set_defaults(handler=_validate_signatures)

    summarize_parser = subparsers.add_parser("summarize-report", help="Print a compact summary of a report.")
    summarize_parser.add_argument("report", help="Path to JSON report.")
    summarize_parser.set_defaults(handler=_summarize_report)

    evidence_parser = subparsers.add_parser("write-evidence", help="Write a reproducible demo evidence manifest.")
    evidence_parser.add_argument("--target", required=True, help="Demo target file or directory.")
    evidence_parser.add_argument("--signatures", required=True, help="Path to JSON signature database.")
    evidence_parser.add_argument(
        "--report",
        action="append",
        dest="reports",
        required=True,
        help="Report artifact to include. Repeat for multiple reports.",
    )
    evidence_parser.add_argument("--output", required=True, help="Path to write evidence manifest JSON.")
    evidence_parser.set_defaults(handler=_write_evidence)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except SignatureError as exc:
        print(f"signature error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"file error: {exc}", file=sys.stderr)
        return 2


def _scan(args: argparse.Namespace) -> int:
    database = load_signature_database(args.signatures)
    report = scan_directory(args.target, database)
    if args.format == "json":
        write_json_report(report, args.report)
    else:
        write_markdown_report(report, args.report)

    summary = report["summary"]
    print(
        "Sentinel scan complete: "
        f"scanned={summary['files_scanned']} "
        f"infected={summary['infected']} "
        f"suspicious={summary['suspicious']} "
        f"clean={summary['clean']} "
        f"errors={summary['error']} "
        f"report={args.report}"
    )
    return 1 if summary["infected"] else 0


def _validate_signatures(args: argparse.Namespace) -> int:
    database = load_signature_database(args.signatures)
    print(
        "Signature database valid: "
        f"schema={database.schema_version} "
        f"signatures={len(database.signatures)} "
        f"patterns={len(database.patterns)}"
    )
    return 0


def _summarize_report(args: argparse.Namespace) -> int:
    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    summary = report.get("summary", {})
    print(
        "Sentinel report summary: "
        f"scanned={summary.get('files_scanned', 0)} "
        f"infected={summary.get('infected', 0)} "
        f"suspicious={summary.get('suspicious', 0)} "
        f"clean={summary.get('clean', 0)} "
        f"errors={summary.get('error', 0)}"
    )
    return 0


def _write_evidence(args: argparse.Namespace) -> int:
    manifest = build_evidence_manifest(
        target=args.target,
        signatures=args.signatures,
        reports=args.reports,
    )
    write_evidence_manifest(manifest, args.output)
    print(
        "Evidence manifest written: "
        f"files={len(manifest['demo_tree'])} "
        f"reports={len(manifest['reports'])} "
        f"output={args.output}"
    )
    return 0
