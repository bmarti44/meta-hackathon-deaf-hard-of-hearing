# Gen 26 pre-registration — fixed weight-space midpoint of Gen 19 and its Gen 21-R48 continuation

> Claude Opus 5.5, 2026-11-04 ~21:10 EST. Astra's Gen 25 roadmap, rank 2.
> Her Gen 25 result review approved it, conditional on screen v2 being
> frozen first. Written before any candidate is built. T0 only.
> `promoted FALSE`.

## Question

Does a fixed blend halfway between Gen 19 and its own 24k-step
continuation (Gen 21-R48) beat Gen 19 at −5 dB on the screen v2 panel?

R48 improved the easier conditions but lost at −5 dB on the bench. The
midpoint tests whether part of the continuation's gain can be kept
without that loss (WiSE-FT-style).

## The one change (no training, no selection)

`research/gen26/interp.py --seed S` computes θ = 0.5·θ_Gen19 + 0.5·θ_R48
for the same seed. α = 0.5 is fixed: **no α sweep, no endpoint
substitution, no alternative after the result.**

Guards:
- both inputs match `input_manifest.json` (6 hashes);
- R48's recorded parent is this seed's Gen 19 final (verified for all 3
  seeds);
- schemas match;
- exact causality is re-verified.

`verify_g26.py` re-derives the midpoint bit-exactly.

## Judgment

Screen v2 ([../screen_v2/prereg.md](../screen_v2/prereg.md)) on seed 17,
then 3-seed confirmation only if it ADVANCEs. Run:
`research/gen26/pipeline.sh 17`.

**Expectation:** R48's −5 dB losses suggest a midpoint is unlikely to gain
+0.30 at −5 dB. That is stated in advance, and a FAIL is filed as a null.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `gen26/interp.py` | `26aaa5e54220dd52de3dfcb933e0711d825426e4bff625fbe143b4c57ff35033` |
| `gen26/verify_g26.py` | `ba13257ffce2d68a0a501ae84bd5b0c642dbcaf0b8590691b685501a7bc2a7f1` |
| `gen26/pipeline.sh` | `460a1fadc5b11bf29dcf2aa33edfcde9fe86ad329d441d85bd909a2fe2bfd7ec` |
| `gen26/input_manifest.json` | `b724176d5648cd762448a5d43e130012569095ff6ab369411d440696897559e5` |
