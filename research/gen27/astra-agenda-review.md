# Astra xhigh review of the goal-aligned research agenda — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 ~21:02–21:07 EST (99,061 tokens). Prompt:
> `/tmp/astra_refocus_prompt.txt`.
>
> Context: the holder redirected the research ("we want to help people who
> wear cochlear implants hear better, that is the goal") away from
> benchmark-matching and score tweaks.

## Verbatim final answer

**Gen27 should test room augmentation, with a fixed direct-plus-early target.** Move real-recording evaluation forward, keep spatial preservation mandatory, and leave Gen24 running under its existing registration. Gen19 remains **13/14 on its original implemented scorecard**.

The panel correction is broader than stated. [Gen17’s training log](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen17/weights/train_log_seed20261117.json:10) includes **all 16 screen-v2 targets and all four reserved speakers: 5338, 3000, 3170, 3752**. The listed ten were also Gen13–16 training speakers. Gen19’s actual training-pool log has no overlap.

**Screen v2 remains usable as a development screen for Gen19-family candidates**, provided their training and checkpoint ancestry remain disjoint. Earlier models’ training exposure does not automatically contaminate Gen19’s weights: Gen19 trained from scratch. However, this is not a historically untouched confirmation panel, and repeated advancement decisions further make it development material.

Append a dated correction to the [registration](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/screen_v2/prereg.md:23), preserving the original record and material hashes:

> Screen v2 is training-disjoint from Gen19 and qualifying descendants, but was incorrectly described as unused in earlier research decisions. Ten targets were training speakers for Gen13–16; all sixteen targets and all four reserved speakers were training speakers for Gen17. Screen v2 is retained for development comparisons only. Fresh, audited speakers and recordings will replace the final-confirmation reserve.

Audit **actual training manifests and checkpoint ancestry**, not inherited `TRAIN_SPK` constants. Reserve a fresh confirmation set—at least 12 targets plus separate interferers—from material unused across training, tuning, screens and pilots. Do not retrospectively replace speakers or rescue historical verdicts.

The **+2.385 versus +1.06 dB** observation establishes panel sensitivity. It does **not** identify crowd identity count as the cause: targets, utterances, mixtures and sampling also differ. Moreover, both generators sample identities with replacement. Keep the finding descriptive; abandon six-voice matching and blend sweeps.

The work priorities should be:

| Priority | Scientific judgment and correction | Laptop feasibility |
|---|---|---|
| **1. Rooms: Gen27** | Strong environmental hypothesis. Vary room geometry, direct-to-reverberant ratio and source positions as well as RT60. Decaying noise plus a direct impulse is a useful stress test, but insufficient evidence of realistic-room robustness. | Plausible with cached RIRs and CPU FFT augmentation; measure overhead first. |
| **2. Real recordings: prepare now** | Essential external check. Include measured-RIR mixtures and separately identified actual room recordings. Synthetic speech convolved with measured RIRs is still simulated material. | Evaluation fits laptop work; obtaining trustworthy recordings and references is the larger task. |
| **3. Two-input processing: next architecture experiment** | Spatial hearing remains a co-equal goal now. Distinguish two microphones feeding one output from bilateral input/output preserving ear cues. Linked gains are a constraint, not demonstrated localization restoration. | A small shared-mask model is plausible; two complete independent networks may exceed the budget. |
| **4. ACE auxiliary objective** | Mechanistically sensible, but the current simulator is too simplified to justify “optimizing what reaches the electrodes.” Retain waveform fidelity and test an auxiliary envelope loss. | Likely modest overhead after repairing gradients and device compatibility. |

Early-reflection removal should not be assumed desirable: a study using more realistic auditory environments found that early reflections were not necessarily detrimental to CI recipients. That supports testing a direct-plus-early target first. [Kressner et al., 2018](https://research-management.mq.edu.au/ws/portalfiles/portal/101328341/100835787.pdf)

**My concrete Gen27 specification is:**

1. **One intervention: room augmentation.** Train seed 20261117 from scratch for 24,000 steps against the existing same-seed Gen19 final. Freeze architecture, SI-SDR loss, optimizer schedule, batch size, training speakers, SNR distribution and crowd recipe. Preserve 10% dry quiet; transform half the noisy examples: approximately **45% dry noisy, 45% reverberant noisy, 10% dry quiet**. Use separate augmentation randomness so underlying speech/noise draws remain paired. Do not incorporate Gen24’s SNR change.

2. **Use a frozen, physically structured RIR bank.** Cover RT60 0.2–0.8 s, with balanced short/medium/long strata. Render each talker through its own source-to-microphone RIR within the same room. Convolve before summation; one RIR applied to the completed crowd puts every interferer on the same acoustic path. Split training and evaluation by **room**, not merely RIR filename. OpenSLR28 supplies simulated and measured RIRs suitable for constructing such banks. [Dataset documentation](https://www.openslr.org/28/)

3. **Fix the target before training:** target speech convolved with its direct path plus reflections through **50 ms after direct arrival**, tapering the final 5 ms. Dry examples retain the original clean target. This cutoff is an engineering choice, not an established CI optimum. Define noisy SNR using full reverberant target energy versus summed interferer energy; report DRR/C50 separately. Preserve target/reference gain relationships, real convolution history and fixed model-delay alignment. Do not independently normalize the reference or optimize alignment per output.

4. **Register a separate reverberant screen.** Retain screen-v2’s speech/crowd draws, saving individual interferer stems. Cross them with six held-out rooms—two per RT60 stratum—and both −5/0 dB SNRs. Include a separate measured-room stratum and reverberant target-only checks. Freeze room IDs, references, manifests, hashes, aggregation and rules before candidate evaluation. The original dry panel stays unchanged.

5. **Advance only when every gate passes:**

| Gate | Proposed prospective rule |
|---|---|
| Reverberant primary | Candidate−Gen19 SI-SDR **≥+0.30 dB**, equally weighted across speakers, rooms and SNRs; paired 95% bootstrap lower bound >0, resampling speakers and rooms; ≥10/16 speaker means improve. |
| Consistency | Mean SI-SDR and STOI differences ≥0 separately at each SNR and in synthetic versus measured-room strata. |
| Dry screen | At both −5 and 0 dB, mean SI-SDR and STOI differences ≥0; speaker-bootstrap lower bounds exceed **−0.15 dB / −0.003**. An inconclusive safeguard does not pass. |
| Existing safeguards | Retain screen-v2 S2/S3, including quiet ≥25 dB SI-SDR and ΔSTOI ≥−0.02. Report dry bench results by SNR, including the outstanding −5 dB row. |
| Spatial safeguard | Preserve existing spatial gates; additionally require no mean worsening against Gen19 in target-ILD or ITD error separately at hard SNR and mirrored directions. |
| Replication | Screen pass authorizes seeds 18/19 only. Require three-seed primary gain ≥+0.30 dB, positive gain in ≥2/3 seeds, positive clustered lower bound, and safeguards in every seed. Fresh-material confirmation follows. |

These are **engineering advancement thresholds**, not clinically meaningful differences or proof of universal no-harm. Keep per-speaker and per-room results visible so averages cannot hide failures.

Gen19 seed 17 took **84.8 minutes** for training in its [recorded run](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen19/weights/train_log_seed20261117.json:2). A 1–2 hour Gen27 training run is plausible, not established. Cache RIR transforms and time a short smoke run, including data preparation. Budget evaluation separately; avoid competing with Gen24 for MPS. Never substitute an interim checkpoint because time expires.

For the later ACE experiment, use **SI-SDR plus a fixed-weight compressed-envelope loss across all 22 channels**, with the coefficient calibrated only on training/development material. Evaluate hard 8-of-22 selection separately. Hard top-k passes gradients through selected amplitudes but does not provide useful gradients through channel-ranking decisions.

The existing [ACE helper](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen13/ace_sim.py:138) is not drop-in training code: its waveform path has `@torch.no_grad()`, assumes J4 framing, and differs from the benchmark’s framing. Other helpers use float64 or return Python floats. Build and validate a differentiable float32 path; MPS does not support float64. [PyTorch documentation](https://docs.pytorch.org/docs/main/notes/mps.html) Its omitted AGC, compression, current mapping and neural effects remain limitations even after repair. Published electrodogram-learning work supports investigating the direction, not treating this proxy as a clinical processor. [Gajecki et al., 2023](https://pubmed.ncbi.nlm.nih.gov/37030808/)

For binaural work, start with **two synchronized inputs predicting a common time-frequency gain applied to separate ear signals**. Preserve ear-specific targets and timing; never duplicate a mono output into both ears. The [current spatial bench](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/spatial_bench.py:39) is only four simplified scenes using independent mono enhancement. Expand geometry, SNR, contents and measured binaural responses. Cue preservation alone cannot establish benefit: linked AGCs did not significantly improve bilateral benefits in one CI study. [Bakal et al., 2021](https://journals.sagepub.com/doi/10.1177/23312165211018147)

For real recordings, use controlled playback with known source signals and calibrated alignment first; natural conversations generally lack a valid clean reference for SI-SDR/STOI. BUT ReverbDB provides recorded retransmitted speech as one external starting point, subject to the same provenance audit. [Dataset paper](https://arxiv.org/abs/1811.06795) Keep real-room results separate, freeze candidates before evaluation, and report them strictly as acoustic or proxy findings—**never listener benefit**.

## Disposition (Claude Opus 5.5, 2026-11-04 ~21:25)

**Agenda adopted, in Astra's order:**
1. Gen 27, room augmentation, with a direct-plus-early (50 ms) target,
   built exactly to her specification;
2. real-recording evaluation, prepared now;
3. a two-input linked-gain architecture;
4. an ACE envelope auxiliary, after repairing a differentiable float32
   path.

**Abandoned:** six-voice crowd matching, blend sweeps, and Gen 26.

**Panel correction:** her wording is appended verbatim to
`../screen_v2/prereg.md`.
- All 16 targets and all 4 reserves were Gen 17 training speakers.
- Screen v2 stays development-only for Gen 19-family candidates.
- A fresh, audited confirmation set (≥ 12 targets plus separate
  interferers, from material unused across training, tuning, screens and
  pilots) replaces the reserve.

**Gen 24** keeps running under its own registration.
