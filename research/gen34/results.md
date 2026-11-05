# Gen 34 — frozen real-recording audit (BRUDEX): VALID ASSET (T0)

> Claude Opus 5.5, 2026-11-05 ~04:05.
> - Registration: [prereg.md](./prereg.md), with amendments 1 and 2. Astra cleared it after a NOT CLEARED review and two verifications.
> - Data: [audit_s17.json](./audit_s17.json). Decision: [asset_verdict_v1.json](./asset_verdict_v1.json).
> - Reviews: [Astra](./astra-review-gen34.md) and [Muse](./muse-review-gen34.md).
> - Evaluation only: no model was trained or selected. `promoted FALSE`.

**Decision: VALID ASSET.** All integrity checks pass:
- A1: provenance and sha256 for 51 files;
- A2: recording overlap excluded by documented SQAM/VCTK provenance; speaker identity unresolved;
- A3: complete 240-item grid for every system;
- A4: channel and delay direction correct for all 16 low-setting target-only items;
- A5: bypass identity;
- A6: two Gen 19 runs identical;
- A7: all 9 metrics present and finite; registered checkpoint hashes; the material hash `a133dd76…` reproduces.

The recordings are now development material. Confirmation needs different voices and rooms.

## What the frozen models do to real recorded speech (descriptive)

**Setup:** each-ear means over 4 talkers × 4 azimuths per cell. These are
mixtures of acoustically recorded speech and babble from one lab at three
reverberation settings. Each ear's reference is that ear's recorded
reverberant talker.

**Gen 19 vs bypass:**

| Setting (T60) | −5 dB | 0 dB | +5 dB | +10 dB |
|---|---|---|---|---|
| low (0.31 s): SI-SDR / STOI | +3.17 / +0.031 | +3.87 / +0.065 | +2.71 / +0.050 | +1.07 / +0.024 |
| medium (0.51 s) | +2.40 / +0.028 | +2.97 / +0.053 | +1.57 / +0.033 | −0.31 / +0.004 |
| high (1.3 s) | +1.36 / −0.000 | +1.61 / +0.014 | +0.06 / −0.007 | **−2.00 / −0.034** |

**Clean reverberant speech alone (target-only), absolute, bypass = 1.000:**
- Gen 19 STOI: 0.971 (low), 0.955 (medium), 0.941 (high).
- Gen 32 STOI: 0.973 / 0.959 / 0.950.

**Gen 32 vs Gen 19:**
- STOI is higher in **15 of 15** cell means. These pool both ears; it is not a universal improvement. Gen 32 loses STOI on 126 of 384 noisy item-ear comparisons, and talker 2 has a small negative overall mean difference (Astra).
- SI-SDR is higher in 11 of 15 cells.
- Target-only SI-SDR is +0.8 to +1.0 dB higher.
- Worst-ear differences: the worst cell-average worst-ear difference is −0.13 dB, and the worst individual noisy item-ear SI-SDR difference is −0.76 dB.

**Reading** (one lab, 4 talkers, development material; descriptive only; wording tightened per Astra and Muse):
- **Gen 19 improves these objective scores in several recorded-babble conditions.**
  - The gains are largest at −5 / 0 dB in the least reverberant setting, and they shrink as reverberation grows.
  - Neither speech understanding nor preserved localisation is demonstrated.
- **Reference fidelity vs intelligibility:** BRUDEX scores against the full reverberant recording, while the room trainer targets direct sound plus 50 ms. A lower target-only STOI flags changed speech; on its own it does not prove that removing reverberation hurts listeners (Astra).
- **Spatial diagnostics:** target-only ILD error is 1.27 / 1.54 / 1.42 dB for Gen 19 and 1.06 / 1.29 / 1.20 dB for Gen 32, vs 0 for bypass. At high reverberation, Gen 19 raises noisy-output target-ILD error at every SNR. These diagnostics do not establish localisation ability.
- **It costs in quiet, echoey conditions.**
  - At +10 dB in the 1.3 s setting it lowers SI-SDR (−2.0 dB) and STOI (−0.034).
  - It also lowers STOI on clean reverberant speech by 0.03 to 0.06.
  - This is the same problem the room line set out to fix.
- **Gen 32, the room-trained candidate that failed its synthetic screen, is slightly better than Gen 19 on these real recordings.**
  - The edge is in every cell for STOI, and in clean reverberant speech.
  - The differences are small and from one seed, so they are not evidence of a listener benefit.
  - It is still the first real-recording sign that the room work moves in the intended direction.

## Two deployment defects the audit exposed: output polarity and DC offset

**Polarity** (`polarity_check.py` → `polarity_check.json`):
- The output is a sign-flipped copy of the voice for Gen 19 seeds 17 and 19 and for Gen 32. Seed 18 is not flipped.
- Astra confirmed the sign on all 96 target-only ear recordings per checkpoint.
- The sign is constant from step 500 onward in every seed (the intermediate checkpoints, committed evidence).
- The SI-SDR loss is sign-blind, so training never fixed it.
- STOI, SI-SDR, ILD and this ITD measure are blind to a sign flip common to both ears; the registered waveform-error metric is not.

**DC offset** (found by Astra):
- The decoder adds a constant bias to every output sample: +0.110 (seed 17), −0.165 (seed 18), −0.146 (seed 19), against an input RMS of 0.14.
- On the low-reverb target-only panel, Gen 19's waveform error is +6.33 dB raw, −2.29 dB after sign correction, and **−18.22 dB after sign correction and bias removal**.
- Inversion alone does **not** explain the waveform error. The earlier wording is withdrawn.
- Mean-removed SI-SDR and STOI hide the offset. On real hardware it costs headroom and can cause clicks at speech-to-silence transitions.

| Gen 19 checkpoint | polarity | decoder bias |
|---|---:|---:|
| seed 17 (Hugging Face default) | −1 | +0.110101 |
| seed 18 | +1 | −0.164652 |
| seed 19 | −1 | −0.145688 |

**Other implementation notes** (Astra):
- The research runner's `undelay` pads the last 63 samples with zeros. Gen 34's scoring window includes 31 to 63 padded samples for some talkers.
- The local Hugging Face `enhance.py` averages stereo to mono and restores RMS, so it cannot speak to two-ear direction.

**Verdicts:** none change (every gate is blind to sign and DC).

**Next:** Gen 35, a registered frozen **output-path repair audit**. It compares existing / sign-corrected / sign-corrected with bias removed, and decides with Astra's engineering rule before any Hugging Face change.
- A envelope-only ACE path is plausibly unaffected by a common acoustic inversion. That is inferred from its structure; the full Nucleus 6 path is not verified.
