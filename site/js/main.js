import { api, mdLite } from './api.js';
const loadWave = () => import('./gl.js').catch(() => {});
if ('requestIdleCallback' in window) requestIdleCallback(loadWave, { timeout: 1500 }); else setTimeout(loadWave, 300);
const C = window.SITE_CONFIG;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fmt = (v, d = 2, sign = true) => (sign && v > 0 ? '+' : '') + Number(v).toFixed(d);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const GLYPH = { baseline: '', advance: '', null: '', fail: '', running: '', pending: '', shelved: '' };
const statusWord = g => (g.status === 'null' || g.status === 'fail') ? (g.aim === 'room' ? 'did not pass' : 'did not help') : WORD[g.status];
const WORD = { baseline: 'our best so far', advance: 'kept', null: 'did not help', fail: 'did not pass', running: 'training now', pending: 'up next', shelved: 'set aside' };

// ---------- brand / repo (one place: js/config.js) ----------
document.title = `${C.brand}: helping kids with cochlear implants hear one voice in a crowd`;
$$('[data-brand-name]').forEach(e => e.textContent = C.brand);
const repoUrl = p => C.repo ? (p ? `${C.repo}/blob/${C.repoBranch}/${p}` : C.repo) : null;
$$('a[data-repo]').forEach(a => {
  const u = repoUrl(a.dataset.repo);
  if (u) { a.href = u; a.target = '_blank'; a.rel = 'noopener'; } else { a.replaceWith(...a.childNodes); }
});
if (!C.repo) $('#repo-link')?.remove();
$$('a[data-hf]').forEach(a => { if (C.huggingface) { a.href = C.huggingface; a.target = '_blank'; a.rel = 'noopener'; } else a.replaceWith(...a.childNodes); });
$$('a[data-hf-file]').forEach(a => { if (C.huggingface) { a.href = C.huggingface.replace(/\/$/, '') + '/resolve/main/' + a.dataset.hfFile; a.target = '_blank'; a.rel = 'noopener'; } else a.replaceWith(...a.childNodes); });

// ---------- header / nav ----------
const bar = $('#bar'), nav = $('#chapnav'), menu = $('#menu-btn');
addEventListener('scroll', () => bar.classList.toggle('solid', scrollY > 40), { passive: true });
const setMenu = o => { nav.classList.toggle('open', o); menu.setAttribute('aria-expanded', o); menu.textContent = o ? 'Close' : 'Menu'; };
menu.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menu.focus(); } });
document.addEventListener('click', e => { if (nav.classList.contains('open') && !bar.contains(e.target)) setMenu(false); });
// Nav fit: show the inline chapter links only when every item fits on one line; otherwise the Menu button.
function fitNav() {
  if (!nav.querySelector('.nav-status')) { const st = document.createElement('a'); st.className = 'nav-status'; st.href = '#generations'; nav.prepend(st); }
  nav.querySelector('.nav-status').textContent = $('#live-text').textContent;
  bar.classList.remove('compact'); bar.classList.add('measuring'); nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false');
  const barIn = bar.querySelector('.bar-in');
  const used = [...barIn.children].filter(e => e !== nav && e !== menu).reduce((a, e) => a + Math.max(e.getBoundingClientRect().width, e.scrollWidth || 0), 0) + 16 * (barIn.children.length);
  const fits = nav.scrollWidth + used <= barIn.clientWidth;
  bar.classList.remove('measuring');
  if (!fits) bar.classList.add('compact');
}
fitNav(); let navT; addEventListener('resize', () => { clearTimeout(navT); navT = setTimeout(fitNav, 80); }); document.fonts && document.fonts.ready.then(fitNav);
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
  // deaf visitors SEE the music: an AnalyserNode feeds a level into the WebGL wave (window.__waveLevel)
  let ac, an, buf;
  function analyser() {
    if (ac) return;
    try { ac = new (window.AudioContext || window.webkitAudioContext)(); const srcN = ac.createMediaElementSource(v); an = ac.createAnalyser(); an.fftSize = 256; buf = new Uint8Array(an.frequencyBinCount); srcN.connect(an); an.connect(ac.destination); } catch (_) { return; }
    let bassPrev = 0; (function tick() { if (!an) return; an.getByteFrequencyData(buf); let sum = 0, bass = 0; for (let i = 0; i < 24; i++) sum += buf[i]; for (let i = 1; i <= 6; i++) bass += buf[i]; bass /= 6 * 255; const rise = Math.max(0, bass - bassPrev); bassPrev = bassPrev * 0.8 + bass * 0.2; const off = v.muted || v.paused; window.__waveLevel = off ? 0 : sum / (24 * 255); window.__kick = off ? 0 : Math.min(1, rise * 6); requestAnimationFrame(tick); })();
  }
  const setPlay = on => { play.textContent = on ? 'Pause' : 'Play'; play.setAttribute('aria-pressed', on); };
  v.addEventListener('play', () => { setPlay(true); window.__dancePlaying = true; }); v.addEventListener('pause', () => { setPlay(false); window.__dancePlaying = false; });
  play.addEventListener('click', () => { attach(); v.paused ? v.play().catch(() => {}) : v.pause(); });
  snd.addEventListener('click', () => { attach(); v.muted = !v.muted; const on = !v.muted; snd.textContent = on ? 'Sound on: tap to mute' : 'Turn sound on'; if (on) analyser(); snd.classList.toggle('is-on', on); snd.setAttribute('aria-pressed', on); snd.setAttribute('aria-label', on ? 'Sound is on. Turn sound off' : 'Sound is off. Turn sound on'); if (on && v.paused) v.play().catch(() => {}); });
  // near the viewport: attach the source; in view: autoplay muted (unless reduced motion); out of view: pause
  new IntersectionObserver(es => { if (es[0].isIntersecting) attach(); }, { rootMargin: '600px 0px' }).observe(v);
  new IntersectionObserver(es => { if (es[0].isIntersecting) { if (!rm) { attach(); v.play().catch(() => {}); } } else if (!v.paused) v.pause(); }, { threshold: 0.4 }).observe(v);
})();


// ---------- "What this could mean": direction illustration (idea only, not data) ----------
(function direction() {
  const host = $('#dir-demo'); if (!host) return;
  const W = 520, H = 360, cx = 260, cy = 190;
  const noise = [[70, 70], [450, 60], [470, 300], [120, 285], [260, 40], [250, 335]];
  const voice = [60, 190];
  function draw(mode) {
    // perceived position of the voice: separate per-ear processing can blur the ear-to-ear loudness clue (pulls toward centre)
    const perceived = mode === 'none' ? voice : mode === 'separate' ? [170, 190] : voice;
    const nAlpha = mode === 'none' ? 0.9 : 0.35, vSize = mode === 'none' ? 14 : 20;
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Illustration: a child in the centre of a noisy room, a voice on the left. In 'each ear separately' mode the voice seems to come from nearer the middle; in 'both ears linked' mode it stays on the left.">
      <rect x="20" y="20" width="${W - 40}" height="${H - 40}" fill="none" stroke="var(--rule)"/>
`;
    noise.forEach(([x, y]) => s += `<circle cx="${x}" cy="${y}" r="10" fill="var(--dim)" opacity="${nAlpha}"/><text x="${x}" y="${y + 22}" text-anchor="middle" class="lbl dim" font-size="10">noise</text>`);
    // child (head with two ears)
    s += `<circle cx="${cx}" cy="${cy}" r="22" fill="var(--bg3)" stroke="var(--bone)" stroke-width="2"/><circle cx="${cx - 24}" cy="${cy}" r="6" fill="var(--bone)"/><circle cx="${cx + 24}" cy="${cy}" r="6" fill="var(--bone)"/><text x="${cx}" y="${cy + 44}" text-anchor="middle" class="lbl">Graham</text>`;
    // true voice
    s += `<circle cx="${voice[0]}" cy="${voice[1]}" r="${vSize}" fill="var(--signal)" opacity=".9"/><text x="${voice[0]}" y="${voice[1] - 24}" text-anchor="middle" class="lbl">teacher</text>`;
    // perceived direction arrow from the child toward where the voice seems to be
    const ang = Math.atan2(perceived[1] - cy, perceived[0] - cx), ax = cx + Math.cos(ang) * 60, ay = cy + Math.sin(ang) * 60;
    s += `<line x1="${cx}" y1="${cy}" x2="${ax}" y2="${ay}" stroke="${mode === 'separate' ? 'var(--hot)' : 'var(--ok)'}" stroke-width="3" stroke-linecap="round"/>`;
    if (mode === 'separate') s += `<circle cx="${perceived[0]}" cy="${perceived[1]}" r="14" fill="none" stroke="var(--hot)" stroke-width="2" stroke-dasharray="4 3"/><text x="${perceived[0]}" y="${perceived[1] - 28}" text-anchor="middle" class="lbl" fill="var(--hot)">seems to be here</text>`;
    s += `</svg>`;
    host.innerHTML = s;
    $('#dir-read').textContent = { none: 'No cleanup: the chatter is as loud as the voice, but the louder-ear clue is intact.', separate: 'Each ear separately: the voice is clearer, but if the two sides turn sound down by different amounts the louder-ear clue blurs, and the voice can seem to come from nearer the middle.', linked: 'Both ears agreeing (our planned next step): one shared decision about how much to turn down, so the voice is clearer and still sounds like it comes from the left.' }[mode]; window.__ears = mode;
  }
  $$('#dir-modes button').forEach(b => b.addEventListener('click', () => { $$('#dir-modes button').forEach(x => x.setAttribute('aria-pressed', x === b)); draw(b.dataset.mode); }));
  draw('none');
})();

const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
// implant chapter: show the 3 most important clips by default
{ const tracks = $$('#implant .imp-track'); if (tracks.length === 8) { const keep = new Set([1, 3, 4, 6, 7]); const hid = tracks.filter((t, i) => !keep.has(i)); hid.forEach(t => t.hidden = true); const b = document.createElement('button'); b.type = 'button'; b.className = 'explain-btn imp-more'; b.textContent = `Show all ${tracks.length} clips`; b.addEventListener('click', () => { const open = hid[0].hidden; hid.forEach(t => t.hidden = !open); b.textContent = open ? 'Show fewer clips' : `Show all ${tracks.length} clips`; }); const groups = $$('#implant .imp-group'); (groups[groups.length - 1] || tracks[0].parentElement).after(b); } }

// ---------- SNR chart + slider ----------
const SNRS = bench.snrs, sys = bench.systems;
const SERIES = [
  { k: 'gen19', label: 'Our program (version 19)', color: 'var(--signal)', w: 2.5 },
  { k: 'causal_gate', label: 'the simple filter that already exists', color: 'var(--dim)', w: 2 },
  { k: 'oracle_noncausal', label: 'a version that cheats by hearing the future', color: 'var(--bone)', w: 1.5, dash: '5 4' }
];
function lineChart(hostId, { xs, series, xl, yl, req, reqLabel, ymin, ymax, xfmt = String, ytick = 2, ariaLabel }) {
  const phone = innerWidth < 700;
  const W = phone ? 360 : 560, H = phone ? 260 : 320, m = { l: 44, r: 16, t: 16, b: 44 };
  const x = v => m.l + (v - xs[0]) / (xs[xs.length - 1] - xs[0]) * (W - m.l - m.r);
  const y = v => m.t + (1 - (v - ymin) / (ymax - ymin)) * (H - m.t - m.b);
  let g = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(ariaLabel)}" class="${phone ? 'phone' : ''}"><g class="grid">`;
  for (let v = Math.ceil(ymin / ytick) * ytick; v <= ymax; v += ytick) g += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/>`;
  g += `</g><g class="axis"><line x1="${m.l}" x2="${W - m.r}" y1="${y(0) > y(ymin) ? y(ymin) : y(0)}" y2="${y(0) > y(ymin) ? y(ymin) : y(0)}"/>`;
  for (let v = Math.ceil(ymin / ytick) * ytick; v <= ymax; v += ytick) g += `<text x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${v}</text>`;
  xs.forEach(v => g += `<text x="${x(v)}" y="${H - 14}" text-anchor="middle">${xfmt(v)}</text>`);
  g += `<text x="${(m.l + W - m.r) / 2}" y="${H - 1}" text-anchor="middle">${esc(xl)}</text><text transform="translate(12 ${(m.t + H - m.b) / 2}) rotate(-90)" text-anchor="middle">${esc(yl)}</text></g>`;
  if (req != null) g += `<line class="req" x1="${m.l}" x2="${W - m.r}" y1="${y(req)}" y2="${y(req)}"/><text class="req-l" x="${W - m.r}" y="${y(req) - 8}" text-anchor="end">${esc(phone ? "goal +1.5" : reqLabel)}</text>`;
  series.forEach(s => {
    const d = s.ys.map((v, i) => `${i ? 'L' : 'M'}${x(xs[i]).toFixed(1)},${y(v).toFixed(1)}`).join('');
    g += `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="${s.w}" ${s.dash ? `stroke-dasharray="${s.dash}"` : ''} stroke-linejoin="round"/>`;
    s.ys.forEach((v, i) => g += `<circle data-s="${esc(s.label)}" data-x="${xs[i]}" data-y="${v}" cx="${x(xs[i])}" cy="${y(v)}" r="4" fill="var(--bg)" stroke="${s.color}" stroke-width="2"><title>${esc(s.label)} at ${xfmt(xs[i])}: ${fmt(v)}</title></circle>`);
    if (s.direct) g += `<text class="lbl" x="${x(xs[xs.length - 1]) - 6}" y="${y(s.ys[s.ys.length - 1]) - 19}" text-anchor="end" fill="${s.color}">${esc(s.direct)}</text>`;
  });
  g += `<g id="${hostId}-marker"></g></svg><div class="tip" role="status"></div>`;
  const host = $('#' + hostId); host.innerHTML = g;
  const tip = $('.tip', host);
  host.addEventListener('pointerover', e => { const c = e.target.closest('circle'); if (!c) return; tip.textContent = `${c.dataset.s} at ${xfmt(+c.dataset.x)}: ${fmt(+c.dataset.y)}`; const r = host.getBoundingClientRect(), b = c.getBoundingClientRect(); tip.style.left = (b.left - r.left + b.width / 2) + 'px'; tip.style.top = (b.top - r.top) + 'px'; tip.classList.add('on'); });
  host.addEventListener('pointerout', () => tip.classList.remove('on'));
  return { x, y, yAxis: H - m.b };
}
const snrScale = lineChart('snr-chart', {
  xs: SNRS, xl: 'how loud the crowd is (dB; lower is harder)', yl: 'how much cleaner (dB)', ymin: -1, ymax: 13, ytick: 2, req: 1.5, reqLabel: 'our goal for the two hardest: +1.5',
  xfmt: v => (v > 0 ? '+' : '') + v, ariaLabel: 'Line chart: how much cleaner the voice gets at each crowd loudness, for our program, the simple filter, and a cheating version; table follows',
  series: SERIES.map(s => ({ ...s, ys: SNRS.map(v => sys[s.k][String(v)]), direct: s.k === 'gen19' ? 'our program' : null }))
});
$('#snr-legend').innerHTML = SERIES.map(s => `<span><i style="background:${s.color}" class="${s.dash ? 'dash' : ''}"></i>${s.label}</span>`).join('') + `<span><i class="dash" style="color:var(--hot)"></i>our goal</span>`;
$('#snr-table').innerHTML = `<table><thead><tr><th scope="col">Crowd loudness</th>${SERIES.map(s => `<th scope="col" class="num">${s.label}</th>`).join('')}<th scope="col">Meets our goal?</th></tr></thead><tbody>${SNRS.map(v => `<tr><td class="num">${v > 0 ? '+' : ''}${v} dB</td>${SERIES.map(s => `<td class="num">${fmt(sys[s.k][String(v)])}</td>`).join('')}<td>${v <= 0 ? (sys.gen19[String(v)] >= 1.5 ? 'yes' : 'no') : 'no goal set here'}</td></tr>`).join('')}</tbody></table>`;
// slider
const sl = $('#snr'), interp = (k, v) => { const i = SNRS.findIndex(s => s >= v); if (i <= 0) return sys[k][String(SNRS[Math.max(i, 0)])]; const a = SNRS[i - 1], b = SNRS[i], t = (v - a) / (b - a); return sys[k][String(a)] * (1 - t) + sys[k][String(b)] * t; };
function slide() {
  const v = +sl.value, g = interp('gen19', v);
  $('#snr-v').textContent = (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v) + ' dB';
  $('#snr-g').textContent = fmt(g) + ' dB'; $('#snr-gate').textContent = fmt(interp('causal_gate', v)) + ' dB'; $('#snr-or').textContent = fmt(interp('oracle_noncausal', v)) + ' dB';
  const vd = $('#snr-verdict');
  if (v === -5) { vd.textContent = 'That misses our goal of +1.5.'; vd.className = 'hot'; }
  else if (v === 0) { vd.textContent = 'That meets our goal of +1.5.'; vd.className = ''; }
  else { vd.textContent = 'We set no goal here.'; vd.className = 'muted'; }
  $('#snr-chart-marker').innerHTML = `<line x1="${snrScale.x(v)}" x2="${snrScale.x(v)}" y1="16" y2="${snrScale.yAxis}" stroke="${v === -5 ? 'var(--hot)' : 'var(--signal)'}" stroke-width="1.5" opacity=".8"/>`;
  window.__fray = (10 - v) / 15;
}
sl.addEventListener('input', slide); slide();
// auto-walk the slider toward the wall when the section scrolls in (once, unless reduced motion)
if (!reduce) {
  let done = false, h = null; const read = $('#snr-read');
  const stop = () => { done = true; if (h) { clearInterval(h); h = null; } read.setAttribute('aria-live', 'polite'); };
  sl.addEventListener('pointerdown', stop); sl.addEventListener('keydown', stop);
  new IntersectionObserver(es => { if (es[0].isIntersecting && !done) { done = true; read.setAttribute('aria-live', 'off'); let v = 10; h = setInterval(() => { v--; sl.value = v; slide(); sl.dispatchEvent(new Event('input', { bubbles: true })); if (v <= -5) { stop(); } }, 420); } }, { threshold: 0.6 }).observe($('.slider-box'));
}
// the slider also drives the shader: the voice line frays toward −5 dB
sl.addEventListener('input', () => { window.__fray = (10 - +sl.value) / 15; });

// ---------- scorecard ----------
const NEED = { crowd_sisdr: 'needs at least +3.0 dB cleaner', crowd_stoi: 'needs at least +0.03 more understandable', crowd_ace: 'the implant pulses must come out at least 0.05 closer to the clean voice', crowd_m5: 'needs at least +1.5 dB cleaner', crowd_0: 'needs at least +1.5 dB cleaner', crowd_m5_stoi: 'must not get less understandable', crowd_every_seed: 'must help in all three runs', crowd_vs_gate: 'must beat the simple filter', ssn: 'needs at least +3.0 dB cleaner', white: 'must not get worse', quiet_abs: 'must stay very clean (25 dB or better)', quiet_stoi: 'must stay understandable', ild: 'must be closer than with no cleanup', itd: 'must be at least as close as with no cleanup', ild_distortion: 'no requirement' };
const UNIT = { crowd_sisdr: ' dB', crowd_m5: ' dB', crowd_0: ' dB', ssn: ' dB', white: ' dB', quiet_abs: ' dB', ild: ' dB', itd: ' samples', crowd_stoi: ' points', crowd_ace: ' points', crowd_m5_stoi: ' points', quiet_stoi: ' points', crowd_vs_gate: ' dB', ild_distortion: ' dB' };
const RESULT = r => { const v = String(r.actual); if (r.id === 'itd') return 'the timing was off by about a quarter of a thousandth of a second'; if (r.id === 'crowd_every_seed') return v.replace(/[\[\]]/g, '').split(',').map(x => '+' + x.trim() + ' dB').join(', '); const n = parseFloat(v); if (isNaN(n)) return v; const neg = n < 0 ? '−' : ''; const abs = v.replace(/^-/, ''); if (r.id === 'crowd_stoi') return 'a little easier to understand (' + neg + abs + ')'; if (r.id === 'crowd_ace') return 'the implant pulses come out a little closer to the clean voice (' + neg + abs + ')'; if (UNIT[r.id] === ' points') return neg + abs + ' points'; const sign = /^(crowd_|ssn|white)/.test(r.id) && n > 0 && !/abs|vs_gate/.test(r.id) ? '+' : ''; return sign + neg + abs + (UNIT[r.id] || ''); };
const PLAIN = { crowd_sisdr: 'Crowd: how clean the voice is', crowd_stoi: 'Crowd: how understandable it is', crowd_ace: 'Crowd: what the electrodes would receive',
  crowd_m5: 'Crowd louder than the voice (−5 dB)', crowd_0: 'Crowd as loud as the voice (0 dB)', crowd_m5_stoi: 'Never harder to understand in the loudest crowd',
  crowd_every_seed: 'Helps in all three training runs', crowd_vs_gate: 'Better than the simple filter that already exists', ssn: 'A steady hum',
  white: 'A hiss it never trained on', quiet_abs: 'Quiet speech left alone: still clean', quiet_stoi: 'Quiet speech left alone: still understandable',
  ild: 'Which-side clue: loudness difference', itd: 'Which-side clue: timing difference', ild_distortion: 'How much the which-side clue moved, just for information' };
const ROW_IDS = r => r.id || r.kpi.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
let level = 'parent';
const tb = $('#score-table tbody');
const scoreRow = r => {
  const st = r.status === 'INFO' ? 'pending' : r.status === 'PASS' ? 'advance' : 'fail';
  const word = r.status === 'INFO' ? 'for information' : r.status === 'PASS' ? 'pass' : 'miss';
  return `<tr class="${r.status === 'FAIL' ? 'fail' : r.status === 'INFO' ? 'info' : ''}" data-row="${ROW_IDS(r)}">
    <td data-l="Check">${esc(PLAIN[r.id] || r.kpi)}${r.status === 'FAIL' ? ' <span class="hot">(the hardest crowd)</span>' : ''}</td>
    <td class="num" data-l="Result">${esc(RESULT(r))}</td><td class="small muted" data-l="Needs">${esc(NEED[r.id] || r.required)}</td>
    <td data-l="Status"><span class="st" data-status="${st}">${GLYPH[st]} ${word}</span></td>
    <td class="ai-only" hidden><button class="explain-btn" type="button" data-explain="${ROW_IDS(r)}" aria-label="Explain ${esc(r.kpi)}">Explain</button></td></tr>`;
};
{
  const fails = score.rows.filter(r => r.status === 'FAIL'), passes = score.rows.filter(r => r.status !== 'FAIL');
  tb.innerHTML = fails.map(scoreRow).join('') + `<tr class="fold-row"><td colspan="5"><details class="fold"><summary>the ${passes.filter(r => r.status === 'PASS').length} checks it passes, plus one we only record</summary><table class="inner"><tbody>${passes.map(scoreRow).join('')}</tbody></table></details></td></tr>`;
  const tech = score.rows.map(r => `<li>${esc(r.kpi)}: result ${esc(r.actual)}, required ${esc(r.required)}${r.stretch ? `; stretch ${esc(r.stretch)} ${r.stretch_pass ? 'met' : 'not met'}` : ''}</li>`).join('');
  $('#score-verdict').insertAdjacentHTML('afterend', `<details class="researchers"><summary>notes for researchers</summary><ul class="plain small muted">${tech}</ul></details>`);
}
$('#score-verdict').textContent = `${score.n_pass} of ${score.n_required} checks pass. Our verdict: not good enough yet, keep working.`;
$('#level-toggle').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; level = b.dataset.level; $$('button', e.currentTarget).forEach(x => x.setAttribute('aria-pressed', x === b)); });

// ---------- generations: tree + cards ----------
const G = gens.generations;
{ const d = new Date(String(gens.updated).replace(' EST', '').replace(' ', 'T')); $('#gen-updated').textContent = isNaN(d) ? gens.updated : 'Last updated ' + d.getDate() + ' ' + d.toLocaleString('en-GB', { month: 'long' }); }
{
  const WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']; const W = n => WORDS[n] || String(n);
  const num = g => +g.id.replace('gen', ''), isNull = g => g.status === 'null' || g.status === 'fail';
  const list = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  const after19 = G.filter(g => isNull(g) && num(g) > 19), allNull = G.filter(isNull), running = G.filter(g => g.status === 'running');
  const cap = s => s[0].toUpperCase() + s.slice(1);
  const crowdTries = after19.filter(g => (g.aim || 'crowd') === 'crowd'), roomTries = after19.filter(g => g.aim === 'room');
  const pending = G.filter(g => g.status === 'pending');
  const next = running[0] || pending[0] || null;
  const nextName = g => g ? `version ${num(g)}${g.short ? ', ' + g.short : ''}` : '';
  const ranVerb = g => g && g.trains === false ? 'run' : 'trained';
  $$('#null-count').forEach(e => { const a = crowdTries.length ? `${W(crowdTries.length)} later version${crowdTries.length === 1 ? '' : 's'} did not help in loud crowds` : ''; const b = roomTries.length ? `${W(roomTries.length)} room ${roomTries.length === 1 ? 'try' : 'tries'} did not pass` : ''; e.textContent = [a, b].filter(Boolean).join(', and ') || 'no later version has helped'; });
  $$('[data-gen-sentence]').forEach(e => { const parts = []; if (crowdTries.length) parts.push(`${cap(W(crowdTries.length))} later version${crowdTries.length === 1 ? '' : 's'} tried to fix that and did not help in loud crowds`); if (roomTries.length) parts.push(`${crowdTries.length ? W(roomTries.length) : cap(W(roomTries.length))} more version${roomTries.length === 1 ? '' : 's'} tried to teach it echoey rooms and did not pass our rules`); let t = parts.length ? parts.join(', and ') : 'No later version has fixed it yet'; if (running.length) t += `, and ${nextName(running[0])} is ${running[0].trains === false ? 'being checked' : 'training'} right now`; else if (pending.length) t += `, and ${nextName(pending[0])} is next`; e.textContent = t + '.'; });
  $$('[data-gen-nulls-after19]').forEach(e => { const a = crowdTries.length ? 'versions ' + list(crowdTries.map(num)) + ' did not help in loud crowds' : ''; const b = roomTries.length ? 'versions ' + list(roomTries.map(num)) + ' tried to teach it echoey rooms and did not pass our rules' : ''; e.textContent = [a, b].filter(Boolean).join(', and ') || 'no later version has moved it'; });
  $$('[data-gen-next-sentence]').forEach(e => { e.textContent = pending.length ? (running.length ? `Version ${pending.map(num).join(' and ')} is drafted but does not count until version ${running.map(num).join(' and ')} has its result and its review.` : `Version ${pending.map(num).join(' and ')} is drafted and being checked before it ${pending[0].trains === false ? 'runs' : 'trains'}. It does not count until it has ${ranVerb(pending[0])} and been reviewed.`) : 'A new version does not count until it has run and been reviewed.'; });
  $$('[data-gen-wall-sentence]').forEach(e => { let t = 'Training longer, two scoring changes, more hard crowds and blending saved versions did not close the gap.'; if (roomTries.length) t += ` Teaching it echoey rooms (versions ${roomTries.length > 1 ? num(roomTries[0]) + ' to ' + num(roomTries[roomTries.length - 1]) : num(roomTries[0])}) did not pass our rules either.`; if (next) t += ` Next: ${nextName(next)}.`; e.textContent = t; });
  $$('[data-gen-next-line]').forEach(e => { e.textContent = next ? `Version ${num(next)} will be added once it has ${ranVerb(next)}.` : 'The next version will be added once it has run.'; });
  $$('[data-gen-nulls-all]').forEach(e => e.textContent = 'Versions ' + list(allNull.map(num)) + ' did not pass our rules, and they');
}
const live = G.find(g => g.status === 'running');
const chip = $('#live-chip');
if (live) { chip.classList.remove('ok', 'off'); $('#live-text').textContent = `${live.trains === false ? 'Checking' : 'Training'} ${live.label.toLowerCase()} now${live.short ? ', ' + live.short : ''}`; $('#live-chip').dataset.short = `Training ${live.label.toLowerCase()}`; }
else { const last = G[G.length - 1]; chip.classList.add('ok'); $('#live-text').textContent = last.status === 'pending' ? `Next: ${last.label.toLowerCase()}${last.short ? ', ' + last.short : ''}` : `${last.label}: ${statusWord(last)}`; }
setTimeout(fitNav, 0);
(function tree() {
  if (innerWidth < 760) { $('#tree').innerHTML = `<ol class="tree-list">${G.map(g => `<li data-status="${g.status}"><b>${esc(g.label)}</b> <span class="st" data-status="${g.status}">${statusWord(g)}</span></li>`).join('')}</ol>`; $('#tree-desc').textContent = 'The versions, in order. ' + G.map(g => `${g.label}, ${statusWord(g)}: ${g.change}.`).join(' '); return; }
  const W = 1000, step = W / (G.length + 1), yT = 140, H = 260;
  let s = `<svg viewBox="0 0 ${W} ${H}">`;
  // trunk through survivors (baseline/advance); dead branches hang off the trunk and end in ×
  const trunk = G.filter(g => g.status === 'baseline' || g.status === 'advance');
  s += `<path class="trunk" d="${G.map((g, i) => `${i ? 'L' : 'M'}${step * (i + 1)},${yT}`).join('')}"/>`;
  G.forEach((g, i) => {
    const x = step * (i + 1), prevX = step * Math.max(1, i);
    const dead = g.status === 'null' || g.status === 'fail', run = g.status === 'running', pend = g.status === 'pending' || g.status === 'shelved';
    if (dead) s += `<path class="dead" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT - 55} ${x},${yT - 62}"/><line class="x" x1="${x - 6}" y1="${yT - 68}" x2="${x + 6}" y2="${yT - 56}"/><line class="x" x1="${x + 6}" y1="${yT - 68}" x2="${x - 6}" y2="${yT - 56}"/>`;
    if (run) s += `<path class="live" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT + 50} ${x},${yT + 56}"/><circle class="running-ring" cx="${x}" cy="${yT + 56}" r="9"/>`;
    if (pend) s += `<path class="pend" d="M${prevX},${yT} C${prevX + step * .4},${yT} ${x - step * .3},${yT + 50} ${x},${yT + 56}"/>`;
    const ny = dead ? yT - 62 : (run || pend) ? yT + 56 : yT;
    s += `<circle class="node ${g.status}" cx="${x}" cy="${ny}" r="${g.status === 'baseline' ? 11 : 7}"/>`;
    s += `<text x="${x}" y="${dead ? yT - 84 - (i % 2) * 14 : ny + 30 + (i % 2) * 28}" text-anchor="middle">${esc(g.label).replace('Version ', 'v')}</text>${dead ? '' : `<text class="dim" x="${x}" y="${ny + 45 + (i % 2) * 28}" text-anchor="middle">${statusWord(g)}</text>`}`;
  });
  $('#tree').innerHTML = s + '</svg>';
  $('#tree-desc').textContent = 'The versions, in order. ' + G.map(g => `${g.label}, ${statusWord(g)}: ${g.change}.`).join(' ') + ` The versions we kept building on: ${trunk.map(t => t.label).join(', ')}.`;
})();
const FOLD = new Set(['gen16', 'gen17', 'gen18']);
const cardHtml = g => `<article class="gen" data-status="${g.status}" id="${g.id}" aria-labelledby="${g.id}-h">
  <h3 id="${g.id}-h"><span>${esc(g.label)}</span><span class="st" data-status="${g.status}">${GLYPH[g.status]} ${statusWord(g)}</span></h3>
  <p class="change">${esc(g.change)}</p>
  ${g.eta ? `<p class="eta">${esc(g.eta)}</p>` : ''}
  ${(g.numbers || []).length ? `<details class="researchers nums"><summary>the numbers</summary><dl>${(g.numbers || []).map(n => `<dt>${esc(n.label)}</dt><dd>${esc(n.value)}</dd>`).join('')}</dl></details>` : ''}
  ${g.note ? `<p class="note">${esc(g.note)}</p>` : ''}
  <div class="acts">${g.link ? `<a href="${/^https?:/.test(g.link) ? esc(g.link) : esc(repoUrl(g.link) || '#')}" target="_blank" rel="noopener">read the full write-up</a>` : ''}
    <button class="explain-btn ai-only" hidden type="button" data-explain="${g.id}">Explain</button>
</div>
  <div class="explain-slot"></div></article>`;
{
  const nums = a => a.map(g => g.id.replace('gen', ''));
  const list = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  if (innerWidth < 760) {
    const newest = G[G.length - 1], base = G.find(g => g.status === 'baseline');
    const shown = [base, newest].filter(Boolean), rest = G.filter(g => !shown.includes(g));
    $('#gen-cards').innerHTML = shown.map(cardHtml).join('') + `<details class="fold earlier"><summary>every other version (${list(nums(rest))})</summary><div class="gen-cards">${rest.map(cardHtml).join('')}</div></details>`;
  } else {
    const early = G.filter(g => FOLD.has(g.id));
    $('#gen-cards').innerHTML = G.filter(g => !FOLD.has(g.id)).map(cardHtml).join('') + `<details class="fold earlier"><summary>earlier versions (${list(nums(early))})</summary><div class="gen-cards">${early.map(cardHtml).join('')}</div></details>`;
  }
}

// ---------- Gen 21 chart (per-seed −5 dB gains, VAL vs bench, two arms) ----------
(function g21chart() {
  const seeds = g21.seeds.map(String), arms = [{ k: 's48', label: 'Way 1: trained from scratch, twice as long', color: 'var(--signal)' }, { k: 'r48', label: 'Way 2: kept training the old version', color: 'var(--bone)' }];
  const W = 560, H = 300, m = { l: 46, r: 16, t: 20, b: 46 }, ymin = -0.6, ymax = 0.6;
  const groups = []; seeds.forEach(sd => ['val', 'bench'].forEach(p => groups.push({ sd, p })));
  const gw = (W - m.l - m.r) / groups.length, bw = gw / 3;
  const y = v => m.t + (1 - (v - ymin) / (ymax - ymin)) * (H - m.t - m.b);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Bar chart: how much cleaner the hardest crowd got for each training run and test set, for both ways of training longer; table follows"><g class="grid">`;
  for (let v = -0.6; v <= 0.61; v += 0.3) s += `<line x1="${m.l}" x2="${W - m.r}" y1="${y(v)}" y2="${y(v)}"/>`;
  s += `</g><g class="axis"><line x1="${m.l}" x2="${W - m.r}" y1="${y(0)}" y2="${y(0)}" stroke="var(--dim)"/>`;
  for (let v = -0.6; v <= 0.61; v += 0.3) s += `<text x="${m.l - 8}" y="${y(v) + 4}" text-anchor="end">${v.toFixed(1)}</text>`;
  s += `<text transform="translate(12 ${(m.t + H - m.b) / 2}) rotate(-90)" text-anchor="middle">how much cleaner (dB)</text></g>`;
  s += `<line class="req" x1="${m.l}" x2="${W - m.r}" y1="${y(0.3)}" y2="${y(0.3)}"/><text class="req-l" x="${W - m.r}" y="${y(0.3) - 6}" text-anchor="end">needed: +0.30 on both</text>`;
  groups.forEach((g, i) => {
    const x0 = m.l + i * gw + gw * 0.15;
    arms.forEach((a, j) => { const v = g21.per_seed[g.sd][a.k][g.p + '_gain_m5'][0]; const top = Math.min(y(v), y(0)), h = Math.abs(y(v) - y(0)); s += `<rect x="${x0 + j * (bw + 2)}" y="${top}" width="${bw}" height="${Math.max(h, 1)}" fill="${a.color}" rx="2"><title>training run ${g.sd}, ${g.p === 'val' ? 'test 1' : 'test 2'}, ${a.label}: ${fmt(v)} dB</title></rect>`; });
    s += `<text class="axis" x="${x0 + bw}" y="${H - 28}" text-anchor="middle" style="fill:var(--dim);font-family:var(--mono);font-size:11px">${g.p === 'val' ? 'test 1' : 'test 2'}</text>`;
    if (g.p === 'val') s += `<text x="${x0 + gw * 0.85}" y="${H - 12}" text-anchor="middle" style="fill:var(--bone);font-family:var(--mono);font-size:11px">training run ${seeds.indexOf(g.sd) + 1}</text>`;
  });
  $('#g21-chart').innerHTML = s + '</svg>';
  $('#g21-legend').innerHTML = arms.map(a => `<span><i style="background:${a.color}"></i>${a.label}</span>`).join('') + `<span><i class="dash" style="color:var(--hot)"></i>what we needed: +0.30</span>`;
  const mg = g21.arms;
  $('#g21-table').innerHTML = `<table><thead><tr><th scope="col">Training run</th><th scope="col">Test set</th>${arms.map(a => `<th scope="col" class="num">${a.label}</th>`).join('')}</tr></thead><tbody>${groups.map(g => `<tr><td>training run ${seeds.indexOf(g.sd) + 1}</td><td>${g.p === 'val' ? 'test 1' : 'test 2'}</td>${arms.map(a => `<td class="num">${fmt(g21.per_seed[g.sd][a.k][g.p + '_gain_m5'][0])}</td>`).join('')}</tr>`).join('')}<tr><td><b>average</b></td><td>test 1</td><td class="num"><b>${fmt(mg.s48.mean_gains.val_gain_m5[0])}</b></td><td class="num"><b>${fmt(mg.r48.mean_gains.val_gain_m5[0])}</b></td></tr><tr><td><b>average</b></td><td>test 2</td><td class="num"><b>${fmt(mg.s48.mean_gains.bench_gain_m5[0])}</b></td><td class="num"><b>${fmt(mg.r48.mean_gains.bench_gain_m5[0])}</b></td></tr><tr><td colspan="2">good enough (at least +0.30 on both)?</td><td>${mg.s48.qualifies ? 'yes' : 'no'}</td><td>${mg.r48.qualifies ? 'yes' : 'no'}</td></tr></tbody></table>`;
})();

// ---------- VAL trajectory chart ----------
(function valchart() {
  const names = { gen19: 'Version 19 (our best)', gen22_cap30: 'Version 22 (new scoring)', gen23: 'Version 23 (second scoring)' };
  const cols = { gen19: 'var(--signal)', gen22_cap30: 'var(--bone)', gen23: 'var(--amber)' };
  const keys = Object.keys(traj.series);
  const xs = traj.series.gen19.filter(e => e.step > 0).map(e => e.step);
  lineChart('val-chart', {
    xs, xl: 'training progress (thousands of steps)', yl: 'how much cleaner (dB)', ymin: -0.8, ymax: 1.2, ytick: 0.4, xfmt: v => (v / 1000) + 'k',
    ariaLabel: 'Line chart: how much cleaner the hardest crowd got as training went on, for versions 19 and 22; table follows',
    series: keys.map(k => ({ k, label: names[k] || k, color: cols[k] || 'var(--dim)', w: 2, ys: traj.series[k].filter(e => e.step > 0).map(e => e.m5), direct: null }))
  });
  $('#val-legend').innerHTML = keys.map(k => `<span><i style="background:${cols[k] || 'var(--dim)'}"></i>${names[k] || k}</span>`).join('') + `<span class="muted">the very start (−23.6 dB) is left off so the rest is readable</span>`;
  $('#val-table').innerHTML = `<table><thead><tr><th scope="col">Training progress</th>${keys.map(k => `<th scope="col" class="num">${names[k] || k}</th>`).join('')}</tr></thead><tbody>${traj.series.gen19.map((e, i) => `<tr><td class="num">${e.step}</td>${keys.map(k => `<td class="num">${traj.series[k][i] ? fmt(traj.series[k][i].m5) : '—'}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
})();

// ---------- Muse: health → show AI UI; Ask; Explain; Brief ----------
{ const fab = $('#ask-fab'); if (fab) { let last = scrollY; const near = () => ['ask', 'meta-lab'].some(id => { const e = $('#' + id); if (!e) return false; const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; }); addEventListener('scroll', () => { const up = scrollY < last - 2; last = scrollY; fab.classList.toggle('show', up && !near() && scrollY > innerHeight); }, { passive: true }); } }
$$('.ai-only').forEach(e => { e.hidden = false; e.classList.add('ai-wait'); });
const health = await api.health();
if (!health) { $$('.ai-only').forEach(e => { e.hidden = true; e.classList.remove('ai-wait'); }); const off = $('#ask-off'); if (off) off.hidden = false; } else $$('.ai-only').forEach(e => e.classList.remove('ai-wait'));
if (health) {
  $$('.ai-only').forEach(e => { e.hidden = false; e.classList.add('ai-ready'); });
  $('#ask-off').hidden = true;
  const SUGGEST = [
    'Why does it struggle when the crowd is louder than the voice?',
    'What did version 22 change and why did it not help?',
    'Is this better than his Nucleus 6?',
    'What would have to happen before Graham could try this?',
    'Did training it longer help?',
    'Who checks the results, and what do they check?'
  ];
  $('#chips').innerHTML = SUGGEST.map(q => `<button type="button" class="chip" role="listitem">${esc(q)}</button>`).join('');
  $('#chips').addEventListener('click', e => { const b = e.target.closest('.chip'); if (!b) return; $('#q').value = b.textContent; ask(b.textContent); setTimeout(() => $('#answer').scrollIntoView({ block: 'start', behavior: 'smooth' }), 50); });
  $('#ask-form').addEventListener('submit', e => { e.preventDefault(); const q = $('#q').value.trim(); if (q) ask(q); });
  // the last "*Still needs to be verified on the Nucleus 6." line becomes a quiet footnote
  function renderAnswer(t) {
    const lines = String(t || '').trim().split('\n'); let foot = '';
    if (lines.length && /^\*\s*still needs/i.test(lines[lines.length - 1].trim())) foot = lines.pop().trim().replace(/^\*\s*/, '');
    return mdLite(lines.join('\n')) + (foot ? `<p class="footnote">* ${esc(foot)}</p>` : '');
  }
  // hero entry + persistent phone entry both route into the Ask section
  const hf = $('#hero-ask'); if (hf) hf.addEventListener('submit', e => { e.preventDefault(); const q = $('#hq').value.trim(); if (!q) return; $('#q').value = q; location.hash = '#ask'; ask(q); });
  async function ask(q) {
    const ans = $('#answer'), th = $('#thinking'), steps = $('#steps'), out = $('#answer-text'), btn = $('#ask-btn');
    ans.classList.add('on'); th.hidden = false; steps.innerHTML = ''; out.innerHTML = ''; btn.disabled = true; window.__musePulse = 1; const t0 = Date.now(); let el = th.querySelector('.elapsed'); if (!el) { el = document.createElement('span'); el.className = 'elapsed'; th.appendChild(el); } el.textContent = '0 s'; const tick = setInterval(() => { el.textContent = Math.round((Date.now() - t0) / 1000) + ' s'; if (th.hidden) clearInterval(tick); }, 1000);
    try {
      const r = await api.ask(q);
      steps.innerHTML = (r.steps || []).map(s => `<li>${esc(s.output || s.input || s.tool || '')}</li>`).join('');
      out.innerHTML = renderAnswer(r.answer) + `<p class="small muted" style="margin:12px 0 0">Answered by Muse (Meta). Based only on the research record.</p>`;
    } catch (err) { out.innerHTML = `<p class="err">${esc(err.message)} <button type="button" class="explain-btn retry">Try again</button></p>`; out.querySelector('.retry').addEventListener('click', () => ask(q)); }
    finally { th.hidden = true; btn.disabled = false; window.__musePulse = 0; }
  }
  document.addEventListener('click', async e => {
    const b = e.target.closest('[data-explain],[data-brief]'); if (!b) return;
    const isBrief = 'brief' in b.dataset, id = b.dataset.explain || b.dataset.brief;
    let slot = b.closest('tr') ? b.closest('tr').nextElementSibling : b.closest('.gen') ? $('.explain-slot', b.closest('.gen')) : (b.closest('.col') || b.closest('section')).querySelector('.explain-slot');
    if (b.closest('tr')) {
      if (!slot || !slot.classList.contains('explain-row')) { slot = document.createElement('tr'); slot.className = 'explain-row'; slot.innerHTML = `<td colspan="5"></td>`; b.closest('tr').after(slot); }
      slot = slot.firstElementChild;
    }
    window.__musePulse = 1; slot.innerHTML = `<div class="explain-out"><span class="thinking"><i aria-hidden="true"></i>Muse is writing${isBrief ? ' a brief' : ` for ${level === 'parent' ? 'a parent' : 'a researcher'}`}… <span class="elapsed">0 s</span></span></div>`; const t0 = Date.now(); const tick = setInterval(() => { const el = slot.querySelector('.elapsed'); if (!el) { clearInterval(tick); return; } el.textContent = Math.round((Date.now() - t0) / 1000) + ' s'; }, 1000);
    b.disabled = true;
    const ctx = b.closest('tr') ? b.closest('tr').querySelector('td') : b.closest('.kv-line') || (b.closest('.gen') && b.closest('.gen').querySelector('h3 span, .change')); const label = b.dataset.name ? b.dataset.name : ctx ? ctx.cloneNode(true).textContent.replace(/\s*(Show|Hide)?\s*notes for researchers[\s\S]*$/i, '').replace(/\bExplain\b/g, '').replace(/\s+/g, ' ').trim().slice(0, 160) : '';
    try { const r = isBrief ? await api.brief(id) : await api.explain(id, level, label); slot.innerHTML = `<div class="explain-out">${renderAnswer(r.text)}<p class="small muted" style="margin:8px 0 0">Explained by Muse (Meta) for ${level === 'parent' ? 'a parent' : 'a researcher'}</p></div>`; }
    catch (err) { slot.innerHTML = `<div class="explain-out err">${esc(err.message)} <button type="button" class="explain-btn retry">Try again</button></div>`; slot.querySelector('.retry').addEventListener('click', () => b.click()); }
    finally { b.disabled = false; window.__musePulse = 0; }
  });
} else if (!live) {
  chip.classList.add('off');
}
// text equivalent of the wave state (aria-live)
{ const ws = $('#wave-state'); if (ws) { let lastTxt = '', lastAt = 0, lastSec = '', lastKey = -1; setInterval(() => { const st = window.__waveState; if (!st) return; const c = st.C; const secEl = document.elementFromPoint(innerWidth / 2, innerHeight / 2); const sec = secEl ? ((secEl.closest('section') || {}).id || '') : ''; const key = Math.round(c.clarity * 10) / 10; if (sec === lastSec && Math.abs(key - lastKey) < 0.1 && !window.__mlFuzz && c.ears < 0.5) return; let txt = c.shake > 0.5 ? 'The line is shaking hard, with a calm centre.' : c.wall > 0.25 ? 'The line has hit a wall.' : c.bands > 0.5 ? 'The line has split into 22 bands.' : c.ears > 0.5 ? (c.clean < 0.5 ? 'The line is fuzzy: no cleanup.' : c.drift > 0.5 ? 'Two lines, drifting apart.' : 'The two lines have become one.') : (window.__mlFuzz > 0) ? 'The line has gone fuzzy: the recording before cleanup.' : (window.__mlFuzz < 0) ? 'The line is clearer: the recording after cleanup.' : (sec === 'scorecard' && c.wall > 0.15) ? 'The line hits the wall again: the one check it fails.' : (sec === 'attempts' && c.waver > 0.2) ? 'The line wobbles but does not clear: those tries did not pass.' : (c.waver > 0.5 && c.beat < 0.3) ? 'The line wavers, unsure.' : (c.kick > 0.3 || c.beat > 0.3 || (window.__dancePlaying && st.T.beat > 0.1)) ? 'A rhythm is running through the line.' : (c.waver > 0.3 && c.clarity > 0.3) ? 'The line wobbles but does not change: those versions did not help.' : c.clarity > 0.75 ? 'The line is mostly clear.' : c.clarity > 0.6 ? 'The line is clear.' : c.clarity > 0.3 ? 'The line is clearing up.' : 'The line is fuzzy, like a crowd.'; if (sec === 'tests') txt = 'The line wavers, unsure.'; if (txt === lastTxt || performance.now() - lastAt < 1200) return; lastTxt = txt; lastSec = sec; lastKey = key; lastAt = performance.now(); ws.textContent = txt; }, 500); } }
