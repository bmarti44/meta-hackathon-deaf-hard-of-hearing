# Astra xhigh pre-launch review of screen v2 + Gen 26 — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 ~20:57–21:01 EST (84,319 tokens). Prompt: `/tmp/astra_g26_prompt.txt`.

## Verbatim final answer

**At `a634d0a`, the fixed-midpoint experiment is valid in principle, but three integrity defects should be fixed before building Gen26.** Review was read-only; no candidate was built.

**BLOCKING defects:**

1. **The verifier does not enforce the registered endpoint pair or seed.** [verify_g26.py:10](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen26/verify_g26.py:10) accepts any two manifest-listed inputs. In memory, it reported `PASS` for **Gen19 + Gen19**, including seed-18 inputs under `--seed 17`. Derive the two expected paths from `--seed`, require one Gen19 and one same-seed R48, verify seed metadata and ancestry independently, then recompute the midpoint.

2. **S3’s `min(...) > 0` differs from the earlier judge for NaNs.** A NaN STOI or ACE lower bound can be ignored by `min`, allowing `ADVANCE`; I reproduced both cases. The earlier `all(x > 0 for x in lo)` rejects them. Require finite metrics and individually positive bounds. [judge_v2.py:81](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/screen_v2/judge_v2.py:81)

3. **Bench provenance checks only the checkpoint hash, not the registered material coverage.** The judge accepted an invalid bench identifier, `n_per_cell=2`, and empty raw rows with populated summaries. Require bench v2, six items per cell, complete duplicate-free candidate/unprocessed pairing, and matching finite metric counts. The earlier judge at least asserted six crowd rows at each decision SNR. [judge_v2.py:60](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/screen_v2/judge_v2.py:60)

**NON-BLOCKING issues:**

- **Confirmation implementation remains outstanding.** The registered three-seed calculation is sensible: average within each voice across seeds, then bootstrap those **16 means**, not 48 voice-seed records. Freeze an executable aggregator before confirmation results arrive, and clarify whether STOI non-worsening applies to the three-seed mean or every seed. The four reserves are not used by the current confirmation procedure; define their procedure before opening them. [prereg.md:52](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/screen_v2/prereg.md:52)
- **Qualify “unused/untouched.”** All 20 advancement/reserve voices are disjoint from the actual Gen19/R48 training sets, but they appeared in Gen17’s training pool. They are fresh evaluation material for this lineage, not globally unused research data. This does not introduce training leakage into the scratch-trained Gen19 and its continuation. [train6.py:43](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen17/train6.py:43)
- **“8–12 talkers” means source draws with replacement.** The frozen crowds contain **3–12 distinct speaker identities**. Describe that accurately; changing to distinct-speaker sampling would change the registered material. [train10.py:112](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:112)
- **Fresh-checkout robustness:** create `weights/` before saving. It exists locally but is absent from tracked files, and neither builder nor pipeline creates it. [interp.py:44](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen26/interp.py:44)

**Validity checks passed:**

- All registered source hashes and six endpoint hashes match. All three R48 parent hashes match their same-seed Gen19 finals; schemas match, with 181 finite float32 tensors each. The builder implements the fixed CPU midpoint and checks suffix invariance before saving.
- Rebuilt **512 items** and reproduced material hash `557ad44f…`. Confirmed **8F/8M**, training disjointness for both endpoints across all seeds, and reserve exclusion.
- Panel grid/hash checks correctly reject missing, duplicate, wrong-speaker and mismatched-hash rows. The self-test reproduces **zero gain, A1–A3 FAIL, A4/S1–S3 PASS**.
- Bootstrap implementation is correct: paired differences → per-voice means → 10,000 resamples of 16 voices → 2.5th/97.5th percentiles. **Equal item weighting equals equal voice weighting** because every voice contributes 16 items per SNR.
- **S3 matches the earlier judge for finite values:** it uses bench v2’s existing item-bootstrap CIs against unprocessed, distinct from A2’s voice bootstrap against Gen19.
- **Crowd construction creates no within-mixture target leakage:** the target speaker is excluded, and both systems receive identical mixtures. Shared interferer identities nevertheless couple target groups; interpret A2 as conditional on this fixed crowd construction, not full uncertainty over independently sampled target and interferer populations.
- **Gen19’s +2.385 versus +1.060 dB changes no threshold or verdict.** Different targets and crowd recipes prevent treating that difference as model improvement. Carry the existing disclosure into reporting; neither number establishes Gen26 improvement or the original KPI.

## Disposition (Claude Opus 5.5, 2026-11-04 ~21:15)

**Gen 26 is SHELVED, not run.**
- The holder redirected the research toward real-world benefit for
  cochlear-implant users and away from score tweaks. A weight blend of two
  existing models is a score tweak.
- No Gen 26 candidate was ever built or evaluated.
- Blocking item 1 (the verifier accepting the wrong endpoint pair) is
  therefore moot for now. It must be fixed before Gen 26 could ever be
  revived.

**Screen v2 blocking items 2 and 3: fixed** in `judge_v2.py` before any
candidate.
- S3 is NaN-safe.
- Bench coverage is enforced.
- The self-test still gives zero gain: FAIL on A1–A3, pass on A4/S1–S3.

**Non-blocking items adopted in `screen_v2/prereg.md`:**
- the "unused" wording corrected (the voices are fresh for the Gen 19
  lineage; they were in the Gen 13–17 training pools);
- "8–12 source draws with replacement (3–12 distinct identities)";
- A2 described as conditional on the fixed crowd construction.

**Still open:**
- the confirmation aggregator, to be frozen before any confirmation
  result;
- the reserve-voice procedure.
