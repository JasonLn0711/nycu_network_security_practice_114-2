# Project II Next Step Runbook - 2026-05-14

Target: NYCU Network Security Practice Project II / Phase II Medium

This runbook defines the next executable step after the analysis report, SPEC,
and SDD have been created.

## Current Decision

The correct next step is submission-oriented.

Current state:

- Protocol-complete partial package: yes.
- Full-credit IC-side success evidence: no.
- Official `/shared/success.txt` observed from IC-side `/backdoor`: no.
- EC-side fake success file: not allowed and not present.

Therefore, proceed with a partial-submission clarification path unless a new
technical mechanism is identified before the submission gate.

## Track A - Ask TA For Submission Clarification

Goal: confirm what artifact should be submitted while full-credit evidence is
still missing.

Steps:

1. Rebuild the current source package:

   ```sh
   ./scripts/run_static_checks.sh
   ./scripts/generate_readiness_report.sh
   ./scripts/build_submission_package.sh
   ```

2. Inspect the newest archive under `dist/`.

3. Send or adapt:

   ```text
   docs/TA_CLARIFICATION_DRAFT.md
   ```

4. Ask three concrete questions:

   - whether a protocol-complete partial EC package may be uploaded before
     official IC-side `/shared/success.txt` evidence exists;
   - whether the TA wants source/build context, a prebuilt Docker image, or
     both;
   - whether the audit and negative validation notes should be included in the
     official upload.

5. Record the TA answer in a new dated note if the answer affects submission.

Acceptance check:

- A TA answer, LMS instruction, or course announcement resolves the upload
  route.

## Track B - Submit Protocol-Complete Partial Package

Use this track only if full-credit success is still missing and the TA permits
or does not prohibit a partial package.

Package posture:

```text
This is a runnable Project II Phase II EC package with the required /exploit
and /triage entry points, shared-volume protocol, state/logging loop,
readiness checks, and documented Phase II validation attempts. The remaining
gap is official IC-side /shared/success.txt evidence.
```

Before upload:

1. Confirm the package contains source and docs, not runtime leftovers:

   ```sh
   ./scripts/build_submission_package.sh
   ```

2. Confirm the zip excludes generated state:

   - no `mock_shared/`;
   - no `dist/`;
   - no `__pycache__/`;
   - no coredumps.

3. Review:

   ```text
   docs/PARTIAL_SUBMISSION_BRIEF.md
   docs/PROJECT_II_ANALYSIS_REPORT_2026-05-14.md
   docs/SUBMISSION_SPEC.md
   docs/SUBMISSION_SDD.md
   docs/REQUIREMENTS_TRACEABILITY.md
   ```

4. Upload the newest zip from `dist/` if that is the required route.

5. Save the LMS receipt or upload confirmation outside the submission zip.

Acceptance check:

- The uploaded package is the newest generated source zip.
- The upload text does not claim full-credit success.

## Track C - Build Docker Image If Requested

Use this only if the TA or grader asks for a prebuilt image.

Steps:

```sh
./scripts/run_static_checks.sh
./scripts/generate_readiness_report.sh
./scripts/build_submission_image.sh
```

Expected output:

```text
dist/project2-agent-submission-image-phase2.tar.gz
```

The image must expose:

```text
/exploit
/triage
```

Acceptance check:

- The image loads with `docker load`.
- The image still does not create `/shared/success.txt` from EC code.

## Track D - Continue Full-Credit Recovery Only With A New Mechanism

Do not restart blind candidate probing.

Before any new technical attempt:

1. Re-check live IC state:

   ```sh
   docker ps
   ```

2. Confirm ASLR and live process state inside the IC container.

3. Confirm `/shared/success.txt` does not already exist.

4. Read the existing negative evidence:

   ```text
   docs/PHASE2_EXPERIMENT_LOG.md
   docs/PHASE2_SUCCESS_VALIDATION.md
   docs/PHASE2_COMPLETION_ATTEMPT_2026-05-14.md
   docs/PHASE2_ARGUMENT_CONTROL_ATTEMPT_2026-05-14.md
   docs/PHASE2_STAGING_BOUNDARY_ATTEMPT_2026-05-14.md
   docs/PHASE2_HEAP_GLOBAL_STATE_ATTEMPT_2026-05-14.md
   docs/PHASE2_MULTILINE_STAGING_ATTEMPT_2026-05-15.md
   docs/PHASE2_REGISTER_REUSE_ATTEMPT_2026-05-15.md
   docs/PHASE2_BACKWARD_PIVOT_FEASIBILITY_2026-05-15.md
   docs/PHASE2_CURRENT_RDI_ARGUMENT_ATTEMPT_2026-05-15.md
   ```

5. Pick exactly one bounded investigation track:

   - argument-control track;
   - pivot track;
   - libc/libstdc++ call-path track.

6. Write the hypothesis before running code. It must explain:

   - what existing blocker it avoids;
   - what observable result would prove progress;
   - what result would falsify the hypothesis;
   - why it does not require EC-side `/shared/success.txt` creation.

7. Run one bounded validation block.

8. Stop after one falsifiable result and record it in both places:

   - a dated attempt note when the evidence is non-trivial;
   - `docs/PHASE2_EXPERIMENT_LOG.md` as the canonical ledger entry.

The ledger entry is mandatory even for a failed static feasibility check, a
no-coredump/no-success run, or a positive primitive that still does not produce
`/shared/success.txt`.

Required stop conditions:

- IC-side `/shared/success.txt` appears;
- a coredump/register artifact proves the hypothesis wrong;
- the attempt repeats a previously closed path;
- the candidate requires EC-side fake success, host tampering, or manual
  `/backdoor` invocation.

Acceptance check for full-credit recovery:

- Official IC-side `/backdoor` creates `/shared/success.txt`.
- The evidence is recorded before any completion claim is made.

## Evidence To Preserve

Keep these artifacts or notes outside generated runtime directories unless the
instructor requests otherwise:

| Evidence | Why it matters |
| --- | --- |
| Latest source zip path | Identifies the exact submitted package. |
| `mock_shared/readiness_report.json` | Shows protocol-readiness gate result. |
| Static-check output | Confirms wrapper/docs/import sanity. |
| Package inspection output | Confirms generated state is excluded. |
| TA answer | Determines source zip vs Docker image vs both. |
| IC-side `/shared/success.txt`, if produced | Only valid full-credit success evidence. |
| `docs/PHASE2_EXPERIMENT_LOG.md` | Canonical record of every Phase II experiment, success or failure. |

## Immediate Work Block

Use this 60-120 minute order:

1. Re-run readiness and packaging.
2. Inspect the new zip.
3. Send the TA clarification draft or prepare the LMS upload text.
4. If no TA response is available before the gate, submit only with the honest
   protocol-complete partial wording.
5. Continue full-credit technical research only if a new, written hypothesis
   passes the Track D gate.

## Non-Goals

Do not spend the next block on:

- broad blind sweeps;
- re-testing direct ret-to-maintenance as if untested;
- manual `/backdoor` invocation;
- EC-side `/shared/success.txt` creation;
- adding general exploit guidance to the docs.
