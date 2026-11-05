# Screen v2 — larger advancement panel (registered for Gen 26 onward)

> Claude Opus 5.5, 2026-11-04 ~21:10 EST, per Astra's Gen 25 pre-launch and
> result reviews and Muse's Gen 25 review. Registered before any candidate
> is evaluated on it.
>
> - **Applies to:** Gen 26 onward.
> - **Unchanged:** Gen 19–25's panels, rules and verdicts. Gen 24 stays
>   under its own registration. Gen 19's original 13/14 scorecard and its
>   +1.5 dB KPI on bench v2.
> - **What a v2 pass does not do:** establish that KPI. That still
>   requires the original registered scorecard.

## Why

The old screen decided advancement on an 8-item VAL panel (2 voices) and a
6-mixture bench in which the crowd always comes from the same 6 voices.
Small model changes moved VAL by +0.15 and −0.34 dB. A larger,
voice-clustered panel judges future changes on many more voices.

## Material (`research/screen_v2/panel_v2.py`)

- **Targets:** 16 LibriSpeech dev-clean voices, training-disjoint (checked
  against Gen 19's 251 train-clean-100 training speakers) and never used
  as a target or crowd voice by any earlier panel. **Corrected 21:15:**
  these voices (and the 4 reserves) were in the Gen 13–17 dev-clean training
  pools, so they are fresh evaluation material for the Gen 19 lineage, not
  globally unused research data. There is no training leakage into Gen 19+.
  - female: 84 1462 1673 1919 3081 3536 3576 3853;
  - male: 174 251 422 652 777 1272 2803 2902.
- **Reserved, untouched for final confirmation:** 5338, 3000, 3170, 3752.
- **Tuning material** (calibration experiments only): the Gen 21 8-voice
  dev panel. It must never be used for advancement.
- **Items:** per target, 4 clean 4-second crops × 4 crowds (8–12 source draws
  **with replacement** from the other 15 panel voices, i.e. 3–12 distinct
  identities) × SNR {−5, 0} dB, giving 512
  items. Seed 20261204.
- **Material sha256:** `557ad44f3f874c25f6fe80c158844ce4a622f52db171f35c1f84464dbfb3eafb`.

## Rules (`research/screen_v2/judge_v2.py`), per seed, candidate − same-seed Gen 19 final

**ADVANCE** requires all of:

| Rule | Requirement |
|---|---|
| A1 | Mean paired −5 dB SI-SDR gain ≥ +0.30 dB (equal weight per item; equal-sized voice groups) |
| A2 | Voice-clustered 95% bootstrap lower bound of that gain > 0 (resample the 16 voices; 10,000 draws; seed 20261204) |
| A3 | ≥ 10/16 voices improve |
| A4 | Mean −5 dB STOI gain ≥ 0 |
| S1 | 0 dB gain ≥ −0.15 dB and STOI gain ≥ −0.003 |
| S2 | Bench v2 quiet abs ≥ 25 dB and ΔSTOI ≥ −0.02 |
| S3 | Bench v2 crowd ≥ 3.0 / 0.03 / 0.05, each with CI lo > 0; SSN ≥ 3.0; white ≥ 0 |

The old VAL and bench −5 dB numbers are reported descriptively only.

**Confirmation:** seeds 18 and 19, same recipe.
- The 3-seed mean −5 dB gain is ≥ +0.30, positive in ≥ 2/3 seeds.
- The voice-clustered CI lower bound of the 3-seed per-voice means is
  > 0, and ≥ 10/16 voices improve on their 3-seed means.
- STOI is non-worsening, and safeguards hold in every seed.
- Only then is a candidate retained. The original scorecard is re-run on
  it before any KPI statement.

## Revisions after Astra's pre-launch review (21:15, before any candidate was evaluated)

- `judge_v2.py`: the S3 safeguard is now NaN-safe (every bound individually
  finite and > 0).
- `judge_v2.py`: bench coverage is enforced (bench v2, `n_per_cell` 6,
  complete duplicate-free candidate/unprocessed pairing, finite metrics,
  ≥ 6 rows per safeguard condition).
- A voice-clustered A2 interval is conditional on this fixed crowd
  construction.
- **Still open** (must be frozen before any confirmation results): the
  three-seed confirmation aggregator. It will average within each voice
  across seeds and bootstrap the 16 means, with STOI non-worsening
  applied to the 3-seed mean and the safeguards to every seed. The
  reserve-voice procedure is to be defined before those voices are
  opened.

## Validation (before any candidate)

A self-test of Gen 19 seed 17 against itself
(`selftest/judge_selftest_s17.json`) gives exactly 0.0000 gain, so A1–A3
FAIL as they should, and S1–S3 pass.

Descriptive and disclosed: Gen 19 seed 17 itself scores +2.385 dB vs
unprocessed at −5 dB on this panel (bench v2: +1.06). That difference
does not change any KPI or verdict.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `screen_v2/judge_v2.py` | `6cf6032ec4c1d84a0dc45d80e3d146c2eb8d7b8e32ea430a3619546dc08c778b` |
| `gen21/train10.py` | `edef9bef12f8639b0855554d4fea0b06a2a35df21c854820547405319fd255df` |
| `gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
