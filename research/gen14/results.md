# Gen 14 — J4 training redesign screen: loss / babble pool / target / LR (T0 only)

> **Model routing.** Requested: **Sol 6.1**. Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> **What this is:** the Gen 13 follow-up. Gen 13 ([results.md](../gen13/results.md)) showed a seed-stable babble null at 4× steps — same-recipe more-steps is a **closed lever**. Gen 14 changes levers instead, architecture ([j4_model.py](../gen11/j4_model.py)) imported **exactly unchanged** (238,656 params asserted; causality re-verified, below).
> **What this is not:** listener, SRT, intelligibility-in-humans, power, or on-processor evidence. **No listener-benefit claim is made or implied.** ACE-sim numbers are T0 in-silico only. J4 status unchanged: `promoted FALSE`.

## Gate (stated in advance) and verdict

**Gate:** per config, seed-mean babble ΔSI-SDR (Gen 13 [eval2.py](../gen13/eval2.py) protocol) bootstrap 95% CI excluding 0 on the positive side = signal; otherwise this recipe family is closed.

**Verdict: no signal — recipe family closed (at screen scale; caveats below).** Best config C2: **+0.06 dB [−0.01, +0.12]**; C1: **−0.01 dB [−0.04, +0.02]**. Neither CI excludes 0. No Gen 14 checkpoint earns listener time.

## Levers and screen design

- **(a) Loss:** mask-MSE + envelope SI-SDR-style term `0.01 × (−SI-SDR_dB)` between masked mel envelope (applied mask × mixture envelope) and clean mel envelope, flattened per item. Weight set by smoke test so the two terms are comparable at init (envSI-SDR ≈ +12 dB, mask-MSE ≈ 0.15).
- **(b) Pool:** babble k ~ U{2..8} talkers (Gen 13: U{2,3,4}); SNR curriculum widening to −5…+15 dB (progress <⅓: U[0,15]; <⅔: U[−2.5,15]; else U[−5,15]; Gen 13: U[−5,10] fixed). Retained: 10% quiet, noisy 70% babble / 30% SSN, interferers from train speakers only, target excluded.
- **(c) Target:** cIRM-style **compressed magnitude** mask IRM^0.5 vs plain IRM. A true complex IRM is impossible in this envelope-only sigmoid architecture — this is the compressed-magnitude part only. Compressed training is **decompressed at inference** (applied mask = predicted²), in the envelope loss and all eval paths. Note eval mask-MSE is still scored against plain IRM (Gen 13 comparability).
- **(d) LR:** Adam 2e-3 cosine to **2e-5** final (Gen 13: 2e-4). Bundled with (b) in all non-control configs; **not isolated** (declared limit).

| Config | (a) env loss | (b) new pool | (c) cIRM target | (d) LR→2e-5 | Isolates |
|---|---|---|---|---|---|
| C0 control | – | – | – | – | Gen 13 recipe replica |
| C1 | ✓ | ✓ | – | ✓ | C1 vs C3 → (a) |
| C2 | ✓ | ✓ | ✓ | ✓ | C2 vs C1 → (c) |
| C3 | – | ✓ | – | ✓ | C3 vs C0 → (b)+(d) |

**Scale:** 700 steps/config (batch 8 × 2 s, as Gen 13). Justification: Gen 12's 750-step and Gen 13's 3000-step runs gave the identical babble point estimate (−0.12 dB), so ~700 steps is the comparable screen point for this family. Data/holdout identical to Gen 13 (imported from [train2.py](../gen13/train2.py), speaker-holdout asserted).

**Selection (pre-registered):** rank by mean babble ΔSI-SDR on the exact eval2 babble crops (quick waveform readout), guardrail SSN ΔSI-SDR > 0; top-2 redesign configs get a second seed. Control ranking is reported, not selected (Gen 13 already ran it at 3000 steps × 3 seeds).

## Screen results (seed 20261113, quick eval, n=32/condition)

| Config | Babble ΔSI-SDR | SSN ΔSI-SDR | Babble logMAE impr. |
|---|---|---|---|
| C0 control | +0.04 | +3.54 | +0.16 |
| C1 (a+b+d) | −0.01 | +2.42 | +0.16 |
| C2 (a+b+c+d) | **+0.07** | +3.32 | +0.17 |
| C3 (b+d) | −0.10 | +3.60 | +0.17 |

All four babble values lie within 0.17 dB of each other and of zero; the control ranks second overall — itself evidence the levers add ~nothing on babble at this scale. Selected for seed 2: **C2 and C1** (top-2 redesign configs; the pair also isolates lever (c) at the final stage). Ablation reads: (a) C1−C3 = +0.09 dB; (c) C2−C1 = +0.07 dB; (b)+(d) C3−C0 = −0.13 dB. All are single-seed, sub-0.15 dB differences on 32 crops — noise-scale, not effects.

## Final results (best-2 × 2 seeds, full Gen 13 eval2 protocol)

104 paired crops (RNG 777), per-seed means and seed-mean (per-crop metrics averaged over the config's 2 seeds first), paired bootstrap 2000 resamples, seed 13 — identical machinery to Gen 13 ([train3.py](./train3.py) `fulleval` imports eval2's `eval_one_model`). Δ = J4 − unprocessed.

### Babble, held-out speakers (primary, n=32)

| Config | ΔSI-SDR seed-mean [95% CI] | per-seed ΔSI-SDR | ΔSTOI | logMAE impr. | ACE Δcorr | ACE Δchan-SNR |
|---|---|---|---|---|---|---|
| C1 | **−0.01 [−0.04, +0.02]** | −0.01 / −0.01 | −0.001 | +0.16 | −0.001 | +0.02 |
| C2 | **+0.06 [−0.01, +0.12]** | +0.07 / +0.05 | −0.005 | +0.17 | −0.003 | +0.14 |

Absolute seed-mean SI-SDR (unproc/J4/oracle IRM): C1 2.47/2.46/9.99; C2 2.47/2.53/9.99 dB. Mask-MSE vs IRM ≈ 0.16 (both) — the same as Gen 13's 3000-step models (0.16–0.17). For reference Gen 13 seed-mean babble was −0.12 [−0.34, +0.12] with ACE Δchan-SNR +0.55: Gen 14's CIs are tighter around a value just as indistinguishable from zero, and the ACE channel-SNR gain is smaller. The oracle gap (+7.5 dB) is unchanged — the representation can express a better mask; none of these recipes find it for competing speech.

### Other conditions (seed-mean ΔSI-SDR)

| Config | SSN (trained) | White (held-out class) |
|---|---|---|
| C1 | +1.21 [+1.06, +1.39] — **see collapse note** | −0.13 [−0.24, −0.04] |
| C2 | +3.30 [+2.88, +3.76] (per-seed +3.32/+3.29) | −0.76 [−1.08, −0.47] |

Held-out white noise remains a failure for every config (Gen 13: −2.65 dB; less negative here partly because screen-scale models mask less aggressively — mask-MSE 0.19–0.21 vs 0.29–0.44). The §4 held-out-class screen still fails.

## Mechanism finding: the envelope SI-SDR term has a constant-mask degenerate optimum

Mask statistics on eval crops explain the C1 anomaly and are the most actionable result of this generation:

- **C1 seed 20261114 collapsed to a constant mask** ≈ 0.515 everywhere (within-crop std 0.001 on SSN/quiet, 0.016 on babble; Gen 13 model: 0.10–0.17). A constant mask is a pure gain — invisible to both SI-SDR readouts (waveform and envelope are scale-invariant) and a stationary point the 0.01-weighted envelope term does not escape. Its SSN ΔSI-SDR is +0.005 (vs seed 1's +2.42), so C1's seed-mean SSN (+1.21) averages a working model with a no-op; treat C1 SSN seed-mean as uninterpretable.
- **Quiet identity is degraded in all envelope-loss configs.** C1/C2 quiet masks sit at ≈0.54–0.58, near-constant (Gen 13: 0.90). Envelope logMAE worsens by 0.55–0.64 on quiet while waveform SI-SDR misleadingly reads 48–71 dB (scale invariance again). The ACE path consumes envelopes, so a constant ~0.55 gain is a real level error there even though correlations are unaffected. Lever (a) **as specified (scale-invariant)** is therefore not merely null — it is harmful to calibration. A non-scale-invariant envelope loss (e.g. log-envelope MAE, or envelope SDR without the projection) would be a *different* lever; it was not tested here and this closure does not cover it.
- C2 did not collapse in either seed and kept Gen-12-level SSN performance (+3.3 dB). Decompression (applied = pred²) makes a constant prediction a worse optimum than in C1, but with n=2 seeds this is an observation, not an established protective effect.
- Babble masks are flatter than SSN masks in every config (within-crop std ≈0.07–0.14 vs 0.11–0.17; means ≈0.51–0.58, i.e. near the 0.5 "do little" point) — same signature as Gen 13: the model does not find time-frequency structure that separates competing talkers.

## Verification

- Causality: shared 0.5 s prefix / differing suffix → prefix mask Δ = 0.0 exactly (123 frames) for all 4 final checkpoints, including through C2's pointwise decompression (`train3.py causality`).
- Architecture: param count asserted 238,656 at every run; Gen 11 suite re-run: **7 passed**.
- Eval determinism/protocol: crops, metrics, ACE sim, bootstrap imported unchanged from Gen 13; per-crop rows in [weights/](./weights) (`fulleval_rows_*.json`, `fulleval_summary.json`).

## Budget accounting

6 train runs × 700 steps. Per-run wall 329–347 s; run 4-way/2-way parallel on an 18-core CPU. Summed single-process train time ≈ 34 min (≈ the ~30 min budget, slightly over); total elapsed wall for training + all evals ≈ 13 min. Quick eval 21 s; full eval 36 s wall (4 checkpoints parallel).

## Reading and what remains open

1. **The gate closes this family:** mask-MSE ± scale-invariant envelope loss, IRM or compressed-IRM targets, babble pools up to k=8 with an SNR curriculum, and lower final LR — none moves babble ΔSI-SDR off zero (best CI [−0.01, +0.12] dB against a +7.5 dB oracle gap). Combined with Gen 13 (steps closed), the *training-recipe* axis around the current target representation is exhausted at screen scale.
2. **Caveats on the closure.** (i) Screen scale is 700 steps, not 3000 — the closure leans on Gen 12→13's demonstrated step-invariance of the babble readout for this family. (ii) CIs cover 32 crops from 2 held-out speakers (not a speaker-population CI), as in Gen 13. (iii) Lever (d) was bundled, not isolated. (iv) Lever (a) was tested in its scale-invariant form, which has the degenerate optimum above; a level-aware envelope loss is untested.
3. **What would reopen the question** is therefore not another recipe tweak in this family, but a different training signal class (level-aware envelope objectives, discriminative/contrastive talker-separation signals), a different noise-world (recorded multi-talker scenes rather than synthetic sums), or a representation change — each a new design decision, not a Gen 14 continuation. No checkpoint from Gen 12–14 has earned listener time; status remains `promoted FALSE`, validation set 0.

## Files

| File | Contents |
|---|---|
| [train3.py](./train3.py) | Screen/train/quickeval/fulleval/causality modes; CONFIGS C0–C3; levers (a)–(d) |
| [weights/](./weights) | `C{0,3}_seed20261113.pt`, `C{1,2}_seed{20261113,20261114}.pt`, train logs, `quickeval.json`, `fulleval_rows_*.json`, `fulleval_summary.json` |

Run commands:

```bash
/tmp/gen9env/bin/python research/gen14/train3.py screen --steps 700
/tmp/gen9env/bin/python research/gen14/train3.py quickeval --weights research/gen14/weights/C*_seed20261113.pt
/tmp/gen9env/bin/python research/gen14/train3.py train --config C1 --seed 20261114 --steps 700  # and C2
/tmp/gen9env/bin/python research/gen14/train3.py fulleval
/tmp/gen9env/bin/python research/gen14/train3.py causality --weights research/gen14/weights/C{1,2}_seed*.pt
```
