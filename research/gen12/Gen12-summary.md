# Gen 12 summary — J4-A1 trained on real speech: SSN gain only; babble null, held-out noise fails (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Date: 2026-11-03. Source: [results.md](./results.md) with
> [eval_results.json](./eval_results.json), building on
> [Gen 11 summary](../gen11/Gen11-summary.md) and
> [candidate-J4-causal.md §4](../gen10/candidate-J4-causal.md).
> **Eval independently re-run for this summary** (below).
> Status unchanged: J4 `promoted FALSE`, FROZEN retained,
> G3b BLOCKED, validation set 0. Everything here is **T0,
> in-silico. No listener-benefit claim is made.**

## Independent re-run

```text
/tmp/gen9env/bin/python research/gen12/eval.py --n-per-cell 4 --out /tmp/gen12_rerun_eval.json
→ EVAL DONE 26s; re-run JSON identical to filed eval_results.json (a==b True, max |diff| 0.0)
weights SHA-256 35a5d4bbee…b26269 matches j4a1_gen12.pt
pytest research/gen11/: 7 passed in 1.73s (causality/streaming suite still green)
```

Exact reproduction is expected (eval RNG seeded 777, same
`/tmp/gen12dl` corpus subset) — it verifies the filed numbers
are what the filed code + weights produce, not that they
generalise. Training itself was **not** re-run here.

## Objective results vs unprocessed and oracle

Setup, briefly: LibriSpeech dev-clean (OpenSLR 12, CC BY 4.0);
10 train target speakers, held-out targets 1988/1993,
interferer-only 8842/8297. J4-A1 trained 750 steps (217 s CPU)
toward the mel-envelope ideal ratio mask (mask-MSE 0.148 → 0.112,
first/last-5 logged). Eval: 52 held-out 4 s crops, SNR
−5/0/+5/+10 dB. Waveform metrics come from a **T0-only**
noisy-phase mel-gain OLA reconstruction — J4-A1 emits no
waveform; unprocessed and oracle pass through the same path
(identity check 139 dB). Oracle = upper bound of *this mel-IRM
representation*, not of enhancement in general.

Waveform T0, Δ vs unprocessed-OLA (SI-SDR dB / STOI / PESQ-WB):

| Condition | J4-A1 Δ | Oracle IRM Δ | Reading |
|---|---|---|---|
| SSN (trained class) | **+3.31 / +.024 / +.11** | +6.14 / +.207 / +.42 | Only gain; ~halfway (dB) to oracle; holds at every SNR (+1.8…+4.8 dB) |
| Babble, unseen talkers | −0.12 / −.004 / −.01 | +7.57 / +.247 / +.52 | **Null on the primary class**, despite large representational headroom |
| White noise (held-out class) | −1.03 / −.023 / .00 | +10.28 / +.182 / +1.02 | **Fails** the §4 held-out-class screen; negative at every SNR |
| All noisy (n=48) | +0.72 / −.001 / +.03 | +8.00 / +.212 / +.66 | Average is carried entirely by SSN |

Envelope domain (native I/O, primary) agrees: log-MAE
unprocessed → J4 → oracle = SSN 2.31 → 1.33 → 0.12; babble
1.71 → 1.53 → 0.13; white 3.01 → 2.93 → 0.10 (mask-MSE 0.513,
≈anti-correlated masks). Quiet: J4 SI-SDR 20.8 dB vs clean
(STOI .997, PESQ 4.62/4.64) — near-identity but not identity;
SI-SDR is the only one of the three that sees it. Trained-weights
causality re-verified in Gen 12 (shared prefix, differing
suffix → prefix mask Δ = 0.0 exactly).

## Honest limits

- **T0 only.** SI-SDR/STOI/PESQ are signal metrics on a
  noisy-phase reconstruction that is not part of J4-A1 and not
  how ACE would consume masked envelopes. They price the mask
  coarsely in familiar units. **No listener, SRT, bench,
  latency-on-target, or power data exists. No listener-benefit
  claim follows from the SSN numbers.**
- **A screen, not convergence.** 750 steps, single seed, loss
  still drifting down; 4 utterances/cell, 2 held-out speakers,
  no CIs. Point estimates only.
- **The failures are the finding.** Gain exists only on a
  trained stationary noise; the primary geometry (competing
  speech) earns nothing and an unseen noise class goes
  backwards. Filed as such per §4 — before any listener is
  recruited. Whether longer/broader training closes the babble
  gap is untested, not assumed either way.
- Corpus subset lives in `/tmp/gen12dl` (not committed);
  regenerate from the documented URL + archive SHA in
  [results.md](./results.md).

## J4 state

Unchanged: `promoted FALSE`, FROZEN retained, G3b BLOCKED,
validation set 0 ([candidate-J4-causal.md](../gen10/candidate-J4-causal.md)).
K-J4-0 (causality desk-kill) remains untriggered; nothing in
Gen 12 is promotion evidence — if anything, the babble null
and white-noise failure are evidence *against* promoting this
checkpoint. K1 (Stage 0 bench) and K-J4-2/3/4 (listener stages)
remain unevaluated.

## Next

| Step | Owner | Note |
|---|---|---|
| Longer/broader training re-screen (more steps, seeds, noise pool incl. non-SSN stationaries; babble + held-out class as primary readout, with CIs) | Machine | **Gate for everything downstream.** Spending listener time on a checkpoint with a T0 babble null is not justified |
| In-silico CI simulation as the T0 consumption model: masked envelopes → ACE-like channel vocoder / electrodogram (n-of-m selection, pulse-rate envelope sampling) → objective metrics on vocoded output, replacing noisy-phase OLA | Machine | Prices the mask as ACE would actually consume it; still T0, still **not** listening evidence |
| Normal-hearing vocoder *listening* study (SRT/intelligibility, J4 vs unprocessed vs oracle, counterbalanced, preregistered) | **Human** — design, ethics, recruitment, running | A design document can be drafted, but the study itself is human-subjects work. Per [protocol.md](../gen00/protocol.md) this is a T3 proxy: vocoder ≠ CI biology, and NH-vocoder arms in the prior literature were not counted as CI data ([attack-causal-extraction.md](../gen10/attack-causal-extraction.md)). It screens "could a listener use this mask at all", nothing more, and only earns its cost **after** the T0 re-screen shows a babble gain |
| Stage 0 bench (B1–B10: latency p99, power, thermal on H-primary), then Stage 1/2 listener SRT vs SCAN 2 | Lab / human subjects | Unchanged from Gen 11; no Gen 12 result moves these closer |

The generation's gain over Gen 11: the causal build now has
real-speech weights and measured objective behaviour — and the
measurement says the current checkpoint solves only the easiest
cell. That is a useful, cheap negative, filed at the right tier.
