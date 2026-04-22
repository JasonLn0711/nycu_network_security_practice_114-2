import json
import tempfile
import unittest
from pathlib import Path

from sentinel.reporting import FileResult, build_report, render_markdown_report, write_json_report, write_markdown_report


class ReportingTests(unittest.TestCase):
    def test_report_summary_and_write(self):
        report = build_report(
            target=Path("demo"),
            started_at="2026-01-01T00:00:00+00:00",
            finished_at="2026-01-01T00:00:01+00:00",
            signature_schema_version="1.0",
            results=[
                FileResult(path="clean.txt", status="clean", severity="info"),
                FileResult(path="mock.txt", status="infected", severity="critical"),
            ],
        )

        self.assertEqual(report["summary"]["files_scanned"], 2)
        self.assertEqual(report["summary"]["infected"], 1)

        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "report.json"
            write_json_report(report, destination)
            loaded = json.loads(destination.read_text(encoding="utf-8"))

        self.assertEqual(loaded["tool"], "Sentinel")
        self.assertEqual(loaded["summary"]["clean"], 1)

    def test_markdown_report_renders_findings(self):
        report = build_report(
            target=Path("demo"),
            started_at="2026-01-01T00:00:00+00:00",
            finished_at="2026-01-01T00:00:01+00:00",
            signature_schema_version="1.0",
            results=[
                FileResult(
                    path="mock.txt",
                    status="infected",
                    severity="critical",
                    sha256="a" * 64,
                    matches=[
                        {
                            "signature_id": "sig-marker",
                            "signature_name": "Marker",
                            "matcher": "hex_pattern",
                            "severity": "critical",
                        }
                    ],
                ),
                FileResult(
                    path="suspicious.txt",
                    status="suspicious",
                    severity="medium",
                    heuristics=[
                        {
                            "rule_id": "api-name-indicator",
                            "severity": "medium",
                            "evidence": "CreateRemoteThread",
                        }
                    ],
                ),
            ],
        )

        markdown = render_markdown_report(report)

        self.assertIn("# Sentinel Scan Report", markdown)
        self.assertIn("sig-marker", markdown)
        self.assertIn("api-name-indicator", markdown)

        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "report.md"
            write_markdown_report(report, destination)
            written = destination.read_text(encoding="utf-8")

        self.assertIn("| Infected | 1 |", written)


if __name__ == "__main__":
    unittest.main()
