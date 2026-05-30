# Filtering And Decoding Contract

The extension implementation uses a two-mode workflow that supports discovery
without weakening the final evidence.

## Normal Mode

`DEBUG_MODE = false`

Normal mode is the submission mode. It logs requests only when:

1. the request URL can be parsed,
2. the path is not a static resource,
3. the request has payload evidence through a request body or query parameters,
   and
4. the hostname matches the advertising-network allowlist.

This proves traffic filtering exists and keeps the report screenshots focused.

## Debug Mode

`DEBUG_MODE = true`

Debug mode is a development-only observation mode. It can log candidate
requests with request bodies so the allowlist can be updated when the current
Cambridge Dictionary ad stack differs from the examples in the PDF.

Final screenshots should use normal mode. Debug mode can be mentioned in the
report as a development aid.

## Decoder Fallbacks

The decoder handles the payload forms likely to appear in ad-tech requests:

1. `requestBody.formData`
2. raw body decoded as UTF-8 JSON
3. raw body decoded as URL-encoded form data
4. raw body decoded as a readable string
5. empty body with query parameters shown separately

This fallback order supports Amazon/Criteo-like examples while staying robust
when the live ad network payload format changes.
