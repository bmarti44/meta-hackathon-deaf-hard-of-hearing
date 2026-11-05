# Gen 34 pre-registration: frozen real-recording audit, an evaluation asset (T0)

> Claude Opus 5.5, 2026-11-05 ~03:40 EST. Written before any model was run
> on the recordings.
> Source: both reviewers' Gen 33 agenda, rank 1 ("stop iterating on
> synthetic gates and build the evaluation asset first"). This is Astra's
> exact pilot, adopted in the disposition in
> [../gen33/astra-review-gen33.md](../gen33/astra-review-gen33.md).
> **No training, selection or gate change, and no model advancement.**
> `promoted FALSE`.

## The one change: an external recorded-speech evaluation panel

**Asset: BRUDEX** (Fejgin, Middelberg, Doclo, University of Oldenburg, 2023;
MIT licence; doi 10.5281/zenodo.8340195).
- It holds speech and babble, each **acoustically recorded** at binaural
  hearing-aid microphones on a KEMAR dummy head.
- One laboratory, with **three reverberation settings**: T60 ≈ 0.31 /
  0.51 / 1.3 s, DRR ≈ 3.5 / −0.5 / −4.0 dB.
- This is one physical lab, not three independent rooms (Astra).

**Subset used** (fetched by HTTP range from the Zenodo archives; zip CRC-32
checked; each file's sha256 in the fetch manifest):
- 4 talkers (SPK1–2 female, SPK3–4 male) × 3 settings × loudspeaker
  azimuth −60 / −30 / +30 / +60° (0° = front, negative = left), all from
  recording run 1 (`eMicRun_1`);
- babble recorded from four corner loudspeakers, for each setting, also
  from run 1.
- Channels: **front-left (1) and front-right (3)** hearing-aid microphones,
  per the BRUDEX README.

**Fixed grid:**
- 4 talkers × 3 settings × 4 azimuths × SNR −5 / 0 / +5 / +10 dB = **192
  noisy items**, plus **48 target-only items**.
- Every SNR is applied to every recording, which removes Gen 33's
  content/SNR confound.

**Rendering and reference:**
- Mixtures are **digital sums of the separately recorded components**, and
  are labelled as such.
- The SNR is set from summed bilateral energy over the scoring window,
  with **one noise multiplier shared by both ears**. Interaural level and
  time differences are preserved (tested).
- 48 → 16 kHz with `resample_poly(1, 3)`.
- Each stereo input is scaled by one shared gain to RMS 0.14 (the
  published `enhance.py` convention).
- **Reference for each ear = that ear's recorded isolated talker.** This
  tests noise removal and speech preservation, not dereverberation.

**Deviation from Astra's text (stated before running):** she specified
"process the first 11 seconds and score seconds 1–11". BRUDEX's short
files are ≤ 10 s; full-length files are in a 59 GB archive. So the whole
10 s file is processed and seconds 1–10 are scored.

**Systems:**
- bypass;
- **Gen 19 seed 17**, independent per ear (`80000b64…`);
- **Gen 32 α = 0.7**, independent per ear (`645a0623…`).

Both models are frozen. Gen 19 is run twice for the duplicate-baseline
check.

**Readouts (descriptive only):** for every setting × SNR cell, against
bypass and against Gen 19:
- each-ear SI-SDR and STOI (the established mean-removed SI-SDR);
- worst-ear differences;
- target-only SI-SDR and STOI;
- both current ILD diagnostics.

## Decision: `judge_recorded_v1.py` returns VALID ASSET or INVALID

All checks must pass. **Model scores cannot determine whether the asset is
accepted.**
- **A1, provenance:** every needed file is present, and its sha256 matches
  the fetch manifest; the source DOI is recorded; the licence on disk is MIT.
- **A2, speaker-overlap audit** (`speaker_audit.json`):
  - The clean talkers are 48 kHz recordings with energy in 8.2–12 kHz at
    −0.7 to −10.7 dB re 4–7.8 kHz.
  - Every model here was trained or tuned only on 16 kHz LibriSpeech, so
    none of the four talkers is LibriSpeech audio.
  - Limitation: whether a talker is the same person as some LibriVox
    reader is unknowable here.
- **A3, complete grid:** exactly 240 unique items per system, with
  registered metadata.
- **A4, channel/delay:** for all 16 target-only items in the 'low' setting,
  the left/right level difference and the cross-correlation lag of the
  recorded reference point to the loudspeaker's side.
- **A5, bypass identity:** every bypass output equals its input exactly.
- **A6, duplicate baseline:** two independent Gen 19 runs give identical
  rows.
- **A7:** every metric is finite, the checkpoint hashes are the registered
  Gen 19 and Gen 32 files, and the material hash reproduces on rebuild.

**After this:** once inspected, these recordings become development
material. A later confirmation must use different voices and physical
rooms (Astra).

**Tests:** `test_gen34.py`, 2/2 passing. They cover:
- the mixing math (SNR, one shared noise multiplier, one shared input gain,
  target-only identity);
- the judge's grid, duplicate-row, bypass, duplicate-baseline and
  checkpoint checks.

Run: `research/gen34/pipeline.sh` (after the fetch completes).

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen34/fetch_brudex.py` | `859c9e118fdf4c68d4c7ed5122b71c78d70ee3033713653e491511b6021c3af5` |
| `research/gen34/recorded_panel.py` | `d36b5a5a7f2933bc62968e84857bc703b0bc72dd2ee8a13d471b256615447167` |
| `research/gen34/run_audit.py` | `94c5376f6817a6de9f187713ba22b2d9ff65c20aa78eb005a24567a976ba910f` |
| `research/gen34/judge_recorded_v1.py` | `7ec28c2c9ab696e0a1aa44ff3bfb85e2281f335d967b3f8106dfc20a0278e55e` |
| `research/gen34/test_gen34.py` | `2d3eb1c6ef5de78896fa82065185ce61c22eef71a847c1d53042a60b2ea876a9` |
| `research/gen34/pipeline.sh` | `9603e319f284288e75ba9e95dbd07c8392a6e93d651cf67e18c584a11c623b10` |
| `research/gen34/speaker_audit.json` | `90f9ecaabe48251afdb4d83940ffc62f777287a6f234422468d2088b788e3a7e` |
| `research/gen33/linked.py` | `9351c9f5eaf054a4252a639fd869107d27bae9da6dab508e2965c71866ab8acd` |
| `research/gen24/train13.py` | `5ad336fc891dac7ceff79a63a78393a8d1a5166b88bee92c734f9841aafdce08` |
| `research/bench-n6/spatial.py` | `1bd0e32b073fdbf228f518269953469e7e0b5c7c0ddef4c980a5af3509a68834` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen32/weights/wiseftpd_seed20261117.pt` | `645a062323718958158f32af4398ce3759aae541168db08a3fe286dba57c90b3` |
