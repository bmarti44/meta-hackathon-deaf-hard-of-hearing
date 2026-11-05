# Gen 33 — linked two-ear processing on frozen Gen 32 weights: REJECTED (feasibility, T0)

> Claude Opus 5.5, 2026-11-05 ~03:10.
> - Registration: [prereg.md](./prereg.md), with amendment 1. Astra cleared it after a NOT CLEARED review and a verification; Muse cleared it.
> - Decision: [link_s17.json](./link_s17.json), from `judge_link.py`.
> - Reviews: [Astra](./astra-review-gen33.md) and [Muse](./muse-review-gen33.md).
> - Run time 29 s. `promoted FALSE`. Gen 32 stays FAIL.

**Decision:** REJECTED. All four checks fail:
- **L1:** original SP. Mirrored ILD is +0.096 dB vs Gen 19 and mirrored ITD +0.125 samples.
- **L2:** crossed mean target-ILD error is 5.523 dB linked vs 5.492 dB independent Gen 32. That is higher, not lower.
- **L3:** linked is worse than Gen 19 in some subsets: ILD at +5 and +10 dB, and ITD at 0 dB.
- **L4:** per-ear clarity is below a control in 18 of 40 comparisons.

**What linking did, by SNR** (crossed scenes; left and right mirror subsets
are identical by symmetry):

| SNR | target-ILD error, linked vs Gen 19 (dB) | ITD error vs Gen 19 (samples) | per-ear SI-SDR vs Gen 19 indep (dB) |
|---|---|---|---|
| −5 dB | **−0.74 (better)** | 0 | ≥ 0 |
| 0 dB | **−0.75 (better)** | +0.5 (worse) | −0.05 |
| +5 dB | +0.85 (worse) | 0 | −0.18 |
| +10 dB | +1.02 (worse) | 0 | −1.04 |

**Existing bench, 4 scenes:**
- ILD *distortion*, how far processing moved the cues away from the mixture: 0.39 dB linked vs 1.04 dB independent Gen 32. Linking keeps the mixture's cues much better.
- Target-ILD error: 5.60 linked vs 5.52 independent. Linking does not move the cues toward the clean voice's own cues.

**Descriptive, not gating:**
- **Gen 19 with linking:** crossed mean target-ILD error 5.471 vs 5.427 independent. At −5 dB, per-ear SI-SDR is +0.12 dB and STOI +0.004 vs independent Gen 19.
- **Target-only scenes:** with no crowd, linked target-ILD error is 0.21 dB vs 0.18 independent Gen 32, and ITD error is 0 for all systems.
- **Worst ear per scene:** linked loses 0.87 dB SI-SDR vs independent Gen 32 in noisy scenes.

**Reading** (16 crossed scenes, one seed, an assumed head model; descriptive beyond the registered rule):
- **This wrapper:** a shared mask helps the direction cue in hard noise (−5 / 0 dB) and hurts it, and each ear's clarity, in easier noise (+5 / +10 dB).
- **What the measures say:**
  - It keeps the *mixture's* cues (low ILD distortion).
  - The registered measure rewards matching the *clean voice's* cues.
  - The two measures disagree about which behaviour is better for a listener, and these data cannot settle that.
- **No change after the result:** the decision rule forbids any tuning of the pooling or of SNR-dependent linking on these 16 scenes. Any such idea needs its own registration and fresh scenes.
- No localisation or speech benefit is established. Nucleus 6 two-ear synchronisation is unverified.

**Artifacts committed:**
- the four stereo-runner documents: Gen 19 / Gen 32 independent, Gen 32 / Gen 19 linked;
- `link_s17.json`.
