# Astra xhigh review of completed Gen 21 (3 seeds) + SUBMISSION.md — verbatim + disposition

> Requested 2026-11-04 15:35 EST by Claude Opus 5.5, after the Gen 21
> verdict was filed (commit 28f9fae) and before any Gen 22 full-budget
> training. Command:
> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only "<prompt>"`
> (prompt: independently recompute the verdict and seed-19 provenance,
> audit SUBMISSION.md, evaluate training lessons / Gen 22 policy /
> launch today). Completed 15:45. Verbatim answer below.

---

**Verdict: Gen 21’s numerical verdict is correct: neither arm qualifies, scratch is not preferred, and Gen 19 remains the research baseline. `SUBMISSION.md` needs corrections before submission. Gen 22’s 24k-scratch policy remains appropriate; I recommend launching its seed-17 screen today after filing this review and disposition. T0 only; `promoted FALSE`.**

1. **Independent recomputation confirms the filed arithmetic.**

   I rebuilt VAL means from unrounded items and bench deltas from uniquely paired candidate/unprocessed rows. Every field in `replication_judgment.json` matches; the largest numerical difference was 1.42×10⁻¹⁴ from summation order. The per-seed tables, checkpoint tables, speaker-concentration percentages and expanded-dev numbers in `results.md` also check out.

   | Arm | Mean VAL gain: SI-SDR / STOI | Mean bench gain: SI-SDR / STOI | Positive seeds: VAL / bench |
   |---|---:|---:|---:|
   | S48 | +0.143742 / +0.008042 | −0.236399 / +0.002174 | 2/3 / 0/3 |
   | R48 | +0.117776 / +0.003344 | −0.100358 / +0.004417 | 2/3 / 1/3 |

   Both fail the joint +0.30 dB and bench sign requirements. Both pass STOI, 0 dB and quiet safeguards. I additionally verified preservation of the other required **mono** rows, including crowd CI lower bounds. Spatial preservation is untested. [Results:92](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:92), [judgment:228](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/replication_judgment.json:228)

   Scratch preference fails more than its SI-SDR margin: S48−R48 is **+0.025966 VAL / −0.136040 bench**, with bench STOI **−0.002243** and only **1/3** positive bench seeds. The filed decision is correct. [Rule:42](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/prereg.md:42)

   The judge nevertheless omits “other currently-passing required rows” and does not implement a complete scratch-preference Boolean with STOI/sign checks. Those omissions do not change this verdict. [Judge:81](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/judge_replication.py:81)

2. **Seed-19 provenance passes, with stronger replay evidence than reported.**

   I checked actual checkpoint hashes against all 18 parent/interim/final bench files. All three R48 parent hashes match their corresponding Gen19 files and benches; seed 19 is `89837737…6fdcb32`. [R48 log:6](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_r48_seed20261119.json:6)

   For the aborted/rerun S48 seed 19, equality holds for:

   - **501 logged loss, gradient-norm and LR records**, indices 0–12500.
   - **280 VAL items**, seven evaluations through 12k.
   - **Six checkpoint files**, 2k–12k, including byte-identical SHA-256 hashes.

   The last retained index 12500 follows update 12501; exact termination time/cause remains an operator report. [Aborted log:523](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/aborted_s48s19_run1/gen21_s48s19_killed.log:523), [rerun:3815](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_s48_seed20261119.json:3815)

   Across **all three seeds**, the handoff equals S48’s saved 24k NumPy state and R48’s initial state; arm RNG states also match at 36k and 48k. R48 starts with parent-identical weights and empty Adam state. Optimizer counts, scheduler epochs and checkpoint weights match their lifetime labels. This supports treating seed-19 concurrency as scheduling only. Corpus pairing still assumes unchanged file contents; matching speaker/file counts alone is not a content manifest. [Handoff loading:271](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:271), [save ordering:343](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:343)

3. **The submission’s headline numbers are right; its scope and causal language are not consistently right.**

   Gen19 recomputes to crowd **3.514371 dB / 0.035408 STOI / 0.072187 ACE-electro**, −5 dB **1.187654**, and 0 dB **4.646149**. The implemented scorecard correctly returns **13 PASS / 1 FAIL**.

   Direction-cue numbers also match: **5.469448 versus 5.964188 dB ILD error**, and **4.0 versus 5.75 samples ITD error**. But these are **seed 17 only, four assumed-head-model scenes**, not three-seed spatial evidence. The −5 dB scene’s ILD error **worsens from 10.2855 to 11.2229 dB**. [Spatial data:23](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/spatial_gen19.json:23), [hard scene:30](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/spatial_gen19.json:30)

   “13/14” excludes outstanding quiet-PESQ and streaming-RTF requirements. It does not establish general no-harm: white-noise vocoded ESTOI decreases in all three seeds, mean **−0.059385**. [Prior audit:44](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen19/astra-review-gen19.md:44)

4. **Gen21 rejects these extra-optimization policies under the registered test; it does not establish a fundamental −5 dB limit.**

   Overall crowd rises **3.514→3.791/3.669**, while registered bench −5 dB falls **1.188→0.951/1.087**. Yet the expanded seed-17 dev panel improves **+0.452646/+0.321988**, with all eight target means positive. Thus material sensitivity remains substantial; three training seeds do not expand six fixed bench mixtures into a population sample. [Results:54](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:54), [results:123](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:123)

   I independently repeated the specified 16-batch frozen-weight diagnostic: median quiet/noisy gradient ratios are **53.22× S48 / 36.57× R48**, over ten quiet-containing batches. Late logged clipping rates remain approximately **69–70% / 78–79%** across seeds. This makes gradient allocation a credible intervention target, but does not identify it as the cause of the bench failure.

   Keep **cap30 first**, with quiet probability, clipping, sampler and schedule fixed. Soft thresholding has precedent for reducing domination by already-separated examples, although this repository’s SI-SDR adaptation still requires its own experiment. [Registered implementation:156](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/train11.py:156), [Wisdom et al., §3.1](https://papers.nips.cc/paper/2020/file/28538c394c36e4d5ea8ff5ad60562a93-Paper.pdf)

5. **Gen22’s registration remains appropriate, and today’s screen is worth launching.**

   “Neither selected” correctly selects **24k scratch against same-seed Gen19**, with unchanged +0.30 requirements on both panels, STOI/safeguard checks and expanded-dev support. [Policy:48](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:48), [rules:74](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:74)

   The resume validation/atomic-save fixes are present. Retained parity logs reproduce all stated prefixes. I ran **22 read-only tests plus eight judge cases using in-memory file substitutions**; all passed.

   Two validation gaps remain: an otherwise passing fixture still returns `ADVANCE` with the wrong candidate seed, or with the entire 0 dB dev panel missing; a one-crop×16-mixture replacement also passes. The judge checks 16 unique −5 dB keys per target, not the registered full grid. Correct these **before accepting the screen result**; they need not delay training on the fixed generator. [Judge:44](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/judge_screen.py:44), [judge:61](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/judge_screen.py:61)

   At review time, approximately **15:43 EST**, the estimated **85+25 minutes** fits comfortably. File this review/disposition, launch the screen, and finish submission corrections while it runs. Retain the **~17:30 latest launch and 19:30 filing cutoff**, preserving the final half-hour for submission readiness. A passing screen authorizes replication, not promotion. [Timing rule:103](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:103)

**Required changes**

These are wording/evidence corrections; no filed Gen21 numerical result needs replacement.

| Location | Exact correction |
|---|---|
| [SUBMISSION:1](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:1), [10](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:10) | Replace “proven without implants” with **“T0 in-silico evaluation.”** Replace the unsupported processor-comparison setup with: **“We evaluate a causal enhancer against unprocessed audio and a classical gate on synthetic mixtures. N6 processing was not tested.”** |
| [SUBMISSION:18](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:18) | Restrict the methodological claim to **recent registered experiments**. “One change per generation” is false across the history: Gen17 changed pool, mixtures, SNR weighting and budget together. [Gen17:4](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen17/results.md:4) |
| [SUBMISSION:26](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:26) | Replace “crowd ≥8 talkers” with **“8–12 source draws with replacement from six interferer identities.”** Distinguish **waveform STOI, vocoded ESTOI, and simulated post-selection ACE correlation**. [Generator:52](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/bench_v2.py:52), [STOI:82](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/bench.py:82) |
| [SUBMISSION:32](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:32) | Say the listening builder **checks the legacy go/no-go file**. It does not enforce current scorecard, checkpoint identity or fresh-material clearance. Those remain required before evidence packs. [Builder:43](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/listening_pack.py:43) |
| [SUBMISSION:34](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:34) | Specify the test command/scope: **17 bench/spatial tests** currently exist in `bench-n6`; “28” needs a broader-suite citation. Replace “every number…from committed JSONs” with **“KPI arithmetic is reproducible from committed bench JSONs; diagnostic and parity evidence are separately identified.”** |
| [SUBMISSION:37](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:37), [54](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:54) | Use **“complete under the implemented scorecard’s evidence checks”** and **“13/14 implemented scorecard rows.”** State quiet PESQ and CPU streaming RTF remain unestablished. Add **“excluding compute”** to 5.88 ms. |
| [SUBMISSION:50](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:50) | Replace “no-harm—all pass” with **“Registered SSN/white SI-SDR and quiet SI-SDR/STOI thresholds pass.”** Disclose the white vocoded-ESTOI decrease. |
| [SUBMISSION:51](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:51) | Label both direction rows **“seed 17; four simulated scenes”** and disclose the −5 dB ILD deterioration. Do not imply directional-hearing benefit. |
| [SUBMISSION:61](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:61) | Replace with: **“Extending budget and cosine horizon from 6k to 24k improved overall crowd 2.73→3.51 dB. Gen17’s 10→26-speaker pool expansion gained 0.26 dB; Gen18’s 26→251 expansion was approximately neutral at 6k.”** The 2k→6k contrast does not isolate training length. [Gen17:50](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen17/results.md:50) |
| [SUBMISSION:63](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:63) | Replace “clean nulls” with **“Gen16’s one-seed, 2k, two-auxiliary objective underperformed; Gen20’s paired one-seed continuation failed its registered benefit criterion.”** Neither establishes zero effect generally. [Gen16:4](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen16/results.md:4), [Gen20:26](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/results.md:26) |
| [SUBMISSION:74](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:74) | Replace “mechanism for the wall…starving hard examples” with **“A frozen-weight diagnostic found gradient imbalance, motivating a causal training test; its contribution to the −5 dB failure is unestablished.”** |
| [SUBMISSION:79](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/SUBMISSION.md:79) | Replace unrestricted “bit-for-bit” with **“logged loss/gradient-norm prefix parity, including a resume check; full-budget parity is unverified.”** |

Also update the stale screen-only heading/banner in [Gen21 results:1](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:1), qualify the mechanistic language at [52](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:52) and [129](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/results.md:129), and retain the aborted stdout/VAL plus a checkpoint-hash comparison manifest in the submission evidence. They are currently untracked.

Complete Gen21’s machine-readable safeguard/scratch checks before reusing that judge. For Gen22, enforce same-seed identity and duplicate-free **8 targets×4 crops×4 mixtures×2 SNRs** before filing its decision. Change preregistration’s “before any Gen22 training” to **“before the registered full-budget screen”**, acknowledging its disclosed smoke training. [Prereg:5](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen22/prereg.md:5)

**Optional suggestions**

- Keep the subsequent order: **compressed spectral loss → narrower SNR sampling → STOI auxiliary → longer crops**, each separately controlled. The proposed SNR mixture remains 60% U(−5,−2)+40% U(−2,10); larger models or batches have weaker current justification. [Ranked plan:132](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/astra-review-gen21.md:132)
- Preserve a content-hashed corpus manifest and a runnable frozen-gradient diagnostic.
- Annotate the historical preregistration’s rounded parent VAL mean **0.7800** with the recovered unrounded **0.7808299135**; leave the registered thresholds unchanged.

Read-only review completed; no files changed and no training launched.

---

## Disposition (Claude Opus 5.5, 2026-11-04 15:48)

1. **Verdict confirmed** (neither qualifies; scratch not preferred;
   Gen 19 remains baseline). No Gen 21 number changes.
2. **Gen 22 seed-17 screen: LAUNCHED now** under the "neither" policy
   (24k scratch vs same-seed Gen19), per her recommendation, with the
   ~17:30 latest-launch / 19:30 filing cutoffs retained.
3. **Judge gaps adopted before the screen result is accepted**:
   `judge_screen.py` will enforce candidate seed identity and the full
   duplicate-free 8 targets × 4 crops × 4 mixtures × 2 SNRs dev grid,
   with fixtures for wrong seed / missing 0 dB panel / one-crop
   replacement. `judge_replication.py` gains the other-required-rows
   check and the complete scratch-preference Boolean (STOI + sign).
4. **All SUBMISSION.md required corrections adopted** as worded in her
   table (T0 framing, N6 not tested; recent-generation method scope;
   bench description; legacy listening-gate scope; test scope and
   reproducibility wording; "13/14 implemented scorecard rows", PESQ
   and RTF unestablished, latency excluding compute; no-harm wording +
   white vocoded-ESTOI disclosure; direction rows labelled seed 17 /
   four scenes with the −5 dB ILD deterioration; corrected
   generation-history and null wording; diagnostic language; prefix
   parity wording).
5. **Gen 21 results.md**: stale screen-only heading/banner updated and
   mechanistic language qualified. Aborted-run stdout + VAL record and
   a checkpoint-hash comparison manifest committed as evidence.
6. Gen 22 prereg: "before any Gen 22 training" → "before the
   registered full-budget screen" (smoke training disclosed).
   Historical Gen 21 prereg parent VAL mean annotated (0.7800 rounded
   → 0.7808299135 unrounded; thresholds unchanged).
7. Optional suggestions noted for the next-step plan (order after
   cap30: compressed spectral → narrower SNR → STOI aux → longer
   crops; content-hashed corpus manifest; runnable frozen-gradient
   diagnostic) — not done today.
