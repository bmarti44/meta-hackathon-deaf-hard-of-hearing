# Gen 12 — J4-A1 trained on real speech: objective metrics (T0 only)

> **Model routing.** Requested: **Sol 6.1**. Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> **What this is:** first real-speech training of the Gen 11 J4-A1 build ([build-report.md](../gen11/build-report.md), spec [candidate-J4-causal.md §4](../gen10/candidate-J4-causal.md)) with held-out **objective, in-silico** metrics.
> **What this is not:** listener, SRT, intelligibility-in-humans, power, or on-processor evidence. **No listener-benefit claim is made or implied.** STOI/PESQ/SI-SDR are signal metrics on a T0 waveform reconstruction (below), not human outcomes.

## Files

| File | Contents |
|---|---|
| [train_j4.py](./train_j4.py) | Real-speech mixture generation + IRM training |
| [eval.py](./eval.py) | Held-out envelope + waveform-T0 evaluation |
| [train_log.json](./train_log.json) | Per-25-step loss log + run metadata |
| [eval_results.json](./eval_results.json) | All 52 per-utterance rows + aggregates |
| [j4a1_gen12.pt](./j4a1_gen12.pt) | Weights (953,088 B), SHA-256 `35a5d4bbee1699985bda79435d5eb06b8ca60c0db116345d9eeb1cba74b26269` |

Environment: `/tmp/gen9env` (Python 3.11.17, torch 2.15.0 CPU). `pystoi` and `pesq` were already installed in that env (verified importable and self-consistent: STOI(x,x)=1.0, PESQ-WB(x,x)=4.64); `pip` is absent from the env, so no install was needed or possible. SI-SDR is implemented in numpy in [eval.py](./eval.py).

## Data (real speech; download succeeded)

- **Corpus:** LibriSpeech `dev-clean`, OpenSLR 12. **URL:** https://www.openslr.org/resources/12/dev-clean.tar.gz (337,926,286 B).
- **Archive SHA-256 (this download):** `76f87d090650617fca0cac8f88b9416e0ebf80350acb97b343a85fa903728ab3`.
- **Licence:** Creative Commons Attribution 4.0 International (`LibriSpeech/LICENSE.TXT` in the archive, read this run).
- **Subset extracted:** 14 speakers, 924 FLAC (16 kHz mono, verified via soundfile) under `/tmp/gen12dl/LibriSpeech/dev-clean` (not committed; regenerate from the URL above).
  - Train target speakers (10; 661 files; 4,869 s pool): 84, 174, 251, 422, 652, 777, 1272, 1462, 1673, 1919.
  - Held-out target speakers (2, eval only): 1988, 1993.
  - Interferer-only speakers (2, eval babble only): 8842, 8297.
- **Mixtures (on-the-fly, seed 20261103):** 2 s target crops RMS-normalised to 0.1 + interferer at SNR −5…+10 dB. Interferer during training: 3-talker babble from other train speakers (70%) or generated speech-shaped noise (SSN; white noise through cascaded one-pole lowpasses — generated, not a recording) (30%). 10% of steps are clean/quiet with IRM = 1 (candidate-J4 §4 quiet-identity term).
- No synthetic fallback was needed; the synthetic component is only the SSN interferer, labelled as such.

## Training

- Target: ideal ratio mask in the model's own 64-band mel-envelope domain, `sqrt(E_clean/(E_clean+E_noise+eps))` (offline target, admissible per §4; identical definition to Gen 11 smoke). Loss: mask MSE. Adam lr 2e-3 → cosine to 2e-4, grad-clip 5. Batch 8 × 2.0 s.
- **Budget: 750 steps, 217 s wall on this CPU** (12,000 s of mixtures seen, with repetition from the 4,869 s pool).
- Loss (logged every 25 steps, single-batch so noisy): first-5 logged mean 0.148 → last-5 logged mean 0.112. Learning is real but modest; the run is short and per-batch loss remains SNR/condition-dominated.

## Evaluation protocol

- Held-out targets 1988/1993, 4 s crops, 4 utterances per cell (52 total). Conditions: **babble3-unseen** (interferers 8842/8297), **SSN** (trained class), **white-heldout** (noise class never trained — the §4 held-out-class screen), **quiet**. SNR −5/0/+5/+10 dB.
- **Envelope-domain (native I/O, primary):** mask-MSE vs IRM; log-envelope MAE of masked vs clean envelope (unprocessed / J4 / oracle IRM).
- **Waveform-domain (T0 reporting only):** J4-A1 emits no waveform (spec §2.1). Solely to compute SI-SDR/STOI/PESQ-WB, [eval.py](./eval.py) maps each mel mask to per-bin gains (filterbank-weighted; DC/Nyquist bins take the frame-mean mask), applies them to the noisy 128/64 STFT (**noisy phase**), and overlap-adds. Comparators pass through the *same* path: unprocessed-OLA (gain 1; identity check vs raw mixture: SI-SDR 139 dB after edge trim) and oracle mel-IRM (upper bound of this masking representation, not of enhancement in general). 256 samples trimmed at each end for every waveform metric.
- Development note: an initial WOLA variant (second synthesis window, division by OLA(win²)) produced edge explosions and a degraded identity path; it was caught by the identity check, replaced, and all numbers below are from the corrected path.

## Results (means over cells; per-SNR detail in [eval_results.json](./eval_results.json))

### Envelope domain (log-envelope MAE ↓, mask-MSE ↓)

| Condition | Unproc | J4-A1 | Oracle IRM | J4 mask-MSE |
|---|---|---|---|---|
| babble3-unseen | 1.708 | 1.528 | 0.129 | 0.170 |
| SSN | 2.306 | 1.334 | 0.124 | 0.054 |
| white-heldout | 3.008 | 2.927 | 0.099 | 0.513 |
| quiet | 0.000 | 0.273 | 0.021 | 0.073 |

### Waveform T0 (SI-SDR dB ↑ / STOI ↑ / PESQ-WB ↑), noisy-phase reconstruction

| Condition | Unproc-OLA | J4-A1 | Oracle IRM | Δ J4−Unproc |
|---|---|---|---|---|
| babble3-unseen | 2.55 / .677 / 1.17 | 2.43 / .673 / 1.17 | 10.12 / .924 / 1.70 | −0.12 dB / −.004 / −.01 |
| SSN | 2.47 / .702 / 1.10 | 5.79 / .726 / 1.22 | 8.61 / .909 / 1.53 | **+3.31 dB / +.024 / +.11** |
| white-heldout | 2.45 / .764 / 1.05 | 1.42 / .741 / 1.05 | 12.73 / .946 / 2.08 | −1.03 dB / −.023 / .00 |
| All noisy (n=48) | 2.49 / .715 / 1.11 | 3.21 / .713 / 1.14 | 10.49 / .926 / 1.77 | +0.72 dB / −.002 / +.03 |

Quiet: J4 SI-SDR 20.8 dB vs clean (unprocessed path ≈139 dB), STOI .997, PESQ 4.62 vs 4.64 — the mask is close to but not exactly identity on clean speech; SI-SDR is the sensitive readout here, STOI/PESQ are near ceiling and near-blind to it.

Per-SNR pattern (in JSON): SSN gains hold at every SNR (−5 dB: +3.46 dB SI-SDR; 0 dB: +4.75; +5: +3.23; +10: +1.80). Babble is within ±0.7 dB of unprocessed at every SNR. White is negative at every SNR.

## Reading (T0 engineering screen, nothing more)

1. **Stationary trained noise works, a little.** On SSN the causal mask buys ≈+3.3 dB SI-SDR and small STOI/PESQ gains, about halfway (in dB) to the mel-IRM oracle. This is the easiest cell and the one most represented (as a stationary class) in training.
2. **Unseen-talker babble does not.** ΔSI-SDR −0.12 dB, ΔSTOI −0.004 against unprocessed, with a +7.6 dB oracle gap proving the representation could express a far better mask. Babble is the primary geometry class of the J-lineage; at this training budget the build earns nothing there. This echoes, at T0, the recorded class weakness in candidate-J4 §1/§4 (2017 speaker-independent babble null) — it does not replicate or refute any human result.
3. **Held-out noise class fails as §4 feared.** White noise: mask-MSE 0.513 (≈anti-correlated masks), metrics at or below unprocessed. A build whose gain exists only on trained noises is filed as such, per §4 — here, before any listener is recruited.
4. **Causality is preserved by the trained weights** (architecture property, re-verified this run: identical 0.5 s prefix + differing suffix → prefix mask Δ = 0.0 exactly, 124 frames).

## Unresolved / not done

- 750 steps is a screen, not convergence; loss was still drifting down. Longer training, LR/schedule search, and broader noise pools are untested. No claim that more training closes the babble gap — that is exactly what a next run would measure.
- Single seed; 4 utterances/cell; no CIs computed. Numbers are point estimates on 52 held-out crops from 2 speakers.
- Waveform metrics use an 8 ms/4 ms noisy-phase reconstruction that is not part of J4-A1 and not how ACE would consume masked envelopes; they price the mask, coarsely, in familiar units.
- No bench (Stage 0), no latency/power measurement, no listener data. J4 status unchanged: `promoted FALSE`, validation set 0.

Run commands:

```bash
/tmp/gen9env/bin/python research/gen12/train_j4.py --steps 750
/tmp/gen9env/bin/python research/gen12/eval.py --n-per-cell 4
```
