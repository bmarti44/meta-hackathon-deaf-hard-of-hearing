# Submission summary — causal noise reduction for cochlear implants, proven without implants

> Hackathon entry state, 2026-11-04. Research-design + in-silico
> (T0) evidence only. No patient data, no implant testing, no
> listener-benefit claim. Detail: [GOAL.md](./GOAL.md),
> [STATUS.md](./STATUS.md), [research/bench-n6/](./research/bench-n6).

## Problem and approach

Cochlear-implant (CI) users struggle most in crowd noise, and
today's processor noise reduction is limited. We set out to
prove — entirely on the bench, before any implant is involved —
whether a small, strictly causal neural enhancer can beat
unprocessed audio and a classical causal noise gate under
CI-relevant readouts, for the holder's son's device class
(bilateral Cochlear Nucleus 6).

Method: an evolutionary loop (generations → selection →
recombination) with pre-registered experiments, one change per
generation, fixed budgets, final-checkpoint-only judgment,
3-seed seed-mean KPIs, and an independent Codex Astra (xhigh)
review between every generation. Failures are filed, not hidden.

## The bench (no-implant proving ground)

`research/bench-n6/`: synthetic mixtures (LibriSpeech, speaker-
disjoint train/test), crowd (≥8 talkers) vs competing-talker
split, SSN/white/quiet no-harm rows, vocoded intelligibility
proxies (STOI/ESTOI, post-selection ACE electrodogram
correlation), a spatial direction-cue screen (assumed head
model), hard KPI scorecard (3 distinct-hash seeds +
hash-matched spatial or INCOMPLETE), and a blinded vocoder
listening-pack builder that refuses unpassed candidates.
21+ automated tests; every number below is reproducible from
committed JSONs.

## Headline result (Gen 19, complete evidence)

Causal Conv-TasNet-style enhancer (602,510 params, exact
causality verified, 5.88 ms algorithmic latency), 24k steps on
train-clean-100. Seed-mean crowd performance vs unprocessed:

| KPI | Required | Gen 19 |
|---|---|---|
| Crowd ΔSI-SDR | ≥ +3.0 dB | **+3.51 ✓** |
| Crowd ΔSTOI | ≥ +0.03 | **+0.035 ✓** |
| Crowd ΔACE-electro | ≥ +0.05 | **+0.072 ✓** |
| Crowd @ 0 dB | ≥ +1.5 dB | +4.65 ✓ |
| Crowd @ −5 dB | ≥ +1.5 dB | **+1.19 ✗** |
| SSN / quiet / spatial | no-harm | ✓ all pass |

**13 of 14 required KPIs pass; the sole failure is the hardest
condition (crowd at −5 dB). Verdict: FAIL — keep optimizing.
promoted FALSE.** (Astra independently recomputed every row
from raw data and confirmed the arithmetic.)

## What the generations taught us

- Training length was the binding constraint (2k→6k→24k steps:
  +1.75 → +2.73 → +3.51 dB). More speakers at matched compute
  was neutral (Gen 17/18). A multi-term loss (Gen 16) and
  crowd-concentrated sampling (Gen 20) were clean nulls under
  matched/paired controls.
- Gen 21 (48k scratch vs parent+24k continuation, paired data
  via RNG handoff): both arms passed the validation screen,
  [REPLICATION VERDICT — filled at completion].
- Astra's gradient diagnostic found a concrete mechanism for
  the −5 dB wall: near-perfect quiet examples produce ~37–53×
  the gradient norm of noisy ones, starving hard examples.
  Next registered change: 30 dB soft-capped SI-SDR loss, then
  compressed-spectral loss, SNR concentration, STOI auxiliary.

## Limits (stated plainly)

Offline bench results cannot claim superiority over the N6's
proprietary processing, and vocoder listening by a
normal-hearing adult cannot predict an individual CI user's
benefit. No candidate has earned the staged listening test yet
(all required KPIs + fresh-material confirmation required).
Implant-involved testing would additionally need assent,
audiologist oversight and MAP-safe levels — none attempted.

## Next steps

Capped-loss generation → compressed spectral → SNR schedule;
fresh-material confirmation package (12 new speakers, genuinely
distinct-voice crowds) before any listening evidence; binaural
linked-gain model for directionality; quiet-PESQ and streaming
RTF/latency measurements to complete the KPI contract.
