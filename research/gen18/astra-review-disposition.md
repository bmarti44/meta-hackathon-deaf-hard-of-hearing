# Astra xhigh reviews of Gen 18 + training strategy — disposition (2026-11-03)

Two reviews (between-generation + holder-requested training
strategy). Verdicts: Gen 18 arithmetic verified; interpretation
narrowed; training length/capacity NOT proven binding (only
compute-matched increments tested). Ranked plan adopted:

1. **Gen 19: 24,000 steps from scratch**, train-clean-100, recipe
   frozen, Adam 1e-3 cosine→1e-4 stretched over 24k, batch 8×2 s,
   clip 5, fixed final-checkpoint rule. Fixed VAL panel
   (targets 5536/5694; interferers 2035/2078/2086/2277/2412/2428;
   crowd k8–12; per-SNR SI-SDR/STOI) for convergence diagnosis at
   6k/12k/18k/24k; screen 1 seed, replicate before KPI claims.
   48k only if 18k→24k still improves waveform + intelligibility.
2. Babble k: 80% k8–12 / 20% k4–7, no k2/3 — via paired 12k
   continuations (warm-up 3e-5→3e-4, cosine→3e-5) vs control.
3. Compressed spectral auxiliary: −SI-SDR + 5·L_CS (multi-res
   256/512/1024 STFT, exponent 0.3, 0.7 mag + 0.3 complex).
4. SNR schedule concentrated at −5..+2.5 dB (75% of noisy).
5. STOI surrogate auxiliary 10(1−STOI) if STOI still binds.
6. Batch 4×4 s context.
Conditional: quiet-objective swap if quiet PESQ <4.0; cLN after
first PReLU if clipping persists. Later: R=3 capacity, finer
L=32/S=16/X=8, MUSAN, level aug, mild reverb, binaural linked.

Contract/code fixes applied with this disposition: checkpoint
metadata (pool_n_files, dataset string), VAL loop in trainer.
(Correction 2026-11-03, Astra interim review: exact-resume state
was claimed here but NOT implemented — checkpoints hold weights
only, no optimizer/scheduler/RNG state and no resume path.
Stopping a run therefore cannot continue the same Adam run.) Known
remaining holes (recorded, scheduled): scorecard does not yet
verify quiet PESQ (needs PESQ-capable eval env), streaming RTF,
or a fresh confirmation set — all required before promotion.
