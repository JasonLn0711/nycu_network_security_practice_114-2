#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.4.0"
EXPECTED_SUMMARY = {
    "files_scanned": 5,
    "infected": 1,
    "suspicious": 1,
    "clean": 3,
    "skipped": 0,
    "error": 0,
}
EXPECTED_PATTERN_ENGINE = "aho-corasick-byte-automaton"
EXPECTED_REPORTS = {
    "reports/demo-report.json",
    "reports/demo-report.md",
    "reports/pattern-benchmark.json",
    "reports/pattern-benchmark.md",
}
EXPECTED_EICAR_MD5 = "44d88612fea8a8f36de82e1278abb02f"
EXPECTED_EICAR_SHA256 = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
EICAR_REFERENCE_PARTS = (
    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}",
    b"$EICAR-STANDARD-ANTIVIRUS-",
    b"TEST-FILE!$H+H*",
)


def main() -> int:
    checks = [
        ("version files agree", check_versions),
        ("standards alignment is present", check_standards_alignment),
        ("EICAR reference hashes are consistent", check_eicar_reference),
        ("demo regeneration passes", run_demo),
        ("demo report is consistent", check_demo_report),
        ("benchmark evidence is consistent", check_benchmark),
        ("evidence manifest is consistent", check_manifest),
        ("private repo export plan is consistent", check_private_export),
        ("final report PDFs exist", check_pdf),
    ]

    failures: list[str] = []
    for label, check in checks:
        try:
            check()
        except (AssertionError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
            failures.append(f"{label}: {exc}")
            print(f"[fail] {label}: {exc}", file=sys.stderr)
        else:
            print(f"[ ok ] {label}")

    if failures:
        print("", file=sys.stderr)
        print("Release check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("")
    print(f"Release check passed for Sentinel {EXPECTED_VERSION}.")
    return 0


def check_versions() -> None:
    version_file = (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (PROJECT_ROOT / "python/pyproject.toml").read_text(encoding="utf-8")
    version_module = (PROJECT_ROOT / "python/src/sentinel/version.py").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert version_file == EXPECTED_VERSION, f"VERSION is {version_file!r}"
    assert _extract_assignment(pyproject, "version") == EXPECTED_VERSION, "pyproject version mismatch"
    assert _extract_dunder_version(version_module) == EXPECTED_VERSION, "version.py mismatch"
    assert f"## {EXPECTED_VERSION} " in changelog, "CHANGELOG missing current version section"

    completed = _run([sys.executable, "-m", "sentinel", "--version"], allow_detection=False)
    assert completed.stdout.strip() == f"sentinel {EXPECTED_VERSION}", completed.stdout.strip()


def check_standards_alignment() -> None:
    alignment = (PROJECT_ROOT / "docs/standards-alignment.md").read_text(encoding="utf-8")
    required_terms = [
        "EICAR Anti-Malware Testfile",
        "NIST SP 800-83 Rev. 1",
        "NIST Cybersecurity Framework 2.0",
        "OWASP File Upload Cheat Sheet",
        "MITRE ATT&CK T1055.002",
        "Do not store the literal EICAR file",
        "symbolic links skipped by default",
    ]
    for term in required_terms:
        assert term in alignment, f"standards alignment missing {term!r}"


def check_eicar_reference() -> None:
    eicar = b"".join(EICAR_REFERENCE_PARTS)
    assert len(eicar) == 68

    import hashlib

    assert hashlib.md5(eicar).hexdigest() == EXPECTED_EICAR_MD5  # nosec: EICAR reference hash
    assert hashlib.sha256(eicar).hexdigest() == EXPECTED_EICAR_SHA256

    reference = _read_json("signatures/eicar-reference-signature.json")
    signature = reference["signatures"][0]
    assert signature["id"] == "sig-eicar-standard-antivirus-test-file"
    values = {matcher["type"]: matcher["value"] for matcher in signature["matchers"]}
    assert values["md5"] == EXPECTED_EICAR_MD5
    assert values["sha256"] == EXPECTED_EICAR_SHA256
    assert "actual EICAR test file" in signature["notes"]


def run_demo() -> None:
    _run([sys.executable, "demo/run_demo.py"], allow_detection=False)


def check_demo_report() -> None:
    report = _read_json("reports/demo-report.json")
    summary = report["summary"]
    for key, expected in EXPECTED_SUMMARY.items():
        assert summary.get(key) == expected, f"summary[{key}]={summary.get(key)!r}, expected {expected!r}"

    metadata = report["scan_metadata"]
    assert metadata["hash_filter"] == "bloom-filter"
    assert metadata["hash_filter_items"] == 2
    assert metadata["hash_filter_bits"] >= 128
    assert metadata["hash_filter_hash_functions"] == 3
    assert metadata["hash_filter_policy"] == "precheck-then-exact-hash-map"
    assert metadata["pattern_engine"] == EXPECTED_PATTERN_ENGINE
    assert metadata["pattern_count"] == 1
    assert metadata["automaton_states"] > 1
    assert metadata["symlink_policy"] == "skip"
    assert metadata["traversal_policy"] == "deterministic-rglob-files"

    infected = _finding(report, "nested/level-1/level-2/sentinel-safe-mock-virus.txt")
    matchers = {match["matcher"] for match in infected.get("matches", [])}
    assert matchers == {"md5", "sha256", "hex_pattern"}, f"unexpected matchers: {sorted(matchers)}"
    assert any("pattern_offset" in match for match in infected["matches"]), "missing pattern offset"

    suspicious = _finding(report, "suspicious/api-names-fixture.txt")
    assert suspicious["status"] == "suspicious"
    assert suspicious.get("heuristics"), "suspicious fixture missing heuristic evidence"


def check_benchmark() -> None:
    benchmark = _read_json("reports/pattern-benchmark.json")
    config = benchmark["config"]
    results = benchmark["results"]
    assert config["live_malware_used"] is False
    assert config["pattern_count"] == 128
    assert config["inserted_pattern_count"] == 8
    assert results["match_sets_equal"] is True
    assert results["aho_corasick_matches"] == results["naive_matches"] == 8
    assert results["automaton_states"] > config["pattern_count"]


def check_manifest() -> None:
    manifest = _read_json("reports/demo-evidence-manifest.json")
    safety = manifest["safety"]
    assert safety["read_only_scanner"] is True
    assert safety["uses_live_malware"] is False
    assert safety["executes_scanned_files"] is False
    assert safety["network_actions"] is False

    reports = {report["path"] for report in manifest["reports"]}
    assert reports == EXPECTED_REPORTS, f"manifest reports are {sorted(reports)}"

    json_report = next(report for report in manifest["reports"] if report["path"] == "reports/demo-report.json")
    assert json_report["summary"]["infected"] == 1
    assert json_report["scan_metadata"]["hash_filter"] == "bloom-filter"
    assert json_report["scan_metadata"]["hash_filter_policy"] == "precheck-then-exact-hash-map"
    assert json_report["scan_metadata"]["pattern_engine"] == EXPECTED_PATTERN_ENGINE
    assert json_report["scan_metadata"]["symlink_policy"] == "skip"


def check_private_export() -> None:
    completed = _run([sys.executable, "scripts/export_private_repo.py", "--dry-run"], allow_detection=False)
    manifest = json.loads(completed.stdout)
    paths = {entry["path"] for entry in manifest["files"]}

    assert manifest["manifest_type"] == "private-repo-export"
    assert manifest["file_count"] >= 40
    assert manifest["safety"]["excludes_project_spec_pdf"] is True
    assert manifest["safety"]["excludes_latex_build_artifacts"] is True
    assert manifest["safety"]["literal_eicar_file_stored"] is False
    assert "README.md" in paths
    assert "docs/requirements-traceability.md" in paths
    assert "docs/python/technical-design.md" in paths
    assert "docs/rust/README.md" in paths
    assert "demo/runbook.md" in paths
    assert "python/README.md" in paths
    assert "python/src/sentinel/scanner.py" in paths
    assert "rust/Cargo.toml" in paths
    assert "rust/src/main.rs" in paths
    assert "scripts/check_release.py" in paths
    assert "scripts/export_private_repo.py" in paths
    assert "report/final-report.pdf" in paths
    assert "report/final-report-v2.pdf" in paths
    assert "report/evidence-screenshots/signature-database.png" in paths
    assert "report/evidence-screenshots/release-gate.png" in paths
    assert "report/submission-package.md" in paths
    assert "project-spec.pdf" not in paths
    assert "report/report-draft.md" not in paths
    assert "report/private-repo-handoff.md" not in paths
    assert "report/submission-checklist.md" not in paths
    assert "report/final-report.aux" not in paths
    assert "report/final-report-v2.aux" not in paths


def check_pdf() -> None:
    expectations = {
        "report/final-report.pdf": (100_000, 5),
        "report/final-report-v2.pdf": (500_000, 10),
    }
    for relative, (minimum_bytes, minimum_pages) in expectations.items():
        pdf_path = PROJECT_ROOT / relative
        assert pdf_path.is_file(), f"{relative} missing"
        assert pdf_path.stat().st_size > minimum_bytes, f"{relative} is unexpectedly small"

        if shutil.which("pdfinfo"):
            completed = subprocess.run(
                ["pdfinfo", str(pdf_path)],
                cwd=PROJECT_ROOT,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            pages = _extract_pdf_pages(completed.stdout)
            assert pages >= minimum_pages, f"expected at least {minimum_pages} PDF pages for {relative}, got {pages}"


def _run(command: list[str], *, allow_detection: bool) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = "python/src"
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0 and not (allow_detection and completed.returncode == 1):
        raise subprocess.CalledProcessError(
            completed.returncode,
            command,
            output=completed.stdout,
            stderr=completed.stderr,
        )
    return completed


def _read_json(path: str) -> dict[str, Any]:
    return json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))


def _finding(report: dict[str, Any], path: str) -> dict[str, Any]:
    for finding in report["findings"]:
        if finding["path"] == path:
            return finding
    raise AssertionError(f"missing finding for {path}")


def _extract_assignment(text: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}\s*=\s*"([^"]+)"$', text, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing {key} assignment")
    return match.group(1)


def _extract_dunder_version(text: str) -> str:
    return _extract_assignment(text, "__version__")


def _extract_pdf_pages(text: str) -> int:
    match = re.search(r"^Pages:\s+(\d+)$", text, re.MULTILINE)
    if not match:
        raise AssertionError("pdfinfo output missing page count")
    return int(match.group(1))


if __name__ == "__main__":
    raise SystemExit(main())
