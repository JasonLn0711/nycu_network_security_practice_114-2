# Handout Note: Environment Variables And Attacks

## Scope

This handout explains how environment variables work at process level and why they become dangerous when privileged programs trust them.

## Core Mechanics

Environment variables are named values attached to a process environment. They influence runtime behavior without changing the program binary itself.

Important points from the handout:

- `PATH` affects how commands are found when no full path is given.
- A child created by `fork()` inherits the parent's environment.
- A process that replaces itself with `execve()` loses the old memory image, but new environment variables can be passed explicitly through `execve()`'s third argument.
- In C, environment variables can be reached through `envp` or the global `environ`.

Subtle but important detail:

- `envp` and `environ` may point to the same place initially.
- After environment changes, storage can move, so `environ` is the safer reference.

## Shell Variables vs Environment Variables

The handout emphasizes that these are not the same thing.

- Shell variables are internal to the shell.
- Environment variables are exported into child processes.
- `export` is the bridge from shell variable to environment variable.

Useful observation command:

```bash
strings /proc/$$/environ
```

This shows the current shell process's environment.

## Major Attack Surfaces

The slides organize the risk into several layers:

### 1. Dynamic Linker

Dangerous variables such as `LD_PRELOAD` and `LD_LIBRARY_PATH` can influence which shared libraries get loaded.

Risk:

- attacker-controlled code may run before the intended library code.

Defense:

- when `EUID != RUID`, the loader treats the program as security-sensitive and ignores dangerous linker-related variables.

### 2. External Program Invocation

If privileged code uses `system("cmd")`, the shell becomes part of the execution path.

Risk:

- command lookup can be hijacked through `PATH`,
- user-controlled data may be reinterpreted as code.

Safer pattern:

- use `execve()` and provide the command path explicitly,
- avoid shell-based execution in privileged code.

### 3. Libraries And Search Paths

Even when the main program looks safe, indirect loading behavior can still be controlled through environment-dependent library resolution.

Main lesson:

- the attack surface is larger than the program source code alone.

### 4. Application Code

Programs may directly call `getenv()` and then misuse the result.

Example risk:

- oversized environment-variable values copied into fixed-size buffers can trigger buffer overflow.

Safer idea:

- use `secure_getenv()` in security-sensitive code,
- validate size and format before use.

## Design Lesson

The handout closes by comparing:

- Set-UID approach: the privileged program directly runs in the user's contaminated environment
- Service approach: privileged work is moved into a dedicated service with a narrower interface

This is the architecture-level defense:

- isolate privilege,
- reduce trust in user-controlled process state,
- keep code and data clearly separated.

## What To Remember

- Environment variables are inputs.
- Hidden inputs are still inputs.
- Privileged code should avoid inheriting behavior from user-controlled runtime state.
- `execve()` is safer than `system()` because it separates command name from data.

## Review Checklist

- Can I explain how `fork()` and `execve()` affect environment inheritance?
- Do I know why `LD_PRELOAD` is dangerous?
- Can I explain a `PATH`-based privilege-escalation attack?
- Do I understand why service-based privilege separation is safer than Set-UID plus environment filtering?
