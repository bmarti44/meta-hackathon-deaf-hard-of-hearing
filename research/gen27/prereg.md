# Gen 27 — room augmentation (REGISTERED 2026-11-04 ~21:55 EST, before any candidate; Astra pre-launch review pending)

> Built by Claude Opus 5.5, 2026-11-04 ~21:10–22:00 EST, to Astra's agenda
> review (`astra-agenda-review.md`, "My concrete Gen27 specification").
> Finalised by Claude Opus 5.5 for review. Nothing has been
> trained. No candidate has been evaluated on any Gen 27 material.
>
> - **Unchanged:** Gen 19's original 13/14 scorecard, the screen-v2 dry
>   panel and its rules, Gen 24's registration and run.
> - **No listener-benefit claim** follows from any result here. All results
>   are acoustic/proxy (in-silico) findings.

## 1. One intervention

| Item | Value |
|---|---|
| Trainer | `research/gen27/train14.py` = `research/gen24/train13.py` (`--loss sisdr --snr legacy`, the Gen 19 recipe) plus `--room aug50` |
| Command (not launched) | `/tmp/gen9env/bin/python research/gen27/train14.py --loss sisdr --snr legacy --room aug50 --mode scratch --seed 20261117` |
| Seed / steps | 20261117, from scratch, 24,000 updates |
| Control | Gen 19 seed-17 final, `research/gen19/weights/causal_seed20261117.pt`, sha256 `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| Frozen | architecture (gen15 `model_causal.py`), SI-SDR loss, Adam 1e-3 cosine to 1e-4, grad-clip 5, batch 8 × 2 s, 251 train-clean-100 speakers, legacy SNR (60% U(−5,5) + 40% U(−5,10)), 70% babble k~U{2..12} / 30% SSN, 10% quiet |
| Not included | Gen 24's SNR change |

## 2. Training mixture (`--room aug50`)

- **Shares:** 45% dry noisy, 45% reverberant noisy, 10% dry quiet. Quiet
  stays dry. Each noisy example is reverberant when `u < 0.5`.
- **Paired draws:** the main RNG (`default_rng(seed)`) makes exactly the
  Gen 19 draws in Gen 19 order. Every augmentation draw comes from a
  separate RNG, `default_rng([seed, 27])`:
  - `u` for every example;
  - stratum ~ U{short, medium, long}, then a room ~ U(the stratum's train rooms);
  - target position ~ U(the room's RIRs);
  - one position per interferer source ~ U(the other positions), with
    replacement;
  - the SSN history noise.
- **Rendering:** each source is convolved with its own RIR before
  summation:
  - each babble talker is its own source; SSN is one point source;
  - the 1 s of audio before each crop, from the same file and at the same
    gain, gives real convolution history;
  - SSN history is new noise from the aug RNG with the same filters; the
    SSN segment itself is the Gen 19 draw.
- **Reference:**
  - reverberant examples: the target convolved with the direct path plus
    reflections through 50 ms after direct arrival, with a half-cosine
    taper over the final 5 ms;
  - direct arrival = argmax |h|;
  - dry examples keep the original clean target.
  - The 50 ms cutoff is an engineering choice, not an established CI optimum.
- **SNR:** the Gen 19 SNR draw, defined as full reverberant target energy
  vs summed reverberant interferer energy. DRR/C50 are reported per RIR
  (manifest) and as running means in the training log.
- **Alignment and gain:** fixed model delay (`delay_target`, 63 samples).
  - No per-output alignment and no independent reference normalisation.
  - Reference and mixture share the same scaled RIR. The single
    per-room gain is fixed in the manifest.
- **Logging and checkpoints:**
  - room-metadata counts (condition, stratum, rooms used, mean target
    DRR/C50) are logged every 25 steps and in the final log;
  - checkpoints record `room_mode` and the RIR manifest sha256;
  - resume identity includes `--room` and the manifest sha256.

## 3. RIR bank (`build_rir_bank.py` → `rir_manifest.json`)

- **Source:** OpenSLR 28, <https://www.openslr.org/resources/28/rirs_noises.zip>,
  Apache 2.0.
  - md5 `e6f48e257286e05de56413b4779d8ffb` (matches the published checksum.md5)
  - sha256 `3b50cfde915b3984738169b4beb341e9f6b8062ae4c2076146c5db71c2c05dc7`
  - 1,311,166,223 bytes
  - The audio is kept under `/tmp/rirs/` (outside git). The manifest pins
    every file's sha256.
- **Manifest sha256:** `0bc488e1ccbe8e90b23b070ca05eec269981671ad83bc64f31d7672daade272b`.
- **Simulated set:** image method, one receiver and 100 source positions
  per room, source–receiver distance ≤ 5 m.
  - Room RT60 = median Schroeder RT60 (T20, fallback T10) over the first 8
    RIRs.
  - Strata: short [0.2, 0.4), medium [0.4, 0.6), long [0.6, 0.8] s.
  - Eligible rooms: short 105, medium 21, long 56 (of 600).
- **Split by room, RNG seed 20261127:**

| Split | Stratum | Rooms | RIRs | Room RT60 min / median / max (s) | median DRR / C50 (dB) |
|---|---|---|---|---|---|
| train | short | 19 | 304 | 0.202 / 0.265 / 0.396 | −1.9 / 12.7 |
| train | medium | 19 | 304 | 0.417 / 0.509 / 0.591 | 3.5 / 14.8 |
| train | long | 19 | 304 | 0.623 / 0.728 / 0.797 | 2.1 / 12.1 |
| eval_synth | short | 2 (smallroom-Room034, mediumroom-Room007) | 32 | 0.307 / 0.346 / 0.384 | 1.9 / 14.1 |
| eval_synth | medium | 2 (mediumroom-Room038, -Room192) | 32 | 0.508 / 0.529 / 0.549 | −0.7 / 9.8 |
| eval_synth | long | 2 (mediumroom-Room123, -Room046) | 32 | 0.671 / 0.727 / 0.783 | 0.9 / 13.5 |
| eval_measured | short | 2 (RWCP_cirline_e2a, air_binaural_meeting_0) | 13 | 0.256 / 0.298 / 0.339 | 7.1 / 19.9 |
| eval_measured | medium | 2 (RWCP_cirline_jr1, RWCP_cirline_jr2) | 15 | 0.490 / 0.544 / 0.598 | −0.5 / 7.8 |
| eval_measured | long | 2 (RWCP_cirline_ofc, RVB2014_largeroom1) | 12 | 0.654 / 0.720 / 0.785 | −1.1 / 6.4 |

- **Room and position counts:**
  - Training uses 19 rooms per stratum. That number is set by the medium
    stratum (21 eligible − 2 held out).
  - Each simulated room keeps 16 source positions; each measured room up
    to 8.
- **Measured rooms:** evaluation only, one microphone channel each.
  Excluded: REVERB's simulated rooms, anechoic RWCP rooms, AIR phone
  mock-ups and single-position entries.
- **Preprocessing (identical in training and evaluation):**
  - channel 0;
  - truncate to 1.0 s with a 10 ms fade;
  - one gain per room, so the room's mean RIR energy = 1.
- **Known confound:** RT60 is correlated with room-size family. Short is
  18/19 smallroom; medium and long are all mediumroom (large simulated
  rooms are almost all > 0.8 s). Results by stratum therefore also differ
  in geometry.

## 4. Reverberant screen (`panel_rev.py`)

- **Draws:** screen-v2's draws (seed 20261204, 16 voices × 4 crops × 4
  crowds of 8–12 talkers), replayed with the same RNG calls but with
  individual crowd stems and 1 s history.
  - Replay check: summing the stems reproduces the registered dry
    material `557ad44f…` bit-for-bit; otherwise the build stops.
- **Strata:**
  - **synthetic (primary):** × 6 held-out simulated rooms × {−5, 0} dB = 3,072 items;
  - **measured:** × 6 measured rooms × {−5, 0} dB = 3,072 items, never
    pooled into the primary;
  - **target-only:** each crop alone through each of the 12 rooms = 768
    items.
- **Positions:** drawn from `default_rng([20261127, room_idx, voice_idx,
  crop, crowd])` and shared by both SNRs. Each crowd talker gets its own
  RIR in the same room. Reference = direct + 50 ms.
- **Metrics:** SI-SDR and STOI vs that reference on [256:−256], with fixed
  `undelay`. They are paired with the unprocessed mixture.
- **Material sha256:** `ed98320cf9f9f175be5bdc48eb52a786ff30975957e24238230a342be74f78ab` (6,912 items). The registered
  hashes are written to `registered_hashes.json` by `judge_v3.py
  --register`; `judge_v3` refuses to judge without them.

## 5. Gates (`judge_v3.py`), per seed, candidate − same-seed Gen 19 final

All gates must pass to ADVANCE. Provenance or completeness failures give
INVALID, never ADVANCE.

| Gate | Rule |
|---|---|
| R1a | Reverberant primary (synthetic stratum) mean SI-SDR gain ≥ +0.30 dB, equal weight per (voice, room) cell; the balanced grid also weights SNRs equally |
| R1b | Paired 95% bootstrap lower bound > 0, resampling the 16 voices and the 6 rooms independently with replacement (10,000 draws, seed 20261204) |
| R1c | ≥ 10/16 voice means > 0 |
| C | Mean SI-SDR gain ≥ 0 and mean STOI gain ≥ 0 in each (synthetic, measured) × (−5, 0 dB) cell |
| D | Dry screen-v2 panel: at −5 and at 0 dB, mean SI-SDR and STOI gains ≥ 0, and voice-bootstrap lower bounds > −0.15 dB and > −0.003. An inconclusive bound fails |
| S2 | Bench v2 quiet absolute SI-SDR ≥ 25 dB and ΔSTOI ≥ −0.02 (judge_v2) |
| S3 | Bench v2 crowd ≥ 3.0 dB / 0.03 / 0.05, each CI lo > 0; SSN ≥ 3.0; white ≥ 0 (judge_v2, NaN-safe) |
| SP | See the spatial rule below |
| Provenance | Registered rev-material, manifest and dry-material hashes. The control sha is Gen 19's same-seed hash; the candidate sha matches across the rev panel, the dry panel, the bench and the spatial bench. Grids are complete and duplicate-free, and every metric is finite |

**SP (spatial):**
- The existing gates must pass: candidate target-ILD error < unprocessed,
  and ITD error ≤ unprocessed.
- There must be no mean worsening vs Gen 19 in target-ILD error or in ITD
  error, separately:
  - at hard SNR (the −5 dB scenes);
  - for left-target and for right-target mirrored scenes.
- These comparisons use the crossed spatial scenes described below.

**Reported, not gating:**
- dry bench by kind × SNR, including the −5 dB row;
- per-voice and per-room primary gains;
- target-only SI-SDR/STOI gains;
- the screen-v2 A1–A4 numbers.

**Open for review:** whether a target-only gate (e.g. no worsening in
target-only SI-SDR) should be added. Astra listed "reverberant target-only
checks" as material but gave no rule.

**Replication (`--replicate`):** a screen pass authorises seeds 18/19 only.
The candidate is retained only if all of these hold:
- the three-seed mean primary gain is ≥ +0.30 dB;
- the gain is > 0 in ≥ 2/3 seeds;
- the two-way clustered lower bound of the three-seed cell means is > 0;
- C/D/S2/S3/SP pass in every seed.

Fresh-material confirmation follows: the screen-v2 reserve is replaced per
the 2026-11-04 correction.

These are engineering advancement thresholds, not clinically meaningful
differences or proof of universal no-harm.

## 6. Spatial safeguard: what the existing bench supports

- **What the existing bench does:** `spatial_bench.py` renders 4 scenes,
  one per babble crop.
  - The crop SNRs are −5/0/5/10 dB.
  - The target is at −60/−30/+30/+60°, with the crowd at the mirror
    azimuth.
  - It has **no mirrored pair at the same SNR**, and only one −5 dB scene.
- **What judge_v3 does:**
  - It runs the existing bench unchanged, for the existing gates.
  - It also renders the closest faithful extension with the same crops and
    head model (`spatial.render_at`): all 4 crops × all 4 target azimuths,
    with the crowd at the mirror. That is 16 scenes.
  - From these it takes the hard-SNR subset (4 scenes, two mirrored pairs)
    and the left/right mirrored subsets (8 scenes each).
- **Caveats:**
  - The head model is ASSUMED, the processing is independent mono per ear,
    and the scenes are dry.
  - It cannot show localisation benefit.
- **Finding from the self-test: the mirrored check is degenerate for
  current systems.** spatial.py's head model is left/right symmetric, and
  every current system processes each ear independently with the same mono
  network.
  - So a −az scene is the exact channel swap of its +az mirror, and the
    left and right subsets give identical errors (self-test: 5.4266 dB /
    3.0 samples on both sides).
  - The mirrored gate becomes informative only with an asymmetric (e.g.
    measured) head response or a binaural/linked system.
  - The hard-SNR gate is informative.
  - Proposal for review: also cross the spatial scenes with the held-out
    rooms. That is not implemented; spatial_bench has no room option.

## 7. Timing

- **Recorded baseline:** Gen 19 seed 17 took 84.8 min for 24k steps on MPS
  (5,088.8 s, i.e. 0.212 s/step, data prep included).
- **Measured augmentation overhead (data only, CPU):** +0.039 s/step
  warm and +0.057 s/step on the first pass.
  - Setup: `make_batch` on the real LibriSpeech pool and the real
    912-RIR bank, 150 batches per pass, run as dry, aug50, dry, aug50.
  - Dry 0.359 / 0.335 s/batch; aug50 0.415 / 0.374 s/batch.
  - The machine was heavily loaded (load average ≈ 34 on 18 cores; Gen 24
    was training). Dry data prep alone measured more than Gen 19's whole
    0.212 s step, so these numbers are inflated.
- **CPU training smoke:** 200 aug50 steps on CPU, contended, completed
  without error.
  - 5.95 s/step wall, of which 0.274 s/step was data prep. RIR cache 1.14 s.
  - Loss (−SI-SDR) went from 6.22 to −2.24 dB (first-5 / last-5 logged means).
  - Shares over 1,600 examples: 46.8% reverberant noisy, 44.9% dry noisy,
    8.3% dry quiet. The quiet share is the Gen 19 main-RNG draw,
    unchanged.
  - Reverberant examples by stratum 254 / 235 / 260; 57 / 57 rooms used.
    Mean target DRR 1.25 dB, C50 13.05 dB.
  - CPU s/step is not the MPS projection basis.
- **Projection:** 84.8 min + 24,000 × (0.039–0.057 s) ≈ **101–108 min on
  MPS** (an upper bound from contended measurements). A 1.5–2 h run is
  plausible, not established.
  - Confirm with a ≤ 60 s MPS timing once Gen 24 has released the GPU,
    before launch. No MPS timing was taken now, because Gen 24 holds the
    GPU and a contended number would mislead.
- **Data and cache facts:**
  - the RIR FFT cache (912 RIRs × 2, complex64, nfft 48000) loads in about 1.1 s;
  - about 350 MB resident.
- **Plan:**
  - Evaluation is budgeted separately: the reverberant panel is 6,912
    items per system, run on CPU with worker processes.
  - Do not compete with Gen 24 for MPS. Launch only after Gen 24 finishes.

**Never substitute an interim checkpoint because time expires.** Only the
24,000-step final is judged. If the run cannot finish, the result is
"not run", never a verdict on an interim checkpoint.

## 8. Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen27/astra-agenda-review.md` | `206d7d8c643e7574a9b43212e05d665823b6cbfba3ceadf171a66c23b52fb765` |
| `research/gen24/train13.py` | `5ad336fc891dac7ceff79a63a78393a8d1a5166b88bee92c734f9841aafdce08` |
| `research/gen19/train8.py` | `030281121e487dd599e4fcd93cd14a49e33c332b801c399f8cffbeb75a50e32a` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/screen_v2/judge_v2.py` | `6cf6032ec4c1d84a0dc45d80e3d146c2eb8d7b8e32ea430a3619546dc08c778b` |
| `research/bench-n6/spatial_bench.py` | `9b5c89ed1d9e32e597dd67ed6cce58f727abf73ffe0c15c58342c12b7dfbb4f2` |
| `research/bench-n6/spatial.py` | `1bd0e32b073fdbf228f518269953469e7e0b5c7c0ddef4c980a5af3509a68834` |
| `research/bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| Gen 19 s17 / s18 / s19 finals | `80000b64…f367` / `ef098dfd…0916` / `89837737…b6326` |
| `research/gen27/rirbank.py` | `46f72de208c89f1b1dbdcef4d3696161d617d24d5f8577875b2643468653dffc` |
| `research/gen27/build_rir_bank.py` | `e46199fbc134edf2d1b4c416074dac4887dac211787a821b3611b3e21e7dade6` |
| `research/gen27/rir_manifest.json` | `0bc488e1ccbe8e90b23b070ca05eec269981671ad83bc64f31d7672daade272b` |
| `research/gen27/train14.py` | `9d39741c2e63aaa7773bd6e88165676a33ff207c034b215664a805b5c01567e7` |
| `research/gen27/panel_rev.py` | `875cd1eed0b869f0fee4631d9adcf0e91e0b90e25e88769a3718cdcd07efebf6` |
| `research/gen27/judge_v3.py` | `415274918b7602197993747ea29f5680ff38d5729c27e0f35e1fc05443d3bc5f` |
| `research/gen27/registered_hashes.json` | `6d8dba0f8802711b5f1f04e0b38de0981a289c943a187b293f29d04ba5ed1ba1` |
| `research/gen27/test_train14.py` | `96bf159838d810046f63bddeb67774b2ee0421b0c131a02cf2d477854deec3d0` |
| `research/gen27/test_judge_v3.py` | `55d25585434727214c33639ec361a0f755223260dae269effd188964112660f4` |

Re-hashed at finalisation (2026-11-04 ~21:55). Any change to these before the judge runs invalidates the screen.

## 9. Tests and self-test (at drafting time)

**Self-test** (`selftest/judge_v3_selftest_s17.json`): Gen 19 s17 judged
against itself.

- **Reverberant panel:** built in 501 s on CPU (6 workers). Stem replay ==
  `557ad44f…`. Material sha256 `ed98320c…78ab`, 6,912 items.
- **Result:** primary gain +0.0000 dB, CI [0, 0], 0/16 voices. All
  consistency, dry, S2, S3 and spatial checks pass at zero difference.
  Verdict **FAIL**, on exactly R1a/R1b/R1c.
- **Descriptive Gen 19 control numbers** (from the self-test; no candidate
  has been evaluated), as ΔSI-SDR / ΔSTOI vs mixture, measured against the
  direct + 50 ms reference:

| Stratum | −5 dB | 0 dB |
|---|---|---|
| synthetic | +0.37 dB / −0.029 | +2.22 dB / −0.005 |
| measured | +0.73 dB / −0.017 | +2.04 dB / −0.009 |

  - Target-only: −1.65 dB / −0.064 (absolute SI-SDR 7.44 dB).

**Tests:** `pytest research/gen27/test_train14.py research/gen27/test_judge_v3.py
research/gen24/test_train13.py` → **27 passed** (8 min 14 s, CPU).
- test_train14 (10):
  - dry = Gen 19 stream;
  - stems sum = babble;
  - aug50 paired draws and dry examples identical;
  - 45/45/10 shares and balanced strata;
  - 50 ms window with 5 ms taper;
  - SNR definition and per-source RIRs from one room;
  - independent direct-convolution rebuild of the reference, noise and mix;
  - manifest room split;
  - a 6-step dry run gives the same weights and logs as train13;
  - aug50 resume is bit-identical, and resume across a room-mode change is
    refused.
- test_judge_v3 (13): synthetic gate cases, INVALID cases, and the
  self-test integration.
