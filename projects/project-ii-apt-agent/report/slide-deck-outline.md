# Slide Deck Outline

Target length: `10` minutes.

Recommended deck size: `9` slides.

Style: concise technical slides with one diagram or evidence screenshot per
slide when possible. Avoid dense paragraphs.

## Slide 1 - Project II: Autonomous APT Agent

Time: `0:00-0:30`

Purpose: identify the project and state the result.

Bullets:

- Course: Network Security Practice - Attack and Defense
- Project II: Autonomous APT Agent
- Team: 313264012 Chen Jingzhong, 513559004 Lin Jiasheng
- Work model: two-person group project with split implementation,
  evidence, and report preparation
- Result: successful bounded lab package with `/exploit`, `/triage`, and
  `/shared/success.txt` evidence

Visual:

- Simple title slide.
- Optional: small EC -> `/shared` -> IC diagram.

Talk track:

> This project builds the external-container side of the course lab. The goal is
> a bounded agent that interacts with the provided shared-volume grading
> environment.

## Slide 2 - Assignment Interface

Time: `0:30-1:20`

Purpose: show what the grader expects.

Bullets:

- EC runs `/exploit` first.
- `/exploit` writes `/shared/config.data`.
- `/exploit` creates `/shared/exploit_done`.
- IC processes `config.data` with `blogic`.
- If `/backdoor` runs, `/shared/success.txt` appears.
- If not, coredump/no-success feedback is used by `/triage`.

Visual:

```text
/exploit -> config.data + exploit_done -> IC/blogic
       <- coredump / no-success / success.txt <- /triage
```

Talk track:

> The interface is the important part: the EC follows the shared-volume
> protocol and causes the IC side to reach the success condition.

## Slide 3 - System Architecture

Time: `1:20-2:20`

Purpose: explain the three-module design.

Bullets:

- Target Analyzer: reads `/shared/blogic.copy` or `/shared/blogic`.
- Exploit Generator: chooses strategy and writes `config.data`.
- Triage Feedback: reads result and updates `state.json`.
- Shared artifacts: `target_info.json`, `state.json`, `config.data`,
  `exploit_done`, `success.txt`.

Visual:

```text
Target Analyzer -> target_info.json
          |              |
          v              v
Exploit Generator -> config.data -> exploit_done
          ^
          |
Triage Feedback <- success/coredump/state
```

Talk track:

> The agent has perception, action, and feedback. It first understands the
> binary, then generates one attempt, then updates state after observing the
> result.

## Slide 4 - Target Analyzer

Time: `2:20-3:25`

Purpose: show why the system is analysis-driven.

Bullets:

- Detects ELF metadata: x86_64, non-PIE, NX / stack status.
- Parses symbols: `execute_task`, `parse_config`, `user_input`,
  `user_input_len`.
- Finds risky imports: `memcpy`, `system`.
- Finds ret gadgets and selects a preferred `ret`.
- Writes structured `target_info.json`.

Visual:

- Screenshot or excerpt from `target_info.json`.
- Highlight:
  - `execute_task = 0x401415`
  - `ret_gadget = 0x401414`

Talk track:

> The important discovery is `execute_task`. It is a helper path that calls
> `maintenance_task(user_input)`, so returning to it avoids the hardest
> first-argument setup problem.

## Slide 5 - Exploit Generation And Payload Flow

Time: `3:25-4:45`

Purpose: explain how the successful attempt works without overloading the
audience.

Bullets:

- Payload starts with `/backdoor\x00`.
- Padding reaches the saved return address.
- Return path uses `ret_gadget` then `execute_task`.
- `execute_task()` calls `maintenance_task(user_input)`.
- `maintenance_task()` calls `system(user_input)`.

Visual:

```text
user_input =
  /backdoor\0
  + padding to offset 104
  + ret gadget
  + execute_task
```

Talk track:

> The core success path is not arbitrary code execution. It is a controlled
> redirection to a helper already inside the lab binary. The helper supplies the
> correct argument from global `user_input`.

## Slide 6 - Triage And Adaptive Probing

Time: `4:45-5:45`

Purpose: explain the feedback loop and autonomous behavior.

Bullets:

- `/triage` checks `success.txt`.
- If no success, it checks coredumps or no-success state.
- Adaptive mode advances offset candidates.
- Demonstrated candidate sequence:
  `64 -> 72 -> 80 -> 88 -> 96 -> 104`.
- Offset `104` is reached within the `60` round limit.

Visual:

```text
Round 1: 64  -> no success
Round 2: 72  -> no success
Round 3: 80  -> no success
Round 4: 88  -> no success
Round 5: 96  -> crash
Round 6: 104 -> success
```

Talk track:

> Fast mode is best for grading. Adaptive mode shows that the system can also
> update its next action based on feedback.

## Slide 7 - System Features

Time: `5:45-6:50`

Purpose: satisfy the "system feature explanation" requirement.

Bullets:

- Analysis-driven: extracts target facts before payload generation.
- State-driven: stores strategy and round state in `/shared/state.json`.
- Feedback-aware: `/triage` uses success/crash/no-success observations.
- Bounded: only uses `/shared` and supplied lab binaries.
- Stable grading path: fast mode can use known-good calibrated offset.
- Demonstration path: adaptive mode shows autonomous search behavior.

Visual:

- Feature matrix:

| Feature | Evidence |
| --- | --- |
| Analyzer | `target_info.json` |
| Exploit | `config.data`, `exploit-log.txt` |
| Triage | `state.json`, adaptive result files |
| Success | `success.txt` |

Talk track:

> The system features are designed for this class lab: enough autonomy to
> analyze and adapt, with a clear course-lab boundary.

## Slide 8 - Demo / Evidence Walkthrough

Time: `6:50-9:20`

Purpose: show the required function demonstration.

Preferred low-risk evidence demo:

1. Open `lab/shared/success.txt`.
2. Open `lab/shared/exploit-log.txt`.
3. Show `target_info.json` entries for `execute_task` and `ret_gadget`.
4. Show the payload flow diagram.

Optional live demo only if pre-tested:

- Start from already built images and a warm Docker environment.
- Run only one command sequence.
- Stop immediately if it takes more than `30` seconds and return to saved
  evidence.

Talk track:

> For the demo, I will show the saved successful run evidence first. The key
> line is that the exploit selected `execute_task`, used offset `104`, wrote
> the payload, signaled `exploit_done`, and the IC produced `success.txt`.

## Slide 9 - Conclusion And Limitation

Time: `9:20-10:00`

Purpose: close honestly and safely.

Bullets:

- Project II package satisfies the EC interface:
  `/exploit`, `/triage`, `config.data`, `exploit_done`.
- Successful evidence exists in the package.
- The work is bounded to the course lab.
- The work stays within the course-lab boundary.
- Binary-version caveat: this success should be tied to this package's IC
  binary context.

Talk track:

> The main result is a bounded analysis-driven agent that completes the course
> lab flow in the successful package. The important technical point is the
> helper function `execute_task`, which bridges controlled data in `user_input`
> to the IC-side `/backdoor` execution path.
