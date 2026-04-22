import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_directory
from sentinel.signatures import parse_signature_database


class ScannerTests(unittest.TestCase):
    def test_scan_directory_reports_clean_infected_and_suspicious(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "clean.txt").write_text("hello\n", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "mock.txt").write_text("marker SAFE_MARKER\n", encoding="utf-8")
            (root / "suspicious.txt").write_text("CreateRemoteThread\n", encoding="utf-8")

            database = parse_signature_database(
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
            )

            report = scan_directory(root, database)

        summary = report["summary"]
        self.assertEqual(summary["files_scanned"], 3)
        self.assertEqual(summary["infected"], 1)
        self.assertEqual(summary["suspicious"], 1)
        self.assertEqual(summary["clean"], 1)

        findings = {finding["path"]: finding for finding in report["findings"]}
        self.assertEqual(findings["nested/mock.txt"]["status"], "infected")
        self.assertEqual(findings["suspicious.txt"]["status"], "suspicious")

    def test_missing_target_is_reported_as_error(self):
        database = parse_signature_database(
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
        )

        report = scan_directory("/path/that/should/not/exist", database)

        self.assertEqual(report["summary"]["error"], 1)
        self.assertEqual(report["findings"][0]["status"], "error")


if __name__ == "__main__":
    unittest.main()
