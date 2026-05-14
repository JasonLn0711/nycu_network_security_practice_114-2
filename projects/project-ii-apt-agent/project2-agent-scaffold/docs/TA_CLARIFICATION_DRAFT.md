# Project II TA Clarification Draft

Purpose: send or adapt this message if Project II reaches the presentation or
submission gate before official Phase II `/shared/success.txt` evidence is
available.

## Short Message

```text
Hi TA,

I am preparing my Project II Phase II external-container submission. The EC
currently has the required /exploit and /triage entry points, writes
/shared/config.data, creates /shared/exploit_done, records JSON/JSONL state and
logs, and runs without external network dependency.

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

## Evidence To Mention If Asked

Use high-level evidence only:

- protocol-ready EC build context;
- `/exploit` and `/triage` wrappers;
- readiness report from `scripts/generate_readiness_report.sh`;
- completion audit in `docs/COMPLETION_AUDIT.md`;
- success-validation log in `docs/PHASE2_SUCCESS_VALIDATION.md`;
- no EC-side fake success file.

Do not include payload recipes, shellcode, ROP chains, or instructions for any
system outside the controlled course lab.
