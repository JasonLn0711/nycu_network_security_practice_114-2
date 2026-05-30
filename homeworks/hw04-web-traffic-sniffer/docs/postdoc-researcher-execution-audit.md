# HW04 Postdoc Researcher Execution Audit

This audit adds a postdoctoral researcher perspective to the HW4 Web Traffic
Sniffer implementation. The homework is already executable and packaged; this
document identifies the remaining high-value controls that make the submission
more defensible, reproducible, and technically mature without exceeding the
official assignment scope.

## Research Framing

Treat the assignment as a small controlled measurement study:

> A browser extension with explicit permission observes ad-tech request payloads
> during a bounded Cambridge Dictionary browsing session. The experiment
> measures what categories of third-party advertising endpoints receive browser
> request data and explains the privacy implications through browser
> architecture.

This framing matters because it keeps the work affirmative and scoped:

- The system demonstrates request observation through a browser-granted
  extension API.
- The evidence is controlled, redacted, and reproducible.
- The privacy analysis is grounded in observed request structure, not broad
  speculation.
- The report separates transport security, CSP, extension permissions, and
  user-governance controls.

## Must-Execute Controls Before Upload

| Control | Why it matters | Concrete action | Evidence |
| --- | --- | --- | --- |
| Re-run final capture once after browser restart | Confirms the evidence is not a one-off service-worker artifact | Close Chromium/Edge, run `scripts/launch-clean-profile.sh`, then run `scripts/capture_sanitized_evidence.js https://dictionary.cambridge.org/` | Updated `evidence/screenshots/sanitized-console-evidence.png` |
| Verify `DEBUG_MODE = false` in the submitted file | Prevents discovery-mode noise from reaching the grader | Search `solution/Extension/background.js` before final ZIP | `const DEBUG_MODE = false;` |
| Compare final ZIP files against official structure | Avoids losing points for packaging | Run `python3 scripts/validate_submission.py --student-id 513559004 --package-dir submission/final/HW6_513559004 --zip submission/final/HW6_513559004.zip` | `OK: submission dry-run package passed structural checks.` |
| Review report PDF visually | Ensures the screenshot is visible and no local file path/header leaked | Open `report/513559004_report.pdf`; confirm 4 pages render and Q1-Q6 are readable | `pdfinfo`, visual check |
| Check raw evidence is ignored | Prevents accidental disclosure | Run `git status --short --ignored -- evidence submission` and `git check-ignore -v evidence/raw-local/...` | ignored `raw-local/` and ZIPs |
| Confirm assignment naming discrepancy at upload | The PDF says `HW6_{student_ID}` while platform says HW4 | Preserve `HW6_513559004.zip`; if E3 rejects name, create a platform-named copy without changing contents | `submission/README.md` note |
| Generate artifact manifest | Gives the submission a reproducible provenance record without storing raw data | Run `python3 scripts/generate_artifact_manifest.py` | `docs/artifact-manifest.json` |

## Technical Details Worth Adding To The Report If Space Allows

### 1. Measurement Window

State the capture window:

- target: Cambridge Dictionary homepage or dictionary page;
- browser profile: clean profile;
- extension mode: normal;
- capture duration: around 25 seconds;
- evidence type: sanitized service-worker console output.

Why: it makes the experiment reproducible and prevents the grader from reading
the evidence as an uncontrolled browsing dump.

### 2. Why Query Parameters Count As Payload Evidence

The official spec asks for request payloads and decoded readable data. Some
ad-tech endpoints send useful data through query parameters rather than raw
request bodies. The implementation therefore treats "payload evidence" as:

- request body;
- form data;
- query parameters.

This is technically defensible because the privacy-relevant data still leaves
the browser as part of the HTTP request. The report should phrase it as
"payload evidence" or "request data" when the request body itself is empty.

### 3. Decoder Failure Mode

Add one sentence that malformed or opaque payloads are preserved as readable raw
strings. This demonstrates engineering maturity: the decoder does not silently
drop non-JSON traffic.

### 4. Ad-Tech Domain Drift

Live advertising stacks change by region, time, consent state, auction path, and
browser profile. The implementation handles this with:

- normal mode for final evidence;
- debug mode for candidate discovery;
- allowlist expansion only after clean-profile observation.

This explains why the code includes more than Amazon and Criteo while still
honoring the assignment examples.

### 5. Browser Permission Boundary

For HTTPS and CSP questions, keep the model precise:

- HTTPS: protects transport, not browser-internal extension visibility.
- CSP: governs page execution/loading, not all browser-extension API activity.
- Extension risk: comes from user/browser-granted permission and privileged
  observation surfaces.

This avoids overclaiming that HTTPS or CSP is "broken."

## Extra Implementation Hardening

These are not required for the grade, but they improve quality.

### Add A Small Header Comment In `background.js`

Recommended comment:

```js
// HW4 controlled evidence capture:
// normal mode logs only ad-tech allowlist requests with payload evidence;
// debug mode is for candidate-domain discovery and should be off for submission.
```

Why: the grader sees intent immediately.

### Add Allowlist Rationale Comments

Group hosts:

- official examples;
- observed/common ad-tech families;
- sync/bid endpoints.

Why: prevents the allowlist from looking arbitrary.

### Add Artifact Hashes

Generate a sanitized manifest of key artifact hashes:

```bash
python3 scripts/generate_artifact_manifest.py
```

Why: the manifest records exact final artifact sizes and SHA-256 hashes for the
report, submission ZIP, sanitized evidence, official PDF, and extension files.
It supports provenance without exposing raw browser evidence.

### Add A Negative Control Note

When time allows, briefly run the extension on `about:blank` or a local static
page and note that no advertiser payloads appear. This is not required by the
assignment, but it strengthens the filtering claim because it shows the sniffer
does not produce ad-tech evidence without a relevant browsing scenario.

### Add Redaction Reminder To Evidence HTML

The generated screenshot already states that values are redacted. Keep this in
the final evidence because it signals privacy-aware handling.

### Keep Raw Evidence Local

Do not commit:

- DevTools raw screenshots;
- HAR files;
- browser profile directories;
- unredacted JSON;
- local runtime summaries.

Only commit:

- `sanitized-console-evidence.png`;
- `sanitized-console-evidence.md`;
- report PDF;
- implementation files.

## Potential Weaknesses And How To Defend Them

| Weakness | Defense |
| --- | --- |
| Some screenshots show query payloads rather than raw request body | The extension also captured a JSON body from Amazon; query parameters are clearly labeled as request data and still privacy-relevant. |
| Evidence was captured with Playwright Chromium fallback, not Microsoft Edge | The implementation uses Manifest V3 and `webRequest` APIs compatible with Edge; final upload can mention the official evaluator is Edge, while local automated capture used Chromium for reproducibility. If possible, run one manual Edge capture before upload. |
| Ad-tech domains may differ when the grader tests | Debug mode and allowlist expansion plan address domain drift; report cites observed domains rather than assuming fixed endpoints. |
| Values are redacted, so grader cannot see exact identifiers | The assignment requires readable payload analysis, not disclosure of personal identifiers. Field names, data types, domains, and structure remain visible. |
| `HW6_513559004` folder name conflicts with HW4 assignment title | The final package follows the official PDF structure and documents the mismatch. |
| Single capture window may be affected by auction randomness | The report frames the capture as a bounded measurement window and the code supports reruns through `runtime_smoke.js` and `capture_sanitized_evidence.js`. |
| Consent banner state can affect ad requests | Use the clean profile protocol and record the capture context; avoid mixing daily profile cookies or prior consent state into evidence. |
| Service-worker lifetime can interrupt capture | The runtime smoke test checks that the background worker target exists before evidence capture. |

## Final Pre-Upload Protocol

Run from `homeworks/hw04-web-traffic-sniffer/`:

```bash
node --check solution/Extension/background.js
node scripts/test_extension_logic.js
python3 -m json.tool solution/Extension/manifest.json >/tmp/hw4-manifest-final.json
python3 scripts/validate_submission.py \
  --student-id 513559004 \
  --package-dir submission/final/HW6_513559004 \
  --zip submission/final/HW6_513559004.zip
unzip -l submission/final/HW6_513559004.zip
pdfinfo report/513559004_report.pdf
python3 scripts/generate_artifact_manifest.py
git status --short --ignored -- evidence submission
```

Pass conditions:

- JavaScript syntax passes.
- Extension logic tests pass.
- Manifest JSON parses.
- ZIP contains exactly the required folder and files.
- PDF is readable.
- Artifact manifest is regenerated after the final ZIP/PDF changes.
- Raw local evidence and ZIPs are ignored.
- No unredacted evidence is staged.

## Recommended Final Human Review

Before E3 upload, inspect three things manually:

1. Open the final PDF and confirm the screenshot is legible.
2. Open the ZIP and confirm the grader will immediately see `Extension/` and
   `513559004_report.pdf`.
3. Confirm the E3 upload form accepts `HW6_513559004.zip`; if it requests HW4
   naming, create a copy named `HW4_513559004.zip` with the same internal
   structure only after confirming the platform expectation.

## Researcher-Level Completion Standard

The work is strong when a reviewer can answer these questions from the repo
alone:

- What was measured?
- In what browser/profile context?
- Which extension API observed the traffic?
- What filtering rule made the evidence relevant?
- How were non-JSON payloads handled?
- Which advertiser families were observed?
- What data was redacted and why?
- What does the evidence imply about HTTPS, CSP, and extension permissions?
- What exactly is being submitted?
- Which exact file hashes define the final artifacts?

The current implementation already covers these points; the remaining value is
careful final human review before upload.
