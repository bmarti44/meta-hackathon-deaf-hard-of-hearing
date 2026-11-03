# Gen 11 summary — J4-A1 built; causality machine-checked

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Date: 2026-11-03. Source:
> [build-report.md](./build-report.md) (Gen 11 build) implementing
> [candidate-J4-causal.md §2](../gen10/candidate-J4-causal.md)
> (Gen 10 spec). Tests **re-run independently for this
> summary** (below). Status unchanged: `promoted FALSE`,
> validation set 0. Everything here is T0, in-silico.

## What was proven

**Causality, Δ = 0 exactly.** The J4-A1 build
([j4_model.py](./j4_model.py): 16 kHz, `W`=128 right-aligned
frames — no padding anywhere, `H`=64, `K`=5, `B`=64 mel
log-energy features, parameter-free per-frame LayerNorm,
2×128 unidirectional LSTM, sigmoid mask, envelope-mask
output with no waveform-OLA path) passes the Gen 10 §2.5
three-part audit:

1. **Suffix-invariance:** identical 0.5 s prefix +
   loud-noise / noise / silence suffixes → masks and
   masked envelopes bitwise `torch.equal` on all 124
   shared-prefix frames, max |Δ| = **0.0**. Truncation
   variant bitwise equal. An impulse at sample 4,000
   changes no frame ending before it — and does change
   later frames, so the test is live, not vacuous.
2. **Static audit:** `frame_bounds(j)=(64j, 64j+127)`,
   entry span 384 samples; no bidirectional/attention/
   conv/pooling/batch-norm module exists in the graph;
   the only norm statistic is {`F_j`}.
3. **Streaming = sequence:** frame-by-frame `step()`
   from zero state reproduces `forward()` bitwise —
   the deployable unit is the audited graph.

Negative control: the barred whole-segment norm (the
Gen 9 failure mode) gives prefix difference 4.118 vs
0.0 built — the test detects what it must.

Scope note: Δ=0 is bitwise at fixed batch/stream shape
(the §2.5 replay protocol; deployment is a single
stream). Cross-batch-size differences ≤6×10⁻⁸ are float
GEMM blocking, not information flow — no op mixes rows.

## Latency / power-relevant compute numbers

- **Parameters** (recounted from tensor shapes):
  L1 98,816 + L2 131,584 + FC 8,256 = **238,656**,
  exactly the filed spec (custom single-bias LSTM cells;
  `nn.LSTM`'s dual bias would build +1,024).
- **Compute:** **237,568 MACs/frame** = spec → **59.4
  MMAC/s** at 250 fps. That is the power-relevant
  figure: **no mW number is derivable and none is
  offered** (needs the target processor, HP-J2-1).
- **CPU latency (this re-run, Apple M5 Max, torch 2.15.0
  CPU, 6 threads):** `step()` median **0.039–0.040 ms**,
  p99 0.16–0.33 ms, end-to-end incl. FFT/filterbank
  **0.049–0.050 ms/frame** vs the 4.0 ms hop deadline —
  >10× margin. (One 12.8 ms single-frame outlier in one
  pass — laptop OS jitter; the deadline question is a
  bench question, Stage 0.) Algorithmic latency per
  spec §3.1: 8.0 ms window + 0 lookahead + 0 synthesis.

Re-run transcript (this summary's own execution):

```text
pytest: 7 passed in 1.40s
PASS (1a) suffix-invariance waveform: prefix Delta exactly 0
PASS (1b) suffix-invariance truncation: Delta exactly 0
PASS (1c) impulse probe: no frame ending before impulse changes
PASS (2) static frame-causality: index/norm/barred-module audits
PASS (2b) streaming step == sequence forward, bitwise
PASS (3) params = 238,656 and MACs/frame = 237,568 (spec S3.4)
PASS (4) CPU latency per frame (vs 4.0 ms deadline)
j4_model.py: params=238656 spec=238656 | MACs/frame=237568 spec=237568
train_smoke: mask-MSE first10 0.10902 -> last10 0.01713 DECREASED (16.9s)
```

Training smoke is **T0 only, not efficacy**: 200 Adam
steps on synthetic harmonic-stack+noise vs an oracle IRM
target; loss falling ~6× shows gradients flow through
the causal graph, nothing about speech or listeners.

## K-J4-0 kill audit status

**Not triggered; audit passes at T0.** K-J4-0 (Gen 10
§9) desk-kills the build if the §2.5 audit finds any
future-frame path or suffix-replay Δ > 0. Measured
Δ = 0.0 bitwise and no barred module/path exists, so
the kill does not fire and the build is bench-eligible
in principle. Caveats that keep this from being a
promotion: the §9 kills are filed as *proposed,
human-ratified pre-scoring — all unevaluated*; K1
(Stage 0 B1–B10 from *measured* records) and K-J4-2/3/4
(adult bridge ≥3 dB, pediatric ≥3 dB, NI bundle) remain
entirely unevaluated. J4 stays `promoted FALSE`,
validation 0.

One reading HP-J4-1 must pin: spec §3.2's 24 ms finite
span implies re-running the LSTM windowed over *j−4…j*;
this build uses persistent state (mask depends on all
frames ≤ *j* — still strictly causal, Δ=0 either way,
and matches §3.4's per-frame MACs; the windowed reading
costs ~5× the recurrent MACs).

## What remains

| Item | Owner |
|---|---|
| Train on real speech/noise corpora → weights of record | Machine, under HP-J4-1 pins |
| HP-J4-1 pins: exact filterbank (mel 50 Hz–8 kHz here is a default), windowed vs persistent `K`, state reset after dropout, dual-mic stratum | **Human** |
| Stage 0 bench: B1–B10 measured (latency p99, power mW, thermal) on H-primary | Lab |
| Stage 1 adult SRT vs SCAN 2 (K-J4-2), Stage 2 pediatric (K-J4-3), NI bundle (K-J4-4) — all listener data | **Human subjects** |

Nothing in Gen 11 is listener evidence. The generation's
gain over Gen 10: the causal design is no longer only
filed — it is built, and its defining claim is now a
passing test instead of an argument.
