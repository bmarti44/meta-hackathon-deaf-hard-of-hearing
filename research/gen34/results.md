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
- STOI is higher in **15 of 15** cells (+0.001 to +0.009).
- SI-SDR is higher in 11 of 15 cells.
- Target-only SI-SDR is +0.8 to +1.0 dB higher.
- Worst-ear differences stay within about 0.1 dB in noisy cells.

**Reading** (one lab, 4 talkers, development material; descriptive only):
- **In crowds, on real recordings, Gen 19 helps.**
  - It helps most at −5 / 0 dB in the least reverberant setting.
  - The help shrinks as reverberation grows.
- **It costs in quiet, echoey conditions.**
  - At +10 dB in the 1.3 s setting it lowers SI-SDR (−2.0 dB) and STOI (−0.034).
  - It also lowers STOI on clean reverberant speech by 0.03 to 0.06.
  - This is the same problem the room line set out to fix.
- **Gen 32, the room-trained candidate that failed its synthetic screen, is slightly better than Gen 19 on these real recordings.**
  - The edge is in every cell for STOI, and in clean reverberant speech.
  - The differences are small and from one seed, so they are not evidence of a listener benefit.
  - It is still the first real-recording sign that the room work moves in the intended direction.

## A deployment defect the audit found: output polarity

The audit's gain-sensitive waveform error was about +6 dB for both models
even where SI-SDR improved. The cause is that the model outputs an
**inverted** waveform:
- The projection of the output onto the reference is α ≈ −0.92, at zero lag.
- SI-SDR, the training loss, is sign-invariant, so training never fixed the sign.
- STOI and the ILD measures are sign-invariant too, so no registered gate could see it.

The sign is set early in training and differs by seed (LibriSpeech dev-clean
check, every committed checkpoint):

| Checkpoint | α (output vs clean, target-only) |
|---|---|
| Gen 19 seed 17 (default Hugging Face `model.safetensors`) | **−0.95** |
| Gen 19 seed 18 | +0.98 |
| Gen 19 seed 19 | **−1.02** |
| Gen 31 fine-tune / Gen 32 candidate (seed 17) | −0.91 / −0.94 |

**What it changes:**
- **Verdicts:** none (all gates are sign-invariant).
- **Envelope-based CI coding (ACE):** probably no effect.
- **Where it can matter:**
  - mixing the output with natural sound (hearing aids, residual acoustic hearing, electro-acoustic stimulation);
  - running different seeds in the two ears, which would put the ears out of phase.
- **The fix is free:** multiply the output by the checkpoint's sign. That leaves every registered metric unchanged.
- **Recommended:** a per-checkpoint `polarity` in the published `config.json`, applied in `enhance.py`. The Hugging Face repo is not changed without the owner's go-ahead.
