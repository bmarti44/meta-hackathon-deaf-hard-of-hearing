# Gen 24 pre-registration — DRAFT: narrower noisy-SNR sampling

> Claude Opus 5.5, 2026-11-04 ~17:42 EST. **DRAFT, not yet
> registered.** It becomes registered only by a dated header edit made
> after (a) the Gen 23 screen verdict is filed and (b) Astra's review of
> that verdict is filed with a disposition. No Gen 24 training has run.
> Source: Astra's Gen 21 review rank 3
> ([../gen21/astra-review-gen21.md](../gen21/astra-review-gen21.md)).
> T0 in-silico only. `promoted FALSE`.

## Condition

- **If Gen 23 FAILs its screen:** Gen 24 = plain SI-SDR (`--loss sisdr`)
  + `--snr hard60`, 24k scratch, vs the Gen 19 final of the same seed.
- **If Gen 23 ADVANCEs:** Gen 24 waits for Gen 23's seed 18/19
  replication. Its objective would then be the retained one, which needs
  a revised registration.

## The one change

`research/gen24/train13.py --snr hard60` changes the noisy-example SNR
distribution:

| | Distribution | Share of noisy items in [−5, −3] dB |
|---|---|---|
| Gen 19 | 0.6·U(−5, 5) + 0.4·U(−5, 10) | 17.3% |
| `hard60` | 0.6·U(−5, −2) + 0.4·U(−2, 10) | 40%, about 2.3× |

The new values come from an affine map of the **same draws**: the branch
draw, then the uniform draw. That means RNG consumption, clean targets,
noise waveforms, quiet 10%, babble/SSN 70/30 and k ~ U{2..12} are all
unchanged; only the noise level differs.

`--snr legacy` reproduces the Gen 19 batch stream bit-for-bit
(test-enforced). The SNR mode is part of the resume identity.

## Control, panels, rules

These are unchanged from Gen 22/23:

- **Judge:** `research/gen24/judge_screen.py`, which calls
  `gen22/judge_screen.judge(cand="hard60", policy={scratch, sisdr,
  snr hard60, 24000})`.
- **Rules:** Gen 22's rules 1–6 and its confirmation rule apply
  verbatim. The bar is +0.30 dB at −5 dB on both VAL and bench, plus the
  0 dB safeguard (Astra: "particularly important" here).
- **Filing check:** `gen23/verify_provenance.py`, extended to Gen 24.

## Evidence so far (draft)

`test_train13.py` and `test_judge_screen_g24.py` (8 tests) cover:

- the legacy stream equals Gen 19's;
- `hard60` has the same clean targets and kinds, noise equal up to
  level, and identical RNG consumption;
- the interval endpoints and the 40% exposure;
- a CPU resume that is bit-identical, with a changed SNR mode refused;
- the judge refusing legacy-SNR logs.

MPS smokes in `research/gen24/smoke/` (re-check with `check_smokes.py`;
run ~17:41 while Gen 23 trained):

- `--snr legacy` matches Gen 19 seed-17 loss and grad norm bit-for-bit,
  steps 0–200;
- two `hard60` runs are bit-identical, and they differ from legacy as
  expected (step-25 loss 5.25 vs 2.85).

## Timing

24k steps took ≈ 50–95 min on MPS today. If registered after ~18:35,
the result will not be judged before the 20:00 submission. It would be
filed later; interim checkpoints are never judged.
