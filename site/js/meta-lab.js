// "Can a computer understand the voice better after our cleanup?"
// Reads precomputed results from data/meta/listen.json (built by research/meta/listen_wer.py).
// Muse Spark (Meta) transcribed each clip once, offline; nothing is sent to Meta from the browser.
(() => {
  const $ = id => document.getElementById(id);
  const root = $("ml"); if (!root) return;
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const words = s => String(s || "").toLowerCase().replace(/[’]/g, "'").replace(/[^a-z0-9' ]+/g, " ").split(/\s+/).map(w => w.replace(/^'+|'+$/g, "")).filter(Boolean);

  // Align the transcript to what was said; return the transcript's words marked right or wrong,
  // and how many of the reader's words were heard correctly.
  function align(ref, hypText) {
    const r = words(ref), raw = String(hypText || "").split(/\s+/).filter(Boolean), h = raw.map(w => words(w).join(" "));
    const n = r.length, m = h.length, D = Array.from({ length: n + 1 }, (_, i) => { const a = new Array(m + 1).fill(0); a[0] = i; return a; });
    for (let j = 1; j <= m; j++) D[0][j] = j;
    for (let i = 1; i <= n; i++) for (let j = 1; j <= m; j++)
      D[i][j] = Math.min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (r[i - 1] === h[j - 1] ? 0 : 1));
    const ok = new Array(m).fill(false); let i = n, j = m, hits = 0;
    while (i > 0 && j > 0) {
      if (r[i - 1] === h[j - 1] && D[i][j] === D[i - 1][j - 1]) { ok[j - 1] = true; hits++; i--; j--; }
      else if (D[i][j] === D[i - 1][j - 1] + 1) { i--; j--; }
      else if (D[i][j] === D[i][j - 1] + 1) j--;
      else i--;
    }
    return { html: raw.map((w, k) => ok[k] || !h[k] ? esc(w) : `<span class="ml-miss">${esc(w)}</span>`).join(" "), hits, total: n };
  }

  const loud = snr => snr < 0 ? "the crowd is louder than the voice" : "the crowd is as loud as the voice";
  let data = null;

  function show(i) {
    const c = data.clips[i];
    document.querySelectorAll("#ml-list button").forEach((b, k) => b.setAttribute("aria-pressed", String(k === i)));
    $("ml-ref").textContent = c.reference;
    for (const [side, key] of [["before", "unproc"], ["after", "gen19"]]) {
      const a = $(`ml-a-${side}`); a.pause(); a.src = c[key].audio;
      const t = c[key].transcript;
      if (t == null) { $(`ml-t-${side}`).textContent = "(This one did not get through to Muse, so there is nothing to show.)"; $(`ml-s-${side}`).textContent = ""; continue; }
      const none = /^\s*\[unintelligible\]\s*$/i.test(t);
      const al = align(c.reference, none ? "" : t);
      $(`ml-t-${side}`).innerHTML = none ? "<em>Muse said it could not make out any words.</em>" : (al.html || "<em>(nothing)</em>");
      $(`ml-s-${side}`).innerHTML = `<b class="ml-big">${al.hits}</b> <span class="ml-of">of ${al.total} words right</span>`;
    }
  }

  // Only one player at a time.
  ["ml-a-before", "ml-a-after"].forEach((id, k, ids) => $(id).addEventListener("play", () => $(ids[1 - k]).pause()));

  fetch("data/meta/listen.json", { cache: "no-cache" }).then(r => r.ok ? r.json() : Promise.reject(r.status)).then(d => {
    data = d;
    $("ml-list").innerHTML = d.clips.map((c, i) =>
      `<li><button type="button" aria-pressed="false" data-i="${i}"><span class="ml-n">${String(i + 1).padStart(2, "0")}</span>` +
      `<span class="ml-what">“${esc(c.reference.split(" ").slice(0, 6).join(" "))}…”</span>` +
      `<span class="ml-how">${c.seconds} s · ${loud(c.snr_db)}</span></button></li>`).join("");
    $("ml-list").addEventListener("click", e => { const b = e.target.closest("button[data-i]"); if (b) show(+b.dataset.i); });

    const s = d.summary, rows = Object.entries(s).filter(([k]) => /dB$/.test(k));
    const P = d.plain || {}, share = o => o && o.words_total ? Math.round(100 * o.words_right / o.words_total) : null;
    $("ml-total").innerHTML = rows.map(([k, v]) => {
      const p = P[k] || {}, b4 = share(p.unproc), af = share(p.gen19);
      const verdict = v.better > v.worse ? `Muse did better after the cleanup on ${v.better} of ${v.n} recordings, and worse on ${v.worse}.`
        : v.better < v.worse ? `So here the cleanup did not help Muse: it did better on ${v.better} of ${v.n} recordings and worse on ${v.worse}.`
        : `It was a draw: Muse did better on ${v.better} of ${v.n} recordings and worse on ${v.worse}.`;
      return `<p><span class="ml-label">All ${v.n} recordings, when ${loud(parseFloat(k))}</span>` +
        (b4 != null ? `Before cleanup, Muse got <b>${b4}%</b> of the reader's words right. After cleanup, <b>${af}%</b>. ` : "") + verdict + `</p>`;
    }).join("") + (share(P.clean?.clean) != null ? `<p class="small muted">For comparison, with no crowd at all Muse got ${share(P.clean.clean)}% of the words right.</p>` : "");

    const m = d.meta, f = x => (x >= 0 ? "+" : "") + (100 * x).toFixed(1);
    $("ml-research").innerHTML = `<p>Exploratory, descriptive check, not a registered KPI (plan written before results: <code class="mono">research/meta/plan.md</code>). ` +
      `Recognizer: <code class="mono">${esc(m.recognizer)}</code>; <code class="mono">muse-voice-transcribe-1.0</code> is listed but had no reachable endpoint. ` +
      `Enhancer: Gen 19 seed 17 (<code class="mono">${esc(m.checkpoint)}</code>). ${m.n_clips_in_study} crowd mixtures (8 to 12 babble draws, test speakers only), whole utterances, one transcription each. ` +
      rows.map(([k, v]) => `${k}: WER ${f(v.unproc_mean_wer)}% unprocessed vs ${f(v.gen19_mean_wer)}% Gen 19, paired Δ ${f(v.delta_gen19_minus_unproc.mean)} pp (95% CI ${f(v.delta_gen19_minus_unproc.ci_lo)} to ${f(v.delta_gen19_minus_unproc.ci_hi)}).`).join(" ") +
      (s.clean ? ` Clean-speech WER ${f(s.clean.mean_wer)}%.` : "") + ` Spark often replies as if no audio was attached, so every clip starts with a short clean check sentence (LibriSpeech ${esc(m.delivery_check_utterance || "")}, a non-test speaker); a reply counts only if Muse writes that sentence back, and only the rest is scored (${s.attempts_total} calls for ${m.n_clips_in_study * 2 + (s.clean?.n || 0)} transcripts, ${s.transcripts_failed} missing). Two earlier runs had broken protocols and are filed, not used; a post-hoc rescore strips check-sentence words that spilled onto the clip line (plan amendment 3). The six recordings shown are, per reader, the first with both transcripts present (chosen on availability, not outcome). Independent review by Muse Wonder (<code class="mono">muse-wonder-1.0</code>): <code class="mono">research/meta/wonder_review.md</code>.</p>`;
    root.hidden = false; $("ml-fallback").remove(); {
      const hits = (c, k) => { const t = c[k] && c[k].transcript; if (t == null || /^\s*\[unintelligible\]\s*$/i.test(t)) return -1; return align(c.reference, t).hits; };
      let best = -1, bi = 0;
      data.clips.forEach((c, i) => { const gain = hits(c, "gen19") - hits(c, "unproc"); const pref = (c.snr_db === 0 ? 1 : 0); const sc = gain * 10 + pref; if (gain > 0 && sc > best) { best = sc; bi = i; } });
      show(bi);
    }
    // styled play buttons instead of the native players
    for (const side of ["before", "after"]) {
      const a = $(`ml-a-${side}`); if (!a) continue; a.removeAttribute("controls"); a.style.display = "none";
      const b = document.createElement("button"); b.type = "button"; b.className = "ml-play"; b.textContent = side === "before" ? "Listen before cleanup" : "Listen after cleanup"; b.setAttribute("aria-pressed", "false");
      a.after(b);
      b.addEventListener("click", () => { document.querySelectorAll("#meta-lab audio").forEach(o => { if (o !== a) o.pause(); }); if (a.paused) { a.play().catch(() => {}); } else { a.pause(); } });
      a.addEventListener("play", () => { b.textContent = "Pause"; b.setAttribute("aria-pressed", "true"); });
      const off = () => { b.textContent = side === "before" ? "Listen before cleanup" : "Listen after cleanup"; b.setAttribute("aria-pressed", "false"); };
      a.addEventListener("pause", off); a.addEventListener("ended", off);
    }
  }).catch(() => { $("ml-fallback").textContent = "The listening test could not be loaded right now."; });
})();
