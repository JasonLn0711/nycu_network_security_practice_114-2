# Redaction Rules

The report needs enough evidence to show advertiser payload structure, but it
does not need stable personal identifiers or session material.

## Redact Before Commit Or Report Export

Redact these values in screenshots, notes, and report assets:

- cookies
- session IDs
- account IDs, email addresses, names, or profile IDs
- stable browser, device, user, or advertising identifiers
- precise location data
- IP addresses when visible
- authorization headers, API keys, tokens, or bearer strings
- long opaque IDs that can reasonably identify a user or browser session

## Preserve For Grading Evidence

Keep these values visible when safe:

- advertiser domain
- request method
- payload field names
- payload data types
- payload object structure
- high-level Cambridge Dictionary page context
- redaction labels such as `[REDACTED_COOKIE]` or `[REDACTED_SESSION_ID]`

## Sanitized Evidence Standard

Use this transformation pattern:

```text
uid=abc123def456789 -> uid=[REDACTED_STABLE_ID]
cookie=session...   -> cookie=[REDACTED_COOKIE]
email=a@b.example   -> email=[REDACTED_ACCOUNT]
lat=25.0330         -> lat=[REDACTED_PRECISE_LOCATION]
```

The final report should explain that identifiers were redacted while preserving
domain, field-name, field-type, and payload-structure evidence.
