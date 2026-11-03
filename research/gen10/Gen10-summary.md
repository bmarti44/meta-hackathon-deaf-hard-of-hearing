# Gen 10 summary — synthesis of `research/gen10/`

> **Model routing (GOAL §9).** Synthesis requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> GOAL **v2.3**: no generation cap, no loop stop. **Authority:**
> agent synthesis = triage only. Human dual extraction,
> protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: Gen 10 takes the build decision Gen 9 left to
> humans, on paper — and moves no scored cell, as its own
> fences require. J4 names the A1 build (Goehring-class
> frame-causal masker, retimed 20/10 → 8/4 ms, T0 latency
> floor 8.0 ms) and scores, conditionally only, at
> 0 FAIL / 6 INSUFFICIENT — its parent J2 cell-for-cell.
> Goehring 2017/2019 causality and effects are now
> full-text-proven and filed as 2 DESIGN ledger rows that
> cannot mint a score. Verdict on the generation's question
> (§3): NO — J4 is not the closest-to-movable lineage under
> either strict reading of "movable"; it is the most
> completely specified unfielded intervention in the
> program, which is a different property. `promoted FALSE`,
> FROZEN retained, G3b BLOCKED, validation set 0, zero
> Gen 0–7 cells move (mechanically diffed).**
> Inputs: [attack-causal-extraction.md](./attack-causal-extraction.md),
> [candidate-J4-causal.md](./candidate-J4-causal.md),
> [manifest-GEN10-J4.csv](./manifest-GEN10-J4.csv),
> [ledger-delta.csv](./ledger-delta.csv),
> [scoring/score-gen10.md](./scoring/score-gen10.md);
> prior: [Gen9-summary.md](../gen09/Gen9-summary.md),
> [causal-dnn-search.md](../gen09/causal-dnn-search.md).

## 1. Extraction closed — the causal evidence base is final at desk level

Gen 9's four desk-closures, closed at full text
(attack-causal-extraction.md; PMC efetch XML, OSF preprint,
arXiv + author code — inspected only):

- **Goehring 2017 NNSE** (N=14, blinded RM): **causal,
  proven** — gain from `[F_n, F_{n−1}]`, "current and past
  frames only"; stated 10 ms delay = derived 20 ms × 50%
  hop. Vs unprocessed ACE: speaker-independent
  **+1.4/+5.4/+0.4 NS** (SWN/ICRA/babble), speaker-dependent
  +2.3/+6.4/+2.0 dB. Paper CIs **not reported** (figure SEM
  only, not derivable). Noise-specific networks.
- **Goehring 2019 RNN-LSTM** (N=10): **causal, proven** —
  mask for frame *j* from *j−4…j*; ms latency unstated,
  derived **10–20 ms** (60 ms history, 0 future). Babble
  **+3.4 dB** (t(9)=7.2; agent-derived 95% CI [+2.3,+4.5]),
  traffic +2.0 dB NS (derived [−0.4,+4.4]). Paper CIs none.
- **Kang 2021**: SRT **N=7** (not 19); "about 6.0/2.2 dB"
  figure-grade only; causality **UNVERIFIED** (directionality
  never stated; STFT alone implies 16–32 ms if causal).
- **Gaultier 2024** (N=12): 1-mic is **bounded-lookahead, not
  causal** (Fig. 1 intra-chunk Bi-LSTM; ~15.6 ms chunk);
  2M/6M stated 4 ms future; 7.4-vs-7.6 resolves to **7.6 dB**
  from printed means (10.5−2.9).
- **Deep ACE**: **UNVERIFIED** for the evaluated model stands
  — paper states no padding/norm ("2 ms" = encoder length,
  the Schulz error; TCN RF 1531 frames ≈765 ms future if
  same-padded); author's code is flag-gated causal-capable
  but ships no paper config/checkpoint and its encoder leaks
  ~1 ms future even in causal mode.

Filed as [ledger-delta.csv](./ledger-delta.csv): the two
Goehring studies as DESIGN rows (`EXT-GOEHRING2017/2019`,
UNASSESSED, vs named *unprocessed* comparators, gaps to the
J4/J2 G2×W3 cell stated in-row) updating the Gen 8 ledger —
mechanically incapable of minting `delta_g2_db` (verified:
adapter 0 rows, no bare-number effect; score §1). The other
three file no row (noncausal/UNVERIFIED; Deep ACE already in
Gen 8). Standing fact, now desk-final: **exactly two
strict-causal models have human CI SRT data, one lineage,
both vs unprocessed in adults** — and that is all a ledger can
ever say. Human dual extraction/GRADE still owed on both
rows; it grades the ledger, never J4.

## 2. J4 scored — conditional 0/6, parent-identical

[candidate-J4-causal.md](./candidate-J4-causal.md) (mutation
M-J4-1: *name the A1 build*; J2 comparator/stages/kills and
J3 bench B1–B10 inherited verbatim) specifies one build:
16 kHz, W=128 (8.0 ms, right-aligned, no centre padding),
H=64 (4.0 ms), L=0 future, K=5 (*j−4…j*), 2×128 unidirectional
LSTM + sigmoid mask, causal-only normalisation (per-frame or
cumulative; `gLN`/BiLSTM/`same`-padding/attention barred as
desk-kills), envelope masking before ACE, no waveform
resynthesis. §3 T0 budget (arithmetic shown, re-verified in
the candidate run): `T_alg = 8.0 + 0 + 0 = 8.0 ms` floor;
**2.0 ms** headroom to B1 (p99 ≤10 ms), 12.0 ms to B2;
24.0 ms total past-only receptive span (vs Schulz 765 ms of
*future*); at PROPOSED B=64: 238,656 params, 59.4 MMAC/s.
Compute/IO/ACE-RF and **all** power figures UNMEASURED by
design. The retiming is stated, not smuggled (§2.4): at
20/10 the window term alone (20.0 ms) equals B2 before any
compute, so the as-published framing cannot pass B1 on any
hardware — and 2019's SRT therefore **does not transfer** to
the 8/4 retrain. T0's only scored work is negative: it
desk-kills both neighbouring designs without hardware.

Scoring ([scoring/score-gen10.md](./scoring/score-gen10.md),
stock adapter + track-map, candidate-filed manifest scorer,
27 tests OK + ASTRA PASS, code unedited): **conditional
single-candidate run only** — G1 NA‡, G2–G6 INSUFFICIENT,
**0 FAIL / 6 INSUFFICIENT, numerics NA, `promoted FALSE`**,
§(f) all required cells present. Adapted J4 ≡ adapted
GEN6-J2 modulo ID (mechanically verified). Combined audit:
370-row Gen 0–7 main matrix **unchanged** (`MOVED = []`);
forced 378-row probe (withheld) would make J4 the 17th entry
at joint-best 0/6 — its print position is the name tie-break,
and unfielded candidates quote no fitness. Kills
K-J4-0/K1/K-J4-2/K-J4-3/K-J4-4 all **unevaluated** — no build
exists for any of them to bite on.

## 3. Is J4 the closest-to-movable lineage? No — with one named distinction

"Movable" is not a GOAL term; two strict readings cover what
it can mean in this repo, and J4 wins neither:

**Reading A — closest to a cell legitimately changing to
PASS.** *No lineage is close, and J4 is mid-pack at best.*
Promotion additionally requires joint G2–G6 PASS at
≥Moderate human-verified GRADE including G3b — and **G3b is
BLOCKED for every candidate** (scorer-forced INSUFFICIENT),
so Reading A is currently unwinnable program-wide regardless
of J4 data. Even for a single G2 cell, J4's chain is long and
strictly sequential: Bench (Stage 0) moves no G-cell **by
design**; adult Stage 1 is T3 provisional/kill-only; the
first cell that could move is pediatric Band-A G2 at Stage 2
(T4) — three human-gated stages after a build that does not
exist, against SCAN 2 (not unprocessed), with an honest prior
the candidate itself prints as weak (+0.4 NS and +3.4 dB vs
*no front-end*, the latter at framing J4 abandons).

**Reading B — closest to a decisive readout (a kill or
precision verdict from the next executable step).** Still no:
**P7 (P-lineage) is closer on step count.** P7 is already
fielded at joint-best 0/6; its next readout needs HP-P7-1..3
pins + centre/EHDI microdata linkage, then one retrospective
analysis (zero enrolment, zero build, zero bench) that can
kill its branch on paper (Gen7-summary §3.1). J4's first
decisive readout (K1 at the bench) needs every blocker in
ranks 1–5 below first — including *training a model*.
SONIX/I-lineage (calendar-bound, est. 2027-12, HP-MON sealing
owed) and QR4 (lab Stages 0→1 to retire a Track-R G4-AAV leg)
are further still on this reading, and neither promotes.

**The distinction J4 does hold** — stated precisely so it is
never inflated into the claim above: J4 is the program's
**most completely specified unfielded intervention and its
only benchable one**. It is the sole lineage whose identity
unknown that killed its predecessor (causality) is now
settled by construction + a pre-filed Δ=0 audit, whose
external precedent class has proven-causal human CI SRT data
(§1), and whose next measurement after the pins is a bench
number (latency/power/sync) rather than a trial readout, a
microdata linkage, or new biology. "Closest to measurable"
is not "closest to movable": the bench decides K1 only, and
specificity has never moved a cell in eleven generations.

### Exact remaining blockers, ranked (gating order; each blocks all below it)

0. **Universal (all lineages):** G3b BLOCKED — qualified
   instrument/MCID via stakeholder co-design absent; plus
   human dual extraction + ≥Moderate GRADE verification,
   H-1…H-8, protocol/freeze/held-out. No J4 result at any
   stage promotes, or PASSes any cell, while rank 0 stands.
1. **HP-J1-4 fielding ruling** (G1=NA for the J-lineage).
   Until it signs J4 does not exist as a scored candidate
   (this score is conditional); denial withdraws
   J1/J2/J3/J4 together. *Gates everything J.*
2. **Manifest/class ratification** of candidate-filed
   [manifest-GEN10-J4.csv](./manifest-GEN10-J4.csv) +
   regulatory class named at human freeze (device-software
   investigational build); FTO/patent status flagged
   **not inspected** (candidate §7) — research-use only.
3. **HP-J4-1 architecture freeze:** exactly one primary
   topology (LSTM vs 2017-NNSE fallback — both-trained =
   two builds, selection on validation = held-out breach);
   filterbank/`B` (64 PROPOSED, Goehring band particulars
   not re-inspected Gen 10); norm choice; state-reset/
   priming; dual-mic stratum Y/N. Then **HP-J2-3** (locked
   build/weights-hash process).
4. **HP-J4-2 training freeze + actual training:** mask
   target/loss (incl. mandatory quiet-identity term),
   corpora + licences, talker/corpus/noise partition
   committed *before* training (≥1 whole noise class + 1
   corpus held out), SNR/level/reverb grid, seeds/hashes —
   producing locked weights (today: none; validation set 0).
   Then **K-J4-0 desk audit** on the real graph (index bound
   ≤ `jH+W−1`; norm statistics ⊆ frames ≤ *j* read from
   source; Gen 9 suffix-replay prefix Δ **exactly 0**).
5. **HP-J3-1 bench freeze + HP-J3-2 blanks** (B4 dropout/
   recovery, B6 bilateral sync — bench must not run
   bilaterally with B6 empty, B7 relative battery-loss %,
   B9 level tolerance; + HP-J1-3 sync spec, HP-J3-3) → J3
   Stage 0 on H-primary (external hardware access itself an
   unmet dependency): measured B1–B10 fills **HP-J2-1**,
   decides **K1 only**, moves no G-cell. Live risk priced at
   T0: 250 frames/s must fit inside 2.0 ms of B1 headroom.
6. **Stage 1 adult bridge prerequisites:** HP-J2-2
   comparator file (per-user SCAN 2/ForwardFocus state as
   fitted; AB IFU stratum decision), HP-J2-4 music battery,
   HP-J2-5 alarm battery, **HP-J4-3** pilot variance →
   locked N (no N assertable today — Goehring N=14/10 barred
   as variance sources) → Stage 1 vs C-J2: **K-J4-2**
   (primary SRT <3 dB, or 95% CI failing to exclude 0 and
   the <3 dB region at locked N, kills before any child is
   recruited) + **K-J4-4** NI bundle.
7. **Stage 2 pediatric decider** (HP-J2-6 N; Bands A/B as
   J2): **K-J4-3** Band-A <3 dB vs C-J2 retires the lineage
   claim (no Band-B rescue; no re-powering after seeing the
   estimate). *First point in the entire chain where a G2
   cell could move* — to PASS only with rank 0 also cleared.
8. **Stage 3 / remaining gates:** G3a trajectory separately
   frozen (SRT→language mediation UNRESOLVED); G4 B8
   bench-verified per build; G5 per-harm NI measured (alarm/
   localisation/wear-time); G6 datalogged wear-time/battery/
   visits + testability coverage by §3.2 stratum (App. D
   numerators still unpinned — no coverage % assertable).

Off critical path (named, not blockers): Goehring 2017 CI
digitisation; Gaultier JASA-vs-preprint wording; Deep ACE
journal separator spec; Kang author code — desk residue that
grades ledger rows and moves nothing (attack, Unresolved).

## 4. Next executable pushes

1. **HP-J1-4 ruling (human; rank 1).** Gen 10 completes its
   brief: the bench now has a named, T0-priced, audit-ready
   A1 to rule on. No further prose J generation substitutes.
2. **If signed: HP-J4-1/2 freezes → train → K-J4-0 audit →
   HP-J3-1/2 → Stage 0 bench** (ranks 3–5). First measured
   latency/power in the program; decides K1, nothing else.
3. **Human queue otherwise unchanged:** HP-P7-1..3 +
   microdata (Reading-B leader, §3); HP-MON-1..3 sealed
   before SONIX opens (NCT07627971, next check 2027-02-03);
   QR4 Stages 0→1; ledger dual extraction/GRADE (now 9 rows:
   Gen 8's 7 + Gen 10's 2); G3b co-design (rank 0 — the only
   structural promotion bar no generation can design around).
4. **Optional T0 (repo-executable, zero cell value):** Gen 9
   replay completions (chunk sweep, real-speech A2 ceiling
   metrics) — they price the offline oracle J4's bench screen
   reports against; they license nothing.

## 5. Loop state

**No PASS, no winner — and under v2.3, no stop.** Eleven
generations filed (0–10), eight with main-matrix scoring
(0–7) plus conditional J runs (Gen 5/6/10); combined main
matrix 370 rows, zero PASS, zero lexicographic improvement
over Gen 0's joint best. Gen 10's yield is the conversion of
Gen 9's open choice into a ruled-on-able object: one causal
build spec, two ledger rows, one conditional score, eight
ranked blockers — every one of them human-held or
measurement-owed. **D1–D17 carry verbatim.** FROZEN
retained. G3b BLOCKED. Validation set 0.

*End. Gen 10 under GOAL v2.3 (no cap, no stop). Closes the
causal-evidence desk, names and conditionally scores the A1
build, answers "closest-to-movable" in the negative with the
blockers ranked, and leaves every gate where it was.*
