# Astra xhigh review of the Gen 32 result — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~02:38–02:47 EST (73,897 tokens).
> - The prompt was identical to Muse's ([muse-review-gen32.md](./muse-review-gen32.md)), apart from the closing note to Muse about file access and length.

## Verbatim final answer

**1. FAIL is correct.** All 21 registered hashes match, and recomputing the judge from saved rows reproduces the report and verdict exactly.

| Gate | Reason for failure |
|---|---|
| R1a | +0.2828 dB < +0.30 dB |
| D | Mean dry 0 dB SI-SDR difference −0.001158 dB < 0 |
| SP | Mirrored mean target-ILD error increases by 0.06577 dB |

The positive room-gain interval supports an improvement on these development materials; it does not override R1a. The dry interval crossing zero establishes neither harm nor equivalence, and does not override D.

Tighten the [draft results](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen32/results.md):

- Replace “Dry preservation worked” with “The preservation term reduced dry drift and enabled a VAL-selected candidate, but screen preservation failed.”
- Replace “best measured-room transfer” with “first positive room-level SI-SDR means in all six measured rooms at both SNRs.” Aggregate measured-room gains remain smaller than Gen27–29’s.
- Remove “closest yet”: no combined distance-to-success was registered.
- Report that **target-only output remains below bypass**: approximately −0.715/−0.645 dB SI-SDR for synthetic/measured rooms; STOI also remains lower.

These are single-seed, repeatedly consulted development results. Neither universal preservation nor improved CI speech understanding or localization is established. The directional pattern motivates investigation; it does not prove independent ear processing caused it.

**2. Pick (c): a separately preregistered, frozen-weight linked-mask feasibility experiment.** Pause further room-duration and dose changes. Neither 16k nor aug75 directly addresses differential processing between ears.

Use this exact intervention:

- **Freeze Gen32’s selected α=0.7, seed-17 checkpoint.** No training, new blend selection, or parameter sweep.
- Using its existing encoder, mask network and decoder, compute  
  `zL = encoder_relu(L)`, `zR = encoder_relu(R)`;  
  `m = mask_network((zL + zR)/2)`;  
  `yL = decoder(zL*m)`, `yR = decoder(zR*m)`.  
  Keep existing padding, cropping and delay. This uses one mask-network evaluation while retaining each ear’s own encoded signal.
- **Controls:** independent-ear Gen32 isolates the linkage effect; independent-ear Gen19 remains the preservation reference; retain bypass.
- **Evaluation:** retain the original four spatial scenes and all 16 crossed scenes, references, metrics and SP thresholds. Add per-ear SI-SDR/STOI and clean-target-only versions of those scenes. Register these additions before running.
- **Engineering checks:** identical-ear input must reproduce the original mono output; swapping inputs must swap outputs; future-input changes must leave causal prefixes unchanged. Hash the adapter, configuration and checkpoint, and verify that the versioned stereo runner reproduces legacy results in independent mode.

**Prospective decision rule:** continue this architecture only if original SP passes, crossed-scene mean ILD error strictly improves versus independent Gen32, and neither ILD nor ITD error worsens versus Gen19 in **any SNR × mirrored-direction subset**. Also require nonnegative mean per-ear SI-SDR and STOI differences versus both controls in every such noisy subset and each mirrored target-only subset. Any failure rejects this specific wrapper.

Call success **“linkage feasibility passed,” not ADVANCE**. Identical-ear parity means the mono R1a and D failures remain. Gen32 stays FAIL; subsequent room advancement still requires every original gate, replication and fresh confirmation. This experiment cannot rescue its verdict.

Crucially, this model uses a **learned-basis mask**: sharing it does not mathematically guarantee acoustic ILD/ITD preservation. Even common Fourier gains preserve binwise mixture ratios, not necessarily the benchmark’s target-referenced cue errors. Measure the outputs.

The architecture is plausible for synchronized stereo software; Nucleus 6 input/output access, synchronization and downstream processing remain unverified. Linked-AGC studies supply a relevant rationale, with localization improvements in one study but no significant speech-benefit change in another—not validation of this enhancer. [Potts et al., 2019](https://journals.sagepub.com/doi/pdf/10.1177/2331216519831492), [Bakal et al., 2021](https://journals.sagepub.com/doi/10.1177/23312165211018147).

**3. Suggested two sentences:**

Gen32’s dry-output-preserving room fine-tune selected a 0.7 weight blend and improved synthetic-room SI-SDR by 0.283 dB versus Gen19 in one seed, with positive room-level means in all six measured rooms at both tested SNRs. It failed the registered room-gain, dry-preservation and spatial gates; Gen19 remains the baseline, and no benefit for cochlear-implant users is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~02:55), covering both reviews

1. **FAIL is adopted:** R1a (+0.283 < 0.30), D (0 dB SI-SDR mean −0.0012 < 0) and SP (mirrored ILD +0.066 dB).
   - Astra's wording corrections are applied to results.md:
     - "Dry preservation worked" is gone, and so is "closest yet";
     - measured rooms are described precisely;
     - target-only output is reported as still below bypass.
2. **Next: both reviewers chose (c), linked two-ear processing.**
   - Gen 32's weights stay frozen, and there is no training.
   - Longer fine-tunes and stronger room doses (a, b) are paused, since neither targets differential processing between the ears.
3. **Astra's version is adopted as Gen 33.** It is a separately registered **linkage feasibility** experiment:
   - shared mask `m = mask_net((enc(L) + enc(R)) / 2)`, applied to each ear's own encoding;
   - parity, swap and causality checks;
   - legacy reproduction in independent mode;
   - extra per-ear and target-only measures;
   - her prospective decision rule.
   Success is called "linkage feasibility passed", not ADVANCE. Gen 32 stays FAIL, and nothing here can rescue a verdict.
4. **Why Muse's version is not adopted:** average the two per-ear gains and run the full judge_v3. For identical-ear (mono) panels, linking reproduces the mono output, so R1a and D cannot change; judge_v3 would only re-fail on them. Muse's diagnostic, linked ILD below unlinked Gen 32 ILD, is part of Astra's rule.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
