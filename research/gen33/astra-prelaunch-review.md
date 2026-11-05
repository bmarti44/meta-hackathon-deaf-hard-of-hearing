# Astra xhigh pre-launch reviews of Gen 33 — verbatim + dispositions

## Review 1 (2026-11-05 ~02:51–03:00 EST, 62,098 tokens): NOT CLEARED

**NOT CLEARED**

1. **L4 accepts incomplete evidence.** In [judge_link.py:36](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen33/judge_link.py:36), dictionaries silently collapse duplicates, and subsets use whatever candidate rows remain. Synthetic checks changed **REJECTED → LINKAGE FEASIBILITY PASSED** after removing one failing noisy or target-only row. Validate complete, unique grids and matching metadata for candidate and both controls before constructing dictionaries: 16 scenes per condition, two per noisy subset, eight per target-only direction.

2. **SI-SDR differs materially from the established metric.** [spatial_linked.py:31](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen33/spatial_linked.py:31) omits mean removal used by the existing benchmark. One independent Gen32 target-only ear scores **−7.832 dB**, versus **44.054 dB** using the established implementation. Restore that implementation before evaluating L4, then update registered hashes.

Non-blocking notes:

- Shared-mask inference matches the design; references, delay alignment, trimming, STOI and cue calculations are sound. L1–L4 arithmetic, strictness, both controls and subset definitions otherwise match.
- All **15 hashes match**. All four existing tests pass under default runtime; the file-writing test was exercised with in-memory I/O. Their coverage misses the blockers above.
- Pin thread settings for exact legacy reproduction: forcing one thread produced tiny numerical differences.
- Feasibility-only disposition is preserved. No linked scene evaluation was computed.

### Disposition 1 (Claude Opus 5.5, ~03:15)

Both blocking items are fixed before any linked output, in pre-launch
amendment 1 of [prereg.md](./prereg.md):
- `judge_link.py` validates complete, unique grids, metadata, metric
  presence and unprocessed-row agreement, and stops with INVALID
  otherwise (tested).
- Per-ear SI-SDR uses the established mean-removed implementation
  (tested).

The thread note is recorded. The fixes go back to Astra for verification.
