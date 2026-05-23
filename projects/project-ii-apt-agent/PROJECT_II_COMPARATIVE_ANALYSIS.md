# Project II Comparative Analysis - Jason vs Jingzhong

Date: 2026-05-23

Perspective: postdoctoral research-style analysis of the two Project II work
lines. This document records why Jason's attempt failed, why Chen Jingzhong's
package succeeded, what the two approaches were really optimizing for, and what
important lessons should be preserved for future coursework, research, and
collaboration.

## Executive Summary

FIRST PRINCIPLE: an exploit result is only complete when the full state
predicate is satisfied in the actual target context: controllable transfer,
valid call target, valid argument state, compatible binary assumptions, and an
observable success artifact. Documentation and packaging help, but they do not
replace that predicate.

The central difference is not merely that Jingzhong found a better payload. The
central difference is that the two work lines were effectively solving different
binary shapes.

Jason's line attacked the earlier preserved `lab.zip` / Phase II binary, where
the problem after return-address control was still unresolved: the exploit had
to make a success-relevant function receive a controlled first argument. Jason's
evidence shows the EC protocol worked, but the IC did not create
`/shared/success.txt`. In concrete terms, Jason could influence control flow but
could not reliably arrange the required semantic state for `/backdoor`
execution.

Jingzhong's successful package contains a different IC server shape. That
server includes an `execute_task()` function that takes no arguments and calls
`maintenance_task(user_input)`, while `maintenance_task()` directly calls
`system(arg)`. This helper turns the hard problem from "control RIP and set up
`rdi`" into a simpler ret-to-helper path: place `/backdoor` in global
`user_input`, then redirect control to `execute_task()`. This removes the
argument-control blocker that stopped Jason's line.

Therefore, the honest attribution is:

- Jason completed Project II setup, scaffold, protocol, documentation, and a
  serious failure/recovery investigation, but his own exploit path did not meet
  the success gate.
- Jingzhong completed the successful Project II package, with evidence under
  `submissions/jingzhong-success/`.
- The success claim should be tied to Jingzhong's package and binary context,
  not retroactively assigned to Jason's earlier scaffold or to the earlier
  preserved `lab.zip` snapshot.

## Source Files Used

Primary comparison files:

| File | What it contributes |
| --- | --- |
| `OWNERSHIP_AND_OUTCOME.md` | Ownership split, binary checksum boundary, evidence caveats, package routing. |
| `project2-agent-scaffold/docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md` | Jason work-line verdict: protocol-complete partial, not full-credit complete. |
| `project2-agent-scaffold/docs/PHASE2_SUCCESS_VALIDATION.md` | Jason failure mechanism: no `/shared/success.txt`, stale/incorrect first-argument state. |
| `submissions/jingzhong-success/lab/IC/server.cpp` | Jingzhong target shape with `execute_task()`, `user_input_len`, binary-mode config parsing, and direct `system(arg)`. |
| `submissions/jingzhong-success/lab/IC/server_prev.cpp` | Older server shape resembling the harder argument-control problem. |
| `submissions/jingzhong-success/lab/EC/exploit` | Jingzhong EC exploit selection logic: analyzer, `execute_task`, ret gadget, offset strategy. |
| `submissions/jingzhong-success/lab/shared/exploit-log.txt` | Saved successful final-mode run evidence. |
| `submissions/jingzhong-success/lab/shared/success.txt` | Saved success artifact. |

## Evidence Boundary

The extracted Jingzhong package is not byte-identical to the earlier repo
`lab.zip` snapshot.

| Item | Earlier `lab.zip` snapshot | Jingzhong success package |
| --- | --- | --- |
| `IC/server_1` SHA-256 | `5fbcb18762083b220d2c21f7cdbeacb359c2dd910f52c375de11f17b57dbb7cf` | `e3a7bd6957d6680982149239f86115f97ec0ea070fbf2f2821400b6002d866d1` |
| `IC/server_2` SHA-256 | `155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c` | `465d7fd6058c6fa4aeddaa05d560ef548bc132cfd675d2d0aadad4b82c6c724b` |
| `execute_task()` | Absent | Present at `0x401415` |
| `user_input_len` | Absent | Present at `0x404540` |
| `log_message` signature | `log_message(char const*)` | `log_message(char const*, unsigned long)` |

Interpretation:

- This does not invalidate Jingzhong's successful package.
- It does mean the success evidence must be attributed to the package that
  actually contains this binary shape.
- If future work needs to claim success against the earlier `lab.zip`, that
  exact environment must be rerun and verified. It should not be inferred from
  Jingzhong's package.

## The Actual Technical Difference

### Jason's harder target shape

The older server shape has:

```cpp
char user_input[64];

void log_message(const char *msg) {
    char buf[96];
    sprintf(buf, "[LOG]: %s", msg);
    cout << buf << endl;
}

void maintenance_task(const char *arg) {
    char cmd[128];
    snprintf(cmd, sizeof(cmd), "echo '%s' >> /tmp/server.log", arg);
    system(cmd);
}
```

The immediate vulnerability is stack overwrite through the logging path. But
even if the return address is controlled, the exploit still needs to make the
target call path receive the right first argument.

Jason's validation log records exactly this failure mode. The candidate used a
command-injection-shaped prefix, padding to the observed saved return address,
and a partial return overwrite toward `maintenance_task+5`. IC consumed
`/shared/exploit_done`, but no `/shared/success.txt` appeared. The debug state
showed that at the end of `log_message`, `rdi` did not point at `user_input`;
it pointed at a glibc stdout-lock area containing zero bytes. Returning into the
maintenance path therefore did not execute the intended `/backdoor` command.

This is a semantic failure, not just an address failure. Control-flow influence
was present, but the program state at the transfer point was wrong.

### Jingzhong's successful target shape

Jingzhong's package includes a server shape with:

```cpp
char user_input[512];
size_t user_input_len = 0;

void maintenance_task(const char *arg) {
    system(arg);
}

__attribute__((used))
void execute_task() {
    maintenance_task(user_input);
    exit(0);
}

void log_message(const char *msg, size_t len) {
    char buf[96];
    memcpy(buf, msg, len);
}
```

This changes the problem dramatically.

The helper `execute_task()` is a ret-to-win style target. It requires no first
argument from the exploit. The function itself loads the already-staged global
`user_input` and passes it to `maintenance_task()`. Since `maintenance_task()`
directly calls `system(arg)`, placing `/backdoor` in `user_input` is sufficient
once control reaches `execute_task()`.

That is why Jingzhong's path succeeds:

1. The config parser copies the `user_input` value into global `user_input`.
2. The payload begins with `/backdoor\x00`, so `system()` sees `/backdoor`.
3. The overflow reaches the saved return address.
4. The saved return address is redirected through a `ret` gadget and then to
   `execute_task()`.
5. `execute_task()` calls `maintenance_task(user_input)`.
6. `maintenance_task()` calls `system(user_input)`.
7. `/backdoor` writes `/shared/success.txt`.

The saved exploit log confirms the selected elements:

- `execute_task = 0x401415`
- `ret_gadget = 0x401414`
- `offset_to_ret = 104`
- mode `final_exploit`
- payload length `120` bytes
- `/shared/exploit_done` created

The success artifact then records:

```text
Backdoor triggered
Fri May 22 16:50:15 UTC 2026
```

## Why Jason's Direction Failed

Jason's direction was technically coherent, but it was aimed at a harder
problem. The preserved notes show the protocol was not the blocker:

- `/exploit` and `/triage` existed.
- `/exploit` wrote `/shared/config.data`.
- `/exploit` created `/shared/exploit_done`.
- IC consumed the marker.
- The scaffold preserved state and evidence.

The blocker was candidate generation against the specific Phase II binary.

The hard constraints were:

- The first argument to the success-relevant function was not controlled at the
  transfer point.
- C-string behavior and embedded NUL bytes constrained how much of the stack
  and follow-on data could be encoded.
- NX blocked direct stack execution.
- Useful gadgets in the main binary were limited.
- Saved RBP / saved RIP interactions made simple maintenance-body entry
  unstable.
- Appended ROP did not behave like a clean second stage because the stack after
  the return was not freely controlled in the expected way.
- Heap and global-state side effects produced interesting primitives but did
  not produce `/shared/success.txt`.

The shortest accurate phrase is:

> Jason controlled parts of the exploit protocol and parts of control flow, but
> did not find a route that controlled the success function's semantic input.

This matters because many exploit failures are not failures of effort. They are
failures to satisfy the full state predicate:

```text
control-flow transfer + valid call target + valid argument state + allowed memory/protection state + observable success artifact
```

Jason's attempts repeatedly achieved subsets of that predicate, but not the full
predicate.

## Why Jingzhong's Direction Succeeded

Jingzhong's direction succeeded because it found or used a target shape where
the success predicate was much easier to satisfy.

The decisive property was not "agentic AI" or "adaptive probing" by itself. The
decisive property was the helper function:

```cpp
void execute_task() {
    maintenance_task(user_input);
    exit(0);
}
```

This helper eliminates the hardest part of Jason's route. Instead of solving
`rdi = user_input` at the moment of hijacked control transfer, the exploit only
has to redirect execution to code that already performs that argument setup.

Jingzhong's implementation then adds useful engineering around that fact:

- analyzer-driven target selection;
- symbol discovery for `execute_task`;
- preferred `ret` gadget discovery;
- fallback / calibrated offset handling;
- adaptive offset candidate probing for demonstration;
- `/triage` state updates;
- saved logs and report narrative.

However, analytically, the core success is the ret-to-helper simplification.
The adaptive agent layer makes the package more assignment-aligned and more
explainable, but the helper function is what makes the exploit tractable.

## Directional Difference

| Dimension | Jason line | Jingzhong line |
| --- | --- | --- |
| Primary goal | Build correct EC protocol, then recover a valid Phase II exploit path. | Produce a successful package with analyzer, exploit, triage, and report. |
| Target assumption | Earlier `lab.zip` Phase II server without `execute_task()`. | Package server with `execute_task()` helper. |
| Main technical bottleneck | First-argument setup after control-flow hijack. | Saved return-address offset and helper-target selection. |
| Success strategy | Try to redirect to maintenance/system-like paths while preserving or staging argument state. | Put `/backdoor` in `user_input`; return to `execute_task()`. |
| Failure/success artifact | No `/shared/success.txt` from official local flow. | Saved `/shared/success.txt` in package. |
| Research value | Strong negative evidence and handoff; maps dead ends. | Successful coursework artifact; demonstrates usable agent loop. |
| Risk in interpretation | Mistaking protocol completeness for exploit completion. | Mistaking a helper-enabled binary for the harder earlier binary. |

## Things Jason May Not Have Fully Considered

### 1. Target identity is the first exploit primitive

Before exploit design, pin the exact binary:

- file hash;
- symbol table;
- protection flags;
- source/binary relationship;
- phase number;
- instructor/package version;
- whether the teammate or TA supplied an updated lab.

In this case, the existence of `execute_task()` is not a small implementation
detail. It changes the vulnerability class from hard argument-control exploit
development to a ret-to-helper pattern. A single helper symbol can dominate the
entire difficulty analysis.

Future rule:

> Never compare exploit attempts until the binary identity and symbol surface
> are compared first.

### 2. "Agentic" behavior and "successful exploit" are separable claims

The report frames the system as an autonomous APT agent with fast mode and
adaptive offset probing. That is acceptable as a course narrative, but the
actual success path in the saved final log uses a calibrated fallback offset
`104` and direct `execute_task` selection.

This means there are two claims:

1. The system can act like an agent: analyze target, maintain state, triage,
   probe offsets.
2. The submitted package succeeds: final mode reaches `/backdoor`.

These are related but not identical. The successful final snapshot proves the
second claim for the package context. The adaptive result files support the
first claim as a demonstration of feedback-loop behavior, but they are not the
same as a complete multi-phase grader transcript.

Future report standard:

> Separate "what makes it autonomous" from "what makes it exploit successfully."

### 3. Negative evidence is a research contribution, not just a failed attempt

Jason's handoff is valuable because it rules out bad assumptions:

- direct ret-to-maintenance was insufficient;
- `rdi` was stale or wrong;
- stack shellcode was blocked by NX in Phase II;
- broad text sweeps did not find success;
- saved-RBP and C-string constraints blocked simple argument reconstruction;
- heap/global-state staging produced primitives but no final artifact.

This is exactly the kind of evidence that prevents future agents from wasting
time. It should be framed as a rigorous failed branch, not as "nothing was
done."

### 4. Protocol correctness can hide exploit incompleteness

Jason built the EC protocol correctly, and that can feel close to completion
because `/exploit`, `/triage`, config writing, marker creation, and state logs
all work. But the grader's core success predicate is IC-side `/backdoor`
execution.

The project has two layers:

```text
Layer 1: EC protocol compliance
Layer 2: exploit success under the IC binary
```

Jason solved much of Layer 1 and investigated Layer 2. Jingzhong's package
solves both for its package context.

### 5. The teammate success route may imply an untracked lab-version update

Because the server binaries differ, one important unanswered question is:

```text
Where did Jingzhong's server_1/server_2 binaries come from?
```

Possibilities:

- the course lab package was updated after Jason archived `lab.zip`;
- Jingzhong rebuilt from a source file that matched a later intended lab;
- Jingzhong included a modified IC for local demonstration;
- the package is a merged working folder rather than a pristine official
  grading bundle.

This does not change the local archive conclusion, but it matters if the result
must be defended to an instructor or reused as evidence.

Recommended next evidence action, if needed:

- ask or record whether Jingzhong used an updated official lab package;
- preserve the exact submitted LMS file if available;
- preserve a final grader transcript for the submitted package;
- do not claim the earlier `lab.zip` and Jingzhong package are equivalent.

### 6. "Why did I fail?" should be answered as "I solved a different/harder state problem"

A less careful interpretation would be: Jingzhong succeeded and Jason failed,
therefore Jingzhong's exploit skill was simply better.

The evidence does not support that simple reading. The better reading is:

- Jingzhong's package had a semantically convenient helper target.
- Jason's target required solving argument setup under strict constraints.
- Jason did not discover a viable argument-control route for that target.
- The two lines therefore differ in target surface, not only in effort or
  competence.

This distinction matters for your own research confidence. The failure is still
real, but it is technically specific: no full success predicate under the
harder binary.

## What To Say In A Presentation Or Handoff

Short version:

> Project II had two separated work lines. Jason built the local scaffold,
> protocol, and recovery analysis, but his attempt did not produce the IC-side
> success artifact. Jingzhong's package is the successful Project II result. The
> key technical reason is that Jingzhong's package contains a target binary with
> an `execute_task()` helper that calls `maintenance_task(user_input)`, removing
> the first-argument-control blocker that stopped Jason's line.

Longer technical version:

> Jason's route reached the point where protocol behavior and some control-flow
> influence were understood, but the attempt failed because the hijacked path
> did not preserve a controlled first argument to the success-relevant function.
> Jingzhong's successful package instead used a binary where `execute_task()`
> already performs the necessary argument setup from global `user_input`.
> Returning to that helper after staging `/backdoor` in `user_input` was enough
> to trigger the success artifact. This is why the package succeeds while the
> earlier scaffold remains a protocol-complete partial.

Evidence caveat to include:

> The successful package's IC binaries differ from the earlier preserved
> `lab.zip` snapshot, so the success evidence should be tied to Jingzhong's
> package unless the earlier binary is rerun and independently validated.

## Research Lessons To Preserve

1. Version pinning comes before exploit reasoning.
2. A helper function can collapse an exploit from argument-control research to
   ret-to-helper engineering.
3. Control-flow hijack is not enough; exploit success requires correct semantic
   state at the target call.
4. Negative exploit evidence is valuable when it is bounded, reproducible, and
   indexed.
5. Assignment reports should separate agent architecture claims from final
   exploit-success claims.
6. Team attribution should distinguish setup/scaffold/failure-analysis work from
   the artifact that actually satisfied the grading condition.
7. When two teammates' results differ, inspect the binary before judging the
   people.

## Recommended Follow-Up

If this archive may be used for grading defense, submission reconstruction, or a
future write-up, do these in order:

1. Ask Jingzhong where the successful IC binaries came from.
2. Preserve the exact final LMS submission package, if available.
3. Rerun the Jingzhong package in Docker and save a full grader transcript.
4. Keep Jason's failed scaffold as a separate research handoff, not as part of
   the successful submission line.
5. If necessary, rerun the earlier `lab.zip` snapshot separately and mark its
   result independently.

## Final Interpretation

Jingzhong succeeded because his package used a target surface with a direct
semantic bridge from controlled data to the success call. Jason failed because
his line did not find such a bridge in the earlier binary and did not solve the
harder argument-control problem.

The important learning is not "try harder." The important learning is:

> Before deep exploit recovery, verify whether the binary gives you a semantic
> helper. If it does, exploit the helper. If it does not, explicitly name the
> missing state variable and decide whether the remaining problem is worth the
> time budget.
