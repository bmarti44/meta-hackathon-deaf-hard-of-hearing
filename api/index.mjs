// beforetheimplant.com AI endpoint: Muse (Meta's model) via the api.meta.ai Responses API.
// Pattern reused from itsthemedium.com: the API key lives in SSM Parameter Store (SecureString)
// and is read only here, server-side. CloudFront serves this under /api/* (OAC-signed Lambda URL).
// Routes (all GET, JSON):
//   /api/health                          {"ok":true,"model":...}
//   /api/ask?q=...                       Muse agent over the research record, with its tool steps
//   /api/explain?row=<id>&level=parent|researcher   one scorecard row or generation, explained
//   /api/brief?gen=<id>                  short brief of one generation
// Muse only sees the research through knowledge.json (built by api/build_knowledge.py from committed files).
// Direct-invoke only (no rawPath, never reachable via CloudFront):
//   {mode:"review", prompt, effort}      Muse Spark second reviewer
//   {mode:"wonder", prompt, effort}      Muse Wonder (muse-wonder-1.0) independent reviewer
//   {mode:"listen", wav_b64}             Muse Spark transcribes one LibriSpeech research clip (research/meta/)
//   {mode:"meta", method, path, body|form}  authenticated passthrough for API discovery
//   {mode:"ws", query, send, waitMs}     realtime WebSocket probe
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

function plainName(f) {
  const m = String(f).match(/gen(\d+)\/(results|prereg|astra[^/]*|muse[^/]*)\.md$/);
  if (m) return m[2] === "results" ? `version ${+m[1]}'s results` : m[2] === "prereg" ? `version ${+m[1]}'s plan` : `a review of version ${+m[1]}`;
  if (/SUBMISSION\.md$/.test(f)) return "the project summary";
  if (/KPI\.md$/.test(f)) return "how the 14 checks work";
  if (/GOAL\.md$/.test(f)) return "why this project exists";
  if (/code-audit|review/.test(f)) return "an independent review";
  return "a project note";
}

function runTool(name, args) {
  if (name === "list_generations") return { step: "Read the list of every version we tried", data: K.generations };
  if (name === "get_scorecard") return { step: "Read the 14 checks and how the model did on each", data: K.scorecard };
  if (name === "search_record") {
    const q = String(args.query || "").slice(0, 120), r = search(q);
    const names = [...new Set(r.map(x => plainName(x.file)))];
    return { step: `Read ${names.join(", ")}`, data: r };
  }
  return { step: null, data: { error: "unknown tool" } };
}

const CONTEXT = `PROJECT: "Before the Implant" (beforetheimplant.com), a hackathon research entry.\n${K.facts}\n\nSTORY: ${K.story}\n\nCURRENT VERDICT: ${K.scorecard.verdict}.`;
const RULES = `Rules you must follow:
- Every number you give must come from a tool result or the context above. Never invent numbers, dates, ages or personal details about Graham or his family.
- Focus only on what the result MEANS, explained like the reader is five: short sentences, everyday words. Explain directly; avoid cute analogies (bikes, video games, building blocks, homework, training wheels). Be really clear.
- Write short, natural sentences a parent would say out loud. No padded or stacked phrasing ("would additionally need with", "has not yet earned a listening test with..."). Do not bring up listening tests unless asked; if you must, say "It has not been tried with listeners yet." once, then say what the next step is. Never explain a thing by restating it ("could not try it because it has not been tried"). Avoid odd phrases like "grown ups watching closely"; say "with an audiologist in charge".
- Write about the voice and what a listener would notice, never about "the tests" being cleaner ("the voice came through 1.2 dB cleaner", not "the program made computer tests cleaner").
- Never describe an error or a loss as "small" or "tiny"; give the number and say plainly whether it is better or worse. Say "the voice came through 1.2 dB cleaner", not "made how clean the voice is better by +1.19 dB". Round to one decimal place for dB.
- Do NOT add caveat lists or "what it does not mean" sections, and do not tack on reminders about testing, real listeners, promotion or the scorecard verdict; a fixed footnote about verifying on the Nucleus 6 is added after your answer automatically. Just never claim it already helps a real listener or beats the Nucleus 6.
- Never add care, medical or audiologist caveats of any kind (a fixed footnote is added automatically). If someone asks about a specific person's own hearing care, answer only what the research shows. Do not use disclaimers, legal language or the phrase "medical advice".
- Always write full, friendly sentences; never shorthand fragments. Never mention file names, paths or internal labels.
- Failures and nulls are part of the result: report them plainly.
- Write in simple, everyday words anyone can follow, unless asked for researcher detail. No em dashes.
- Never use these technical words unless the reader asks for researcher detail; use the plain version instead: "parameters" -> "about 600,000 numbers"; "causal" -> "uses only sound that has already happened"; "oracle" or "non-causal" -> "a version that cheats by hearing the future"; "loss" or "loss function" -> "how the model is scored while it learns"; "SI-SDR" -> "how clean the voice is"; "STOI" -> "how easy the speech is to understand"; "seed" -> "training run"; "bench" or "in-silico" -> "computer tests"; "Gen 22" -> "version 22"; "ms" -> "thousandths of a second". Say "dB" only with a plain explanation; the "every 3 dB cuts the leftover noise in half" explanation applies only to noise-cleanup numbers, not to direction clues (for those, dB is how much louder the sound is in one ear than the other).
- Never open with "This row", "This check" or similar; start directly with what it means for a listener.
- Never use the words FAIL, PASS, promoted, verdict or 'keep optimizing'; describe results in plain words ("it reached the goal" / "it fell short of the goal").
- Call the model "the program" (never "the helper" or "the AI"). Always keep apostrophes ("Graham's", "parents'").
- Always give units with numbers (for example "5.47 dB"). Call the 14 tests "checks", never "rows". Only if consent or trying it with Graham comes up, use the site's wording: "That would only happen with an audiologist in charge, his parents' permission and Graham's own agreement." Mention the Nucleus 6 only if the question is about it.`;

const askPrompt = q => ({
  instructions: `You answer questions about a cochlear-implant noise-reduction research project, using tools that read its committed research record.\n\n${CONTEXT}\n\n${RULES}
- Prefer one to three tool calls. Use get_scorecard for KPI questions, list_generations for history, search_record for details.
- If the question has nothing to do with this project, hearing, cochlear implants or how to read the site, do not call tools; reply in one sentence that you can only answer questions about this project.
Final answer: under 170 words of Markdown, in full, friendly sentences (no shorthand fragments). Lead with a direct one-sentence answer, then supporting detail. Never mention file names or paths.`,
  input: `Question: ${q}`, max: 520, tools: true,
});

function explainPrompt(item, kind, level, label = "") {
  const who = level === "researcher"
    ? "Write for a speech/hearing researcher: precise, terse, with the exact numbers and what would change the verdict. Under 120 words."
    : "Write for a parent of a child with cochlear implants: explain it like they are five: warm, very plain words, no jargon (explain any term you must use in a few words), under 90 words. Say clearly what it means. Nothing about what it does not mean.";
  return {
    instructions: `You explain one item from a cochlear-implant noise-reduction research project.\n\n${CONTEXT}\n\n${RULES}\n${who}`,
    input: `${label ? `On the site, the reader clicked Explain next to this text: "${label}". Do not repeat or quote that text; talk about it in your own plain words, and never use internal ids.\n` : ""}Explain this ${kind}:\n${JSON.stringify(item)}`, max: 700, tools: false,
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
  // de-duplicate identical step lines (several searches can read the same notes)
  const seen = new Set();
  steps = steps.filter(st => (seen.has(st.output) ? false : (seen.add(st.output), true)));
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

// Muse Spark as a listener: upload a WAV to /files, then pass it as input_audio by file_id.
// (muse-voice-transcribe-1.0 is listed by /models but no endpoint accepts it as of 2026-11-04; see research/meta/plan.md.)
const LISTEN_INSTRUCTIONS = "You are a speech transcriber. Write down exactly the words spoken by the main talker in the audio, in order, as plain text. Write only words you actually hear. Never guess, complete, continue or tidy up a sentence. If a stretch is too unclear to make out, skip it. If you cannot make out any words at all, reply with exactly [unintelligible]. Output only the transcript.";
async function listen(wavB64, prompt) {
  const key = await getKey();
  const fd = new FormData();
  fd.append("purpose", "user_data");
  fd.append("file", new Blob([Buffer.from(wavB64, "base64")], { type: "audio/wav" }), "clip.wav");
  const up = await fetch(`${BASE}/files`, { method: "POST", body: fd, headers: { authorization: `Bearer ${key}`, "x-client-id": "beforetheimplant:listen" } });
  if (!up.ok) throw new Error(`files ${up.status} ${(await up.text()).slice(0, 200)}`);
  const file = await up.json();
  // Spark intermittently answers as if no audio were attached (about half of identical calls on 2026-11-04);
  // those replies are detected and retried, and the attempt count is returned so the caller can disclose it.
  const NO_AUDIO = /(no audio|audio (file )?(was|is) not|not (see|have|detect|find|hear)[^.]{0,40}audio|upload|attach|unable to transcribe|can(no|')t transcribe|cannot transcribe|provide the audio)/i;
  const tries = [];
  for (let attempt = 1; attempt <= 6; attempt++) {
    const r = await respond({ model: MODEL, store: false, max_output_tokens: 5000, reasoning: { effort: "low" },
      input: [{ role: "user", content: [{ type: "input_text", text: prompt || LISTEN_INSTRUCTIONS }, { type: "input_audio", file_id: file.id }] }] });
    const tag = `[${r.status}${r.incomplete_details?.reason ? "/" + r.incomplete_details.reason : ""} out=${r.usage?.output_tokens}] `;
    const text = textOf(r.output).trim();
    if (text && !NO_AUDIO.test(text)) return { model: MODEL, file_id: file.id, attempts: attempt, text, tries };
    tries.push(tag + text.slice(0, 240));
  }
  return { model: MODEL, file_id: file.id, attempts: 6, text: null, error: "audio not received", tries };
}

export const handler = async (event) => {
  // Direct-invoke only: transcribe one LibriSpeech-derived research clip with Muse Spark (research/meta/listen_wer.py).
  if (!event.rawPath && event.mode === "listen" && typeof event.wav_b64 === "string" && event.wav_b64.length < 5_000_000) {
    return await listen(event.wav_b64, typeof event.prompt === "string" ? event.prompt.slice(0, 2000) : null);
  }
  // Direct-invoke only: Muse Wonder (muse-wonder-1.0, Meta's deeper reasoning model) as an independent reviewer.
  if (!event.rawPath && event.mode === "wonder" && typeof event.prompt === "string") {
    const effort = ["low", "medium", "high", "max"].includes(event.effort) ? event.effort : "high";
    const r = await respond({ model: "muse-wonder-1.0", store: false, max_output_tokens: 16000, reasoning: { effort },
      instructions: "You are an independent scientific reviewer of an in-silico speech-enhancement research project for cochlear-implant users. Be concrete, skeptical and concise. Recompute any arithmetic you can from the data given. Say plainly what the evidence does and does not support. Never claim benefit for a real listener.",
      input: event.prompt.slice(0, 120000) });
    return { model: "muse-wonder-1.0", effort, status: r.status, text: textOf(r.output) };
  }
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
  if (!event.rawPath && event.mode === "meta" && /^\/[a-z0-9_\/.:-]+(\?[a-z0-9_=&.:-]*)?$/i.test(String(event.path || ""))) {
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
    const raw = String(qs.context || "").replace(/[^\p{L}\p{N} ,.'()%+\-−:/]/gu, "").slice(0, 120).trim();
    const label = /\p{L}{4,}/u.test(raw) ? raw : "";  // ignore labels that are only a number and a unit
    p = explainPrompt(item, ROWS.has(id) ? "scorecard check" : "research generation", level, label); kind = "explain";
  } else if (path.endsWith("/brief")) {
    const g = GENS.get(String(qs.gen || "").trim());
    if (!g) return json(400, { error: "Unknown generation." });
    p = briefPrompt(g); kind = "brief";
    if (g.status === "running" || g.status === "drafted") cache = 600;
  } else return json(404, { error: "Unknown route." });
  if (limited(ip, kind)) return { ...json(429, { error: "Too many requests. Please wait a couple of minutes." }), headers: { ...json(429, {}).headers, "retry-after": "120" } };
  const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 55000);
  try {
    let r = await runMuse(p, ctl.signal);
    if (!r.answer) { console.error("muse empty answer, retrying once", kind); r = await runMuse(p, ctl.signal); }
    if (!r.answer) throw new Error("empty response");
    const out = r.answer + "\n\n*Still needs to be verified on the Nucleus 6.";  // owner request: one fixed footnote, no caveat lists
    return json(200, kind === "ask" ? { answer: out, steps: r.steps, model: MODEL } : { text: out, model: MODEL }, cache);
  } catch (e) {
    console.error("muse error", kind, e?.message);
    return json(502, { error: "Muse is busy right now. Please try again in a moment." });
  } finally { clearTimeout(timer); }
};
