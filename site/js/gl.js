// The sound wave behind the page. One GPU particle cloud, reshaped by scroll.
// The central device: uClarity (0 = a fuzzy band of many talkers, 1 = one clean line), driven by
// story beats and by REAL bench numbers (data/bench_snr.json). Story modes on top:
//   shake (jackhammer with a silent centre), waver (no answers), beat (music / dancing video),
//   bands (22 electrodes, ~8 lit, in the implant chapter), ears (two lines that drift apart or lock), wall.
// Never fades to nothing: the wave runs the whole way down, thinner and quieter after the wall.
import * as THREE from '../vendor/three.module.min.js';

const host = document.getElementById('gl');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true, powerPreference: 'low-power', preserveDrawingBuffer: true });
window.__gl = renderer;
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
renderer.setClearColor(0x000000, 0);
host.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 0, 9);

const isSmall = innerWidth < 700;
const N = isSmall ? 12000 : 24000;
const crowd = new Float32Array(N * 3), voice = new Float32Array(N * 3), wall = new Float32Array(N * 3), seed = new Float32Array(N);
let s = 20261117; const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
const env = x => { const t = x * 0.9 + 3; return (0.55 + 0.45 * Math.sin(t * 2.1)) * (0.6 + 0.4 * Math.sin(t * 0.7 + 1.3)); };
for (let i = 0; i < N; i++) {
  const i3 = i * 3;
  // crowd: twelve overlapping talker waveforms, a thick fuzzy band
  const line = i % 12, x = (rnd() - 0.5) * 16;
  const ph = line * 1.7, f = 1.2 + line * 0.19, amp = 0.5 + 0.6 * ((line * 7) % 5) / 4;
  crowd[i3] = x;
  crowd[i3 + 1] = (line - 5.5) * 0.5 + Math.sin(x * f + ph) * amp * (0.6 + 0.4 * Math.sin(x * 0.6 + ph)) + (rnd() - 0.5) * 0.18;
  crowd[i3 + 2] = -1.5 + (line % 4) * 0.6 + (rnd() - 0.5) * 0.5;
  // voice: one clean speech-like line (same x, so each particle travels straight home)
  const e = env(x);
  voice[i3] = x; voice[i3 + 1] = Math.sin(x * 2.2) * e * 1.7 + (rnd() - 0.5) * 0.08; voice[i3 + 2] = (rnd() - 0.5) * 0.2;
  // wall: a dense plane facing the camera
  wall[i3] = (rnd() - 0.5) * 18; wall[i3 + 1] = (rnd() - 0.5) * 10; wall[i3 + 2] = -1.5 + (rnd() - 0.5) * 0.12;
  seed[i] = rnd();
}
const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(crowd, 3));
geo.setAttribute('aVoice', new THREE.BufferAttribute(voice, 3));
geo.setAttribute('aWall', new THREE.BufferAttribute(wall, 3));
geo.setAttribute('aSeed', new THREE.BufferAttribute(seed, 1));

const U = {
  uTime: { value: 0 }, uClarity: { value: 0.1 }, uShake: { value: 0 }, uWaver: { value: 0 }, uBeat: { value: 0 },
  uBands: { value: 0 }, uEars: { value: 0 }, uEarsDrift: { value: 0 }, uEarsClean: { value: 1 }, uKick: { value: 0 }, uPulse: { value: 0 }, uKickGain: { value: 2.4 }, uStillC: { value: new THREE.Vector2(3.2, 0) }, uWall: { value: 0 }, uThin: { value: 0 },
  uPR: { value: renderer.getPixelRatio() }, uScale: { value: isSmall ? 1.15 : 1.15 }, uXS: { value: 1 }, uYOff: { value: 0 }, uAlphaK: { value: isSmall ? 1.0 : 1.2 },
  uBone: { value: new THREE.Color('#c9c2b2') }, uSignal: { value: new THREE.Color('#5fdcff') }, uHot: { value: new THREE.Color('#ff5c3f') }
};
const mat = new THREE.ShaderMaterial({
  uniforms: U, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `
    attribute vec3 aVoice; attribute vec3 aWall; attribute float aSeed;
    uniform float uTime, uClarity, uShake, uWaver, uBeat, uBands, uEars, uEarsDrift, uEarsClean, uWall, uThin, uPR, uScale, uXS, uYOff, uKick, uPulse, uKickGain; uniform vec2 uStillC;
    varying float vClar, vSeed, vDepth, vStill, vWall, vLit, vThin, vEar, vLinked;
    vec3 hash3(vec3 p){ p = fract(p*0.3183099+vec3(.1,.2,.3)); p *= 17.0; return fract(vec3(p.x*p.y*p.z*(p.x+p.y+p.z)))*2.0-1.0; }
    float ease(float t){ return t*t*(3.0-2.0*t); }
    void main(){
      float c = ease(clamp(uClarity, 0.0, 1.0));
      vec3 fuzz = hash3(position*1.9 + floor(uTime*1.2 + aSeed*20.0)) * vec3(0.12, 0.22, 0.3) * (1.0-c);
      vec3 p = mix(position + fuzz, aVoice, c);
      p.y += c * sin(p.x*2.6 + uTime*1.6 + aSeed*6.28) * 0.08;
      // jackhammer: violent field + shock rings, but a flat silent centre (Graham, asleep)
      float still = 1.0 - smoothstep(1.6, 3.0, length(position.xy - uStillC));
      float ring = sin(length(position.xy - uStillC)*3.5 - uTime*16.0);
      vec3 quake = hash3(position*9.0 + floor(uTime*28.0)) * vec3(1.4, 1.6, 0.6) * uShake * (1.0-still);
      quake.y += (ring*0.6 + sin(uTime*60.0 + position.x*3.0)*0.15) * uShake * (1.0-still);
      quake.z += ring*0.6 * uShake * (1.0-still);
      p += quake;
      p.y = mix(p.y, uStillC.y + (aSeed-0.5)*0.15, still * uShake);
      p.x = mix(p.x, uStillC.x + (position.x - uStillC.x), still * uShake);
      // weeks of tests: slow, uncertain wavering
      p.y += uWaver * (sin(p.x*0.7 + uTime*0.7 + aSeed) * 0.5 + sin(p.x*1.9 - uTime*0.4)*0.2);
      // music: a rhythm runs through it
      p.y += uBeat * sin(p.x*1.4 + uTime*8.0) * 1.3;
      p.y += uKick * sin(p.x*0.9 + aSeed*3.0) * uKickGain * (1.0 + 0.5*sin(uTime*30.0));   // lands on the beat
      p.y += uPulse * sin(p.x*2.0 - uTime*5.0) * 0.35;                               // Muse is writing
      // the implant: 22 horizontal bands, about 8 lit at a time
      float band = floor(aSeed*22.0);
      float lit = step(0.63, fract(band*0.618 + floor(uTime*2.5)*0.37));
      p = mix(p, vec3(aVoice.x, (band - 10.5)*0.42 + (aSeed*22.0 - band - 0.5)*0.38, 0.0), uBands);
      vLit = mix(1.0, lit, uBands);
      // two ears: split into two lines; "separate" lets them drift apart, "linked" locks them
      float ear = step(0.5, aSeed)*2.0-1.0;
      vec3 earP = aVoice; earP.y = aVoice.y * (1.0 + uEarsDrift*ear*0.35) + ear*uEarsDrift*1.2; earP.x += uEarsDrift*ear*0.6*sin(uTime*0.9);
      earP = mix(position + fuzz*2.0, earP, uEarsClean);   // no cleanup: fuzzy crowd, not two lines
      p = mix(p, earP, uEars);
      vEar = ear * uEars;
      p = mix(p, aWall, uWall);
      p.x *= uXS; p.y += uYOff;
      vec4 mv = modelViewMatrix * vec4(p,1.0);
      gl_Position = projectionMatrix * mv;
      float size = mix(1.0, 1.4, uEars*(1.0-uEarsDrift)*uEarsClean) * mix(1.0, 1.6, uBands) * mix(2.6, 2.2, c) * (1.0 + 0.9*uShake*(1.0-still)) * mix(1.0, 1.9, uWall) * mix(1.0, 0.95, uThin) * mix(1.0, 1.5, uEars) * uPR * uScale;
      gl_PointSize = size * (12.0 / -mv.z);
      vClar = c; vSeed = aSeed; vDepth = -mv.z; vStill = still*uShake; vWall = uWall; vThin = uThin; vLinked = uEars*(1.0-uEarsDrift)*uEarsClean;
    }`,
  fragmentShader: `
    precision mediump float;
    uniform vec3 uBone, uSignal, uHot; uniform float uAlphaK;
    varying float vClar, vSeed, vDepth, vStill, vWall, vLit, vThin, vEar, vLinked;
    void main(){
      vec2 q = gl_PointCoord - 0.5; float d = dot(q,q); if (d > 0.25) discard;
      float soft = smoothstep(0.25, 0.0, d);
      vec3 col = mix(uBone, uSignal, vClar * (0.6 + 0.4*vSeed));
      col = mix(col, vEar < 0.0 ? uSignal : uBone, abs(vEar));   // left ear cyan, right ear bone
      col = mix(col, uSignal, vLinked);                               // linked: both lines go signal-cyan
      col = mix(col, uHot, vWall);
      col = mix(col, uSignal*0.6, vStill);
      float a = (0.55 + 0.35*vClar) * soft * uAlphaK;
      a *= mix(1.0, 1.1, vStill);
      a *= 0.35 + 1.6*vLit;
      a *= mix(1.0, 1.0, vThin);
      a *= mix(1.0, 2.2, vLinked);
      a *= mix(1.0, 0.35 + 0.65*step(0.985, fract(vSeed*7.0)), vWall);
      a *= clamp(1.7 - vDepth*0.1, 0.3, 1.0);
      gl_FragColor = vec4(col, a);
    }`
});
scene.add(new THREE.Points(geo, mat));

// ---------- story beats ----------
let bench = null;
fetch('data/bench_snr.json').then(r => r.json()).then(b => { bench = b; measure(); }).catch(() => {});
// real numbers: this model's gain at an SNR divided by the cheating upper bound at that SNR
const ratioAt = v => {
  if (!bench) return 0.3;
  const S = bench.snrs, g = bench.systems.gen19, o = bench.systems.oracle_noncausal;
  let i = S.findIndex(x => x >= v); if (i < 0) i = S.length - 1;
  const lo = Math.max(0, i - 1), hi = i, t = hi === lo ? 0 : (v - S[lo]) / (S[hi] - S[lo]);
  const gg = g[String(S[lo])] * (1 - t) + g[String(S[hi])] * t, oo = o[String(S[lo])] * (1 - t) + o[String(S[hi])] * t;
  return Math.max(0, gg / oo);
};
const show = r => Math.pow(r, 0.6);  // visual scaling of the real ratio: 0.10 at −5 dB → 0.25, 0.43 at 0 dB → 0.6
const modelLevel = () => bench ? show(bench.summary_seed_mean.gen19.crowd.d_sisdr / bench.summary_seed_mean.oracle_noncausal.crowd.d_sisdr) : 0.5;

const $ = id => document.getElementById(id);
const els = () => ({ born: $('born'), tests: $('tests'), music: $('music'), crowd: $('crowd'), dancing: $('dancing'),
  model: $('model'), implant: $('implant'), dir: document.querySelector('.dir-wrap'), failRow: document.querySelector('#score-table tr.fail'), sliderBox: document.querySelector('.slider-box'), meta: $('meta-lab'), impStage: document.querySelector('#imp-stage') || document.querySelector('#implant .imp-steps'), wall: $('wall'), gens: $('generations'), attempts: $('attempts'), graham: $('graham'), honest: $('honest') });
let E = els();
const clamp01 = v => Math.min(1, Math.max(0, v));
const baseAlpha = U.uAlphaK.value;
const top = el => el ? el.getBoundingClientRect().top + scrollY : 0;
const presence = (el, pad = 0.15) => {   // share of the viewport this section fills now (0..1)
  if (!el) return 0;
  const r = el.getBoundingClientRect(), h = innerHeight;
  const vis = Math.min(r.bottom, h) - Math.max(r.top, 0);
  return clamp01((vis / Math.min(h, r.height) - pad) / (1 - pad));
};
const T = { clarity: 0.1, shake: 0, waver: 0, beat: 0, bands: 0, ears: 0, drift: 0.5, clean: 1, wall: 0, thin: 0, kick: 0, pulse: 0 };
const C = { ...T }; window.__waveState = { T, C, U };
let sliderClar = null, counterDb = 0;
function measure() {
  E = els();
  const y = scrollY, h = innerHeight, ml = modelLevel();
  const mh = E.model ? E.model.offsetHeight : 0;
  const beats = [[0, 0.1], [top(E.tests), 0.08], [top(E.music), 0.65], [top(E.crowd), 0.15], [top(E.dancing), 0.3],
    [top(E.model), 0.15], [top(E.model) + mh * 0.8, ml]];
  if (E.implant) beats.push([top(E.implant), ml]);
  beats.push([top(E.wall), ml], [top(E.gens), ml], [top(E.attempts), ml], [top(E.graham), ml], [top(E.honest), 0.8], [document.body.scrollHeight, 0.8]);
  const yy = y + h * 0.5;
  let cl = beats[0][1];
  for (let i = 0; i < beats.length - 1; i++) {
    const [a, va] = beats[i], [b, vb] = beats[i + 1];
    if (yy >= a && yy < b) { cl = va + (vb - va) * (b > a ? (yy - a) / (b - a) : 0); break; }
    if (yy >= b) cl = vb;
  }
  const pw = presence(E.wall);
  if (pw > 0 && sliderClar != null) cl = cl * (1 - pw) + sliderClar * pw;   // the wall: clarity is the slider's real ratio
  T.clarity = cl;
  T.shake = presence(E.born, 0.25);
  T.waver = Math.max(presence(E.tests), 0.35 * presence(E.gens));
  const lvl = window.__waveLevel;
  T.beat = Math.max(presence(E.music) * 0.9, presence(E.dancing) * (lvl > 0 ? lvl * 1.2 : 0.18));
  T.bands = Math.max(presence(E.impStage, 0.05), presence(document.querySelector('.imp-head'), 0.05));
  T.ears = presence(E.dir, 0.05);
  T.drift = window.__ears === 'separate' ? 1 : 0;
  T.wall = pw > 0 && sliderClar != null ? Math.min(pw, presence(E.sliderBox, 0.05)) * clamp01((0.32 - sliderClar) / 0.1) : 0;   // slams in only toward −5 dB, only while the slider is on screen
  const pf = presence(E.failRow, 0.05); if (pf > 0.3 && sliderClar != null) { T.wall = Math.max(T.wall, 0.25 * pf); T.clarity = Math.min(T.clarity, sliderClarity(-5)); }
  T.waver = Math.max(T.waver, 0.35 * presence(E.attempts));
  T.thin = clamp01((y - (top(E.wall) + (E.wall ? E.wall.offsetHeight : 0))) / h) * (1 - Math.min(1, 3 * Math.max(presence(E.dir, 0.05), presence(E.gens))));
  const afterModel = y + h * 0.5 > top(E.model);
  counterDb = bench && afterModel ? bench.summary_seed_mean.gen19.crowd.d_sisdr * clamp01((cl - 0.15) / Math.max(0.01, ml - 0.15)) : 0;
}
const sliderClarity = v => show(ratioAt(v)) * (0.55 + 0.45 * (v + 5) / 15);   // +10 → ~0.66, 0 → ~0.46, −5 → ~0.14
document.addEventListener('input', e => { if (e.target && e.target.id === 'snr') { sliderClar = sliderClarity(+e.target.value); measure(); } });
addEventListener('load', () => { const sl = $('snr'); if (sl) sliderClar = sliderClarity(+sl.value); measure(); });

function resize() { const w = innerWidth, h = innerHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); U.uXS.value = Math.min(1, Math.max(0.35, camera.aspect * 0.6)); U.uYOff.value = camera.aspect < 0.9 ? -1.2 : 0; U.uStillC.value.set(camera.aspect < 0.9 ? 0 : 3.2, camera.aspect < 0.9 ? 2.2 : 0); }
addEventListener('resize', () => { resize(); measure(); });
addEventListener('scroll', measure, { passive: true });
resize(); measure();

let running = !document.hidden, t0 = performance.now(), gensPhase = 0;
document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running && !reduce) loop(); });

function frame(now) {
  const t = (now - t0) / 1000; U.uTime.value = t;
  // live inputs every frame (not only on scroll): the clip's sound level and the ear toggle
  const lvl = window.__waveLevel; T.beat = Math.max(presence(E.music) * 0.9, presence(E.dancing) * (lvl > 0 ? lvl * 1.2 : 0.3));
  T.drift = window.__ears === 'separate' ? 1 : 0;
  const pd = presence(E.dir, 0.05); if (pd > 0.2) T.clarity = window.__ears === 'none' ? 0.3 : 0.85;
  T.clean = window.__ears === 'none' ? 0 : 1;
  const mf = window.__mlFuzz || 0; if (mf !== 0 && presence(E.meta) > 0.2) { T.clarity = mf > 0 ? 0.1 : 0.8; T.waver = Math.max(T.waver, mf > 0 ? 0.5 : 0); }
  const pm = Math.max(presence(E.music), (lvl > 0 ? 0 : presence(E.dancing))); const synth = pm > 0.2 ? (Math.sin(t * Math.PI * 4) > 0.9 ? 0.6 * pm : 0) : 0;   // a gentle 2 Hz pulse while the music line is on screen
  T.kick = Math.max(window.__kick || 0, synth, (lvl > 0 ? (presence(E.dancing) > 0.2 && Math.sin(t * Math.PI * 4) > 0.9 ? 0.3 : 0) : 0), C.kick * 0.82);          // short decaying pulse on each beat
  T.pulse = window.__musePulse ? 0.6 + 0.4 * Math.sin(t * 3.0) : 0;
  for (const k in T) C[k] += (T[k] - C[k]) * (k === 'shake' ? 0.12 : k === 'beat' ? 0.35 : k === 'kick' ? 0.9 : 0.08);
  let cl = C.clarity;
  if (E.gens && presence(E.gens) > 0) { gensPhase += 0.05; cl += Math.sin(gensPhase) * 0.3 * presence(E.gens); }  // nulls: a flat wobble
  U.uClarity.value = cl; U.uShake.value = C.shake; U.uWaver.value = C.waver; U.uBeat.value = C.beat;
  U.uBands.value = C.bands; U.uEars.value = C.ears; U.uEarsDrift.value = C.drift; U.uEarsClean.value = C.clean; U.uKick.value = C.kick; U.uPulse.value = C.pulse; U.uKickGain.value = (window.__waveLevel > 0) ? 3.5 : 2.4;
  U.uAlphaK.value = baseAlpha * 1 * (1 + 0.5 * C.wall) * (isSmall ? 1 + 0.5 * C.thin : 1) * (1 + 0.3 * presence(E.music)) * (isSmall && C.ears > 0.5 ? 1.4 : 1) * ((window.__mlFuzz || 0) > 0 && presence(E.meta) > 0.2 ? 1.8 : 1); U.uWall.value = C.wall; U.uThin.value = C.thin;
  camera.position.z = 9 - 0.6 * cl - 4.5 * C.wall * C.wall;
  camera.position.x = Math.sin(t * 0.1) * 0.25 + (Math.random() - 0.5) * 0.12 * C.shake;
  camera.position.y = (Math.random() - 0.5) * 0.12 * C.shake;
  renderer.render(scene, camera);
}
function loop() { if (!running || reduce) return; frame(performance.now()); requestAnimationFrame(loop); }
if (reduce) {
  let tick = null;
  const still = () => { measure(); Object.assign(C, T); frame(t0 + 1000); };
  still();
  addEventListener('scroll', () => { if (!tick) tick = setTimeout(() => { tick = null; still(); }, 120); }, { passive: true });
} else {
  loop();
}
