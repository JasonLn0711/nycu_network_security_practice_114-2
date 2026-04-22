import unittest
import tempfile
from pathlib import Path

from sentinel.matchers import (
    PatternScanEngine,
    compute_hashes,
    find_hash_matches,
    find_pattern_matches,
    scan_file_content,
)
from sentinel.signatures import parse_signature_database


class MatcherTests(unittest.TestCase):
    def test_hashes_are_computed(self):
        hashes = compute_hashes(b"safe demo")

        self.assertEqual(hashes["md5"], "00ed24f2abe0d1fc23ba8a7abaca7eeb")
        self.assertEqual(hashes["sha256"], "45e777cc8b81bfb652f2f1f3d46dd1b1c70caf720f61eba585af451b31d27afd")

    def test_hash_matches_use_bloom_precheck_then_exact_index(self):
        digest = "45e777cc8b81bfb652f2f1f3d46dd1b1c70caf720f61eba585af451b31d27afd"
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-hash",
                        "name": "Hash Marker",
                        "category": "safe-mock-virus",
                        "severity": "critical",
                        "matchers": [{"type": "sha256", "value": digest}],
                    }
                ],
            }
        )

        matches = find_hash_matches({"sha256": digest}, database)
        misses = find_hash_matches({"sha256": "0" * 64}, database)

        self.assertEqual([match.signature.id for match in matches], ["sig-hash"])
        self.assertEqual(misses, [])

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
        self.assertEqual(content.pattern_matches[0].matcher.signature.id, "sig-boundary-marker")
        self.assertEqual(content.pattern_matches[0].offset, 3)

    def test_aho_corasick_engine_finds_overlapping_patterns(self):
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-abc",
                        "name": "ABC",
                        "category": "safe-mock-virus",
                        "severity": "high",
                        "matchers": [{"type": "hex_pattern", "value": "414243"}],
                    },
                    {
                        "id": "sig-bc",
                        "name": "BC",
                        "category": "safe-mock-virus",
                        "severity": "medium",
                        "matchers": [{"type": "hex_pattern", "value": "4243"}],
                    },
                ],
            }
        )

        matches = PatternScanEngine(database.patterns).scan(b"xxABCxx")

        self.assertEqual([match.matcher.signature.id for match in matches], ["sig-abc", "sig-bc"])
        self.assertEqual([match.offset for match in matches], [2, 3])

    def test_aho_corasick_stream_preserves_state_between_chunks(self):
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-stream",
                        "name": "Stream",
                        "category": "safe-mock-virus",
                        "severity": "critical",
                        "matchers": [{"type": "hex_pattern", "value": "53545245414d"}],
                    }
                ],
            }
        )
        scanner = PatternScanEngine(database.patterns).stream()

        scanner.feed(b"xxSTR")
        scanner.feed(b"EAMyy")
        matches = scanner.finish()

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].matcher.signature.id, "sig-stream")
        self.assertEqual(matches[0].offset, 2)


if __name__ == "__main__":
    unittest.main()
