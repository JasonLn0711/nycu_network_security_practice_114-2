# HW04 Web Traffic Sniffer Work Plan

This plan turns the official HW4 Web Traffic Sniffer assignment into a concrete
implementation, evidence, report, and packaging workflow.

For the detailed engineering procedure, use
`docs/technical-implementation-plan.md`. That file expands this plan into
browser setup, extension architecture, filtering logic, decoder fallback order,
evidence capture, report sections, validation gates, and final packaging
commands.

For the research-quality final review, use
`docs/postdoc-researcher-execution-audit.md`. That file lists the overlooked
controls that make the submission more reproducible, privacy-aware, and
defensible.

## Target Outcome

Deliver a Microsoft Edge / Chrome Manifest V3 extension that observes browser
request payloads during the Cambridge Dictionary browsing scenario, filters for
advertising-network requests, decodes request bodies into readable evidence,
and packages the extension plus a PDF report for submission.

## Repository Layout

Use these working paths:

```text
homeworks/hw04-web-traffic-sniffer/
├── raw/                         # official source files, kept unchanged
├── starter/example/             # extracted official starter
├── docs/                        # capture, redaction, filtering, and report controls
├── solution/Extension/          # implemented extension
├── evidence/                    # screenshots and sanitized notes
├── report/                      # report draft, assets, final PDF
├── scripts/                     # profile launch and submission validators
└── submission/                  # final upload package staging
```

## Step 1 - Bootstrap The Extension

1. Copy the official starter into the solution folder:

   ```bash
   mkdir -p solution/Extension
   cp starter/example/manifest.json solution/Extension/manifest.json
   cp starter/example/background.js solution/Extension/background.js
   ```

2. Keep Manifest V3 and `webRequest` permission.
3. Keep host permissions broad enough for the assignment scenario during
   evidence capture, then document that this permission is intentionally broad
   for controlled homework observation.
4. Load `solution/Extension/` in Edge through `edge://extensions/` with
   Developer mode enabled.
5. Open the extension service worker console before browsing the target site.

Current implementation:

- `solution/Extension/manifest.json`
- `solution/Extension/background.js`
- `scripts/launch-clean-profile.sh`

## Step 2 - Implement Request Filtering

The extension should keep useful ad-tech traffic visible while suppressing
general browser noise.

Implementation direction:

1. Define an allowlist of advertising-network host patterns observed during the
   Cambridge Dictionary scenario. Start with likely targets from the spec:
   `amazon`, `criteo`, and add other observed ad endpoints only when evidence
   confirms them.
2. Parse each request URL with `new URL(details.url)`.
3. Check `hostname` and optionally `pathname` against the allowlist.
4. Return early for unrelated domains.
5. Log a compact summary with:
   - request URL
   - method
   - request ID
   - initiator, when available
   - decoded payload

Acceptance check:

- The console is not flooded with unrelated static assets.
- At least two advertiser-related domains appear with decoded payloads.

Current implementation control:

- Normal mode uses `DEBUG_MODE = false` and logs allowlisted ad-tech hosts with
  request bodies.
- Debug mode uses `DEBUG_MODE = true` for candidate discovery when the live
  Cambridge Dictionary ad stack changes.
- Filtering and decoding are documented in
  `docs/filtering-and-decoding-contract.md`.

## Step 3 - Decode Request Bodies

The grading contract needs complete readable payloads.

Implementation direction:

1. In `chrome.webRequest.onBeforeRequest`, request `["requestBody"]`.
2. Handle `details.requestBody.raw`:
   - concatenate `ArrayBuffer` chunks
   - decode with `TextDecoder("utf-8")`
   - try `JSON.parse`
   - if JSON parse fails, try `URLSearchParams`
   - if both fail, log the decoded raw string
3. Handle `details.requestBody.formData` when present.
4. Keep the logging structure stable:
   - `console.groupCollapsed(...)`
   - `console.table(...)` for metadata when useful
   - `console.dir(decodedPayload, { depth: null })`
   - `console.groupEnd()`

Acceptance check:

- Payloads are readable as JSON objects, form-data objects, query-like key/value
  maps, or clear strings.
- The raw URL and decoded payload are shown together for evidence screenshots.

## Step 4 - Capture Evidence

Use a controlled browsing workflow and record only assignment-relevant output.

1. Install the extension from `solution/Extension/`.
2. Open the service worker console.
3. Visit Cambridge Dictionary in a fresh browser window or profile.
4. Search or navigate through several dictionary pages to trigger ad traffic.
5. Capture screenshots showing:
   - the extension is loaded
   - the service worker console is open
   - at least two advertiser payloads are decoded
   - one Amazon-like endpoint and one Criteo-like endpoint when available
6. Save screenshots under:

   ```text
   evidence/screenshots/
   ```

7. Save a short sanitized observation note:

   ```text
   evidence/traffic-observations.md
   ```

Safety and privacy control:

- Use your own browser session or a clean test profile.
- Do not publish cookies, account identifiers, tokens, or stable personal IDs in
  the report.
- Redact sensitive values in screenshots when necessary while keeping advertiser
  domain, payload shape, and field names visible.

Current evidence controls:

- Clean profile protocol: `docs/clean-browser-profile.md`
- Redaction rules: `docs/redaction-rules.md`
- Raw local evidence ignore rules: `evidence/.gitignore`
- Sanitized observation template: `evidence/traffic-observations.md`

## Step 5 - Write The Report

Create the report in `report/report.md`, then export it to PDF.

Required sections:

1. **Code Analysis**
   - Explain Manifest V3 service worker architecture.
   - Explain `chrome.webRequest.onBeforeRequest`.
   - Explain domain filtering.
   - Explain raw request body decoding.
2. **Evidence Of Results**
   - Include screenshots.
   - Name at least two receiving advertisers.
   - Explain specific payload fields and what they reveal.
3. **Privacy Risk Assessment**
   - Describe browsing-interest inference, cross-site tracking, profiling, and
     identifier leakage risks.
4. **HTTPS Analysis**
   - Explain that HTTPS protects network transit but browser extensions run
     inside the browser privilege boundary and can observe requests before or
     after encryption.
5. **Content Security Policy**
   - Explain extension privilege boundaries and why extension APIs/content
     scripts can operate outside normal page CSP assumptions.
6. **Attack Vectors And Mitigation**
   - Choose one conceptual attack, such as cookie theft, keylogging, ad
     injection, or form-data capture.
   - Pair it with concrete mitigation: permission review, extension allowlists,
     enterprise policies, least-privilege permissions, store review, and browser
     profile separation.

Report quality checklist:

- Every claim is tied to code behavior, observed evidence, or browser
  architecture.
- Screenshots are numbered and referenced in the text.
- Sensitive values are redacted.
- The report answers all six questions explicitly.

## Step 6 - Validate The Package

Before packaging:

1. Reload the extension in Edge.
2. Confirm no syntax errors in the service worker console.
3. Confirm relevant traffic still appears after a browser refresh.
4. Confirm the report PDF opens.
5. Confirm the submission package includes only required deliverables.

Suggested local validation commands:

```bash
find solution/Extension -maxdepth 2 -type f -print
find report evidence -maxdepth 3 -type f -print
```

Submission dry-run verifier:

```bash
scripts/build_submission_dry_run.sh 513559004
```

## Step 7 - Build The Submission ZIP

The official PDF labels the assignment as HW4 but gives the submission folder
name as `HW6_{student_ID}`. Confirm the final folder name on the course platform
before upload.

Staging structure from the PDF:

```text
submission/HW6_{student_ID}/
├── Extension/
│   ├── manifest.json
│   └── background.js
└── {student_ID}_report.pdf
```

Packaging command pattern:

```bash
mkdir -p submission/HW6_${STUDENT_ID}/Extension
cp solution/Extension/manifest.json submission/HW6_${STUDENT_ID}/Extension/
cp solution/Extension/background.js submission/HW6_${STUDENT_ID}/Extension/
cp report/${STUDENT_ID}_report.pdf submission/HW6_${STUDENT_ID}/
cd submission
zip -r HW6_${STUDENT_ID}.zip HW6_${STUDENT_ID}
```

## Implementation Milestones

| Milestone | Done when |
| --- | --- |
| M1 starter copied | `solution/Extension/` loads in Edge |
| M2 filtering works | unrelated console traffic is suppressed |
| M3 decoding works | raw payloads are readable as JSON/form/string |
| M4 evidence captured | screenshots show two advertiser payloads |
| M5 report complete | all six questions have evidence-backed answers |
| M6 package ready | final ZIP contains extension files and report PDF |

## Immediate Next Action

Create `solution/Extension/` from the starter, implement the filtering and
payload decoder in `background.js`, then run the first Edge service-worker
console smoke test.
