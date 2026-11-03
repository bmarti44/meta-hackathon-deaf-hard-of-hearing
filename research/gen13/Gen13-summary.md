# Gen 13 summary — more babble training does not create a babble gain; ACE-sim confirms the null (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`.
> Date: 2026-11-03. Source: [results.md](./results.md) with
> [eval_results.json](./eval_results.json), executing the
> [Gen 12 Next gate](../gen12/Gen12-summary.md).
> **Eval independently re-run for this summary** (below).
> Status unchanged: J4 `promoted FALSE`, validation set 0.
> Everything here is **T0, in-silico. No listener-benefit
> claim is made or implied.**

## Independent re-run

```text
/tmp/gen9env/bin/python research/gen13/eval2.py --n-per-cell 8
→ EVAL DONE 52s, 104 paired crops × 3 seeds; output bit-identical
  to filed eval_results.json (cmp equal, SHA-256 4afad265…fd67bd)
weights SHA-256 dc57333e… / d61aa478… / 567e6b69… match results.md
```

Exact reproduction is expected (eval RNG 777, same
`/tmp/gen12dl` corpus). It verifies the filed numbers are what
the filed code + weights produce, not that they generalise.
Training was **not** re-run here.

## Does a babble gain appear with babble training? No

Framing correction first: babble was already 70% of noisy
training items in Gen 12. Gen 13 is not a first exposure — it
is the Gen 12 recipe at 4× budget (750 → 3000 steps, unchanged
[J4-A1 architecture](../gen11/j4_model.py), 238,656 params),
3 seeds, broader babble (talkers k ~ U{2,3,4}, train speakers
only). Eval babble uses held-out interferers 8842/8297; white
noise is a wholly held-out class. Δ = J4 − unprocessed, paired
32 crops/condition, 95% bootstrap CIs over crops:

| Condition (seed-mean) | ΔSI-SDR dB | ΔSTOI | vs Gen 12 |
|---|---|---|---|
| SSN (trained) | **+4.02 [+3.55, +4.48]** | +.042 | was +3.31 |
| Babble, held-out spk | **−0.12 [−0.34, +0.12]** | −.006 | was −0.12 |
| White, held-out class | **−2.65 [−3.14, −2.16]** | −.045 | was −1.03 |

All 3 seeds agree in sign in every cell. The babble point
estimate is numerically identical to Gen 12 despite 4× steps
and broader mixtures, while the oracle mel-IRM reaches
9.99 dB (unprocessed 2.47) — the representation can express
a better babble mask; this training recipe does not find it.
Longer training on the same pool entrenched class
specificity: SSN improved modestly, held-out white got
*worse*. More steps of the same recipe is a closed lever.

## ACE-sim verdict

[ace_sim.py](./ace_sim.py) prices J4's native mel envelopes
as an ACE-like processor would consume them (22 channels,
8-of-22 maxima, no waveform synthesis; cited vs ASSUMED
parameters in its docstring). Seed-mean Δ vs unprocessed:

| Condition | Δ env. corr. | Δ channel-SNR | Δ maxima overlap |
|---|---|---|---|
| SSN | +.131 [+.092, +.172] | +4.53 dB | +.053 |
| Babble held-out spk | −.014 [−.023, −.006] | +0.55 dB | +.004 |
| White held-out | −.125 [−.152, −.100] | −2.11 dB | −.022 |

The ACE readout sharpens, and does not soften, the waveform
null. In babble the mask removes some noise energy
(channel-SNR +0.55 dB) but slightly *degrades* envelope
fidelity to clean speech and barely changes which channels
would be stimulated. Energy suppression without envelope
fidelity is not a plausible substrate for listener gain —
an engineering reading, not a perception claim. SSN is the
only condition positive on every ACE metric.

## Honest T0 limits

- **No listener evidence of any kind.** No SRT, intelligibility,
  power, latency, or on-processor data. ACE-sim is deliberately
  crude: ASSUMED band edges, no AGC or T/C loudness mapping,
  no current spread or neural model, 250 frames/s vs 900 pps.
  It cannot rank perceptual outcomes.
- CIs cover eval-crop sampling only: 32 crops/condition from
  **2 held-out target speakers**. They are not
  speaker-population CIs. Seeds vary training RNG only.
- Waveform SI-SDR/STOI/PESQ pass through a T0-only
  noisy-phase OLA reconstruction; J4 emits no waveform.
- Untested, none assumed to help: loss/objective change,
  LR search, broader noise pool, babble-specific curriculum.
  What might fix babble remains unknown.

## Next

| Step | Owner | Note |
|---|---|---|
| Different training signal/objective or noise-pool design, screened at T0 for a babble gain first | Machine | The Gen 12 gate still binds: no Gen 13 checkpoint earns listener time on a T0 babble null. More steps of this recipe is ruled out by this generation |
| Normal-hearing vocoder *listening* study (SRT/intelligibility, J4 vs unprocessed vs oracle, counterbalanced, preregistered) | **Human** — design, ethics, recruitment, running | Only earns its cost **after** a T0 babble gain exists. A T3 proxy per [protocol.md](../gen00/protocol.md): vocoder ≠ CI biology; screens "could a listener use this mask at all", nothing more |
| Stage 0 bench, then Stage 1/2 listener SRT vs SCAN 2 | Lab / human subjects | Unchanged; no Gen 13 result moves these closer |

The generation's gain: the "just train longer with babble"
hypothesis is now tested at 3 seeds with CIs and an
ACE-consumption readout — and is refuted cleanly, at T0
cost, before any listener time was spent.
