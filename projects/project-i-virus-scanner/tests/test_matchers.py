import unittest
import tempfile
from pathlib import Path

from sentinel.matchers import compute_hashes, find_pattern_matches, scan_file_content
from sentinel.signatures import parse_signature_database


class MatcherTests(unittest.TestCase):
    def test_hashes_are_computed(self):
        hashes = compute_hashes(b"safe demo")

        self.assertEqual(hashes["md5"], "00ed24f2abe0d1fc23ba8a7abaca7eeb")
        self.assertEqual(hashes["sha256"], "45e777cc8b81bfb652f2f1f3d46dd1b1c70caf720f61eba585af451b31d27afd")

    def test_pattern_match_finds_hex_signature(self):
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

        matches = find_pattern_matches(b"prefix SAFE suffix", database)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].signature.id, "sig-marker")

    def test_chunked_scan_finds_pattern_across_chunk_boundary(self):
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-boundary-marker",
                        "name": "Boundary Marker",
                        "category": "safe-mock-virus",
                        "severity": "critical",
                        "matchers": [{"type": "hex_pattern", "value": "4142434445"}],
                    }
                ],
            }
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "boundary.bin"
            path.write_bytes(b"xxxABCDEyyy")
            content = scan_file_content(path, database, chunk_size=4)

        self.assertEqual(content.size_bytes, 11)
        self.assertEqual(len(content.pattern_matches), 1)
        self.assertEqual(content.pattern_matches[0].signature.id, "sig-boundary-marker")


if __name__ == "__main__":
    unittest.main()
