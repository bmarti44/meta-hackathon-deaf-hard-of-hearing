# Gen 25 pre-registration — weight-space checkpoint averaging (no training)

> Claude Opus 5.5, 2026-11-04 ~20:30 EST. Written before any candidate is
> built or evaluated. The holder asked whether the weights themselves can
> be edited to make improvements; this is the most reliable such method
> and the cheapest one to test first. T0 in-silico only. `promoted FALSE`.
> Runs alongside Gen 24 (a different axis); each is judged against Gen 19
> on its own.

## Question

Does averaging the weights of Gen 19's late checkpoints (stochastic weight
averaging, applied post hoc) lift crowd −5 dB performance over the Gen 19
final of the same seed?

## The one change (no training, no selection)

`research/gen25/swa.py --seed S` makes the candidate:

- It averages every parameter of Gen 19 seed S's checkpoints at steps
  20000, 20500, …, 23500 and the final 24000 (**9 checkpoints**).
  That window is the last sixth of the cosine schedule.
- The average is uniform and fixed in advance. No checkpoint is chosen,
  weighted or dropped based on any result.
- It uses the same architecture (602,510 params). Exact causality is
  re-verified on the averaged weights.
- The model has no batch-norm statistics to recompute; its normalisation is
  cumulative layer norm, with affine parameters only.

This is a post-hoc rule declared before evaluation, not interim-checkpoint
judging: the candidate is one fixed function of the run, and the Gen 19
final is unchanged as the control.

**VAL parity guard.** The script first re-evaluates the Gen 19 final with
the same VAL function (`gen22/train11.py` `eval_val`). It must reproduce
the control VAL record (the Gen 21 R48 step-0 entry) item for item, with
max |diff| < 1e-4, or the run aborts.

## Control, panels, rules

These are identical to Gen 22–24:

- **Control:** Gen 19 final, same seed (VAL from the R48 step-0 record;
  `bench_v2_gen19.json`; dev system `control`).
- **Judge:** `research/gen25/judge_screen.py`, which calls
  `gen22/judge_screen.judge(cand="swa9", policy={swa, sisdr, 24000})`.
- **Rules:** Gen 22's rules 1–6 verbatim. The screen ADVANCEs only with
  +0.30 dB at −5 dB on BOTH VAL and bench, STOI non-worsening, the 0 dB
  safeguard, quiet, the other required rows with CI lower bounds, and the
  dev panel > 0 with ≥ 5/8 targets.
- **Provenance:** `gen23/verify_provenance.py --gen 25` must PASS.
- **Confirmation (only if the seed-17 screen ADVANCEs):** seeds 18 and 19,
  same recipe, under Gen 22's confirmation rule (3-seed means; positive in
  ≥ 2/3 seeds on each of VAL and bench; dev 3-seed mean > 0 with ≥ 5/8
  targets). Because no training is needed, confirmation takes minutes.
  Only then would the averaged model replace Gen 19 as the baseline.

## Expectation (stated in advance)

Checkpoint averaging usually gives small gains, a few tenths of a dB at
most. A FAIL against the +0.30 bar is the likely outcome, and it is filed
as a null like any other.

## Source hashes at registration (sha256)

| File | sha256 |
|---|---|
| `gen25/swa.py` | `11cd8a17e044e40c4fcdae255c7f817737893436556bfa3566491c8c7fd24aa1` |
| `gen25/judge_screen.py` | `59cc985ec3574961c6af9cb0fd65d069470d1a628ff031628c67354dad828122` |
| `gen22/judge_screen.py` | `1ad8b64dff41cc817275f93e06613163b6013b8a913378ba00b2d87ce00deff2` |
| `gen22/train11.py` | `961c878c3358a210a53d522bb41c252eff5a494b51f9349aacde7621f90047c7` |
| `gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `gen21/dev_audit.py` | `4d160387aab1aab604d9dd2c4d0a575afebd883234d7d35a66493f605a4ab168` |
| `gen23/verify_provenance.py` | `eba3c530ad8df0b8ea56175b782cd0b9895c4a5b2acf84ebefdc09ef5b5b11b7` |

Run: `/tmp/gen25_pipeline.sh 17` (build → bench → dev → judge →
provenance, each gated on exit status).
