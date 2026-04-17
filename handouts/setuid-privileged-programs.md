# Handout Note: Set-UID Privileged Programs

## Scope

This handout explains why privileged programs exist, how Set-UID works, and why it is both useful and dangerous.

## Why Privileged Programs Exist

The motivating example is the password dilemma:

- ordinary users need to change their passwords,
- but the sensitive password database must not be writable by ordinary users.

Operating systems solve this with controlled privilege-extension mechanisms rather than making every access-control rule infinitely fine-grained.

The handout distinguishes:

- daemons: privileged background services
- Set-UID programs: executable files that temporarily run with the owner's privilege

## Set-UID Mechanics

When a Set-UID program runs:

- `RUID` identifies who launched the program
- `EUID` identifies which privilege the process currently has
- access-control checks use `EUID`

For normal programs:

- `RUID == EUID`

For a root-owned Set-UID program:

- `RUID` stays as the invoking user
- `EUID` becomes `0`

Classic example:

```bash
ls -l /usr/bin/passwd
```

The `s` bit in the owner execute field marks Set-UID behavior.

## Attack Surfaces

The handout groups the risk into several categories.

### 1. Explicit User Input

Examples:

- buffer overflow
- format string bugs
- unsafe input sanitization in tools such as shell-changing programs

Lesson:

- a Set-UID bug is more dangerous because the bug runs while the process holds elevated privilege.

### 2. System Input

Examples:

- race conditions,
- symbolic-link abuse,
- world-writable-directory tricks.

Lesson:

- not all dangerous input comes from command-line arguments; filesystem state is also attacker-controlled input.

### 3. Environment Variables

Set-UID programs can be influenced by hidden process state such as:

- `PATH`
- loader-related variables

This connects directly to the environment-variable handout.

### 4. Capability Leaking

A privileged program may open a privileged resource, drop privilege, and then accidentally leave a powerful capability behind.

Example from the slides:

- an open file descriptor to a root-only file remains usable after privilege is downgraded.

Fix:

- clean up privileged resources before dropping privilege.

## Invoking External Commands Safely

The slides warn strongly against shell-based invocation.

Unsafe:

- `system()` mixes command execution with shell parsing
- user-provided data can become command code

Safer:

- use `execve()`
- provide the program path explicitly
- pass user input only as data arguments

Still risky:

- `execlp()`, `execvp()`, and similar helpers may search `PATH`

Broader lesson:

- this problem is not limited to C; shell-like invocation in Perl, PHP, and other languages creates the same risk.

## Design Principles

Two principles are made explicit in the handout:

### Isolation

Do not mix code and data.

This is the same mental model behind:

- command injection,
- SQL injection,
- XSS,
- many memory-corruption exploitation paths.

### Least Privilege

- give the program only the power it needs
- drop or discard privilege when it is no longer needed
- use `seteuid()` or `setuid()` when appropriate

## What To Remember

- Set-UID is a narrow privilege-delegation mechanism, not a general license to trust the program.
- The attack surface includes user input, system state, environment state, and leftover capabilities.
- Shell-based execution inside privileged programs is almost always a red flag.

## Review Checklist

- Can I explain `RUID` vs `EUID` clearly?
- Do I know why Set-UID exists even though it is risky?
- Can I describe why `system()` is dangerous in a privileged program and why `execve()` is safer?
- Do I understand how privilege dropping can still fail if resources are not cleaned up?
