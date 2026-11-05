# Meta listening check: does cleanup help Meta's model understand the voice?

Written 2026-11-04 ~19:07 EST, before any transcript was produced.
Exploratory and descriptive. Not a registered KPI, not part of the
scorecard, and it changes no verdict. Nothing here is a listener
result: a speech recognizer is not a person and not a cochlear-implant
user.

## Question

On bench-style crowd mixtures, is a Meta model's transcript of the
target talker closer to the true words after the Gen 19 enhancer than
before it?

## Recognizer (a deviation from the brief, decided before results)

The brief asked for `muse-voice-transcribe-1.0`. Probing on 2026-11-04
found no reachable request format for it:

- `/v1/audio/transcriptions` (JSON or multipart) and ~15 other
  transcription paths return an empty 404;
- `/v1/responses` and `/v1/chat/completions` return `model_not_found`;
- `/v1/realtime?model=muse-voice-transcribe-1.0` returns
  `invalid model name` (Spark returns `model is not a realtime model`,
  so the route exists), and a WebSocket upgrade is refused.

What does work: upload a WAV to `/v1/files`, then send it to
**Muse Spark (`muse-spark-1.3`)** in `/v1/responses` as
`{"type":"input_audio","file_id":...}`. A 4 s probe clip was
transcribed correctly up to where the audio stops, and then Spark
invented a continuation. So Spark is used as the recognizer, with an
instruction to write only the words it hears and never complete a
sentence. Its tendency to invent words is a known weakness and will
show up as insertions in both conditions.

## Material (fixed before running)

- Targets: LibriSpeech dev-clean test speakers 1988 1993 5895 6241
  6295 6313 only. Two whole utterances per speaker, 4 to 10 s long,
  picked by `numpy.random.default_rng(20261104)` from each speaker's
  sorted utterance list. 12 utterances.
- Noise: bench crowd babble (`train2.babble`, 8 to 12 draws with
  replacement from interferers 8297 8842 6319 6345 7850 7976), cut to
  the utterance length. Clean RMS 0.1, noise scaled to SNR, exactly as
  in `bench_v2.build_crops_v2`.
- SNRs: -5 dB and 0 dB. Each utterance at both. 24 mixtures.
- Model: Gen 19 seed 17 final checkpoint,
  `research/gen19/weights/causal_seed20261117.pt`, run via
  `bench.load_gen15` (causal, output undelayed).
- Conditions transcribed: clean (once per utterance, a ceiling for the
  recognizer), unprocessed mixture, Gen 19 output. 60 transcriptions.
  Vocoded audio is not run (time).

## Readout

- Word error rate against the LibriSpeech transcript: lowercase,
  punctuation removed except apostrophes, Levenshtein over words.
  Digits are not spelled out (expected to be rare in these
  utterances). WER can exceed 100% because of insertions.
- Reported: mean WER per condition per SNR, the paired difference
  (Gen 19 minus unprocessed) with a bootstrap 95% CI over the 12
  utterances (`common.bootstrap_ci`), and how many of 12 got better,
  worse or tied.
- One transcription per clip (no repeats), so recognizer randomness is
  folded into the numbers. Disclosed, not corrected.

## How it will be read

Descriptive only. With n = 12 per SNR, a CI that excludes 0 is a hint
and nothing more. A null or a loss gets reported the same way as a
gain. Whatever happens, the result is about a machine recognizer on
synthetic mixtures.

## Outputs

- `research/meta/listen_wer.py` (script), `research/meta/results.json`
  (every transcript and WER), `research/meta/results.md` (summary).
- Six of the clips (one per speaker) become the site's "hear and read
  the difference" demo: `site/assets/audio/meta-lab/` (mp3, not
  committed) and `site/data/meta/listen.json`.
- Audio credit: LibriSpeech, Panayotov et al. 2015, CC BY 4.0.

## Amendment 1 (19:17 EST, after run 1, before run 2)

Run 1 broke the protocol: 38 of 60 transcripts came back empty, and the
empties were concentrated in the crowd clips. A diagnostic call showed why:
on crowd clips Spark finishes normally but writes nothing (as the "skip
unclear stretches" rule allows), and an empty reply looks the same as the
intermittent "no audio attached" reply, which the Lambda retries. Run 1 then
dropped those clips, leaving 1 to 2 pairs per SNR, which is meaningless.
It is kept as `results_run1_protocol_bug.json` and not interpreted.

Change for run 2, made before seeing any run 2 output: the instruction now
says "if you cannot make out any words at all, reply with exactly
[unintelligible]". That reply is a valid transcript with no words (WER 100%,
all deletions). Empty replies and "no audio" replies are treated as the
delivery flake and retried (up to 6 times inside the Lambda). Everything else
is unchanged: same clips, same seeds, same checkpoint, and the plan's readout.
The site also reports "share of the reader's words Muse got right" (matched
words / reference words, from the same alignment), because WER above 100%
from made-up words is hard to read in plain language.

## Amendment 2 (19:21 EST, after run 2, before run 3)

Run 2 is also invalid: Spark answered "[unintelligible]" for 9 of 12 *clean*
clips and for all 48 crowd clips, all on the first try. The new escape
reply simply absorbed the delivery flake. Kept as
`results_run2_unintelligible_flake.json`, not interpreted.

Run 3 adds a delivery check inside every clip: a short clean LibriSpeech
sentence from a validation speaker (5536, never a test speaker or
interferer), then 0.8 s of silence, then the clip. Spark writes the check
sentence on line 1 and the main reader's words on line 2. A reply counts only
if line 1 gets at least half of the check sentence's words right (WER <= 0.5);
otherwise it is treated as not delivered and retried (up to 4 outer x 6
inner tries). Only line 2 is scored. Same clips, seeds, checkpoint and
readout as before. If a clip never passes the check, it is reported as
missing, not dropped silently.

## Amendment 3 (19:30 EST, after run 3, post hoc)

Not pre-specified. In run 3, Spark sometimes split the check sentence ("the
savage philosopher the dual mind") across both lines, so line 2 began with
"The dual mind" and those words were scored as if they came from the clip
(Muse Wonder's review flagged the repeated "The dual mind." outputs). Rescore:
a leading tail of the check sentence on line 2 is removed; if nothing is left,
the transcript counts as no words. No new API calls; `hyp_raw` keeps every
original reply, and the unstripped scoring is `results_run3_raw.json`. Both
scorings point the same way (see results.md).
