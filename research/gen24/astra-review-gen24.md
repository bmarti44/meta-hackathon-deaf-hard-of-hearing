# Astra xhigh review of the Gen 24 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 ~22:00–22:05 EST (50,669 tokens). The prompt was identical
> to Muse's ([muse-review-gen24.md](./muse-review-gen24.md)).

## Verbatim final answer

1. **FAIL is correct.** I reran the judge and provenance verifier: both reproduce the reported results. Rules 1, 2, 3 and 6 fail; quiet and other required rows pass. The [registered 0 dB safeguard](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:75) permits losses of at most 0.15 dB and 0.003 STOI: VAL breaches both (−0.296/−0.0107), and bench breaches STOI (−0.0043). Dev’s positive mean does not compensate for only 4/8 targets improving versus five required.

   Characterize this as **failed advancement with observed regressions**, or an operational null—not evidence of zero effect. It rejects this specific SNR redistribution under plain SI-SDR, 24k steps and this seed. Pairing the draws strengthens attribution to the redistribution, but the experiment reallocates the entire SNR distribution; it neither isolates hard-example exposure alone nor establishes that other exposure schedules cannot help. No confirmation-seed expansion is authorized by this screen.

2. **Keep the planned order:** Gen27 rooms, real recordings, two-input processing, then ACE auxiliary; prepare real-recording evaluation now. Use Gen19’s original SNR recipe for Gen27. Its [pre-launch corrections and prerequisites](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/astra-prelaunch-review.md) still apply. The provisional reverberation findings motivate that experiment but require recomputation after reference correction; they establish no listener harm or benefit. Gen19 remains the baseline at 13/14, `promoted FALSE`.

   Preserve “pending at submission” for the 20:00 snapshot and file this result in a separately dated update, as [registered](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen24/prereg.md).

3. Suggested two sentences:

> Gen24’s pre-registered single-seed screen of narrower noisy-SNR sampling failed: versus Gen19, −5 dB SI-SDR gains were −0.212 dB on VAL and −0.019 dB on the bench, STOI declined on both, the 0 dB safeguard failed, and only 4/8 dev targets improved. Provenance passed, but this sampling recipe was not retained; this late-filed T0 result does not establish that hard-SNR exposure is generally ineffective.

## Disposition (Claude Opus 5.5, 2026-11-04 ~22:08), covering both reviews

1. **Verdict: adopted** as "failed advancement with observed regressions",
   an operational null. The redistribution is rejected for this recipe
   and seed only. No confirmation seeds are authorized.
2. **Plan unchanged:** Gen 27 (rooms) uses Gen 19's original SNR recipe,
   and its pre-launch corrections are in progress. Then real recordings,
   two-input processing, and the ACE auxiliary.
3. **Snapshot preserved:** the 20:00 submission snapshot (ebf026f) keeps
   Gen 24 as "pending at submission". This result is filed as a
   separately dated update in SUBMISSION.md, using Astra's two
   sentences.
