#!/usr/bin/env node
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const port = process.env.HW4_REMOTE_DEBUGGING_PORT || "9222";
const base = `http://127.0.0.1:${port}`;
const targetUrl = process.argv[2] || "https://dictionary.cambridge.org/";
const waitMs = Number(process.env.HW4_RUNTIME_WAIT_MS || "15000");
const repoDir = path.join(__dirname, "..");
const rawLocalDir = path.join(repoDir, "evidence", "raw-local");

let nextId = 1;

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${url} -> ${response.status}`);
  }
  return response.json();
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  const pending = new Map();
  const events = [];

  ws.addEventListener("message", (message) => {
    const data = JSON.parse(message.data);
    if (data.id && pending.has(data.id)) {
      const { resolve, reject } = pending.get(data.id);
      pending.delete(data.id);
      if (data.error) {
        reject(new Error(JSON.stringify(data.error)));
      } else {
        resolve(data.result);
      }
      return;
    }
    events.push(data);
  });

  const ready = new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  function send(method, params = {}) {
    const id = nextId++;
    const payload = { id, method, params };
    const result = new Promise((resolve, reject) => {
      pending.set(id, { resolve, reject });
    });
    ws.send(JSON.stringify(payload));
    return result;
  }

  return { ws, ready, send, events };
}

async function main() {
  const targets = await fetchJson(`${base}/json/list`);
  const workerTarget = targets.find(
    (target) => target.type === "service_worker" && target.url.endsWith("/background.js")
  );
  assert(workerTarget, "HW4 background.js service worker target not found");

  const pageTarget = targets.find((target) => target.type === "page");
  assert(pageTarget, "page target not found");

  const worker = connect(workerTarget.webSocketDebuggerUrl);
  await worker.ready;
  await worker.send("Runtime.enable");

  const filterResult = await worker.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `shouldLogRequest({
      requestId: "smoke",
      method: "GET",
      url: "https://criteo.com/track?uid=abc&event=view",
      tabId: 1,
      initiator: "https://dictionary.cambridge.org"
    })`,
  });
  assert.equal(filterResult.result.value.shouldLog, true);
  assert.equal(filterResult.result.value.reason, "advertising-host-allowlist");

  const decodeResult = await worker.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `decodePayload({
      requestBody: {
        raw: [{ bytes: new TextEncoder().encode("uid=abc&event=view").buffer }]
      }
    })`,
  });
  assert.equal(decodeResult.result.value.type, "urlEncodedForm");

  const page = connect(pageTarget.webSocketDebuggerUrl);
  await page.ready;
  await page.send("Page.enable");
  await page.send("Page.navigate", { url: targetUrl });

  await new Promise((resolve) => setTimeout(resolve, waitMs));

  const consoleEvents = worker.events.filter((event) => event.method === "Runtime.consoleAPICalled");
  const snifferEvents = consoleEvents.filter((event) =>
    JSON.stringify(event.params || {}).includes("[HW4 sniffer]")
  );
  const snifferLabels = snifferEvents
    .flatMap((event) => event.params?.args || [])
    .map((arg) => arg.value || arg.description || "")
    .filter((value) => value.includes("[HW4 sniffer]"));
  const hostCounts = {};
  for (const label of snifferLabels) {
    const match = label.match(/\[HW4 sniffer\]\s+\w+\s+([^\s]+)/);
    if (!match) {
      continue;
    }
    hostCounts[match[1]] = (hostCounts[match[1]] || 0) + 1;
  }
  const sortedHostCounts = Object.entries(hostCounts).sort((a, b) => b[1] - a[1]);

  fs.mkdirSync(rawLocalDir, { recursive: true });
  fs.writeFileSync(
    path.join(rawLocalDir, "runtime-smoke-summary.json"),
    JSON.stringify(
      {
        targetUrl,
        waitMs,
        consoleEvents: consoleEvents.length,
        snifferEvents: snifferEvents.length,
        hostCounts: Object.fromEntries(sortedHostCounts),
      },
      null,
      2
    )
  );

  console.log("OK: HW4 extension runtime smoke passed.");
  console.log(`Browser target: ${pageTarget.url}`);
  console.log(`Navigated to: ${targetUrl}`);
  console.log(`Console events observed: ${consoleEvents.length}`);
  console.log(`HW4 sniffer console events observed: ${snifferEvents.length}`);
  console.log("HW4 sniffer host counts:");
  for (const [host, count] of sortedHostCounts.slice(0, 20)) {
    console.log(`- ${host}: ${count}`);
  }
  console.log("Raw local summary:");
  console.log(path.join(rawLocalDir, "runtime-smoke-summary.json"));

  worker.ws.close();
  page.ws.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
