# Meta listening check: results (exploratory, descriptive)

Plan and its three dated amendments: [plan.md](./plan.md). Not a KPI, changes no verdict, says nothing about any human listener.

**Plain answer: no.** Muse Spark wrote clean speech down well (88% of words right), but in these crowd mixtures it got almost nothing right, before or after the Gen 19 cleanup. Cleanup did not help it at either loudness. The test sits at the recognizer's floor, so it can't show a gain or a loss.

## Run 3 (the one that counts), rescored per amendment 3

Recognizer `muse-spark-1.3` (audio via `/v1/files` + `input_audio`), Gen 19 seed 17 (`causal_seed20261117.pt`), 12 utterances from test speakers, crowd of 8 to 12 babble draws.

| Condition | Paired clips | WER unprocessed | WER Gen 19 | Paired Δ (Gen 19 − unproc), 95% CI | better / worse / tied |
|---|---:|---:|---:|---|---|
| Clean (ceiling) | 12 | 0.141 | | | |
| Crowd −5 dB | 8 | 0.923 | 1.000 | +0.077 (0.000 to +0.231) | 0 / 1 / 7 |
| Crowd 0 dB | 6 | 1.000 | 0.885 | −0.115 (−0.346 to 0.000) | 1 / 0 / 5 |

Share of the reader's words heard right (all delivered transcripts, unpaired):

| | Unprocessed | Gen 19 |
|---|---|---|
| Clean | 183 / 207 (88%) | |
| Crowd −5 dB | 8 / 167 (5%), n = 10 | 0 / 150 (0%), n = 9 |
| Crowd 0 dB | 9 / 120 (8%), n = 7 | 10 / 132 (8%), n = 8 |

Unstripped run 3 scoring (`results_run3_raw.json`): −5 dB Δ +0.075 (−0.014 to +0.236); 0 dB Δ −0.108 (−0.346 to +0.021). Same picture.

## What limits this

- **Delivery.** Spark's audio input is unreliable: about half of identical calls answer as if no audio were attached. 14 of 60 transcripts never passed the delivery check (329 calls for 46 transcripts). The missing clips are probably not random.
- **Floor effect.** Most crowd clips give `[unintelligible]` or a few stray words, so WER sits near 1.0 in both conditions and each SNR's delta comes down to one clip (Muse Wonder's leave-one-out check).
- **Recognizer.** An LLM with audio input, nondeterministic, one transcript per clip. `muse-voice-transcribe-1.0` would be the right tool, but no endpoint accepted it on 2026-11-04.
- Digits aren't spelled out (one clean clip, "1680 to 1704").

## Runs that failed and are not used

- Run 1 (`results_run1_protocol_bug.json`): 38 of 60 empty; empty replies were confused with the delivery flake.
- Run 2 (`results_run2_unintelligible_flake.json`): `[unintelligible]` on 9 of 12 clean clips; the escape reply absorbed the flake.

## Independent review

Muse Wonder (`muse-wonder-1.0`, effort high), verbatim: [wonder_review_pre_rescore.md](./wonder_review_pre_rescore.md) (run 3 raw; it flagged the "The dual mind." spill that led to amendment 3) and [wonder_review.md](./wonder_review.md) (rescored).

## Next step (if pursued)

A dedicated, deterministic recognizer (Voice Transcribe once it is reachable), all pairs scored with failures counted, numbers normalized, and milder SNRs (+5, +10 dB) where the recognizer is off the floor.

Audio: LibriSpeech, Panayotov et al. 2015, CC BY 4.0.
