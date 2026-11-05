# Gen 36 — output-contract repair candidate: INVESTIGATE (T0)

> Claude Opus 5.5, 2026-11-05 ~05:55.
> - Registration: [prereg.md](./prereg.md), with amendments 1 and 2. Astra cleared it after two NOT CLEARED reviews.
> - Rows: `contract_rows.json` (19,551 rows; 551 s). Decision: [contract_decision.json](./contract_decision.json).
> - Reviews: [Astra](./astra-review-gen36.md) and [Muse](./muse-review-gen36.md).
> - No training. `promoted FALSE`. **Nothing is published.**

**Decision: INVESTIGATE.**

| Gate | Result |
|---|---|
| G0 schema and binding (release tensors, config, enhance, model module; sealed fresh material; rebuilt identities) | ✓ |
| G1 polarity positive (every export target-only row; A2 on research target-only ears) | ✓ |
| G2 target preservation | ✗ |
| G3 noisy quality | ✗ |
| G4 alignment and cues (export lag 0; ILD/ITD vs the equally flushed A1; silence/tail) | ✓ |
| G5 headroom (pre-write and decoded peaks ≤ −1 dBFS plus the codec step; no full-scale samples) | ✓ |

**Where the failures are** (attributed from the rows; descriptive):

- **G3 fails only on the X2 regression panel** (the screen-v2 dry panel): 178 item-seeds.
  - **358 of X2's 512 inputs exceed full scale.** The panel reuses training-scale mixtures (clean RMS 0.1 plus babble), which were never meant to fit in a file.
  - 177 of the 178 failures are such inputs, and in all 178 the published output's pre-write peak is above 1 (up to 2.5).
  - There, E1's hard clip on write happens to score up to 0.68 dB higher SI-SDR than the candidate's clean −1 dBFS scaling, on items whose SI-SDR is around −9 dB.
  - X2 was not labelled as an overload panel in the registration. That is a design gap, missed in drafting and in review.
  - **G3 passes on every fresh F1 item** (all representable, at all rates and formats) and on X1, and the research per-ear checks on P1 and P4 pass.
- **G2 fails in three groups:**
  1. **Labelled overload items** (predicted in the registration):
     - all 630 F2 failures are |AC-gain error| on items whose input exceeds full scale;
     - the X3 level-0.56 items also fail on gain, some on waveform error;
     - two X3 cell means at level 0.56 (seed 17: medium, low) fail too.
     - The −1 dBFS cap attenuates these more than E1's clipped output loses.
  2. **Near-full-scale clean items:**
     - 13 X3q quiet crops and 19 X3 level-0.14 items have input peaks of about 0.82–1.02.
     - The cap binds and costs up to 0.56 dB more level than E1 loses.
     - E1 itself is about 2.3 dB below the input's level on these crops, because the published code spends part of the level on DC.
  3. **Research P1: 39 item-ears are floating-point ties, not losses.**
     - A2 and A1 differ only by a constant, so their |AC-gain error| is identical in theory. The largest "excess" is 7.9 × 10⁻⁸ dB.
     - The judge's strict ≤ has no numerical tie tolerance. That is a judge design flaw, recorded rather than waived.
- **On fresh, representable inputs the candidate passes everything:**
  - every F1 noisy item;
  - every representable F2 item-rate;
  - polarity, alignment, cues and headroom everywhere.

**Reading:**
- The candidate does what an output fix should for audio that fits in a file:
  - correct sign;
  - no DC;
  - speech at the input's level instead of about 2.3 dB under it;
  - never above −1 dBFS;
  - no change to the direction cues.
- The registered rule fails it on behaviour beyond full scale, where peak safety and level preservation trade off. It also fails it on numerical ties.
- No threshold is rescued, and nothing is published.
- What happens next is decided with the reviewers and, for any release, the owner:
  - an explicit, pre-registered overload policy (for example a declared input-headroom precondition or a limiter);
  - and a declared numerical tolerance for ties.
