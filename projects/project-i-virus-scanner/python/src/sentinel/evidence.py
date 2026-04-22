from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


def build_evidence_manifest(
    *,
    target: str | Path,
    signatures: str | Path,
    reports: list[str | Path],
) -> dict[str, Any]:
    target_path = Path(target)
    signature_path = Path(signatures)
    report_paths = [Path(report) for report in reports]

    if not target_path.exists():
        raise FileNotFoundError(f"Target path does not exist: {target_path}")
    if not signature_path.is_file():
        raise FileNotFoundError(f"Signature database does not exist: {signature_path}")
    for report_path in report_paths:
        if not report_path.is_file():
            raise FileNotFoundError(f"Report artifact does not exist: {report_path}")

    return {
        "tool": "Sentinel",
        "manifest_type": "demo-evidence",
        "generated_at": _timestamp(),
        "safety": {
            "read_only_scanner": True,
            "uses_live_malware": False,
            "executes_scanned_files": False,
            "network_actions": False,
            "fixture_note": "Current local demo uses a safe mock-virus marker, not live malware.",
        },
        "inputs": {
            "target": _target_metadata(target_path),
            "signature_database": _file_metadata(signature_path),
        },
        "demo_tree": _tree_metadata(target_path),
        "reports": [_report_metadata(report_path) for report_path in report_paths],
        "reproducibility": {
            "test_command": "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m unittest discover -s python/tests -v",
            "signature_validation_command": (
                f"PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m sentinel "
                f"validate-signatures {signature_path}"
            ),
            "json_scan_command": (
                f"PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m sentinel scan {target_path} "
                f"--signatures {signature_path} --report reports/demo-report.json --format json"
            ),
            "markdown_scan_command": (
                f"PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=python/src python3 -m sentinel scan {target_path} "
                f"--signatures {signature_path} --report reports/demo-report.md --format markdown"
            ),
        },
    }


def write_evidence_manifest(manifest: dict[str, Any], output: str | Path) -> None:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _target_metadata(path: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "path": str(path),
        "kind": "directory" if path.is_dir() else "file",
    }
    if path.is_file():
        metadata.update(_file_metadata(path))
    return metadata


def _tree_metadata(root: Path) -> list[dict[str, Any]]:
    if root.is_symlink():
        return []
    if root.is_file():
        metadata = _file_metadata(root)
        metadata["path"] = root.name
        return [metadata]

    files = sorted(path for path in root.rglob("*") if path.is_file() and not path.is_symlink())
    tree = []
    for path in files:
        metadata = _file_metadata(path)
        metadata["path"] = str(path.relative_to(root))
        tree.append(metadata)
    return tree


def _report_metadata(path: Path) -> dict[str, Any]:
    metadata = _file_metadata(path)
    metadata["path"] = str(path)
    if path.suffix.lower() == ".json":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}
        if isinstance(payload, dict):
            metadata["summary"] = payload.get("summary", {})
            metadata["scan_metadata"] = payload.get("scan_metadata", {})
            metadata["tool"] = payload.get("tool")
            metadata["target"] = payload.get("target")
    return metadata


def _file_metadata(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
