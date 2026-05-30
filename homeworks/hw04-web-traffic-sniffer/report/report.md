# HW4 Web Traffic Sniffer Report

Student ID: 513559004

## 1. Code Analysis

The extension uses Manifest V3 with a background service worker. The service
worker registers `chrome.webRequest.onBeforeRequest` with the `requestBody`
option so it can inspect outgoing request bodies before the browser sends the
request.

The filtering path parses each request URL, checks the hostname against the
advertising-network allowlist, excludes static resources, and requires a request
body for normal-mode logging. Debug mode is available only for development
candidate discovery; final evidence uses normal mode.

The decoder first handles `formData`, then raw UTF-8 JSON, then URL-encoded
form data, then readable raw strings. Query parameters are shown separately so
requests with empty bodies still have inspectable structure when needed.

## 2. Evidence Of Results

Screenshots:

- Figure 1: Criteo-family request in `evidence/screenshots/sanitized-console-evidence.png`
- Figure 2: Amazon ad-system request in `evidence/screenshots/sanitized-console-evidence.png`
- Figure 3: DoubleClick ad-tech request in `evidence/screenshots/sanitized-console-evidence.png`

Advertiser/domain observations:

| Figure | Receiver | Payload type | Data sent |
| --- | --- | --- | --- |
| Figure 1 | `gum.criteo.com` | query payload | page-context and auction-related fields such as `origin`, `topUrl`, `domain`, and `bundle`; values redacted |
| Figure 2 | `web-banner.ads.aps.amazon-adsystem.com` | JSON body | structured ad request body; values redacted |
| Figure 3 | `cm.g.doubleclick.net` | query payload | URL context field; value redacted |

Identifiers were redacted according to `docs/redaction-rules.md`; domain names,
field names, data types, and payload structure remain visible for grading.

## 3. Privacy Risk Assessment

The captured payloads can support browsing-interest inference because the
advertising network can associate page context, identifiers, and request timing.
If stable IDs or session material leak, the receiver may connect dictionary
lookup behavior with a larger cross-site advertising profile.

## 4. HTTPS Analysis

HTTPS protects traffic while it travels across the network. A browser extension
with `webRequest` permission sits inside the browser privilege boundary, so it
can observe request metadata and bodies at the browser layer before network
transit encryption is the only relevant control. This is different from an
external network attacker: the extension is not breaking HTTPS on the wire; it
is operating with browser-granted visibility inside the client.

## 5. Content Security Policy

CSP constrains what a web page can load or execute inside the page context.
Browser extensions operate through a separate extension permission model. When
a user grants extension permissions, extension APIs and content scripts can
observe or interact with browser/page state in ways that are not equivalent to
ordinary page JavaScript. The security question is therefore extension privilege
and permission stewardship, not simply a website CSP configuration issue.

## 6. Attack Vectors And Mitigation

Example attack vector:

- Cookie theft, keylogging, ad injection, or form-data capture.

Mitigation:

- Use least-privilege extension permissions, review extension publishers and
  requested permissions, apply enterprise extension allowlists where available,
  separate sensitive browsing into dedicated profiles, and remove extensions
  that do not need broad host permissions.
