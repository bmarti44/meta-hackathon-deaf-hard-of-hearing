# Gen 31 pre-registration: fine-tune Gen 19 on rooms, then blend back (WiSE-FT) (T0)

> Claude Opus 5.5, 2026-11-05 ~01:25 EST. Written before any Gen 31
> fine-tune, blend or validation run on a real candidate.
> Source: Muse's Gen 29 review, choice (c), adopted in the disposition in
> [../gen29/astra-review-gen29.md](../gen29/astra-review-gen29.md).
> **Runs only if Gen 30 fails**, which ends the dose-only campaign
> (Gen 30 registration). If Gen 30 ADVANCEs, Gen 31 is deferred.
> T0 only. `promoted FALSE`. Requires Astra's pre-launch clearance.

## Question

Gen 27–29 trained from scratch with rooms. Each kept a room gain, and each
lost a little on speech with no room echo (dry). Can a short room
fine-tune of Gen 19, blended back toward Gen 19 in weight space, keep a
room gain with **no** dry loss?

WiSE-FT (Wortsman et al., 2022, arXiv 2109.01903) reports that such blends
can keep much of a fine-tune's gain on the new conditions while keeping
the original's performance. Astra's caution is recorded: that evidence is
from vision models, not CI enhancement, and it guarantees nothing. Here,
preservation is measured.

## The one change: the method (three steps, no other free choices)

**Step 1, fine-tune** (`research/gen31/train18.py --mode finetune`):
- Start from the registered Gen 19 seed-17 final
  (`80000b64…f367`; the trainer refuses any other parent).
- Continue Gen 19's own main data stream from its committed 24k RNG
  handoff, `research/gen21/weights/rng_handoff_seed20261117.pt`. The
  fine-tune therefore sees batches Gen 19 never saw.
- Room mix **aug50** (Gen 27's: 45 / 45 / 10).
  - Muse's sketch named the aug125 mix. aug50 is used because the blend
    step can only give back part of the fine-tune's room gain.
  - The strongest registered room exposure is expected to give the blend
    the most to keep, and the dry loss it brings is what the blend is
    chosen to remove.
  - This is a fixed hypothesis, not a guarantee (Astra): neither stronger
    augmentation nor a larger α is certain to give more room benefit.
- **8,000 updates**, a fresh Adam at lr 1e-4 with cosine decay to 1e-5,
  final checkpoint only. Everything else is as in Gen 27–30:
  - batch 8 × 2 s, SI-SDR loss, clipping 5;
  - speakers, SNR and noise recipe;
  - the corrected RIR manifest `f306700d…` and its train split;
  - per-talker RIRs, the direct-plus-50 ms target and taper,
    augmentation RNG `[seed, 27]`.

**Step 2, blend** (`research/gen31/blend.py`):
- θ(α) = (1 − α)·θ_Gen19 + α·θ_FT for every tensor (all 181 are float32
  parameters; the model has no buffers).
- Grid α ∈ {0.1, 0.2, …, 1.0}. α = 0 is Gen 19 bit-for-bit and α = 1 is
  the fine-tune bit-for-bit (tested).

**Step 3, choose α on fresh voices, never on screen material**
(`research/gen31/val_testclean.py`):
- **VAL panel:** LibriSpeech **test-clean**, never used in this repo
  before. Archive md5 `32fa31d27d2e1cad72775fee3f4849a9` (matches
  OpenSLR), sha256 `39fde525e59672dc6d1551919b1478f724438a95aa55f874b576be21967e6c23`.
  - 16 targets: the 8 lowest-numbered female and 8 lowest-numbered male
    speakers.
  - The other 24 test-clean speakers are **reserved**, untouched, for a
    later fresh confirmation.
  - Built exactly like screen v2: 4 × 4 s crops × 4 crowds (k ~ U{8..12}
    from the other 15 VAL voices) × {−5, 0} dB = 512 dry items. Seed
    20261131. Material sha256
    `c2c4f89a59533601dc0a3f2b219fb6b65fe9a4d468349cd5a442709c9873b638`.
  - The script asserts that every VAL and reserved voice is disjoint from
    every earlier speaker list (Gen 13–19 training, TEST, TEST_BABBLE,
    VAL, VAL interferers, screen-v2 targets and reserved,
    train-clean-100).
- **Rule:**
  - For each α, d = the mean over items of (blend − Gen 19), paired per
    item, for SI-SDR and STOI at −5 and at 0 dB.
  - pass(α) means all four d ≥ 0 (NaN fails).
  - **α\* = the largest grid α such that every grid α′ ≤ α passes.** A
    later pass cannot rescue an earlier failure.
  - If α = 0.1 fails: **NO CANDIDATE.** Gen 31 is filed as FAIL and no
    screen material is touched.
- The chosen blend is copied byte-for-byte to
  `weights/wiseft_seed20261117.pt`. Nothing else is selected:
  - no other α is judged;
  - the fine-tune endpoint is not screened separately;
  - no step or checkpoint selection.

**Mechanics smoke (stand-in fine-tune, not a result):** Gen 19 plus
N(0, 1e-3) noise.
- It ran end to end in 92 s, and the rule gave NO CANDIDATE.
  - SI-SDR changes ran from about −0.0001 dB at α = 0.1 (−0.000112 /
    −0.000032 dB at −5 / 0 dB) to about −0.002 dB at α = 1.
  - Corrected per Astra; the earlier text said −0.002 dB at every α.
- This shows the rule is strict. Like D, it treats any measurable dry loss
  as a failure.
- The smoke used no room-trained weights, so it reveals nothing about the
  hypothesis. Its outputs stayed in the session scratchpad.

**Tests:** `test_gen31.py`, 5/5 passing.
- Blend endpoints are bit-exact and the midpoint is exact.
- The prefix rule holds, including NaN and the both-SNR / both-metric
  cases.
- VAL voices are disjoint from earlier lists.
- train18 scratch batches are bit-identical to Gen 30's train17.
- The fine-tune refuses a wrong parent, a missing handoff and a mode
  change on resume. Its CPU smoke starts from Gen 19's trained weights
  (first loss < −3 dB, drift < 0.01) and records parent sha, handoff,
  lr and lifetime steps.

## Judgment (unchanged)

- Gen 27's `judge_v3.py` (cleared at 2b548df), against **same-seed
  Gen 19**, on the same registered materials, applied **once**, to the
  α\* blend.
- ADVANCE needs R1a ≥ +0.30 dB, R1b CI lo > 0, R1c ≥ 10/16, and C, T,
  D, S2, S3, SP all true. No tolerance; D needs non-negative means and
  lower bounds > −0.15 dB / > −0.003 at both SNRs.
- Reported descriptively:
  - the full VAL curve (all 10 α);
  - the fine-tune's train log;
  - Gen 31 vs Gen 29 on the primary and dry scores.
- ADVANCE authorizes seeds 18/19. Each repeats all three steps with the
  same rule (its own fine-tune and its own α\*). After that comes a fresh
  confirmation on the reserved voices.

**Expectation, stated in advance:**
- NO CANDIDATE is a real possibility: the rule needs the blend to be at
  least as good as Gen 19 on dry speech from new voices.
- If a candidate exists, R1a ≥ +0.30 is uncertain, because blending
  shrinks the room gain.

Run: `research/gen31/pipeline.sh` (fine-tune ~13 min; blends and VAL
~3 min; screen ~5 min).

## Pre-launch amendment (2026-11-05 ~01:35, before any run)

From Astra's pre-launch review
([astra-prelaunch-review.md](./astra-prelaunch-review.md)), which
CLEARED Gen 31 with no blocking items. Muse also CLEARED it
([muse-prelaunch-review.md](./muse-prelaunch-review.md)).

1. `pipeline.sh` now refuses to run unless `research/gen30/screen_s17.json`
   says `"verdict": "FAIL"`.
2. The aug50 rationale is softened, and the smoke description is
   corrected (above).
3. Before any seed-18/19 replication, the Gen 19 seed-18/19 parent hashes
   must be added to `GEN19_SHA`; the trainer currently permits only
   seed 17.
4. No tolerance and no finer-grid rescue will follow a failure.

The hash table below is updated for `pipeline.sh` only; every other
hash is unchanged.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen31/train18.py` | `c214820a08fa24cc9b94af7752e513b114b51f114fe425fa7a9127a67c717963` |
| `research/gen31/blend.py` | `652206ffed4ae4bd8138ef34a3756b57c55e7027f23d79da81dbd5c6d23654e1` |
| `research/gen31/val_testclean.py` | `349e6a0f7a17f4d59374f96e418ca1d76fd9e482cbb0cef416f2170e4f92a776` |
| `research/gen31/test_gen31.py` | `41a55ff0267aa61ed700d2a41079b59b026f6828476c648e697c68f5a02a806b` |
| `research/gen31/pipeline.sh` | `2d4bf71c6f00cf0d6f17d8b79f848f32b67fd92fcef2ea926959450591be5dc2` |
| `research/gen30/train17.py` | `3966507a07ec470d505668a5575ff05efb278bd75f79cd079d9e9d6e96eacbfa` |
| `research/gen27/train14.py` | `9d39741c2e63aaa7773bd6e88165676a33ff207c034b215664a805b5c01567e7` |
| `research/gen27/rirbank.py` | `14376aafb87c73eaed6482d07b3958834b86b51b96100b7698d8e7ea7cc0e7f1` |
| `research/gen27/rir_manifest.json` | `f306700d0dce5aded749a5f48e6da6d6bc66a6bdce3d0e27677081a41b7c1711` |
| `research/gen27/panel_rev.py` | `875cd1eed0b869f0fee4631d9adcf0e91e0b90e25e88769a3718cdcd07efebf6` |
| `research/gen27/judge_v3.py` | `faa38995052d38de526fbc868baed6dab577bc0598c1c045dcb956023ba4beb7` |
| `research/gen27/registered_hashes.json` | `49fb96fd28ca1b4545fca5e2b8fda24390c914a7f1e818e5a56773f58a97b7d4` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen21/weights/rng_handoff_seed20261117.pt` | `23277723b3c4f3187a0a1fd8e33c9281a09895308aa146bd4df0ee427bc36c3d` |
