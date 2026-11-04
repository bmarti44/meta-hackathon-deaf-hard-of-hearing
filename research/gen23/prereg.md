# Gen 23 pre-registration — plain SI-SDR + 5 × compressed spectral loss

> Claude Opus 5.5, 2026-11-04 ~17:30 EST. Written before the
> full-budget screen. Only the disclosed smoke runs below came first.
> Source: Astra's Gen 21 review rank 2
> ([../gen21/astra-review-gen21.md](../gen21/astra-review-gen21.md)),
> frozen by her Gen 22 screen review
> ([../gen22/astra-review-gen22-screen.md](../gen22/astra-review-gen22-screen.md)).
> Gen 22 (30 dB cap) failed its screen, so the cap is **not** retained
> and the retained objective is plain SI-SDR. T0 in-silico only.
> `promoted FALSE`.

## Question

Does adding compressed multi-resolution spectral supervision to the
waveform SI-SDR objective lift crowd −5 dB performance over the same-seed
Gen 19 model, with the training budget unchanged?

## The one change

`research/gen23/train12.py --loss sisdr_cs5`. For item *i*,
resolution *r*, STFT *Z*:

- `P(Z) = Re(Z)² + Im(Z)² + 1e-12`
- `M(Z) = P^0.15`
- `C(Z) = Z · P^−0.35`
- `L_CS,i = (1/3) Σ_r [ 0.7·mean_{f,t}(M(Ẑ)−M(Z))² + 0.3·mean_{f,t}|C(Ẑ)−C(Z)|² ]`
- `L = mean_i [ −SI-SDR_i + 5·L_CS,i ]`

| Setting | Value |
|---|---|
| Resolutions (FFT / hop) | 256/64, 512/128, 1024/256 |
| Window | periodic Hann, `center=False`, one-sided |
| Normalization | `normalized=True` (÷√N), equal resolution weights |
| Complex error | re² + im² (no /2) |
| Comparison | output vs the same DELAY-shifted clean target, full tensors |
| Level convention | clean RMS 0.1 (unchanged generator) |
| Execution device | **CPU** for the L_CS term |

L_CS is not scale-invariant. Scaling both signals by *a* scales it by
about |a|^0.6, so its effective weight is level-dependent, and it
penalizes output gain errors (disclosed, not tuned).

CPU execution is needed because MPS `torch.stft` gradients were not
bit-deterministic across identical calls (2026-11-04). CPU gradients
are, and they cross back to the MPS model.

Everything else is the Gen 22 trainer, which is Gen 19's update path:

- same model (602,510 params), data, batch 8×2 s, 10% quiet, clip 5;
- Adam, cosine 1e-3→1e-4 over 24k, 24k scratch;
- resume identity check (seed/mode/loss/steps/data/parent).

**Source hashes at registration (sha256):**

| File | sha256 |
|---|---|
| `gen23/train12.py` | `edbad003850c288dfeb2d48e63b1efa241def64aae38005e4c17c40bcf9947ec` |
| `gen23/judge_screen.py` | `82a60b5c90b754491d956cfa48db6746e84423e42fc3e33edd717b5d89cdf53d` |
| `gen22/judge_screen.py` | `1ad8b64dff41cc817275f93e06613163b6013b8a913378ba00b2d87ce00deff2` |
| `gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `gen21/dev_audit.py` | `4d160387aab1aab604d9dd2c4d0a575afebd883234d7d35a66493f605a4ab168` |

Any change to these files before the judge runs invalidates the screen.

## Logs (no decision role)

For `sisdr_cs5`, every 25 steps:

- `total_loss` (the combined objective);
- `neg_sisdr_db` (plain);
- `cs_raw` and `cs_weighted`;
- grad norm and LR.

Every 500 steps:

- quiet/noisy gradient norms;
- `gn_sisdr` and `gn_cs5`, the gradient norms of the mean plain term and
  the mean 5·L_CS term (actual batch weighting), computed with
  `autograd.grad` before the real backward.

## Pre-launch evidence (disclosed smoke runs, MPS, `research/gen23/smoke/`; re-check with `smoke/check_smokes.py`)

- `sisdr_parity.log`: `--loss sisdr` reproduces Gen 19 seed-17
  loss and grad-norm bit-for-bit at every logged step 0–200.
- `cs5_a.log` vs `cs5_nodiag.log`: diagnostic every 50 vs off gives
  identical logged updates through step 200, and a repeated
  diagnostic run was bit-identical.
- `gn_cs5 > 0` at every diagnostic step, so the CPU-computed CS
  gradient reaches the model parameters on MPS.
- At step 0–200 `gn_cs5` is 0.13–0.48 against `gn_sisdr` 1.6–170, so
  5·L_CS is a small fraction of the gradient early in training. This
  is disclosed, not tuned.
- Tests: `test_train12.py` and `test_judge_screen_g23.py` (10 tests):
  - `sisdr_cs5` ≡ plain + 5·L_CS with frozen constants;
  - L_CS = 0 at a perfect output and > 0 for errors and gain errors;
  - finite gradient at silence;
  - MPS-input gradient bit-deterministic;
  - Gen 19 batch stream replayed;
  - CPU uninterrupted run vs a run resumed from its saved intermediate
    state is bit-identical, with the renamed fields (wording corrected
    per the Astra code audit, 17:40);
  - a changed loss refused on resume;
  - judge = Gen 22 rules with the Gen 23 name and policy, Gen 22 logs
    and dev rows refused.

## Control, panels, rules — unchanged from Gen 22

The control is the Gen 19 final of the same seed. Panels:

- VAL: the Gen 19 step-0 record in the Gen 21 R48 log;
- `bench_v2_gen19.json`;
- dev systems `control`/`cs5`, 8 targets × 4 crops × 4 mixtures ×
  2 SNRs.

Judge: `research/gen23/judge_screen.py --seed 17`, which calls
`gen22/judge_screen.judge(cand="cs5", policy={scratch, sisdr_cs5,
24000})`. Gen 22's rules 1–6 and its confirmation rule apply verbatim
([../gen22/prereg.md](../gen22/prereg.md)). That includes **+0.30 dB at
−5 dB on BOTH VAL and bench**, the safeguards with CI lower bounds,
and a dev panel with a positive gain and ≥5/8 targets improving. Final
checkpoint only.

A passing screen authorizes seeds 18/19 replication. It does not
authorize retention or promotion.

## Defects and incomplete runs

A defect found by the concurrent audit, or a crash that cannot be
resumed with the identity check, makes the run **invalid** (filed, not
judged). An unfinished run is **pending**. In neither case is the
objective changed or an interim checkpoint judged.

## Timing and deadline

The diag-off smoke ran at 0.1225 s/step. Gen 22's production run
averaged 0.227 s/step, so the estimate is 50–100 min of training plus
~3 min of bench, dev and judge.

The run launches ~17:35 via `/tmp/gen23_s17_pipeline.sh` (train →
bench → dev → judge, gated). If it is not judged by 19:40, SUBMISSION
records it as pending and the result is filed later in the repo. An
Astra code audit runs concurrently with training.

Run: `/tmp/gen9env/bin/python research/gen23/train12.py --loss sisdr_cs5 --mode scratch --seed 20261117`
