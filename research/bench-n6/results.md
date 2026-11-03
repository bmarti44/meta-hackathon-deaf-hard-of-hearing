# Bench-N6 results — run 1 (2026-11-03)

> T0 in-silico only. No listener, implant, or "beats the N6" claim.
> Protocol: [PROTOCOL.md](./PROTOCOL.md). Data: 52 paired 4 s crops,
> identical construction to Gen 13 (RNG 777; held-out targets
> 1988/1993; held-out babble interferers 8842/8297; SNR −5/0/+5/+10).
> Δ = system − unprocessed, paired bootstrap 95% CI over crops
> (crop sampling only; 2 target speakers — not a population CI).
> Full rows: [bench_results.json](./bench_results.json).
> Re-run: `/tmp/gen9env/bin/python research/bench-n6/bench.py
> --n-per-cell 4 --gen15 research/gen15/weights/causal_seed20261115_step500.pt`

## Headline (babble, held-out speakers, n=16)

| System | ΔSI-SDR dB | ΔSTOI | ΔACE electro-corr (post 8-of-22) |
|---|---|---|---|
| Classical causal gate | +0.04 [−0.22, +0.25] | −0.009 | −0.001 [−0.006, +0.005] |
| Gen15 waveform, interim step-500 | **+0.41 [+0.26, +0.57]** | −0.005 | +0.003 [−0.004, +0.012] |
| Oracle IRM (non-causal ceiling) | +10.93 [+9.83, +11.95] | +0.279 | +0.343 [+0.239, +0.449] |

By SNR, babble SI-SDR (absolute): Gen15 interim −4.54 / +0.43 /
+5.49 / +10.46 dB at −5/0/+5/+10 vs unprocessed −4.74 / +0.02 /
+4.97 / +9.96 — a small gain at every SNR, largest where it is
already easiest.

## Sanity checks that passed

- The bench detects known effects: the classical gate gains
  +2.11 dB on SSN and +2.91 dB on held-out white noise (CIs > 0)
  while staying babble-null — the textbook pattern for conventional
  NR. A babble null here is a result, not bench insensitivity.
- Gen15 interim does no harm where earlier models did: quiet
  absolute SI-SDR 20.6 dB (ΔSTOI −0.029), held-out white +1.46 dB.
- Safety: all example/pack wavs peak ≤ 0.889 (verified on disk).

## Go/no-go verdict (Stage B gates, PROTOCOL.md)

**No system earns vocoder listening as evidence.**
Gen15 interim passes 5 of 6 gates (babble ΔSI-SDR CI > 0; beats the
classical gate in babble; quiet absolute; quiet ΔSTOI; white-noise
harm) and fails the one that matters most for a CI: after 8-of-22
selection, what would actually be stimulated barely moves toward
clean (+0.003, CI crosses 0), and STOI slightly declines. In plain
terms: at step 500 the waveform model makes babble measurably
cleaner on a waveform ruler — the first causal model in this
project to do so — but not yet in the channel patterns an implant
or vocoder would present. That is a lead to finish training, not
a result to listen to as evidence.

A labeled methods-shakedown pack (72 blinded vocoded items incl.
oracle + clean controls) exists under `listening_pack/` for the
father to sanity-check the *setup* (can he understand vocoded
speech at all; does the oracle control sound clearly better).
It is explicitly **not evidence** about any system.

## Bench bugs found and fixed during this run (kept visible)

1. Run 1 classical gate scored ≈ −4.5 dB everywhere: Hann-tail
   division artifacts. Fixed with flat-tail window + gain smoothing;
   same gate then showed the expected stationary-noise pattern.
2. Run 1 oracle peaks > 100 from OLA edge division. Fixed (norm
   floor); regression test added. Example files were peak-limited
   throughout, so nothing unsafe was ever written for listening.
3. Quiet gate originally used Δ vs unprocessed (≈148 dB reference),
   producing meaningless −127 dB deltas. Replaced with absolute
   SI-SDR + ΔSTOI; gate-logic test added.
4. Codex Astra review ([filed](./codex-astra-review.md)): ACE gate
   metric was pre-selection — now post-selection; gates compared
   only vs unprocessed — now also vs the classical gate; pilot
   listening separated from evidence listening in the protocol.

## Next

- Gen 15 full training (2000 steps) finishes in its workflow →
  re-bench the final checkpoint on this identical protocol.
- If the post-selection ACE gate still fails at full training, the
  waveform axis needs a different objective (e.g. envelope-domain
  loss term), screened here before any listening.
- Implants remain untouched. Stage D is not authorized by anything
  in this bench.

---

## Run 2 — Gen 15 final checkpoint (2000 steps), same day

Rows: [bench_results_run2.json](./bench_results_run2.json).
Gen 15's own full eval (32 crops/condition) is filed at
[gen15/results.md](../gen15/results.md); the two agree (babble
ΔSI-SDR +1.14 dB there, +1.07 here on 16 crops).

| Checkpoint | Babble ΔSI-SDR | Babble ΔSTOI | Babble ΔACE electro-corr | Verdict |
|---|---|---|---|---|
| Step 500 | +0.41 [+0.26, +0.57] | −0.005 | +0.003 [−0.004, +0.012] | NO-GO |
| Step 1000 | +1.01 [+0.59, +1.47] | −0.012 | +0.010 [−0.002, +0.025] | NO-GO |
| Step 2000 (final) | +1.07 [+0.57, +1.59] | −0.016 | +0.011 [−0.004, +0.027] | **NO-GO** |

Final checkpoint elsewhere: SSN +4.30 dB with post-selection ACE
+0.086 [+0.052, +0.122] (implant patterns do improve for steady
noise); held-out white +0.84 dB; quiet absolute SI-SDR 26.1 dB.
Per-SNR (Gen 15 summary): the babble gain lives at favourable SNRs
(+5/+10 dB) and is absent at −5 dB.

**Reading:** training more on a waveform-only objective plateaued
in babble after step 1000. The objective is the bottleneck, not
the budget. Gen 16 therefore changes the objective: SI-SDR plus
an ACE-envelope loss term (post-selection patterns vs clean),
plus a quiet-identity term (quiet PESQ regressed to 3.11 in
Gen 15's own readout). Same bench, same gates. Implants still
untouched.

---

## Spatial (direction-cue) screen — 2026-11-03

Holder interest: sound localization. [spatial_bench.py](./spatial_bench.py)
renders target/babble at opposing azimuths (±30°, ±60°) with an
ASSUMED head model (Woodworth ITD + smooth head shadow; cue
*distortion* comparisons only) and measures per-ACE-band ILD
error. Rows: [spatial_results.json](./spatial_results.json).

| System | ILD error vs target (dB) | ILD distortion vs mixture (dB) | ITD err (samples) |
|---|---|---|---|
| Unprocessed | 5.96 | 0 (by construction) | 5.8 |
| Classical gate, per-ear | 5.79 | 0.26 | 4.3 |
| Classical gate, linked gains | 5.78 | 0.19 | 4.3 |
| Gen 15, per-ear | 5.42 | 0.95 | 4.3 |

Reading: on these 4 scenes the noise itself dominates target-ILD
error (~6 dB); processing-induced distortion is smaller but real
for the per-ear neural model (0.95 dB mean) and lowest with linked
gains. Nothing here shows a system *restoring* direction — that
would require linked bilateral processing beyond this screen —
and nothing yet earns a spatial claim. Gate added to PROTOCOL:
candidate ILD distortion must not exceed the linked gate's.

---

## Bench v2 first scoring — Gen 15 final (2026-11-03, n=8/kind)

Pre-registered in [bench-v2-prereg.md](./bench-v2-prereg.md)
(committed before scoring). Rows: bench_v2_results.json.

| Gen 15 Δ vs unproc | Crowd (≥8 talkers) | Competing (2 talkers) |
|---|---|---|
| ΔSI-SDR | +1.97 dB | +1.10 dB |
| ΔSTOI / Δvocoded-ESTOI | 0.000 / +0.019 | −0.013 / +0.002 |
| ΔACE electro-corr / ΔNCM-simple | +0.043 / +0.030 | +0.014 / +0.006 |

As REVIEW §1.1 predicted, the same model looks materially
better on crowd babble than on competing talkers — crowd is the
solvable single-mic problem; competing needs a cue (binaural or
enrollment). Small n; treat as v2 baseline, not a new claim.
