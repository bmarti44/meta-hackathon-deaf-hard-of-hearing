# Gen 9 summary — synthesis of `research/gen09/`

> **Model routing (GOAL §9).** Synthesis requested: **xhigh**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> GOAL **v2.3**: no generation cap, no loop stop. **Authority:**
> agent synthesis = triage only. Human dual extraction,
> protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: Gen 9 closes both Gen 8 DNN unknowns without
> moving a scored cell. Strictly causal models WITH human CI
> SRT data exist — two, both Goehring filterbank mask/gain
> designs, neither ConvTasNet-class. The executed Schulz/Keles
> replay quantifies Gen 8's serialized NONCAUSAL verdict: a
> future suffix rewrites every sample of the shared past,
> from sample 0. No candidate, manifest, or scoring run;
> `promoted FALSE`, FROZEN retained, G3b BLOCKED,
> validation set 0.**
> Inputs: [causal-dnn-search.md](./causal-dnn-search.md),
> [attack-replay.md](./attack-replay.md),
> [gen9_replay.py](./gen9_replay.py),
> [replay-output.txt](./replay-output.txt);
> prior: [Gen8-summary.md](../gen08/Gen8-summary.md),
> [candidate-J3-bench.md](../gen07/candidate-J3-bench.md).

## 1. Causal-model verdict — YES, two, one lineage, narrow

**Strict frame-causal + human CI adaptive-SRT data: exactly
two models found**, both inspected at full text:

- **Goehring 2017 NNSE** (PMC5256482): gain from current +
  past frames only, 10 ms stated delay. N=14 CI. Vs
  unprocessed ACE, speaker-independent SRT **+1.4 dB (SWN),
  +5.4 dB (ICRA), +0.4 dB NS (babble)**; speaker-dependent
  +2.3/+6.4/+2.0 dB. Noise-specific training.
- **Goehring 2019 RNN-LSTM** (PMC6773603): mask for frame *j*
  from frames *j−4…j* only. N=10 CI. Vs unprocessed:
  **+3.4 dB babble (sig.), +2.0 dB traffic (NS)**. End-to-end
  ms delay not numerically stated.

Nearest neighbours, all excluded from "strict-causal CI SRT":
Gaultier & Goehring 2024 (N=12 CI SRT +2.3 dB 1-mic, up to
+10.3 dB 6-mic) is **low-latency bounded-lookahead** (~15 ms /
4 ms future), not causal. Deep ACE/Fused (N=8/5 CI) causality
**UNVERIFIED** — no padding/norm in inspected text; "2 ms" =
encoder length (the Schulz error); fixed-SNR WRS, not SRT.
Kang 2021 UNVERIFIED (directionality/N unextracted).
Borjigin 2024 (N=13) and DCCTN (N=4) have CI data but are
explicitly/by-construction noncausal. Schulz 2026 is proven
noncausal (§2).

**Direct negative:** no causal ConvTasNet, DeepFilterNet,
DPCRN, or CRN with *any* human CI evaluation surfaced
(PubMed/HF/arXiv, 2026-11-03). Causal ConvTasNet configs
exist (Luo cLN; arXiv:2103.14882) — objective-only, N=0 CI.
DeepFilterNet3 is lookahead=2, N=0 CI. Healy's effectively-
causal GCRN is HI, not CI; Mamun 2019 causal CNN is
objective-only. All causal positives are vs **unprocessed**,
adults, 1–2 noise classes — none vs a commercial front-end,
none pediatric, none quiet-noninferiority. Ranks 1–2 do not
predict a causal-ConvTasNet retrain's SRT cost.

## 2. Replay result — executed, future rewrites the past

Gen 8 §4 push 1, executed (T0 only). Modern route:
Python 3.11.17, torch 2.15.0 / asteroid 0.7.0 in
`/tmp/gen9env`; checkpoint re-downloaded at pinned HF rev
`f47048ac…`, 20,122,511 B, SHA-256 `a96014fc…3b9026a`
**exact match**; `model_args` identical to Gen 8
(`causal=False`, `gLN`, 32/16); `load_state_dict(strict=True)`
all keys matched, 5,000,881 params; asteroid 0.7 `gLN`/
padding semantics verified same as 0.5.2.

Identical 1 s prefix, differing 1 s suffixes, one 2 s
forward each (synthetic 16 kHz, CPU): identical-input
control RMS Δ = **exactly 0**; zero-vs-loud suffix inside
the shared prefix: **16,000/16,000 samples differ, first
at sample 0**, rel. RMS **0.593**, prefix SNR **4.53 dB**;
in [0, 0.235) s — >765 ms before the suffix, beyond
convolutional reach — rel. RMS **0.783** (2.13 dB),
consistent with segment-wide `gLN` (architectural
inference; no ablation run). Zero-vs-tone rel. 0.119;
continuation-vs-loud 0.566. A causal system must give 0.
This **prices** noncausality; identity was already settled
by the serialized args.

Not run: pinned torch 1.10/asteroid 0.5.2 numerics,
chunk-length sweep, real speech, SI-SDR/STOI/SRT,
on-processor latency/power, causal rebuild. Output RMS
~10³ treated as arbitrary scale-invariant units (inferred);
only relative metrics interpreted. Checkpoint stays J3
**A2 offline reference only**; Schulz 5.9 dB stays offline,
ledger-only, unscoreable.

## 3. J-lineage state — ALIVE as protocol, DEAD as shipped build

| Piece | State | Needs |
|---|---|---|
| Schulz/Keles checkpoint as A1 causal build | **DEAD** — noncausal proven (Gen 8) + quantified (Gen 9); B3 (look-ahead = 0) unmeetable; flag-flip ≠ repair | Nothing. Retain only as **A2 offline oracle/ceiling** |
| Causal A1 build (any) | **DOES NOT EXIST** in-project; no causal ConvTasNet has CI data anywhere (§1) | New retrain (`causal=True` + cLN/cgLN *or* a Goehring-class per-frame design): training corpus, compute, locked weights hash (HP-J2-3) — a new unmeasured model |
| J1/J2 fielding | **UNFIELDED** | **HP-J1-4** human ruling (gates the whole lineage, or withdraws it together) |
| J3 Stage-0 bench (Gen 7 App. B) | **ALIVE, unscored, never run**; K1 unevaluated (not triggered, not cleared) | HP-J1-4, then **HP-J3-1** freeze + **HP-J3-2** thresholds (B4/B6/B7/B9 blanks), then HP-J3-3; fills HP-J2-1 measured latency/power — moves no G-cell |
| External causal CI evidence | **ALIVE, ledger-class** (Goehring ×2) | Human dual extraction/GRADE before any ledger use; vs-unprocessed adults only — cannot mint `delta_g2_db` or a PASS |

Standing state unchanged: `promoted FALSE`, FROZEN
retained, G3b BLOCKED, validation set 0, D1–D17 carry
verbatim, Q0 UNDECIDABLE-no-data. Gen 9 files no scored
candidate; combined matrix unchanged (370 Gen 0–7 rows,
zero PASS; ten generations filed 0–9, eight scored).

## 4. Next executable pushes

1. **HP-J1-4 ruling (human, gates everything J).** No bench,
   rebuild, or human stage is licensed before it. Gen 9
   sharpens its brief: the only causal-with-CI-SRT precedent
   is Goehring-class mask/gain, not TasNet-class.
2. **Causal-build decision (needs 1).** Choose and build A1:
   causal-ConvTasNet retrain vs Goehring-class design.
   Either is unmeasured; the replay's A2 numbers price the
   offline ceiling it must be compared against, not its SRT.
3. **J3 bench run (needs 1 + HP-J3-1/2 + a build).** First
   measured latency/power/sync (B1–B10); decides K1 only.
4. **Replay completion (T0, repo-executable now, optional):**
   chunk-length sweep to expose `gLN` segment dependence;
   real held-out speech objective metrics for A2 ceiling.
   Zero clinical PASS expected either way.
5. **Cheap desk closures:** Deep ACE journal-version
   padding/norm or code (causality stays UNVERIFIED until
   inspected); Kang 2021 full-text extraction (PMC8606413);
   Gaultier 7.4-vs-7.6 dB discrepancy. None moves a cell
   without human dual extraction.
6. **Human queue otherwise unchanged from Gen 8 §4.5:**
   HP-P7-1..3 + microdata; HP-MON-1..3 before SONIX
   (NCT07627971, next check 2027-02-03); QR4 Stages 0→1;
   ledger dual extraction/GRADE.

## 5. Loop state

**No PASS, no winner — and under v2.3, no stop.** Gen 9's
yield is decision-grade narrowing, not progress toward a
cell: the causal question now has a named positive class
(Goehring), a named empty class (causal TasNet-class in
CI), and a quantified dead checkpoint. The J-lineage's
next move is a human pin (HP-J1-4), not another prose
generation.

*End. Gen 9 under GOAL v2.3 (no cap, no stop). Scores
nothing; finds the only causal CI SRT lineage, executes
the noncausality replay, leaves every gate where it was.*
