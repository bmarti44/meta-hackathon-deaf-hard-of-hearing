// Client for the site's Muse endpoint (AWS Lambda behind CloudFront at /api/*).
// Contract assumed:
//   GET /api/health                       -> {"ok":true,"model":"muse-spark-1.3"}
//   GET /api/ask?q=...                    -> {"answer":"...","steps":[{"tool","input","output"}],"model":"..."}
//   GET /api/explain?row=<id>&level=parent|researcher -> {"text":"...","model":"..."}
//   GET /api/brief?gen=<id>               -> {"text":"..."}
//   errors: {"error":"..."} with 4xx/5xx. Requests may take up to 60 s.
const TIMEOUT_MS = 60000;

async function call(path, params = {}) {
  const u = new URL(path, location.href);
  for (const [k, v] of Object.entries(params)) if (v != null) u.searchParams.set(k, v);
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), TIMEOUT_MS);
  try {
    const r = await fetch(u.pathname + u.search, { signal: ctl.signal, headers: { Accept: 'application/json' } });
    let body = null;
    try { body = await r.json(); } catch (_) { /* non-JSON error page */ }
    if (!r.ok) {
      const msg = (body && body.error) || (r.status === 429 ? 'Too many questions right now. Please wait a moment and try again.' : `The endpoint returned ${r.status}.`);
      throw Object.assign(new Error(msg), { status: r.status });
    }
    if (body && body.error) throw new Error(body.error);
    return body;
  } catch (e) {
    if (e.name === 'AbortError') throw new Error('Muse took longer than 60 seconds. Please try again.');
    throw e;
  } finally { clearTimeout(t); }
}

export const api = {
  async health() {
    try {
      const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 6000);
      const r = await fetch('/api/health', { signal: ctl.signal }); clearTimeout(t);
      if (!r.ok) return null;
      const j = await r.json(); return j && j.ok ? j : null;
    } catch (_) { return null; }
  },
  ask: q => call('/api/ask', { q }),
  explain: (row, level) => call('/api/explain', { row, level }),
  brief: gen => call('/api/brief', { gen })
};

// Minimal "markdown-lite": paragraphs, **bold**, `code`, line-start "- " bullets. Escapes HTML first.
export function mdLite(s) {
  const esc = String(s || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const blocks = esc.trim().split(/\n{2,}/);
  return blocks.map(b => {
    const lines = b.split('\n');
    if (lines.every(l => /^\s*[-*] /.test(l))) return '<ul>' + lines.map(l => '<li>' + inline(l.replace(/^\s*[-*] /, '')) + '</li>').join('') + '</ul>';
    return '<p>' + inline(lines.join('<br>')) + '</p>';
  }).join('');
  function inline(t) { return t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/`([^`]+)`/g, '<code class="mono">$1</code>'); }
}
