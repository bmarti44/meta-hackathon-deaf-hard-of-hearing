# Bench-N6 protocol — prove it without implants first

> Holder direction (2026-11-03): test and get this working well
> **without** the implants. Do not pull in the implants until the
> process is proven. The implantee is the holder's son (bilateral
> Nucleus 6 / CP900 series); the holder is not implanted and cannot
> listen through a CI himself.
>
> Model routing: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Status of everything here: **T0 in-silico + normal-hearing (NH)
> screening files. No listener-benefit claim. No implant claim.**

## What "beat what exists" can and cannot mean offline

The [Cochlear N6 professional page](https://www.cochlear.com/us/en/professionals/products-and-candidacy/nucleus/nucleus-sound-processors/nucleus-6-processor)
(inspected 2026-11-03) identifies the device only as the CP900-series
processor and links a user guide; it publishes no noise-reduction
algorithm, parameters, or performance numbers. Cochlear's on-device
front-end processing is proprietary. Therefore:

- We **cannot** replicate the N6's actual noise reduction offline,
  and no bench result here is "beats the N6."
- We **can** require a candidate to beat, on identical held-out
  material: (a) unprocessed audio (what ACE channel selection alone
  receives), and (b) a classical strictly-causal spectral gate
  (`baselines.CausalSpectralGate`, a stand-in for the *class* of
  conventional NR, explicitly not Cochlear's). The oracle IRM is a
  non-causal ceiling showing remaining headroom, never a competitor.
- Only a later, separately-designed streamed comparison on the real
  processors could speak to the N6 itself — Stage D below, gated.

## Stages (in order; no skipping)

### Stage A — Machine correctness (no audio a human needs)
- Causality: exact suffix-invariance test (bitwise, on block boundary
  for block systems). Enhancer latency stated in ms, compute excluded
  and labeled as such.
- Safety: every file any person may hear passes `limit_signal`
  (target RMS 0.1, hard peak ≤ 0.89; silence stays silence).
- Holdout hygiene: eval target speakers 1988/1993 and babble
  interferers 8842/8297 are disjoint from all training speakers
  (asserted in `test_bench.py`).
- Gate: `pytest research/bench-n6/test_bench.py` green.

### Stage B — Objective bench (`bench.py`)
Identical crops to Gen 13 (RNG 777; babble held-out speakers, SSN,
held-out white noise, quiet; SNR −5/0/+5/+10 dB). Per system:
SI-SDR, STOI, ACE envelope correlation vs clean (22-ch, per
`gen13/ace_sim.py` parameters), peak/RMS. Paired bootstrap CIs vs
unprocessed (crop sampling only — 2 speakers, stated).

**Go/no-go to earn Stage C listening time** (all required, implemented
in `bench.evaluate_go_nogo`):
1. Babble ΔSI-SDR 95% CI lower bound > 0, **and** babble SI-SDR
   above the classical causal gate's (both baselines, not just
   unprocessed).
2. Babble ΔACE correlation **after 8-of-22 selection** (the
   electrodogram the device/vocoder actually consumes) 95% CI
   lower bound > 0. (Energy suppression without envelope fidelity
   failed this in Gen 13 and does not count.) Envelope metrics are
   unvalidated proxies — supporting evidence, not truth.
3. Quiet judged absolutely (unprocessed quiet ≈ clean vs itself, so
   a delta is meaningless): absolute SI-SDR > 15 dB **and**
   ΔSTOI > −0.05 (do not damage clean speech).
4. Held-out white-noise ΔSI-SDR mean > −1 dB (no class-specific harm).

Failing any gate = back to model work **for evidence purposes**.
A small father-only pilot listen for debugging is allowed at any
time (`listening_pack.py --allow-unpassed`, output labeled
"METHODS SHAKEDOWN — NOT EVIDENCE"; include clean-vocoded and
oracle-vocoded controls to check the setup has headroom). Pilot
impressions carry no benefit claim and never substitute for the
gated Stage C test on fresh material. (Separation of debugging
from evidence per Codex Astra review, 2026-11-03.)

### Stage C — NH vocoder screening (father, headphones)
Only for a system that passed Stage B. `vocoder.py` renders an
8-of-22 ACE-like noise-vocoded approximation the (normal-hearing)
father can hear on ordinary headphones. `listening_pack.py` builds a
blinded, randomized pack (system identity sealed in a separate key
file): transcribe-what-you-hear + clarity rating per item.

Honest limits, printed in every pack: a vocoder is not a CI. It has
no current spread, loudness map, neural survival, adaptation, or the
son's individual fitting. Stage C can only screen "could a listener
use this signal at all" and catch gross artifacts cheaply. It cannot
predict the son's benefit, and a Stage C win is not a win.

Gate to Stage D discussion: pre-registered improvement in the
father's blinded vocoder transcription score in babble vs
unprocessed-vocoded, with no quiet-condition degradation — plus
Stage B still passing on a fresh seed set.

### Stage B2 — Direction-cue screen (`spatial_bench.py`)
Target and babble rendered at opposing azimuths under an ASSUMED
head model. Gate: candidate's mean ILD distortion vs the mixture
must not exceed the linked-gain classical gate's on the same
scenes. Preserving cues is a floor, not a localization claim;
restoring direction would need linked bilateral processing the
current processors do not expose.

### Stage D — Implant consideration (NOT authorized by this protocol)
Out of scope until A–C pass. Would additionally require, at minimum:
the son's own assent/consent as appropriate, his audiologist/clinician
involved, streamed (Phone Clip / Mini Mic) delivery that bypasses no
safety limit of his clinical map, loudness checked against his
program before any speech material, an immediate-stop rule, and a
pre-registered A/B design (candidate vs his everyday program).
Nothing in Stages A–C, however good, substitutes for any of that.

Pre-hookup homework (do all of this before Stage D is discussed):
- Confirm exact processor model per ear (CP910 vs CP920 — monitor
  earphones are supported on CP910, not CP920 per the N6 manual).
- From his audiologist: current programs/maps summary, any
  streaming level limits, and whether a streamed A/B session is
  acceptable and how loudness should be verified first.
- Verify laptop → Phone Clip / Mini Mic → both processors pairing
  and latency with ordinary music/speech (delivery path only).
- Optional: Cochlear Monitor Earphones (N6 accessory) so the
  father can check the processors' microphone input — this is
  the pre-processing audio, NOT what his son perceives.
- Baseline measures with his everyday program (e.g. sentence
  scores in quiet/noise from clinic records) to compare against.
- Written session plan: materials, randomization, stop rule,
  assent process. None of this is started by the bench.

## Current standing entering this bench

- Envelope-mask line (J4, Gens 11–14): causal, +4.0 dB SI-SDR on
  stationary noise, **babble null** (−0.12 dB, seed-stable), held-out
  white noise harmed. Recipe family closed in Gen 14. It would fail
  Stage B gates 1, 2 and 4.
- Waveform line (Gen 15, causal Conv-TasNet-style): interim
  step-500 checkpoint benched here (see results.md); full Gen 15
  training/eval still in progress in its own workflow — interim
  numbers only, treat the generation as unfinished.
- Oracle headroom in babble remains large (~+7.5 dB SI-SDR over
  unprocessed in Gen 13/15 readouts): the representation can express
  a better babble output; no causal candidate has found it yet.

## Files

| File | Role |
|---|---|
| [common.py](./common.py) | Metrics, bootstrap CIs, safety limiter |
| [vocoder.py](./vocoder.py) | ACE-like NH noise vocoder + envelope extraction |
| [baselines.py](./baselines.py) | Causal classical gate; oracle ceiling |
| [bench.py](./bench.py) | Stage B runner + go/no-go + example wavs |
| [listening_pack.py](./listening_pack.py) | Stage C blinded pack builder |
| [test_bench.py](./test_bench.py) | Stage A durable tests |
| [results.md](./results.md) | Filed bench outcomes (updated per run) |
