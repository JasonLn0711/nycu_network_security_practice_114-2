# HW04 Web Traffic Sniffer Technical Implementation Plan

This plan is the step-by-step engineering route for finishing the Network
Security Practice HW4 assignment without weakening the official requirements.
The project should be executed as a controlled privacy evidence-capture task:
build the extension, capture only assignment-relevant browser traffic, redact
sensitive values, and package the final extension plus report.

## 0. Assignment Contract

Official objective:

- Build a Microsoft Edge / Chrome Manifest V3 extension.
- Use `chrome.webRequest.onBeforeRequest`.
- Observe request payloads while browsing Cambridge Dictionary.
- Filter browser noise and focus on advertising-network requests.
- Decode request payloads into readable JSON, form data, or strings.
- Capture evidence from at least two advertising networks.
- Write a report answering the six required questions.
- Submit a ZIP containing `Extension/manifest.json`, `Extension/background.js`,
  and `{student_ID}_report.pdf`.

Local repo target:

```text
homeworks/hw04-web-traffic-sniffer/
├── solution/Extension/manifest.json
├── solution/Extension/background.js
├── evidence/screenshots/
├── evidence/traffic-observations.md
├── report/report.md
└── submission/
```

## 1. Environment And Browser Setup

### 1.1 Install / Locate Browser

The official spec says the assignment is evaluated with Microsoft Edge. Use
Microsoft Edge when available. Chromium or Chrome is acceptable for local
development checks because the extension APIs are the same family, but final
evidence should use Edge if possible.

Check locally:

```bash
command -v microsoft-edge || command -v microsoft-edge-stable || command -v chromium || command -v google-chrome
```

Current shell note: this environment does not expose Edge/Chromium/Chrome on
`PATH`, so live capture must run in a desktop environment that has Edge or
Chromium installed.

### 1.2 Launch Clean Profile

Use an isolated profile so daily cookies, accounts, and browsing history do not
enter the evidence.

```bash
cd homeworks/hw04-web-traffic-sniffer
scripts/launch-clean-profile.sh
```

Profile path:

```text
evidence/raw-local/edge-profile/
```

This path is intentionally ignored by Git.

### 1.3 Load Extension

In the clean browser profile:

1. Open `edge://extensions/`.
2. Enable Developer mode.
3. Click `Load unpacked`.
4. Select:

   ```text
   homeworks/hw04-web-traffic-sniffer/solution/Extension/
   ```

5. Confirm the extension appears as `HW4 Web Traffic Sniffer`.
6. Click the service worker link to open DevTools.
7. Keep the Console tab open before browsing Cambridge Dictionary.

Acceptance evidence:

- Screenshot showing the extension loaded in the clean profile.
- Screenshot showing the service worker console with the extension loaded
  message.

## 2. Extension Architecture

### 2.1 Manifest

File:

```text
solution/Extension/manifest.json
```

Required shape:

```json
{
  "manifest_version": 3,
  "name": "HW4 Web Traffic Sniffer",
  "version": "1.0",
  "permissions": ["webRequest"],
  "host_permissions": ["<all_urls>"],
  "background": {
    "service_worker": "background.js"
  }
}
```

Technical reason:

- `manifest_version: 3` matches the assignment.
- `webRequest` allows the background service worker to observe outgoing
  requests.
- `<all_urls>` is broad by design for controlled homework observation; the code
  then narrows what appears in the console through filtering.
- `background.service_worker` runs `background.js` as the extension's event
  worker.

### 2.2 Service Worker Responsibilities

File:

```text
solution/Extension/background.js
```

The service worker has five responsibilities:

1. register `chrome.webRequest.onBeforeRequest`;
2. decide whether a request is relevant;
3. decode request body and query payloads;
4. print stable, screenshot-friendly console evidence;
5. support debug discovery without changing final normal-mode behavior.

## 3. Filtering Design

### 3.1 Normal Mode

Constant:

```js
const DEBUG_MODE = false;
```

Normal mode is the final report mode. It logs a request only when all conditions
are true:

1. `new URL(details.url)` succeeds.
2. The URL path does not end with static asset extensions such as `.png`,
   `.jpg`, `.css`, `.js`, `.woff`, or `.svg`.
3. The request has payload evidence:
   - `details.requestBody.raw`,
   - `details.requestBody.formData`, or
   - URL query parameters.
4. The hostname matches the ad-tech allowlist.

This directly supports the 10% filtering criterion because the report can
explain exactly how unrelated traffic is suppressed.

### 3.2 Debug Mode

Constant:

```js
const DEBUG_MODE = true;
```

Debug mode is only for development. It helps discover current ad-tech domains
when live Cambridge Dictionary traffic does not show the same Amazon/Criteo
examples from the PDF.

Debug workflow:

1. Temporarily set `DEBUG_MODE = true`.
2. Reload the extension.
3. Browse Cambridge Dictionary.
4. Record candidate domains in `evidence/raw-local/`.
5. Add confirmed advertising-network domains to `AD_TECH_HOST_PATTERNS`.
6. Set `DEBUG_MODE = false`.
7. Capture final screenshots only in normal mode.

### 3.3 Allowlist Strategy

Start with the official examples and known advertising infrastructure:

- Amazon: `amazon-adsystem.com`, `aax.amazon-adsystem.com`, `aps.amazon.com`
- Criteo: `criteo.com`, `criteo.net`
- Other observed/common ad-tech families: `doubleclick.net`,
  `googlesyndication.com`, `googleadservices.com`, `openx.net`,
  `pubmatic.com`, `rubiconproject.com`, `rlcdn.com`, `taboola.com`,
  `adnxs.com`, `adsrvr.org`

Rule for expanding the allowlist:

- Add a domain only when the clean-profile debug capture shows it receiving
  advertising or tracking payloads during the Cambridge Dictionary scenario.
- Record the reason in `evidence/traffic-observations.md`.

## 4. Payload Decoding Design

### 4.1 Event Listener

The listener must request the body:

```js
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    // filter and decode
  },
  { urls: ["<all_urls>"] },
  ["requestBody"]
);
```

### 4.2 Decode Order

Decoder fallback order:

1. `details.requestBody.formData`
2. raw chunks decoded with `TextDecoder("utf-8")`
3. `JSON.parse(rawString)`
4. `URLSearchParams(rawString)`
5. raw readable string
6. query parameters from `new URL(details.url).searchParams`

Technical rationale:

- Advertising payloads are not guaranteed to be JSON.
- Some payloads are URL-encoded forms.
- Some requests put evidence in query parameters.
- The report needs readable evidence, so the decoder should keep the best
  available representation rather than fail on non-JSON input.

### 4.3 Screenshot-Friendly Console Output

Each logged request should use:

```js
console.groupCollapsed(`[HW4 sniffer] ${method} ${hostname}`);
console.table(metadata);
console.dir(decodedPayload);
console.groupEnd();
```

Metadata to show:

- `requestId`
- `method`
- `url`
- `hostname`
- `initiator`
- `tabId`
- `filterReason`
- `payloadType`

This gives the report enough material to explain both filtering and decoding.

## 5. Evidence Capture Workflow

### 5.1 Raw Local Evidence

Use:

```text
evidence/raw-local/
```

Allowed contents:

- unredacted temporary screenshots;
- temporary candidate-domain notes;
- browser profile;
- local console notes.

These files are ignored and should not be committed.

### 5.2 Sanitized Evidence

Use:

```text
evidence/screenshots/
evidence/traffic-observations.md
```

Only move redacted screenshots into `evidence/screenshots/`.

Minimum final screenshots:

1. Extension loaded in the clean browser profile.
2. Service worker console with normal-mode loaded message.
3. First advertiser payload decoded.
4. Second advertiser payload decoded.
5. Optional: screenshot showing the browser page context on Cambridge
   Dictionary.

### 5.3 Redaction Rules

Redact:

- cookies;
- session IDs;
- email/account IDs;
- stable browser, device, user, or advertising IDs;
- exact location;
- IP addresses when visible;
- auth headers, tokens, API keys;
- long opaque values that can identify a user or session.

Preserve:

- advertiser domain;
- request method;
- field names;
- data types;
- payload object structure;
- non-sensitive page context.

## 6. Report Writing Plan

Draft path:

```text
report/report.md
```

Final PDF path:

```text
report/513559004_report.pdf
```

### Q1 Code Analysis

Include:

- Manifest V3 service worker architecture.
- Why `webRequest` and `onBeforeRequest` are used.
- Why `<all_urls>` is paired with code-level filtering.
- How host allowlist filtering works.
- How static assets are excluded.
- How the decoder handles JSON, forms, strings, and query parameters.

Evidence references:

- `solution/Extension/manifest.json`
- `solution/Extension/background.js`
- screenshots showing filtered console output.

### Q2 Evidence Of Results

Include:

- screenshot references;
- two advertiser domains;
- payload type for each;
- example field names;
- what the data indicates.

Use a table:

| Figure | Advertiser domain | Payload type | Relevant fields | Interpretation |
| --- | --- | --- | --- | --- |

### Q3 Privacy Risk Assessment

Explain risks through the observed payload structure:

- cross-site tracking;
- interest profiling;
- dictionary lookup inference;
- identifier correlation;
- leakage of browsing context to third parties.

Keep the language evidence-backed: connect each risk to a field type or
request context shown in screenshots.

### Q4 HTTPS Analysis

Core claim:

HTTPS protects network transit, but the extension operates inside the browser
privilege boundary. A granted extension can observe metadata and request bodies
before the network attacker model is the relevant layer.

Avoid saying:

- "HTTPS is broken."

Say:

- "HTTPS remains effective for transport confidentiality, while extension
  permissions create a separate browser-internal observation path."

### Q5 CSP Analysis

Core claim:

CSP controls page-loaded scripts and resources. Extensions operate under the
browser extension permission model, so extension APIs and content scripts are
not equivalent to ordinary website JavaScript.

Avoid saying:

- "CSP has a bug."

Say:

- "The security boundary is extension permission governance, not only website
  CSP configuration."

### Q6 Attack Vector And Mitigation

Pick one:

- cookie theft;
- keylogging;
- ad injection;
- form-data capture.

Recommended answer path:

- Describe the attack at a high level.
- Explain why extension permissions make it possible.
- Propose mitigations:
  - least-privilege permissions;
  - extension allowlists;
  - user review of requested permissions;
  - separate browser profiles;
  - removing unused extensions;
  - enterprise policy controls.

## 7. Local Validation Plan

### 7.1 Static Validation

Run:

```bash
node --check solution/Extension/background.js
python3 -m json.tool solution/Extension/manifest.json >/tmp/hw4-manifest.json
```

Pass condition:

- no JavaScript syntax error;
- manifest is valid JSON.

### 7.2 Extension Runtime Smoke Test

In Edge:

1. Load extension.
2. Open service worker console.
3. Confirm loaded message:

   ```text
   [HW4 sniffer] Loaded. mode=normal; target=Cambridge Dictionary; filtering=ad-tech allowlist
   ```

4. Visit Cambridge Dictionary.
5. Confirm logged groups have:
   - hostname;
   - filter reason;
   - payload type;
   - decoded payload or query parameters.

Command-line runtime smoke test after launching the clean profile:

```bash
scripts/runtime_smoke.js https://dictionary.cambridge.org/
```

This uses the Chromium remote debugging endpoint to confirm the background
service worker is loaded, evaluate the filtering and decoder functions inside
the extension runtime, and navigate the clean-profile page to Cambridge
Dictionary.

### 7.3 Evidence Quality Gate

Before final report:

- at least two advertiser domains;
- final screenshots in normal mode;
- screenshots redacted;
- `traffic-observations.md` filled;
- no raw local captures tracked by Git.

Check:

```bash
git status --short --ignored -- evidence submission
git check-ignore -v evidence/raw-local/edge-profile
```

### 7.4 Submission Dry Run

Run:

```bash
scripts/build_submission_dry_run.sh 513559004
```

This validates:

- root folder: `HW6_513559004`;
- `Extension/manifest.json`;
- `Extension/background.js`;
- `513559004_report.pdf`;
- PDF header;
- no `.git`, `.DS_Store`, `raw-local`, or cache files.

## 8. Final Submission Build

After final report export:

```bash
cd homeworks/hw04-web-traffic-sniffer
rm -rf submission/final
mkdir -p submission/final/HW6_513559004/Extension
cp solution/Extension/manifest.json submission/final/HW6_513559004/Extension/
cp solution/Extension/background.js submission/final/HW6_513559004/Extension/
cp report/513559004_report.pdf submission/final/HW6_513559004/
cd submission/final
zip -r HW6_513559004.zip HW6_513559004
cd ../..
python3 scripts/validate_submission.py \
  --student-id 513559004 \
  --package-dir submission/final/HW6_513559004 \
  --zip submission/final/HW6_513559004.zip
```

Before upload, confirm whether E3 expects the PDF's `HW6_{student_ID}` folder
name exactly as written in the official PDF or a corrected HW4-based name.

## 9. Execution Checklist

| Phase | Action | Output |
| --- | --- | --- |
| Setup | Launch clean profile | ignored `evidence/raw-local/edge-profile/` |
| Setup | Load extension | extension visible in Edge |
| Debug | Candidate-domain discovery if needed | local notes under `raw-local/` |
| Implementation | Update allowlist if evidence supports it | `background.js` |
| Capture | Normal-mode console screenshots | `evidence/screenshots/` |
| Evidence | Fill observations | `evidence/traffic-observations.md` |
| Report | Complete six answers | `report/report.md` |
| Export | Build PDF | `report/513559004_report.pdf` |
| Package | Build final ZIP | `submission/final/HW6_513559004.zip` |
| Validate | Run verifier | `OK: submission dry-run package passed structural checks.` |

## 10. Definition Of Done

The assignment is ready to upload when all of these are true:

- Extension loads in Microsoft Edge clean profile.
- Final capture uses `DEBUG_MODE = false`.
- At least two advertiser payloads are visible and decoded.
- Screenshots are redacted and referenced in the report.
- Report answers all six official questions.
- Final PDF opens.
- Final ZIP validates with `scripts/validate_submission.py`.
- No raw local evidence, browser profile, cookies, logs, or unredacted captures
  are tracked by Git.
