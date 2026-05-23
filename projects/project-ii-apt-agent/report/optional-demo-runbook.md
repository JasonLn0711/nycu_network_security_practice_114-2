# Optional Demo Runbook

Purpose: support the required "system function demonstration" without risking a
failed live Docker session during a `10` minute report.

## Recommendation

Use the evidence walkthrough as the default demo.

Only run a live Docker demo if all of these are true before class:

- Docker is already running.
- IC and EC images are already built.
- The demo command has passed on the same laptop within the last hour.
- You can complete the demo in under `60` seconds.
- You have screenshots/logs ready as fallback.

## Demo Option A - Evidence Walkthrough

Risk: low.

Time: `90-120` seconds.

Use this unless the instructor explicitly asks for a live run.

### Step A1 - Show success artifact

File:

```text
../submissions/jingzhong-success/lab/shared/success.txt
```

Expected content:

```text
Backdoor triggered
Fri May 22 16:50:15 UTC 2026
```

Talking point:

> This is the saved IC-side success artifact. It is the grading condition we
> want: `/backdoor` has run and wrote `/shared/success.txt`.

### Step A2 - Show exploit log

File:

```text
../submissions/jingzhong-success/lab/shared/exploit-log.txt
```

Lines to point out:

- analyzer completed;
- selected `execute_task = 0x401415`;
- selected `ret_gadget = 0x401414`;
- used `offset_to_ret = 104`;
- wrote final payload;
- created `/shared/exploit_done`.

Talking point:

> This shows the EC-side `/exploit` behavior: analyze, select target and gadget,
> write the payload, then signal IC through `exploit_done`.

### Step A3 - Show target analysis

File:

```text
../submissions/jingzhong-success/lab/shared/target_info.json
```

Fields to show:

- `pie_info.pie = false`;
- `discovered_targets.execute_task.address = 0x401415`;
- `discovered_targets.user_input.address = 0x404340`;
- `discovered_targets.user_input_len.address = 0x404540`;
- `discovered_gadgets.preferred_ret.address = 0x401414`.

Talking point:

> The agent is not only emitting a hard-coded command. It records target facts
> and uses the discovered helper path.

### Step A4 - Show payload flow diagram

Use Slide 5:

```text
user_input =
  /backdoor\0
  + padding to offset 104
  + ret gadget
  + execute_task
```

Talking point:

> The payload stages `/backdoor` as data and then returns to the helper that
> calls `system(user_input)`.

## Demo Option B - Terminal Evidence Demo

Risk: low-medium.

Time: `60-90` seconds.

Run from:

```sh
cd /Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/nycu_114-2_network_security_practices/projects/project-ii-apt-agent
```

Commands:

```sh
sed -n '1,5p' submissions/jingzhong-success/lab/shared/success.txt
sed -n '1,25p' submissions/jingzhong-success/lab/shared/exploit-log.txt
python3 - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("submissions/jingzhong-success/lab/shared/target_info.json").read_text())
targets = data["discovered_targets"]
gadgets = data["discovered_gadgets"]

print("pie:", data["pie_info"]["pie"])
for name in ("execute_task", "user_input", "user_input_len"):
    target = targets[name]
    print(f"{name}: {target['address']} ({target['symbol']})")
print("preferred_ret:", gadgets["preferred_ret"]["address"])
PY
```

Fallback:

- If the terminal is too small, show the saved slide or open the JSON file in
  the editor.

## Demo Option C - Live Docker Run

Risk: medium-high in a `10` minute slot.

Use only if pre-tested immediately before class.

Rationale:

- Full Docker startup can exceed the report time.
- Container state, image cache, volume cleanup, and architecture flags can
  produce non-content failures.
- The instructor's requirement is system function demonstration and feature
  explanation, not necessarily a fresh rebuild.

Suggested live-demo stance:

> I have a pre-verified package and saved success evidence. I can run it live if
> time allows, but I will first show the deterministic evidence so the report is
> not dependent on Docker startup time.

If doing live demo:

1. Pre-build images before class.
2. Keep terminal in the package folder.
3. Keep one cleanup command ready.
4. Stop after one failed/slow command and switch to evidence.

Do not troubleshoot Docker during the `10` minute presentation.

## What Not To Demo

- Do not build images from scratch during the presentation.
- Do not run unrelated scans or external network commands.
- Do not show personal files outside the project folder.
- Do not present Jason's failed scaffold as the successful package.
- Do not claim success against the earlier `lab.zip` snapshot unless you have a
  separate rerun transcript for that exact binary.

## Final Demo Choice

Use Option A by default.

Use Option B if the classroom allows terminal display and you want a live feel
without running containers.

Use Option C only if the environment is already warm and the command sequence
has been tested immediately before class.
