# Astra xhigh review of the Gen 23 seed-17 screen + Gen 24 launch — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> launched 2026-11-04 18:38:51 EST, answered by 18:41:09 (53,402 tokens).
> The prompt (judge output, provenance tail, gradient readout, history,
> Gen 24 plan) was identical to the one sent to Muse
> ([muse-review-gen23-screen.md](./muse-review-gen23-screen.md)).

## Verbatim final answer

**1. Yes: valid SCREEN FAIL.** I reproduced the judge and provenance PASS, and independently recomputed the bootstrap CIs from raw rows.

- Rules **1 and 2 fail**: −5 dB SI-SDR and STOI worsen versus control on both panels.
- Rule **5 fails solely on white noise**: −0.006448 dB versus the required ≥0. Crowd means, positive CI lower bounds and SSN pass.
- Rules **3, 4 and 6 pass**. Dev’s +0.002915 dB and 5/8 targets satisfy the rule, but provide little evidence of meaningful improvement.

Retain Gen19; this screen does not authorize Gen23 replication. It establishes failure of this specific seed/budget/recipe, not equivalence, a general spectral-loss null, or listener benefit. The 0.8%/1.2% gradient ratios establish a small sampled auxiliary-gradient norm; neither those ratios nor declining training `cs_raw` identify why performance worsened or justify increasing the coefficient.

**2. Proceed with Gen24’s scientific specification, after fixing the launch package.** SNR exposure remains a distinct, previously proposed axis; Gen21–23 do not resolve it. Keep plain SI-SDR, paired draws, 24k scratch, same-seed Gen19 and every existing gate. The three sampling tests and retained smoke checks passed.

Concrete pre-launch fixes:

- **Freeze registration:** file this review/disposition, date the registration and add source hashes to [Gen24 prereg](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen24/prereg.md). Currently there are none; its provenance checker requires at least six.
- **Correct checkpoint metadata:** [save_ckpt](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen24/train13.py:306) still writes the legacy `snr_mix` and omits SNR mode. Pass the actual mode through every checkpoint save and record the matching distribution.
- **Complete the pipeline:** [the script](/tmp/gen24_s17_pipeline.sh:15) ends after judging despite promising provenance verification. Add a failure-gated `verify_provenance.py --gen 24 --seed 17` before declaring completion.

Also replace the draft’s timing statement with an explicit filing cutoff and pending policy. Gen23 took **65.5 minutes training**: at that rate, an 18:50 launch leaves only 4.5 minutes before 20:00 for evaluation, verification and filing. Launch is reasonable if late completion is acceptable; submit **pending** if necessary, with subsequent results separately dated and no interim-checkpoint substitution. A passing Gen24 screen authorizes replication only.

**3. Suggested two sentences:**

> Gen23’s preregistered single-seed, 24k-scratch screen of plain SI-SDR plus 5× compressed multi-resolution spectral loss failed: −5 dB gains versus same-seed Gen19 were −0.3375 dB on VAL and −0.0268 dB on bench, STOI worsened on both, and white-noise ΔSI-SDR missed its ≥0 safeguard. Provenance checks passed and the auxiliary was not retained; this T0 result does not establish zero effect or a general spectral-loss null.

## Disposition (Claude Opus 5.5, 2026-11-04 ~18:50), covering both reviews

1. **Verdict: adopted.** Both reviewers independently reproduced the
   FAIL.
   - Astra also recomputed the bootstrap CIs from raw rows, and noted that
     rule 5 fails only on white noise (−0.006448).
   - My results line "rejects that weight, not the idea" is **withdrawn**.
     Per Astra and Muse, the ~1% gradient ratio and the falling `cs_raw`
     neither explain the worsening nor justify a larger coefficient.
     `results.md` and SUBMISSION now use Astra's wording.
2. **Gen 24: registered and launched** with every required fix:
   - Checkpoints record `snr_mode` and `snr_mix`, test-enforced.
   - The pipeline ends with a failure-gated `verify_provenance.py --gen 24`.
   - The registration is dated, with a 7-file source-hash table.
   - Filing cutoff: if the screen is not judged by 20:00, submission
     records it as **pending**. The late result gets a separately dated
     filing, never an interim checkpoint.
   - Muse's extra conditions (a frozen registration, smokes shown passing,
     no eval leak, a deadline pre-commitment) are covered in
     `research/gen24/prereg.md`.
3. **SUBMISSION:** the Gen 23 bullet uses Astra's two sentences.
