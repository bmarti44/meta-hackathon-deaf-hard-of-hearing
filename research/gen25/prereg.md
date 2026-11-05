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

## Revision after Astra's pre-launch review (2026-11-04 ~20:50, before any candidate was built)

Per [astra-prelaunch-review.md](./astra-prelaunch-review.md):

- **Input identities:** every input must match the committed
  `input_manifest.json` (27 hashes, 9 per seed), and the verifier
  re-derives the average bit-exactly.
- **Parity guard:** covers both metrics, finite values, unique keys and
  exact panel membership.
- **Own verifier:** Gen 25 has its own
  `research/gen25/verify_provenance_g25.py`, so the shared
  `gen23/verify_provenance.py` stays byte-identical to Gen 24's
  registration.
- **CPU only**, with no-overwrite guards.
- **Disclosure:** this hypothesis arose after seeing Gen 19's trajectory
  and the holder's question about editing weights.
- **KPI arithmetic:** Gen 19's exact seed-mean at −5 dB is 1.187654, so
  clearing the +1.5 KPI needs +0.312346 dB. A +0.30 screen pass alone does
  not clear the KPI.

## Source hashes at registration (sha256, revised)

| File | sha256 |
|---|---|
| `gen25/swa.py` | `202a8293f6390759cd01af1eeb196ead409810da9713283016b3794ac4b14bba` |
| `gen25/judge_screen.py` | `59cc985ec3574961c6af9cb0fd65d069470d1a628ff031628c67354dad828122` |
| `gen22/judge_screen.py` | `1ad8b64dff41cc817275f93e06613163b6013b8a913378ba00b2d87ce00deff2` |
| `gen22/train11.py` | `961c878c3358a210a53d522bb41c252eff5a494b51f9349aacde7621f90047c7` |
| `gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `gen21/dev_audit.py` | `4d160387aab1aab604d9dd2c4d0a575afebd883234d7d35a66493f605a4ab168` |
| `gen25/verify_provenance_g25.py` | `55017367b7c42bdce1aad15fdfac2ddd0e97b83b75dd75c84bb70fa116e13078` |
| `gen25/pipeline.sh` | `e68db687b80876c71222d1697c1b3c35507e8628751e84eab64f19e6ec949f39` |
| `gen25/input_manifest.json` | `27a14a3f5748c29b031b1525e6039b4ee9dfa13a324b0a617961fd159b1692f0` |

Run: `research/gen25/pipeline.sh 17` (build → bench → dev → judge →
provenance, each gated on exit status).
