# Muse Wonder review of the Meta listening check, run 3 raw scoring (verbatim)

This review read `results.json` before amendment 3 (spill stripping). Its point about repeated "The dual mind." outputs is what led to amendment 3. The review of the rescored data is `wonder_review.md`.

Model `muse-wonder-1.0`, reasoning effort `high`, response status `completed`, 2026-11-04 19:29 EST. Prompt built by `research/meta/wonder_review.py` from `plan.md` and `results.json` (all rows and transcripts). Filed unedited.

---

# Review

## 1. Arithmetic recomputed from rows

| Condition | Paired/items used | Unprocessed mean WER | Gen 19 mean WER | Gen19 − unproc |
|---|---:|---:|---:|---:|
| Clean | 12 | — | 0.141 overall | — |
| −5 dB | 8 pairs | 0.918 | 0.993 | +0.075 |
| 0 dB | 6 pairs | 0.980 | 0.872 | −0.108 |

Sums check: clean WER sum = 1.687/12 = 0.141; −5 dB = 7.343/8 vs 7.944/8; 0 dB = 5.881/6 vs 5.231/6. **Summary means, deltas, and better/worse/tied counts (1/2/5 at −5 dB; 1/1/4 at 0 dB) match the rows.** But effective n is 8 and 6 pairs, not 12: 14/60 transcripts are missing, and unpaired survivors are discarded.

## 2. What the evidence supports

Weakly: **no detectable Gen 19 effect for this recognizer on these synthetic mixtures.** Point estimates oppose each other by SNR, both bootstrap CIs include 0 (−5 dB: −0.014 to 0.236; 0 dB: −0.346 to 0.021), and most pairs tie at WER ≈ 1.0 — hypotheses are mostly “[unintelligible]” or “The dual mind.” Each mean is driven by one clip: removing 5895-34622-0003 changes −5 dB delta from +0.075 to ≈ +0.002; removing 6295-244435-0005 changes 0 dB delta from −0.108 to ≈ +0.008. This is recognizer behavior on bench mixtures only; it supports nothing about any human listener.

## 3. Threats to validity

- **Recognizer validity — could flip it.** Muse Spark is a nondeterministic LLM, not a dedicated ASR. One transcript per clip, with up to 19 attempts and acceptance conditioned on passing the prepended delivery check, means accepted outputs are selected resamples. Repeated identical “The dual mind.” responses suggest canned/hallucinated output saturating WER at ~1.0. A rerun could plausibly reverse either sign.
- **Missingness — could flip it.** Failures are unlikely random; delivery failure plausibly correlates with clip/condition difficulty. Losing 4 pairs at −5 dB and 6 at 0 dB can bias deltas either way.
- **WER normalization — could flip the small residuals, not create the main pattern.** Digits are penalized despite being semantically right (clean “1680/1704” vs spelled-out reference gives WER 0.385), and compounds like “counterattack” vs “counter attack” add spurious errors. This inflates the clean ceiling (mean 0.141 includes one clean WER = 1.0) and matters because leave-one-out deltas are near zero.
- **Crowd-word insertions:** anticipated, but barely observed — output is dominated by deletions/empty responses, so WER is floor/ceiling-bound and insensitive to genuine insertion differences.

## 4. Concrete next step

Re-run the identical 24 paired mixtures with a pinned, deterministic dedicated ASR (temperature 0, no prepended check sentence), pre-specifying spelled-out number normalization and retaining all 12 pairs per SNR with failures scored, not dropped.
