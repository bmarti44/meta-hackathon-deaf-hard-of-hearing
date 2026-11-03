# Status log

Append new status here only, newest first within the relevant
section. Do not add status back to `GOAL.md`. Durable intent,
gates, and loop rules stay in `GOAL.md`.

---

## Current direction

GEN 15 DONE + BENCH RUN 2 (2026-11-03): causal waveform
Conv-TasNet-style model (602k params, exact causality, 5.88 ms
architectural latency) trained 2000 steps. First non-null
babble readout in the line: +1.14 dB SI-SDR (own eval, re-run
bit-identical) / +1.07 on bench-n6 — but babble STOI −.01,
post-selection ACE +0.011 CI crosses 0, quiet PESQ 3.11
regression. Bench verdict NO-GO; promoted FALSE. Waveform
objective plateaued after step 1000. Next: Gen 16 adds
ACE-envelope + quiet-identity loss terms, same bench/gates.

BENCH-N6 BUILT — NO-IMPLANT PROVING GROUND (2026-11-03,
holder direction: prove it without implants first; implantee
is holder's son, bilateral N6, holder not implanted):
research/bench-n6/ stages causal candidates through objective
bench (vs unprocessed + classical causal gate + oracle ceiling),
post-selection ACE readout, go/no-go gates, then NH vocoder
screening for the father; implant stage not authorized.
Run 1: classical gate babble-null (+0.04 dB); Gen15 waveform
interim step-500 first causal babble gain (+0.41 dB, CI>0) but
post-selection ACE null -> NO-GO for evidence listening;
labeled shakedown pack only. Codex Astra reviewed the plan
(sound; fixes applied same day). 8 durable tests green.
Next: re-bench Gen15 final checkpoint when training lands.

GOAL v2.3 — STOP RULES REMOVED, BROADEN + DEEPEN
(2026-11-03, holder direction): generation cap and §7
loop stopping rules deleted from GOAL.md; loop runs until
a legitimate win or holder directs otherwise. Kill criteria
+ FMEA safety stops kept. LOOP-EXHAUSTED (clock 4/4) is
superseded by this amendment. Codex Astra unstick mission
running in parallel. Next: broadened Gen 5 (new families +
deepened best lineages).

LOOP EXHAUSTED AT CLOCK 4/4 — GEN 3 + GEN 4 DONE
(2026-11-03): Gen 3 (P3/W3/QR3/AD3) and Gen 4 final
generation (P4/W4/QR4/AD4) each tied cell-for-cell
(matrices parent-reproduced). 13 Track-P pathways at
0/6, PASS still 0 across 322 rows. research/gen04/
LOOP-EXHAUSTED.md: no Gen 5 without (i) new external
evidence AND (ii) signed human clock amendment.
Reopening is human-owned (W1–W8). Sisyphus directive
executed to GOAL §7's own limit.

GEN 2 DONE — TIE AGAIN, CLOCK 2/4 (2026-11-02, holder
Sisyphus directive): sweep = 0 validation admissions
(PMID 42362868 AAV re-dose = late-found DESIGN hook).
4 candidates (P2 fused, H2 norming-only, Q1 Q0-decider,
R1 G4-AAV falsification); P2/H2 tie parents cell-for-cell
(matrix parent-reproduced); no-improvement counter 2/2,
STOP still not met (gaps conjunct). Next: Astra judge,
then Gen 3 as attack execution (not new designs).

WIN-PATH PACKET FILED — BALL WITH HUMANS (2026-11-02):
research/win-path/ (W1–W8 action list, W2 G3b brief,
W3 extraction checklist). Agent-doable loop work is
exhausted: every remaining step to a legitimate win is
human-owned (fund/name roster, G3b co-design, dual
extraction, re-freeze, primary data). Loop will re-score
immediately when human-verified evidence lands.

CODEX ASTRA REVIEW DONE + SCORER FIXED (2026-11-02):
reviews/codex-astra-external-review.md (gpt-6-astra)
UPHOLDS no-winner (independent re-run + cell adjudication);
found (a) 5 adult-archival rows miscoded T4, (b) gate_table
aggregation could permanently block a legit G2 PASS and
didn't enforce tier/GRADE. Fixes applied by parent:
gate_table v2 (mechanism-only G2 W0/W1 excluded; PASS
requires ≥Moderate + Appendix A min tier; Astra probes in
test_astra_probes.py pass; Gen 0 matrix unchanged);
extraction_v2 (T4→T3 ×5, 48 unrowed joined, verdicts
identical). Astra's top win lever: funded G3b co-design
project (human-owned). Remaining path to any win is
W1–W8 human actions — agent loop has no further
gate-moving work until humans act or new data appears.

GAP ROUND 2 DONE + CODEX ROUTE APPROVED (2026-11-02):
Round 2: FDA PDFs verified MD5-exact (Otarmeni USPI 16pp,
MED-EL 7mo, AB 12mo resolved, WHO grades; Seyyedi rubric
verbal-only); A1 v2 model (10 tests OK, parent-verified
MD5s; still UNEVALUABLE, not grid-converged); 48 unrowed
cells rowed; skeptic proved matrices byte-identical —
0 cells changed, no-winner stands. Win path W1–W8 (all
human-owned) in round2-summary §6. Holder approved Astra
(GPT-6 via Muse, probe ROUTE-OK) as §9 disclosed
substitution for independent judging. Next: Codex external
review of full loop.

GAP ATTACKS ROUND 1 DONE — 0 CELLS CHANGED (2026-11-02,
holder-directed continuation; Sol 6.1 retry: route rejected,
not in catalog — fallback continues): CDC EHDI 2022 PDF
extracted via pypdf (D1 documented ear-avg 810 = 0.228/1000
screened; P0 better-ear count still UNPINNABLE from
marginals, Fréchet [0,804]); 5 papers upgraded to full text
(Srinivasan N=6; Kamakura; Pfingst sequence; Dieter;
Keppeler); Q0 UNDECIDABLE stands (new find NCT07752888
post-CI AAV n=1, no results); A1 in-silico model run
(deterministic, parent-verified md5) but UNEVALUABLE +
skeptic Shannon-unit hit. Gen 2 NOT justified (no verdict
changed). Next: round 2 (PDF unlock → USPI/SSED, A1
convergence+units, unrowed cells). Win still requires
human gates (G3b, dual extraction, freeze).

STEP 5 DONE — NO WINNER, FROZEN RETAINED (2026-11-02):
research/Step5-decision-no-winner.md. No Track-P survivor
frozen; promotion impossible at v1 (G3b BLOCKED, human
extraction pending, pins unfrozen) and 0 PASS in Gen0+Gen1.
C0 untested (all cells INSUFFICIENT), Q0 UNDECIDABLE.
Deliverable = §5.1 open synthesis + prioritized designs
(Ga first). Not §12 abandonment (§7 stop not met; budget
not stated). Full loop Steps 0–5 complete; continuation =
human gates + gap attacks (§6 of decision), holder's call.

STEP 4 DONE — GEN 1 NO FITNESS IMPROVEMENT (2026-11-02):
5 Gen 1 designs from survivors only (P1 portfolio G+H+
A-standard, A1 kill-test, Ga, H1, F1m). Re-score: every
child ties its parent cell-for-cell (PASS 0; matrix
reproduced diff-clean by parent). Skeptic: H1 mutation
bundle-or-restatement; A1 specifiable-only. §7 stop (b)
counter 1/2, not met. Next: Step 5 decision.

STEP 3 DONE — GEN 0 SCORED, NO PASS, NO PROMOTION
(2026-11-02): gate matrix reproduced deterministically by
parent (gate_table diff-clean). 199 extraction rows; PASS 0,
FAIL 7 (completeness/staging/presumptive only), rest
INSUFFICIENT/NA. Q0 = UNDECIDABLE-no-data (thresholds
unmoved). B KILLED as specified (lifetime/refill arm;
lenient reversal D11 preserved for human panel). A/F/G/H
kills unevaluable. C/D Track-R watch, E parked. Lex ranking
P: F>G>H>A>B (paperwork order — no numeric effects exist).
3 LLM judges triaged (dissents preserved); human experts
still decide. Next: Step 4 Gen 1 from A/F/G/H survivors.

STEP 2 DONE — PRE-REGISTERED, NOT HUMAN-FROZEN (2026-11-02):
8 candidates A–H (Appendix B complete, 18/18 FMEA rows each),
protocol, Q0 thresholds (patency ≥80% HIGH; AAV retention
≥0.80+≤10 dB; conventions, unratified), held-out manifest
(validation = 0), extraction schema, freeze checklist
(signatures PENDING), gate_table.py + epi arithmetic.
Skeptic F1 (schema incompatibility) FIXED by parent:
research/scoring/adapt_extraction.py + tests; end-to-end
template→adapter→gate_table verified, 31 tests OK.
Step 3 proceeds as screening/falsification only; no
promotion possible at v1 (G3b BLOCKED, pins unfrozen,
human extraction pending). Next: Step 3 scoring.

STEP 1 DONE — PROPOSED PIN, NOT FROZEN (2026-11-02):
research/frozen_baseline/ (frozen def, AppendixA-v1, cost
dictionary, skeptic, summary). 44 synthesis rows: 12 PINNED
(definitional only), 13 PROVISIONAL, 18 UNPINNABLE, 1 BLOCKED
(G3b, stakeholder co-design pending — all G3b cells
INSUFFICIENT, so no Track-P promotion is possible at v1).
G1 anchor 8 kept as convention + 4/10/16 sensitivities +
head-to-head bar; timing +20% DELETED; fibrosis scale 0–3.
Skeptic: 12/12 spot-checks exact; amendments A1–A6 owed
(cross-file reconciliation) before any freeze. Holder +
co-approver freeze and human dual extraction still PENDING.
Next: Step 2 pre-registration as screening/falsification
generation under these pins.

STEP 0 DONE — AGENT PRE-EXTRACTION ONLY (2026-11-02): 52-row
verified bibliography in research/step0/ (4 workers + skeptic +
synthesis). Sol 6.1 unavailable in this runtime; all agents ran
muse-wonder-full-1.0 fallback at the §9 effort split (high
workers, xhigh skeptic/synthesis) — disclosed per §9 rule 3.
Human dual extraction PENDING: no Step 0 row is gate-deciding
until an independent human extractor verifies it (§9). Key
corrections: Friesen 2001 authors Baskent/Wang (not Cruz) and
4–10 channels is a gloss (Berg 2019: 16>8 gains — G1 point-8
anchor contested); Kral 2023 is crossmodal review, sensitive-
period cite is Kral & Sharma 2012; Otarmeni label 16/20=80%
(single-source, human PDF re-read owed), no numeric age limits;
MED-EL min age 7 mo (provisional, re-pull owed); Liu 2025/Qiao
2024 UNVERIFIABLE as cited; ANI chronic-cat denominators
REFUTED as stated; P0 ≥70 dB denominator still missing (CDC
EHDI table not extracted); Q0 undecidable (no patency % / no
post-CI AAV data). Next: Step 1 pin (provisional where Step 0
is abstract-level; pins needing human extraction flagged).

SOL 6.1 ROUTING ADDED — GOAL v2.2 (2026-11-02): Per holder
direction, GOAL S9 now routes all agent work to Sol 6.1:
xhigh for new-generation ideation/recombination design,
adversarial/judge/synthesis and amendments; high for generation
execution workers (sweeps, pre-extraction, scoring population);
deterministic code for mechanical work. Runs must record
model+effort; fallback disclosed, never silent. Human extraction/
freeze rules unchanged.

ROUND 3 BOTH PASS >=90 (2026-11-02): Gaps 92/100 PASS,
Skeptical 91/100 PASS on GOAL.md v2.1. Review loop complete
(R1 68/57 -> R2 90/85 -> R3 92/91). Residual MEDIUM/LOW errata
applied (S4.1 NA wording, anchor label, claim cap, extractor
independence, README/S12 sync). See reviews/round-3-scores.md.
Next: GOAL S11 Step 0 full-text source verification.

ROUND 2 + GOAL v2.1 (2026-11-02): Round 2 scores on v2 — Gaps
90/100 PASS, Skeptical 85/100 FAIL (2 HIGH). GOAL.md patched to
v2.1 fixing both HIGHs and all Round 2 MEDIUM/LOW items (G1 NA/
portfolio + point anchor, frozen contents, modality co-primaries,
GRADE map, FAIL-first fitness, unilateral variant dropped, human
dual extraction). See reviews/round-2-*. Awaiting Round 3
re-review (target both >=90).

GOAL v2 AFTER ROUND 1 DUAL REVIEW (2026-11-02): Gaps reviewer
68/100 FAIL, skeptical reviewer 57/100 FAIL on v1 (e9d4050).
All verified issues addressed in GOAL.md v2: two-track (P/R)
operationalized gates + Appendix A, C0 triage claim replacing
single-device PRESERVE-30 (channel target relativized), P0/strata,
de-cargo-culted inference (no Gen-0 >=90% claim), per-harm stresses,
lexicographic fitness, Families G/H + Q0, adult-first regulatory
path, Step 0 source verification. Disposition:
reviews/round-1-disposition.md. Awaiting Round 2 re-review
(target both >=90). No challenger scored; baseline unpinned.

GOAL ESTABLISHED (2026-11-02): Created `GOAL.md` defining the
PRESERVE-30 thesis — genotype-agnostic, biology-preserving,
developmentally-timed hearing targeting >30 independent channels
vs frozen bilateral electrical CI (`frozen_bilateral_eCI_v1`) —
with joint gates G1–G6, primary/stress costs, selection-adjusted
inference, walk-forward developmental windows W0–W3, and the
generations/selection/recombination loop (two-dry-round stop,
one-gap-one-follow-up) adapted from `business/INTENT.md` and
`research/durable_strategy.py`. Gen 0 seed families A–F specified.
No challenger scored yet; frozen baseline not yet pinned.
Next step is GOAL.md "First executable steps" #1: pin the frozen
baseline outcome table before pre-registering Gen 0 candidates.
