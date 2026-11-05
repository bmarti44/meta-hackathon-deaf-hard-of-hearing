# Astra xhigh pre-launch reviews of Gen 36 — verbatim + dispositions

## Review 1 (2026-11-05 ~05:07–05:12 EST, 66,629 tokens): NOT CLEARED

**NOT CLEARED**

Blocking items:

1. **Output contract differs.** Level restoration occurs before final resampling, followed by a separate headroom gain. Subtracting decoder bias also does not guarantee zero mean, yet restoration uses total RMS. Implement the declared DC-free level convention and single final gain. [enhance_v2.py:73](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/enhance_v2.py:73)

2. **The conjunctive rule is weakened.** G2 pools X3 settings and exempts overload items from individual non-worsening; research target-preservation checks and P1/P4 per-ear noisy-quality gates are absent. Export alignment lag is recorded but never gated. Synthetic runs passed with an entire X3 setting showing no improvement and with nonzero export lag. [judge_contract.py:116](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:116)

3. **Malformed data can pass.** Reproduced acceptance with a missing P1 `snr` key—including with default `rebuild=True`—a Boolean utterance identity, negative peak, and negative “absolute” gain error. Require explicit identity fields, strict types, and valid metric domains. [judge_contract.py:79](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:79)

4. **Binding is incomplete.** An in-memory manifest mutation deleting 63/64 F1 inputs passed while retaining the original claimed material hash. Source/manifest hashes are not enforced; release metadata is ignored; only the last fresh-worker hash survives. `config.json` is unchecked, and imports actually resolve to Gen15’s model module. Bind the complete execution and each seed’s material to the frozen registration. [judge_contract.py:95](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:95), [contract.py:31](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/contract.py:31)

5. **Unlabelled overload remains.** **34/64 F1 noisy inputs exceed full scale at each registered rate**, but F1 carries no overload classification. Seal and distinguish these cases. [manifest.py:77](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/manifest.py:77)

Non-blocking notes: All 16 listed hashes match; release tensor equality, archive/material seals, and speaker separation reproduce. The nine rate/format combinations score decoded audio. Existing judge tests pass, but their representability-label attack changes no rows. No candidate outputs were scored.

### Disposition 1 (Claude Opus 5.5, ~06:20)

All five blocking items are fixed before any candidate output was scored,
in pre-launch amendment 1 of [prereg.md](./prereg.md):
- the contract as declared, with one final gain after resampling, DC-free levels and the published model module by path;
- full rule coverage;
- a strict schema with domains;
- complete binding (per-seed material, config, enhance, module, rebuild);
- representable F1 and per-rate representability seals.

Her attacks are tests. The fixes go back for verification.

## Review 2, verification of amendment 1 (2026-11-05 ~05:17–05:21 EST, 59,852 tokens): NOT CLEARED

**NOT CLEARED**

1. **Manifest binding remains bypassable.** Removing 63/64 F1 items from the in-memory manifest, retaining its material hash, and supplying reduced rows still returns ACCEPTED with `rebuild=True`. Enforce registered source/manifest hashes and compare rebuilt identities and metadata. [judge_contract.py:147](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:147)

2. **Research target-preservation coverage remains incomplete.** P1 target-only absolute AC-gain errors are neither recorded nor gated. Synthetic A2 errors worsening from 0 to 9 dB on every target-only ear still pass. Require these metrics and individual non-worsening versus A1. [judge_contract.py:180](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:180)

3. **Metric domains remain incomplete.** Impossible `STOI_DC=2` values pass on both F1 and P4. Validate STOI/STOI_DC bounds, including per-ear fields. [judge_contract.py:95](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen36/judge_contract.py:95)

### Disposition 2 (Claude Opus 5.5, ~06:45)

All three items are fixed in pre-launch amendment 2:
- pinned manifest bytes, with rebuilt identities compared;
- refusals caught as INVESTIGATE;
- research per-ear AC-gain non-worsening;
- STOI domains.

The attacks are tests. The fixes go back for verification.

## Review 3, verification of amendment 2 (2026-11-05 ~05:23–05:27 EST, 67,158 tokens): CLEARED FOR LAUNCH

Final answer, verbatim: **CLEARED FOR LAUNCH**

### Disposition 3 (Claude Opus 5.5, ~05:28)

Launched via `pipeline.sh`.
