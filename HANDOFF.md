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

## Current state (2026-11-04 18:40 — VERIFY, may be stale)

- **Gen 23 COMPLETE: seed-17 screen FAIL.** −5 dB gains vs Gen19 s17
  were VAL −0.338 and bench −0.027. The STOI and white rows also fail.
  `verify_provenance.py --gen 23` PASSES.
  - Results in `research/gen23/results.md`; the spectral term was ~1% of
    the gradient.
  - Muse's review is filed: `research/gen23/muse-review-gen23-screen.md`.
  - Astra's review is running (`/tmp/astra_g23_screen.out`). File it
    verbatim plus disposition as `research/gen23/astra-review-gen23-screen.md`
    BEFORE launching Gen 24.
- **Gen 24 REGISTERED** (`research/gen24/prereg.md`, 18:50).
  - Run 1 was stopped at step ~100 by holder decision: 0.7 s/step on a
    shared machine. Logs are in `research/gen24/aborted_run1/`; not
    judged.
  - **Restart after deployment** with `/tmp/gen24_s17_pipeline.sh` (log
    `/tmp/gen24_s17_pipeline.log`). It runs train → bench → dev → judge →
    provenance, each gated. Delete `/tmp/gen24_s17_pipeline.log` and
    `/tmp/gen24_hard60_s17.log` first.
  - Then file `research/gen24/results.md`, reviews (Astra + Muse) and
    disposition.
- Gen 22 is complete (FAIL); details are in `research/gen22/results.md`.

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

## Next actions (in order)

1. **When `/tmp/gen23_s17_pipeline.log` says PIPELINE DONE**:
   - run `research/gen23/verify_provenance.py --gen 23 --seed 17`
     (it must PASS);
   - read `research/gen23/screen_s17.json` and write
     `research/gen23/results.md`;
   - replace SUBMISSION's `[GEN 23 STATUS — updated at completion]`;
   - prepend STATUS and update this file;
   - commit the final weights, train log, bench, dev and screen JSON
     (not `*_step*.pt` / `*_state_*.pt`) and push.
2. Run Astra's xhigh review of the Gen 23 result and file it verbatim
   with a disposition.
   - If Gen 23 FAILs and she agrees, register Gen 24: dated header,
     source hashes, MPS smoke. Launch `/tmp/gen24_s17_pipeline.sh`.
     Its result will likely land after 20:00, so it is filed later and
     never judged from an interim checkpoint.
   - If Gen 23 ADVANCEs, seeds 18/19 replication comes next.
3. If Gen 23 is not judged by 19:40, mark the placeholder "screen
   pending at submission", then commit and push.
4. By 20:00: final commit and push. `git status` should show only
   intentionally-untracked files: interim `*_step*.pt`,
   `*_state_*.pt`, `*_val_partial.json`, aborted-run ckpts, local
   audio, and the pre-existing `bench_v2_gen17_control10.json`.

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
