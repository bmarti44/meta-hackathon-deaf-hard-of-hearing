# Astra xhigh review — disposition (2026-11-03)

Holder requested Sol 6.1 xhigh; route rejected ("not supported
when using Codex with a ChatGPT account", reproduced this day).
Fallback per holder's earlier approval: Codex `gpt-6-astra`,
reasoning effort xhigh, read-only. Findings and disposition:

1. **Scorecard didn't implement the KPI contract** (v2 KeyError;
   missing spatial silently PASS). FIXED: explicit babble-kind,
   INCOMPLETE-never-PASS, regression tests added.
2. **Spatial gate would reject perfect target recovery**
   (mixture-ILD deviation as damage). FIXED: gate is now
   target-ILD error vs clean; distortion diagnostic only.
   PROTOCOL/KPI/scorecard updated; regression test added.
3. **V2 filed run tested only 2 of 6 target speakers** (per-cell
   index restart at n=2). FIXED: global speaker counter;
   balanced n=6 re-run supersedes the first baseline.
4. **"NCM-simple" mislabeled** (raw-waveform Pearson, not NCM,
   not vocoded). FIXED: renamed band-env Pearson; prereg
   amended with date, not silently.
5. **KPI table mixed bench versions; causal claims overstated**
   ("objective is the bottleneck"). FIXED: wording softened to
   what one seed shows; Gen 16 conclusion = "this loss recipe
   showed no demonstrated improvement."
6. **Gen 17 design**: keep architecture/loss and 6000 steps, but
   changing speakers+k+SNR+steps together does not isolate data
   scale. ADOPTED: matched 10-speaker control (--train-set 10,
   same seeds/settings); final-checkpoint rule frozen (final
   checkpoint scored; interims diagnostic only); 26 speakers is
   an increment, not REVIEW's full Phase 1 (train-clean-100
   remains the follow-on).
7. Crowd = 8–12 draws from 6 identities: accepted limitation,
   recorded in prereg terms; wider interferer diversity needs
   train-clean/test-clean pools (later phase).

NO-GO verdict for all current candidates stands.
