# Muse (Meta) pre-launch review of Gen 31 — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~01:20.
> - Muse has no file access. A first call that pointed to repo files returned "Need repo files to verify — no tool access provided in this turn."
> - It was re-asked with the full registration text inline, and asked to judge the design only. Astra did the hash and code checks.
> - Disposition: see [astra-prelaunch-review.md](./astra-prelaunch-review.md).

## Verbatim answer

CLEARED FOR LAUNCH

Blocking items: none.

1. Sound single-method test: yes. One parent (Gen19 seed-17, enforced), one 8k-update fine-tune final-checkpoint-only, one 10-point blend grid, one dry-VAL rule to pick single alpha*, one judge_v3 run vs same-seed Gen19. No checkpoint / endpoint / alpha cherry-picking. Fail-safe: NO CANDIDATE if alpha=0.1 fails, no screen touched.
2. Leakage screen->selection: none. Selection uses only test-clean VAL, asserted disjoint from all training / TEST / screen lists, 24 speakers reserved untouched. Fine-tune uses train-split RIR `f306700d…`, continued RNG handoff. Screen judged once on alpha* only. Full VAL curve + train log reported descriptively only.
3. aug50 + prefix rule: keep both as registered. Do not change before launch.
 - aug50 45/45/10: coherent for WiSE-FT - maximize FT room signal because blend will dilute it; dry cost is what blend is for. Single pre-fixed choice avoids dose-tuning.
 - prefix alpha* = largest alpha with all <=alpha passing on all 4 dry d>=0: sensible anti-cherry-pick. Prevents rescuing dip with noisy later pass. Strictness (-0.002dB fails in smoke) errs to NO CANDIDATE / FAIL, not false ADVANCE. Final dry safety still in judge D bounds.
Arithmetic: 16 targets x4 crops x4 crowds x2 SNRs =512 items correct.

Non-blocking notes:
- VAL d>=0 with no margin has ~50% false-fail at true zero, plus prefix compounding. Cost is power / NO CANDIDATE rate, not safety. Acceptable for T0.
- Grid 0.1 coarse, blend uniform over 181 tensors, assumes monotonic room-vs-alpha. Room not used for selection; zero-room blend just fails R1a>=0.30dB. Safe.
- Seed 20261131 is non-calendar but valid as integer; keep exact.
- Future seeds 18/19 + reserved-voice confirmation out of scope for this T0 clearance.
