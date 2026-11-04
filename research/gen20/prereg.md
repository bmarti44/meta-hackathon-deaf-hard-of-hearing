# Gen 20 pre-registration — babble-k distribution, paired continuations

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Written before training; amended 2026-11-04 per Astra Gen19
> review disposition ([../gen19/astra-review-gen19.md](../gen19/astra-review-gen19.md)),
> still before any Gen20 training.

## Hypotheses

H1: the −5 dB crowd shortfall partly reflects training k mass
wasted on low-k/competing-like mixtures. H2: concentrating k on
8–12 improves crowd ΔSI-SDR at −5 dB by ≥0.3 dB (VAL) without
worsening VAL −5 dB ΔSTOI.

## Frozen design (per Astra training-strategy step 2)

Paired 12,000-step continuations from the SAME validated Gen19
seed-1 parent (`causal_seed20261117.pt`), identical reproducible
optimizer protocol per branch: fresh Adam, 250-step warm-up
3e-5→3e-4, cosine→3e-5, clip 5, batch 8×2 s, train-clean-100,
arch/loss/SNR mix frozen. A: legacy k~U{2..12} (control).
B: 80% k8–12 / 20% k4–7 (no k2/3). VAL acceptance B vs A:
≥+0.3 dB at −5 dB, ΔSTOI not worse. If accepted, B is retrained
from scratch (24k) before any bench claim; continuations alone
make no KPI claim. Judged on final checkpoints.

## Amendment (Astra disposition, pre-launch)

- **Continuation seed 20261120**, shared by both arms (the parent
  seed replayed parent mixtures in arm A — Astra verified four
  bit-identical batches). Per-example purpose-isolated substreams:
  arms share clean targets, SNRs, quiet/SSN choices and the
  interferer prefix; only k differs. Tested in test_train9.py.
- Branch-specific outputs `legacy_seed20261120.pt` /
  `crowd80_seed20261120.pt`; checkpoints record branch, parent
  hash (`80000b64…f367`), continuation seed, schedule.
- **Safeguards:** B−A at 0 dB (VAL) no worse than −0.15 dB
  SI-SDR / −0.003 STOI; quiet read on bench v2 finals
  (abs ≥25 dB, ΔSTOI ≥−0.02) before B advances.
- Report **A−parent and B−parent** (VAL step 0 = parent). A B
  "win" caused by A deteriorating is not an absolute improvement
  and does not advance B.
- Rank after Gen20 (Astra): if B accepted → 24k from-scratch
  crowd80 ×3 seeds; then 48k on the retained recipe; then
  compressed-spectral → SNR → STOI auxiliaries.
