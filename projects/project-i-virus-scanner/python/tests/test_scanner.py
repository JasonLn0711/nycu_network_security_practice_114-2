import tempfile
import unittest
from pathlib import Path

from sentinel.scanner import scan_directory
from sentinel.signatures import parse_signature_database


def _marker_database():
    return parse_signature_database(
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


class ScannerTests(unittest.TestCase):
    def test_scan_directory_reports_clean_infected_and_suspicious(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "clean.txt").write_text("hello\n", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "mock.txt").write_text("marker SAFE_MARKER\n", encoding="utf-8")
            (root / "suspicious.txt").write_text("CreateRemoteThread\n", encoding="utf-8")

            database = _marker_database()

            report = scan_directory(root, database)

        summary = report["summary"]
        self.assertEqual(summary["files_scanned"], 3)
        self.assertEqual(summary["infected"], 1)
        self.assertEqual(summary["suspicious"], 1)
        self.assertEqual(summary["clean"], 1)
        self.assertEqual(report["scan_metadata"]["hash_filter"], "bloom-filter")
        self.assertEqual(report["scan_metadata"]["hash_filter_policy"], "precheck-then-exact-hash-map")
        self.assertGreaterEqual(report["scan_metadata"]["hash_filter_bits"], 128)
        self.assertEqual(report["scan_metadata"]["pattern_engine"], "aho-corasick-byte-automaton")
        self.assertEqual(report["scan_metadata"]["symlink_policy"], "skip")
        self.assertGreater(report["scan_metadata"]["automaton_states"], 1)

        findings = {finding["path"]: finding for finding in report["findings"]}
        self.assertEqual(findings["nested/mock.txt"]["status"], "infected")
        self.assertEqual(findings["nested/mock.txt"]["matches"][0]["pattern_offset"], 7)
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

    def test_directory_scan_skips_symbolic_links_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            root = workspace / "target"
            root.mkdir()
            outside = workspace / "outside-marker.txt"
            outside.write_text("SAFE_MARKER\n", encoding="utf-8")
            (root / "clean.txt").write_text("hello\n", encoding="utf-8")
            link = root / "outside-link.txt"
            try:
                link.symlink_to(outside)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symbolic links unavailable: {exc}")

            report = scan_directory(root, _marker_database())

        self.assertEqual(report["summary"]["files_scanned"], 1)
        self.assertEqual(report["summary"]["infected"], 0)
        self.assertEqual(report["summary"]["skipped"], 1)
        self.assertEqual(report["findings"][0]["path"], "outside-link.txt")
        self.assertEqual(report["findings"][0]["status"], "skipped")
        self.assertIn("Symbolic link skipped", report["findings"][0]["skip_reason"])

    def test_symlink_target_is_reported_as_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            target = workspace / "marker.txt"
            target.write_text("SAFE_MARKER\n", encoding="utf-8")
            link = workspace / "target-link.txt"
            try:
                link.symlink_to(target)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symbolic links unavailable: {exc}")

            report = scan_directory(link, _marker_database())

        self.assertEqual(report["summary"]["files_scanned"], 0)
        self.assertEqual(report["summary"]["infected"], 0)
        self.assertEqual(report["summary"]["skipped"], 1)
        self.assertEqual(report["findings"][0]["status"], "skipped")


if __name__ == "__main__":
    unittest.main()
