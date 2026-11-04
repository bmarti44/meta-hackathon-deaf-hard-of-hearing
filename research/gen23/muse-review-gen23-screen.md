# Muse (Meta) independent review of the Gen 23 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), reasoning effort `high`, via the
> Meta Model API Responses endpoint, through the `beforetheimplant-muse`
> Lambda's direct-invoke-only `review` mode (`api/index.mjs`). The key was
> read server-side from SSM.
>
> - **Invoked:** 2026-11-04 18:38:51 EST, answered by 18:39:28.
> - **Prompt:** identical to Astra's (judge output, provenance tail,
>   gradient readout, history, Gen 24 plan, three questions). The Muse
>   instruction was: "independent scientific reviewer… check arithmetic…
>   never claim clinical benefit".
> - **Role:** a second reviewer beside Codex Astra (Gen 23 is the first
>   generation reviewed by both). The disposition is in
>   [astra-review-gen23-screen.md](./astra-review-gen23-screen.md).

## Verbatim answer

1. Verdict arithmetic / characterization: CORRECT - FAIL stands.

- Checked: VAL -5 0.2266-0.5641=-0.3375; bench -5 1.0336-1.0604=-0.0268; dev mean [-0.076+0.366-0.322+0.033+0.168+0.008-0.209+0.054]/8=+0.00275~+0.003 with 5/8>0. Checks 1=False, 2=False, 5=False correctly force SCREEN FAIL under both-gates rule, despite 3,4,6=True. Quiet 35.3~35.28 rounding only.
- Provenance tail supports summaries from raw.
- May conclude: single-seed in-silico candidate did not meet pre-reg +0.30dB both VAL+bench and STOI non-worsening; numerically worse at -5dB.
- May NOT conclude: clinical benefit/harm, intelligibility for CI users, or general disproof of compressed spectral loss. One seed, one 5x weighting, metrics only. Gradient readout gn_cs5/gn_sisdr median 0.008, late 0.012; cs_raw 0.0574->0.0428 is descriptive only, not causal proof of under-weighting vs optimization.

2. Gen24 narrower-SNR, plain SI-SDR, same rules: CONDITIONAL GO, do not launch as timed.

- Condition met for plain SI-SDR fallback: Gen23 FAILED.
- Keep rules unchanged: +0.30dB BOTH, STOI non-worsening, 0dB, quiet, other-rows CI-lo, dev>0 + >=5/8. No threshold relaxation after Gen21-null / Gen22 VAL+0.149 bench-0.010 / Gen23-negative.
- Blocking: NOT registered yet, files unverified here. Must freeze research/gen24/prereg.md + train13.py affine remap 0.6*U(-5,-2)+0.4*U(-2,10) + judge + tests/smokes, show smokes pass, confirm same-seed control and no eval leak, BEFORE any training. Affine remap must be exact and documented.
- Timing blocks: 18:50 launch -> 19:45-19:55 verdict leaves ~5-15min to 20:00 deadline. Launch only with hard pre-commit to stop/report before deadline; if slow, defer. Expectation low given 3 misses; risk trading 0dB/other-rows for -5dB.

3. SUBMISSION.md Gen23 bullet:

Gen23 seed-17 SCREEN FAIL: plain SI-SDR + 5x compressed multi-resolution loss vs same-seed control gave -5dB SI-SDR gains -0.34dB VAL / -0.03dB bench and STOI -0.0120/-0.0028, failing pre-reg +0.30dB-both and non-worsening gates; provenance rehash PASS, no in-silico advantage shown.
