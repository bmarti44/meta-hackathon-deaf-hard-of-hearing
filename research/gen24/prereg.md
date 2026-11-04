# Gen 24 pre-registration — narrower noisy-SNR sampling (REGISTERED)

> Drafted by Claude Opus 5.5 at ~17:42. **REGISTERED 2026-11-04 ~18:50 EST**,
> after the Gen 23 FAIL verdict and both of its reviews were filed:
> - Astra: [../gen23/astra-review-gen23-screen.md](../gen23/astra-review-gen23-screen.md),
>   with disposition;
> - Muse: [../gen23/muse-review-gen23-screen.md](../gen23/muse-review-gen23-screen.md).
>
> Both cleared the science and required the launch-package fixes below
> (all applied). No Gen 24 training preceded this registration beyond
> the disclosed 200-step smokes.
> Source: Astra's Gen 21 review rank 3
> ([../gen21/astra-review-gen21.md](../gen21/astra-review-gen21.md)).
> T0 in-silico only. `promoted FALSE`.

## Condition

- **Gen 23 FAILED its screen (applies):** Gen 24 = plain SI-SDR (`--loss sisdr`)
  + `--snr hard60`, 24k scratch, vs the Gen 19 final of the same seed.
- *(Not applicable)* If Gen 23 had advanced: Gen 24 waits for Gen 23's seed 18/19
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

## Launch-package fixes (Astra/Muse Gen 23 reviews)

- **Checkpoint metadata:** every checkpoint save now records `snr_mode`
  and the matching `snr_mix` distribution (test-enforced).
- **Pipeline:** `/tmp/gen24_s17_pipeline.sh` ends with a failure-gated
  `verify_provenance.py --gen 24 --seed 17` before `PIPELINE DONE`, and
  every step is gated on its exit status.
- **No evaluation leak:** VAL, bench v2 and the dev panel are unchanged.
  The SNR remap touches only training draws, and train and evaluation
  speakers are disjoint as before.
- **Tests:** 8 Gen 24 tests pass, including the checkpoint metadata.

## Source hashes at registration (sha256)

Any change to these before the judge runs invalidates the screen.

| File | sha256 |
|---|---|
| `gen24/train13.py` | `5ad336fc891dac7ceff79a63a78393a8d1a5166b88bee92c734f9841aafdce08` |
| `gen24/judge_screen.py` | `b176836d5ad023a0cbc0ae2eae4d6e3c25ec8c85276713bb72bc41b9a394c471` |
| `gen22/judge_screen.py` | `1ad8b64dff41cc817275f93e06613163b6013b8a913378ba00b2d87ce00deff2` |
| `gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `gen21/dev_audit.py` | `4d160387aab1aab604d9dd2c4d0a575afebd883234d7d35a66493f605a4ab168` |
| `gen23/verify_provenance.py` | `1b1bf42bba4bbefed0e7b89895dc9573fe3cc187fd853b95807741cb99481880` |

## Timing, filing cutoff and pending policy

- **Expected finish:** Gen 23 trained in 65.5 min. Launched ~18:50, Gen 24
  is expected to be judged ~19:55–20:10, plus the provenance check.
- **Filing cutoff:** the repository's submission state is frozen at 20:00
  EST. If the screen is not judged and provenance-verified by then,
  SUBMISSION.md records **"Gen 24 screen pending at submission"**.
- **Late result:** filed afterwards in a separately dated commit, with
  results, reviews and disposition.
- **Never:** an interim checkpoint judged or substituted, or a rule
  relaxed.
- **A passing screen** authorizes seeds 18/19 replication only.

Run: `/tmp/gen9env/bin/python research/gen24/train13.py --loss sisdr --snr hard60 --mode scratch --seed 20261117`
