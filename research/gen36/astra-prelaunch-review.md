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
