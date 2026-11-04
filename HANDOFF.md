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
- Tests (37 green as of 13:25; ~35 s, one CPU resume test needs the data):
  `/tmp/gen9env/bin/python -m pytest research/bench-n6/ research/gen20/ research/gen21/ research/gen22/ -q`
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
- Nulls on record: Gen 16 multi-term loss; Gen 20 babble-k
  concentration (paired continuations, B−A +0.02 dB). Speaker
  count beyond ~26 was neutral at matched compute (Gen 17/18).
- Astra's key diagnosis for the −5 dB wall (verified by her
  frozen-weight diagnostic): near-perfect quiet examples give
  ~37–53× the gradient norm of noisy ones; clipping on 69–78%
  of late batches → hard examples starve. See
  `research/gen21/astra-review-gen21.md`.

## Current state (2026-11-04 16:00 — VERIFY, may be stale)

- **Gen 21 COMPLETE — NEITHER ARM QUALIFIES**; Astra's final
  review confirmed every number (`research/gen21/astra-review-gen21-final.md`,
  disposition filed). 3-seed mean −5 dB gains: S48 VAL +0.144 /
  bench −0.236; R48 VAL +0.118 / bench −0.100 (bar +0.30 both).
  Gen 19 stays the baseline. Seed-19 replay evidence committed:
  `research/gen21/weights/aborted_s48s19_run1/{gen21_s48s19_killed.log,
  s48_seed20261119_val_partial.json,replay_manifest.json}` (6 ckpt
  hashes + 7 VAL evals identical).
- **SUBMISSION.md corrected per Astra** (T0 framing, N6 untested,
  scorecard scope, PESQ/RTF unestablished, white vocoded-ESTOI and
  −5 dB ILD disclosures, generation-history wording). One
  placeholder left: `[GEN 22 SCREEN RESULT — filled at completion]`.
- **Gen 22 seed-17 screen RUNNING** (launched 15:45:55; detached
  pipeline `/tmp/gen22_s17_pipeline.sh`, log
  `/tmp/gen22_s17_pipeline.log`, trainer log
  `/tmp/gen22_cap30_s17.log`). The pipeline trains → benches
  (`research/bench-n6/benchv2_g22cap30s17.json`) → dev panel
  (`research/gen22/dev_audit_s17.json`) → judges
  (`research/gen22/screen_s17.json`), each gated on the previous
  step; ETA ~16:45 for PIPELINE DONE. If the trainer dies,
  re-running the pipeline script resumes from
  `research/gen22/weights/cap30_scratch_seed20261117_state_latest.pt`.
  Judge now also enforces seed identity + full 8×4×4×2 dev grid
  (Astra's final-review gaps); 41 tests green.

## Next actions (in order)

1. **When `/tmp/gen22_s17_pipeline.log` says PIPELINE DONE**: read
   `research/gen22/screen_s17.json`; write `research/gen22/results.md`
   (VAL/bench/dev table vs Gen19 s17, gradient-diagnostic summary
   from the train log `grad_diag` records, verdict ADVANCE/FAIL);
   fill the SUBMISSION placeholder; prepend STATUS; update this
   file; commit the final weights, train log, bench, dev JSON,
   screen JSON (not `*_step*.pt` / `*_state_*.pt`); push.
2. **Astra xhigh review of the Gen 22 screen** (+ final SUBMISSION
   check) if time allows before 19:30; file verbatim + disposition.
3. If ADVANCE: seeds 18/19 replication is the next step (tomorrow).
   If FAIL: file the null; Gen 23 = compressed spectral 5·L_CS.
4. By 20:00: final commit + push; `git status` shows only
   intentionally-untracked files (interim `*_step*.pt`,
   `*_state_*.pt`, `*_val_partial.json`, aborted-run ckpts, local
   audio, pre-existing `bench_v2_gen17_control10.json`).

## Key files map

| What | Where |
|---|---|
| KPI contract + scorecard | `research/bench-n6/KPI.md`, `kpi_scorecard.py` |
| Bench / spatial / vocoder | `research/bench-n6/bench_v2.py`, `spatial_bench.py`, `vocoder.py` |
| Listening pack (gated) | `research/bench-n6/listening_pack.py` |
| Best model (Gen 19) | `research/gen19/{train8.py,results.md,weights/}` |
| Gen 21 trainers/logs | `research/gen21/{train10.py,prereg.md,results.md,judge_replication.py,weights/}` |
| Gen 22 (capped SI-SDR) | `research/gen22/{prereg.md,train11.py,judge_screen.py,astra-prelaunch-review.md,smoke/}` |
| Astra reviews | `research/gen19/astra-review-gen19.md`, `research/gen20/astra-review-gen20.md`, `research/gen21/astra-{interim-review,review-gen21}.md` |
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
