# Muse Wonder review of the Meta listening check (verbatim)

Model `muse-wonder-1.0`, reasoning effort `high`, response status `completed`, 2026-11-04 19:30 EST. Prompt built by `research/meta/wonder_review.py` from `plan.md` and `results.json` (all rows and transcripts). Filed unedited.

---

# Review

## 1. Recomputed WER

| Condition | Recomputed mean | Summary |
|---|---:|---:|
| Clean, n=12 | $(0.385+1.000+0.040+0.167+0.095)/12=0.141$ | 0.141 |
| −5 dB, 8 complete pairs | Unprocessed: $(7+0.385)/8=0.923$; Gen 19: $8/8=1.000$; Δ $=+0.077$ | Matches |
| 0 dB, 6 complete pairs | Unprocessed: $6/6=1.000$; Gen 19: $(5+0.308)/6=0.885$; Δ $=-0.115$ | Matches |

The arithmetic matches, but these are **complete-pair means, not the planned n=12 per SNR**. Fourteen of 48 crowd transcripts are missing, leaving 8 pairs at −5 dB and 6 at 0 dB.

## 2. What the evidence supports

Only a weak, descriptive statement about Muse Spark on these synthetic mixtures: it returned “[unintelligible]” (WER 1.0) for almost every crowd clip. At −5 dB, 7/8 pairs tied and one favoured unprocessed; at 0 dB, 5/6 tied and one favoured Gen 19. Each SNR’s direction rests on a single discordant utterance, and both reported CIs include or touch zero.

Thus there is **no reliable evidence that Gen 19 changed this recognizer’s transcripts**, in either direction. The opposite point estimates at the two SNRs add no confidence.

## 3. Threats to validity

- **LLM recognizer, not dedicated ASR:** Spark can abstain rather than make a best-effort transcription, creating a severe floor effect at WER 1.0. A different prompt or recognizer could produce a different result. This could flip the conclusion.
- **Nondeterminism plus selective retries:** Attempts ranged from 1 to 19, with retries conditioned on passing a delivery check. With one retained transcription per clip, a redraw could change the sole discordant pair at either SNR. This could easily flip either sign.
- **Missing transcripts:** The 14 failures may not be missing at random; delivery success may depend on audio condition or intelligibility. Restoring them could flip the result.
- **Crowd-word insertions/hallucinations:** Few crowd transcripts contain substantive words, so this is not the main driver here. It remains possible in principle, particularly for the partial transcripts.
- **WER normalization:** Digits were scored literally. For example, “1680 to 1704” against spelled-out reference words contributed to WER 0.385 despite being largely semantically correct, apart from 1688 versus 1680. This inflates absolute WER and the magnitude of the sole −5 dB discordance, but alone would not reverse it because the paired Gen 19 result was “[unintelligible].”

The post-hoc check-sentence stripping in Amendment 3 is another researcher degree of freedom, although it is disclosed and reportedly did not change direction.

## 4. Concrete next step

Repeat the same 24 mixtures with a pinned, deterministic dedicated ASR, using pre-specified numeric-word normalization, no abstention category, and enough additional utterances to yield at least 30 complete pairs per SNR.
