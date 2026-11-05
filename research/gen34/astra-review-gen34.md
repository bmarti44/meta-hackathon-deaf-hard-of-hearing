# Astra xhigh review of the Gen 34 result — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~03:57–04:10 EST (139,006 tokens).
> - The prompt was identical to Muse's ([muse-review-gen34.md](./muse-review-gen34.md)), apart from the closing note to Muse about file access and length.

## Verbatim final answer

**VALID ASSET stands, but the interpretation needs tightening. I also found a substantial DC offset: polarity is not the only output defect. That changes my next-experiment recommendation.**

**1. Verdict and reporting**

I reran the read-only judge: A1–A7 pass, the material hash reproduces, and all registered file hashes match.

Revise these claims:

- Replace “Gen 19 helps in crowds” with **“Gen 19 improves these objective scores in several recorded-babble conditions.”** Neither speech understanding nor preserved localization has been demonstrated.
- “15/15 cells” describes **means pooled across ears**, not universal improvement. Gen32 loses STOI on 126/384 noisy item-ear comparisons; talker 2 has a small negative overall mean difference.
- “Worst-ear differences within about 0.1 dB” needs “cell-average” explicitly. The worst individual noisy-ear Gen32–Gen19 SI-SDR difference is **−0.762 dB**; the worst cell-average worst-ear difference is −0.129 dB.
- Report the spatial results. Target-only mean ILD error is **1.27/1.54/1.42 dB** for Gen19 and **1.06/1.29/1.20 dB** for Gen32, versus zero for bypass. At high reverberation, Gen19 increases noisy-output target-ILD error at every SNR. These diagnostics do not establish localization ability. [Audit data](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen34/audit_s17.json)

Also distinguish **reference fidelity from intelligibility**. The room trainer targets direct sound plus early reflections; BRUDEX scoring targets the complete reverberant recording. Lower target-only STOI flags changed speech, but does not by itself prove that removing reverberation hurts listeners. [Training reference](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen32/train19.py:220)

**2. Polarity: correct mechanism, incomplete diagnosis**

I verified consistent signs across all 96 target-only ear recordings per checkpoint: negative for Gen19 seeds 17/19 and Gen32; positive for seed18. “Seed-dependent sign” is supported. “Set early” requires intermediate-checkpoint evidence.

Yes, publish checkpoint-specific polarity metadata and apply it exactly once:

| Gen19 checkpoint | Polarity multiplier | Decoder bias |
|---|---:|---:|
| Default / seed17 | −1 | +0.110100776 |
| Seed18 | +1 | −0.164651990 |
| Seed19 | −1 | −0.145688012 |

Bind metadata to checkpoint hashes, including renamed files. Never estimate polarity separately for each incoming utterance or ear.

Corrections to the explanation:

- Common two-ear inversion preserves SI-SDR, STOI, ILD and this ITD diagnostic. **It changes the registered waveform-error metric.** Existing verdicts remain unchanged.
- Gen32’s preservation loss is sign-sensitive relative to its teacher; it preserves the teacher’s inverted convention.
- Opposite acoustic signs do not automatically imply opposite electrical stimulation polarity. Ideal magnitude-envelope ACE processing is invariant to acoustic inversion; this is an inference from its processing structure, not verification of the son’s complete N6 path. Cancellation matters where waveforms actually combine before envelope extraction. [ACE processing study](https://journals.sagepub.com/doi/full/10.1177/23312165211030411)

**The additional defect is DC.** On Gen19’s low-reverberation target-only panel, mean waveform error is +6.33 dB raw, **−2.29 dB after sign correction**, and **−18.22 dB after sign correction plus decoder-bias subtraction**. Mean-removed SI-SDR hides this offset. Therefore, withdraw the claim that inversion alone explains the waveform error.

Future registrations should require positive signed projection on every eligible target-only clip/ear after fixed delay alignment, and report DC, gain, clipping and silence output. Fix legacy polarity without retraining. For future training, use signed, gain-sensitive reconstruction supervision and remove or constrain the decoder bias; loss changes do not replace these checks.

**3. Best next single experiment: frozen output-path repair audit**

Choose **(c), before further training**, because the current export path can change the meaning of both waveform and spatial results.

Freeze Gen19 seeds 17/18/19 and compare three predefined outputs:

1. Existing output.
2. Polarity-corrected output.
3. `polarity × (raw_output − decoder_bias)`.

Subtract the bias before delay removal and output level normalization. Keep every other operation identical across arms; no fitted gain, filter sweep or model selection.

Use:

- The complete BRUDEX development grid.
- Existing dry, quiet and spatial development panels.
- Target-only inputs at three fixed levels, plus silence and speech-to-silence transitions.
- Both the research inference path and the exact exported entry point, reported separately.

Two implementation details need explicit treatment:

- The research runner’s `undelay` inserts terminal zeros; its scoring window includes **31 padded samples for talker 1 and 63 for talker 4**. First reproduce v1, then flush the fixed 63-sample delay identically in all new arms.
- The inspected local Hugging Face export averages stereo to mono and restores output RMS independently of the audit’s bilateral convention. It cannot establish preserved directional hearing. [Export implementation](</tmp/claude-501/-Users-bmarti44-bufferright-research-deaf-hard-of-hearing/a5cff5f4-dddd-4b30-a3a9-da58b9d4637a/scratchpad/hf_repo/enhance.py:75>)

**Pre-register this engineering decision rule:** accept the repair only if polarity is positive throughout the target-only level checks; waveform error improves over sign-only in every target-only setting/ear mean; no noisy item-ear loses more than 0.01 dB SI-SDR or 0.001 STOI; no item’s ILD error increases by more than 0.05 dB or its ITD error increases; and clipping, delay and silence behavior do not worsen. These are engineering tolerances, not clinical margins. Failure means investigate, without threshold rescue.

A pass authorizes an inference repair only, with `promoted FALSE`. Preserve Gen34 unchanged and label the new results separately.

Afterward, **(a) becomes my first training choice**: matched fine-tunes with/without signed reconstruction of the **full isolated reverberant target**, retaining dry preservation against a corrected teacher. Do not preserve Gen19’s damaged reverberant output. Trained bilateral processing comes next; ACE auxiliary training follows. BRUDEX remains development material throughout—splitting its already-inspected four talkers cannot restore confirmation status. Confirmation needs different voices and physical rooms.

**4. Two sentences for SUBMISSION.md**

> Gen34 validated a frozen BRUDEX evaluation asset containing recorded speech and babble from four talkers in one laboratory under three reverberation settings; no model was promoted. Objective scores showed condition-dependent gains and speech-preservation costs, while review identified polarity and DC-offset defects requiring correction; no benefit for cochlear-implant speech understanding or localization is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~04:15), covering both reviews

1. **VALID ASSET is adopted.** Both reviewers' wording fixes are applied in results.md:
   - "improves these objective scores", not "helps";
   - pooled-ear means, with the item-ear exceptions and worst individual ear;
   - spatial diagnostics;
   - reference fidelity vs intelligibility;
   - the undelay padding;
   - the Hugging Face export being mono.
   The asset stays development material. Confirmation needs different voices and physical rooms.
2. **Polarity and DC.**
   - Astra's DC-offset finding is adopted, and the polarity-only explanation is withdrawn.
   - "Set early" is now backed by committed evidence: `polarity_check.json` shows every intermediate checkpoint of each seed with a constant sign from step 500.
   - For the future (Astra and Muse): a signed, delay-aligned projection check (α > 0 on target-only clips) plus DC, gain, clipping and silence reporting. For training: signed, gain-sensitive reconstruction with the decoder bias removed or constrained. Legacy models get fixed in inference, never per-utterance.
3. **Next: both, in order.**
   - **Gen 35 = Astra's (c):** a frozen output-path repair audit, with no training.
     - Seeds 17/18/19 on three arms: existing; polarity-corrected; polarity × (raw − decoder bias).
     - The 63-sample delay is flushed identically in the new arms, after first reproducing v1.
     - Panels: the full BRUDEX grid, the dry, quiet and spatial development panels, target-only at three fixed levels, and silence and speech-to-silence transitions. The research path and the exported entry point are reported separately.
     - Her pre-registered engineering decision rule applies. A pass authorises only an inference repair, still `promoted FALSE`.
   - **Then Muse's (a)**, which Astra also ranks first among training options: matched fine-tunes with and without signed reconstruction of the full isolated reverberant target, keeping dry preservation against a **corrected** teacher. BRUDEX stays frozen and descriptive only, and is never trained on.
4. **Hugging Face:** the published repo is not changed until Gen 35 passes **and** the owner agrees, because it is a public change. The proposal is a config-level polarity and bias patch with a version bump, bound to the checkpoint hashes; the weights stay unchanged.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
