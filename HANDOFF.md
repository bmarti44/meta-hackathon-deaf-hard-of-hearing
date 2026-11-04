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
- Tests (23 green at handoff):
  `/tmp/gen9env/bin/python -m pytest research/bench-n6/ research/gen20/ research/gen21/ -q`
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

## Current state (2026-11-04 13:10 — VERIFY, may be stale)

- Gen 21 (S48 = 48k scratch vs R48 = Gen19 parent + 24k
  restart, paired data via RNG handoff at 24k) — pre-reg:
  `research/gen21/prereg.md`, results: `…/results.md`.
  Seed-17 screen: both ADVANCE on VAL (S48 1.005, R48 0.880
  @−5 vs parent 0.564). Bench @−5 seed-17: S48 0.93, R48 1.20
  (parent 1.06). Dev diagnostic (128 paired items @−5):
  S48 +0.453, R48 +0.322 over parent, all 8 targets positive.
- Seed-18 pair DONE and benched: VAL gains vs its strong
  parent (1.006): S48 −0.158, R48 −0.042; bench @−5 gains:
  S48 −0.436, R48 −0.266 (parent bench file
  `benchv2_gen19s2.json`, candidate `gen19s2`, @−5 = 1.356).
- **Seed-19 S48 was KILLED at step 12,500 (12:57) when the
  previous session ended** (no process left; no full state
  before 24k, so no exact resume). Relaunched from scratch,
  same seed, at 13:00 as a detached `nohup` chain
  S48s19 → R48s19 (logs `/tmp/gen21_s48s19.log`,
  `/tmp/gen21_r48s19.log`, chain markers
  `/tmp/gen21_chain_s19.log`). Rerun losses are bit-identical
  to the killed run (checked steps 100–225), so this is a
  faithful replay, not a protocol change. Killed-run
  artifacts kept untracked in
  `research/gen21/weights/aborted_s48s19_run1/`.
  ETA: S48s19 ~15:32, R48s19 ~16:40.
- Judgment script committed: `research/gen21/judge_replication.py`
  (reproduces filed seed-17/18 numbers exactly). 2-seed means:
  VAL S +0.141 / R +0.137; bench S −0.281 / R −0.064.
  Acceptance needs 3-seed means ≥+0.30 on both panels →
  **expect NEITHER arm to qualify**; do not pre-judge in
  writing until seed-19 finals are benched.

## Next actions (in order)

1. **When R48s19 prints DONE** (~16:40; check `/tmp/gen21_chain_s19.log`): bench seed-19
   registered checkpoints (`bench_v2.py --n-per-cell 6`):
   `s48_seed20261119{,_step24000,_step36000}.pt`,
   `r48_seed20261119{,_step36000}.pt` → separate JSONs in
   `research/bench-n6/` named like the seed-18 ones.
2. **Full 3-seed judgment** per `research/gen21/prereg.md`:
   unrounded VAL gains vs each seed's own parent (parent raw
   −5 values: s17 0.5641/0.0091, s18 1.0061/0.0134, s19 from
   its R48 val_log step 0 items); bench @−5 gains vs
   `bench_v2_gen19.json` (gen19), `benchv2_gen19s2.json`
   (gen19s2), `benchv2_gen19s3.json` (check meta for name).
   Acceptance per arm: mean gain ≥+0.30 on BOTH panels,
   non-worsening mean STOI @−5, positive in ≥2/3 seeds,
   0 dB safeguards (≤0.15 dB / 0.003 STOI degradation),
   quiet safeguards. Scratch preferred only if S48−R48
   ≥0.15 on both panel means. A failed R48 is NOT accepted
   by default. Run `python research/gen21/judge_replication.py --out
   research/gen21/replication_judgment.json`.
3. **Only if an arm qualifies**: `spatial_bench.py` on its
   48k finals (hash-matched) + `kpi_scorecard.py` with that
   arm's three 48k-final benches ONLY (never 3 checkpoints of
   one seed). If all 14 required rows pass: fresh-material
   confirmation (Astra's package in
   `research/gen19/astra-review-gen19.md`) still gates any
   listening test; `listening_pack.py` needs hash-binding
   work first and must run WITHOUT `--allow-unpassed`.
4. File the replication section in `research/gen21/results.md`,
   prepend `STATUS.md`, fill the `[REPLICATION VERDICT]` line
   in `SUBMISSION.md`, update this file, commit + push.
5. **Astra xhigh review** of completed Gen 21 + SUBMISSION.md
   accuracy; file verbatim + disposition.
6. **Gen 22** (Astra ranking, one change at a time, seed-17
   screen then 18/19, +0.30 both-panel bar): (1) 30 dB
   soft-capped SI-SDR loss — the one-line denominator change
   is quoted in her review; (2) compressed spectral
   5·L_CS (256/512/1024 STFT, exp 0.3, 0.7 mag/0.3 complex);
   (3) SNR concentration 60% U(−5,−2)+40% U(−2,10) with
   paired draws; (4) STOI auxiliary only as repair;
   (5) 4 s crops. Budget/policy = whichever Gen 21 selects
   (R48→24k continuation, S48→48k scratch, neither→24k
   scratch). Copy the relevant trainer (`gen19/train8.py` for
   scratch, `gen21/train10.py` modes for continuation),
   pre-register first, smoke-test, test before launching.
   **Deadline caveat: only launch a Gen 22 screen today if it
   can train+bench+file by 19:30; otherwise preregister +
   smoke and state it as next step.**
7. Before 20:00: final commit + push; `git status` should
   show only intentionally-untracked files.

## Key files map

| What | Where |
|---|---|
| KPI contract + scorecard | `research/bench-n6/KPI.md`, `kpi_scorecard.py` |
| Bench / spatial / vocoder | `research/bench-n6/bench_v2.py`, `spatial_bench.py`, `vocoder.py` |
| Listening pack (gated) | `research/bench-n6/listening_pack.py` |
| Best model (Gen 19) | `research/gen19/{train8.py,results.md,weights/}` |
| Gen 21 trainers/logs | `research/gen21/{train10.py,prereg.md,results.md,weights/}` |
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
