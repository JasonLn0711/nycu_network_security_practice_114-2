# HW04 Safety And Packaging Checklist

This checklist maps the controlled privacy evidence-capture requirements to
repo evidence and verification commands.

| Requirement | Status | Repo evidence | Verification |
| --- | --- | --- | --- |
| 1. Clean test browser profile | Runtime-smoked | `docs/clean-browser-profile.md`, `scripts/launch-clean-profile.sh`, ignored path `evidence/raw-local/edge-profile/` | Script launched a clean profile with Playwright Chromium fallback, auto-loaded `solution/Extension/`, exposed remote debugging on port 9222, and navigated to Cambridge Dictionary. |
| 2. Redaction rules before screenshots | Done | `docs/redaction-rules.md` | Rules cover cookies, session IDs, account IDs, stable identifiers, location, IPs, auth material, and opaque IDs. |
| 3. Raw/sanitized evidence separation | Done | `evidence/.gitignore`, `evidence/README.md`, `evidence/screenshots/.gitkeep`, `evidence/traffic-observations.md` | `git check-ignore` confirms `evidence/raw-local/` is ignored. |
| 4. Avoid Amazon/Criteo-only dependency | Done | `solution/Extension/background.js`, `docs/filtering-and-decoding-contract.md` | The allowlist includes Amazon, Criteo, and additional observed/common ad-tech host families; debug mode supports candidate discovery. |
| 5. Debug mode / normal mode | Done | `solution/Extension/background.js` | `DEBUG_MODE = false` is the final normal mode; toggling to `true` enables candidate discovery. |
| 6. Prove filtering exists | Done | `solution/Extension/background.js`, `docs/filtering-and-decoding-contract.md`, `report/report.md` | Filtering parses hostname, excludes static resources, requires payload evidence, and matches the ad-tech allowlist. |
| 7. Non-JSON payload handling | Done | `solution/Extension/background.js` | Decoder handles `formData`, JSON, URL-encoded form, raw strings, and query parameters. |
| 8. Browser architecture explanation | Done | `report/report.md` | Q4 draft explains HTTPS transit protection versus browser-internal extension visibility. |
| 9. CSP privilege-boundary explanation | Done | `report/report.md` | Q5 draft frames CSP through extension permissions and browser privilege boundaries. |
| 10. Submission dry run | Done | `scripts/build_submission_dry_run.sh`, `scripts/validate_submission.py`, `submission/README.md`, `submission/final/HW6_513559004.zip` | Final ZIP validates required files, PDF header, and absence of local artifacts. The PDF labels the root folder `HW6_{student_ID}` while E3 labels the assignment HW4; the package follows the PDF structure and the discrepancy is documented. |

## Verified Commands

```bash
node --check homeworks/hw04-web-traffic-sniffer/solution/Extension/background.js
node homeworks/hw04-web-traffic-sniffer/scripts/test_extension_logic.js
node homeworks/hw04-web-traffic-sniffer/scripts/runtime_smoke.js
python3 -m json.tool homeworks/hw04-web-traffic-sniffer/solution/Extension/manifest.json
homeworks/hw04-web-traffic-sniffer/scripts/build_submission_dry_run.sh 513559004
python3 homeworks/hw04-web-traffic-sniffer/scripts/validate_submission.py --student-id 513559004 --package-dir homeworks/hw04-web-traffic-sniffer/submission/final/HW6_513559004 --zip homeworks/hw04-web-traffic-sniffer/submission/final/HW6_513559004.zip
git check-ignore -v homeworks/hw04-web-traffic-sniffer/evidence/raw-local/edge-profile
git check-ignore -v homeworks/hw04-web-traffic-sniffer/submission/dry-run/HW6_513559004.zip
```

## Final Evidence

The runtime smoke gate produced ignored raw-local evidence and sanitized
tracked evidence:

- Clean profile: `evidence/raw-local/edge-profile/` (ignored)
- Runtime summary: `evidence/raw-local/runtime-smoke-summary.json` (ignored)
- Sanitized console evidence: `evidence/screenshots/sanitized-console-evidence.png`
- Report PDF: `report/513559004_report.pdf`
- Final package: `submission/final/HW6_513559004.zip`

The final report cites the sanitized evidence and answers all six official
questions. Raw payload values, local browser profile state, and local runtime
summaries remain outside tracked evidence.
