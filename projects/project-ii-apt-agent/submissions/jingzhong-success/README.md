# Jingzhong Successful Project II Package

Date archived: 2026-05-23

Owner: Chen Jingzhong

Outcome: successful Project II package provided by Jingzhong. This is separate
from Jason's earlier unsuccessful `project2-agent-scaffold/` work line.

## Files

| Path | Role |
| --- | --- |
| `lab-jingzhong-success-2026-05-23.rar` | Raw incoming RAR archive, moved from Downloads. |
| `lab/` | Extracted lab package from the RAR. |
| `lab/EC/` | External-container implementation with Dockerfile, analyzer, `/exploit`, and `/triage`. |
| `lab/IC/` | IC files included in Jingzhong's package. These differ from the earlier repo `lab.zip` snapshot. |
| `lab/shared/` | Saved run artifacts including `config.data`, `success.txt`, tracked log-text copies, state, and target analysis. |
| `report/autonomous-apt-agent-report-jingzhong-success-2026-05-23.docx` | Original Word report. |
| `report/autonomous-apt-agent-report-extracted-text.txt` | Searchable text extraction of the Word report. |
| `report/extracted-media/` | Four embedded report images extracted from the Word package. |
| `artifact-manifest.md` | File inventory, checksums, and evidence notes. |

## Success Evidence

`lab/shared/success.txt` records:

```text
Backdoor triggered
Fri May 22 16:50:15 UTC 2026
```

`lab/shared/exploit-log.txt` records a final exploit run using:

- `execute_task = 0x401415`
- `ret_gadget = 0x401414`
- `offset_to_ret = 104`
- mode `final_exploit`

The report also describes adaptive offset probing, where the agent advances
through candidates and reaches offset `104` within the 60-round limit.

## Review Boundary

This package's IC server binaries differ from the repo's earlier preserved
`lab.zip` snapshot. Treat this as Jingzhong's successful package and preserve
the earlier `lab.zip` separately. To prove the same result against the earlier
snapshot, rerun that exact environment and save a new validation log.
