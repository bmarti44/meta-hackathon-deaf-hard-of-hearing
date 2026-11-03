# Gen 15 — strictly causal Conv-TasNet-style waveform enhancer (T0 only)

> **Model routing.** Requested: **Sol 6.1**. Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> **What this is:** a new design axis after [Gen 14 closed the J4 envelope-mask recipe family](../gen14/Gen14-summary.md): direct waveform enhancement with a strictly causal learned-basis masking network trained on waveform SI-SDR, screened on the identical Gen 13 protocol.
> **What this is not:** listener, SRT, intelligibility-in-humans, power, or on-processor evidence. **No listener-benefit claim is made or implied.** J4 status unchanged: `promoted FALSE`, validation set 0; nothing here is a promotion candidate on one seed.

## Files

| File | Contents |
|---|---|
| [model_causal.py](./model_causal.py) | Causal Conv-TasNet-style model + causality audit/suffix test + receptive-field arithmetic |
| [train4.py](./train4.py) | Training (Gen 13 mixture protocol copied verbatim; negative SI-SDR loss) |
| [eval4.py](./eval4.py) | Paired held-out eval vs unprocessed + oracle-IRM waveform; bootstrap CIs |
| [eval_results.json](./eval_results.json) | Per-crop rows + summaries with CIs |
| [weights/](./weights) | `causal_seed20261115.pt` + interim checkpoints + `train_log_seed20261115.json` |

Environment: `/tmp/gen9env` (Python 3.11, torch 2.15.0 CPU), as Gen 12–14.

## Architecture (`model_causal.py`, 602,510 params)

Learned-basis masking (Conv-TasNet family, single target): encoder
Conv1d(1→160, kernel L=64, stride S=32; 4 ms window / 2 ms hop at
16 kHz) → ReLU → cumulative layer norm → 1×1 bottleneck (80 ch) → TCN
mask estimator (2 repeats × 7 dilated depthwise blocks, kernel 3,
dilations 1–64, hidden 160, skip 80; 1×1 + PReLU + causal depthwise +
cLN per block) → sigmoid mask (160 ch) → ConvTranspose1d decoder.

Geometry note: L=64/S=32 is coarser than the original 8 kHz
Conv-TasNet's 2 ms/1 ms; chosen so the screen fits the stated CPU
budget. It is a limitation, recorded, not tuned.

## Causality proof

Construction:

- Every convolution has `padding=0`; all temporal padding is
  **left-only** (`F.pad(x, (pad, 0))`). No symmetric padding anywhere.
- Normalisation is **cumulative layer norm only** (statistics at frame
  *t* from frames ≤ *t*). No gLN, no batch/instance/group norm.
  `audit_causality()` iterates all modules and returns `[]` (clean).
- Encoder frame *t* (after left-pad L−1) sees input samples
  [S·t−(L−1) … S·t]. Decoder places frame *t* at output samples
  [S·t … S·t+L−1], so output sample *p* only receives frames with
  S·t ≤ p, whose inputs are ≤ p. The raw output is therefore
  sample-wise causal, at the price of a fixed content delay of
  L−1 = 63 samples (training targets are delayed by exactly 63;
  eval shifts estimates back by 63 before scoring).

Receptive-field arithmetic: past span = R·Σ(P−1)·d = 2·2·(1+2+…+64)
= 508 frames × 32 samples + (L−1) = **16,319 past samples ≈ 1.02 s,
0 future samples**. **Algorithmic latency ≤ (L−1)+(S−1) = 94 samples
= 5.88 ms** (content delay 63 + worst-case frame-emit granularity 31;
excludes compute; no other lookahead exists).

Suffix-invariance test (inputs identical for the first P samples,
randomised after; raw outputs compared): **max|Δ| over the first P
output samples = 0.0 exactly** at P ∈ {8000, 16000, 24001} — verified
pre-training, post-training, and again on the loaded weights inside
`eval4.py` (different RNG seeds each time; suffix max|Δ| ≈ 0.5–0.8,
so the test has power). Numbers are filed in the train log and in
`eval_results.json` (`meta.causality`).

## Data and training (Gen 13 protocol verbatim)

- Corpus/split: LibriSpeech `dev-clean` subset under `/tmp/gen12dl`;
  train target speakers 84, 174, 251, 422, 652, 777, 1272, 1462, 1673,
  1919 (661 files, 4,869 s); held-out targets 1988, 1993; eval-babble
  interferers 8842, 8297. Holdout asserted in code.
- Mixtures copied from `gen13/train2.py`: 2 s crops RMS-normalised to
  0.1, SNR −5…+10 dB, 10% quiet, noisy items 70% babble (k~U{2,3,4},
  train speakers only, target excluded) / 30% generated SSN (same
  generator). **White noise never trained** (held-out class).
- Objective: negative waveform SI-SDR vs the 63-sample-delayed clean
  target. Adam 1e-3 cosine → 1e-4, grad-clip 5, batch 8 × 2 s.
- **Stated CPU budget: 2000 steps, single seed 20261115** (a screen,
  not a seed study). Actual wall 3,973 s (≈66 min, shared machine).
  Logged loss (neg SI-SDR, dB) first-5-logged mean +7.66 → last-5
  −6.79 (per-batch values are condition/SNR-dominated, range roughly
  −2…−11 late in training). Weights SHA-256 `f59882b5…f741bd`;
  interim checkpoints at 500/1000/1500 steps are filed alongside.

## Evaluation protocol

Gen 13's eval verbatim (RNG 777, same draw order): 104 paired 4 s
crops — SSN / babble-heldout-spk / white-heldout at SNR
−5/0/+5/+10 dB × 8 (n=32 each) + 8 quiet. Systems: unprocessed
(mixture scored directly; Gen 13 scored its unprocessed through a
mel-OLA identity path, a readout difference noted below), causal
model (63-sample delay compensated), and **oracle-IRM waveform**
(STFT 512/128 Hann ideal ratio mask from true clean/noise — a
**non-causal** upper bound for magnitude masking, not a competitor).
Metrics: SI-SDR/STOI/PESQ-WB on samples [256:−256] (Gen 13 trim);
paired bootstrap 95% CIs over crops (2000 resamples, seed 13) as
Gen 13. CIs cover eval-crop sampling only — 2 held-out speakers,
not a speaker population.

## Results

Δ = causal − unprocessed (paired, same crops); brackets are 95%
bootstrap CIs over crops. Full rows in
[eval_results.json](./eval_results.json). Eval re-run produced a
**bit-identical** JSON (SHA-256 `98cb3bd8…bcfd`).

| Condition (n=32) | ΔSI-SDR dB | ΔSTOI | ΔPESQ |
|---|---|---|---|
| SSN (trained) | **+4.52 [+3.99, +5.05]** | +.03 [+.02, +.04] | +.08 [+.05, +.11] |
| Babble, held-out spk | **+1.14 [+0.76, +1.52]** | −.01 [−.02, −.00] | +.02 [−.01, +.05] |
| White, held-out class | **+0.69 [+0.43, +0.97]** | −.00 [−.01, +.00] | +.00 [−.00, +.00] |
| ALL-NOISY (n=96) | +2.12 [+1.70, +2.51] | +.00 [−.00, +.01] | +.03 [+.02, +.05] |

Absolute levels (unproc / causal / oracle STFT-IRM): SI-SDR SSN
2.46/6.98/11.62, babble 2.47/3.61/13.23, white 2.46/3.15/14.39 dB;
STOI SSN .701/.729/.941, babble .681/.670/.958, white .743/.739/.963;
PESQ SSN 1.10/1.18/2.68, babble 1.14/1.16/3.08, white 1.05/1.05/3.41.
Unprocessed SI-SDR absolutes (2.46/2.47/2.46) match Gen 13's filed
values exactly, confirming identical eval crops and that the
direct-vs-OLA unprocessed readout difference is negligible. The
oracle gap remains large (babble oracle ΔSI-SDR +10.76 dB): this
screen captures roughly a tenth of the STFT-mask ceiling on babble.

Quiet (n=8): SI-SDR vs clean mean 24.5 dB (21.0–29.1), STOI .988,
**RMS ratio 0.985 (0.94–1.00)** — output level is preserved, so the
Gen 14 constant-mask/level collapse of scale-invariant *envelope*
loss does not occur here; but PESQ falls to 3.11 (unprocessed 4.64),
so quiet passthrough is not transparent on that metric. The model is
not quiet-neutral and that counts against it.

Honest reading of the babble row: ΔSI-SDR's CI excludes 0 — the first
non-null babble readout in this line under the pre-stated Gen 13/14
gate — **but ΔSTOI is slightly negative and ΔPESQ is null**. A
waveform SI-SDR objective buys time-domain energy/alignment fit
without moving either intelligibility/quality proxy on competing
speech. That pattern (SI-SDR up, STOI flat) is not evidence a
listener could use the output; it is a T0 signal that the axis is
not dead, nothing more. One seed, coarse 4 ms/2 ms geometry, and
2000 steps all bound how far this can be read.

## Head-to-head vs Gen 13 J4 (seed-mean, 3000 steps × 3 seeds)

Gen 13 filed numbers ([gen13/results.md](../gen13/results.md),
waveform-T0 via noisy-phase mel-OLA reconstruction; J4 emits no
waveform): ΔSI-SDR SSN **+4.02 [+3.55, +4.48]**, babble **−0.12
[−0.34, +0.12]**, white **−2.65 [−3.14, −2.16]** dB; ΔSTOI
+.042 / −.006 / −.045; ΔPESQ +0.13 / +0.02 / −0.01. Absolute SI-SDR
(unproc/J4/oracle mel-IRM): SSN 2.46/6.49/8.73, babble 2.47/2.35/9.99,
white 2.46/−0.18/12.42 dB. Readout caveats before comparing absolutes:
(1) Gen 13's oracle is the mel-envelope IRM bound, Gen 15's oracle is
a finer STFT-IRM bound — different ceilings; (2) Gen 13's system and
unprocessed both passed through the mel-OLA reconstruction, Gen 15's
are native/direct waveforms on the **same crops**; (3) Gen 15 is one
seed at 2000 steps vs Gen 13's three seeds at 3000. Δ-vs-unprocessed
on identical crops is the fairest common readout.

| Δ vs unprocessed | SSN | Babble held-out spk | White held-out class |
|---|---|---|---|
| Gen 15 causal TasNet (1 seed, 2000 steps) SI-SDR / STOI / PESQ | +4.52 / +.03 / +.08 | **+1.14 / −.01 / +.02** | +0.69 / −.00 / +.00 |
| Gen 13 J4 seed-mean (3 seeds, 3000 steps) SI-SDR / STOI / PESQ | +4.02 / +.042 / +.13 | −0.12 / −.006 / +.02 | −2.65 / −.045 / −.01 |

Where the new axis differs, at T0: (1) **babble ΔSI-SDR moves from
null to +1.14 dB** (CI excludes 0) — but with STOI still flat/negative
in both generations, so neither system shows a babble gain on an
intelligibility proxy; (2) **held-out white flips from −2.65 dB
(failure) to +0.69 dB** — the waveform model does not show J4's
noise-class collapse on SI-SDR (STOI ≈ 0 vs −.045); (3) SSN is a wash
(J4 slightly better on STOI/PESQ deltas, causal slightly better on
SI-SDR, absolute PESQ low for both). Quiet: J4 was near-transparent
on its readout (PESQ 4.62); the causal model's quiet PESQ 3.11 is
**worse** — a real regression to fix before anything downstream,
and a reason this checkpoint earns no listener time as-is. Gen 15
also has no ACE-consumption readout (Gen 13 §ACE): the waveform
output would need the waveform→envelope path through `ace_sim.py`
before any envelope-delivery comparison is possible.

## Unresolved / not done

- **One seed, one budget.** No seed replication; CIs are over 32
  crops/condition from 2 held-out speakers (not a speaker
  population), exactly as Gen 13. Seed variance of the babble
  ΔSI-SDR signal is unknown.
- **STOI/PESQ do not corroborate the babble SI-SDR gain.** Whether a
  finer encoder geometry (2 ms/1 ms), more steps, a multi-term loss
  (SI-SDR + spectral/STOI-proxy), or larger TCN changes that is
  untested — none assumed to help.
- **Quiet non-transparency** (PESQ 3.11 vs 4.64) unresolved; a
  quiet-identity/level term or passthrough gate is a candidate fix,
  untested. Noisy-condition output RMS runs 1.08–1.21× clean RMS.
- No ACE/envelope-consumption readout, no streaming implementation
  (causality is proven for the batch network; a frame-by-frame
  stateful implementation was not built or measured), no RTF/power
  measurement (offline CPU inference only), no bench or listener
  data. Latency 5.88 ms is arithmetic on the architecture, not a
  measured streaming latency.
- Training data remains synthetic mixtures of LibriSpeech dev-clean
  from `/tmp/gen12dl` (not committed; regenerate per
  [gen12/results.md](../gen12/results.md)). Nothing here tests
  recorded scenes, reverberation, or other corpora.
- Status unchanged: `promoted FALSE`, validation set 0. Per the
  standing gate, no listener time is argued for: the babble signal
  is SI-SDR-only, single-seed, with a quiet regression.

Run commands:

```bash
/tmp/gen9env/bin/python research/gen15/model_causal.py   # params + causality self-test
/tmp/gen9env/bin/python research/gen15/train4.py --steps 2000 --seed 20261115
/tmp/gen9env/bin/python research/gen15/eval4.py --n-per-cell 8
```
