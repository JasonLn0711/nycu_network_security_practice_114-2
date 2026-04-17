# Handout Note: Linux Security Basics

## Scope

This handout covers the baseline host-security mechanisms in Linux:

- identities,
- permissions,
- controlled privilege use,
- authentication storage and policy.

## Users And Groups

Linux access control begins with identity.

- Each user has a unique UID.
- Groups let the system assign permissions to sets of users.
- A user can belong to multiple groups.
- The primary account record is stored in `/etc/passwd`.

Study point:

- Linux does not reason about names first; it reasons about identifiers and membership.

Useful commands:

```bash
id
groups
getent passwd
getent group
```

## Traditional Permissions

The handout reviews the classic owner/group/other model.

For files:

- `r`: read content
- `w`: modify content
- `x`: execute file

For directories:

- `r`: list directory entries
- `w`: create or remove entries
- `x`: traverse or enter the directory

Important companion concept:

- `umask` controls the default permissions of newly created files and directories.

Useful commands:

```bash
ls -l
umask
chmod
chown
chgrp
```

## ACLs

POSIX ACLs extend the traditional model with more fine-grained rules.

Why they matter:

- the owner/group/other model is often too coarse for real collaboration.

Typical tools:

```bash
getfacl <path>
setfacl -m u:alice:rwx <path>
```

## Running Commands With Privilege

The handout compares several mechanisms:

- `sudo`
- Set-UID programs
- POSIX capabilities

Key idea:

- "root" can be decomposed. Not every task needs full superuser power.

Examples from the slides:

- `sudo` for controlled admin command execution
- `ping` using `CAP_NET_RAW`
- Wireshark splitting privileged packet capture into `dumpcap` rather than making the whole GUI privileged

Study takeaway:

- least privilege is easier to enforce when privileges are narrow and explicit.

## Authentication

The last section covers how Linux stores and protects account information.

- `/etc/passwd` stores account metadata
- `/etc/shadow` stores password hashes and related policy data
- salts make identical passwords produce different hashes and weaken dictionary/rainbow-table attacks
- accounts can be locked by placing an invalid value in the password field

Related security idea:

- authentication can be based on what the user knows, has, or is/does
- MFA combines factors rather than relying only on passwords

## What To Remember

- Linux security basics are mostly about identifying the subject correctly and then applying the right policy layer.
- Traditional permissions are simple but limited.
- ACLs and capabilities improve granularity.
- `/etc/shadow` exists because password material must be more tightly protected than general account metadata.

## Review Checklist

- Can I explain the difference between file and directory `r`, `w`, and `x`?
- Do I know when ACLs help more than plain UNIX permissions?
- Can I explain why capabilities are safer than giving every privileged tool full root power?
- Do I understand the security reason for separating `/etc/passwd` and `/etc/shadow`?
