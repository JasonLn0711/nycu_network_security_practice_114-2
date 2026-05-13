# Project II Requirements Traceability Matrix

Date: 2026-05-13
Target: Project II - Autonomous APT Agent, Phase II / Medium

This matrix checks the submission against the official brief and the local rubric.
It separates **implemented**, **verified**, and **remaining risk** so the final
package is honest and auditable.

## Official Requirement Coverage

| Brief requirement | Evidence in this repo | Current status | Verification command / note |
| --- | --- | --- | --- |
| Student prepares the external container (EC). | `Dockerfile` in this directory. | Implemented | `docker build -t project2-agent-scaffold-readiness .` passed locally. |
| `/exploit` exists at container root. | Dockerfile creates `ln -sf ... /exploit`; wrapper file `exploit`. | Implemented | `scripts/run_static_checks.sh` checks wrapper. |
| `/triage` exists at container root. | Dockerfile creates `ln -sf ... /triage`; wrapper file `triage`. | Implemented | `scripts/run_static_checks.sh` checks wrapper. |
| `/exploit` modifies `/shared/config.data`. | `src/exploit_runner.py` atomic byte writer. | Implemented | Mock readiness and real shared smoke test changed config hash/content. |
| `/exploit` creates `/shared/exploit_done`. | `src/exploit_runner.py`. | Implemented | Mock readiness and real shared smoke test. |
| Uses shared volume `/shared`. | `src/path_config.py`; override via `PROJECT2_SHARED_DIR` for tests. | Implemented | Static checks and mock grader. |
| Can examine `blogic.copy`. | `resolve_blogic_path()` accepts `blogic.copy` and supplied-lab `blogic`. | Implemented | Real lab metadata smoke test found `/shared/blogic`. |
| `/triage` reads coredump feedback. | `src/coredump_scanner.py`, `src/coredump_analyzer.py`, `src/triage_runner.py`. | Implemented | Mock grader creates fake coredumps and state updates. |
| Phase II Medium target: non-PIE, ASLR disabled, NX stack. | `src/phase2_payload.py` uses non-PIE partial text-address probe; Docker image enables probe mode. | Partially implemented | Control-flow probe written; IC-side `/backdoor` success not yet observed. |
| Score depends on time to execute `/backdoor`. | `docs/COMPLETION_AUDIT.md` records that final success is not observed yet. | Remaining gap | Need official IC `/shared/success.txt` evidence. |
| No external network runtime dependency. | Python-only local code; no network calls. | Implemented | Readiness report scans for obvious runtime network tokens. |
| No grader bypass / fake success. | Code does not write `/shared/success.txt`; docs forbid doing so. | Implemented | Reviewed `src/`; only IC-side `/backdoor` should create success. |

## Current Honest Grade-Risk Summary

- Strong coverage: container interface, `/exploit` and `/triage` protocol,
  state/logging, controlled-lab path handling, buildability, documentation.
- Main grade risk: the current Phase II probe has **not** produced IC-side
  `/shared/success.txt`, so full C-section success points are not yet earned.
- The package is therefore a high-quality partial implementation unless the
  final Phase II candidate is completed and validated before submission.

## Commands Used For Current Verification

```sh
python3 -m compileall -q src
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
docker build -t project2-agent-scaffold-readiness .
git diff --check
```

## Required Before Claiming Full Completion

1. Run the EC image with the official Phase II IC.
2. Confirm that `/shared/success.txt` is created by IC-side `/backdoor`.
3. Save the grader log and `mock_shared/readiness_report.json` or equivalent
   real-run report.
4. Re-run this traceability matrix and update the remaining gap to complete.
