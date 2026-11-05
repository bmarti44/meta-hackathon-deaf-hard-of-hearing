// "How an implant hears": the squeeze animation and the listening row.
// The animation is drawn from real data (assets/audio/implant/electrodogram.json, written by
// site/tools/make_implant_audio.py): a 48-bin spectrum of the sentence flows in from the left,
// is funnelled into the 22 ACE bands, and the 8 loudest bands per 16 ms frame pulse on the right,
// exactly the 8-of-22 selection the vocoder makes. While a clip plays, the picture follows it.
// One clip plays at a time. Reduced motion: one still frame, redrawn only when the clip changes.
(() => {
  const root = document.getElementById('implant');
  if (!root) return;
  const stage = root.querySelector('#imp-stage');
  const canvas = root.querySelector('#imp-canvas');
  const nowEl = root.querySelector('#imp-now');
  const live = root.querySelector('#imp-live');
  const buttons = [...root.querySelectorAll('.imp-play')];
  const ctx = canvas.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DATA_URL = 'assets/audio/implant/electrodogram.json';
  const NB = 48, NE = 22, NMAX = 8;
  const BG = '#090b10';

  // ---------- data ----------
  let meta = null; const sigs = {};
  let cur = 'clean', curTitle = 'The voice, as recorded';
  const b64 = s => { const bin = atob(s), u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u; };
  function prep(d) {
    const env = b64(d.env), spec = b64(d.spec), n = d.frames, sel = new Uint8Array(n * NE), idx = new Array(NE);
    for (let f = 0; f < n; f++) {
      for (let b = 0; b < NE; b++) idx[b] = b;
      idx.sort((a, c) => env[f * NE + c] - env[f * NE + a]);
      for (let k = 0; k < NMAX; k++) if (env[f * NE + idx[k]] > 0) sel[f * NE + idx[k]] = 1;
    }
    return { n, env, spec, sel };
  }
  // spectrum bin -> ACE band (same edges as research/bench-n6/vocoder.py ace_edges())
  const aceEdges = (() => {
    const e = []; for (let i = 0; i < 9; i++) e.push(188 + (1312 - 188) * i / 9);
    for (let i = 0; i < 14; i++) e.push(Math.exp(Math.log(1312) + (Math.log(7938) - Math.log(1312)) * i / 13));
    return e;
  })();
  const binBand = new Uint8Array(NB);
  for (let i = 0; i < NB; i++) {
    const lo = 120 * Math.pow(7900 / 120, i / NB), hi = 120 * Math.pow(7900 / 120, (i + 1) / NB), fc = Math.sqrt(lo * hi);
    let b = 0; while (b < NE - 1 && fc >= aceEdges[b + 1]) b++;
    binBand[i] = b;
  }
  let loading = null;
  function load() {
    if (loading) return loading;
    loading = fetch(DATA_URL).then(r => r.ok ? r.json() : Promise.reject(r.status)).then(j => {
      meta = j; for (const k in j.signals) sigs[k] = prep(j.signals[k]);
      draw(stillT());
    }).catch(() => { stage.hidden = true; });
    return loading;
  }

  // ---------- geometry ----------
  let W = 0, H = 0, dpr = 1, G = null;
  function layout() {
    const r = stage.getBoundingClientRect();
    W = Math.max(1, r.width); H = Math.max(1, r.height);
    dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    const small = W < 600, top = small ? 66 : 70, bot = H - 30;
    const xA1 = W * (small ? 0.38 : 0.42), xE = W * (small ? 0.55 : 0.56);
    G = { top, bot, xA1, xE, small, rowB: (bot - top) / NB, rowE: (bot - top) / NE,
          pxA: Math.max(1.3, xA1 / 190), pxC: Math.max(1.8, (W - xE) / 170) };
    stage.style.setProperty('--imp-b', (xE / W * 100).toFixed(2) + '%');
  }
  const yBin = i => G.bot - (i + 0.5) * G.rowB;
  const yBand = b => G.bot - (b + 0.5) * G.rowE;
  const hash = n => { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); };

  // ---------- drawing ----------
  let focus = reduce ? 1 : 0;
  function draw(t) {
    const S = sigs[cur]; if (!S || !G) return;
    const fs = meta.frame_s, fF = (t - meta.frame_offset_s) / fs, f0 = Math.floor(fF), frac = fF - f0;
    const at = (arr, ch, f, c) => (f < 0 || f >= S.n) ? 0 : arr[f * ch + c] / 255;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
    const blur = (1 - focus) * (1 - focus);

    // A: ridgelines of the arriving spectrum (future flows in from the left toward "now")
    const nA = Math.ceil(G.xA1 / G.pxA), step = G.small ? 2 : 1;
    ctx.lineWidth = 1;
    for (let i = NB - 1; i >= 0; i--) {
      const base = yBin(i), amp = G.rowB * 3.1;
      ctx.beginPath();
      for (let k = 0; k <= nA; k += step) {
        const f = f0 + k, v = at(S.spec, NB, f, i) * (1 - frac) + at(S.spec, NB, f + 1, i) * frac;
        const j = blur * G.rowB * 5 * (hash(i * 977 + f) - 0.5);
        const x = G.xA1 - (k - frac) * G.pxA, y = base - Math.pow(v, 1.7) * amp + j;
        k === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.lineTo(-2, base + 2); ctx.lineTo(G.xA1, base + 2); ctx.closePath();
      ctx.fillStyle = BG; ctx.fill();
      ctx.strokeStyle = `rgba(236,231,220,${(0.22 + 0.5 * focus) * (0.55 + 0.45 * (i / NB))})`;
      ctx.stroke();
    }
    // the "now" hairline
    ctx.fillStyle = 'rgba(95,220,255,0.35)'; ctx.fillRect(G.xA1, G.top - 6, 1, G.bot - G.top + 12);

    // B: funnel, 48 bins squeezed into 22 bands
    const fNow = Math.max(0, Math.min(S.n - 1, f0)), bw = G.xE - G.xA1;
    for (let i = 0; i < NB; i++) {
      const b = binBand[i], v = at(S.spec, NB, fNow, i), on = S.sel[fNow * NE + b];
      const y0 = yBin(i), y1 = yBand(b);
      ctx.beginPath(); ctx.moveTo(G.xA1, y0);
      ctx.bezierCurveTo(G.xA1 + bw * 0.55, y0, G.xE - bw * 0.5, y1, G.xE - 6, y1);
      ctx.strokeStyle = on ? `rgba(95,220,255,${(0.15 + 0.75 * v) * focus})` : `rgba(174,168,155,${(0.06 + 0.22 * v) * focus})`;
      ctx.stroke();
    }

    // electrode column + C: pulse trains on the 8 selected lanes, flowing away to the right
    const nC = Math.ceil((W - G.xE) / G.pxC), sq = Math.max(3, Math.min(8, G.rowE * 0.5)), xC = G.xE + sq + 6;
    for (let b = 0; b < NE; b++) {
      const y = yBand(b);
      ctx.fillStyle = 'rgba(38,44,56,0.9)'; ctx.fillRect(xC, Math.round(y), W - xC, 1);
      const on = S.sel[fNow * NE + b], e = at(S.env, NE, fNow, b);
      if (on) { ctx.fillStyle = `rgba(95,220,255,${(0.55 + 0.45 * e) * focus})`; ctx.fillRect(G.xE - sq / 2, y - sq / 2, sq, sq); }
      else { ctx.strokeStyle = 'rgba(116,110,99,0.7)'; ctx.strokeRect(G.xE - sq / 2 + 0.5, y - sq / 2 + 0.5, sq - 1, sq - 1); }
      for (let k = 0; k < nC; k++) {
        const f = f0 - k; if (f < 0 || f >= S.n || !S.sel[f * NE + b]) continue;
        const lv = S.env[f * NE + b] / 255, age = k / nC;
        const h = G.rowE * 0.8 * (0.2 + 0.8 * lv), x = xC + (k + frac) * G.pxC;
        ctx.fillStyle = `rgba(95,220,255,${Math.pow(1 - age, 1.3) * (0.3 + 0.7 * lv) * focus})`;
        ctx.fillRect(x, y - h / 2, 1, h);
      }
    }
  }

  // ---------- clock ----------
  const audio = new Audio(); audio.preload = 'none';
  let active = null, visible = false, raf = 0, t0 = performance.now(), focusT0 = 0;
  const dur = () => sigs[cur] ? sigs[cur].n * meta.frame_s : 8;
  const stillT = () => (meta ? meta.lead_s : 0.45) + 2.1;
  function tick(ts) {
    raf = 0;
    if (focus < 1) focus = Math.min(1, (ts - focusT0) / 1800);
    const t = (active && !audio.paused) ? audio.currentTime : stillT() + ((ts - t0) / 1000) % Math.max(0.5, dur() - stillT());
    draw(t);
    if (active && !audio.paused && audio.duration) active.style.setProperty('--p', (audio.currentTime / audio.duration).toFixed(4));
    if (visible) raf = requestAnimationFrame(tick);
  }
  function start() { if (!reduce && !raf && visible) raf = requestAnimationFrame(tick); }

  new IntersectionObserver(es => {
    for (const e of es) {
      if (e.isIntersecting) load();
      visible = e.isIntersecting;
      if (visible && !focusT0) focusT0 = performance.now();
      if (visible) start();
    }
  }, { rootMargin: '400px 0px' }).observe(stage);
  new ResizeObserver(() => { layout(); if (reduce || !raf) draw(active && !audio.paused ? audio.currentTime : stillT()); }).observe(stage);
  layout();

  // ---------- listening row ----------
  const mmss = s => `0:${String(Math.floor(s)).padStart(2, '0')}`;
  const titleOf = btn => btn.querySelector('.imp-title').textContent;
  const setState = (btn, txt) => { btn.querySelector('.imp-state').textContent = txt; };
  function showing(btn, playing) {
    nowEl.textContent = '';
    nowEl.append(playing ? 'Playing ' : 'Showing ');
    nowEl.append(titleOf(btn));
    if (!playing) nowEl.append(', replaying without sound');
  }
  function reset(btn) {
    btn.setAttribute('aria-pressed', 'false'); btn.classList.remove('is-loading');
    btn.style.setProperty('--p', 0); setState(btn, 'Listen');
  }
  function stop(announce) {
    if (!active) return;
    const btn = active; audio.pause(); reset(btn); showing(btn, false);
    if (announce) live.textContent = 'Stopped.';
    t0 = performance.now() - audio.currentTime * 1000;
  }
  buttons.forEach(btn => btn.addEventListener('click', () => {
    if (active === btn && !audio.paused) { stop(true); return; }
    if (active) { audio.pause(); reset(active); }
    active = btn; cur = btn.dataset.sig; curTitle = titleOf(btn);
    load();
    btn.classList.add('is-loading'); setState(btn, 'Loading'); btn.setAttribute('aria-pressed', 'true');
    audio.src = btn.dataset.src;
    audio.play().catch(() => { reset(btn); setState(btn, 'Tap again'); });
    if (reduce) draw(stillT());
  }));
  audio.addEventListener('playing', () => {
    if (!active) return;
    active.classList.remove('is-loading'); showing(active, true);
    live.textContent = `Playing: ${curTitle}.`;
    start();
  });
  audio.addEventListener('timeupdate', () => {
    if (!active || audio.paused) return;
    setState(active, `Playing ${mmss(audio.currentTime)}`);
    if (reduce && audio.duration) active.style.setProperty('--p', (audio.currentTime / audio.duration).toFixed(4));
  });
  audio.addEventListener('ended', () => { const b = active; if (!b) return; reset(b); showing(b, false); live.textContent = 'Finished.'; t0 = performance.now(); });
  audio.addEventListener('error', () => { if (active) { reset(active); setState(active, 'Unavailable'); } });
})();
