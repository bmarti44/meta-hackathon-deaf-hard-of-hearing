// WebGL layer: one GPU particle system morphing between three shapes as you scroll.
//   shape 0 "crowd"  — thousands of voices scattered through the room (hero)
//   shape 1 "voice"  — the same particles resolve onto one speech-like waveform (Part 1–2)
//   shape 2 "wall"   — then slam into a flat vertical wall at −5 dB (Part 3)
// All morphing happens in the vertex shader from three position attributes; JS only pushes
// two scroll uniforms per frame. Reduced motion renders one static "voice" frame and stops.
import * as THREE from '../vendor/three.module.min.js';

const host = document.getElementById('gl');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true, powerPreference: 'low-power' });
} catch (e) { host.style.opacity = '0.6'; throw e; }
renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));
renderer.setClearColor(0x000000, 0);
host.appendChild(renderer.domElement);

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 0, 9);

const isSmall = innerWidth < 700;
const N = isSmall ? 9000 : 22000;
const crowd = new Float32Array(N * 3), voice = new Float32Array(N * 3), wall = new Float32Array(N * 3);
const seed = new Float32Array(N);
// deterministic pseudo-random so the shape is identical every load
let s = 20261117; const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
// speech-like envelope: a few "syllables" of varying amplitude along x
const env = x => { const t = x * 0.9 + 3; return (0.55 + 0.45 * Math.sin(t * 2.1)) * (0.6 + 0.4 * Math.sin(t * 0.7 + 1.3)); };
for (let i = 0; i < N; i++) {
  const i3 = i * 3;
  // crowd: a broad slab with clumps (many talkers), spread deep in z
  const r = Math.pow(rnd(), 0.35) * 7.5, a = rnd() * Math.PI * 2;
  crowd[i3] = Math.cos(a) * r * 1.4 + (rnd() - 0.5) * 2;
  crowd[i3 + 1] = Math.sin(a) * r * 0.75 + (rnd() - 0.5) * 2;
  crowd[i3 + 2] = (rnd() - 0.5) * 9 - 1;
  // voice: a horizontal waveform band, thickness follows the envelope
  const x = (rnd() - 0.5) * 13;
  const e = env(x);
  const y = (rnd() - 0.5) * 2 * e * 1.9 * Math.pow(rnd(), 0.5);
  voice[i3] = x; voice[i3 + 1] = y; voice[i3 + 2] = (rnd() - 0.5) * 0.6;
  // wall: a flat plane facing the camera, slightly wider than the viewport, tiny grain
  wall[i3] = (rnd() - 0.5) * 16; wall[i3 + 1] = (rnd() - 0.5) * 9; wall[i3 + 2] = -1.5 + (rnd() - 0.5) * 0.15;
  seed[i] = rnd();
}
const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(crowd, 3));
geo.setAttribute('aVoice', new THREE.BufferAttribute(voice, 3));
geo.setAttribute('aWall', new THREE.BufferAttribute(wall, 3));
geo.setAttribute('aSeed', new THREE.BufferAttribute(seed, 1));

const uniforms = {
  uTime: { value: 0 }, uMix1: { value: 0 }, uMix2: { value: 0 }, uPR: { value: renderer.getPixelRatio() },
  uBone: { value: new THREE.Color('#aea89b') }, uSignal: { value: new THREE.Color('#5fdcff') }, uHot: { value: new THREE.Color('#ff5c3f') },
  uScale: { value: isSmall ? 0.75 : 1 }, uShake: { value: 0 }
};
const mat = new THREE.ShaderMaterial({
  uniforms, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
  vertexShader: `
    attribute vec3 aVoice; attribute vec3 aWall; attribute float aSeed;
    uniform float uTime, uMix1, uMix2, uPR, uScale, uShake;
    varying float vMix1, vMix2, vSeed, vDepth, vStill;
    // cheap 3D hash noise for the "murmur" of the crowd
    vec3 hash3(vec3 p){ p = fract(p*0.3183099+vec3(.1,.2,.3)); p *= 17.0; return fract(vec3(p.x*p.y*p.z*(p.x+p.y+p.z)))*2.0-1.0; }
    float ease(float t){ return t*t*(3.0-2.0*t); }
    void main(){
      float m1 = ease(clamp(uMix1,0.,1.)); float m2 = ease(clamp(uMix2,0.,1.));
      // crowd murmur: every particle jitters, fading as it resolves into the voice
      vec3 jit = hash3(position*1.7 + floor(uTime*0.8 + aSeed*20.0)) * 0.35 * (1.0-m1);
      // the jackhammer: a violent reverberation field; inside a quiet radius around the centre
      // (the sleeping newborn's world) nothing moves at all
      float still = 1.0 - smoothstep(1.6, 3.2, length(position.xy));
      vec3 quake = hash3(position*9.0 + floor(uTime*28.0)) * vec3(0.9, 0.9, 0.3) * uShake * (1.0-still) * (1.0-m1);
      quake.y += sin(uTime*60.0 + position.x*3.0) * 0.12 * uShake * (1.0-still) * (1.0-m1);
      vec3 p = mix(position + jit + quake, aVoice, m1);
      vStill = still * uShake;
      // the voice ripples slowly (it is sound, after all)
      p.y += (1.0-m2) * m1 * sin(p.x*2.6 + uTime*1.4 + aSeed*6.28) * 0.12;
      p = mix(p, aWall, m2);
      // particles that overshoot in the wall transition pile against it
      p.z = mix(p.z, aWall.z, m2*m2);
      vec4 mv = modelViewMatrix * vec4(p,1.0);
      gl_Position = projectionMatrix * mv;
      float size = mix(1.9, 2.3, m1) * mix(1.0, 1.6, m2) * (1.0 + 0.6*uShake*(1.0-still)) * uPR * uScale;
      gl_PointSize = size * (12.0 / -mv.z);
      vMix1 = m1; vMix2 = m2; vSeed = aSeed; vDepth = -mv.z;
    }`,
  fragmentShader: `
    precision mediump float;
    uniform vec3 uBone, uSignal, uHot;
    varying float vMix1, vMix2, vSeed, vDepth, vStill;
    void main(){
      vec2 c = gl_PointCoord - 0.5; float d = dot(c,c); if (d > 0.25) discard;
      float soft = smoothstep(0.25, 0.0, d);
      vec3 col = mix(uBone, uSignal, vMix1 * (0.55 + 0.45*vSeed));
      col = mix(col, uHot, vMix2);
      col = mix(col, uSignal, vStill * 0.6);             // the quiet centre glows faintly cool
      float a = (0.28 + 0.4*vMix1) * soft;
      a *= 1.0 - 0.75*vStill;                              // and stays dim: nothing reaches it
      a *= mix(1.0, 0.35 + 0.65*step(0.985, fract(vSeed*7.0 + vMix2*0.0)), vMix2); // the wall is dense but grainy
      a *= clamp(1.6 - vDepth*0.1, 0.25, 1.0);
      gl_FragColor = vec4(col, a);
    }`
});
const pts = new THREE.Points(geo, mat);
scene.add(pts);

// --- scroll mapping -------------------------------------------------------
// uMix1 goes 0→1 over the first ~1.2 viewports (hero → Part 1), uMix2 0→1 across Part 3's approach.
const wallEl = document.getElementById('wall'), bornEl = document.getElementById('born'), crowdEl = document.getElementById('crowd');
let targetMix1 = 0, targetMix2 = 0, targetShake = 0, mix1 = 0, mix2 = 0, shake = 0;
const clamp01 = v => Math.min(1, Math.max(0, v));
const docTop = el => el.getBoundingClientRect().top + scrollY;
function measure() {
  const y = scrollY, h = innerHeight;
  // jackhammer: ramps in as the "born" chapter arrives, holds while it is on screen, ramps out after
  const bt = docTop(bornEl), bh = bornEl.offsetHeight;
  const bin = clamp01((y - (bt - h * 0.9)) / (h * 0.5)), bout = clamp01((y - (bt + bh - h * 0.6)) / (h * 0.5));
  targetShake = bin * (1 - bout);
  // crowd → one voice: resolves as the pivot chapter ("crowd") scrolls into view
  const ct = docTop(crowdEl);
  targetMix1 = clamp01((y - (ct - h * 1.3)) / (h * 1.0));
  const wt = docTop(wallEl);                                     // wall section top, document coords
  targetMix2 = clamp01((y - (wt - h * 1.1)) / (h * 0.9));
}
function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix();
}
addEventListener('resize', () => { resize(); measure(); });
addEventListener('scroll', measure, { passive: true });
resize(); measure();

let running = true, t0 = performance.now();
document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) loop(); });

function frame(now) {
  // ease toward targets so the morph feels physical; the camera also pushes toward the wall and stops dead
  mix1 += (targetMix1 - mix1) * 0.08; mix2 += (targetMix2 - mix2) * 0.08; shake += (targetShake - shake) * 0.1;
  uniforms.uMix1.value = mix1; uniforms.uMix2.value = mix2; uniforms.uShake.value = shake;
  const t = uniforms.uTime.value = (now - t0) / 1000;
  camera.position.z = 9 - 1.2 * mix1 - 5.4 * mix2 * mix2;
  // the camera itself trembles under the jackhammer; the text panel does not
  camera.position.x = Math.sin(t * 0.1) * 0.25 * (1 - mix2) + (Math.random() - 0.5) * 0.09 * shake;
  camera.position.y = (Math.random() - 0.5) * 0.09 * shake;
  // past the wall section, fade the layer so the reading sections stay clean
  const past = Math.max(0, (scrollY - (wallEl.offsetTop + wallEl.offsetHeight * 0.6)) / innerHeight);
  host.style.opacity = String(Math.max(0, 1 - past * 1.4));
  renderer.render(scene, camera);
}
function loop() {
  if (!running || reduce) return;
  frame(performance.now());
  requestAnimationFrame(loop);
}
if (reduce) {
  // one static frame: the voice, no murmur, no camera drift
  uniforms.uMix1.value = 1; uniforms.uMix2.value = 0; camera.position.z = 7.8;
  renderer.render(scene, camera);
  addEventListener('scroll', () => {
    const past = Math.max(0, (scrollY - (wallEl.offsetTop + wallEl.offsetHeight * 0.6)) / innerHeight);
    host.style.opacity = String(Math.max(0, 1 - past * 1.4));
  }, { passive: true });
} else {
  loop();
}
