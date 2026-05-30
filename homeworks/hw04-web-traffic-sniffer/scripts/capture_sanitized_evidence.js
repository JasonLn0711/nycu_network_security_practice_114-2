#!/usr/bin/env node
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");

const port = process.env.HW4_REMOTE_DEBUGGING_PORT || "9222";
const base = `http://127.0.0.1:${port}`;
const repoDir = path.join(__dirname, "..");
const screenshotsDir = path.join(repoDir, "evidence", "screenshots");
const rawLocalDir = path.join(repoDir, "evidence", "raw-local");
const targetUrl = process.argv[2] || "https://dictionary.cambridge.org/";
const waitMs = Number(process.env.HW4_CAPTURE_WAIT_MS || "25000");

let nextId = 1;

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`${url} -> ${response.status}`);
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
      data.error ? reject(new Error(JSON.stringify(data.error))) : resolve(data.result);
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
    const promise = new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
    ws.send(JSON.stringify({ id, method, params }));
    return promise;
  }

  return { ws, ready, send, events };
}

function argText(arg) {
  return arg?.value ?? arg?.description ?? "";
}

function methodAndHost(label) {
  const match = label.match(/\[HW4 sniffer\]\s+(\w+)\s+([^\s]+)/);
  if (!match) return null;
  return { method: match[1], host: match[2] };
}

function family(host) {
  if (host.includes("criteo")) return "criteo";
  if (host.includes("amazon") || host.includes("aps.amazon")) return "amazon";
  return "other";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function propertiesFor(worker, objectId) {
  if (!objectId) return null;
  const result = await worker.send("Runtime.getProperties", {
    objectId,
    ownProperties: true,
    accessorPropertiesOnly: false,
    generatePreview: true,
  });
  const object = {};
  for (const prop of result.result || []) {
    if (!prop.enumerable) continue;
    object[prop.name] = prop.value?.value ?? prop.value?.description ?? prop.value?.type ?? null;
  }
  return object;
}

function sanitizeShapeValue(value) {
  if (value === null || value === undefined) return "null";
  if (Array.isArray(value)) return value.length === 0 ? [] : ["array"];
  if (typeof value === "object") return sanitizeShapeObject(value);
  if (
    typeof value === "string" &&
    ["string", "number", "boolean", "null", "[redacted-string]", "[nested]"].includes(value)
  ) {
    return value;
  }
  if (typeof value === "string" && /^https?:\/\//.test(value)) return "[redacted-url]";
  if (typeof value === "string") return value.length > 0 ? "string" : "empty-string";
  return typeof value;
}

function sanitizeShapeObject(object) {
  const sanitized = {};
  for (const [key, value] of Object.entries(object || {})) {
    sanitized[key] = sanitizeShapeValue(value);
  }
  return sanitized;
}

async function main() {
  const targets = await fetchJson(`${base}/json/list`);
  const workerTarget = targets.find(
    (target) => target.type === "service_worker" && target.url.endsWith("/background.js")
  );
  const pageTarget = targets.find((target) => target.type === "page");
  assert(workerTarget, "HW4 background.js service worker target not found");
  assert(pageTarget, "page target not found");

  const worker = connect(workerTarget.webSocketDebuggerUrl);
  await worker.ready;
  await worker.send("Runtime.enable");

  const page = connect(pageTarget.webSocketDebuggerUrl);
  await page.ready;
  await page.send("Page.enable");
  await page.send("Page.navigate", { url: targetUrl });

  await new Promise((resolve) => setTimeout(resolve, waitMs));

  const records = [];
  let current = null;
  let expecting = null;

  for (const event of worker.events.filter((item) => item.method === "Runtime.consoleAPICalled")) {
    const params = event.params || {};
    const text = (params.args || []).map(argText).join(" ");
    const labelInfo = methodAndHost(text);

    if (labelInfo) {
      current = {
        label: text,
        method: labelInfo.method,
        host: labelInfo.host,
        family: family(labelInfo.host),
        metadata: {},
        queryShape: {},
        payloadShape: {},
      };
      records.push(current);
      expecting = null;
      continue;
    }

    if (!current) continue;

    if (params.type === "table" && params.args?.[0]?.objectId) {
      current.metadata = await propertiesFor(worker, params.args[0].objectId);
      continue;
    }

    if (text.includes("Query parameters:")) {
      expecting = "queryShape";
      continue;
    }

    if (text.includes("Sanitized payload shape for report screenshots:")) {
      expecting = "payloadShape";
      continue;
    }

    if (expecting && params.args?.[0]?.objectId) {
      current[expecting] = sanitizeShapeObject(await propertiesFor(worker, params.args[0].objectId));
      expecting = null;
    }
  }

  const selected = [];
  for (const wanted of ["criteo", "amazon"]) {
    const record = records.find((item) => item.family === wanted);
    if (record) selected.push(record);
  }
  for (const record of records) {
    if (selected.length >= 3) break;
    if (!selected.includes(record)) selected.push(record);
  }

  assert(selected.length >= 2, "expected at least two advertiser evidence records");

  fs.mkdirSync(screenshotsDir, { recursive: true });
  fs.mkdirSync(rawLocalDir, { recursive: true });
  fs.writeFileSync(
    path.join(rawLocalDir, "sanitized-evidence-records.json"),
    JSON.stringify({ targetUrl, waitMs, selected, totalRecords: records.length }, null, 2)
  );

  const sections = selected
    .map((record, index) => {
      const metadata = record.metadata || {};
      return `
        <section class="console-card">
          <div class="caption">Figure ${index + 1}. Sanitized service worker console evidence</div>
          <div class="line label">${escapeHtml(record.label)}</div>
          <div class="grid">
            <div><span>hostname</span>${escapeHtml(record.host)}</div>
            <div><span>method</span>${escapeHtml(record.method)}</div>
            <div><span>filterReason</span>${escapeHtml(metadata.filterReason || "advertising-host-allowlist")}</div>
            <div><span>payloadType</span>${escapeHtml(metadata.payloadType || "query/body payload")}</div>
          </div>
          <pre>query parameters shape:
${escapeHtml(JSON.stringify(record.queryShape || {}, null, 2))}

sanitized payload shape:
${escapeHtml(JSON.stringify(record.payloadShape || {}, null, 2))}</pre>
          <p class="note">Values are redacted; domain, field names, data types, and payload structure are preserved.</p>
        </section>
      `;
    })
    .join("\n");

  const html = `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    body { margin: 0; background: #f4f6f8; color: #17202a; font-family: Arial, "Noto Sans TC", sans-serif; }
    main { width: 1120px; padding: 28px; }
    h1 { font-size: 28px; margin: 0 0 8px; }
    .sub { color: #4a5568; margin-bottom: 20px; }
    .console-card { background: #111827; color: #d1d5db; border-radius: 8px; padding: 18px; margin: 0 0 18px; }
    .caption { color: #93c5fd; font-weight: 700; margin-bottom: 10px; }
    .line { color: #f9fafb; font-family: "DejaVu Sans Mono", monospace; font-size: 15px; margin-bottom: 12px; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 14px; }
    .grid div { background: #1f2937; border: 1px solid #374151; border-radius: 6px; padding: 8px; font-size: 13px; overflow-wrap: anywhere; }
    .grid span { display: block; color: #9ca3af; font-size: 11px; text-transform: uppercase; margin-bottom: 4px; }
    pre { background: #0b1020; border: 1px solid #374151; border-radius: 6px; padding: 12px; white-space: pre-wrap; overflow-wrap: anywhere; }
    .note { color: #fbbf24; margin: 10px 0 0; }
  </style>
</head>
<body>
  <main>
    <h1>HW4 Web Traffic Sniffer - Sanitized Console Evidence</h1>
    <div class="sub">Clean profile capture from ${escapeHtml(targetUrl)}. Raw local evidence is ignored; this screenshot preserves only domains, field names, data types, and payload structure.</div>
    ${sections}
  </main>
</body>
</html>`;

  const htmlPath = path.join(screenshotsDir, "sanitized-console-evidence.html");
  const pngPath = path.join(screenshotsDir, "sanitized-console-evidence.png");
  fs.writeFileSync(htmlPath, html);

  const renderPage = await fetchJson(`${base}/json/new?${encodeURIComponent(`file://${htmlPath}`)}`, {
    method: "PUT",
  });
  const render = connect(renderPage.webSocketDebuggerUrl);
  await render.ready;
  await render.send("Page.enable");
  await new Promise((resolve) => setTimeout(resolve, 1000));
  const screenshot = await render.send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: true,
  });
  fs.writeFileSync(pngPath, Buffer.from(screenshot.data, "base64"));
  render.ws.close();

  const markdown = selected
    .map(
      (record, index) =>
        `| Figure ${index + 1} | \`${record.host}\` | \`${record.metadata?.payloadType || "query/body"}\` | \`${record.metadata?.filterReason || "advertising-host-allowlist"}\` | Values redacted; structure preserved |`
    )
    .join("\n");
  fs.writeFileSync(
    path.join(screenshotsDir, "sanitized-console-evidence.md"),
    `# Sanitized Console Evidence\n\n![Sanitized console evidence](sanitized-console-evidence.png)\n\n| Figure | Domain | Payload type | Filter reason | Redaction |\n| --- | --- | --- | --- | --- |\n${markdown}\n`
  );

  console.log("OK: sanitized evidence captured.");
  console.log(`Records observed: ${records.length}`);
  console.log(`Evidence PNG: ${pngPath}`);
  console.log(`Evidence Markdown: ${path.join(screenshotsDir, "sanitized-console-evidence.md")}`);

  worker.ws.close();
  page.ws.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
