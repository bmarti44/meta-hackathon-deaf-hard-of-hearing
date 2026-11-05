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
file is processed and **1 s to end of file** is scored; lengths vary,
e.g. SPK1 ends at 7.65 s (Astra).

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

## Pre-launch amendment 1 (2026-11-05 ~03:50, before any model was run on the recordings)

Astra's first pre-launch review was **NOT CLEARED**, with three blocking
items ([astra-prelaunch-review.md](./astra-prelaunch-review.md)). Fixes:

1. **A2 basis.** It is replaced by documented corpus provenance.
   - The BRUDEX paper (§3) states the talkers are "two female and two male
     English speech signals … from the SQAM and VCTK corpus". The quote was
     verified from the paper PDF.
   - Neither corpus is LibriSpeech, so **recording overlap is excluded**.
   - **Speaker identity is recorded as unresolved**, because whether a talker
     is also a LibriVox reader cannot be verified. That is a limitation, not
     a pass.
   - A2 now checks `recording_overlap: false`, the cited provenance, and a
     recorded identity status. The bandwidth measurement is kept as
     supporting evidence only.
2. **Missing readouts.** These are added:
   - **mixture-ILD distortion** (output vs input mixture);
   - **gain-sensitive waveform error** per ear (10·log10 of error energy over
     reference energy) for every item, target-only included;
   - **each-ear cell summaries** (left, right and worst ear, where worst
     means the higher waveform error).
3. **Judge completeness.**
   - A7 now requires every prescribed metric (`recorded_panel.METRICS`, 9
     fields) to be present, numeric (not boolean) and finite in every row.
   - A6 handles missing systems.
   - `judge_safe` returns INVALID for any malformed or unreadable audit
     instead of raising.
   - Tested by deleting each metric in turn, replacing one with a boolean,
     removing the Gen 19 rows, and feeding unparsable JSON.

Also:
- The fetcher retries the size probe (Zenodo answered one 504).
- Parallel fetches write separate manifests, which are merged with a
  sha256 re-check.

Tests: `test_gen34.py`, 3/3 passing. The hash table is updated below.

## Pre-run amendment 2 (2026-11-05 ~03:52; the first pipeline run crashed before any model output)

- **The crash.** The first run of `pipeline.sh` (03:48) crashed while scoring the **bypass** system.
  - `bench-n6/vocoder._stft` raises when `(length − N_FFT)` is not a multiple of `HOP` (512 / 128).
  - The registered benches always used aligned lengths; BRUDEX files vary.
  - No model had been run, and no audit file was written.
- **The fix:** the scoring window is now 1 s to the **last full vocoder hop** before the end of the file (`recorded_panel.score_window`). It drops fewer than 128 samples (8 ms) at the end, and it applies to every metric.
- **What is not changed:** the shared, registered `vocoder.py` is left untouched.
- Tested for arbitrary lengths (`test_gen34.py`, 4/4).
- The hash table below is updated for `recorded_panel.py` and `test_gen34.py`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen34/fetch_brudex.py` | `470a79b497a5f08ea62d1b2339e7fa8da1a18781b96ccc3b99693ca03e9f9f4e` |
| `research/gen34/recorded_panel.py` | `6aef539828ed399f77933fc61ef6f57c54de43400bfca40a7f5a7b5b012d312d` |
| `research/gen34/run_audit.py` | `dba6cd66e416d54d46a88c6426e609a2171b2b67723e2d7a7f91f6dbb4f6d231` |
| `research/gen34/judge_recorded_v1.py` | `bfa9443b09bcf3072d3c55504a49b5319322e9220948da508e144af16c63368e` |
| `research/gen34/test_gen34.py` | `edc7d64c5df24ba0a66e9791886f861f0a7c1dbb4942735943832fa01492ba3c` |
| `research/gen34/pipeline.sh` | `9603e319f284288e75ba9e95dbd07c8392a6e93d651cf67e18c584a11c623b10` |
| `research/gen34/speaker_audit.json` | `385e466bbe2b806b8ff8135fdf18a3d834583dbe190a698fb72bd3486c90a830` |
| `research/gen33/linked.py` | `9351c9f5eaf054a4252a639fd869107d27bae9da6dab508e2965c71866ab8acd` |
| `research/gen24/train13.py` | `5ad336fc891dac7ceff79a63a78393a8d1a5166b88bee92c734f9841aafdce08` |
| `research/bench-n6/spatial.py` | `1bd0e32b073fdbf228f518269953469e7e0b5c7c0ddef4c980a5af3509a68834` |
| `research/bench-n6/vocoder.py` | `fc2cbd942dcd096cd5ff2428adbc23adb258810a4e43d9e87dbcb6334dc39fd0` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen32/weights/wiseftpd_seed20261117.pt` | `645a062323718958158f32af4398ce3759aae541168db08a3fe286dba57c90b3` |
