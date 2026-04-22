import unittest

from sentinel.matchers import compute_hashes, find_hash_matches
from sentinel.signatures import parse_signature_database


EICAR_PARTS = (
    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}",
    b"$EICAR-STANDARD-ANTIVIRUS-",
    b"TEST-FILE!$H+H*",
)
EICAR_REFERENCE = b"".join(EICAR_PARTS)


class EicarReferenceTests(unittest.TestCase):
    def test_eicar_reference_bytes_match_known_length_and_hashes(self):
        hashes = compute_hashes(EICAR_REFERENCE)

        self.assertEqual(len(EICAR_REFERENCE), 68)
        self.assertEqual(hashes["md5"], "44d88612fea8a8f36de82e1278abb02f")
        self.assertEqual(hashes["sha256"], "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f")

    def test_eicar_reference_signature_matches_in_memory_fixture(self):
        database = parse_signature_database(
            {
                "schema_version": "1.0",
                "signatures": [
                    {
                        "id": "sig-eicar-standard-antivirus-test-file",
                        "name": "EICAR Standard Anti-Virus Test File",
                        "category": "safe-standard-test-file",
                        "severity": "high",
                        "matchers": [
                            {"type": "md5", "value": "44d88612fea8a8f36de82e1278abb02f"},
                            {
                                "type": "sha256",
                                "value": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
                            },
                        ],
                    }
                ],
            }
        )

        matches = find_hash_matches(compute_hashes(EICAR_REFERENCE), database)

        self.assertEqual({match.matcher.type for match in matches}, {"md5", "sha256"})
        self.assertEqual({match.signature.id for match in matches}, {"sig-eicar-standard-antivirus-test-file"})


if __name__ == "__main__":
    unittest.main()
