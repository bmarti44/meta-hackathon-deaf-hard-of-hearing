# Gen 8 summary — synthesis of `research/gen08/`

> **Model routing (GOAL §9).** Synthesis requested: **xhigh**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> GOAL **v2.3**: no generation cap, no loop stop. **Authority:**
> agent synthesis = triage only. Human dual extraction,
> protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: Gen 8 executed Astra (codex-unstick-2) ranks 1
> (identity half) and 3, plus the evidence ledger Astra asked
> for — and moved no scored cell, as all three inputs predicted.
> The cited DNN checkpoint is NONCAUSAL as serialized
> (`causal=False`, `gLN`, kernel/stride 32/16 — direct pickle
> inspection, no execution). Kim et al. verifies as a real
> post-CI OHC cohort (exact child-level 5/5 vs 0/6,
> p=0.002165) and moves no Q0/G4 cell. The 7-row external
> ledger is filed mechanically incapable of minting a scorer
> `delta_g2_db`. No candidate, manifest, or scoring run;
> `promoted FALSE`, FROZEN retained, G3b BLOCKED,
> validation set 0.**
> Inputs: [attack-checkpoint-identity.md](./attack-checkpoint-identity.md),
> [attack-kim-dpoae.md](./attack-kim-dpoae.md),
> [external-evidence-ledger.csv](./external-evidence-ledger.csv),
> [ledger-note.md](./ledger-note.md).

## 1. Checkpoint verdict — NONCAUSAL, resolved (Astra rank 1)

`cankeles/ConvTasNet_WHAMR_enhsingle_16k` (Schulz 2026 §2.4,
"without further modification") serializes in its own
`model_args`: **`causal=False`, `norm_type='gLN'`,
`kernel_size=32`, `stride=16`**, `asteroid=0.5.2`,
`torch=1.10.0+cu111`. Method: hash-verified download
(20,122,511 B; SHA-256 `a96014fc…b9026a` = HF LFS oid,
binary unchanged since 2022-02-15) + stdlib
`pickletools.genops` disassembly of `archive/data.pkl` — no
`torch.load`, instantiation, or inference. Either property
alone defeats streaming identity under Asteroid 0.5.2
(symmetric padding; segment-wide `gLN`); the checkpoint has
both. Recomputed masker future context: 765 latent frames ×
16 samples = **765 ms**, superseding unstick-2's 382.5 ms
(card stride 8). Both the HF card and Schulz's 16/8 + "1 ms
look-ahead" misdescribe the cited binary. Consequences:
J3 **B3 cannot be met by this checkpoint**; it is admissible
only as J3 **A2 (offline oracle/ceiling reference)**. Flipping
the flag is not a repair — weights trained with symmetric
context + global norm make a causal rebuild a new, unmeasured
model. Schulz's 5.9 dB stands as offline-processing external
evidence, not evidence any streaming build preserves it.
Residual (named, not settled): Schulz runtime overrides /
chunk length / compute versions are unreported in the paper.

## 2. Kim verdict — pointer verifies, no cell moves (Astra rank 3)

Kim et al., *MedComm* 7(9):e71006 (PMID 42719247,
PMC13555795), retrieved via NCBI PMC XML + Europe PMC XML
+ supplement/Figure 1 (publisher PDF 403 — nothing depends
on it). Per-child/ear extraction (11 bilateral *OTOF*
children, 16 assessment rows) replaces unstick-2's bound
with an exact count: child-level any-ear detectable
**5/5 (≤12 mo) vs 0/6, Fisher p=0.002165**; authors' ear-level
7/10 vs 0/12 (recomputed p=0.00070; 6/10 under latest-row
counting — finding F1, which row entered their analysis is
unstated). Strict figure "Regeneron Yes": only **2/10 early
ears (2/5 children), p=0.182 NS**. Middle-ear status and
per-ear pre-op baselines unreported (negative ears
individually uninterpretable; bias is downward). Age /
duration / era / electrode fully confounded — no 12-month
threshold claim. **Q0/G4 verdict VERIFIED, no move:**
`G,G4,ALL,OTOF` stays INSUFFICIENT; DPOAE supplies no patency
(Q0-P), no post-CI transduction/ABR (Q0-A; OHC ≠ IHC target),
no PTA-shift, density/count, fibrosis, or G4-AAV evidence.
Ledger-only change: "no post-CI hair-cell function" is now
inspected-false as a universal for OHCs in the early subset.

## 3. Ledger filed — external ≠ scoreable

`external-evidence-ledger.csv`: **7 rows × 14-col schema**,
all `grade=UNASSESSED`, `verdict_proposed=INSUFFICIENT` —
Schulz 2026, Borjigin 2024, Gajecki 2023, Fused Deep ACE v1,
DB-OTO/CHORD, Cheng JAMA Fig. 3B and 3C, each `effect` in
source units vs its *named external comparator* with the
external-vs-cell gap in `claim`. Guards verified by
execution: `EXT-*` keys have no track-map entry
(`adapt()` = 0 rows), no bare-number effect, file not named
`extract-*.csv` — no `delta_g2_db` (vs-frozen, ranking-
consumed even on INSUFFICIENT) can be minted; Astra's ban on
inserting Schulz 5.9 (and Cheng 6.3, Borjigin pp→dB) holds.
Human dual extraction + GRADE pending on all 7 rows.
**Staleness note:** `ledger-note.md`'s closing limits still
call the checkpoint "unverified / 382.5 ms conditional" —
superseded the same day by §1 above (765 ms, serialized);
the ledger CSV itself carries no checkpoint number and is
unaffected. GOAL.md and all `extract-*.csv` untouched.

## 4. Next executable pushes

1. **Checkpoint replay (T0 quantification only).** Identity
   no longer needs execution; replay would only quantify
   common-prefix perturbation and offline objective metrics,
   and price causality against a future causal build. Zero
   clinical PASS expected. **Exactly what is needed, none
   currently in place except a scratch weights copy:**
   - *Weights (re-obtain, pin, do not rely on `/tmp`):*
     `cankeles/ConvTasNet_WHAMR_enhsingle_16k` @ HF sha
     `f47048ac…73c3024`, `pytorch_model.bin` 20,122,511 B,
     SHA-256 `a96014fc1ddf…3b9026a`. A verified copy sits at
     `/tmp/cankeles_pytorch_model.bin` (session scratch,
     not repo-filed); re-download and re-hash before use.
   - *Runtime (absent here — verified 2026-11-03: Python
     3.14.8, `import torch` → ModuleNotFoundError; no
     torch/asteroid installed):* a project-local env with
     **PyTorch (CPU suffices for the prefix test), Asteroid
     (for the `serialize()`/`from_pretrained` format),
     NumPy/SciPy + an audio I/O lib**. Checkpoint records
     torch 1.10.0+cu111 / asteroid 0.5.2 / PL 1.4.9, which
     will not install on Python 3.14 — so either an older-
     Python pinned env reproducing those versions, or
     modern torch/asteroid **with a filed check that the
     reconstructed `model_args` match the serialized table
     in attack §2 before any number is trusted**; pickle
     loading under modern `weights_only` defaults must be
     handled explicitly. Until one route runs, replay is
     unexecuted, not approximated.
   - *Inputs & harness:* licensed public clean speech +
     noise, held-out speakers/noises, fixed seeds/hashes;
     same-prefix/different-suffix test at multiple chunk
     lengths (to expose `gLN` segment dependence), metrics
     reported as T0 per Astra (stationary / competing
     talker / alarm / clean separately; SI-SDR/STOI ≠ SRT).
   Formal J3 benching of any *causal A1* build remains
   separate and still gated on HP-J1-4 + HP-J3-1/2.
2. **Causal rebuild decision (J-lineage).** A `causal=True`
   + cLN/cgLN retrain is a new model (training corpus +
   compute + locked weights hash); its benefit is unmeasured
   until 1. prices the offline ceiling and a J3 bench runs.
   No prose J generation substitutes for either.
3. **Correct-comparator adult study (Astra rank 2, not
   executed in Gen 8).** Needs a proven-causal build (push 2),
   Schulz paired raw data / missingness reconciliation, and a
   human team/rig under HP-J1-4 study pins. Not executable
   from this repo; no messages sent.
4. **Kim follow-ons (cheap, bounded).** Re-extract
   Santarelli 2024 directly (this pass used Kim's
   characterisation only); carry Kim's ear-level anchors
   (detectable fraction only in the ≤12 mo / short-duration /
   slim-array corner; frequent within-child ear discordance)
   into QR4 post-CI model choice. F1 counting-row question
   is author-query territory; neither moves a cell.
5. **Human queue unchanged from Gen 7 §3:** HP-P7-1..3 +
   microdata; HP-J1-4 (then HP-J3-1/2); HP-MON-1..3 before
   SONIX (NCT07627971, est. 2027-12; next monitoring check
   2027-02-03); QR4 Stages 0→1 + licensed full texts; human
   dual extraction/GRADE for the §3 ledger.

## 5. Loop state

Gen 8 files no scored candidate, so the combined matrix is
unchanged by construction: 370 Gen 0–7 rows, zero PASS,
`promoted FALSE`, zero lexicographic improvement over
Gen 0's joint best — now nine generations filed (0–8),
eight of them scored. **D1–D17 carry verbatim.** No ranking
is a winner; external benefit ≠ project PASS; doses /
thresholds absent from inspected records stay blank;
Q0 UNDECIDABLE-no-data (Q0-P/Q0-A untouched by §2);
H harm not cleared. **FROZEN retained. G3b BLOCKED.
Validation set 0. No PASS, no winner — and under v2.3, no
stop:** the loop continues on pushes 1–5 above, human pins
first where they gate.

*End. Gen 8 under GOAL v2.3 (no cap, no stop). Scores
nothing; resolves one implementation identity, verifies one
physiology pointer, files one non-scoreable ledger.*
