# HANDOFF — take over here

> Written 2026-11-04 ~12:55 EST by the outgoing agent
> (requested Sol 6.1 / actual `muse-wonder-full-1.0`).
> **Maintaining this file is part of the job: update "Current
> state" and "Next actions" at every verified step, in the same
> commit as the work.** Everything below is checkable against
> committed files — trust files over this summary.

## Mission

Prove, **without using any implant**, causal noise-reduction
software that could beat existing processing for the holder's
son's bilateral Cochlear Nucleus 6. Holder is the father
(normal hearing, NOT implanted); the son is the implantee.
Optimize as far as laptop-scale training allows. Co-equal
goals: speech understanding **and** directional hearing.
Repo: `bmarti44/meta-hackathon-deaf-hard-of-hearing`.
**Deadline: submission-ready and pushed by 20:00 tonight
(2026-11-04), submitted by 21:00** (holder instruction).

## Non-negotiable constraints

1. No implants until the bench process is proven. No stage has
   authorized implant use. Vocoder audio ≠ what the son hears.
2. Never claim ≥90%/promotion/listener benefit. Every candidate
   so far is `promoted FALSE`. Offline bench ≠ "beats N6".
3. Evidence discipline: pre-register before training, one
   change per generation, fixed step budgets, judge FINAL
   checkpoints only, 3 seeds judged on seed-mean, matched
   controls. File failures visibly (nulls stay in the record).
4. **Astra xhigh review between every generation** (holder
   standing rule; Sol 6.1 unavailable, holder approved Astra).
   File her verbatim answer + your disposition beside the
   generation before training the next one:
   `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only "<prompt>"`
   (watch for usage-limit errors; retry after the reset time).
5. Commit + push every verified step, naming files explicitly
   (`git add <files> && git commit && git push origin HEAD`).
   Untracked interim `*_step*.pt` checkpoints and local audio
   (`research/bench-n6/examples/`, `listening_pack/`) stay
   untracked on purpose.
6. Append `STATUS.md` (prepend under "Current direction").
   Update this HANDOFF in the same commit as any state change.

## Environment

- Python: `/tmp/gen9env/bin/python` (torch 2.15.0, MPS works).
  If `/tmp` was wiped, rebuild a venv with torch, numpy, scipy,
  soundfile, pystoi, pytest.
- Data (also in /tmp — re-download from OpenSLR LibriSpeech if
  gone): dev-clean at `/tmp/gen12dl/LibriSpeech/dev-clean`,
  train-clean-100 at `/tmp/gen17dl/LibriSpeech/train-clean-100`
  (251 spk; archive SHA-256 `d4ddd1d5…bf6e2`).
- Tests (59 green as of 17:40; ~100 s, three CPU resume tests need the data; avoid running while an MPS run trains, the CPU contention slows it):
  `/tmp/gen9env/bin/python -m pytest research/bench-n6/ research/gen20/ research/gen21/ research/gen22/ research/gen23/ research/gen24/ -q`
- Model: `research/gen15/model_causal.py` — causal waveform
  TasNet-style, 602,510 params, exact causality asserted in
  trainers, 5.88 ms algorithmic latency.

## Where the science stands

- **Accepted baseline = Gen 19** (24k steps, 3 seeds):
  seed-mean crowd ΔSI-SDR **+3.51 dB**, ΔSTOI +0.035,
  ΔACE-electro +0.072; **13/14 required KPIs pass**; sole FAIL
  crowd @−5 dB **+1.19 vs required +1.5**. Scorecard and KPIs:
  `research/bench-n6/{KPI.md,kpi_scorecard.py,bench_v2.py}`.
  Judge with:
  `kpi_scorecard.py --bench <3 seed JSONs> --spatial <hash-matched> --candidate gen19 --babble-kind crowd`
- Nulls on record:
  - Gen 16 multi-term loss.
  - Gen 20 babble-k concentration (paired continuations, B−A +0.02 dB).
  - Gen 21 extra optimization (48k scratch or +24k restart; neither
    qualifies on 3 seeds).
  - Gen 22 30 dB cap (screen VAL +0.149, bench −0.010). Speaker
  count beyond ~26 was neutral at matched compute (Gen 17/18).
- Astra's gradient-imbalance hypothesis for the −5 dB wall: her
  frozen-weight diagnostic found quiet examples giving ~37–53× the
  gradient norm of noisy ones, with clipping on 69–78% of late
  batches. See `research/gen21/astra-review-gen21.md`. Gen 22's cap
  cut clipping severity but not frequency and did not lift −5 dB, so
  the hypothesis is neither falsified nor established.

## Current state (2026-11-05 02:30 — VERIFY, may be stale)

- **Room line (seed 17, judge_v3 vs Gen 19), all FAIL:**
  - Gen 27–30 scratch room doses (P = 0.5 → 0.0625): room gain +0.51 → +0.31; dry 0 dB cost −0.49 → −0.06; D failed every time.
  - Gen 30's failure ended the dose-only campaign (registered boundary).
  - Gen 31 (WiSE-FT: fine-tune Gen 19 on aug50, blend back, α on fresh test-clean voices) gave **NO CANDIDATE**: α = 0.1 missed only on −5 dB STOI −0.00003.
  - All are filed with Astra + Muse reviews.
- **Margins:** the reviewers split (Muse wants NI margins; Astra finds none justifiable a priori). The disposition **keeps zero-margin** D and the VAL rule; see `research/gen31/astra-review-gen31.md`.
- **Gen 32 is TRAINING** (launched 02:15; both reviewers cleared it): Gen 31's procedure plus `--preserve-dry 100`, a relative-MSE penalty vs frozen Gen 19 outputs on dry items.
  - Logs: `/tmp/gen32_s17_pipeline.log` and `/tmp/gen32_ft_s17.log`.
  - The verdict is due ~02:37.
  - Exit "NO CANDIDATE" = FAIL with no screen run.
- **Reserved, untouched voices:** screen-v2's 4 dev-clean voices and 24 test-clean voices. The test-clean VAL panel (16 voices) is development material since Gen 31.
- **Before any seed-18/19 replication of a WiSE-FT line:** add the Gen 19 seed-18/19 parent hashes to `GEN19_SHA` in train18/train19.
- **Site:** round 15 scored 86.1 (Trust 92, Perf 91; Meta 80 because of Explain bugs, now fixed server-side but not yet deployed). Fable is on round-16 fixes.
  - **Deploy only when Fable is idle:** `deploy/deploy_site.sh` uploads the working tree.

## Demo site (beforetheimplant.com) — LIVE since 18:32 (added 2026-11-04 ~18:20)

- **Status 18:38:** https://beforetheimplant.com and www return 200 over
  HTTPS. Muse Ask/Explain work through CloudFront.
- **Updating:** after each verdict, edit `site/data/generations.json` (one
  source for both the site and Muse), then run `deploy/deploy_site.sh`.
- **Explainer video:** in production by a Fable agent in `video/`, using
  the ElevenLabs voice from the itsthemedium video. Its output goes to
  `site/assets/video/` (git-ignored, deploy-only); the site shows it once
  the file exists.

- **Domain:** `beforetheimplant.com` registered via Route 53 at 18:08
  (operation `e9b8f53a…`). Hosted zone `Z031443727CBVQM2UB5R`. ACM cert
  `91ad1661…` uses DNS validation. A background waiter runs
  `deploy/attach_domain.sh` once the cert is ISSUED.
- **Hosting:** private S3 bucket `beforetheimplant-com-site` + CloudFront
  `E34H0K147DZSC0` (`d2lytzwcdc23no.cloudfront.net`), with OAC (the same
  pattern as itsthemedium.com).
- **Meta API:** Lambda `beforetheimplant-muse` (`api/index.mjs`) is served
  at `/api/*` through a Lambda OAC, with reserved concurrency 5.
  - It calls **Muse Spark 1.3** via the `api.meta.ai` Responses API.
  - The key is read server-side from SSM `/itsthemedium/muse-api-key`.
    It never leaves AWS and is never read locally.
  - Routes: `health`, `ask` (tool-using agent: `list_generations`,
    `get_scorecard`, `search_record`), `explain`, `brief`.
  - A direct-invoke-only `mode:"review"` makes Muse a second reviewer of
    verdicts.
  - Its only view of the research is `api/build/knowledge.json`, built by
    `api/build_knowledge.py`. Re-run `deploy/deploy_site.sh` after each
    verdict so the Gen 23/24 entries stay current.
- **Site:** `site/`, designed by a Fable agent (three.js scroll story
  modelled on itsthemedium.com, with Graham's story).
  - Family photos live in `site/assets/family/`. They are git-ignored on
    purpose and deploy to S3 only, with metadata stripped.
  - Deploy with `deploy/deploy_site.sh`, which runs a secret scan and an
    audio-file refusal first.

## Site/demo work in flight (updated 2026-11-04 20:00)

- **20:00 state:**
  - **Site review loop:** round 1 scored 63, round 2 scored 72.9, and the
    round 3 fixes are deployed (fa425b8) with round 3 scoring in progress.
  - **Video:** final at `video/out/before-the-implant.mp4` (2:58, quieter
    jackhammer, `mix.py` jackhammer volume=0.01). A voice-consistency
    re-render is in progress by the video agent. YouTube upload is by the
    owner, and the site carries no film.
  - **HF model:** published. The card credits Muse Wonder Full.
  - **Meta lab:** live. Results are in `research/meta/`.


- **Review loop (owner rule):** fresh Opus reviewers score 11 categories
  each round (UX, wow, animation, mobile, story, a11y, perf, Meta AI,
  trust, cohesiveness, AI tells). The loop continues until **every**
  category is ≥ 90. Fable applies each round's fixes, then
  `deploy/deploy_site.sh`.
  - Round 1 scored 63/100. The review is in this session's agent report;
    its screenshots are in the session scratchpad `qa/`.
  - The capture tool `qa/shot.mjs` uses CDP device emulation, because
    headless Chrome clamps windows to 500 px.
- **Owner preferences:**
  - The sound wave coming into focus is the spine of the page.
  - No AI tells: no cards, rounded borders, pills, glass panels or emoji.
  - No conflict-disclosure note, no "medical advice", no legalese.
  - Muse answers are ELI5 and meaning-only, with the fixed footnote
    "*Still needs to be verified on the Nucleus 6".
  - Graham's clip is portrait SDR with sound and comes after #crowd,
    captioned "shaking his booty with the gray hairs".
- **Agents and pieces in progress:**
  - Explainer video (Fable): `video/`, output to `site/assets/video/`.
  - Meta integration (Opus): `api/` routes plus `site/partials/meta-lab.html`
    and `research/meta/`. One idea: Muse Voice Transcribe word error
    rate on noisy vs model-cleaned speech. Available Meta models:
    muse-spark-1.3, muse-wonder-1.0, muse-voice-transcribe-1.0,
    muse-image-1.0, sam-3.1.
  - Implant explainer + simulated CI audio (Opus):
    `site/partials/implant.html`, `site/assets/audio/implant/`.
  - Hugging Face release (Opus): `bmarti44/before-the-implant-causal-enhancer`
    (Gen 19 safetensors, `enhance.py`, model card, MIT).
  - Snippets go into the `<!-- SLOT:implant -->` and
    `<!-- SLOT:meta-lab -->` markers in index.html.
- **Gen 24:** restart after the site work settles (holder instruction).

## Next actions (in order)

1. **When `/tmp/gen32_s17_pipeline.log` says PIPELINE DONE:**
   - write `research/gen32/results.md`, in the Gen 31 format;
   - run the Astra + Muse reviews (Muse inline, effort medium, under 700 words, or it returns empty);
   - file them with a disposition;
   - update `site/data/generations.json` and SUBMISSION, plus STATUS and this file;
   - commit the FT final weights and log (`git add -f`), the blend index, the selection JSON and, if screened, the screen JSONs.
2. **If Gen 32 fails:** ask both reviewers for the next step. Candidates from their earlier rankings:
   - better measured-room training coverage;
   - a deployable dry-bypass/gating design (which could truly satisfy zero-margin D);
   - two-input linked gain;
   - an ACE envelope auxiliary.
   Plus Astra's standing item: a frozen actual-room-recording evaluation.
3. **Site:** when Fable reports round 16, commit, deploy (that also ships the Lambda fixes) and run review round 17 with a fresh Opus reviewer (brief: `scratchpad/site_review_r14_prompt.txt`, updated). Repeat until every category is ≥ 90.

## Key files map

| What | Where |
|---|---|
| KPI contract + scorecard | `research/bench-n6/KPI.md`, `kpi_scorecard.py` |
| Bench / spatial / vocoder | `research/bench-n6/bench_v2.py`, `spatial_bench.py`, `vocoder.py` |
| Listening pack (gated) | `research/bench-n6/listening_pack.py` |
| Best model (Gen 19) | `research/gen19/{train8.py,results.md,weights/}` |
| Gen 21 trainers/logs | `research/gen21/{train10.py,prereg.md,results.md,judge_replication.py,weights/}` |
| Gen 22 (capped SI-SDR, FAIL) | `research/gen22/{prereg.md,train11.py,judge_screen.py,results.md,screen_s17.json,dev_audit_s17.json,diag_summary.py,astra-prelaunch-review.md,astra-review-gen22-screen.md,smoke/,weights/}` |
| Gen 23 (SI-SDR + 5·L_CS) | `research/gen23/{prereg.md,train12.py,judge_screen.py,verify_provenance.py,astra-code-audit.md,test_*.py,smoke/}` |
| Gen 24 (DRAFT, narrower SNR) | `research/gen24/{prereg.md,train13.py,judge_screen.py,test_*.py}` |
| Astra reviews | `research/gen19/astra-review-gen19.md`, `research/gen20/astra-review-gen20.md`, `research/gen21/astra-{interim-review,review-gen21,review-gen21-final}.md`, `research/gen22/astra-{prelaunch-review,review-gen22-screen}.md` |
| Submission summary | `SUBMISSION.md` |
| Holder-commissioned review | `REVIEW.md` |

## Known traps (learned the hard way)

- Bench filenames' candidate names vary (`gen19`, `gen19s2`,
  …); read `meta` before scripting against summaries.
- Quiet ΔSI-SDR is meaningless (−100 dB-ish); judge quiet on
  absolute SI-SDR only. VAL "999" rows likewise.
- Tiny panels swing wildly: VAL −5 is 8 items, bench −5 is 6
  mixtures. The dev diagnostic (`gen21/dev_audit.py`, 128
  paired items) exists precisely to sanity-check them; it is
  development evidence, never a KPI claim.
- Trainers refuse to overwrite weights (by design); smokes
  must use `--out` in /tmp. Editing a trainer file does NOT
  affect already-running processes (used deliberately once).
- `ls` sorts alphabetically — use `ls -lt` to judge training
  progress; never bench a checkpoint before its DONE line.
- Personalization (holder/wife voices) was recorded as holder-
  approved in `REVIEW.md` §7 but never directly reconfirmed;
  keep any future recordings local/out of git.
