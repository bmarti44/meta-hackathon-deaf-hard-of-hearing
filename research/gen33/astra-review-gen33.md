# Astra xhigh review of the Gen 33 result and agenda — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~03:04–03:15 EST (98,715 tokens).
> - The prompt was identical to Muse's ([muse-review-gen33.md](./muse-review-gen33.md)), apart from the closing note to Muse about file access and length.

## Verbatim final answer

**REJECTED is correct.** All 16 registered hashes match, and recomputing the judge from saved rows reproduces [the decision](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen33/link_s17.json) exactly: L1–L4 all fail. Gen32 remains FAIL; Gen19 remains the baseline.

Tighten three claims in the draft:

- **“18/40 comparisons” means 18 failing subset-level criteria pooling both ears**, not 18 failing ears or independent observations.
- **The SNR pattern is descriptive.** Each SNR uses different speech/noise content; mirrored scenes supply redundant evidence under this symmetric head model. This does not establish that linking helps whenever noise is hard and hurts whenever it is easy.
- Attribute linkage effects using **linked versus independent Gen32**. Comparisons with independent Gen19 also contain the effects of changing weights. Say “SI-SDR declined,” rather than “clarity declined,” especially where STOI moves differently.

The supported conclusion is narrow: **this frozen-weight, mean-encoding shared-mask wrapper failed its feasibility requirements.** It reduced mixture-ILD distortion on the existing bench, but slightly increased mean target-ILD error and incurred substantial worst-ear SI-SDR losses. It does not reject trained bilateral processing, shared acoustic gains, or linking generally. Sharing a learned-basis mask also gives no mathematical guarantee of acoustic cue preservation.

**Neither current ILD statistic should stand alone as the direction measure.** Bilateral CI research strongly supports the importance of usable ILDs and shows localization benefits from coordinated gain control; speech benefits vary across experiments. Those findings do not validate either repository statistic as a predictor of localization. [Potts et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6391546/), [Bakal et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8182628/).

The distinction is:

| Intended question | Appropriate reference |
|---|---|
| Did processing preserve a particular sound’s direction? | That source’s original binaural cues |
| Did processing change the overall sound field? | The mixture’s cues |

For **target localization**, target-referenced cues are more appropriate than requiring the output to match the mixture. Perfect target recovery can legitimately change mixture ILD; bypass always has zero mixture distortion. Conversely, the current whole-output-to-clean-target error conflates source suppression with cue distortion and does not protect other audible sources.

**Prospectively, change the spatial endpoint’s construction—not simply its reference to the mixture.** Make source-specific, short-time band-ILD preservation the primary safeguard, initially on isolated-source recordings and subsequently with a validated measure in mixtures. Retain noisy-output target-ILD error and mixture distortion as separate diagnostics, alongside envelope timing and each-ear speech measures. Register audibility masks, aggregation and tolerances before testing. CI beamforming studies support assessing speech and localization separately: better speech scores can coexist with poor localization. [Yun et al., 2021](https://pubmed.ncbi.nlm.nih.gov/34241104/). Nothing changes Gen33’s verdict.

**Stop the synthetic-gate iteration now and build the evaluation asset first.** These seven failures are dependent development results, not seven independent demonstrations that room enhancement cannot work. My ranked next three experiments are:

1. **Frozen real-recording audit.** Establish what Gen19 and the fixed Gen32 candidate actually do to recorded bilateral speech in reverberation. This provides more useful information than another dose, blend or pooling adjustment.
2. **Train the existing bilateral shared-mask path.** Run matched 4,000-update fine-tunes from Gen19 on identical stereo batches: independent versus shared masks, with identical losses and preservation terms. Mask sharing is the sole between-arm change. This tests learned adaptation to bilateral input; keep the 602k model and judge final checkpoints only.
3. **One ACE-envelope auxiliary ablation.** Matched short fine-tunes with/without one fixed compressed-envelope loss across all 22 channels, retaining waveform and preservation losses. First repair the differentiable float32 path; evaluate hard channel selection separately. The simulator remains a proxy, not the N6 processing chain.

The two training comparisons plausibly fit roughly one laptop hour each with prepared data and existing evaluation code. Both need each-ear, quiet, dry and spatial safeguards; pooled improvements cannot compensate for a failing ear.

For **#1, I would register this exact pilot**:

- **Single change:** add an external recorded-speech evaluation panel. Freeze Gen19 seed17 and independent Gen32 α=0.7 before evaluation; include bypass. No training, selection or historical gate changes.
- **Asset:** BRUDEX’s actual recorded speech and babble components, using one documented left/right front hearing-aid microphone pair from the same individual recording run. It contains four speech signals and three reverberation settings in **one physical laboratory**, not three independent rooms. [Dataset paper](https://uol.de/f/6/dept/mediphysik/ag/sigproc/download/papers/SP2023_14.pdf).
- **Fixed grid:** four speech signals × three settings × target azimuths −60/−30/+30/+60° × SNRs −5/0/+5/+10 dB = **192 noisy items**, plus **48 target-only items**. Process the first 11 seconds and score seconds 1–11. Apply every SNR to every recording, removing Gen33’s content/SNR confound.
- **Rendering and reference:** digitally combine the recorded components, explicitly labelled as such. Set SNR from summed bilateral energy using one noise multiplier shared across ears. Preserve interaural levels and delays. Reference each ear’s recorded isolated target: this tests noise removal and speech preservation, **not dereverberation against a direct-plus-early target**.
- **Readouts:** each-ear SI-SDR/STOI, worst-ear differences, target-only waveform error/STOI, and both current ILD diagnostics. Report every acoustic-setting × SNR cell against bypass and Gen19.
- **Judge and decision:** a separately frozen `judge_recorded_v1.py` returns **VALID ASSET** only after provenance, speaker-overlap audit, complete-grid, channel/delay, bypass-identity and duplicate-baseline zero-difference checks pass; otherwise **INVALID**. Model scores cannot determine whether the asset is accepted. This experiment authorizes no model advancement.
- **Practical limit:** the published short speech/noise archives total about 20 GB. The one-hour audit requires a staged subset; acquisition may take longer. [Files](https://zenodo.org/records/8340195). Once inspected, these recordings become development material; reserve different voices and physical rooms for confirmation.

For SUBMISSION.md:

> Gen33’s shared-mask test on frozen Gen32 weights reduced mixture-cue distortion on the four-scene simulated bench but failed all four registered feasibility checks. This rejects that specific wrapper; Gen19 remains the baseline, and no improvement in speech understanding or directional hearing for cochlear-implant users is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~03:20), covering both reviews

1. **REJECTED is adopted**, as is Astra's narrower wording in results.md: the 18/40 criteria pool both ears, the SNR pattern is descriptive, and linkage effects are read against independent Gen 32. Gen 32 stays FAIL and Gen 19 stays the baseline.
2. **Direction measure: no retrospective change** (both reviewers).
   - Muse keeps target-ILD error as primary.
   - Astra's prospective redesign is recorded for the next spatial registration: source-specific short-time band-ILD preservation as the primary safeguard, with audibility masks, aggregation and tolerances registered in advance. Noisy-output target-ILD error and mixture distortion stay as separate diagnostics, alongside each-ear speech measures.
3. **Agenda: stop iterating on synthetic gates and build the evaluation asset first** (both reviewers, ranked #1). The seven failures are dependent development results that score against one assumed head model and one synthetic room family.
   - **Gen 34 is Astra's frozen real-recording audit:** BRUDEX's actually recorded bilateral hearing-aid-microphone speech and babble, Gen 19 and the fixed Gen 32 candidate frozen, plus bypass. No training, selection or gate change, and no model advancement.
   - Its judge returns VALID ASSET or INVALID on provenance and integrity checks only. Model scores cannot decide whether the asset is accepted.
   - Muse's alternative (measured BRIRs convolved with LibriSpeech) is not adopted as the primary asset. Astra notes that speech convolved with measured RIRs is still simulated material, whereas BRUDEX's components were acoustically recorded.
   - Muse's "ideal extension" is recorded for the owner to decide: the same geometry recorded with ordinary microphones in the family's own rooms. It needs no implant.
   - Acquisition comes first. The short archives total about 20 GB, so a staged subset is needed. Licence and file layout are checked before registration.
4. **Later agenda** (Astra's ranks 2 and 3):
   - a matched trained comparison of independent vs shared-mask bilateral fine-tunes;
   - a single ACE-envelope auxiliary ablation, after the differentiable float32 path is repaired.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
