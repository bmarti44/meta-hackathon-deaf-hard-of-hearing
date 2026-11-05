# Astra xhigh pre-launch reviews of Gen 35 — verbatim + dispositions

## Review 1 (2026-11-05 ~04:14–04:22 EST, 64,594 tokens): NOT CLEARED

**NOT CLEARED**

1. **V0 can pass incomplete data.** Counts do not establish unique, complete coverage; indexing silently collapses duplicates. Synthetic checks returned **REPAIR ACCEPTED** with a missing P2 item, the entire P5 high level missing, or P7 silence missing, replaced by duplicates. Validate exact expected keys, uniqueness, required metrics and matching arms before judging. [judge_repair.py:39](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/judge_repair.py:39)

2. **The engineering rule is narrowed.** R2 ignores P3 and P5 waveform errors—I confirmed acceptance with both arbitrarily worsened. R3 omits noisy spatial item-ear scores; R5 checks clipping only in P1/P5 and delay only in P1. Extend the applicable checks across the registered conditions. [judge_repair.py:59](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/judge_repair.py:59)

3. **Export coverage is insufficient.** P7 has no sign-only comparator, noisy panels or speech-to-silence transitions, and cannot veto acceptance. Its only waveform-error measure rescales the reference using each output’s standard deviation, hiding gain errors. Audit the applicable conditions through the exported path, apply the relevant gates separately, and report unadjusted error against the correctly scaled reference. [run_repair.py:122](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/run_repair.py:122)

4. **Checkpoint polarity binding is incomplete.** Seeds 18/19 inherit polarity by filename and then receive whatever hash those files currently have; only seed17 has a pinned hash. Freeze all three SHA→polarity mappings, reject mismatches, and validate provenance in V0. [repair.py:36](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/repair.py:36)

Non-blocking notes: All **15 hashes match**; **5 tests pass**. A0 parity, identical A1/A2 flushing, and bias subtraction before RMS restoration are correct; subtraction commutes with the pure delay crop. Correct “Every registered metric is blind to both”—waveform error is sensitive. No audit scoring was launched.

### Disposition 1 (Claude Opus 5.5, ~04:45)

All four blocking items and the wording note are fixed before any repaired
output was scored, in pre-launch amendment 1 of [prereg.md](./prereg.md):
- strict V0 (exact keys, uniqueness, metrics, matched arms, provenance);
- full rule coverage;
- a gated export path with a sign-only arm and unadjusted waveform error;
- the frozen sha → polarity table for all three seeds.

Her attacks are reproduced as tests. The fixes go back to Astra for verification.

## Review 2, verification of amendment 1 (2026-11-05 ~04:23–04:26 EST, 54,092 tokens): NOT CLEARED

**NOT CLEARED**

- **P1 labels still bypass gates.** Relabeling a target-only A2 row as `noisy` allowed negative polarity, +100 dB waveform error and an 80-sample lag to receive **REPAIR ACCEPTED**. Validate `cond` against `snr` across arms and derive gate applicability from registered keys. [judge_repair.py:87](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/judge_repair.py:87)
- **V0 ignores unexpected seed/arm groups.** Adding an unregistered seed or arm with null required metrics still received **REPAIR ACCEPTED**. Reject unexpected groups before evaluating completeness. [judge_repair.py:76](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/judge_repair.py:76)

### Disposition 2 (Claude Opus 5.5, ~04:55)

Both items are fixed in pre-launch amendment 2. Gate applicability is now
derived from the registered key, with labels validated, and unregistered
groups are rejected. Both attacks are tests. The fixes go back for
verification.
