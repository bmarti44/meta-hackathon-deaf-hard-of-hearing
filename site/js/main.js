import { api, mdLite } from './api.js';
const C = window.SITE_CONFIG;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fmt = (v, d = 2, sign = true) => (sign && v > 0 ? '+' : '') + Number(v).toFixed(d);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const GLYPH = { baseline: '●', advance: '▲', null: '×', fail: '×', running: '◉', pending: '○' };
const WORD = { baseline: 'baseline', advance: 'advanced', null: 'null', fail: 'fail', running: 'running', pending: 'pending' };

// ---------- brand / repo (one place: js/config.js) ----------
document.title = `${C.brand} — causal noise reduction for cochlear implants, tested on a bench first`;
$$('[data-brand-name]').forEach(e => e.textContent = C.brand);
const repoUrl = p => C.repo ? (p ? `${C.repo}/blob/${C.repoBranch}/${p}` : C.repo) : null;
$$('a[data-repo]').forEach(a => {
  const u = repoUrl(a.dataset.repo);
  if (u) { a.href = u; a.target = '_blank'; a.rel = 'noopener'; } else { a.replaceWith(...a.childNodes); }
});
if (!C.repo) $('#repo-link')?.remove();

// ---------- header / nav ----------
const bar = $('#bar'), nav = $('#chapnav'), menu = $('#menu-btn');
addEventListener('scroll', () => bar.classList.toggle('solid', scrollY > 40), { passive: true });
menu.addEventListener('click', () => { const o = nav.classList.toggle('open'); menu.setAttribute('aria-expanded', o); });
nav.addEventListener('click', e => { if (e.target.tagName === 'A') { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); } });
const secs = $$('main section[id]');
const navObs = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) $$('a', nav).forEach(a => a.setAttribute('aria-current', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-40% 0px -55% 0px' });
secs.forEach(s => navObs.observe(s));
// reveal
const rvo = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); rvo.unobserve(en.target); } }), { threshold: 0.15 });
$$('.rv').forEach(e => rvo.observe(e));
// safety net: anything already on screen (or if the observer never fires) becomes visible
setTimeout(() => $$('.rv:not(.in)').forEach(e => { const r = e.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) e.classList.add('in'); }), 1200);
setTimeout(() => $$('.rv:not(.in)').forEach(e => e.classList.add('in')), 8000);

// ---------- data ----------
const load = p => fetch(p).then(r => { if (!r.ok) throw new Error(p); return r.json(); });
const [model, bench, score, traj, g21, gens] = await Promise.all([
  load('data/model.json'), load('data/bench_snr.json'), load('data/scorecard.json'),
  load('data/val_traj.json'), load('data/gen21_replication.json'), load('data/generations.json')
]);

// ---------- model facts ----------
$$('[data-model="params"]').forEach(e => e.textContent = model.params.toLocaleString('en-US'));
$$('[data-model="latency"]').forEach(e => e.textContent = model.algorithmic_latency_ms_max.toFixed(2));
$$('[data-model="future"]').forEach(e => e.textContent = model.future_samples);
$$('[data-model="prefix"]').forEach(e => e.textContent = model.causality_post_max_prefix_diff.toFixed(1));
$$('[data-model="past"]').forEach(e => e.textContent = model.past_context_s.toFixed(2));
$('#lat-bar').style.width = (model.algorithmic_latency_ms_max / 10 * 100).toFixed(2) + '%';
$$('[data-bench="crowd_d"]').forEach(e => e.textContent = fmt(bench.summary_seed_mean.gen19.crowd.d_sisdr) + ' dB');
$$('[data-bench="snr0"]').forEach(e => e.textContent = fmt(bench.systems.gen19['0']) + ' dB');
$$('[data-bench="snr-5"]').forEach(e => e.textContent = fmt(bench.systems.gen19['-5']) + ' dB');
$$('[data-bench="white_estoi"]').forEach(e => e.textContent = fmt(bench.summary_seed_mean.gen19['white-heldout'].d_voc_estoi, 3));

// ---------- Graham dancing: lazy, in-view autoplay (muted), accessible sound toggle, captions ----------
(function video() {
  const v = $('#dance'), play = $('#v-play'), snd = $('#v-sound'), note = $('#v-note');
  if (!v) return;
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saver = (navigator.connection && navigator.connection.saveData) || innerWidth < 700;
  const src = saver ? 'assets/family/graham-dancing-640.mp4' : 'assets/family/graham-dancing.mp4';  // both versions have sound
  let loaded = false;
  function attach() { if (loaded) return; loaded = true; const s = document.createElement('source'); s.src = src; s.type = 'video/mp4'; v.insertBefore(s, v.firstChild); v.preload = 'metadata'; v.load(); }
  const setPlay = on => { play.textContent = on ? 'Pause' : 'Play'; play.setAttribute('aria-pressed', on); };
  v.addEventListener('play', () => setPlay(true)); v.addEventListener('pause', () => setPlay(false));
  play.addEventListener('click', () => { attach(); v.paused ? v.play().catch(() => {}) : v.pause(); });
  snd.addEventListener('click', () => { attach(); v.muted = !v.muted; const on = !v.muted; snd.innerHTML = on ? '<span aria-hidden="true">♪ </span>Sound on: tap to mute' : '<span aria-hidden="true">♪ </span>Turn sound on'; snd.classList.toggle('is-on', on); snd.setAttribute('aria-pressed', on); snd.setAttribute('aria-label', on ? 'Sound is on. Turn sound off' : 'Sound is off. Turn sound on'); if (on && v.paused) v.play().catch(() => {}); });
  // near the viewport: attach the source; in view: autoplay muted (unless reduced motion); out of view: pause
  new IntersectionObserver(es => { if (es[0].isIntersecting) attach(); }, { rootMargin: '600px 0px' }).observe(v);
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!rm) { attach(); v.play().catch(() => {}); } } else if (!v.paused) v.pause(); }, { threshold: 0.4 }).observe(v);
})();

// ---------- hero film slot: shown only if the file exists ----------
(async function film() {
  const box = $('#film'); if (!box) return;
  try {
    const r = await fetch('assets/video/before-the-implant.mp4', { method: 'HEAD' });
    if (!r.ok) return;
    const v = $('video', box); const s = document.createElement('source'); s.src = 'assets/video/before-the-implant.mp4'; s.type = 'video/mp4'; v.insertBefore(s, v.firstChild);
    box.hidden = false;
    const p = $('#film-play'); p.addEventListener('click', () => { v.preload = 'auto'; v.paused ? v.play().catch(() => {}) : v.pause(); });
    v.addEventListener('play', () => { p.textContent = 'Pause'; p.setAttribute('aria-pressed', 'true'); }); v.addEventListener('pause', () => { p.textContent = 'Play the film'; p.setAttribute('aria-pressed', 'false'); });
    const m = $('#film-sound'); m.addEventListener('click', () => { v.muted = !v.muted; m.textContent = v.muted ? 'Sound: off' : 'Sound: on'; m.setAttribute('aria-pressed', !v.muted); });
  } catch (_) { /* no film yet */ }
})();

// ---------- "What this could mean": direction illustration (idea only, not data) ----------
(function direction() {
  const host = $('#dir-demo'); if (!host) return;
  const W = 520, H = 360, cx = 260, cy = 190;
  const noise = [[70, 70], [450, 60], [470, 300], [90, 310], [260, 40], [250, 335]];
  const voice = [60, 190];
  function draw(mode) {
    // perceived position of the voice: separate per-ear processing can blur the ear-to-ear loudness clue (pulls toward centre)
    const perceived = mode === 'none' ? voice : mode === 'separate' ? [170, 190] : voice;
    const nAlpha = mode === 'none' ? 0.9 : 0.35, vSize = mode === 'none' ? 14 : 20;
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Illustration: a child in the centre of a noisy room, a voice on the left. In 'each ear separately' mode the voice seems to come from nearer the middle; in 'both ears linked' mode it stays on the left.">
      <rect x="20" y="20" width="${W - 40}" height="${H - 40}" rx="18" fill="none" stroke="var(--rule)"/>
      <text x="30" y="${H - 28}" class="lbl dim">top-down room · illustration of the idea, not measured data</text>`;
    noise.forEach(([x, y]) => s += `<circle cx="${x}" cy="${y}" r="10" fill="var(--dim)" opacity="${nAlpha}"/><text x="${x}" y="${y + 24}" text-anchor="middle" class="lbl dim">chatter</text>`);
    // child (head with two ears)
    s += `<circle cx="${cx}" cy="${cy}" r="22" fill="var(--bg3)" stroke="var(--bone)" stroke-width="2"/><circle cx="${cx - 24}" cy="${cy}" r="6" fill="var(--bone)"/><circle cx="${cx + 24}" cy="${cy}" r="6" fill="var(--bone)"/><text x="${cx}" y="${cy + 44}" text-anchor="middle" class="lbl">Graham</text>`;
    // true voice
    s += `<circle cx="${voice[0]}" cy="${voice[1]}" r="${vSize}" fill="var(--signal)" opacity=".9"/><text x="${voice[0]}" y="${voice[1] - 24}" text-anchor="middle" class="lbl">teacher</text>`;
    // perceived direction arrow from the child toward where the voice seems to be
    const ang = Math.atan2(perceived[1] - cy, perceived[0] - cx), ax = cx + Math.cos(ang) * 60, ay = cy + Math.sin(ang) * 60;
    s += `<line x1="${cx}" y1="${cy}" x2="${ax}" y2="${ay}" stroke="${mode === 'separate' ? 'var(--hot)' : 'var(--ok)'}" stroke-width="3" stroke-linecap="round"/>`;
    if (mode === 'separate') s += `<circle cx="${perceived[0]}" cy="${perceived[1]}" r="14" fill="none" stroke="var(--hot)" stroke-width="2" stroke-dasharray="4 3"/><text x="${perceived[0]}" y="${perceived[1] - 22}" text-anchor="middle" class="lbl" fill="var(--hot)">seems to be here</text>`;
    s += `</svg>`;
    host.innerHTML = s;
    $('#dir-read').textContent = { none: 'No processing: the chatter is as loud as the voice, but the left-right loudness clue is intact.', separate: 'Each ear separately: the voice is clearer, but if the two sides turn sound down by different amounts the ear-to-ear loudness clue blurs and the voice can seem to come from nearer the middle.', linked: 'Both ears linked (the registered next step): one shared decision about how much to turn down, so the voice is clearer and still sounds like it comes from the left.' }[mode];
  }
  $$('#dir-modes button').forEach(b => b.addEventListener('click', () => { $$('#dir-modes button').forEach(x => x.setAttribute('aria-pressed', x === b)); draw(b.dataset.mode); }));
  draw('none');
})();

// ---------- electrodes (22 channels, 8 on) ----------
const el = $('#electrodes');
for (let i = 0; i < 22; i++) el.appendChild(document.createElement('i'));
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
function electrodeFrame(t) {
  const bars = el.children, on = new Set();
  // a smooth, speech-like moving formant pattern: pick 8 largest of a synthetic spectrum
  const spec = [...Array(22)].map((_, i) => Math.sin(i * 0.9 + t * 1.3) + 0.8 * Math.sin(i * 0.33 - t * 0.7) + 0.5 * Math.sin(i * 2.1 + t * 2.2));
  [...spec.keys()].sort((a, b) => spec[b] - spec[a]).slice(0, 8).forEach(i => on.add(i));
  for (let i = 0; i < 22; i++) { bars[i].classList.toggle('on', on.has(i)); if (!on.has(i)) bars[i].style.height = (18 + 30 * (spec[i] + 2.3) / 4.6) + '%'; else bars[i].style.height = ''; }
}
electrodeFrame(0);
if (!reduce) { let eo = new IntersectionObserver(es => { es[0].isIntersecting ? start() : stop(); }); let h; function start() { if (!h) h = setInterval(() => electrodeFrame(performance.now() / 1000), 160); } function stop() { clearInterval(h); h = null; } eo.observe(el); }

// ---------- SNR chart + slider ----------
const SNRS = bench.snrs, sys = bench.systems;
const SERIES = [
  { k: 'gen19', label: 'Gen 19 (3-seed mean)', color: 'var(--signal)', w: 2.5 },
  { k: 'causal_gate', label: 'classical causal gate', color: 'var(--dim)', w: 2 },
  { k: 'oracle_noncausal', label: 'non-causal oracle (ceiling)', color: 'var(--bone)', w: 1.5, dash: '5 4' }
];
function lineChart(hostId, { xs, series, xl, yl, req, reqLabel, ymin, ymax, xfmt = String, ytick = 2, ariaLabel }) {
  const W = 560, H = 320, m = { l: 46, r: 20, t: 16, b: 40 };
  const x = v => m.l + (v - xs[0]) / (xs[xs.length - 1] - xs[0]) * (W - m.l - m.r);
  const y = v => m.t + (1 - (v - ymin) / (ymax - ymin)) * (H - m.t - m.b);
  let g = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(ariaLabel)}"><g class="grid">`;
  for (let v = Math.ceil(ymin / ytick) * ytick; v <= ymax; v += ytick) g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/>`;
  g += `</g><g class="axis"><line x1="${m.l}" x2="${W - m.r}" y1="${y(0) > y(ymin) ? y(ymin) : y(0)}" y2="${y(0) > y(ymin) ? y(ymin) : y(0)}"/>`;
  for (let v = Math.ceil(ymin / ytick) * ytick; v <= ymax; v += ytick) g += `<text x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${v}</text>`;
  xs.forEach(v => g += `<text x="${x(v)}" y="${H - 14}" text-anchor="middle">${xfmt(v)}</text>`);
  g += `<text x="${(m.l + W - m.r) / 2}" y="${H - 1}" text-anchor="middle">${esc(xl)}</text><text transform="translate(12 ${(m.t + H - m.b) / 2}) rotate(-90)" text-anchor="middle">${esc(yl)}</text></g>`;
  if (req != null) g += `<line class="req" x1="${m.l}" x2="${W - m.r}" y1="${y(req)}" y2="${y(req)}"/><text class="req-l" x="${W - m.r}" y="${y(req) - 6}" text-anchor="end">${esc(reqLabel)}</text>`;
  series.forEach(s => {
    const d = s.ys.map((v, i) => `${i ? 'L' : 'M'}${x(xs[i]).toFixed(1)},${y(v).toFixed(1)}`).join('');
    g += `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="${s.w}" ${s.dash ? `stroke-dasharray="${s.dash}"` : ''} stroke-linejoin="round"/>`;
    s.ys.forEach((v, i) => g += `<circle data-s="${esc(s.label)}" data-x="${xs[i]}" data-y="${v}" cx="${x(xs[i])}" cy="${y(v)}" r="4" fill="var(--bg)" stroke="${s.color}" stroke-width="2"><title>${esc(s.label)} · ${xfmt(xs[i])}: ${fmt(v)}</title></circle>`);
    if (s.direct) g += `<text class="lbl" x="${x(xs[xs.length - 1]) - 6}" y="${y(s.ys[s.ys.length - 1]) - 9}" text-anchor="end" fill="${s.color}">${esc(s.direct)}</text>`;
  });
  g += `<g id="${hostId}-marker"></g></svg><div class="tip" role="status"></div>`;
  const host = $('#' + hostId); host.innerHTML = g;
  const tip = $('.tip', host);
  host.addEventListener('pointerover', e => { const c = e.target.closest('circle'); if (!c) return; tip.textContent = `${c.dataset.s} · ${xfmt(+c.dataset.x)}: ${fmt(+c.dataset.y)}`; const r = host.getBoundingClientRect(), b = c.getBoundingClientRect(); tip.style.left = (b.left - r.left + b.width / 2) + 'px'; tip.style.top = (b.top - r.top) + 'px'; tip.classList.add('on'); });
  host.addEventListener('pointerout', () => tip.classList.remove('on'));
  return { x, y };
}
const snrScale = lineChart('snr-chart', {
  xs: SNRS, xl: 'crowd SNR (dB)', yl: 'ΔSI-SDR vs unprocessed (dB)', ymin: -1, ymax: 13, ytick: 2, req: 1.5, reqLabel: 'required at −5 and 0 dB: +1.5',
  xfmt: v => (v > 0 ? '+' : '') + v, ariaLabel: 'Line chart of crowd ΔSI-SDR by SNR for Gen 19, the classical gate and the non-causal oracle; table follows',
  series: SERIES.map(s => ({ ...s, ys: SNRS.map(v => sys[s.k][String(v)]), direct: s.k === 'gen19' ? 'Gen 19' : null }))
});
$('#snr-legend').innerHTML = SERIES.map(s => `<span><i style="background:${s.color}" class="${s.dash ? 'dash' : ''}"></i>${s.label}</span>`).join('') + `<span><i class="dash" style="color:var(--hot)"></i>requirement</span>`;
$('#snr-table').innerHTML = `<table><thead><tr><th scope="col">SNR</th>${SERIES.map(s => `<th scope="col" class="num">${s.label}</th>`).join('')}<th scope="col">Gen 19 vs +1.5</th></tr></thead><tbody>${SNRS.map(v => `<tr><td class="num">${v > 0 ? '+' : ''}${v} dB</td>${SERIES.map(s => `<td class="num">${fmt(sys[s.k][String(v)])}</td>`).join('')}<td>${v <= 0 ? (sys.gen19[String(v)] >= 1.5 ? 'PASS' : 'FAIL') : 'not gated'}</td></tr>`).join('')}</tbody></table>`;
// slider
const sl = $('#snr'), interp = (k, v) => { const i = SNRS.findIndex(s => s >= v); if (i <= 0) return sys[k][String(SNRS[Math.max(i, 0)])]; const a = SNRS[i - 1], b = SNRS[i], t = (v - a) / (b - a); return sys[k][String(a)] * (1 - t) + sys[k][String(b)] * t; };
function slide() {
  const v = +sl.value, g = interp('gen19', v);
  $('#snr-v').textContent = (v > 0 ? '+' : '') + v + ' dB';
  $('#snr-g').textContent = fmt(g) + ' dB'; $('#snr-gate').textContent = fmt(interp('causal_gate', v)) + ' dB'; $('#snr-or').textContent = fmt(interp('oracle_noncausal', v)) + ' dB';
  const vd = $('#snr-verdict');
  if (v === -5) { vd.textContent = '× FAIL — +1.5 required'; vd.className = 'hot'; }
  else if (v === 0) { vd.textContent = '✓ PASS — +1.5 required'; vd.className = ''; }
  else { vd.textContent = 'not a gated row'; vd.className = 'muted'; }
  $('#snr-chart-marker').innerHTML = `<line x1="${snrScale.x(v)}" x2="${snrScale.x(v)}" y1="16" y2="280" stroke="${v === -5 ? 'var(--hot)' : 'var(--signal)'}" stroke-width="1.5" opacity=".8"/>`;
  document.documentElement.style.setProperty('--wall-glow', v === -5 ? '1' : '0');
}
sl.addEventListener('input', slide); slide();
// auto-walk the slider toward the wall when the section scrolls in (once, unless reduced motion)
if (!reduce) { let done = false; new IntersectionObserver(es => { if (es[0].isIntersecting && !done) { done = true; let v = 10; const h = setInterval(() => { v--; sl.value = v; slide(); if (v <= -5) clearInterval(h); }, 420); } }, { threshold: 0.5 }).observe($('#wall')); }

// ---------- scorecard ----------
const ROW_IDS = r => r.id || r.kpi.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
let level = 'parent';
const tb = $('#score-table tbody');
tb.innerHTML = score.rows.map(r => {
  const st = r.status === 'INFO' ? 'pending' : r.status === 'PASS' ? 'advance' : 'fail';
  const word = r.status === 'INFO' ? 'diagnostic' : r.status;
  return `<tr class="${r.status === 'FAIL' ? 'fail' : r.status === 'INFO' ? 'info' : ''}" data-row="${ROW_IDS(r)}">
    <td>${esc(r.kpi)}${r.status === 'FAIL' ? ' <span class="hot">— the −5 dB wall</span>' : ''}</td>
    <td class="num">${esc(r.actual)}</td><td class="mono small">${esc(r.required)}${r.stretch ? `<br><span class="muted">stretch ${esc(r.stretch)}: ${r.stretch_pass ? 'met' : 'not met'}</span>` : ''}</td>
    <td><span class="status" data-status="${st}" data-glyph="${GLYPH[st]}">${word}</span></td>
    <td class="ai-only" hidden><button class="explain-btn" type="button" data-explain="${ROW_IDS(r)}" aria-label="Explain ${esc(r.kpi)}">Explain</button></td></tr>`;
}).join('');
$('#score-verdict').textContent = `${score.n_pass} of ${score.n_required} required rows pass. Scorecard verdict: ${score.verdict}. promoted FALSE. Source: ${score.source}.`;
$('#level-toggle').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; level = b.dataset.level; $$('button', e.currentTarget).forEach(x => x.setAttribute('aria-pressed', x === b)); });

// ---------- generations: tree + cards ----------
const G = gens.generations;
$('#gen-updated').textContent = 'updated ' + gens.updated;
$('#null-count').textContent = G.filter(g => (g.status === 'null' || g.status === 'fail') && +g.id.replace('gen', '') > 19).length;
const live = G.find(g => g.status === 'running');
const chip = $('#live-chip');
if (live) { chip.classList.remove('ok', 'off'); $('#live-text').textContent = `${live.label} running${live.eta ? ' · ' + live.eta : ''}`; }
else { const last = G[G.length - 1]; chip.classList.add('ok'); $('#live-text').textContent = `${last.label}: ${WORD[last.status]}`; }
(function tree() {
  const W = 1000, step = W / (G.length + 1), yT = 110, H = 200;
  let s = `<svg viewBox="0 0 ${W} ${H}">`;
  // trunk through survivors (baseline/advance); dead branches hang off the trunk and end in ×
  const trunk = G.filter(g => g.status === 'baseline' || g.status === 'advance');
  s += `<path class="trunk" d="${G.map((g, i) => `${i ? 'L' : 'M'}${step * (i + 1)},${yT}`).join('')}"/>`;
  G.forEach((g, i) => {
    const x = step * (i + 1), prevX = step * i;
    const dead = g.status === 'null' || g.status === 'fail', run = g.status === 'running', pend = g.status === 'pending';
    if (dead) s += `<path class="dead" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT - 55} ${x},${yT - 62}"/><line class="x" x1="${x - 6}" y1="${yT - 68}" x2="${x + 6}" y2="${yT - 56}"/><line class="x" x1="${x + 6}" y1="${yT - 68}" x2="${x - 6}" y2="${yT - 56}"/>`;
    if (run) s += `<path class="live" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT + 50} ${x},${yT + 56}"/><circle class="running-ring" cx="${x}" cy="${yT + 56}" r="9"/>`;
    if (pend) s += `<path class="pend" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT + 50} ${x},${yT + 56}"/>`;
    const ny = dead ? yT - 62 : (run || pend) ? yT + 56 : yT;
    s += `<circle class="node ${g.status}" cx="${x}" cy="${ny}" r="${g.status === 'baseline' ? 11 : 7}"/>`;
    s += `<text x="${x}" y="${dead ? yT - 84 : ny + 30}" text-anchor="middle">${esc(g.label)}</text><text class="dim" x="${x}" y="${dead ? yT - 70 + 4 : ny + 45}" text-anchor="middle">${GLYPH[g.status]} ${WORD[g.status]}</text>`;
  });
  $('#tree').innerHTML = s + '</svg>';
  $('#tree-desc').textContent = 'Generation tree. ' + G.map(g => `${g.label}: ${WORD[g.status]} — ${g.change}.`).join(' ') + ` Trunk survivors: ${trunk.map(t => t.label).join(', ')}.`;
})();
$('#gen-cards').innerHTML = G.map(g => `<article class="gen" data-status="${g.status}" id="${g.id}" aria-labelledby="${g.id}-h">
  <h3 id="${g.id}-h"><span>${esc(g.label)}</span><span class="status" data-status="${g.status}" data-glyph="${GLYPH[g.status]}">${WORD[g.status]}</span></h3>
  <p class="change">${esc(g.change)}</p>
  ${g.eta ? `<p class="eta">◉ ${esc(g.eta)}</p>` : ''}
  <dl>${(g.numbers || []).map(n => `<dt>${esc(n.label)}</dt><dd>${esc(n.value)}</dd>`).join('')}</dl>
  ${g.note ? `<p class="note">${esc(g.note)}</p>` : ''}
  <div class="acts">${g.link ? `<a href="${/^https?:/.test(g.link) ? esc(g.link) : esc(repoUrl(g.link) || '#')}" target="_blank" rel="noopener">filed record ↗</a>` : ''}
    <button class="explain-btn ai-only" hidden type="button" data-explain="${g.id}">Explain</button>
    <button class="explain-btn ai-only" hidden type="button" data-brief="${g.id}">Brief</button></div>
  <div class="explain-slot"></div></article>`).join('');

// ---------- Gen 21 chart (per-seed −5 dB gains, VAL vs bench, two arms) ----------
(function g21chart() {
  const seeds = g21.seeds.map(String), arms = [{ k: 's48', label: 'S48 (48k scratch)', color: 'var(--signal)' }, { k: 'r48', label: 'R48 (parent + 24k)', color: 'var(--bone)' }];
  const W = 560, H = 300, m = { l: 46, r: 16, t: 20, b: 46 }, ymin = -0.6, ymax = 0.6;
  const groups = []; seeds.forEach(sd => ['val', 'bench'].forEach(p => groups.push({ sd, p })));
  const gw = (W - m.l - m.r) / groups.length, bw = gw / 3;
  const y = v => m.t + (1 - (v - ymin) / (ymax - ymin)) * (H - m.t - m.b);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Bar chart of Gen 21 −5 dB gains over the Gen 19 parent, per seed and panel, both arms; table follows"><g class="grid">`;
  for (let v = -0.6; v <= 0.61; v += 0.3) s += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/>`;
  s += `</g><g class="axis"><line x1="${m.l}" x2="${W - m.r}" y1="${y(0)}" y2="${y(0)}" stroke="var(--dim)"/>`;
  for (let v = -0.6; v <= 0.61; v += 0.3) s += `<text x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${v.toFixed(1)}</text>`;
  s += `<text transform="translate(12 ${(m.t + H - m.b) / 2}) rotate(-90)" text-anchor="middle">−5 dB gain vs parent (dB)</text></g>`;
  s += `<line class="req" x1="${m.l}" x2="${W - m.r}" y1="${y(0.3)}" y2="${y(0.3)}"/><text class="req-l" x="${W - m.r}" y="${y(0.3) - 6}" text-anchor="end">bar: +0.30 on both panels</text>`;
  groups.forEach((g, i) => {
    const x0 = m.l + i * gw + gw * 0.15;
    arms.forEach((a, j) => { const v = g21.per_seed[g.sd][a.k][g.p + '_gain_m5'][0]; const top = Math.min(y(v), y(0)), h = Math.abs(y(v) - y(0)); s += `<rect x="${x0 + j * (bw + 2)}" y="${top}" width="${bw}" height="${Math.max(h, 1)}" fill="${a.color}" rx="2"><title>seed ${g.sd} · ${g.p.toUpperCase()} · ${a.label}: ${fmt(v)} dB</title></rect>`; });
    s += `<text class="axis" x="${x0 + bw}" y="${H - 28}" text-anchor="middle" style="fill:var(--dim);font-family:var(--mono);font-size:11px">${g.p.toUpperCase()}</text>`;
    if (g.p === 'val') s += `<text x="${x0 + gw * 0.85}" y="${H - 12}" text-anchor="middle" style="fill:var(--bone);font-family:var(--mono);font-size:11px">seed ${g.sd}</text>`;
  });
  $('#g21-chart').innerHTML = s + '</svg>';
  $('#g21-legend').innerHTML = arms.map(a => `<span><i style="background:${a.color}"></i>${a.label}</span>`).join('') + `<span><i class="dash" style="color:var(--hot)"></i>+0.30 qualification bar</span>`;
  const mg = g21.arms;
  $('#g21-table').innerHTML = `<table><thead><tr><th scope="col">Seed</th><th scope="col">Panel</th>${arms.map(a => `<th scope="col" class="num">${a.label}</th>`).join('')}</tr></thead><tbody>${groups.map(g => `<tr><td>${g.sd}</td><td>${g.p.toUpperCase()}</td>${arms.map(a => `<td class="num">${fmt(g21.per_seed[g.sd][a.k][g.p + '_gain_m5'][0])}</td>`).join('')}</tr>`).join('')}<tr><td><b>mean</b></td><td>VAL</td><td class="num"><b>${fmt(mg.s48.mean_gains.val_gain_m5[0])}</b></td><td class="num"><b>${fmt(mg.r48.mean_gains.val_gain_m5[0])}</b></td></tr><tr><td><b>mean</b></td><td>bench</td><td class="num"><b>${fmt(mg.s48.mean_gains.bench_gain_m5[0])}</b></td><td class="num"><b>${fmt(mg.r48.mean_gains.bench_gain_m5[0])}</b></td></tr><tr><td colspan="2">qualifies (≥ +0.30 both)</td><td>${mg.s48.qualifies ? 'yes' : 'no'}</td><td>${mg.r48.qualifies ? 'yes' : 'no'}</td></tr></tbody></table>`;
})();

// ---------- VAL trajectory chart ----------
(function valchart() {
  const names = { gen19: 'Gen 19 (plain SI-SDR)', gen22_cap30: 'Gen 22 (30 dB cap)', gen23: 'Gen 23 (SI-SDR + 5× spectral)' };
  const cols = { gen19: 'var(--signal)', gen22_cap30: 'var(--bone)', gen23: 'var(--amber)' };
  const keys = Object.keys(traj.series);
  const xs = traj.series.gen19.filter(e => e.step > 0).map(e => e.step);
  lineChart('val-chart', {
    xs, xl: 'training step', yl: 'VAL −5 dB ΔSI-SDR (dB)', ymin: -0.8, ymax: 1.2, ytick: 0.4, xfmt: v => (v / 1000) + 'k',
    ariaLabel: 'Line chart of validation −5 dB ΔSI-SDR by training step for Gen 19 and Gen 22 on seed 17; table follows',
    series: keys.map(k => ({ k, label: names[k] || k, color: cols[k] || 'var(--dim)', w: 2, ys: traj.series[k].filter(e => e.step > 0).map(e => e.m5), direct: null }))
  });
  $('#val-legend').innerHTML = keys.map(k => `<span><i style="background:${cols[k] || 'var(--dim)'}"></i>${names[k] || k}</span>`).join('') + `<span class="muted">step 0 (−23.6 dB) omitted for scale</span>`;
  $('#val-table').innerHTML = `<table><thead><tr><th scope="col">Step</th>${keys.map(k => `<th scope="col" class="num">${names[k] || k}</th>`).join('')}</tr></thead><tbody>${traj.series.gen19.map((e, i) => `<tr><td class="num">${e.step}</td>${keys.map(k => `<td class="num">${traj.series[k][i] ? fmt(traj.series[k][i].m5) : '—'}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
})();

// ---------- Muse: health → show AI UI; Ask; Explain; Brief ----------
const health = await api.health();
if (health) {
  $$('.ai-only').forEach(e => e.hidden = false);
  $('#ask-off').hidden = true;
  const SUGGEST = [
    "Why can't the model pass crowd noise at −5 dB?",
    'What did Gen 22 change and why did it fail?',
    'Is this better than his Nucleus 6?',
    'What would have to happen before Graham could try this?',
    'What did Gen 21 show about training longer?',
    'What does the independent reviewer actually check?'
  ];
  $('#chips').innerHTML = SUGGEST.map(q => `<button type="button" class="chip" role="listitem">${esc(q)}</button>`).join('');
  $('#chips').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; $('#q').value = b.textContent; ask(b.textContent); });
  $('#ask-form').addEventListener('submit', e => { e.preventDefault(); const q = $('#q').value.trim(); if (q) ask(q); });
  async function ask(q) {
    const ans = $('#answer'), th = $('#thinking'), steps = $('#steps'), out = $('#answer-text'), btn = $('#ask-btn');
    ans.classList.add('on'); th.hidden = false; steps.innerHTML = ''; out.innerHTML = ''; btn.disabled = true;
    try {
      const r = await api.ask(q);
      steps.innerHTML = (r.steps || []).map(s => `<li><b>${esc(s.tool)}</b><span>${esc(s.input || '')}${s.output ? ` → <span class="muted">${esc(s.output)}</span>` : ''}</span></li>`).join('');
      out.innerHTML = mdLite(r.answer) + `<p class="small muted" style="margin:12px 0 0">Answered by ${esc(r.model || health.model)}. Based only on the research record.</p>`;
    } catch (err) { out.innerHTML = `<p class="err">${esc(err.message)}</p>`; }
    finally { th.hidden = true; btn.disabled = false; }
  }
  document.addEventListener('click', async e => {
    const b = e.target.closest('[data-explain],[data-brief]'); if (!b) return;
    const isBrief = 'brief' in b.dataset, id = b.dataset.explain || b.dataset.brief;
    let slot = b.closest('tr') ? b.closest('tr').nextElementSibling : b.closest('.gen') ? $('.explain-slot', b.closest('.gen')) : b.closest('.kv').nextElementSibling;
    if (b.closest('tr')) {
      if (!slot || !slot.classList.contains('explain-row')) { slot = document.createElement('tr'); slot.className = 'explain-row'; slot.innerHTML = `<td colspan="5"></td>`; b.closest('tr').after(slot); }
      slot = slot.firstElementChild;
    }
    slot.innerHTML = `<div class="explain-out"><span class="thinking"><i aria-hidden="true"></i>Muse is writing${isBrief ? ' a brief' : ` for ${level === 'parent' ? 'a parent' : 'a researcher'}`}…</span></div>`;
    b.disabled = true;
    try { const r = isBrief ? await api.brief(id) : await api.explain(id, level); slot.innerHTML = `<div class="explain-out">${mdLite(r.text)}<p class="small muted" style="margin:8px 0 0">${esc(r.model || health.model)} · ${isBrief ? 'generation brief' : 'for ' + level + 's'} · AI answers can contain mistakes.</p></div>`; }
    catch (err) { slot.innerHTML = `<div class="explain-out err">${esc(err.message)}</div>`; }
    finally { b.disabled = false; }
  });
} else if (!live) {
  chip.classList.add('off');
}
