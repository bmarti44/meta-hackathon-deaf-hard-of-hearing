# Gen 15 summary — waveform-causal moves babble SI-SDR only (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Date: 2026-11-03. Source: [results.md](./results.md).
> **Eval independently re-run for this summary** (below).
> Status unchanged: `promoted FALSE`, validation set 0.
> Everything here is **T0, in-silico. No listener-benefit
> claim is made or implied.**

## Independent re-run

```text
/tmp/gen9env/bin/python research/gen15/eval4.py --n-per-cell 8 \
  --out /tmp/gen15_rerun_eval.json
→ EVAL DONE 27 s; cmp vs filed eval_results.json: BIT-IDENTICAL
  (both SHA-256 98cb3bd8…bcfd; weights f59882b5…f741bd)
  Causality on loaded weights re-asserted in eval:
  max|Δ| prefix = 0.0 exactly at P=8000/16000/24001
```

Exact reproduction is expected (fixed RNG 777 eval crops,
filed checkpoint). It verifies filed numbers are what filed
code + weights produce, not that they generalise. Training
(2000 steps, 3,973 s) was **not** re-run here.

## Does waveform-causal beat the envelope-mask on babble?

**On ΔSI-SDR alone, yes — first non-null in this line. On
intelligibility/quality proxies, no.** Same Gen 13 crops
(unprocessed absolutes 2.46/2.47/2.46 dB match Gen 13
exactly), Δ = system − unprocessed, 95% bootstrap CIs over
32 crops/condition (2 held-out speakers only):

| Δ vs unprocessed | Babble, held-out spk | SSN | White, held-out class |
|---|---|---|---|
| Gen 15 causal TasNet (1 seed, 2000 steps) SI-SDR / STOI / PESQ | **+1.14 [+0.76, +1.52]** / −.01 / +.02 | +4.52 / +.03 / +.08 | +0.69 / −.00 / +.00 |
| Gen 13 J4 envelope-mask (3 seeds, 3000 steps) SI-SDR / STOI / PESQ | −0.12 [−0.34, +0.12] / −.006 / +.02 | +4.02 / +.042 / +.13 | −2.65 / −.045 / −.01 |

Caveats on "beat": 1 seed vs 3, 2000 vs 3000 steps, native
waveform vs mel-OLA readout, different oracle ceilings
(Gen 15 STFT-IRM babble Δ +10.76 dB; this screen captures
~1/10 of it). Δ-on-identical-crops is the fairest readout.

Per-SNR babble (recomputed from filed rows, n=8/cell):
ΔSI-SDR −0.08 / +0.69 / +2.03 / +1.91 dB and ΔSTOI
−.037 / −.019 / +.010 / +.002 at −5/0/+5/+10 dB — the gain
lives at favourable SNRs; at ≤0 dB it is null on SI-SDR
and negative on STOI. Overall ΔSTOI −.011 [−.020, −.004]
and ΔPESQ +.02 [−.01, +.05] do not corroborate the SI-SDR
rise: waveform SI-SDR training buys time-domain fit
without moving either proxy on competing speech. That is
a T0 signal the axis is not dead, not usable-output
evidence. Held-out white flipping −2.65 → +0.69 dB (J4's
noise-class collapse absent) is the second real
difference; SSN is a wash.

Against it: quiet (n=8) PESQ **3.11 vs 4.64 unprocessed**
(J4: 4.62), SI-SDR 24.5 dB, RMS ratio 0.985. Level is
preserved but passthrough is not transparent. Per
[results.md](./results.md), this checkpoint earns **no
listener time as-is**.

## Latency

Strictly causal by construction (left-only padding,
cumulative LN only; `audit_causality()` clean, suffix
Δ = 0.0 above). **Algorithmic latency ≤ 94 samples =
5.88 ms** at 16 kHz (63-sample content delay + 31-sample
emit granularity, L=64/S=32); receptive field 16,319 past
samples ≈ 1.02 s, **0 future**. This is architectural
arithmetic only — no streaming implementation, measured
latency, RTF, or power exists yet. 602,510 params.

## Next

Gate before any listener argument (unchanged): a babble
gain corroborated beyond SI-SDR, without a quiet
regression. In order:

1. **Seed replication** (≥2 more seeds, same budget):
   is +1.14 dB inside seed variance? Currently unknown.
2. **Fix quiet** + require ΔSTOI ≥ 0 on babble: candidate
   levers (untested, none assumed to help) — quiet-identity
   term/passthrough gate, finer 2 ms/1 ms geometry,
   multi-term SI-SDR + spectral/STOI-proxy loss, more steps.
3. **ACE-consumption readout** via waveform→envelope path
   (`ace_sim.py`) before any envelope-delivery comparison;
   then streaming implementation with measured latency/RTF.

Unresolved: single seed/budget; CIs cover 2 speakers, not
a population; synthetic LibriSpeech mixtures only (no
reverb/recorded scenes); noisy output RMS 1.08–1.21× clean.
