# Submission summary — causal noise reduction for cochlear implants: a T0 in-silico evaluation

> Hackathon entry state, 2026-11-04. Research-design + in-silico
> (T0) evidence only. No patient data, no implant testing, no
> listener-benefit claim. Detail: [GOAL.md](./GOAL.md),
> [STATUS.md](./STATUS.md), [research/bench-n6/](./research/bench-n6).

**Live site: [beforetheimplant.com](https://beforetheimplant.com).**
It tells Graham's story in his dad's words and walks through the
research. Muse, Meta's AI model, answers questions about it.

**The model is public:**
[huggingface.co/bmarti44/before-the-implant-causal-enhancer](https://huggingface.co/bmarti44/before-the-implant-causal-enhancer).
It ships Gen 19's three seeds as safetensors, model code, a one-command
`enhance.py` and a plain-language model card. The upload was round-trip
verified bit-identical to the research checkpoints, and `enhance.py`
reproduces the bench (crowd +3.44 dB vs the bench's +3.49 on seed 17).

## How Meta's models are used

The site calls **Muse Spark** (`muse-spark-1.3`) through the Meta
Model API Responses endpoint, from an AWS Lambda
([api/index.mjs](./api/index.mjs)) served under `/api/*`.

| Feature | What Muse does |
|---|---|
| **Ask the research** | Works as an agent. It picks from three function tools, runs them, then answers in plain words. Every tool step is shown. |
| **Explain this** | Every scorecard row and generation has a button that explains it at a parent or researcher level. Answers are cached at the edge. |
| **Generation briefs** | A short what / why / what-happened / what-it-means summary of each generation. |
| **Second reviewer** | A direct-invoke-only mode (not reachable from the web) reviews each verdict independently of Codex Astra. Its answer is filed verbatim beside Astra's. |
| **Listening test of our model** | Muse Spark listens to crowd recordings before and after our model's cleanup, writing down what it hears ([research/meta/](./research/meta/), plan written first). Result: a null. Spark transcribed clean speech well (88% of words right) but got almost nothing in these crowds either way (−5 dB: 5% → 0%; 0 dB: 8% → 8%), so the test sits at the recognizer's floor and can't show a gain or loss. The site's "hear and read the difference" demo plays these clips. |
| **Muse Wonder as reviewer** | `muse-wonder-1.0` independently recomputed that listening study from raw rows (filed verbatim): "no reliable evidence that Gen 19 changed this recognizer's transcripts". |

The three tools are `list_generations`, `get_scorecard` and
`search_record`. The last is a keyword search over the committed
record: this summary, results, pre-registrations, the independent
reviews and the KPI contract.

Muse only sees the research through these tools and a knowledge file
built from committed files ([api/build_knowledge.py](./api/build_knowledge.py)),
so every number it quotes comes from the record. It is told:

- to point questions about a child's own care to their audiologist, without disclaimers;
- never to imply the model beats the N6 or helps any listener;
- to report nulls plainly.

The API key lives only in AWS SSM Parameter Store (SecureString) and
is read by the Lambda at runtime. It never reaches the browser or this
repo. The Lambda URL only accepts CloudFront (origin access control),
with reserved concurrency as a hard cap.

### Muse Wonder Full ran the research loop

Most of the research loop was run by **Muse Wonder Full**
(`muse-wonder-full-1.0`, Meta's model) under the holder's direction:
designing, training, judging and filing each generation, from Gen 0
through Gen 21. That includes:

- the frozen baseline and gap analyses;
- the no-implant bench (`research/bench-n6/`) and the 14-row KPI scorecard;
- **the Gen 19 model**, the published baseline that is now on Hugging
  Face.

Each record is labelled `Model: … actual muse-wonder-full-1.0` in its
results file.

Claude Opus 5.5 (Anthropic) took over on 2026-11-04 at about 13:00. It
ran Gen 21's seed 19 and verdict and Gen 22 to 24, and built the site's
infrastructure; a Claude (Fable) agent designed the site. Codex Astra
was the independent reviewer between generations throughout, and from
Gen 23 Muse Spark reviews each verdict alongside Astra.

## Problem and approach

Cochlear-implant (CI) users struggle most in crowd noise. The
motivating case is the holder's son, who wears bilateral Cochlear
Nucleus 6 processors. We evaluate a small, strictly causal neural
enhancer against unprocessed audio and a classical causal noise
gate on synthetic mixtures, under CI-relevant readouts, before any
implant is involved. **N6 processing was not tested**, so nothing
here compares against it.

Method: an evolutionary loop of generations. In the recent
registered experiments (Gen 19–22) each generation is
pre-registered with one change, fixed budgets, final-checkpoint-only
judgment, 3-seed seed-mean KPIs, and an independent Codex Astra
(xhigh) review between generations. Earlier generations were less
disciplined (e.g. Gen 17 changed pool, mixtures, SNR weighting and
budget together). Failures are filed, not hidden.

## The bench (no-implant proving ground)

`research/bench-n6/` builds synthetic LibriSpeech mixtures with
speaker-disjoint train/test sets. It covers:

- a **crowd** condition (8–12 source draws with replacement from six
  interferer identities) and a competing-talker condition;
- SSN, held-out white noise and quiet rows;
- three intelligibility proxies: waveform STOI, vocoded ESTOI, and
  simulated post-selection (8-of-22) ACE electrodogram correlation;
- a spatial direction-cue screen on an assumed head model;
- a hard KPI scorecard that reports INCOMPLETE unless it has 3
  distinct-hash seeds plus a hash-matched spatial run.

A vocoder listening-pack builder exists, but it only checks the
legacy go/no-go file. It does not yet enforce the current
scorecard, checkpoint identity or fresh-material clearance; those
are required before any evidence pack.

Tests: 17 bench/spatial tests in `research/bench-n6/`, plus 42
trainer/judge tests in `research/gen20–24/` (`pytest research/bench-n6
research/gen20 research/gen21 research/gen22 research/gen23
research/gen24`; Gen 24's 8 cover a drafted, not-yet-registered
trainer). KPI arithmetic is
reproducible from committed bench JSONs. Diagnostic and parity
evidence is identified separately where it is used.

## Headline result (Gen 19, complete under the implemented scorecard's evidence checks)

The model is a causal Conv-TasNet-style enhancer: 602,510 params,
exact causality verified, 5.88 ms algorithmic latency (excluding
compute), trained 24k steps on train-clean-100. Seed-mean results
vs unprocessed (3 seeds):

| KPI | Required | Gen 19 |
|---|---|---|
| Crowd ΔSI-SDR | ≥ +3.0 dB, CI lo > 0 | **+3.51 ✓** |
| Crowd ΔSTOI | ≥ +0.03, CI lo > 0 | **+0.035 ✓** |
| Crowd ΔACE-electro | ≥ +0.05, CI lo > 0 | **+0.072 ✓** |
| Crowd @ 0 dB | ≥ +1.5 dB | +4.65 ✓ |
| Crowd @ −5 dB | ≥ +1.5 dB | **+1.19 ✗** |
| SSN / white SI-SDR, quiet SI-SDR / STOI | registered thresholds | ✓ pass |
| Direction cues: target-ILD error (seed 17; four simulated scenes) | < unprocessed (5.96 dB) | 5.47 ✓ |
| Direction cues: ITD error (seed 17; four simulated scenes) | ≤ unprocessed (5.75 smp) | 4.0 ✓ |

**13 of 14 implemented scorecard rows pass.** The only failure is
the hardest condition, crowd at −5 dB. **Verdict: FAIL — keep
optimizing. promoted FALSE.** Astra independently recomputed every
row from raw data.

Disclosures:

- Quiet PESQ and CPU streaming RTF are required by the KPI contract
  but remain unestablished.
- White-noise vocoded ESTOI decreases in all three seeds (mean
  −0.059), even though the registered white SI-SDR row passes.
- The direction-cue rows come from one seed on simulated scenes. In
  the −5 dB scene, target-ILD error worsens (10.29 → 11.22 dB).
  Nothing here implies a directional-hearing benefit.

## What the generations taught us

- **Training budget:** extending the budget and cosine horizon from
  6k to 24k steps improved overall crowd ΔSI-SDR from 2.73 to 3.51 dB.
- **Data:** Gen 17's 10→26-speaker pool expansion gained 0.26 dB;
  Gen 18's 26→251 expansion was roughly neutral at 6k.
- **Failed changes:** Gen 16's one-seed, 2k-step, two-auxiliary
  objective underperformed. Gen 20's paired one-seed continuation
  (crowd-concentrated sampling) failed its registered benefit
  criterion. Neither result establishes a general zero effect.
- **Gen 21** compared 48k scratch training against parent + 24k
  continuation, with data paired via an RNG handoff. Both arms
  passed the seed-1 validation screen, but **neither qualified on 3
  seeds**. Mean −5 dB gains were VAL +0.14/+0.12 and bench
  −0.24/−0.10, against a +0.30 bar on both panels. Extra
  optimization raised overall crowd (+3.51 → +3.79 dB) and the easy
  conditions, but not −5 dB. Gen 19 stays the baseline; Gen 21 is
  filed as a null ([research/gen21/results.md](./research/gen21/results.md)).
  This rejects those extra-optimization policies; it does not
  establish a fundamental −5 dB limit.
- **Gradient diagnostic:** a frozen-weight diagnostic found gradient
  imbalance (quiet/noisy gradient-norm ratio ~37–53×; clipping on
  69–79% of late batches), which motivates a causal training test.
  Its contribution to the −5 dB failure is unestablished.
- **Gen 22** (30 dB soft-capped SI-SDR loss, 24k scratch vs
  same-seed Gen 19,
  [research/gen22/results.md](./research/gen22/results.md)). Its
  control mode showed logged loss/gradient-norm prefix parity with
  Gen 19, including a resume check.
  - **Result:** the pre-registered single-seed screen failed the
    required +0.30 dB improvement on both −5 dB panels. Gains versus
    same-seed Gen 19 were +0.149 dB on VAL and −0.010 dB on the bench.
    All remaining screen criteria passed.
  - **Reading:** the cap was not retained. This operational null does
    not establish zero effect or resolve the gradient-imbalance
    hypothesis.
- **Gen 23** ([research/gen23/results.md](./research/gen23/results.md)).
  - **Result:** the pre-registered single-seed, 24k-scratch screen of
    plain SI-SDR plus 5× compressed multi-resolution spectral loss
    failed. −5 dB gains versus same-seed Gen 19 were −0.3375 dB on VAL
    and −0.0268 dB on the bench, STOI worsened on both, and white-noise
    ΔSI-SDR missed its ≥0 safeguard.
  - **Reading:** provenance checks passed and the auxiliary was not
    retained. This T0 result does not establish zero effect or a
    general spectral-loss null.
  - **Reviews:** Codex Astra and Muse (Meta) both reviewed the verdict
    independently; both reviews are filed verbatim in research/gen23/.
- **Gen 25** ([research/gen25/results.md](./research/gen25/results.md)),
  checkpoint averaging with no training.
  - **Result:** the pre-registered single-seed uniform average of nine
    late Gen 19 checkpoints failed advancement. −5 dB gains versus
    same-seed Gen 19 were +0.1706 dB on VAL and +0.0296 dB on the bench,
    below the required +0.30 dB on both, and bench STOI declined by
    0.000970.
  - **Other checks:** provenance and all remaining screen criteria
    passed, including a dev improvement of +0.100 dB with 7/8 targets
    improving.
  - **Outcome:** the averaged model was not retained, and Gen 19 remains
    the baseline. Reviewed by Codex Astra and Muse.
- **Gen 24** (narrower noisy-SNR sampling: 40% of noisy training
  examples at −5 to −3 dB instead of 17%, same random draws) is next
  ([research/gen24/prereg.md](./research/gen24/prereg.md)).
  It is registered and will run after tonight's deployment. A first launch was stopped at step ~100 because the machine was shared with the site build; it is not judged.
  - **Update, 2026-11-04 22:08 (after the 20:00 snapshot), in Astra's
    wording:**
    - Gen 24's pre-registered single-seed screen of narrower noisy-SNR
      sampling failed. Versus Gen 19, −5 dB SI-SDR gains were
      −0.212 dB on VAL and −0.019 dB on the bench, STOI declined on
      both, the 0 dB safeguard failed, and only 4/8 dev targets
      improved.
    - Provenance passed, but this sampling recipe was not retained.
      This late-filed T0 result does not establish that hard-SNR
      exposure is generally ineffective
      ([research/gen24/results.md](./research/gen24/results.md)).

- **Gen 27, real rooms** (update 2026-11-04 23:25, after the 20:00
  snapshot; [research/gen27/results.md](./research/gen27/results.md)).
  - **Background:** the holder redirected the research to real-world
    benefit for cochlear-implant users. On simulated reverberant rooms,
    Gen 19 itself showed metric degradation.
  - **Result, in Astra's wording:** Gen 27's registered single-seed
    room-augmentation experiment improved synthetic-room SI-SDR by
    0.514 dB versus Gen 19 (95% voice-and-room bootstrap CI 0.238–0.844;
    15/16 voices improved), with positive aggregate measured-room and
    target-only gains. It failed advancement because dry noisy-speech
    performance declined, crowd STOI narrowly missed its threshold, and
    mirrored spatial errors increased slightly. Gen 19 remains the
    baseline, and no listener benefit is established.
  - **Next:** Gen 28 halves the reverberant training share, to try to
    keep the room gains without the dry cost.

- **Gen 28, half the room dose** (update 2026-11-05 00:15;
  [research/gen28/results.md](./research/gen28/results.md)), in Astra's
  wording:
  - **Result:** Gen 28 halved the room-augmentation probability and
    improved synthetic-room SI-SDR by 0.459 dB versus Gen 19 in one
    training seed, while reducing but not eliminating the dry-speech
    losses seen in Gen 27.
  - **Verdict:** it failed the registered dry-preservation and spatial
    ITD gates despite passing the other checks. Gen 19 remains the
    baseline, and no listener benefit is established.
  - **Next:** Gen 29 halves the dose again (12.5%).

## Limits (stated plainly)

Offline bench results cannot establish superiority over the N6's
proprietary processing, which was never tested. Vocoder listening
by a normal-hearing adult cannot predict an individual CI user's
benefit. No candidate has earned the staged listening test yet;
that requires all required KPIs plus fresh-material confirmation.
Implant-involved testing would additionally need assent,
audiologist oversight and MAP-safe levels. None was attempted.

## Next steps

- Finish the capped-loss generation, then compressed-spectral loss,
  then narrower SNR sampling, each separately controlled.
- Build a fresh-material confirmation package (12 new speakers,
  genuinely distinct-voice crowds) before any listening evidence.
- Develop a binaural linked-gain model for directionality.
- Measure quiet PESQ and streaming RTF to complete the KPI contract.
