# Gen 20 pre-registration — babble-k distribution, paired continuations

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Written before training; Astra Gen19 review pending (rate limit
> until ~1:35 AM) — launches wait for its disposition.

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
