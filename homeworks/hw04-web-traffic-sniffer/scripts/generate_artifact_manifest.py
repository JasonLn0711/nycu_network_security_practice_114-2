#!/usr/bin/env python3
"""Generate a sanitized artifact manifest for HW4 submission evidence."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "artifact-manifest.json"

ARTIFACTS = [
    ("official_spec", "raw/hw04-web-traffic-sniffer-spec.pdf", "official assignment PDF"),
    ("starter_zip", "raw/hw04-web-traffic-sniffer-example.zip", "official starter ZIP"),
    ("extension_manifest", "solution/Extension/manifest.json", "submitted extension manifest"),
    ("extension_service_worker", "solution/Extension/background.js", "submitted extension service worker"),
    ("sanitized_evidence_png", "evidence/screenshots/sanitized-console-evidence.png", "tracked sanitized evidence"),
    ("sanitized_evidence_md", "evidence/screenshots/sanitized-console-evidence.md", "tracked sanitized evidence summary"),
    ("report_pdf", "report/513559004_report.pdf", "final report PDF"),
    ("submission_zip", "submission/final/HW6_513559004.zip", "final generated upload ZIP"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    artifacts = []
    for artifact_id, relative_path, role in ARTIFACTS:
        path = ROOT / relative_path
        if not path.exists():
            artifacts.append(
                {
                    "id": artifact_id,
                    "path": relative_path,
                    "role": role,
                    "exists": False,
                }
            )
            continue

        artifacts.append(
            {
                "id": artifact_id,
                "path": relative_path,
                "role": role,
                "exists": True,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "assignment": "HW4 Web Traffic Sniffer",
        "student_id": "513559004",
        "privacy_note": "Manifest records file hashes and sizes only. Raw local evidence remains ignored under evidence/raw-local/.",
        "artifacts": artifacts,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
