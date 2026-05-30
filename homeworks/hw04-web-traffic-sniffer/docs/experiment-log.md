# HW04 Web Traffic Sniffer Experiment Log

This log records the concrete experiment steps, commands, environment facts,
outputs, metrics, evidence paths, and packaging checks for the HW4 Web Traffic
Sniffer assignment. It intentionally records sanitized summaries only. Raw
browser profile state and raw runtime evidence remain under ignored
`evidence/raw-local/`.

## Experiment Scope

| Field | Value |
| --- | --- |
| Assignment | HW4. Web Traffic Sniffer |
| Course | Network Security Practices - Attack and Defense |
| Student ID | `513559004` |
| Target site | `https://dictionary.cambridge.org/` |
| Extension mode | Normal mode, `DEBUG_MODE = false` |
| Clean profile | `evidence/raw-local/edge-profile/` (ignored) |
| Evidence policy | raw local evidence ignored; sanitized screenshots tracked |
| Final package | `submission/final/HW6_513559004.zip` |

## Environment Facts

| Item | Observed value |
| --- | --- |
| Date | 2026-05-30 |
| OS context | Linux local shell |
| Node.js | `v22.22.2` |
| Python | `Python 3.12.3` |
| Browser runtime | Playwright-managed Chromium |
| Browser version | `Chrome/148.0.7778.96` |
| Browser binary | `~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome` |
| Remote debugging port | `9222` |

## Source Inputs

| Artifact | Path | Notes |
| --- | --- | --- |
| Official PDF | `raw/hw04-web-traffic-sniffer-spec.pdf` | 3-page assignment spec |
| Official starter ZIP | `raw/hw04-web-traffic-sniffer-example.zip` | Extracts to `example/manifest.json` and `example/background.js` |
| Starter manifest | `starter/example/manifest.json` | Official Manifest V3 starter |
| Starter service worker | `starter/example/background.js` | Official incomplete request-body starter |

## Implementation Artifacts

| Artifact | Path | Purpose |
| --- | --- | --- |
| Manifest | `solution/Extension/manifest.json` | Manifest V3 extension metadata and permission declaration |
| Service worker | `solution/Extension/background.js` | Filtering, decoding, logging, debug/normal mode |
| Logic test | `scripts/test_extension_logic.js` | Unit-level validation for filtering and decoder behavior |
| Runtime smoke | `scripts/runtime_smoke.js` | CDP-based clean-profile runtime validation |
| Sanitized capture | `scripts/capture_sanitized_evidence.js` | Generates sanitized PNG/HTML/Markdown evidence |
| Submission verifier | `scripts/validate_submission.py` | Checks ZIP/PDF/package structure and forbidden artifacts |

## Experiment Timeline

### E1. Official Material Import

Actions:

```bash
mkdir -p homeworks/hw04-web-traffic-sniffer/{raw,starter,notes}
mv ~/Downloads/SL-[2026\ NS]\ Web\ Traffic\ Sniffer-210526-010145.pdf \
  homeworks/hw04-web-traffic-sniffer/raw/hw04-web-traffic-sniffer-spec.pdf
mv ~/Downloads/example.zip \
  homeworks/hw04-web-traffic-sniffer/raw/hw04-web-traffic-sniffer-example.zip
unzip -q homeworks/hw04-web-traffic-sniffer/raw/hw04-web-traffic-sniffer-example.zip \
  -d homeworks/hw04-web-traffic-sniffer/starter
```

Observed:

- PDF metadata: title `[2026 NS] Web Traffic Sniffer - SENSE LAB - Confluence`.
- PDF pages: 3.
- ZIP contents:
  - `example/background.js`
  - `example/manifest.json`

### E2. Extension Implementation

Implemented:

- normal mode / debug mode through `DEBUG_MODE`;
- ad-tech allowlist including Amazon, Criteo, DoubleClick, Google ad, OpenX,
  PubMatic, Rubicon, AppNexus, and related host families;
- URL parsing with `new URL(details.url)`;
- static resource exclusion;
- payload evidence requirement through request body or query parameters;
- decoder fallback:
  1. `formData`
  2. JSON
  3. URL-encoded form
  4. raw string
  5. query parameters
- sanitized payload-shape logging for report screenshots.

Key design control:

```js
const DEBUG_MODE = false;
```

### E3. Clean Browser Profile Setup

Command:

```bash
HW4_REMOTE_DEBUGGING_PORT=9222 \
  scripts/launch-clean-profile.sh about:blank
```

Runtime arguments:

- `--user-data-dir=evidence/raw-local/edge-profile`
- `--no-first-run`
- `--disable-sync`
- `--load-extension=solution/Extension`
- `--remote-debugging-port=9222`
- `--no-sandbox` only for Playwright Chromium fallback on this Linux host

Observed:

- Browser launched successfully with Playwright Chromium fallback.
- Remote debugging endpoint available at
  `http://127.0.0.1:9222/json/version`.
- Extension service worker target visible:
  `chrome-extension://.../background.js`.

### E4. Static And Unit Validation

Commands:

```bash
node --check solution/Extension/background.js
node scripts/test_extension_logic.js
python3 -m json.tool solution/Extension/manifest.json >/tmp/hw4-manifest-final.json
```

Observed:

```text
OK: extension filtering and decoder logic tests passed.
```

Validated behavior:

- exactly one `chrome.webRequest.onBeforeRequest` listener is registered;
- listener uses `{ urls: ["<all_urls>"] }`;
- listener requests `["requestBody"]`;
- Amazon/Criteo allowlisted request logs in normal mode;
- unrelated request is filtered out;
- static resource is filtered out;
- query-parameter ad-tech request logs even without body;
- JSON body decodes as JSON;
- URL-encoded body decodes as object;
- `formData` body is preserved;
- opaque string stays `rawString`.

### E5. Runtime Smoke On Cambridge Dictionary

Command:

```bash
HW4_RUNTIME_WAIT_MS=20000 \
  node scripts/runtime_smoke.js https://dictionary.cambridge.org/
```

Observed metrics from ignored raw local summary:

```json
{
  "targetUrl": "https://dictionary.cambridge.org/",
  "waitMs": 20000,
  "consoleEvents": 732,
  "snifferEvents": 106
}
```

Top observed ad-tech hosts:

| Host | Count |
| --- | ---: |
| `pixel.rubiconproject.com` | 15 |
| `pagead2.googlesyndication.com` | 14 |
| `cm.g.doubleclick.net` | 11 |
| `securepubads.g.doubleclick.net` | 10 |
| `fastlane.rubiconproject.com` | 6 |
| `ib.adnxs.com` | 6 |
| `ads.pubmatic.com` | 4 |
| `ut.pubmatic.com` | 4 |
| `secure.adnxs.com` | 4 |
| `gum.criteo.com` | 3 |
| `s.amazon-adsystem.com` | 3 |
| `us-u.openx.net` | 3 |
| `web-banner.ads.aps.amazon-adsystem.com` | 2 |
| `rtb.openx.net` | 2 |
| `grid-bidder.criteo.com` | 2 |
| `hbopenbid.pubmatic.com` | 2 |
| `image8.pubmatic.com` | 2 |
| `token.rubiconproject.com` | 2 |
| `dis.criteo.com` | 2 |
| `ssp-sync.criteo.com` | 2 |

Evidence control:

- Full raw summary path: `evidence/raw-local/runtime-smoke-summary.json`
  (ignored).
- Tracked observation summary: `evidence/traffic-observations.md`.

### E6. Sanitized Evidence Capture

Command:

```bash
HW4_CAPTURE_WAIT_MS=25000 \
  node scripts/capture_sanitized_evidence.js https://dictionary.cambridge.org/
```

Observed:

```text
OK: sanitized evidence captured.
Records observed: 116
Evidence PNG: evidence/screenshots/sanitized-console-evidence.png
Evidence Markdown: evidence/screenshots/sanitized-console-evidence.md
```

Selected sanitized figures:

| Figure | Domain | Method | Payload type | Filter reason |
| --- | --- | --- | --- | --- |
| 1 | `gum.criteo.com` | GET | query payload / `none` body | `advertising-host-allowlist` |
| 2 | `web-banner.ads.aps.amazon-adsystem.com` | POST | JSON body | `advertising-host-allowlist` |
| 3 | `cm.g.doubleclick.net` | GET | query payload / `none` body | `advertising-host-allowlist` |

Redaction behavior:

- long opaque values are not shown in tracked evidence;
- URLs are represented as `[redacted-url]`;
- field names are preserved;
- data types and payload structure are preserved;
- raw selected records stay in
  `evidence/raw-local/sanitized-evidence-records.json` (ignored).

Tracked evidence:

- `evidence/screenshots/sanitized-console-evidence.png`
- `evidence/screenshots/sanitized-console-evidence.md`
- `evidence/screenshots/sanitized-console-evidence.html`
- `evidence/traffic-observations.md`

### E7. Report Generation

Inputs:

- `report/report.html`
- `evidence/screenshots/sanitized-console-evidence.png`

Command:

```bash
chrome=~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome
"$chrome" \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf=report/513559004_report.pdf \
  file://$(realpath report/report.html)
```

Observed:

```text
report/513559004_report.pdf: PDF document, version 1.4, 4 page(s)
```

PDF metadata:

| Field | Value |
| --- | --- |
| Title | `HW4 Web Traffic Sniffer Report` |
| Pages | 4 |
| Encrypted | no |
| JavaScript | no |
| File size | 177325 bytes |

Report content:

- Q1 code analysis;
- Q2 evidence table and sanitized screenshot;
- Q3 privacy risk assessment;
- Q4 HTTPS/browser architecture analysis;
- Q5 CSP/extension privilege-boundary analysis;
- Q6 malicious extension attack vector and mitigations.

### E8. Submission Package Build

Commands:

```bash
rm -rf submission/final
mkdir -p submission/final/HW6_513559004/Extension
cp solution/Extension/manifest.json submission/final/HW6_513559004/Extension/
cp solution/Extension/background.js submission/final/HW6_513559004/Extension/
cp report/513559004_report.pdf submission/final/HW6_513559004/
cd submission/final
zip -qr HW6_513559004.zip HW6_513559004
```

Validation:

```bash
python3 scripts/validate_submission.py \
  --student-id 513559004 \
  --package-dir submission/final/HW6_513559004 \
  --zip submission/final/HW6_513559004.zip
```

Observed:

```text
OK: submission dry-run package passed structural checks.
```

ZIP contents:

```text
HW6_513559004/
HW6_513559004/Extension/
HW6_513559004/Extension/background.js
HW6_513559004/Extension/manifest.json
HW6_513559004/513559004_report.pdf
```

Package metrics:

| File | Size |
| --- | ---: |
| `Extension/background.js` | 6759 bytes |
| `Extension/manifest.json` | 371 bytes |
| `513559004_report.pdf` | 177325 bytes |
| ZIP total listed payload | 184455 bytes |

### E9. Redaction And Ignore Verification

Commands:

```bash
git check-ignore -v evidence/raw-local/edge-profile
git check-ignore -v evidence/raw-local/runtime-smoke-summary.json
git check-ignore -v evidence/raw-local/sanitized-evidence-records.json
git check-ignore -v submission/dry-run/HW6_513559004.zip
git check-ignore -v submission/final/HW6_513559004.zip
```

Observed:

- `evidence/.gitignore:1:raw-local/` ignores raw local browser/evidence state.
- `submission/.gitignore:1:dry-run/` ignores dry-run package.
- `submission/.gitignore:2:*.zip` ignores final ZIP archive.

Tracked sanitized evidence check:

```bash
rg -n "file:///|[A-Za-z0-9_-]{80,}|uid=|bearer|authorization" \
  evidence/screenshots report
```

Observed:

- no local `file:///` header/footer remains in PDF text after regenerating with
  `--no-pdf-header-footer`;
- tracked evidence uses `[redacted-url]`, `string`, and payload-shape labels
  instead of raw long identifiers.

## Current Evidence Inventory

Tracked evidence:

| Path | Purpose |
| --- | --- |
| `evidence/screenshots/sanitized-console-evidence.png` | report-ready sanitized service-worker console evidence |
| `evidence/screenshots/sanitized-console-evidence.md` | figure/domain/payload summary |
| `evidence/screenshots/sanitized-console-evidence.html` | HTML source for screenshot rendering |
| `evidence/traffic-observations.md` | sanitized narrative observation log |
| `report/513559004_report.pdf` | final report PDF |
| `submission/final/HW6_513559004/` | final package staging directory |

Ignored evidence:

| Path | Purpose |
| --- | --- |
| `evidence/raw-local/edge-profile/` | clean Chromium profile state |
| `evidence/raw-local/runtime-smoke-summary.json` | local runtime domain-count summary |
| `evidence/raw-local/sanitized-evidence-records.json` | local selected CDP event records |
| `submission/dry-run/` | dry-run package output |
| `submission/final/HW6_513559004.zip` | generated final ZIP archive |

## Artifact Provenance

Generate the artifact manifest after final report or ZIP changes:

```bash
python3 scripts/generate_artifact_manifest.py
```

The manifest records SHA-256 hashes and byte sizes for:

- official spec PDF;
- official starter ZIP;
- submitted `manifest.json`;
- submitted `background.js`;
- sanitized evidence image and Markdown;
- final report PDF;
- final upload ZIP.

Tracked manifest path:

```text
docs/artifact-manifest.json
```

## Reproducibility Protocol

To reproduce the full experiment:

```bash
cd homeworks/hw04-web-traffic-sniffer

# 1. Static and unit checks
node --check solution/Extension/background.js
node scripts/test_extension_logic.js
python3 -m json.tool solution/Extension/manifest.json >/tmp/hw4-manifest-final.json

# 2. Clean profile runtime
HW4_REMOTE_DEBUGGING_PORT=9222 scripts/launch-clean-profile.sh about:blank
HW4_RUNTIME_WAIT_MS=20000 node scripts/runtime_smoke.js https://dictionary.cambridge.org/

# 3. Sanitized evidence capture
HW4_CAPTURE_WAIT_MS=25000 node scripts/capture_sanitized_evidence.js https://dictionary.cambridge.org/

# 4. Report PDF
~/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf=report/513559004_report.pdf \
  file://$(realpath report/report.html)

# 5. Package validation
python3 scripts/validate_submission.py \
  --student-id 513559004 \
  --package-dir submission/final/HW6_513559004 \
  --zip submission/final/HW6_513559004.zip
```

## Notes And Caveats

- The official assignment page says HW4, while the PDF submission structure says
  `HW6_{student_ID}`. The final package follows the PDF structure and documents
  the mismatch in `submission/README.md`.
- Local automated capture used Playwright Chromium because Microsoft Edge was
  not available on `PATH`. The implementation remains Manifest V3 and
  `chrome.webRequest` compatible with Edge.
- The observed ad-tech domains may vary by time, region, consent state, and
  auction path. The implementation's debug mode and allowlist expansion plan
  are the reproducibility controls for this drift.
- Values in report screenshots are intentionally redacted. The evidence
  preserves domain, method, filter reason, payload type, field names, data
  types, and structure.
