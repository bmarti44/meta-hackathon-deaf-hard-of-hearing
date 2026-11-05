# Astra xhigh pre-launch review of Gen 31 — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~01:12–01:16 EST (112,521 tokens).
> She verified:
> - all 17 registered hashes;
> - the archive md5/sha256 and the rebuilt VAL material hash;
> - 4 read-only tests.

## Verbatim final answer

**CLEARED FOR LAUNCH**

Blocking items: none for the seed-17 T0 experiment, **only after Gen30 returns FAIL**. The pipeline does not enforce that prerequisite.

Non-blocking notes:

- **Sound scope:** one fixed fine-tune/blend/selection procedure, with unchanged causal architecture and one final screen. It tests this recipe; failure would not disprove WiSE-FT generally. Passing would justify further research, not establish better hearing or universal preservation for CI users. Objective metrics still require [listener validation](https://pubmed.ncbi.nlm.nih.gov/38501923/).

- **No selection leakage found:** VAL targets and interferers are separate from earlier lists; reserved voices remain unused. Alpha selection consumes no screen scores or room material. Previous generations’ screen feedback informed the hypothesis, so the reused screen remains developmental; fresh confirmation matters.

- **Keep the prefix rule and aug50 unchanged.** The prefix is conservative and correctly implemented, including nonfinite rejection and NO CANDIDATE. Aug50 is a defensible fixed hypothesis. However, neither stronger augmentation nor larger alpha guarantees greater room benefit; soften that certainty in the rationale. No tolerance or finer-grid rescue should follow a failure.

- **Verification:** all 17 registered file hashes match, as do archive MD5/SHA256 and the rebuilt VAL material hash. Four read-only checks pass, including blend endpoints, prefix selection, voice separation and scratch-batch equivalence. I did not rerun the writing/training smoke.

- **Correct the smoke description:** the saved curve is **not −0.002 dB at every alpha**. At α=0.1, SI-SDR changes are approximately −0.000112/−0.000032 dB at −5/0 dB; approximately −0.002 occurs at α=1. NO CANDIDATE remains correct. Update [prereg.md:85](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen31/prereg.md:85).

- Before replication, add registered seed-18/19 parent hashes: `GEN19_SHA` currently permits only seed 17.

## Disposition (Claude Opus 5.5, 2026-11-05 ~01:35)

CLEARED; all non-blocking notes are adopted as a dated pre-launch
amendment in [prereg.md](./prereg.md):
- the pipeline now enforces the Gen 30 FAIL prerequisite;
- the aug50 rationale is softened;
- the smoke description is corrected;
- seed-18/19 parent hashes will be added before any replication;
- no tolerance or finer-grid rescue will follow a failure.

The prefix rule and aug50 are kept, as both reviewers advised. Gen 31
launches only after Gen 30 returns FAIL.
