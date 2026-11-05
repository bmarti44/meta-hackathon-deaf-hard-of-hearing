# Astra xhigh pre-launch review of Gen 27 (room augmentation) — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 21:48–21:54 EST (116,328 tokens). Prompt:
> `/tmp/astra_g27_prompt.txt`. Reviewed commit 29174f7.

## Verbatim final answer

**Do not launch commit `29174f7` yet.** The core augmentation is sound, but three defects need correction. I verified the registered source hashes and all 1,048 RIR file hashes; 21 read-only tests passed. I did not rerun the tests that write training checkpoints.

Three defects are **BLOCKING**:

1. **The target is peak-plus-50 ms, not reliably direct-plus-50 ms.** [rirbank.py:54](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/rirbank.py:54) defines arrival as the largest sample. In training RIR `smallroom/Room179/Room179-00007.wav`, a strong arrival occurs around sample 229, but the chosen peak is 464: approximately **14.7 ms later**. Held-out `mediumroom/Room192/Room192-00012.wav` has the same problem, approximately 5.3 ms later. This changes the reference cutoff and acoustic descriptors. Use an audited direct-arrival rule, validate it on these multiple-peak examples, and regenerate affected metadata and references.

2. **Completeness safeguards accept invalid evidence.** I confirmed that deleting every −5 dB bench row still leaves S2/S3 passing. Spatial checks accept duplicate rows, incorrect crop IDs, and empty existing-bench rows when summaries remain. See [judge_v2.py:62](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/screen_v2/judge_v2.py:62) and [judge_v3.py:209](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/judge_v3.py:209). Require exact registered grids, duplicate rejection before dictionary construction, matching scene metadata, and summaries recomputed from validated rows. Reverberant room IDs—including target-only rooms—must match the manifest, rather than merely satisfy room counts.

3. **Replication can retain results without safeguards.** [judge_v3.py:261](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/judge_v3.py:261) derives required safeguard names from the first input’s keys. Three documents with empty checks and positive **1×1** cell arrays returned `RETAIN` in my check. Require explicit safeguard keys, Boolean values, 16×6 cells with fixed voice/room ordering, consistent provenance, and the prerequisite seed-17 screen pass.

Preserve this registration and self-test as versioned evidence; issue a dated superseding registration after corrections, before training.

There is also an outstanding **launch prerequisite**: the registered MPS timing check after Gen24 releases the device. The 101–108 minute estimate is an extrapolation, **not an established upper bound**.

The following are **NON-BLOCKING**:

- **Target-only reporting without a gate follows my original specification**, which supplied no threshold. I recommend adding a prospective SI-SDR/STOI non-worsening safeguard against Gen19, separately for synthetic and measured target-only conditions. Passing that would still not establish non-harm against bypass.
- **Mirrored checks are redundant, not vacuous.** They can detect candidate regression, but the two sides supply identical evidence under channel-swap symmetry. A linked/binaural system does not automatically remove that symmetry. The dry, assumed-head bench cannot establish spatial preservation in rooms.
- **RT60/geometry confounding, point-source SSN and limited positions** restrict generalization; they do not invalidate this augmentation comparison. Report room-specific results and avoid attributing differences solely to RT60.
- **The 1 s cap is acceptable for this screen.** My audit found at most approximately 0.11% of original RIR energy beyond the cap among selected files. Keep truncation disclosed.
- Six synthetic rooms provide limited room-level uncertainty estimation. The replication interval conditions on the three trained seeds; it does not quantify generalization across arbitrary training seeds.

The target/SNR/alignment definitions otherwise match the specification:

| Definition | Assessment |
|---|---|
| Target | Dry clean speech unchanged; reverberant speech through the early RIR, tapering from arrival+45 to +50 ms. **Correct once arrival identification is fixed.** |
| SNR | Full reverberant target energy versus the energy of the **summed reverberant interferers**, with one final interferer scaling. Correct; late target reverberation remains target energy. |
| Gain/history | Shared target/reference RIR gain and real preceding speech history are correct. SSN history is separately generated, with a filter-state discontinuity at the join—a minor approximation. |
| Alignment | Preserve acoustic timing; apply the fixed 63-sample training delay and evaluation `undelay`, then `[256:-256]` scoring. Correct; no output-dependent alignment. |

**Report the Gen19 observation now**, explicitly as a provisional descriptive result from this implementation:

> On the Gen27 reverberant development panel, Gen19 seed 17 increased mean SI-SDR relative to unprocessed mixtures at −5 dB by +0.37 dB with synthetic RIRs and +0.73 dB with measured RIRs, while mean STOI decreased by 0.029 and 0.017. For reverberant target-only speech, mean changes were −1.65 dB SI-SDR and −0.064 STOI. These results use the current peak-anchored early reference and fixed model-delay alignment.

Call this **metric degradation on simulated reverberant speech**, not established intelligibility loss or harm to CI listeners. Measured-RIR convolution is still simulated material. Recompute after the arrival correction and retain both versions; do not present the current numbers as validated direct-plus-50 ms results.

## Disposition (Claude Opus 5.5, 2026-11-04 ~21:58)

**Launch held.** All three blocking defects go back to the builder for
correction:
1. an audited direct-arrival rule, validated on the cited multi-peak
   RIRs, with regenerated metadata, references and hashes;
2. exact-grid, duplicate-rejecting, recomputed-summary completeness
   checks, with room IDs matched to the manifest, in `judge_v2` and
   `judge_v3`;
3. explicit-key, fixed-shape replication with a seed-17 screen
   prerequisite.

**Also adopted:**
- a prospective target-only non-worsening safeguard, by stratum;
- room-by-room reporting;
- the MPS timing check as a launch prerequisite.

**Process:** the original registration and self-test stay as versioned
evidence. A dated superseding registration follows the corrections and
comes before any training.

**The Gen 19 observation** is reported now, in Astra's exact provisional
wording, in `gen19-rooms-provisional.md`. It will be recomputed after the
arrival correction, and both versions kept.
