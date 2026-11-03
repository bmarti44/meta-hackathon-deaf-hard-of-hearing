# Gen 14 summary — no lever moves babble; J4 recipe family closed (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Date: 2026-11-03. Source: [results.md](./results.md),
> executing the [Gen 13 Next gate](../gen13/Gen13-summary.md).
> **Eval independently re-run for this summary** (below).
> Status unchanged: J4 `promoted FALSE`, validation set 0.
> Everything here is **T0, in-silico. No listener-benefit
> claim is made or implied.**

## Independent re-run

```text
/tmp/gen9env/bin/python research/gen14/train3.py fulleval
→ FULLEVAL rc [0,0,0,0], wall 49 s; fulleval_summary.json
  parsed-identical to filed version
/tmp/gen9env/bin/python research/gen14/train3.py quickeval
  --weights …/C{0,1,2,3}_seed20261113.pt
→ quickeval.json parsed-identical to filed version
/tmp/gen9env/bin/python research/gen14/train3.py causality
  --weights …/C{1,2}_seed{20261113,20261114}.pt
→ prefix 123 frames, max|dmask| = 0.0, all 4 final checkpoints
```

Exact reproduction is expected (fixed eval RNG, filed
checkpoints). It verifies filed numbers are what filed code +
weights produce, not that they generalise. Training was
**not** re-run here.

## Did any lever move babble? No

Architecture is Gen 11 J4-A1 imported exactly unchanged
(238,656 params). Levers: (a) scale-invariant envelope
SI-SDR loss, (b) babble k=2–8 + SNR curriculum to −5…+15 dB,
(c) compressed-magnitude `IRM^0.5` target (decompressed
at inference; a true complex IRM is impossible in this
envelope-only arch), (d) cosine LR to 2e-5 — bundled
with (b), never isolated. Screen: C0 Gen 13 control,
C1 a+b+d, C2 a+b+c+d, C3 b+d; 700 steps, seed 20261113.
Pre-registered top-2 redesign configs (C2, C1) got seed 2.
Gate, stated in advance: seed-mean babble ΔSI-SDR 95% CI
excluding 0 = signal.

| Config | Screen babble ΔSI-SDR (1 seed) | Final babble, seed-mean [95% CI] |
|---|---|---|
| C0 control | +0.04 | — (not selected) |
| C1 a+b+d | −0.01 | **−0.01 [−0.04, +0.02]** |
| C2 a+b+c+d | +0.07 | **+0.06 [−0.01, +0.12]** |
| C3 b+d | −0.10 | — (not selected) |

All four screen values lie within 0.17 dB of zero and the
control ranks second. Ablations are noise-scale:
(a) +0.09, (c) +0.07, (b)+(d) −0.13 dB. Neither final CI
excludes 0 against an unchanged **+7.5 dB oracle gap**
(unprocessed/oracle 2.47/9.99 dB): the representation can
express a better babble mask; none of these recipes finds
it. SSN is retained only where the model did not collapse
(C2 +3.30 dB, both seeds); held-out white still fails
(C1 −0.13, C2 −0.76 dB).

The one actionable finding is a harm, not a gain: the
scale-invariant envelope loss (a) has a constant-mask
degenerate optimum. C1 seed 2 collapsed to mask ≈0.515
everywhere (within-crop std 0.001; SSN ΔSI-SDR +0.005 vs
+2.42 for seed 1), and C1/C2 quiet masks sit at ~0.54–0.58
(Gen 13: 0.90), a real level error on the ACE envelope
path that scale-invariant readouts hide. Lever (a) as
specified is harmful to calibration, not merely null.

## J-lineage verdict: closed, via no config

**No Gen 14 config keeps the J lineage alive.** Per the
pre-stated gate, the recipe family — mask-MSE ±
scale-invariant envelope loss, IRM or compressed-IRM
targets, babble pools to k=8 with SNR curriculum, lower
final LR — is **closed at screen scale**, and with
Gen 13 (more steps closed) the training-recipe axis
around the current target representation is exhausted.
C2 is the least-bad checkpoint (best babble point
estimate, SSN intact) but its CI includes 0, its STOI
delta is negative, and white/quiet fail: it earns no
listener time and is not a promotion candidate.

Closure caveats, all from [results.md](./results.md):
700-step screen, not 3000 — leans on Gen 12→13
step-invariance of the babble readout; (d) bundled, not
isolated; CIs cover 32 crops from 2 held-out speakers,
not a speaker population; a *level-aware* (non-scale-
invariant) envelope loss is a different, untested lever
and is **not** covered by this closure.

## Next

| Step | Owner | Note |
|---|---|---|
| New design decision, not a Gen 14 continuation: different training-signal class (level-aware envelope objective, discriminative/contrastive talker-separation signal), different noise-world (recorded multi-talker scenes, not synthetic sums), or representation change | Machine, after holder picks the axis | Any candidate must first pass the same T0 gate: seed-mean babble ΔSI-SDR CI excluding 0, without breaking quiet identity or held-out noise classes |
| Listener work (vocoder SRT, Stage 0/1/2) | Human / lab | Unchanged and not advanced: no Gen 12–14 checkpoint has earned listener time; only reconsider after a T0 babble gain exists |

The generation's gain: four named levers were screened
against a pre-stated gate at T0 cost, all read null on
babble, and one (scale-invariant envelope loss) was shown
actively harmful — before any listener time was spent.
