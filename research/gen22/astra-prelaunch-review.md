# Astra xhigh pre-launch review of Gen 22 (trainer, prereg, judge, tests) — verbatim + disposition

> Requested 2026-11-04 ~13:12 EST by Claude Opus 5.5, before any
> Gen 22 training and before the Gen 21 verdict. Command:
> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only "<prompt>"`
> (prompt: review train11.py vs train10.py, the control-parity
> claim, prereg/judge fidelity to her rules, tests, and whether to
> launch today). Verbatim answer below.

---

**Hold launch until the resume and judging gaps below are fixed.** The capped loss is correct and worth screening. Gen21’s verdict remains pending; this review does not select its outcome. T0 only; `promoted FALSE`.

1. **Loss and diagnostic: correct.** The implementation preserves centering, projection and numerical floors, adding exactly `1e-3 * power` to the denominator. The normal backward, clipping and optimizer/scheduler sequence is unchanged. Uncapped logging evaluates the same pre-update output without gradients. [train11.py:156](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:156), [train11.py:361](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:361)

   The quiet/noisy diagnostic correctly retains each contribution’s `/8` weighting and uses `retain_graph=True`. I independently checked both losses on synthetic CPU inputs: diagnostics preserved existing `.grad` values, and the subsequent backward was bit-identical to backward without diagnostics. No optimizer updates were performed.

2. **Resume works for matching arguments, but permits invalid continuations.** Optimizer, scheduler, NumPy generator, CPU Torch RNG, accumulated logs and elapsed time are restored; `start = saved_step − life0` is correctly indexed. However, validation checks only seed/mode/loss. It neither stores nor validates the original total budget, data identity or restart provenance. [train11.py:248](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:248), [train11.py:347](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:347)

   This has concrete consequences: resuming a 48k scratch schedule with default `--steps 24000` restores its old cosine horizon but stops at 24k. In restart mode, the restored scheduler retains the newly constructed lambda, which closes over the current `a.steps`; changing that argument changes subsequent learning rates. A saved step beyond the requested endpoint is also accepted and can be relabeled as that earlier endpoint. [train11.py:325](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:325), [train11.py:418](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:418)

   The Gen21 handoff path is correct. Restart resume nevertheless reloads the original parent/handoff and overwrites the initial-state artifact **before validating the resume file**. Load and validate resume first. Also make rolling saves atomic: directly overwriting the sole latest checkpoint leaves it vulnerable to another session termination during serialization. [train11.py:295](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:295), [train11.py:342](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:342), [train11.py:409](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:409)

   Only CPU Torch RNG is saved. That suffices for this deterministic model/data path; it is not a general guarantee for future MPS-random operations.

3. **Gen19 is a defensible matched control under the 24k-scratch policy.** The source audit supports reuse: initialization and schedule match, the loss/data helpers are AST-identical, and current pool counts match Gen19’s 251 speakers/28,539 files. Reported MPS parity through 325 and resume parity through 425 strengthen that conclusion, but scalar equality over this prefix does not prove a bit-identical 24k final. I could not locate the retained smoke artifacts, so I have not independently verified those particular claims. Preserve their commands, logs and comparison results. [prereg.md:29](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:29), [train8.py:229](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen19/train8.py:229)

   **The control VAL source is correct.** R48’s step-zero/lifetime-24000 entry evaluates the loaded Gen19 parent before updates. I recomputed −5 values **0.5640785145 / 0.0091385745**, and 0 dB **4.1003555310 / 0.0798482616**. Its `parent_sha256`, the actual Gen19 checkpoint and Gen19 bench hash match. [R48 log:7042](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_r48_seed20261117.json:7042), [Gen19 bench:2](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/bench_v2_gen19.json:2)

4. **The principal numeric rules match; safeguard and evidence validation are incomplete.** Both-panel +0.30, non-worsening STOI, −0.15/−0.003 limits, quiet thresholds, and positive dev mean with five improving targets are implemented correctly. [judge_screen.py:50](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/judge_screen.py:50)

   However, “currently-passing required rows” includes **positive CI lower bounds for crowd SI-SDR, STOI and ACE-electro**. Both the preregistration’s enumeration and judge omit these. They are part of the existing contract and pass for the parent. [prereg.md:69](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:69), [KPI.md:30](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/KPI.md:30)

   The judge also discards dev hashes and trusts summary dictionaries without requiring the eight registered targets or paired rows. My in-memory fixture returned `ADVANCE` with **five arbitrary targets, a wrong dev checkpoint hash and negative crowd CI bounds**. Require matching candidate/control hashes, exact target sets, and 16 paired items per target per SNR. The intended panel generator itself is correct: **128 items per SNR, 256 total**. [judge_screen.py:25](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/judge_screen.py:25), [dev_audit.py:40](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/dev_audit.py:40)

   Finally, enforce final-checkpoint metadata. `--steps` can select an interim VAL entry while the imported `val()` helper returns the log’s **final** hash, allowing the hash check to pair interim VAL with final bench. For control provenance, compare the R48 log’s **parent** hash with Gen19’s bench/checkpoint hash. [judge_screen.py:21](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/judge_screen.py:21), [judge_replication.py:21](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/judge_replication.py:21)

5. **Keep policy selection genuinely conditional.** Remove “Gen21 selected neither arm” from help and “expected” from the table. Use **selected policy**, since qualification and selection are different when both arms qualify. If R48 or S48 is selected, the judge’s hard-coded Gen19 control and scratch filenames must change alongside the preregistration; a prose addendum alone is insufficient. Confirmation currently also hard-codes Gen19 controls. [train11.py:267](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:267), [prereg.md:40](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:40), [prereg.md:75](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:75)

   Specify confirmation aggregation before launch: positive changes in ≥2/3 seeds **on each primary panel**, and how the eight-target dev condition aggregates across seeds.

6. **Tests are useful but insufficient for the new infrastructure.** All **five Gen22 tests plus two Gen21 tests passed** with cache writes disabled. Existing Gen22 tests cover loss properties and four synthetic batches, not diagnostic isolation, optimizer/scheduler resume or judging. [test_train11.py:33](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/test_train11.py:33)

   The most valuable addition is uninterrupted-versus-resumed equality with the **same original schedule horizon**, comparing parameters, optimizer state, next batch, learning rate and log sequence across diagnostic/evaluation boundaries. Add rejection tests for changed budgets/provenance and judge fixtures for missing targets, wrong hashes, interim checkpoints and failed CI bounds.

7. **Worth launching today conditionally; submission readiness takes priority.** After Gen21’s filed verdict/review/disposition and these fixes, a 24k screen is a reasonable next experiment. Allow time for **bench, expanded dev, judging and filing**, not training alone. The historical Gen19 seed-17 run took **84.8 minutes**, so 76 minutes is plausible but not a guaranteed allowance. [Gen19 log:3](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen19/weights/train_log_seed20261117.json:3)

   I would target launch **by approximately 17:30 local**, with a credible completion budget through the registered 19:30 cutoff. Otherwise, file it as the next step. A selected 48k policy needs a separate timing calculation; seed-18 S48 took **174 minutes**. [prereg.md:87](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:87), [S48 log:7](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_s48_seed20261118.json:7)

**Required before launch:** fix resume validation/atomic persistence; restore the omitted CI safeguards; enforce panel/hash/final-checkpoint identity; freeze the actual selected policy and confirmation aggregation; add focused regression coverage and retain parity evidence.

**Optional:** make the milestone `*_state_step*.pt` files resumable too—they currently omit logs required by `--resume`—and ensure custom diagnostic intervals are logged even when not divisible by 25. [train11.py:383](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:383)

No repository files were changed.

---

## Disposition (Claude Opus 5.5, 2026-11-04 ~13:25)

All "required before launch" items adopted; Gen 22 still NOT launched
(Gen 21 verdict + its Astra review come first).

1. **Resume validation / atomic persistence — fixed.** `--resume` is
   loaded and validated right after argument parsing, before any
   artifact is touched: seed, mode, loss, total budget (`--steps`),
   data root, `--init-from` must match; saved step must lie strictly
   inside the run; restart parent sha and pool file count are checked
   once known. Restart+resume no longer rewrites the initial-state
   file. All state saves go to `<file>.tmp` then `os.replace`.
   Milestone `*_state_step*.pt` now carry log/VAL/identity and are
   saved after that step's VAL, so they are resumable (optional item
   adopted). Diagnostic steps are always logged (optional item adopted).
2. **Regression coverage — added.** CPU end-to-end test: 6-step run vs
   the same run resumed from its step-3 rolling state (same horizon,
   diagnostics every 2 steps straddling the resume) → identical
   weights, logs (incl. LR), VAL; `--steps 8` and `--loss sisdr`
   resumes are REFUSED. Judge fixtures from real Gen21 artifacts:
   clean FAIL reproduces S48 s17 numbers (+0.4409 VAL / −0.1267
   bench), ADVANCE path works, failed CI bound FAILs, and missing
   target / wrong dev hash / interim checkpoint / bench-hash
   mismatch / wrong policy each raise `Invalid`. 37 tests green.
3. **Parity evidence retained**: `research/gen22/smoke/*.log` +
   `parity_check.py`; re-run on the fixed trainer: bit-identical to
   Gen19 s17 through step 200. Prereg now states that prefix parity
   is not a proof of a bit-identical 24k final.
4. **CI safeguards restored** (crowd SI-SDR/STOI/ACE CI lower bound
   > 0) in prereg rule 5 and the judge. Judge now enforces final-only
   (`lifetime_steps == 24000`, registered loss/mode/steps), candidate
   hash identity across VAL log / bench / dev rows, control hash
   identity across R48 parent / Gen19 bench / dev rows, exact 8
   targets × 16 paired items, and recomputes dev gains from rows.
   `gen21/judge_replication.py` also asserts R48 parent == parent bench.
5. **Policy wording** now "selected policy", no "expected"; the judge
   refuses non-24k-scratch policies; R48/S48 selection requires a
   dated addendum + matching judge reviewed before launch.
   Confirmation aggregation pre-specified (≥2/3 seeds positive on
   EACH of VAL and bench; dev 3-seed mean > 0 with ≥5/8 targets on
   3-seed per-target means).
6. **Timing**: Gen21 seed-19 R48 now runs concurrently with S48s19's
   second half (launched on its 24k RNG handoff) to bring the Gen21
   verdict forward; deterministic training makes this a scheduling
   change only. Launch Gen22 seed 17 only if possible by ~17:30.
