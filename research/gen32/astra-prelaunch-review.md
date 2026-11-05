# Astra xhigh pre-launch review of Gen 32 — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~02:13–02:20 EST (62,339 tokens).

## Verbatim final answer

**CLEARED FOR LAUNCH**

Blocking items: none for the registered seed-17 T0 experiment.

Non-blocking notes:

- Diffs match the registered preservation penalty, coefficient metadata/logging, per-item VAL retention, and necessary Gen32 pipeline paths. Selection and judgment remain unchanged.
- **All 21 registered hashes match**, including calibration inputs. Rebuilt VAL material hash matches. **Five read-only tests passed**; I did not rerun the writing smoke test.
- No coefficient or selection leakage found: calibration uses training speakers and training RIRs only; coefficient stays **100**. Alpha selection uses only the designated development VAL panel. Reserved voices remain untouched.
- The pipeline enforces Gen31’s null selection; independently recomputing its prefix result confirms **NO CANDIDATE**. Gen32 selection failure stops before screening. Output paths are distinct from Gen31 artefacts.
- Soften [the scale-check interpretation](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen32/prereg.md:40): **0.614 loss units** establishes numerical scale, not gradient balance, non-dominance, or an expected 0.6 dB improvement.
- Soft preservation and passing reused development panels cannot establish CI-user benefit or universal absence of harm. Keep the registered fresh confirmation and bypass comparisons.

## Disposition (Claude Opus 5.5, 2026-11-05 ~02:25)

CLEARED. The scale-check interpretation is softened in the prereg. The
fresh confirmation and the bypass comparisons stay registered. Gen 32 is
launched as registered.
