# Gen 32 pre-registration: room fine-tune that keeps Gen 19's dry output, then blend back (T0)

> Claude Opus 5.5, 2026-11-05 ~02:30 EST. Written before any Gen 32
> fine-tune.
> Source: Astra's Gen 30 review (rank 1) and Gen 31 review (choice a),
> adopted in the disposition in
> [../gen31/astra-review-gen31.md](../gen31/astra-review-gen31.md).
> **Runs only if Gen 31 selected no candidate** (it did; the pipeline
> checks). T0 only. `promoted FALSE`. Requires Astra's pre-launch clearance.

## Question

Gen 31's room fine-tune changed Gen 19's output on speech with no room
echo (dry). Every blend failed the zero-loss dry rule, the first one by
−0.00003 STOI. If the fine-tune is also asked to keep Gen 19's output on
dry items, can a blend pass the dry rule while keeping a room gain?

## The one change (vs Gen 31): a dry-output-preservation term in the fine-tune

`research/gen32/train19.py --preserve-dry 100` adds to the loss:

  100 · mean over dry items i (dry noisy and dry quiet) of
  mean_t((f_θ(x_i) − f_19(x_i))²) / (mean_t(f_19(x_i)²) + 1e−8)

- f_19 is a frozen, detached copy of the registered Gen 19 seed-17 parent.
- Outputs are raw and identically delayed, with no gain fitting.
- The term is zero for a batch with no dry items.
- The SI-SDR loss still applies to every item.

This is an output-preservation idea related to Learning without Forgetting
(Li & Hoiem, arXiv 1606.09282). It encourages preservation; it does not
guarantee it (Astra).

**Coefficient: fixed at 100, no sweep.** Scale check, on training batches
only, with no VAL or screen material (`calibrate_coef.py` →
[coef_calibration.json](./coef_calibration.json)):
- 100 batches from a fresh training stream (seed 20261132), 432 dry items.
- Gen 31's unpenalised fine-tune drifts r = 0.0061 (median 0.0044) from
  Gen 19 on dry input.
- At 100, that drift would cost 0.61 loss units, about 0.6 dB of the SI-SDR
  objective (mean −SI-SDR −10.1 dB).
- So the term is the same order as the main loss: neither negligible nor
  dominating. This answers Muse's "uncalibrated" concern without choosing
  the value from any result.

**Everything else is Gen 31 exactly:**
- Gen 19 seed-17 parent (`80000b64…`, enforced);
- Gen 19's own data stream from its committed 24k RNG handoff;
- aug50 (45 / 45 / 10) with the training RIR split;
- 8,000 updates, fresh Adam 1e-4 cosine to 1e-5, clipping 5, batch 8 × 2 s, final checkpoint only;
- Gen 31's `blend.py`, unchanged, grid α = 0.1…1.0;
- the same test-clean VAL panel (material `c2c4f89a…`) and the same prefix rule:
  - α\* is the largest α such that every α′ ≤ α has all four paired dry mean deltas vs Gen 19 ≥ 0;
  - if α = 0.1 fails, the result is **NO CANDIDATE → FAIL**, and no screen material is touched;
- one unchanged judge_v3 screen of the α\* blend vs same-seed Gen 19.

There is no coefficient, checkpoint, grid or margin rescue.

**Additions adopted from Astra's Gen 31 review (record-keeping only):**
- `preserve_dry` is written into the checkpoint metadata.
- `val_testclean2.py` is Gen 31's VAL script with one addition: it keeps
  per-item scores for every system, for descriptive voice-clustered
  intervals. The panel, material and rule are identical (tested).
- The Gen 31 VAL panel is now development material. The 24 reserved
  test-clean voices stay untouched.

**Timing (measured, MPS, 200 steps):**
- 0.104 s per step with the teacher, vs 0.094 s without (+11%).
- Fine-tune ≈ 14 min; blends and VAL ≈ 1 min; screen ≈ 5 min.

**Tests:** `test_train19.py`, 6/6 passing. They check that:
- the penalty is exactly 0 when student = teacher and 0 with no dry items;
- after a perturbation only the student gets gradients (finite), and the
  teacher gets none;
- the dry mask covers dry noisy and dry quiet;
- batches are bit-identical to Gen 31's train18;
- `--preserve-dry` is refused outside finetune;
- the CPU smoke logs a step-0 penalty of 0 and records the coefficient in
  the log and the checkpoint;
- the VAL copy has an identical panel, material hash and rule.

## Judgment (unchanged)

- judge_v3 (cleared at 2b548df) vs **same-seed Gen 19**.
- ADVANCE needs R1a ≥ +0.30 dB, R1b CI lo > 0, R1c ≥ 10/16, and C, T,
  D, S2, S3, SP all true. No tolerance.
- Reported descriptively:
  - the full VAL curve, with per-item clustered intervals;
  - the logged penalty trajectory;
  - Gen 32 vs Gen 31 VAL curves;
  - measured-room results room by room, and quiet / target-only results
    against bypass (Astra).
- ADVANCE authorizes seeds 18/19 (each repeats the procedure; the Gen 19
  seed-18/19 parent hashes must be added to `GEN19_SHA` first), then a
  fresh confirmation on reserved voices.

**Expectation, stated in advance:**
- NO CANDIDATE remains possible, because the zero-margin rule cannot be
  guaranteed by soft preservation.
- If a candidate exists, R1a ≥ +0.30 is uncertain.

Run: `research/gen32/pipeline.sh`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen32/train19.py` | `99d06d7f864c3c041eea48e72cc5add45ba777559f99ad9ffab72f7f9de3425f` |
| `research/gen32/test_train19.py` | `8b24a53c6d271b5bb72a35801f41701b7c7849751b0d841655f21a44d0b7e694` |
| `research/gen32/val_testclean2.py` | `f4716880680f52dab1d6f924eec9f6908b047de8da1ee09af015faf7bcbd0ccd` |
| `research/gen32/pipeline.sh` | `a63032649662767adb29768fb77d413cf827d8a346b784c87900f31888d0c43a` |
| `research/gen32/calibrate_coef.py` | `8f6aabe41aa810e7d420512a2ee563e2404a0299aa24d5bc405186c5d03ed09d` |
| `research/gen32/coef_calibration.json` | `48681f0d69f9a82f700a83ba9848aed1799576132839f0b18b6af562233c01a7` |
| `research/gen31/train18.py` | `c214820a08fa24cc9b94af7752e513b114b51f114fe425fa7a9127a67c717963` |
| `research/gen31/blend.py` | `652206ffed4ae4bd8138ef34a3756b57c55e7027f23d79da81dbd5c6d23654e1` |
| `research/gen31/val_testclean.py` | `349e6a0f7a17f4d59374f96e418ca1d76fd9e482cbb0cef416f2170e4f92a776` |
| `research/gen31/weights/ft_aug50_seed20261117.pt` | `4d356359a0362d3bdfef717789c0c5cc142fcb14c4c7a94137230d28f7f6994e` |
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
