# Codex Astra review of the bench plan (2026-11-03)

Run: `codex exec -m gpt-6-astra -s read-only` (holder request).
Prompt: review PROTOCOL.md against bench code/results; brief and blunt;
no edits. Verbatim findings, disposition appended below each.

> 1. **The staging is sound; "proven" needs a narrow meaning.** Bench →
>    father's blinded vocoder screening → separately considered implant
>    work fits the stated direction. A father's screening win establishes
>    usefulness in that setup, not benefit for his son or superiority to N6.
>    Current results show **no convincing babble win**: the step-500
>    candidate gains **0.41 dB SI-SDR**, its envelope-correlation CI
>    crosses zero, and babble STOI slightly *declines*. Both causal
>    systems fail Stage B.

> 2. **Biggest over-engineering: making an unvalidated proxy an absolute
>    veto on cheap listening.** "No listening just to see" blocks useful
>    debugging. Worse, the purported ACE metric measures all 22 envelopes
>    **before** 8-of-22 selection; the vocoder actually applies selection.
>    And the protocol promises comparison against the classical baseline,
>    but the implemented gates compare only against unprocessed. Sixteen
>    babble crops from two target speakers cannot establish broad robustness.

> 3. **First change: separate debugging from evidence.** Permit a small
>    father-only pilot now, explicitly carrying no benefit claim. Include
>    clean-vocoded and oracle-vocoded controls to check whether the
>    screening setup has usable headroom. Keep blinded transcription on
>    fresh material as the evidence test. Then enforce comparisons against
>    **both** baselines, expand speakers and babble conditions, and report
>    results by SNR. Treat envelope correlation as supporting evidence
>    until validated. Verify the actual candidate's streaming causality
>    and measured latency — the bench's suffix-invariance test currently
>    covers only the classical gate.

## Disposition (same day)

- Post-selection metric: **done** — `ace_electro_corr` added; gate 2 now
  uses it. Pre-selection corr retained as supporting readout.
- Both-baseline gate: **done** — candidate must also beat the classical
  gate's babble SI-SDR.
- Pilot vs evidence: **done** — PROTOCOL amended; `--allow-unpassed`
  shakedown pack built (72 items incl. oracle control), labeled
  non-evidence.
- By-SNR reporting: **done** in results.md from filed rows.
- Candidate causality/latency: already proven in
  `research/gen15/model_causal.py` (exact suffix test, 5.88 ms
  algorithmic latency excl. compute); bench does not duplicate it.
- More speakers/conditions: **not done** — recorded limit (2 target
  speakers) stands until a candidate passes; widening the bench before
  then is effort in the wrong place.
