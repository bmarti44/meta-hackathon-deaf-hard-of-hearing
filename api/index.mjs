// beforetheimplant.com AI endpoint: Muse (Meta's model) via the api.meta.ai Responses API.
// Pattern reused from itsthemedium.com: the API key lives in SSM Parameter Store (SecureString)
// and is read only here, server-side. CloudFront serves this under /api/* (OAC-signed Lambda URL).
// Routes (all GET, JSON):
//   /api/health                          {"ok":true,"model":...}
//   /api/ask?q=...                       Muse agent over the research record, with its tool steps
//   /api/explain?row=<id>&level=parent|researcher   one scorecard row or generation, explained
//   /api/brief?gen=<id>                  short brief of one generation
// Muse only sees the research through knowledge.json (built by api/build_knowledge.py from committed files).
import { readFileSync } from "node:fs";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";

const MODEL = process.env.MUSE_MODEL || "muse-spark-1.3";
const EFFORT = process.env.MUSE_EFFORT || "low";
const BASE = process.env.MUSE_BASE || "https://api.meta.ai/v1";
const PARAM = process.env.KEY_PARAM || "/itsthemedium/muse-api-key";
const K = JSON.parse(readFileSync(new URL("./knowledge.json", import.meta.url)));
const GENS = new Map(K.generations.map(g => [g.id, g]));
const ROWS = new Map(K.scorecard.rows.map(r => [r.id, r]));

let keyPromise = null;
function getKey() {
  if (!keyPromise) {
    keyPromise = new SSMClient({}).send(new GetParameterCommand({ Name: PARAM, WithDecryption: true }))
      .then(r => r.Parameter.Value.trim())
      .catch(e => { keyPromise = null; throw e; });
  }
  return keyPromise;
}

const hits = new Map();
const LIMITS = { ask: 30, explain: 150, brief: 150 };
function limited(ip, kind) {
  const now = Date.now(), win = 10 * 60 * 1000, key = kind + "|" + ip;
  const arr = (hits.get(key) || []).filter(t => now - t < win);
  arr.push(now); hits.set(key, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > LIMITS[kind];
}

/* ---------- tools: Muse's only window onto the research ---------- */
const TOOLS = [
  { type: "function", name: "list_generations",
    description: "List every research generation (Gen 16 to Gen 24): the one change it tested, its status (baseline, null, fail, running, drafted...) and its headline result.",
    parameters: { type: "object", properties: {}, additionalProperties: false } },
  { type: "function", name: "get_scorecard",
    description: "The 14 required KPI scorecard rows for the accepted baseline (Gen 19, 3-seed means): name, actual value, requirement, pass/fail, plus the disclosures.",
    parameters: { type: "object", properties: {}, additionalProperties: false } },
  { type: "function", name: "search_record",
    description: "Keyword search over the committed research record (submission summary, results, pre-registrations, independent reviews, KPI contract, motivation). Returns the best-matching passages with their file paths. Use it for any detail not in the other tools.",
    parameters: { type: "object", properties: { query: { type: "string", description: "A few keywords, e.g. \"gradient clipping cap\" or \"fresh-material confirmation\"" } }, required: ["query"], additionalProperties: false } },
];

const tok = s => (String(s).toLowerCase().match(/[a-z0-9]+(?:[.-][a-z0-9]+)*/g) || []).filter(w => w.length > 1);
const DF = new Map();
const DOCS = K.docs.map(d => { const t = tok(d.heading + " " + d.text); new Set(t).forEach(w => DF.set(w, (DF.get(w) || 0) + 1)); return { ...d, t }; });
function search(q) {
  const qs = [...new Set(tok(q))], N = DOCS.length;
  const scored = DOCS.map(d => {
    let s = 0;
    for (const w of qs) { const tf = d.t.filter(x => x === w).length; if (tf) s += (1 + Math.log(tf)) * Math.log(1 + N / (DF.get(w) || 1)); }
    return [s, d];
  }).filter(x => x[0] > 0).sort((a, b) => b[0] - a[0]).slice(0, 4);
  return scored.map(([, d]) => ({ file: d.file, heading: d.heading, text: d.text.slice(0, 1100) }));
}

function runTool(name, args) {
  if (name === "list_generations") return { step: "Listed all research generations", data: K.generations };
  if (name === "get_scorecard") return { step: "Read the 14-row KPI scorecard", data: K.scorecard };
  if (name === "search_record") {
    const q = String(args.query || "").slice(0, 120), r = search(q);
    return { step: `Searched the research record for "${q}" (${r.length} passages: ${[...new Set(r.map(x => x.file))].join(", ") || "none"})`, data: r };
  }
  return { step: null, data: { error: "unknown tool" } };
}

const CONTEXT = `PROJECT: "Before the Implant" (beforetheimplant.com), a hackathon research entry.\n${K.facts}\n\nSTORY: ${K.story}\n\nCURRENT VERDICT: ${K.scorecard.verdict}.`;
const RULES = `Rules you must follow:
- Every number you give must come from a tool result or the context above. Never invent numbers, dates, ages or personal details about Graham or his family.
- Focus only on what the result MEANS, explained like the reader is five: short sentences, everyday words, one simple picture or comparison if it helps. Be really clear.
- Do NOT add caveat lists or "what it does not mean" sections, and do not tack on reminders about testing, real listeners, promotion or the scorecard verdict; a fixed footnote about verifying on the Nucleus 6 is added after your answer automatically. Just never claim it already helps a real listener or beats the Nucleus 6.
- If asked about a person's own hearing, implant settings or care, say in one friendly sentence that their audiologist is the right person for that, then explain what the research does show. Do not use disclaimers, legal language or the phrase "medical advice".
- Failures and nulls are part of the result: report them plainly.
- Write in simple, everyday words anyone can follow, unless asked for researcher detail. No em dashes.`;

const askPrompt = q => ({
  instructions: `You answer questions about a cochlear-implant noise-reduction research project, using tools that read its committed research record.\n\n${CONTEXT}\n\n${RULES}
- Prefer one to three tool calls. Use get_scorecard for KPI questions, list_generations for history, search_record for details.
- If the question has nothing to do with this project, hearing, cochlear implants or how to read the site, do not call tools; reply in one sentence that you can only answer questions about this project.
Final answer: under 170 words of Markdown. Lead with a direct one-sentence answer, then supporting detail. Name the file a key fact comes from when useful.`,
  input: `Question: ${q}`, max: 520, tools: true,
});

function explainPrompt(item, kind, level) {
  const who = level === "researcher"
    ? "Write for a speech/hearing researcher: precise, terse, with the exact numbers and what would change the verdict. Under 120 words."
    : "Write for a parent of a child with cochlear implants: explain it like they are five: warm, very plain words, no jargon (explain any term you must use in a few words), under 90 words. Say clearly what it means. Nothing about what it does not mean.";
  return {
    instructions: `You explain one item from a cochlear-implant noise-reduction research project.\n\n${CONTEXT}\n\n${RULES}\n${who}`,
    input: `Explain this ${kind}:\n${JSON.stringify(item)}`, max: 360, tools: false,
  };
}

const briefPrompt = g => ({
  instructions: `You write a short brief of one research generation.\n\n${CONTEXT}\n\n${RULES}\nFormat: Markdown, under 120 words, explained like the reader is five: **What we changed**, **Why**, **What happened**, **What it means**.`,
  input: `Generation:\n${JSON.stringify(g)}\n\nAll generations for context:\n${JSON.stringify(K.generations)}`, max: 420, tools: false,
});

const scrub = s => s.replace(/\s*—\s*/g, ", ").replace(/(\d)\s*–\s*(\d)/g, "$1 to $2").replace(/\s*–\s*/g, ", ").trim();

async function respond(body, signal) {
  const key = await getKey();
  const res = await fetch(`${BASE}/responses`, {
    method: "POST", signal,
    headers: { authorization: `Bearer ${key}`, "content-type": "application/json", "x-client-id": "beforetheimplant:web" },
    body: JSON.stringify(body),
  });
  if (!res.ok) { const t = await res.text().catch(() => ""); throw new Error(`upstream ${res.status} ${t.slice(0, 200)}`); }
  return res.json();
}
const textOf = out => (out || []).filter(o => o.type === "message" && o.phase !== "commentary")
  .flatMap(o => (o.content || []).filter(c => c.type === "output_text").map(c => c.text)).join("");

async function runMuse(p, signal) {
  const base = { model: MODEL, instructions: p.instructions, store: false, max_output_tokens: p.max + 1600, reasoning: { effort: EFFORT } };
  if (!p.tools) { const r = await respond({ ...base, input: p.input }, signal); return { answer: scrub(textOf(r.output)), steps: [] }; }
  let input = [{ role: "user", content: p.input }], steps = [], answer = "";
  const MAX_ROUNDS = 5;
  for (let round = 0; round < MAX_ROUNDS; round++) {
    if (round === MAX_ROUNDS - 2) input.push({ role: "user", content: "You have enough data. Write the final answer now without calling more tools." });
    const r = await respond({ ...base, input, tools: TOOLS, parallel_tool_calls: true }, signal);
    const out = r.output || [];
    answer = textOf(out) || answer;
    const calls = out.filter(o => o.type === "function_call");
    if (!calls.length) break;
    const results = calls.map(c => {
      let args = {}; try { args = JSON.parse(c.arguments || "{}"); } catch {}
      const t = runTool(c.name, args);
      if (t.step) steps.push({ tool: c.name, input: JSON.stringify(args).slice(0, 120), output: t.step });
      return { type: "function_call_output", call_id: c.call_id, output: JSON.stringify(t.data) };
    });
    input = [...input, ...out.filter(o => o.type !== "message"), ...results];
  }
  return { answer: scrub(answer), steps };
}

const json = (status, obj, cache) => ({
  statusCode: status,
  headers: { "content-type": "application/json; charset=utf-8", "x-content-type-options": "nosniff",
    "cache-control": cache ? `public, max-age=${cache}, s-maxage=${cache}` : "no-store" },
  body: JSON.stringify(obj),
});

// Realtime WebSocket session (Node 22 global WebSocket, undici: accepts { headers }). Collects server events.
function wsSession(key, query, send, waitMs, until, auth) {
  const url = BASE.replace(/^http/, "ws") + "/realtime" + (query ? "?" + query : "");
  return new Promise(resolve => {
    const got = [], t0 = Date.now(); let done = false, ws;
    const finish = why => { if (done) return; done = true; try { ws.close(); } catch {} resolve({ url, why, ms: Date.now() - t0, events: got }); };
    try {
      ws = auth === "protocol"
        ? new WebSocket(url, ["realtime", "openai-insecure-api-key." + key])
        : new WebSocket(url, { headers: { authorization: `Bearer ${key}`, "x-client-id": "beforetheimplant:probe" } });
    } catch (e) { return resolve({ url, why: "ctor " + e.message, events: [] }); }
    const timer = setTimeout(() => finish("timeout"), waitMs);
    ws.onopen = () => { for (const m of send) ws.send(typeof m === "string" ? m : JSON.stringify(m)); };
    ws.onmessage = m => {
      let d; try { d = JSON.parse(m.data); } catch { d = String(m.data).slice(0, 500); }
      got.push(d);
      if (until && d && d.type === until) { clearTimeout(timer); finish("until"); }
      if (d && d.type === "error") { clearTimeout(timer); setTimeout(() => finish("error"), 300); }
    };
    ws.onerror = e => { got.push({ wsError: String(e?.message || e?.error?.message || e?.type || e) }); };
    ws.onclose = e => { clearTimeout(timer); got.push({ closed: e.code, reason: e.reason }); finish("closed"); };
  });
}

export const handler = async (event) => {
  // Direct-invoke only (no rawPath, so never reachable via CloudFront): Muse as a second,
  // independent reviewer of a research verdict. The caller files the verbatim answer.
  if (!event.rawPath && event.mode === "review" && typeof event.prompt === "string") {
    const effort = ["low", "medium", "high"].includes(event.effort) ? event.effort : "high";
    const r = await respond({ model: MODEL, store: false, max_output_tokens: 6000, reasoning: { effort },
      instructions: "You are an independent scientific reviewer of a pre-registered in-silico research loop. Be concrete, skeptical and concise. Check arithmetic against the data given. Never claim clinical benefit.",
      input: event.prompt.slice(0, 60000) });
    return { model: MODEL, effort, text: textOf(r.output) };
  }
  // Direct-invoke only: authenticated passthrough to the Meta API for model discovery/testing by the
  // project's own IAM principals (key stays server-side; never reachable via CloudFront).
  if (!event.rawPath && event.mode === "meta" && /^\/[a-z0-9_\/.:-]+$/i.test(String(event.path || ""))) {
    const key = await getKey();
    // Optional multipart body: event.form = { field: "text" | { b64, filename, type } } (e.g. audio uploads).
    let mp = null;
    if (event.method === "POST" && event.form && typeof event.form === "object") {
      mp = new FormData();
      for (const [k, v] of Object.entries(event.form)) {
        if (v && typeof v === "object" && v.b64) mp.append(k, new Blob([Buffer.from(v.b64, "base64")], { type: v.type || "application/octet-stream" }), v.filename || "file");
        else mp.append(k, String(v));
      }
    }
    const headers = { authorization: `Bearer ${key}`, "x-client-id": "beforetheimplant:probe" };
    if (!mp) headers["content-type"] = "application/json";
    const res = await fetch(`${BASE}${event.path}`, {
      method: event.method === "POST" ? "POST" : "GET", headers,
      body: event.method === "POST" ? (mp || JSON.stringify(event.body || {})) : undefined,
    });
    const text = await res.text();
    let body; try { body = JSON.parse(text); } catch { body = text.slice(0, 20000); }
    return { status: res.status, body };
  }
  // Direct-invoke only: realtime (WebSocket) session against the Meta API, e.g. muse-voice-transcribe-1.0.
  // event = { mode:"ws", query:"model=...", send:[{...event}], waitMs, until:"event.type" }. Returns received events.
  if (!event.rawPath && event.mode === "ws" && /^[a-z0-9_=&.:-]*$/i.test(String(event.query || ""))) {
    const key = await getKey();
    return await wsSession(key, String(event.query || ""), Array.isArray(event.send) ? event.send : [],
      Math.min(Number(event.waitMs) || 15000, 120000), event.until ? String(event.until) : null, event.auth || "header");
  }
  const path = (event.rawPath || "").replace(/\/+$/, "");
  const qs = event.queryStringParameters || {};
  const ip = (event.headers?.["cloudfront-viewer-address"] || event.requestContext?.http?.sourceIp || "").split(":")[0];
  if ((event.requestContext?.http?.method || "GET") !== "GET") return json(405, { error: "Use GET." });
  if (path.endsWith("/health")) {
    let ok = false; try { ok = !!(await getKey()); } catch { ok = false; }
    return json(200, { ok, model: MODEL });
  }
  let p, kind, cache = 604800;
  if (path.endsWith("/ask")) {
    const q = String(qs.q || "").replace(/[\u0000-\u001f]/g, " ").replace(/\s+/g, " ").trim().slice(0, 300);
    if (q.length < 3) return json(400, { error: "Please ask a question." });
    p = askPrompt(q); kind = "ask"; cache = 86400;
  } else if (path.endsWith("/explain")) {
    const id = String(qs.row || "").trim(), level = qs.level === "researcher" ? "researcher" : "parent";
    const item = ROWS.get(id) || GENS.get(id);
    if (!item) return json(400, { error: "Unknown scorecard row or generation." });
    p = explainPrompt(item, ROWS.has(id) ? "scorecard row" : "research generation", level); kind = "explain";
  } else if (path.endsWith("/brief")) {
    const g = GENS.get(String(qs.gen || "").trim());
    if (!g) return json(400, { error: "Unknown generation." });
    p = briefPrompt(g); kind = "brief";
    if (g.status === "running" || g.status === "drafted") cache = 600;
  } else return json(404, { error: "Unknown route." });
  if (limited(ip, kind)) return { ...json(429, { error: "Too many requests. Please wait a couple of minutes." }), headers: { ...json(429, {}).headers, "retry-after": "120" } };
  const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 55000);
  try {
    const r = await runMuse(p, ctl.signal);
    if (!r.answer) throw new Error("empty response");
    const out = r.answer + "\n\n*Still needs to be verified on the Nucleus 6.";  // owner request: one fixed footnote, no caveat lists
    return json(200, kind === "ask" ? { answer: out, steps: r.steps, model: MODEL } : { text: out, model: MODEL }, cache);
  } catch (e) {
    console.error("muse error", kind, e?.message);
    return json(502, { error: "Muse is busy right now. Please try again in a moment." });
  } finally { clearTimeout(timer); }
};
