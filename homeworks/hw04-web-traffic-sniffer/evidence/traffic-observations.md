# Traffic Observations

This file records sanitized evidence from the controlled Cambridge Dictionary
browsing session.

## Capture Context

- Browser profile: clean HW4 profile
- Extension path: `solution/Extension/`
- Extension mode: normal mode for final evidence; debug mode only for candidate
  discovery
- Target site: Cambridge Dictionary
- Capture date: 2026-05-30
- Browser: Playwright-managed Chromium `Chrome/148.0.7778.96` with isolated
  `evidence/raw-local/edge-profile/`
- Runtime smoke wait: 25 seconds for sanitized evidence capture
- Runtime smoke summary: `evidence/raw-local/runtime-smoke-summary.json`
  (ignored raw-local evidence)

## Observed Advertiser Payloads

| Screenshot | Advertiser / domain | Payload type | Evidence summary | Redaction applied |
| --- | --- | --- | --- | --- |
| `screenshots/sanitized-console-evidence.png`, Figure 1 | `gum.criteo.com` | query payload, decoded by extension runtime | Criteo-family ad-tech request appeared in normal mode while browsing Cambridge Dictionary. Field names include `origin`, `topUrl`, `domain`, `bundle`, `cw`, and `lsw`; values are type-shaped or redacted. | Values redacted; domain, field names, data types, and payload structure preserved. |
| `screenshots/sanitized-console-evidence.png`, Figure 2 | `web-banner.ads.aps.amazon-adsystem.com` | JSON body, decoded by extension runtime | Amazon ad-system request appeared in normal mode while browsing Cambridge Dictionary. The extension classified it through the ad-tech allowlist and JSON decoder path. | Values redacted; domain, method, payload type, filter reason, and structure preserved. |
| `screenshots/sanitized-console-evidence.png`, Figure 3 | `cm.g.doubleclick.net` | query payload, decoded by extension runtime | Additional ad-tech request appeared, confirming the implementation should not depend only on Amazon/Criteo examples. | Values redacted; domain, field names, and data types preserved. |

## Filtering Evidence

Record how the final evidence shows filtering:

- Hostname parsed from request URL: implemented in `shouldLogRequest()` using
  `new URL(details.url)`.
- Allowlist match: implemented through `AD_TECH_HOST_PATTERNS`; live normal-mode
  smoke observed Criteo, Amazon, Rubicon, Google ad, PubMatic, AppNexus, and
  OpenX-family hosts.
- Static asset excluded: implemented through `STATIC_RESOURCE_EXTENSIONS`.
- Payload evidence required through request body or query parameters:
  implemented through `hasRequestBody()` and `hasQueryParameters()`.
- Debug-only candidates excluded from final screenshots: `DEBUG_MODE = false`
  in `solution/Extension/background.js`.

## Notes For Report

- Q2 should cite screenshot numbers and explain who receives the data.
- Q3 should translate payload fields into privacy risks without publishing
  stable identifiers.
- Q4 and Q5 should use browser architecture, not only the screenshots.
- Redacted service-worker console evidence now exists at
  `screenshots/sanitized-console-evidence.png`; final report can cite Figure 1
  for Criteo-family evidence and Figure 2 for Amazon-family evidence.
