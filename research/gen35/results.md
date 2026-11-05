# Gen 35 — frozen output-path repair audit: INVESTIGATE (T0)

> Claude Opus 5.5, 2026-11-05 ~05:05.
> - Registration: [prereg.md](./prereg.md), with amendments 1 and 2. Astra cleared it after two NOT CLEARED reviews.
> - Rows: `repair_rows.json` (17,874 rows; 914 s). Decision: [repair_decision.json](./repair_decision.json).
> - Reviews: [Astra](./astra-review-gen35.md) and [Muse](./muse-review-gen35.md).
> - No training or selection. `promoted FALSE`. Nothing is published.

**Decision: INVESTIGATE**, by the registered rule. No threshold rescue.

| Check | Research path (A2 vs A0/A1) | Export path (E2 vs E0/E1) |
|---|---|---|
| V0 well-formed, provenance, v1 reproduced | ✓ | ✓ |
| polarity positive everywhere (R1 / E1) | ✓ | ✓ |
| waveform error below sign-only (R2 / E2) | ✓ | ✓ |
| no noisy loss (R3 / E3) | ✗ worst STOI −0.0028 | ✗ worst STOI −0.0022 |
| no cue loss (R4) | ✗ one ITD +1 sample (seed 18) | n/a (mono) |
| clip, delay, silence (R5 / E5) | ✗ clip fraction | ✗ clip fraction |

**What the repair does** (descriptive):
- Sign correction makes the output positively signed on every clip and level, in both paths.
- Removing the decoder bias then cuts the waveform error sharply. Mean target-only error on the exported path (X3):

  | seed | published | sign-only | sign + bias removed |
  |---|---|---|---|
  | 17 | +5.3 dB | −2.9 dB | **−13.3 dB** |
  | 18 | −1.2 dB | −1.2 dB | **−12.8 dB** |
  | 19 | +5.1 dB | −2.1 dB | **−14.2 dB** |

- Alignment lag is 0 everywhere. Silence and transition-tail RMS never rise.

**Where each failure comes from** (attributed by comparing arms; descriptive):
- **STOI (R3, E3):** from the **bias removal** (A2 vs A1, E2 vs E1); the sign and delay-flush differences are about 10⁻¹⁰.
  - *Corrected per Astra:* across P1, **146 item-ears decrease and 1,294 increase**, ranging from −0.0028 to **+0.0102**. Bias removal mostly *raises* STOI. The earlier "within ±0.003, a similar number higher" was wrong.
  - Demeaning both signals before STOI shrinks the worst difference to about 4×10⁻¹⁰. STOI is DC-sensitive, mostly in its lowest two bands.
  - SI-SDR, which is mean-removed, is unchanged to within 0.0003 dB.
- **ITD (R4):** one P1 scene for seed 18 (talker 1, low, +60°, −5 dB) moves from 0 to 1 sample of error. The estimated lag goes 8 → 9 against a reference of 8, as Astra verified. The cause is the **delay flush** (A1 vs A0), not sign or bias: the last 63 samples now hold real output instead of zeros, and the whole-utterance cross-correlation estimate shifts by one bin.
- **Clipping (R5, E5):** the clip fraction counts samples with |x| > 1.
  - *Research path:* removing a DC offset of ±0.11–0.16 moves the waveform relative to the fixed ±1 thresholds. Some peaks that the offset kept below 1 now cross it, and others drop below.
  - *Export path:* the published code restores the output RMS **with the DC included**, so the offset used part of the level budget and the speech came out quieter than the input. Without the offset, speech returns to the input's level, and loud inputs (input RMS 0.56) cross ±1 more often.
  - Flushing alone also raises clipping on 8 P2 rows. Export increases reach 0.93 percentage points (X2) and 3.70 (X3).
  - *Corrected per Astra:* the published writer applies `np.clip`, so these crossings become real waveform distortion. The earlier "neither shows that the speech gets worse" is withdrawn: the rows establish neither harm nor harmlessness.

**A sign-only export patch is exactly neutral:**
- On every exported panel, E1 (sign only) equals −E0 for seeds 17 and 19, and E0 itself for seed 18, which is already positive. SI-SDR, STOI, clip fraction and RMS are identical in the audited floating-point export core (max difference 0).
- Waveform error and signed projection change. This is not an end-to-end file-writing neutrality result (Astra).
- It fixes the polarity: minimum α across clips and levels goes from −0.78 / +0.52 / −0.70 to +0.63 / +0.52 / +0.58 for seeds 17 / 18 / 19.
- It leaves the DC offset in place.
- The registered candidate was E2 (sign plus bias removal), so this is a finding, not a verdict.

**Reading:**
- The repair corrects the sign, cuts waveform error sharply, and causes no delay or silence regression.
- It fails the registered STOI, ITD and clipping checks.
  - The STOI failures come from STOI's own DC sensitivity; most item-ears improve.
  - The clipping is real distortion once the file is written.
- Nothing is waived.
- A follow-up should be decided with the reviewers. Options include:
  - registering the sign-only patch, which is exactly neutral, as its own candidate;
  - pre-registering DC handling and clip criteria that measure what matters, such as peak-safe level restoration and DC-invariant intelligibility scoring.

  Either needs registration before any result.
