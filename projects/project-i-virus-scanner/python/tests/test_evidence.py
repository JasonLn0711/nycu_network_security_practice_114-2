import json
import tempfile
import unittest
from pathlib import Path

from sentinel.evidence import build_evidence_manifest, write_evidence_manifest


class EvidenceTests(unittest.TestCase):
    def test_build_evidence_manifest_records_tree_reports_and_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "demo-tree"
            target.mkdir()
            (target / "clean.txt").write_text("clean\n", encoding="utf-8")
            nested = target / "nested"
            nested.mkdir()
            (nested / "mock.txt").write_text("SAFE_MARKER\n", encoding="utf-8")
            signatures = root / "signatures.json"
            signatures.write_text('{"schema_version": "1.0", "signatures": []}\n', encoding="utf-8")
            report = root / "report.json"
            report.write_text(
                json.dumps({"tool": "Sentinel", "target": str(target), "summary": {"infected": 1}}),
                encoding="utf-8",
            )

            manifest = build_evidence_manifest(
                target=target,
                signatures=signatures,
                reports=[report],
            )

        self.assertEqual(manifest["tool"], "Sentinel")
        self.assertFalse(manifest["safety"]["uses_live_malware"])
        self.assertEqual(len(manifest["demo_tree"]), 2)
        self.assertEqual(manifest["reports"][0]["summary"]["infected"], 1)
        self.assertIn("test_command", manifest["reproducibility"])

    def test_write_evidence_manifest_writes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "manifest.json"
            write_evidence_manifest({"tool": "Sentinel"}, output)
            loaded = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(loaded["tool"], "Sentinel")


if __name__ == "__main__":
    unittest.main()
