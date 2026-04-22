import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class PrivateRepoExportTests(unittest.TestCase):
    def test_dry_run_lists_curated_private_repo_package(self):
        completed = subprocess.run(
            [sys.executable, "scripts/export_private_repo.py", "--dry-run"],
            cwd=PROJECT_ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        manifest = json.loads(completed.stdout)
        paths = {entry["path"] for entry in manifest["files"]}

        self.assertEqual(manifest["manifest_type"], "private-repo-export")
        self.assertIn("docs/requirements-traceability.md", paths)
        self.assertIn("docs/python/technical-design.md", paths)
        self.assertIn("docs/rust/README.md", paths)
        self.assertIn("demo/runbook.md", paths)
        self.assertIn("python/README.md", paths)
        self.assertIn("python/src/sentinel/cli.py", paths)
        self.assertIn("rust/Cargo.toml", paths)
        self.assertIn("rust/src/main.rs", paths)
        self.assertIn("scripts/check_release.py", paths)
        self.assertIn("report/final-report.pdf", paths)
        self.assertIn("report/final-report-v2.pdf", paths)
        self.assertIn("report/evidence-screenshots/signature-database.png", paths)
        self.assertIn("report/evidence-screenshots/release-gate.png", paths)
        self.assertIn("report/submission-package.md", paths)
        self.assertNotIn("project-spec.pdf", paths)
        self.assertNotIn("report/report-draft.md", paths)
        self.assertNotIn("report/private-repo-handoff.md", paths)
        self.assertNotIn("report/submission-checklist.md", paths)
        self.assertNotIn("report/final-report.aux", paths)
        self.assertNotIn("report/final-report-v2.aux", paths)
        self.assertFalse(manifest["safety"]["literal_eicar_file_stored"])

    def test_export_copies_package_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "export"
            manifest_path = Path(tmp) / "manifest.json"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/export_private_repo.py",
                    "--output",
                    str(output),
                    "--manifest",
                    str(manifest_path),
                    "--clean",
                ],
                cwd=PROJECT_ROOT,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            self.assertTrue((output / "README.md").is_file())
            self.assertTrue((output / "python/README.md").is_file())
            self.assertTrue((output / "python/src/sentinel/scanner.py").is_file())
            self.assertTrue((output / "rust/Cargo.toml").is_file())
            self.assertTrue((output / "rust/src/main.rs").is_file())
            self.assertTrue((output / "docs/python/technical-design.md").is_file())
            self.assertTrue((output / "demo/runbook.md").is_file())
            self.assertTrue((output / "report/submission-package.md").is_file())
            self.assertTrue((output / "report/final-report-v2.pdf").is_file())
            self.assertTrue((output / "report/evidence-screenshots/release-gate.png").is_file())
            self.assertFalse((output / "project-spec.pdf").exists())
            self.assertFalse((output / "report/final-report.aux").exists())
            self.assertFalse((output / "report/final-report-v2.aux").exists())
            self.assertGreater(manifest["file_count"], 40)


if __name__ == "__main__":
    unittest.main()
