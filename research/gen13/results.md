# Gen 13 — J4 re-screen: 3000 steps × 3 seeds + ACE consumption model (T0 only)

> **Model routing.** Requested: **Sol 6.1**. Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> **What this is:** the Gen 12 next-step gate ([Gen12-summary.md Next](../gen12/Gen12-summary.md)): longer training of the unchanged Gen 11 J4-A1 architecture with babble in training, 3 seeds, bootstrap CIs, plus an in-silico ACE-like consumption model replacing part of the noisy-phase OLA readout.
> **What this is not:** listener, SRT, intelligibility-in-humans, power, or on-processor evidence. **No listener-benefit claim is made or implied.** ACE-sim numbers are **T0 in-silico, NOT listening evidence**. J4 status unchanged: `promoted FALSE`, validation set 0.

## Files

| File | Contents |
|---|---|
| [train2.py](./train2.py) | Retraining (arch. unchanged, `--seed`, default 3000 steps) |
| [eval2.py](./eval2.py) | Paired held-out eval: envelope + waveform-T0 + ACE + bootstrap CIs |
| [ace_sim.py](./ace_sim.py) | Simplified ACE-like electrodogram (22 ch, 8-of-22); params cited/ASSUMED in its docstring |
| [eval_results.json](./eval_results.json) | 312 per-crop rows (104 crops × 3 seeds) + summaries with CIs |
| [weights/](./weights) | `j4_seed{20261103,104,105}.pt` + per-seed `train_log_seed*.json` |

Weights SHA-256: seed20261103 `dc57333e…e555d7`, seed20261104 `d61aa478…27ca5a`, seed20261105 `567e6b69…0eb196` (full hashes in the train logs). Environment: `/tmp/gen9env` (Python 3.11, torch 2.15.0 CPU), as Gen 12.

## Data and holdout (whole noise class + speakers held out)

- Corpus: LibriSpeech `dev-clean` (OpenSLR 12, CC BY 4.0), same `/tmp/gen12dl` subset as Gen 12 (regenerate per [gen12/results.md](../gen12/results.md): URL + archive SHA-256 `76f87d09…728ab3`).
- Train target speakers (10): 84, 174, 251, 422, 652, 777, 1272, 1462, 1673, 1919 (661 files, 4,869 s). Held-out targets: 1988, 1993. Interferer-only speakers (eval babble): 8842, 8297. No held-out speaker appears in any training pool (asserted in [train2.py](./train2.py)).
- Training interferers: multi-talker babble drawn only from train speakers (target excluded per item), or generated SSN (Gen 12 generator; not a recording). **White noise is never trained** — it is the held-out noise **class**. Eval babble is therefore a **seen class with held-out speakers**; eval white is an **unseen class**.

## Training

- Architecture and target identical to Gen 12: [j4_model.py](../gen11/j4_model.py) imported unchanged (238,656 params, asserted), mel-envelope IRM target, mask-MSE, Adam 2e-3 cosine to 2e-4, clip 5, batch 8 × 2 s, SNR −5…+10 dB, 10% quiet, noisy items 70% babble / 30% SSN.
- One deliberate mixture change vs Gen 12, recorded so the comparison is not overstated: babble talker count k ~ U{2,3,4} instead of fixed k=3 (broader babble pool).
- Note on the task wording: babble was already in Gen 12 training (70%). Gen 13 keeps that and changes budget/seeds/mixture breadth — it is a re-screen, not a first exposure to babble.

| Seed | Steps | Wall (s) | Loss first-5 → last-5 logged |
|---|---|---|---|
| 20261103 | 3000 | 1116 | 0.147 → 0.100 |
| 20261104 | 3000 | 1100 | 0.147 → 0.108 |
| 20261105 | 3000 | 1087 | 0.155 → 0.112 |

Loss is per-batch mask-MSE (SNR/condition-dominated, noisy). For scale, Gen 12's 750-step run went 0.148 → 0.112.

## ACE consumption model ([ace_sim.py](./ace_sim.py))

Simplified ACE-like electrodogram, T0 only. Primary path consumes J4's native output (masked 64-band mel envelopes) with **no waveform synthesis**: mel energies → 22 ACE channels by filterbank-overlap map → 8-of-22 maxima selection per 4 ms frame. Unprocessed/oracle pass through the same map; reference is clean-speech envelopes.

- Cited from web sources inspected 2026-11-03 (full notes in the [ace_sim.py](./ace_sim.py) docstring): 22 channels; 8 maxima default; 900 pps/channel nominal; allocation 188–7938 Hz, linear to ~1312 Hz then logarithmic.
- **ASSUMED** (labeled in code): exact 23-edge table (9 linear + 13 log bands constructed from the cited rule, not a copied clinical table); no pre-emphasis/AGC; no T/C loudness mapping (electrodogram = linear amplitudes); no pulse timing/interleaving, current spread, or neural model; envelope rate = J4's 250 frames/s, not 900 pps cycles; mel→ACE overlap map is an approximation.
- Sanity checks run: n-of-m keeps exactly 8/frame; identity correlation 1.0; mel-path vs waveform-path clean ACE envelopes correlate r = 0.9999 (one 4 s held-out utterance); mel bands below 188 Hz map to no ACE channel (column sums 0), as the allocation implies.
- ACE metrics per crop: 22-ch envelope correlation vs clean (pre-selection), electrodogram correlation vs clean electrodogram (post-selection), maxima-selection overlap vs clean, channel-SNR from clean/noise components through the same mask.

## Evaluation protocol

- 104 paired 4 s crops (eval RNG 777, as Gen 12): conditions **SSN** (trained class), **babble-heldout-spk** (seen class, held-out interferers 8842/8297), **white-heldout** (held-out class) at SNR −5/0/+5/+10 dB × 8 crops (n=32/condition), plus 8 quiet. Identical crops for every seed/system.
- Envelope domain (primary): mask-MSE vs IRM, log-envelope MAE. Waveform T0 (Gen 12 comparability only): SI-SDR/STOI/PESQ-WB via Gen 12's noisy-phase OLA path. ACE domain: above.
- CIs: paired bootstrap over eval crops (2000 resamples, percentile 95%, seeded), per seed and for seed-mean (per-crop metrics averaged over seeds first). CIs cover eval-crop sampling only — 2 held-out target speakers, so they are **not** speaker-population CIs.
- Determinism: eval re-run produced a bit-identical JSON. Causality re-verified per seed (shared 0.5 s prefix, differing suffix → prefix mask Δ = 0.0 exactly, 124 frames). Gen 11 suite: 7 passed.

## Results

Δ = J4 − unprocessed (paired, same crops). Brackets are 95% bootstrap CIs over crops. Full per-crop rows and every metric in [eval_results.json](./eval_results.json).

### Waveform T0 + native envelope (ΔSI-SDR dB / ΔSTOI / log-MAE improvement; mask-MSE)

| Seed | SSN (n=32) | Babble, held-out spk (n=32) | White, held-out class (n=32) |
|---|---|---|---|
| 20261103 | +4.06 [+3.55,+4.55] / +.041 / +1.12; MSE .043 | −0.00 [−0.22,+0.21] / −.005 / +0.18; MSE .162 | −2.56 [−3.17,−2.03] / −.051 / +0.17; MSE .380 |
| 20261104 | +3.92 [+3.44,+4.38] / +.046 / +1.09; MSE .044 | −0.23 [−0.52,+0.04] / −.006 / +0.17; MSE .170 | −2.00 [−2.61,−1.48] / −.032 / +0.12; MSE .438 |
| 20261105 | +4.09 [+3.62,+4.57] / +.040 / +1.14; MSE .042 | −0.12 [−0.34,+0.11] / −.008 / +0.18; MSE .162 | −3.38 [−3.90,−2.90] / −.051 / +0.25; MSE .294 |
| Seed-mean | **+4.02 [+3.55,+4.48]** / +.042 / +1.12 | **−0.12 [−0.34,+0.12]** / −.006 / +0.18 | **−2.65 [−3.14,−2.16]** / −.045 / +0.18 |

(STOI CIs exclude 0 wherever the sign is shown consistent above; PESQ seed-mean Δ: SSN +0.13, babble +0.02, white −0.01. Detail in JSON.)

Absolute seed-mean levels (unproc / J4 / oracle IRM): SI-SDR SSN 2.46/6.49/8.73 dB; babble 2.47/2.35/9.99; white 2.46/−0.18/12.42. Oracle = upper bound of this mel-IRM representation only.

### Through the ACE sim (seed-mean; unproc / J4 / oracle, then ΔJ4−unproc [CI])

| Condition | Env. corr. | Δ corr | Chan-SNR (dB) | Δ chan-SNR | Maxima overlap | Δ overlap |
|---|---|---|---|---|---|---|
| SSN | .759/.890/.982 | +.131 [+.092,+.172] | 3.5/8.0/9.7 | +4.53 [+4.10,+4.96] | .617/.669/.944 | +.053 [+.046,+.060] |
| Babble held-out spk | .688/.674/.991 | −.014 [−.023,−.006] | 3.0/3.6/10.9 | +0.55 [+0.28,+0.81] | .674/.678/.940 | +.004 [+.002,+.006] |
| White held-out | .735/.610/.983 | −.125 [−.152,−.100] | 4.0/1.9/14.3 | −2.11 [−2.61,−1.63] | .486/.465/.943 | −.022 [−.031,−.013] |

Per-seed ACE Δs agree in sign in every cell (babble Δcorr −.011/−.016/−.016; Δchan-SNR +0.61/+0.49/+0.55; white Δcorr −.136/−.099/−.140). Electrodogram correlation (post-selection) tracks envelope correlation (seed-mean Δ: SSN +.162, babble −.010, white −.106).

Quiet (n=8): J4 SI-SDR vs clean 21.2/25.4/21.4 dB by seed (Gen 12: 20.8 dB), STOI ≈ .998, PESQ 4.62; ACE env. corr. .994–.997, maxima overlap .978–.991 — near-identity, not identity, as in Gen 12. (Quiet ΔSI-SDR vs the unprocessed-OLA identity path is not informative and is not headlined.)

## Reading vs Gen 12 (T0 engineering screen, nothing more)

1. **More training did not close the babble gap.** At 4× the steps, 3 seeds, broader babble mixtures: babble ΔSI-SDR −0.12 dB [−0.34,+0.12] — statistically indistinguishable from unprocessed and numerically identical to Gen 12's −0.12 dB point estimate. All three seeds agree. The oracle gap (+7.5 dB) shows the representation could express a better mask; this training recipe does not find it for competing speech. The ACE readout sharpens the picture: the mask removes some noise energy (channel-SNR +0.55 dB) but slightly *degrades* envelope fidelity to clean (corr −.014) and barely changes which channels ACE would stimulate (+.004 overlap). Energy suppression without envelope fidelity is not a plausible substrate for listener gain — stated as an engineering reading, not a perception claim.
2. **SSN gain grew modestly and is seed-stable:** +4.02 dB (Gen 12: +3.31), ACE corr +.131, chan-SNR +4.53 dB. Still only the trained stationary class.
3. **Held-out white noise got worse, not better:** −2.65 dB (Gen 12: −1.03), ACE corr −.125 — every seed, every CIs exclude 0. Longer training on the same noise pool entrenched class specificity. The §4 held-out-class screen fails more clearly than in Gen 12.
4. The Gen 12 gate ("spending listener time on a checkpoint with a T0 babble null is not justified") therefore still binds: **no Gen 13 checkpoint earns listener time on this evidence.** What would change the question is a different training signal/objective or noise-pool design that first shows a babble gain at T0 — not more steps of the same recipe (3000 steps here; loss still drifting slowly, but the babble readout did not move between 750 and 3000 steps).

## Unresolved / not done

- CIs are over 32 crops/condition from 2 held-out speakers; speaker generalisation untested. Seeds vary training RNG only (same data pool, same eval set).
- ACE sim is deliberately crude (ASSUMED items above; 250 fps vs 900 pps; no loudness/neural model). It prices envelope delivery to an n-of-m selector; it cannot rank perceptual outcomes.
- No LR/schedule search, no loss change (e.g. envelope-domain or multi-resolution losses), no broader stationary/non-stationary noise pool, no babble-specific curriculum — all untested, none assumed to help.
- No bench (Stage 0), no latency/power measurement, no listener data. Status unchanged: `promoted FALSE`.

Run commands:

```bash
for s in 20261103 20261104 20261105; do /tmp/gen9env/bin/python research/gen13/train2.py --seed $s --steps 3000; done
/tmp/gen9env/bin/python research/gen13/eval2.py --n-per-cell 8
/tmp/gen9env/bin/python research/gen13/ace_sim.py   # self-checks
```
