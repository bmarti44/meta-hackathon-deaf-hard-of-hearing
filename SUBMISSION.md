# Submission summary — causal noise reduction for cochlear implants: a T0 in-silico evaluation

> Hackathon entry state, 2026-11-04. Research-design + in-silico
> (T0) evidence only. No patient data, no implant testing, no
> listener-benefit claim. Detail: [GOAL.md](./GOAL.md),
> [STATUS.md](./STATUS.md), [research/bench-n6/](./research/bench-n6).

## Problem and approach

Cochlear-implant (CI) users struggle most in crowd noise. The
motivating case is the holder's son, who wears bilateral Cochlear
Nucleus 6 processors. We evaluate a small, strictly causal neural
enhancer against unprocessed audio and a classical causal noise
gate on synthetic mixtures, under CI-relevant readouts, before any
implant is involved. **N6 processing was not tested**, so nothing
here compares against it.

Method: an evolutionary loop of generations. In the recent
registered experiments (Gen 19–22) each generation is
pre-registered with one change, fixed budgets, final-checkpoint-only
judgment, 3-seed seed-mean KPIs, and an independent Codex Astra
(xhigh) review between generations. Earlier generations were less
disciplined (e.g. Gen 17 changed pool, mixtures, SNR weighting and
budget together). Failures are filed, not hidden.

## The bench (no-implant proving ground)

`research/bench-n6/` builds synthetic LibriSpeech mixtures with
speaker-disjoint train/test sets. It covers:

- a **crowd** condition (8–12 source draws with replacement from six
  interferer identities) and a competing-talker condition;
- SSN, held-out white noise and quiet rows;
- three intelligibility proxies: waveform STOI, vocoded ESTOI, and
  simulated post-selection (8-of-22) ACE electrodogram correlation;
- a spatial direction-cue screen on an assumed head model;
- a hard KPI scorecard that reports INCOMPLETE unless it has 3
  distinct-hash seeds plus a hash-matched spatial run.

A vocoder listening-pack builder exists, but it only checks the
legacy go/no-go file. It does not yet enforce the current
scorecard, checkpoint identity or fresh-material clearance; those
are required before any evidence pack.

Tests: 17 bench/spatial tests in `research/bench-n6/`, plus 24
trainer/judge tests in `research/gen20–22/` (`pytest research/bench-n6
research/gen20 research/gen21 research/gen22`). KPI arithmetic is
reproducible from committed bench JSONs. Diagnostic and parity
evidence is identified separately where it is used.

## Headline result (Gen 19, complete under the implemented scorecard's evidence checks)

The model is a causal Conv-TasNet-style enhancer: 602,510 params,
exact causality verified, 5.88 ms algorithmic latency (excluding
compute), trained 24k steps on train-clean-100. Seed-mean results
vs unprocessed (3 seeds):

| KPI | Required | Gen 19 |
|---|---|---|
| Crowd ΔSI-SDR | ≥ +3.0 dB, CI lo > 0 | **+3.51 ✓** |
| Crowd ΔSTOI | ≥ +0.03, CI lo > 0 | **+0.035 ✓** |
| Crowd ΔACE-electro | ≥ +0.05, CI lo > 0 | **+0.072 ✓** |
| Crowd @ 0 dB | ≥ +1.5 dB | +4.65 ✓ |
| Crowd @ −5 dB | ≥ +1.5 dB | **+1.19 ✗** |
| SSN / white SI-SDR, quiet SI-SDR / STOI | registered thresholds | ✓ pass |
| Direction cues: target-ILD error (seed 17; four simulated scenes) | < unprocessed (5.96 dB) | 5.47 ✓ |
| Direction cues: ITD error (seed 17; four simulated scenes) | ≤ unprocessed (5.75 smp) | 4.0 ✓ |

**13 of 14 implemented scorecard rows pass.** The only failure is
the hardest condition, crowd at −5 dB. **Verdict: FAIL — keep
optimizing. promoted FALSE.** Astra independently recomputed every
row from raw data.

Disclosures:

- Quiet PESQ and CPU streaming RTF are required by the KPI contract
  but remain unestablished.
- White-noise vocoded ESTOI decreases in all three seeds (mean
  −0.059), even though the registered white SI-SDR row passes.
- The direction-cue rows come from one seed on simulated scenes. In
  the −5 dB scene, target-ILD error worsens (10.29 → 11.22 dB).
  Nothing here implies a directional-hearing benefit.

## What the generations taught us

- **Training budget:** extending the budget and cosine horizon from
  6k to 24k steps improved overall crowd ΔSI-SDR from 2.73 to 3.51 dB.
- **Data:** Gen 17's 10→26-speaker pool expansion gained 0.26 dB;
  Gen 18's 26→251 expansion was roughly neutral at 6k.
- **Failed changes:** Gen 16's one-seed, 2k-step, two-auxiliary
  objective underperformed. Gen 20's paired one-seed continuation
  (crowd-concentrated sampling) failed its registered benefit
  criterion. Neither result establishes a general zero effect.
- **Gen 21** compared 48k scratch training against parent + 24k
  continuation, with data paired via an RNG handoff. Both arms
  passed the seed-1 validation screen, but **neither qualified on 3
  seeds**. Mean −5 dB gains were VAL +0.14/+0.12 and bench
  −0.24/−0.10, against a +0.30 bar on both panels. Extra
  optimization raised overall crowd (+3.51 → +3.79 dB) and the easy
  conditions, but not −5 dB. Gen 19 stays the baseline; Gen 21 is
  filed as a null ([research/gen21/results.md](./research/gen21/results.md)).
  This rejects those extra-optimization policies; it does not
  establish a fundamental −5 dB limit.
- **Gradient diagnostic:** a frozen-weight diagnostic found gradient
  imbalance (quiet/noisy gradient-norm ratio ~37–53×; clipping on
  69–79% of late batches), which motivates a causal training test.
  Its contribution to the −5 dB failure is unestablished.
- **Gen 22** (30 dB soft-capped SI-SDR loss, 24k scratch vs
  same-seed Gen 19) is pre-registered
  ([research/gen22/prereg.md](./research/gen22/prereg.md)). Its
  control mode shows logged loss/gradient-norm prefix parity with
  Gen 19, including a resume check; full-budget parity is
  unverified. [GEN 22 SCREEN RESULT — filled at completion]

## Limits (stated plainly)

Offline bench results cannot establish superiority over the N6's
proprietary processing, which was never tested. Vocoder listening
by a normal-hearing adult cannot predict an individual CI user's
benefit. No candidate has earned the staged listening test yet;
that requires all required KPIs plus fresh-material confirmation.
Implant-involved testing would additionally need assent,
audiologist oversight and MAP-safe levels. None was attempted.

## Next steps

- Finish the capped-loss generation, then compressed-spectral loss,
  then narrower SNR sampling, each separately controlled.
- Build a fresh-material confirmation package (12 new speakers,
  genuinely distinct-voice crowds) before any listening evidence.
- Develop a binaural linked-gain model for directionality.
- Measure quiet PESQ and streaming RTF to complete the KPI contract.
