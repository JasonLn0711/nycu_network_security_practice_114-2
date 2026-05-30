#!/usr/bin/env python3
"""Validate the HW4 submission dry-run package structure."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path


FORBIDDEN_PARTS = {
    ".git",
    ".DS_Store",
    "raw-local",
    "__pycache__",
    ".pytest_cache",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_directory(package_dir: Path, student_id: str) -> None:
    expected_root = f"HW6_{student_id}"
    if package_dir.name != expected_root:
        fail(f"package directory should be named {expected_root}, got {package_dir.name}")

    required = [
        package_dir / "Extension" / "manifest.json",
        package_dir / "Extension" / "background.js",
        package_dir / f"{student_id}_report.pdf",
    ]
    for path in required:
        if not path.is_file():
            fail(f"missing required file: {path}")

    for path in package_dir.rglob("*"):
        parts = set(path.parts)
        if parts & FORBIDDEN_PARTS:
            fail(f"forbidden local artifact in package: {path}")

    report = package_dir / f"{student_id}_report.pdf"
    if report.read_bytes()[:4] != b"%PDF":
        fail(f"report is not a PDF file: {report}")


def validate_zip(zip_path: Path, student_id: str) -> None:
    expected_root = f"HW6_{student_id}/"
    required = {
        f"{expected_root}Extension/manifest.json",
        f"{expected_root}Extension/background.js",
        f"{expected_root}{student_id}_report.pdf",
    }

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        missing = required - names
        if missing:
            fail(f"zip missing required files: {sorted(missing)}")

        for name in names:
            parts = set(Path(name).parts)
            if parts & FORBIDDEN_PARTS:
                fail(f"forbidden local artifact in zip: {name}")

        report_name = f"{expected_root}{student_id}_report.pdf"
        if archive.read(report_name)[:4] != b"%PDF":
            fail(f"report inside zip is not a PDF: {report_name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", required=True)
    parser.add_argument("--package-dir", type=Path)
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()

    if not args.package_dir and not args.zip:
        fail("provide --package-dir or --zip")

    if args.package_dir:
        validate_directory(args.package_dir, args.student_id)

    if args.zip:
        validate_zip(args.zip, args.student_id)

    print("OK: submission dry-run package passed structural checks.")


if __name__ == "__main__":
    main()
