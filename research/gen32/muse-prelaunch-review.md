# Muse (Meta) pre-launch review of Gen 32 — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~02:14.
> - It received the registration text inline (Muse has no file access) and was asked to judge the design only.
> - Disposition: see [astra-prelaunch-review.md](./astra-prelaunch-review.md). The dry-share wording is clarified in the prereg. The zero-margin rule is kept, per the Gen 31 disposition.

## Verbatim answer

**CLEARED FOR LAUNCH**

Blocking items: none.

- Real CI-user risk: T0 in-silico only, `promoted FALSE`, same-seed Gen 19 comparator, conservative dry-gate. No human exposure, no clinical claim.
- Leakage: none found in design. Teacher is frozen detached Gen 19 seed-17; calibration uses 100 fresh training-stream batches only, no VAL/screen material; VAL panel/material hash unchanged; 24 reserved voices stated untouched; NO CANDIDATE touches no screen material.
- Arithmetic checked: 100 x 0.0061 = 0.61 loss units. If main loss is -SI-SDR in dB, 0.61 units ~= 0.61 dB. Stated ~0.6 dB vs mean -10.1 dB is mathematically consistent. Neither negligible nor dominating claim holds on that scale.
- Test coverage for zero-penalty, teacher-no-grad, dry-mask, bit-identical batches is adequate for design review; hash/code left to other reviewer.

Non-blocking notes:
- Single fixed 100 + zero-margin dry rule remains inefficient. Prior -0.00003 STOI miss suggests noise-dominated gating; repeat NO CANDIDATE likely. Does not create false ADVANCE, only wasted run.
- Soft raw MSE with no gain fitting mismatched to SI-SDR loss and STOI gate; may penalize inaudible gain while missing STOI regression. Acknowledged as non-guaranteeing.
- 432/800 = 54% dry items vs "aug50 (45/45/10)" description unclear; clarify dry fraction definition.
- Retain pre-stated expectation: NO CANDIDATE possible, R1a >=+0.30 dB uncertain.
