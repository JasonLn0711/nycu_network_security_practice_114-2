#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "dist/sentinel-private-repo"
DEFAULT_MANIFEST = PROJECT_ROOT / "dist/sentinel-private-repo-manifest.json"

EXPORT_PATHS = (
    "VERSION",
    "CHANGELOG.md",
    "Makefile",
    "pyproject.toml",
    "README.md",
    "docs",
    "src/sentinel",
    "tests",
    "signatures/malware-signatures.json",
    "signatures/eicar-reference-signature.json",
    "demo",
    "reports/demo-report.json",
    "reports/demo-report.md",
    "reports/pattern-benchmark.json",
    "reports/pattern-benchmark.md",
    "reports/demo-evidence-manifest.json",
    "scripts",
    "report/final-report.tex",
    "report/final-report.pdf",
    "report/submission-package.md",
)

EXCLUDED_SUFFIXES = (
    ".aux",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".pyc",
)
EXCLUDED_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", "dist", "build"}
EXCLUDED_NAMES = {"project-spec.pdf", "report-draft.md", ".DS_Store", "Thumbs.db", ".gitkeep"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export the Sentinel project files that should be mirrored into the private submission repo."
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Destination folder for the export package.",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Where to write the export manifest when not using --dry-run.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the destination folder before exporting.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the export manifest without copying files.",
    )
    args = parser.parse_args(argv)

    output = Path(args.output)
    try:
        files = list(_selected_files())
    except (AssertionError, FileNotFoundError) as exc:
        print(f"export error: {exc}", file=sys.stderr)
        return 2
    manifest = _build_manifest(files, output)

    if args.dry_run:
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0

    if output.exists():
        if args.clean:
            shutil.rmtree(output)
        elif any(output.iterdir()):
            print(f"export destination is not empty: {output}", file=sys.stderr)
            print("rerun with --clean or choose a different --output path", file=sys.stderr)
            return 2

    for source in files:
        relative = source.relative_to(PROJECT_ROOT)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Private repository export package written:")
    print(f"- output: {output}")
    print(f"- manifest: {manifest_path}")
    print(f"- files: {manifest['file_count']}")
    print(f"- bytes: {manifest['total_bytes']}")
    return 0


def _selected_files() -> list[Path]:
    files: list[Path] = []
    missing: list[str] = []
    for relative in EXPORT_PATHS:
        path = PROJECT_ROOT / relative
        if not path.exists():
            missing.append(relative)
            continue
        if path.is_dir():
            files.extend(_iter_directory_files(path))
        else:
            if _is_allowed_file(path):
                files.append(path)

    if missing:
        joined = ", ".join(missing)
        raise FileNotFoundError(f"export path does not exist: {joined}")

    unique_files = sorted(set(files), key=lambda item: item.relative_to(PROJECT_ROOT).as_posix())
    _assert_export_boundaries(unique_files)
    return unique_files


def _iter_directory_files(directory: Path) -> list[Path]:
    files = []
    for path in directory.rglob("*"):
        if path.is_dir():
            continue
        if _is_allowed_file(path):
            files.append(path)
    return files


def _is_allowed_file(path: Path) -> bool:
    relative = path.relative_to(PROJECT_ROOT)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    return not path.name.endswith(EXCLUDED_SUFFIXES)


def _assert_export_boundaries(files: list[Path]) -> None:
    relative_paths = {path.relative_to(PROJECT_ROOT).as_posix() for path in files}
    forbidden = {
        "project-spec.pdf",
        "report/report-draft.md",
        "report/private-repo-handoff.md",
        "report/submission-checklist.md",
        "report/final-report.aux",
        "report/final-report.fdb_latexmk",
        "report/final-report.fls",
        "report/final-report.log",
        "report/final-report.out",
    }
    leaked = sorted(relative_paths & forbidden)
    if leaked:
        raise AssertionError(f"forbidden export paths selected: {', '.join(leaked)}")


def _build_manifest(files: list[Path], output: Path) -> dict[str, Any]:
    entries = [_file_entry(path) for path in files]
    return {
        "tool": "Sentinel",
        "manifest_type": "private-repo-export",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_root": str(PROJECT_ROOT),
        "output": str(output),
        "file_count": len(entries),
        "total_bytes": sum(entry["size_bytes"] for entry in entries),
        "safety": {
            "excludes_project_spec_pdf": True,
            "excludes_latex_build_artifacts": True,
            "excludes_live_malware": True,
            "literal_eicar_file_stored": False,
        },
        "next_steps": [
            "Create or choose the private GitHub/GitLab repository.",
            "Copy the export package contents into the private repository root.",
            "Run python3 -m pip install -e .",
            "Run python3 scripts/check_release.py.",
            "Record the private repository URL and final commit hash.",
        ],
        "files": entries,
    }


def _file_entry(path: Path) -> dict[str, Any]:
    relative = path.relative_to(PROJECT_ROOT).as_posix()
    return {
        "path": relative,
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
