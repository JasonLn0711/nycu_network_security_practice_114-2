const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");

const extensionDir = path.join(__dirname, "..", "solution", "Extension");
const source = fs.readFileSync(path.join(extensionDir, "background.js"), "utf8");

const listeners = [];
const context = {
  console,
  URL,
  URLSearchParams,
  TextDecoder,
  Array,
  Object,
  Boolean,
  chrome: {
    webRequest: {
      onBeforeRequest: {
        addListener(listener, filter, extraInfoSpec) {
          listeners.push({ listener, filter, extraInfoSpec });
        },
      },
    },
  },
};

vm.createContext(context);
vm.runInContext(source, context, { filename: "background.js" });

assert.equal(listeners.length, 1, "background registers one onBeforeRequest listener");
assert.deepEqual(JSON.parse(JSON.stringify(listeners[0].filter)), { urls: ["<all_urls>"] });
assert.deepEqual(Array.from(listeners[0].extraInfoSpec), ["requestBody"]);

function rawBody(text) {
  return [{ bytes: new TextEncoder().encode(text).buffer }];
}

function request(overrides) {
  return {
    requestId: "r1",
    method: "POST",
    url: "https://aax.amazon-adsystem.com/e/dtb/bid?slot=top",
    tabId: 1,
    initiator: "https://dictionary.cambridge.org",
    requestBody: {
      raw: rawBody('{"page":"dictionary","slot":"top"}'),
    },
    ...overrides,
  };
}

let decision = context.shouldLogRequest(request({}));
assert.equal(decision.shouldLog, true);
assert.equal(decision.reason, "advertising-host-allowlist");

decision = context.shouldLogRequest(
  request({
    url: "https://dictionary.cambridge.org/static/app.js",
  })
);
assert.equal(decision.shouldLog, false);
assert.equal(decision.reason, "static-resource");

decision = context.shouldLogRequest(
  request({
    url: "https://example.com/collect",
  })
);
assert.equal(decision.shouldLog, false);
assert.equal(decision.reason, "not-advertising-allowlist");

decision = context.shouldLogRequest(
  request({
    method: "GET",
    url: "https://criteo.com/track?uid=abc&event=view",
    requestBody: undefined,
  })
);
assert.equal(decision.shouldLog, true);
assert.equal(decision.reason, "advertising-host-allowlist");

let payload = context.decodePayload(request({}));
assert.equal(payload.type, "json");
assert.deepEqual(JSON.parse(JSON.stringify(payload.value)), { page: "dictionary", slot: "top" });

payload = context.decodePayload(
  request({
    requestBody: {
      raw: rawBody("uid=abc&event=view&event=bid"),
    },
  })
);
assert.equal(payload.type, "urlEncodedForm");
assert.deepEqual(JSON.parse(JSON.stringify(payload.value)), { uid: "abc", event: ["view", "bid"] });

payload = context.decodePayload(
  request({
    requestBody: {
      formData: { slot: ["top"], page: ["dictionary"] },
    },
  })
);
assert.equal(payload.type, "formData");
assert.deepEqual(payload.value, { slot: ["top"], page: ["dictionary"] });

payload = context.decodePayload(
  request({
    requestBody: {
      raw: rawBody("opaque-binary-ish-string"),
    },
  })
);
assert.equal(payload.type, "rawString");
assert.equal(payload.value, "opaque-binary-ish-string");

const parsedUrl = new URL("https://criteo.com/track?uid=abc&event=view");
assert.deepEqual(JSON.parse(JSON.stringify(context.queryParameters(parsedUrl))), {
  uid: "abc",
  event: "view",
});

console.log("OK: extension filtering and decoder logic tests passed.");
