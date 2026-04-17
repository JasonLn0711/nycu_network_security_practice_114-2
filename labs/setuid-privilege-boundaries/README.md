# Lab: Set-UID Privilege Boundaries

## Goal

Understand how privileged programs cross user boundaries and why environment handling matters.

## Tasks

- Explain RUID and EUID with a small example.
- Inspect permissions for a known privileged system binary.
- Identify environment variables that should not be trusted by privileged code.
- Summarize safer alternatives such as least privilege, capabilities, and service separation.

## Expected Evidence

- Command output or notes showing file permissions.
- A short RUID/EUID explanation.
- A defense checklist for privileged program design.
