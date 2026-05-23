# Project II Ownership And Outcome

Date: 2026-05-23

Purpose: separate the two Project II work lines so future readers do not mix
Jason's unsuccessful local attempt with Chen Jingzhong's successful package.

Detailed postdoctoral-style comparison: `PROJECT_II_COMPARATIVE_ANALYSIS.md`.

## Direct Verdict

FIRST PRINCIPLE: a course archive should preserve what actually satisfied the
success condition, who produced it, and which binary/package context created
the evidence. Do not collapse a failed local investigation and a successful
teammate package into one vague "we solved it" story.

Project II should now be read as two distinct parts:

| Work line | Owner | Canonical files | Outcome |
| --- | --- | --- | --- |
| Jason / local recovery attempt | Jason Lin | `project2-agent-scaffold/`, `../../HANDOFF_PHASE2.md`, scaffold docs | Did not meet the full assignment success gate. The official local Phase II loop did not produce `/shared/success.txt`. |
| Jingzhong successful package | Chen Jingzhong | `submissions/jingzhong-success/` | Successful package provided by Jingzhong. The archived report and lab evidence show `/exploit`, `/triage`, target analysis, adaptive probing, and a `success.txt` artifact. |

Team context: Project I was completed by Jason for the same two-person group.
Project II's successful completion package should be attributed to Chen
Jingzhong. Jason's Project II experiments remain useful as a failure/recovery
record, not as the successful result.

## Important Evidence Boundary

Do not overwrite or reinterpret the preserved official bundle:

- official repo snapshot: `lab.zip`
- Jingzhong package: `submissions/jingzhong-success/lab-jingzhong-success-2026-05-23.rar`

The extracted Jingzhong package contains IC server binaries that differ from the
repo's earlier `lab.zip` snapshot. That may mean Jingzhong used a newer lab
package, a locally rebuilt IC, or a modified copy. The correct archive policy is
therefore:

1. Keep `lab.zip` as the preserved official/local source snapshot already in
   this repo.
2. Keep Jingzhong's full successful package separately under
   `submissions/jingzhong-success/`.
3. Attribute success to Jingzhong's package, not to Jason's earlier
   `project2-agent-scaffold/`.
4. If a future report needs to claim success against the original `lab.zip`
   snapshot, rerun and verify that exact environment instead of inferring it
   from this package.

Observed binary differences:

| Item | Earlier `lab.zip` snapshot | Jingzhong success package |
| --- | --- | --- |
| `IC/server_1` SHA-256 | `5fbcb18762083b220d2c21f7cdbeacb359c2dd910f52c375de11f17b57dbb7cf` | `e3a7bd6957d6680982149239f86115f97ec0ea070fbf2f2821400b6002d866d1` |
| `IC/server_2` SHA-256 | `155fee01eb0e2a88e9f19738b7bd92bd25306a387247047ca525a2ff7cf8304c` | `465d7fd6058c6fa4aeddaa05d560ef548bc132cfd675d2d0aadad4b82c6c724b` |
| `execute_task()` symbol | Absent | Present at `0x401415` |
| `user_input_len` symbol | Absent | Present at `0x404540` |
| `log_message` shape | `log_message(char const*)` | `log_message(char const*, unsigned long)` |

This does not invalidate Jingzhong's work. It means the success evidence should
be cited with its exact package and binary context.

For the technical reason this matters, see
`PROJECT_II_COMPARATIVE_ANALYSIS.md`: the successful package has an
`execute_task()` helper that removes the first-argument-control problem that
blocked Jason's earlier line.

## Jason Work Line - Not Successful

Canonical area:

- `project2-agent-scaffold/`
- `project2-agent-scaffold/docs/PHASE2_SUCCESS_VALIDATION.md`
- `project2-agent-scaffold/docs/COMPLETION_AUDIT.md`
- `project2-agent-scaffold/docs/PHASE2_EXPERIMENT_LOG.md`
- `../../HANDOFF_PHASE2.md`

What Jason completed:

- archived the official Project II brief and `lab.zip`;
- wrote local SPEC/SDD/checklists/rubric/safety-boundary docs;
- built a classroom-safe EC scaffold with executable `/exploit` and `/triage`;
- implemented shared-volume protocol behavior, state handling, logs, and
  package/readiness checks;
- ran and documented multiple bounded Phase II recovery attempts;
- preserved detailed failure evidence so a future agent would not repeat the
  same dead ends.

What Jason did not complete:

- no validated candidate caused the official local IC Phase II flow to create
  `/shared/success.txt`;
- no final official grader transcript or timing score was produced from the
  Jason scaffold;
- the local scaffold is therefore a protocol-complete partial, not the
  successful Project II deliverable.

Short attribution sentence:

> Jason contributed Project II setup, specification, scaffold, and failed
> recovery analysis. Jason's own Project II exploit result did not satisfy the
> success requirement.

## Jingzhong Work Line - Successful Package

Canonical area:

- `submissions/jingzhong-success/`
- `submissions/jingzhong-success/lab/`
- `submissions/jingzhong-success/report/autonomous-apt-agent-report-jingzhong-success-2026-05-23.docx`
- `submissions/jingzhong-success/report/autonomous-apt-agent-report-extracted-text.txt`

Incoming files moved into this repo:

| Original file | New path |
| --- | --- |
| `/Users/iKev/Downloads/lab.rar` | `submissions/jingzhong-success/lab-jingzhong-success-2026-05-23.rar` |
| `/Users/iKev/Downloads/Autonomous_APT_Agent_Report.docx` | `submissions/jingzhong-success/report/autonomous-apt-agent-report-jingzhong-success-2026-05-23.docx` |

Jingzhong package contents:

- `lab/EC/Dockerfile`
- `lab/EC/analyze_target.py`
- `lab/EC/exploit`
- `lab/EC/triage`
- `lab/README.md`
- `lab/phase2_adaptive_result.txt`
- `lab/phase3_adaptive_result.txt`
- `lab/shared/config.data`
- `lab/shared/success.txt`
- `lab/shared/exploit-log.txt`
- `lab/shared/state.json`
- `lab/shared/target-analysis-log.txt`
- `lab/shared/target_info.json`

Core implementation idea:

1. `/exploit` runs `/analyze_target.py`.
2. The analyzer reads `/shared/blogic.copy` or `/shared/blogic`.
3. It extracts ELF metadata, PIE/NX status, symbols, interesting strings,
   risky imports, candidate target functions, and `ret` gadgets.
4. `/exploit` selects `execute_task()` and a preferred `ret` gadget from
   `target_info.json`.
5. `/exploit` writes `/shared/config.data` and creates
   `/shared/exploit_done`.
6. `/triage` observes `success.txt`, coredumps, or no-success feedback and
   updates `/shared/state.json`.

Successful evidence in the archived package:

- `lab/shared/success.txt` contains:

```text
Backdoor triggered
Fri May 22 16:50:15 UTC 2026
```

- `lab/shared/exploit-log.txt` records final mode selecting:
  - `execute_task = 0x401415`
  - `ret_gadget = 0x401414`
  - `offset_to_ret = 104`
  - mode `final_exploit`
  - payload length `120` bytes
  - creation of `/shared/exploit_done`
- `lab/shared/config.data` contains a `user_input=` payload beginning with
  `/backdoor\x00`, padded to the saved return address, followed by the selected
  `ret` gadget and `execute_task` addresses.
- `lab/shared/target_info.json` records a non-PIE ELF target, discovered
  `execute_task`, discovered `user_input`, discovered `user_input_len`, and the
  preferred `ret` gadget.
- The Word report states that fast mode succeeds in Phase I/II/III and that
  adaptive offset probing reaches the working offset within the 60-round limit.

Evidence caveat:

- The current `lab/shared/` snapshot is a final successful run against
  `server_1` / `shared/blogic` with executable stack metadata.
- `phase2_adaptive_result.txt` and `phase3_adaptive_result.txt` preserve
  adaptive-mode state up through the step that advances from offset `96` to
  offset `104`; they do not themselves include a full final grader transcript.
- The Word report provides the broader narrative claim for Phase I/II/III fast
  mode and adaptive behavior. The package gives strong local evidence, but a
  future verifier should rerun Docker if the exact grading transcript is needed.

Short attribution sentence:

> Chen Jingzhong completed the successful Project II package, including the
> runnable EC agent, report, and success evidence. This is the part that met the
> assignment result.

## Report Summary

The report title is `Autonomous APT Agent 系統功能展示與特色說明報告`.

Named authors in the report:

- `313264012 陳靖中`
- `513559004 林家聖`

Report claims and matching package evidence:

| Claim area | Evidence in package | Assessment |
| --- | --- | --- |
| `/exploit` exists and writes config | `lab/EC/exploit`, `lab/shared/config.data`, `lab/shared/exploit-log.txt` | Supported. |
| `/triage` exists and updates state | `lab/EC/triage`, phase adaptive result files | Supported for adaptive feedback. |
| Target analysis | `lab/EC/analyze_target.py`, `target_info.json`, `target-analysis-log.txt` | Supported. |
| Fast mode | `lab/shared/exploit-log.txt`, `success.txt`, report text | Supported for the archived final snapshot; rerun needed for full multi-phase transcript. |
| Adaptive probing | `phase2_adaptive_result.txt`, `phase3_adaptive_result.txt`, report text | Supported as a feedback-loop demonstration; result files capture the move to offset `104`. |
| Safety boundary | EC code uses `/shared` and analyzer targets only | Supported by code review; no external network behavior observed in static review. |

## Presentation / Handoff Wording

Use this wording when the two parts need to be explained honestly:

> Project II has two separated work lines. Jason's line built the local
> scaffold, audit trail, and failed Phase II recovery attempts, but did not meet
> the `/shared/success.txt` success gate. Chen Jingzhong's line is the
> successful submitted package: it contains the EC agent, `/exploit`, `/triage`,
> report, target-analysis outputs, and success evidence. The successful Project
> II result should therefore be attributed to Jingzhong.
