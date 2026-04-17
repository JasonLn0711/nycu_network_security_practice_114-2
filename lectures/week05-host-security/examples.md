# Week 05 Examples

## Set-UID Example

The `passwd` program needs controlled privilege to update password data that ordinary users cannot edit directly. The risk is that any input-parsing or environment-handling bug may run with elevated privilege.

## Access Control Example

An ACL answers "who can access this object?" A capability answers "what objects can this subject access?" Both can implement the same access matrix from different directions.

## Bell-LaPadula Example

"No read up" prevents a lower-cleared subject from reading higher-classified data. "No write down" prevents a higher-cleared subject from leaking data into a lower-classified object.

## Practice Prompt

Choose one privileged program and write:

- needed privilege
- risky inputs
- safer design
- audit evidence
