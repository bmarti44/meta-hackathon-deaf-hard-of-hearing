# Gen 16 — multi-term loss does not beat Gen 15 (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-03.
> Same architecture/protocol as Gen 15; only the objective changed:
> neg SI-SDR + 5·ACE log-envelope MAE (pre-selection) + 5·waveform L1.
> One seed (20261116), 2000 steps. Benched on bench-n6 (n=16/condition):
> [bench_results_gen16.json](../bench-n6/bench_results_gen16.json).
> T0 only, no listener claim. `promoted FALSE`.

| Babble (held-out) | Gen 15 final | Gen 16 final |
|---|---|---|
| ΔSI-SDR dB | +1.07 [+0.57, +1.59] | +0.93 |
| ΔSTOI | −0.016 | −0.033 |
| ΔACE electro-corr | +0.011 [−0.004, +0.027] | +0.003 |
| ΔSI-SDR @ −5 / 0 dB | −0.05 / +1.25 | −0.27 / +1.27 |

Elsewhere: SSN +4.23 dB, white +1.22 dB, quiet abs SI-SDR 24.9 dB —
comparable to Gen 15. Spatial screen (4 scenes): ILD distortion
1.06 dB per-ear, target-ILD error 5.47 dB — no spatial change.

**Verdict:** the Gen 16 objective change is a null-to-slightly-negative
result on every babble KPI. Consistent with the independent review
([REVIEW.md](../../REVIEW.md) §1.4): the log-envelope MAE with a 1e-6
floor spends weight on near-silent bands a processor never
stimulates, and it is pre-selection while the gate is post-selection.
Training loss terms are in `weights/train_log_seed20261116.json`
(ace_env_loss ≈0.43–0.49 late in training; it optimized its term
without moving the gated metrics).

**Next (per REVIEW §3, holder-approved split):** Phase 0 bench v2
(crowd vs competing-talker babble, more held-out speakers, ESTOI/NCM
on vocoded output, MPS training), then Gen 17 = data scale with the
Gen 15 recipe as control. The eval-babble target-ambiguity diagnosis
(REVIEW §1.1: k=3 from only 2 interferer voices; at −5 dB each
interferer ≈ target loudness) is accepted and drives the split.
