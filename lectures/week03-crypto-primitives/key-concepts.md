# Week 03 Key Concepts

## Security Goals

- Confidentiality: unauthorized parties cannot read the data.
- Integrity: unauthorized changes can be detected.
- Authentication: the sender or peer is who they claim to be.
- Non-repudiation: a party cannot plausibly deny an action after the fact.

## Primitive Map

| Primitive | Primary Use |
| --- | --- |
| Symmetric encryption | Confidentiality with a shared key |
| Public-key encryption | Confidentiality or key exchange with asymmetric keys |
| Hash | Fixed-size digest for integrity checks and indexing |
| MAC | Integrity and authenticity with a shared secret |
| Digital signature | Integrity, authenticity, and non-repudiation with asymmetric keys |

## Exam Cue

Never say "hashing encrypts data." Hashing is one-way and does not provide confidentiality.
