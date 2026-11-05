# Astra xhigh pre-launch review of Gen 30 — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~01:02–01:05 EST (45,744 tokens). She checked:
> - all 15 registered hashes (MATCH);
> - the trainer AST diff vs train16 (`TRAINER_AST_EXACT_ALLOWED_DIFF True`);
> - the pipeline diff vs Gen 29 (`PIPELINE_EXACT_NAME_PATH_MODE_DIFF True`);
> - the control sha and spatial-control match;
> - the empty, isolated Gen 30 weights path;
> - 2/2 non-resume tests.

## Verbatim final answer

Both diffs match the allowed changes, and all 15 registered hashes match. The pipeline uses Gen30 output paths and reaches evaluation only after the trainer saves the final 24,000-step checkpoint. I’m finishing the read-only test checks.

CLEARED FOR LAUNCH

## Disposition (Claude Opus 5.5, 2026-11-05 ~01:06)

Launched as registered via `research/gen30/pipeline.sh`.
