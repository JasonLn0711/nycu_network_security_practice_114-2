# Project II Submission Action Packet - 2026-05-14

Target: NYCU Network Security Practice Project II / Phase II Medium

This packet is the next operational artifact after the analysis report, SPEC,
SDD, partial-submission brief, TA clarification draft, and next-step runbook.

## Executive Decision

Proceed with the TA clarification / protocol-complete partial submission path.

Current status:

- EC protocol package: ready.
- Submission-facing documentation: ready.
- Full-credit IC-side success proof: not ready.
- Official `/shared/success.txt` from IC-side `/backdoor`: not observed.

Therefore, do not claim full Phase II completion. The current defensible
posture is:

```text
Protocol-complete partial package; official IC-side success evidence pending.
```

## FIRST PRINCIPLE Routing

Scarce resource: trustable proof and deadline-safe submission clarity.

Canonical ownership:

| Layer | Owns |
| --- | --- |
| Course repo | EC code, Docker build context, validation evidence, SPEC, SDD, runbook, package. |
| Planning repo | Status, deadline pressure, next gate, capacity boundary, locators. |
| TA / instructor | Final upload format and grading posture. |

Decision rule:

- If official IC-side `/shared/success.txt` appears, update completion evidence
  before claiming full success.
- If it does not appear before the gate, submit or ask using the
  protocol-complete partial wording.
- Do not make the EC create `/shared/success.txt`.

## Package To Use

Build a fresh source package from this directory:

```sh
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
./scripts/build_submission_package.sh
```

Use the newest zip under:

```text
dist/
```

The package must include:

- `Dockerfile`
- `exploit`
- `triage`
- `src/`
- `scripts/`
- `docs/`
- `README.md`

The package must exclude:

- `mock_shared/`
- `dist/`
- `__pycache__/`
- `.pytest_cache/`
- coredumps
- local Docker layers

## Upload / Message Text

Use this wording if submitting before full-credit evidence is available:

```text
This submission provides a runnable Project II Phase II EC package. It
implements the required /exploit and /triage entry points, shared-volume
config.data writing, exploit_done signaling, triage state, JSONL logs,
readiness checks, and documented Phase II validation attempts.

Current honest status: protocol-complete partial. The remaining validation
gap is official IC-side /shared/success.txt evidence. The EC does not create
/shared/success.txt directly.
```

Use this shorter status if the LMS textbox is tight:

```text
Protocol-complete partial EC package. /exploit, /triage, shared-volume
protocol, readiness report, and validation notes are included. Official
IC-side /shared/success.txt evidence is still pending; EC does not fabricate
success.
```

## TA Clarification Message

Send or adapt this if asking before upload:

```text
Hi TA,

I am preparing my Project II Phase II external-container submission. The EC
currently has the required /exploit and /triage entry points, writes
/shared/config.data, creates /shared/exploit_done, records JSON/JSONL state
and logs, and runs without external network dependency.

I want to clarify the expected grading posture if I submit a protocol-complete
partial package before I can produce official IC-side /shared/success.txt.

Current honest status:
- EC protocol and packaging are ready.
- /triage feedback handling and readiness reports are implemented.
- Several bounded Phase II validation attempts are documented.
- I have not observed official IC-side /shared/success.txt yet.
- The EC does not create /shared/success.txt directly.

Questions:
1. If official IC-side success is not reached before the gate, should I still
   submit the runnable EC package with the audit notes?
2. Do you prefer source/build context, a Docker image tarball, or both?
3. For grading, should I include the validation/audit notes, or keep the upload
   limited to the EC build context?

Thank you.
```

## If TA Answers

| TA answer | Action |
| --- | --- |
| Source/build context only | Upload the newest `dist/project2-agent-scaffold-*.zip`. |
| Docker image required | Run `./scripts/build_submission_image.sh` and upload the image tarball if allowed. |
| Source and image required | Upload both the source zip and image tarball; mention matching build date. |
| Audit notes should be excluded | Upload only build context if requested, but keep audit notes locally. |
| Partial package not acceptable | Continue only one bounded full-credit recovery block at a time; do not claim success. |
| TA gives a different official route | Follow the TA route and record the answer in a dated note. |

## Final Upload Checklist

Run from `project2-agent-scaffold/`:

```sh
git diff --check
./scripts/run_static_checks.sh
python3 -m compileall -q src
./scripts/generate_readiness_report.sh
./scripts/build_submission_package.sh
```

Then inspect the newest zip:

```sh
python3 - <<'PY'
from pathlib import Path
from zipfile import ZipFile

zip_path = max(Path("dist").glob("project2-agent-scaffold-*.zip"))
required = {
    "project2-agent-scaffold/Dockerfile",
    "project2-agent-scaffold/exploit",
    "project2-agent-scaffold/triage",
    "project2-agent-scaffold/docs/PROJECT_II_SUBMISSION_ACTION_PACKET_2026-05-14.md",
    "project2-agent-scaffold/docs/PARTIAL_SUBMISSION_BRIEF.md",
    "project2-agent-scaffold/docs/TA_CLARIFICATION_DRAFT.md",
}
with ZipFile(zip_path) as archive:
    names = set(archive.namelist())
missing = sorted(required - names)
forbidden = sorted(
    name for name in names
    if "/mock_shared/" in name or "/dist/" in name or "__pycache__/" in name
)
print(f"zip={zip_path}")
print(f"missing={missing}")
print(f"forbidden_count={len(forbidden)}")
PY
```

Acceptance check:

- `missing=[]`
- `forbidden_count=0`
- upload text does not claim full-credit completion

## Evidence To Keep After Upload

Keep these outside the upload zip unless the TA asks for them:

- LMS receipt or upload screenshot;
- generated `mock_shared/readiness_report.json`;
- exact package filename;
- TA answer, if any;
- official IC-side `/shared/success.txt`, if it appears later.

## Full-Credit Recovery Gate

Continue technical work only if a new written hypothesis passes this gate:

1. It avoids the already documented blockers.
2. It has one observable success or failure signal.
3. It does not require EC-side fake success.
4. It can be tested in one bounded block.

Already documented blockers:

- direct ret-to-maintenance did not produce success;
- direct stack shellcode is blocked by NX;
- broad `.text` one-shot sweep found no success;
- saved-RBP maintenance-body entry is blocked by C-string/NUL-byte constraints;
- caller-stack staging is fixed, not attacker-controlled;
- direct heap/global-state adjacency crashes before useful success state.

Stop technical work immediately if a proposed path requires:

- manual `/backdoor` invocation;
- EC-side `/shared/success.txt` creation;
- host or grader tampering;
- broad blind sweeps without a written hypothesis.

## Current Next Action

1. Rebuild package.
2. Confirm the zip includes this packet.
3. Send TA clarification or submit with protocol-complete partial wording.
4. Record TA response or upload receipt in the planning layer.
5. Keep full-credit recovery separate from submission honesty.
