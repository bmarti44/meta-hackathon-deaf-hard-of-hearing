# Gen 31 — WiSE-FT (room fine-tune of Gen 19, blended back): NO CANDIDATE → FAIL (T0)

> Claude Opus 5.5, 2026-11-05 ~02:10.
> - Registration: [prereg.md](./prereg.md), with its pre-launch amendment. Astra and Muse cleared it.
> - Launched 01:47 after the pipeline verified Gen 30's FAIL.
> - Selection record: [val_selection_s17.json](./val_selection_s17.json).
> - Reviews: [Astra](./astra-review-gen31.md) and [Muse](./muse-review-gen31.md).
> - `promoted FALSE`.

**Verdict:** FAIL by the registered rule. **No blend passed at α = 0.1**, so
there is no candidate. No screen material was touched: no rev panel, dry
panel, bench or spatial run, and no judge_v3.

**Step 1, fine-tune:**
- 8,000 updates from Gen 19 seed 17 (parent `80000b64…` verified), on aug50 (45 / 45 / 10). Realised counts: 28,598 / 28,910 / 6,492 of 64,000 items.
- It continued Gen 19's data stream from its 24k handoff. Lifetime: 32,000 updates.
- Wall time 13.0 min (781.5 s). Final `ft_aug50_seed20261117.pt`, sha256 `4d356359…94e`.
- Descriptive only: on the trainer's built-in 8-item dev VAL, −5 dB SI-SDR vs unprocessed went from +0.56 dB (step 0 = Gen 19) to +0.91 dB.

**Steps 2–3, blends chosen on the fresh test-clean dry panel.** Values are
the mean of (blend − Gen 19) over 256 paired items per SNR. VAL material
`c2c4f89a…`.

| α | −5 dB SI-SDR | −5 dB STOI | 0 dB SI-SDR | 0 dB STOI | pass |
|---|---|---|---|---|---|
| 0.1 | +0.0213 | **−0.00003** | +0.0008 | +0.00040 | ✗ |
| 0.2 | +0.0393 | −0.00007 | −0.0010 | +0.00074 | ✗ |
| 0.3 | +0.0539 | −0.00012 | −0.0054 | +0.00101 | ✗ |
| 0.5 | +0.0737 | −0.00026 | −0.0216 | +0.00134 | ✗ |
| 0.7 | +0.0813 | −0.00043 | −0.0470 | +0.00143 | ✗ |
| 1.0 (the fine-tune) | +0.0710 | −0.00075 | −0.1011 | +0.00115 | ✗ |

The full 10-point curve is in `val_selection_s17.json`.

**Reading** (descriptive; dry speech, new voices, this seed only):
- The room fine-tune does not simply cost dry speech. On these new voices it:
  - **improves** −5 dB SI-SDR at every α (up to +0.08 dB);
  - **improves** 0 dB STOI at every α;
  - **costs** 0 dB SI-SDR from α = 0.2 (down to −0.10 dB at α = 1);
  - **costs** a very small amount of −5 dB STOI (−0.00003 at α = 0.1).
- The rule failed on that last number. That is a real failure under the registered rule. Its size is far below anything a listener could notice, but no tolerance or finer-grid rescue follows (registered).
- Muse's pre-launch note anticipated this: a zero-margin "≥ 0 on all four" rule fails often when the true effect is near zero. The same holds for judge_v3's D, which also requires non-negative means.
- No listener benefit is established.

**Artifacts committed:**
- the fine-tune final weights and train log;
- the blend `index.json` (blends are regenerable from Gen 19 and the fine-tune, and are git-ignored);
- the selection JSON.

**Next:** decided with Astra and Muse (see the review files). The drafted
default is Gen 32: the same procedure with a dry-output-preservation term
during the fine-tune (`research/gen32/train19.py`, not registered).
