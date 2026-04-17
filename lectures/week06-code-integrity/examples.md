# Week 06 Examples

## Signed Update Example

A software update should be downloaded over a protected channel and verified with a trusted signature before execution. The signature matters because attackers may be able to replace the file in transit or at rest.

## Loader Policy Example

An operating system may allow only signed drivers to load into privileged contexts. This reduces risk, but it depends on signing-key protection and policy enforcement.

## Practice Prompt

For one software update flow, identify:

- artifact being trusted
- integrity check
- signing identity
- trust root
- failure mode
