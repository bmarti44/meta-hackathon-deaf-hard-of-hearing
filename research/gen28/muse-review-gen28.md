# Muse (Meta) independent review of the Gen 28 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~00:07. The prompt was identical to Astra's.

## Verbatim answer

1. FAIL is correct. Do not re-interpret.

* Gates: R1a True (+0.4591 >=0.30), R1b True (lo +0.230>0), R1c True (15/16), C True, T True, S2 True, S3 True, but D False (-0.1149/-5dB, -0.317/0dB, both lo<0) and SP False. Conjunctive screen = FAIL. Label "GEN27 SCREEN FAIL" in output is presumably typo for Gen28.
* Characterisation is correct: R1 retained, dry cost reduced vs Gen27 but still <0 at both SNRs, S3 fail->pass, SP fail remains but now ITD-only.
* Dose-response: 0.514->0.459 dB = -0.055dB, ~89% retained; dry -0.228->-0.115/-5dB, -0.492->-0.317/0dB. Direction is dose-consistent but N=1 seed/dose, no CI on difference, 0.055dB is ~1/10th of voice+room CI width 0.230-0.736. Suggestive only. No causal monotonicity claim.
* SP: 3.125 vs 3.000 = +0.125 mean over 8 scenes = exactly 1 sample total excess. ITD is integer-sample argmax, so this is the minimum possible non-zero worsening. Not evidence of meaningful spatial regression, but also not evidence of no-regression. Report as: "SP FAIL per prereg, sole miss mirrored ITD +0.125 samples, i.e. 1-sample step in 1/8 scenes, at measure granularity." No rule change, no post-hoc pass.

Do not use bench v2 crowd +3.34 to override registered D FAIL. Different material/measure.

2. Next: (a) P=0.125. Reject others.

* (c) 48k doubles cost to ~2-3h, violates 1-1.5h, more steps predicts more dry specialization, wrong direction.
* (b) fine-tune Gen19 8k changes init+budget+regularizer at once, breaks Gen27/28 dose chain, confounds forgetting/optimizer state.
* (a) is the single-parameter continuation.

Exact Gen29 spec: identical to Gen28 except P(rev|noisy)=0.125 -> 78.75/11.25/10 dry/reverb/10, same seed 20261117, same steps/optimizer/code, same-seed Gen19 comparator, judge_v3 unchanged, dry replay hash check required.

Decision rule: same gates vs Gen19, no relaxation. PASS only if R1a>=0.30 + R1b lo>0 + R1c>=10/16 + C + T + D both SNRs + S2 + S3 + SP ILD and ITD no-worsening. Report Gen29-Gen28 deltas for primary and dry. Expectation: likely still D FAIL; if R1a<0.30 stop taper, taper insufficient, need loss/mixture change, not further dose cut.

3. SUBMISSION.md Gen28, 2 sentences:

Gen28 halved room-augmentation probability to 0.25 and retained +0.46 dB reverberant SI-SDR gain with 15/16 voices improved in-silico, but failed the pre-registered dry-preservation gate at both SNRs. Overall screen FAIL, with S3 passing and the only spatial miss a minimal +0.125-sample mirrored ITD difference; reduced dose lessened dry cost without eliminating it.
