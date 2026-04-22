import unittest

from sentinel.signatures import SignatureError, parse_signature_database


class SignatureDatabaseTests(unittest.TestCase):
    def test_valid_database_builds_hash_and_pattern_indexes(self):
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-demo",
                        "name": "Demo",
                        "category": "safe-mock-virus",
                        "severity": "critical",
                        "matchers": [
                            {"type": "sha256", "value": "a" * 64},
                            {"type": "hex_pattern", "value": "53414645"},
                        ],
                    }
                ],
            }
        )

        self.assertEqual(database.schema_version, "1.0")
        self.assertIn("a" * 64, database.hash_index["sha256"])
        self.assertEqual(database.patterns[0].pattern, b"SAFE")

    def test_invalid_hash_is_rejected(self):
        with self.assertRaises(SignatureError):
            parse_signature_database(
                {
                    "schema_version": "1.0",
                    "signatures": [
                        {
                            "id": "sig-demo",
                            "name": "Demo",
                            "category": "safe-mock-virus",
                            "severity": "critical",
                            "matchers": [{"type": "sha256", "value": "too-short"}],
                        }
                    ],
                }
            )


if __name__ == "__main__":
    unittest.main()
