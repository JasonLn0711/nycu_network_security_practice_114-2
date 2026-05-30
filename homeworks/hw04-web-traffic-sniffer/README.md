# HW04 - Web Traffic Sniffer

This directory is the canonical archive and working area for Network Security
Practice HW4, **Web Traffic Sniffer**.

## Source Materials

| File | Role |
| --- | --- |
| [raw/hw04-web-traffic-sniffer-spec.pdf](raw/hw04-web-traffic-sniffer-spec.pdf) | Official assignment PDF exported from the course platform |
| [raw/hw04-web-traffic-sniffer-example.zip](raw/hw04-web-traffic-sniffer-example.zip) | Official starter ZIP |
| [starter/example/manifest.json](starter/example/manifest.json) | Extracted Manifest V3 starter manifest |
| [starter/example/background.js](starter/example/background.js) | Extracted starter service worker |
| [solution/Extension/](solution/Extension/) | Working extension implementation with filtering and payload decoding |
| [docs/redaction-rules.md](docs/redaction-rules.md) | Evidence redaction rules before report export |
| [docs/clean-browser-profile.md](docs/clean-browser-profile.md) | Clean browser profile capture protocol |
| [docs/technical-implementation-plan.md](docs/technical-implementation-plan.md) | End-to-end technical implementation, evidence, report, and packaging plan |
| [docs/postdoc-researcher-execution-audit.md](docs/postdoc-researcher-execution-audit.md) | Postdoc-level implementation audit, overlooked controls, and final review protocol |
| [docs/experiment-log.md](docs/experiment-log.md) | Detailed experiment steps, commands, logs, metrics, evidence inventory, and reproducibility protocol |
| [docs/artifact-manifest.json](docs/artifact-manifest.json) | SHA-256 and size manifest for source, evidence, report, and final package artifacts |
| [scripts/validate_submission.py](scripts/validate_submission.py) | Submission dry-run structure verifier |

Original platform filenames:

- `SL-[2026 NS] Web Traffic Sniffer-210526-010145.pdf`
- `example.zip`

## Course Platform Facts

- Course: `【114 Spring】535607網路安全實務-攻擊與防禦 Network Security Practices-Attack and defense`
- Assignment: `HW4. Web Traffic Sniffer`
- Opened: `2026-05-21 00:00`
- Due: `2026-06-14 23:59`
- Submission status at import: no submission made yet
- Grading status at import: not graded

## Assignment Focus

The homework asks students to build a Chrome Extension / Microsoft Edge
extension using Manifest V3. The extension monitors browser background traffic
with `chrome.webRequest.onBeforeRequest`, filters relevant advertising-network
requests, decodes raw request payloads into readable JSON or strings, and uses
the captured evidence to analyze privacy exposure in real-world web traffic.

The target browsing scenario in the official spec is Cambridge Dictionary. The
evaluation browser is Microsoft Edge.

## Grading Contract

| Area | Weight | Evidence |
| --- | ---: | --- |
| Extension implementation | 40% | Traffic filtering and decoded logging |
| Report | 60% | Six written answers with screenshots and analysis |

Implementation requirements:

- Traffic filtering: console output should focus on relevant requests.
- Data decoding and logging: capture and display complete payloads for at
  least two advertising networks, such as Amazon and Criteo.
- Payload readability: decoded output should be inspectable as JSON or a clear
  raw string.

Report questions:

1. Explain the code, including `chrome.webRequest.onBeforeRequest`, domain
   filtering, and raw request-body decoding.
2. Provide screenshots of console output and explain who receives the data and
   what data is sent.
3. Assess privacy and security risks if the captured data leaks.
4. Explain whether HTTPS protects users from malicious browser extensions.
5. Explain how browser extensions may bypass a website's Content Security
   Policy.
6. Describe one malicious extension attack vector and one mitigation.

## Submission Note

The official PDF labels the assignment as HW4 but states the zipped submission
directory as `HW6_{student_ID}`. Preserve that source wording when preparing
submission evidence, and confirm the final folder name against the course
platform before upload.

Expected structure from the PDF:

```text
HW6_{student_ID}/
├── Extension/
│   ├── manifest.json
│   └── background.js
└── {student_ID}_report.pdf
```

## Working Area

Recommended local working paths:

- `solution/Extension/` for the implemented extension.
- `report/` for report drafts, screenshots, and the final PDF.
- `evidence/` for captured console screenshots or sanitized logs.

Keep raw official files under `raw/` unchanged. Put personal implementation,
report, and evidence in separate working folders so the source materials remain
easy to verify.

## Controlled Evidence Capture

Treat this assignment as a controlled privacy evidence capture task. Use the
clean browser profile protocol, keep raw captures in ignored local storage, move
only redacted screenshots into tracked evidence, and use normal-mode extension
logging for final report screenshots.
