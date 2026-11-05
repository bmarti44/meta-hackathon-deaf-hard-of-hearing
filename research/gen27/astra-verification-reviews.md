# Astra xhigh verification reviews of Gen 27 (after the pre-launch review) — verbatim + disposition

## 1. Verification at b0300f0 (2026-11-04 22:10–22:14, 85,652 tokens)

**NOT CLEARED FOR LAUNCH.** Arrival correction is resolved, but two blocking validation gaps remain:

- **Spatial:** only crossed-scene unprocessed values are compared between candidate/control. I changed existing-bench candidate ILD error to 100 and its unprocessed baseline to 101, updating summaries; SP still passed. Validate existing baselines against control and corresponding crossed scenes. [judge_v3.py:309](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/judge_v3.py:309)
- **Replication:** seed-17’s `ADVANCE` label is trusted despite contradictory gates. A seed-17 gain of −0.2 with all three R1 gates false, followed by +1/+1, still returned `RETAIN`. Require seed-17 gates to pass and verify verdict/R1 consistency against cells. [judge_v3.py:376](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/judge_v3.py:376)

Registered hashes, all 1,048 RIR hashes, timing figures, and 30 read-only tests verified. Spatial-control reuse and pipeline judge arguments are valid.

**Disposition:** both gaps fixed in 2b548df (prereg S10).

## 2. Re-verification at 2b548df (22:16–22:18, 50,617 tokens)

CLEARED FOR LAUNCH
Both attacks succeed on the parent commit and return INVALID at `2b548df`.
Both targeted tests pass; S10 hashes match. No new blockers found.

**Disposition:** cleared. Gen 27 seed-17 training launches via `research/gen27/pipeline.sh` (sha registered in S9).
