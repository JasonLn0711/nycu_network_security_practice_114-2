#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


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
        ("Rust verification commands pass", run_rust_verification),
        ("demo report is consistent", check_demo_report),
        ("evidence manifest is consistent", check_manifest),
        ("private repo export plan is consistent", check_private_export),
        ("final report PDF exists", check_pdf),
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
    cargo_toml = (PROJECT_ROOT / "rust/Cargo.toml").read_text(encoding="utf-8")
    changelog = (PROJECT_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert version_file == EXPECTED_VERSION, f"VERSION is {version_file!r}"
    assert _extract_assignment(cargo_toml, "version") == EXPECTED_VERSION, "Cargo.toml version mismatch"
    assert f"## {EXPECTED_VERSION} " in changelog, "CHANGELOG missing current version section"

    completed = _run_rust(["--version"])
    assert completed.stdout.strip() == f"sentinel-v2-rust {EXPECTED_VERSION}", completed.stdout.strip()


def check_standards_alignment() -> None:
    alignment = (PROJECT_ROOT / "docs/standards-alignment.md").read_text(encoding="utf-8")
    required_terms = [
        "EICAR Anti-Malware Testfile",
        "NIST SP 800-83 Rev. 1",
        "NIST Cybersecurity Framework 2.0",
        "OWASP File Upload Cheat Sheet",
        "MITRE ATT&CK T1055.002",
        "Generate the EICAR demo fixture at runtime",
        "symbolic links skipped by default",
    ]
    for term in required_terms:
        assert term in alignment, f"standards alignment missing {term!r}"


def check_eicar_reference() -> None:
    import hashlib

    eicar = b"".join(EICAR_REFERENCE_PARTS)
    assert len(eicar) == 68
    assert hashlib.md5(eicar).hexdigest() == EXPECTED_EICAR_MD5  # nosec: EICAR reference hash
    assert hashlib.sha256(eicar).hexdigest() == EXPECTED_EICAR_SHA256

    reference = _read_json("signatures/eicar-reference-signature.json")
    signature = reference["signatures"][0]
    assert signature["id"] == "sig-eicar-standard-antivirus-test-file"
    values = {matcher["type"]: matcher["value"] for matcher in signature["matchers"]}
    assert values["md5"] == EXPECTED_EICAR_MD5
    assert values["sha256"] == EXPECTED_EICAR_SHA256
    assert "actual EICAR test file" in signature["notes"]


def run_rust_verification() -> None:
    _run(["cargo", "fmt", "--check"], cwd=PROJECT_ROOT / "rust")
    _run(["cargo", "test"], cwd=PROJECT_ROOT / "rust")
    _run(["cargo", "clippy", "--all-targets", "--", "-D", "warnings"], cwd=PROJECT_ROOT / "rust")
    _run_rust(["validate-signatures", "--signatures", "../signatures/malware-signatures.json"])
    _run_rust(["prepare-eicar-demo", "--target", "../demo/demo-tree"])
    _run_rust(["verify-demo", "--target", "../demo/demo-tree", "--signatures", "../signatures/malware-signatures.json"])
    _run_rust(
        [
            "scan",
            "--target",
            "../demo/demo-tree",
            "--signatures",
            "../signatures/malware-signatures.json",
            "--json",
            "../reports/demo-report.json",
            "--markdown",
            "../reports/demo-report.md",
        ],
        allow_detection=True,
    )
    _run_rust(
        [
            "write-evidence",
            "--target",
            "../demo/demo-tree",
            "--signatures",
            "../signatures/malware-signatures.json",
            "--report",
            "../reports/demo-report.json",
            "--report",
            "../reports/demo-report.md",
            "--output",
            "../reports/demo-evidence-manifest.json",
        ]
    )


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

    infected = _finding(report, "nested/level-1/level-2/eicar.com.txt")
    matchers = {match["matcher"] for match in infected.get("matches", [])}
    assert matchers == {"md5", "sha256", "hex_pattern"}, f"unexpected matchers: {sorted(matchers)}"
    assert any("pattern_offset" in match for match in infected["matches"]), "missing pattern offset"
    assert {match["signature_id"] for match in infected["matches"]} == {
        "sig-eicar-standard-antivirus-test-file"
    }

    suspicious = _finding(report, "suspicious/api-names-fixture.txt")
    assert suspicious["status"] == "suspicious"
    assert suspicious.get("heuristics"), "suspicious fixture missing heuristic evidence"


def check_manifest() -> None:
    manifest = _read_json("reports/demo-evidence-manifest.json")
    safety = manifest["safety"]
    assert safety["read_only_scanner"] is True
    assert safety["uses_live_malware"] is False
    assert safety["executes_scanned_files"] is False
    assert safety["network_actions"] is False

    reports = {report["path"] for report in manifest["reports"]}
    assert reports == {"reports/demo-report.json", "reports/demo-report.md"}, f"manifest reports are {sorted(reports)}"
    demo_paths = {entry["path"] for entry in manifest["demo_tree"]}
    assert "nested/level-1/level-2/eicar.com.txt" in demo_paths

    json_report = next(report for report in manifest["reports"] if report["path"] == "reports/demo-report.json")
    assert json_report["summary"]["infected"] == 1
    assert json_report["scan_metadata"]["hash_filter"] == "bloom-filter"
    assert json_report["scan_metadata"]["hash_filter_policy"] == "precheck-then-exact-hash-map"
    assert json_report["scan_metadata"]["pattern_engine"] == EXPECTED_PATTERN_ENGINE
    assert json_report["scan_metadata"]["symlink_policy"] == "skip"


def check_private_export() -> None:
    completed = _run([sys.executable, "scripts/export_private_repo.py", "--dry-run"], cwd=PROJECT_ROOT)
    manifest = json.loads(completed.stdout)
    paths = {entry["path"] for entry in manifest["files"]}

    assert manifest["manifest_type"] == "private-repo-export"
    assert manifest["file_count"] >= 25
    assert manifest["safety"]["excludes_project_spec_pdf"] is True
    assert manifest["safety"]["excludes_latex_build_artifacts"] is True
    assert manifest["safety"]["excludes_legacy_python_path"] is True
    assert manifest["safety"]["literal_eicar_file_stored"] is False
    assert "README.md" in paths
    assert "docs/requirements-traceability.md" in paths
    assert "docs/rust/README.md" in paths
    assert "demo/runbook.md" in paths
    assert "rust/Cargo.toml" in paths
    assert "rust/Cargo.lock" in paths
    assert "rust/src/main.rs" in paths
    assert "scripts/check_release.py" in paths
    assert "scripts/export_private_repo.py" in paths
    assert "report/final-report.tex" in paths
    assert "report/final-report.pdf" in paths
    assert "report/evidence-screenshots/rust-demo-scan.png" in paths
    assert "reports/demo-report.json" in paths
    assert "reports/demo-report.md" in paths
    assert "reports/demo-evidence-manifest.json" in paths
    assert "demo/demo-tree/nested/level-1/level-2/eicar.com.txt" not in paths
    assert "project-spec.pdf" not in paths
    assert not any(path.startswith("python/") for path in paths)
    assert not any(path.startswith("docs/python/") for path in paths)
    assert not any(path.endswith((".aux", ".fdb_latexmk", ".fls", ".log", ".out")) for path in paths)


def check_pdf() -> None:
    pdf_path = PROJECT_ROOT / "report/final-report.pdf"
    assert pdf_path.is_file(), "report/final-report.pdf missing"
    assert pdf_path.stat().st_size > 500_000, "report/final-report.pdf is unexpectedly small"

    if shutil.which("pdfinfo"):
        completed = _run(["pdfinfo", str(pdf_path)], cwd=PROJECT_ROOT)
        pages = _extract_pdf_pages(completed.stdout)
        assert pages >= 10, f"expected at least 10 PDF pages, got {pages}"


def _run(command: list[str], *, cwd: Path, allow_detection: bool = False) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
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


def _run_rust(args: list[str], *, allow_detection: bool = False) -> subprocess.CompletedProcess[str]:
    return _run(["cargo", "run", "--quiet", "--", *args], cwd=PROJECT_ROOT / "rust", allow_detection=allow_detection)


def _read_json(path: str) -> dict:
    return json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))


def _finding(report: dict, path: str) -> dict:
    for finding in report["findings"]:
        if finding["path"] == path:
            return finding
    raise AssertionError(f"missing finding for {path}")


def _extract_assignment(text: str, key: str) -> str:
    match = re.search(rf'^{re.escape(key)}\s*=\s*"([^"]+)"$', text, re.MULTILINE)
    if not match:
        raise AssertionError(f"missing {key} assignment")
    return match.group(1)


def _extract_pdf_pages(text: str) -> int:
    match = re.search(r"^Pages:\s+(\d+)$", text, re.MULTILINE)
    if not match:
        raise AssertionError("pdfinfo output missing page count")
    return int(match.group(1))


if __name__ == "__main__":
    raise SystemExit(main())
