from contextlib import redirect_stdout
import io
import json
import tempfile
import unittest
from pathlib import Path

from sentinel.cli import main


class CliTests(unittest.TestCase):
    def test_scan_command_writes_report_and_returns_detection_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            (target / "mock.txt").write_text("SAFE_MARKER\n", encoding="utf-8")
            signatures = root / "signatures.json"
            signatures.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "signatures": [
                            {
                                "id": "sig-marker",
                                "name": "Marker",
                                "category": "safe-mock-virus",
                                "severity": "critical",
                                "matchers": [{"type": "hex_pattern", "value": "534146455f4d41524b4552"}],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = root / "report.json"

            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        "scan",
                        str(target),
                        "--signatures",
                        str(signatures),
                        "--report",
                        str(report),
                    ]
                )

            loaded = json.loads(report.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 1)
        self.assertEqual(loaded["summary"]["infected"], 1)

    def test_validate_signatures_returns_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            signatures = Path(tmp) / "signatures.json"
            signatures.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "signatures": [
                            {
                                "id": "sig-marker",
                                "name": "Marker",
                                "category": "safe-mock-virus",
                                "severity": "critical",
                                "matchers": [{"type": "hex_pattern", "value": "53414645"}],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            with redirect_stdout(io.StringIO()):
                exit_code = main(["validate-signatures", str(signatures)])

        self.assertEqual(exit_code, 0)

    def test_version_flag_returns_success(self):
        with redirect_stdout(io.StringIO()) as stdout:
            with self.assertRaises(SystemExit) as exc:
                main(["--version"])

        self.assertEqual(exc.exception.code, 0)
        self.assertIn("sentinel 0.2.0", stdout.getvalue())

    def test_scan_command_can_write_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            (target / "clean.txt").write_text("hello\n", encoding="utf-8")
            signatures = root / "signatures.json"
            signatures.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "signatures": [
                            {
                                "id": "sig-marker",
                                "name": "Marker",
                                "category": "safe-mock-virus",
                                "severity": "critical",
                                "matchers": [{"type": "hex_pattern", "value": "53414645"}],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = root / "report.md"

            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        "scan",
                        str(target),
                        "--signatures",
                        str(signatures),
                        "--report",
                        str(report),
                        "--format",
                        "markdown",
                    ]
                )

            markdown = report.read_text(encoding="utf-8")

        self.assertEqual(exit_code, 0)
        self.assertIn("# Sentinel Scan Report", markdown)
        self.assertIn("| Clean | 1 |", markdown)

    def test_write_evidence_command_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target"
            target.mkdir()
            (target / "clean.txt").write_text("hello\n", encoding="utf-8")
            signatures = root / "signatures.json"
            signatures.write_text('{"schema_version": "1.0", "signatures": []}\n', encoding="utf-8")
            report = root / "report.json"
            report.write_text(
                json.dumps({"tool": "Sentinel", "target": str(target), "summary": {"clean": 1}}),
                encoding="utf-8",
            )
            output = root / "evidence.json"

            with redirect_stdout(io.StringIO()):
                exit_code = main(
                    [
                        "write-evidence",
                        "--target",
                        str(target),
                        "--signatures",
                        str(signatures),
                        "--report",
                        str(report),
                        "--output",
                        str(output),
                    ]
                )

            manifest = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(manifest["manifest_type"], "demo-evidence")
        self.assertEqual(len(manifest["demo_tree"]), 1)


if __name__ == "__main__":
    unittest.main()
