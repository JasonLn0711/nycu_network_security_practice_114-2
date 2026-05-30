const DEBUG_MODE = false;

// HW4 controlled evidence capture:
// normal mode logs only ad-tech allowlist requests with payload evidence;
// debug mode is for candidate-domain discovery and should be off for submission.

const TARGET_PAGE_HOST_PATTERNS = [
  "cambridge.org",
  "dictionary.cambridge.org",
];

const AD_TECH_HOST_PATTERNS = [
  // Official examples from the assignment.
  "amazon-adsystem.com",
  "aax.amazon-adsystem.com",
  "aps.amazon.com",
  "criteo.com",
  "criteo.net",

  // Observed/common ad-tech bidding, sync, and measurement families.
  "bidr.io",
  "doubleclick.net",
  "googlesyndication.com",
  "googleadservices.com",
  "openx.net",
  "pubmatic.com",
  "rubiconproject.com",
  "rlcdn.com",
  "scorecardresearch.com",
  "taboola.com",
  "adnxs.com",
  "adsrvr.org",
];

const STATIC_RESOURCE_EXTENSIONS = [
  ".css",
  ".gif",
  ".ico",
  ".jpg",
  ".jpeg",
  ".js",
  ".map",
  ".png",
  ".svg",
  ".ttf",
  ".woff",
  ".woff2",
];

function parseUrl(url) {
  try {
    return new URL(url);
  } catch (error) {
    return null;
  }
}

function hostMatches(hostname, patterns) {
  return patterns.some((pattern) => hostname === pattern || hostname.endsWith(`.${pattern}`));
}

function hasStaticResourcePath(pathname) {
  const normalizedPath = pathname.toLowerCase();
  return STATIC_RESOURCE_EXTENSIONS.some((extension) => normalizedPath.endsWith(extension));
}

function hasRequestBody(details) {
  return Boolean(
    details.requestBody &&
      ((details.requestBody.raw && details.requestBody.raw.length > 0) ||
        details.requestBody.formData)
  );
}

function hasQueryParameters(parsedUrl) {
  return Array.from(parsedUrl.searchParams.keys()).length > 0;
}

function shouldLogRequest(details) {
  const parsedUrl = parseUrl(details.url);
  if (!parsedUrl) {
    return { shouldLog: false, reason: "invalid-url" };
  }

  const isAdTechHost = hostMatches(parsedUrl.hostname, AD_TECH_HOST_PATTERNS);
  const isTargetPageHost = hostMatches(parsedUrl.hostname, TARGET_PAGE_HOST_PATTERNS);

  if (hasStaticResourcePath(parsedUrl.pathname)) {
    return { shouldLog: false, reason: "static-resource" };
  }

  const hasPayloadEvidence = hasRequestBody(details) || hasQueryParameters(parsedUrl);

  if (isAdTechHost && hasPayloadEvidence) {
    return {
      shouldLog: true,
      reason: "advertising-host-allowlist",
      parsedUrl,
      isAdTechHost,
      isTargetPageHost,
    };
  }

  if (!hasPayloadEvidence) {
    return {
      shouldLog: DEBUG_MODE && isAdTechHost,
      reason: "no-body-or-query-payload",
      parsedUrl,
      isAdTechHost,
      isTargetPageHost,
    };
  }

  if (DEBUG_MODE) {
    return {
      shouldLog: true,
      reason: isTargetPageHost ? "debug-target-page-host" : "debug-candidate-request",
      parsedUrl,
      isAdTechHost,
      isTargetPageHost,
    };
  }

  return {
    shouldLog: false,
    reason: "not-advertising-allowlist",
    parsedUrl,
    isAdTechHost,
    isTargetPageHost,
  };
}

function decodeRawChunks(rawChunks) {
  const decoder = new TextDecoder("utf-8");
  return rawChunks
    .map((chunk) => {
      if (!chunk.bytes) {
        return "";
      }
      return decoder.decode(chunk.bytes, { stream: false });
    })
    .join("");
}

function objectFromUrlSearchParams(rawString) {
  if (!rawString.includes("=")) {
    return null;
  }

  const params = new URLSearchParams(rawString);
  const decoded = {};
  let count = 0;

  for (const [key, value] of params.entries()) {
    count += 1;
    if (Object.prototype.hasOwnProperty.call(decoded, key)) {
      if (!Array.isArray(decoded[key])) {
        decoded[key] = [decoded[key]];
      }
      decoded[key].push(value);
    } else {
      decoded[key] = value;
    }
  }

  return count > 0 ? decoded : null;
}

function decodePayload(details) {
  if (!details.requestBody) {
    return {
      type: "none",
      value: null,
      rawString: "",
    };
  }

  if (details.requestBody.formData) {
    return {
      type: "formData",
      value: details.requestBody.formData,
      rawString: "",
    };
  }

  if (!details.requestBody.raw || details.requestBody.raw.length === 0) {
    return {
      type: "empty",
      value: null,
      rawString: "",
    };
  }

  const rawString = decodeRawChunks(details.requestBody.raw);
  const trimmed = rawString.trim();

  if (!trimmed) {
    return {
      type: "emptyRawBody",
      value: "",
      rawString,
    };
  }

  try {
    return {
      type: "json",
      value: JSON.parse(trimmed),
      rawString,
    };
  } catch (error) {
    const formLike = objectFromUrlSearchParams(trimmed);
    if (formLike) {
      return {
        type: "urlEncodedForm",
        value: formLike,
        rawString,
      };
    }
  }

  return {
    type: "rawString",
    value: rawString,
    rawString,
  };
}

function queryParameters(parsedUrl) {
  const params = {};
  for (const [key, value] of parsedUrl.searchParams.entries()) {
    params[key] = value;
  }
  return params;
}

function payloadShape(value, depth = 0) {
  if (depth > 3) {
    return "[nested]";
  }

  if (value === null) {
    return "null";
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return [];
    }
    return [`array<${typeof value[0]}>`];
  }

  if (typeof value === "object") {
    const shaped = {};
    for (const [key, nestedValue] of Object.entries(value).slice(0, 24)) {
      shaped[key] = payloadShape(nestedValue, depth + 1);
    }
    return shaped;
  }

  if (typeof value === "string") {
    if (value.length > 24 || /[A-Za-z0-9_-]{16,}/.test(value)) {
      return "[redacted-string]";
    }
    return "string";
  }

  return typeof value;
}

function logRequest(details, decision) {
  const payload = decodePayload(details);
  const metadata = {
    requestId: details.requestId,
    method: details.method,
    url: details.url,
    hostname: decision.parsedUrl.hostname,
    initiator: details.initiator || "(not provided)",
    tabId: details.tabId,
    filterReason: decision.reason,
    payloadType: payload.type,
  };

  console.groupCollapsed(`[HW4 sniffer] ${metadata.method} ${metadata.hostname}`);
  console.table(metadata);

  const query = queryParameters(decision.parsedUrl);
  if (Object.keys(query).length > 0) {
    console.log("Query parameters:");
    console.dir(query);
  }

  console.log("Decoded payload:");
  console.dir(payload.value);

  console.log("Sanitized payload shape for report screenshots:");
  console.dir(payloadShape(payload.value));

  if (payload.type !== "json" && payload.rawString) {
    console.log("Raw decoded string:");
    console.log(payload.rawString);
  }

  console.groupEnd();
}

chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    const decision = shouldLogRequest(details);
    if (!decision.shouldLog) {
      return;
    }
    logRequest(details, decision);
  },
  { urls: ["<all_urls>"] },
  ["requestBody"]
);

console.log(
  `[HW4 sniffer] Loaded. mode=${DEBUG_MODE ? "debug" : "normal"}; target=Cambridge Dictionary; filtering=ad-tech allowlist`
);
