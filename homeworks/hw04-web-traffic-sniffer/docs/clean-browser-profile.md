# Clean Browser Profile Protocol

The HW4 traffic capture should run in a clean browser profile so the evidence
represents a controlled homework scenario rather than the user's everyday
browsing state.

## Profile Location

Use a local, ignored profile directory:

```text
evidence/raw-local/edge-profile/
```

This path is ignored through `evidence/.gitignore`.

## Launch Command

Use the helper script from the homework directory:

```bash
scripts/launch-clean-profile.sh
```

The script looks for Microsoft Edge first, then Chromium or Chrome, then a
Playwright-managed Chromium binary under `~/.cache/ms-playwright`. It starts a
new browser process with:

- `--user-data-dir=evidence/raw-local/edge-profile`
- `--no-first-run`
- `--disable-sync`
- `--load-extension=solution/Extension`
- `--remote-debugging-port=9222`
- `--no-sandbox` only when the fallback Playwright Chromium binary needs it on
  the local Linux test host

The remote debugging port allows command-line smoke checks against the clean
profile without using the daily browser profile.

After the clean profile opens, confirm the extension appears in
`edge://extensions/` or `chrome://extensions/`. If the browser does not auto-load
the extension, enable Developer mode and load:

```text
solution/Extension/
```

## Capture Protocol

1. Open the clean profile.
2. Load only the HW4 extension.
3. Open the extension service worker console.
4. Visit Cambridge Dictionary.
5. Navigate a small number of dictionary pages to trigger ad traffic.
6. Save unredacted local captures only under `evidence/raw-local/`.
7. Move only redacted screenshots and sanitized notes into tracked evidence.

## Report Statement

Use this scope statement in the report:

> Traffic evidence was captured in a clean browser profile created for this
> homework. The profile was used only for the Cambridge Dictionary scenario and
> the HW4 extension, which keeps the evidence aligned with a controlled privacy
> observation context.
