# Step 3 scoring — Candidate B (biohybrid eluting array) [Track P]

> **Model routing (GOAL §9).** Requested route: **Sol 6.1 route,
> worker high**. Actual runtime model: **`muse-wonder-full-1.0`**
> (Sol 6.1 unavailable in this runtime), same effort split.
> Substitution disclosed per §9 rule 3. No claim here is Sol 6.1 work.
>
> **Date:** 2026-11-02. **Status: agent pre-extraction scoring —
> sensitivity/screening output, never gate-deciding.** Human dual
> extraction: **PENDING**. Human freeze: **PENDING**. Human-expert
> review PENDING — open synthesis, not a freeze.
>
> **Read in full before scoring:** `protocol.md`, `Q0-thresholds.md`,
> `AppendixA-v1.md`, `Step1-pin-summary.md`,
> `Step0-verified-bibliography.md`, `candidate-B-biohybrid.md`,
> `cost_dictionary_v1.md`, `heldout-manifest.md`,
> `extraction-schema.md` + template. Scorer additionally re-inspected
> PMID 24760189 (Pinyon) abstract via PubMed E-utilities MEDLINE on
> 2026-11-02 (verbatim-match to Step 0 D3a/D3b). All other evidence
> is Step 0/1 **design-side, abstract-level**; validation set empty.
>
> **Binding caps applied:** PASS requires ≥Moderate GRADE
> (human-verified) **and** Appendix A minimum tier; abstract-level /
> agent-only evidence caps at **PROVISIONAL-SIGNAL** (never PASS);
> rows carry `grade=UNASSESSED`. UNSW is the inventor lab for the
> sole primary → allegiance downgrade + non-inventor replication
> required for any G1 PASS. G3b all **INSUFFICIENT**. INSUFFICIENT
> never imputed. Treatment-policy estimand; decision-time analysis.
> No invented numbers (dose, kinetics, duration: none asserted by
> the candidate, none added here).
>
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.** No Track P
> promotion is possible at v1. No ≥90% claim is made.
>
> Rows: `extract-AB.csv` (29 rows for B). Deterministic check:
> `adapt_extraction.py` + `gate_table.py` → B: G1/G2/G3a/G3b/G4/G5
> INSUFFICIENT, G6 FAIL (completeness), promoted FALSE.

## Headline: kill criterion TRIGGERED on the lifetime/refill arm

Candidate B as specified **meets its own pre-committed kill
criterion** (GOAL §8B, candidate §11 arm ii): *no credible lifetime
burden plan* — duration/refill/revision accounting to adolescence
cannot be stated from inspected kinetics (detail § "Kill criterion"
below). The tonotopy arm (T2) is separately **unevaluable**. A kill
verdict is a candidate-retirement statement, not a gate FAIL: the
gate cells below remain INSUFFICIENT where the evidence is missing
rather than adverse, because INSUFFICIENT must never be converted
to FAIL by narrative. Retirement is also not erasure: a redesigned
candidate with one declared branch + inspected kinetics would be a
new candidate (protocol §11).

## Verdict summary

| Gate | W1 | W2 | W3 | ALL/ADOL | Headline |
|---|---|---|---|---|---|
| G1-spectral | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | No numerator at anchors 8/4/10/16; one T2 provisional mechanism signal |
| G1-temporal | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | Interaction (stim ON/OFF) unmeasured |
| G2 (+music) | mechanism-only | INSUFFICIENT | INSUFFICIENT | — | Zero human B data at any tier |
| G3a | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | All strata; causal chain absent |
| G3b | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | BLOCKED |
| G4 (+G4-AAV) | — | — | — | INSUFFICIENT | Veto neither passed nor triggered; branch undeclared |
| G5 | — | — | — | INSUFFICIENT | FMEA complete; no rate-NI possible; stresses: no change |
| G6 | — | — | — | **FAIL (completeness)** | No numeric timeline **and** no lifetime count |

## Threshold blocker: delivery branch undeclared

Candidate §2 pre-commits to "exactly one declared branch before
Step 3 scoring; undeclared branch = INSUFFICIENT on G4/G5/G6," then
specifies two branches — **B-E** (plasmid electroporation, the
Pinyon mechanism) and **B-L** (drug elution) — and selects neither.
By its own rule, G4/G5/G6 are INSUFFICIENT before any evidence is
weighed. The branches are not interchangeable: Step 0 C12 verifies
that Pinyon supports **electroporation only — not elution and not
any lifetime-reservoir claim** — and no elution citation was
inspected in Step 0 (unresolved item 9). Scoring B-L from Pinyon
would be a category error; scoring B-E still leaves expression
duration unknown. Protocol §3 (S-B) likewise requires electroporation
and elution to be screened/extracted separately.

## G1-spectral — INSUFFICIENT at anchor 8 and sensitivities 4/10/16

The sole primary is Pinyon et al. 2014 (PMID 24760189, UNSW,
guinea pig, bilateral ototoxic deafening with **2-week** neurite
atrophy — a short-deafness model, not congenital lifelong
deafness). The abstract (re-inspected verbatim 2026-11-02) reports
BDNF-cDNA electroporation → SGN neurite regrowth toward electrodes
"with localized ectopic branching," GFP-only control failing to
restore structure, and bipolar stimulation with "low stimulus
thresholds and expanded dynamic range" via eABR — **with no numeric
values and no per-arm N in the abstract**. There is therefore no
channel count, no ripple threshold, and no numeric spread for B:
INSUFFICIENT at anchors 8, 4, 10 and 16 alike (no anchor flips a
missing numerator). The regrowth finding is logged as a
PROVISIONAL-SIGNAL (T2 mechanism, inventor-lab single source, SYRCLE
domains invisible at abstract level). Appendix A §3.2's head-to-head
bar (ripple + spread vs named frozen array, same study/model) is
unmet; candidate §3 correctly adds that growth without tonotopic
order cannot PASS — and order was not measured (next section).
Decision-time: a 2-week-atrophy adult-animal result cannot justify
infant W1 decisions; every proxy-chain arrow (animal neurophysiology
→ adult psychophysics → infant CAEP/VRA → W2/W3 language) after the
first is entirely missing for B.

## G1-temporal — INSUFFICIENT

No numeric PASS exists in v1 (+20% ITD deleted). B's candidate-
specific temporal question — does chronic stimulation attract,
repel, prune or destabilise regrown neurites (ON vs OFF history) —
is pre-specified but **unmeasured** in inspected records; by
candidate §2 that alone makes G1 INSUFFICIENT. eABR dynamic range
is not a temporal-fidelity metric against frozen.

## G2 / G3a / G3b — INSUFFICIENT / BLOCKED (no human data exist)

There is no inspected human evidence for B at any tier (eABR ≠
speech, Step 0 D3b). The 2014–2026 translation silence is honestly
carried as **unexplained**: bounded search 2026-11-02 (CTgov
CI+BDNF/neurotrophin returned zero studies, D3c); the frozen
multi-registry re-run (CTgov + EU CTIS + ANZCTR + ChiCTR) and
post-2014 follow-up census are still owed, so this file asserts no
cause (safety/durability/IP/funding all uninspected hypotheses) and
conflates no neighbours (AAV2-BDNF Alzheimer's NCT05040217;
progenitor-cell NCT07032038 secondary-source only). Music: CAMP
adult-only cap as for A; no B data. G3a: no language data, plus the
shared U10/U11 instrument/frozen-score blockers; developmental
causal chain absent → mediation UNRESOLVED. G3b: BLOCKED
(INSUFFICIENT) — co-design pending.

## G4 (veto) + G4-AAV — INSUFFICIENT; tonotopy arm unevaluable

No same-model comparative histology (fibrosis 0–3 per segment, SGN
density, residual hearing) exists for B; frozen-context archival
rows (PMIDs 25122600, 27371868) score the comparator. Scala patency
UNPINNABLE; Q0 **UNDECIDABLE** on current inputs (no Q0-P %, no
established-implant Q0-A study) → Q0-dependent cells INSUFFICIENT.
**G4-AAV:** neither branch as written uses AAV (plasmid
electroporation / drug elution), so the presumptive-FAIL rule does
not attach — but with the branch undeclared, "NA" cannot be
certified either → INSUFFICIENT, with the presumptive FAIL armed if
any future branch adopts AAV. The veto is thus neither passed nor
triggered on histology: a FAIL would need a component worse than
comparator at ≥Moderate GRADE, and the only adverse signal (ectopic
branching) is abstract-level, inventor-lab, denominator-free.

## G5 — INSUFFICIENT; stress scenarios change nothing

FMEA completeness met (all 18 Appendix C rows, incl. candidate-
central C12 neurotrophin misrouting/tumour and C15 elution
depletion, bands honestly UNPINNABLE). No rate-NI PASS is possible
in v1 (U13); no ≥Moderate absolute-signal FAIL is available (no
durability/tumour data in the Pinyon abstract — absence of data,
not absence of risk). Branch-undeclared independently forces
INSUFFICIENT. Stress re-scoring (cost dictionary §6 proxies,
INSUFFICIENT-proxy-reported): S-revision 3.2%→3.7% upper-CI proxy,
S-nonuse <8 h/day 6.8%/12.3%→10.0%/17.1%, S-access LTF/D era-max
42.1%/39.4%, S-surgical meningitis 0.07%→0.10% (malformation
→0.380%/ear) — **verdict change under each stress: none.** G5 is
INSUFFICIENT at base and at every stress, and no B-specific rate
exists to move; the one directional note is that any future refill
plan would *add* surgeries to the revision count, worsening
S-revision burden — unquantifiable until a plan exists. The §6
trade rule (added risk only with G2 PASS + G3b NI) cannot be
satisfied: G2 INSUFFICIENT, G3b BLOCKED.

## G6 — FAIL (completeness: timeline + lifetime count)

Two completeness failures, each sufficient: (1) adult-first stage
sequence stated but **no numeric earliest-plausible infant
timeline** (candidate §11: "stated numerically at handoff or G6
FAIL" — no handoff exists); (2) the **lifetime refill/revision
surgery count to adolescence**, pre-declared as a headline G6
output (candidate §10), is absent and unstateable (kill-linked,
below). Coverage % UNPINNABLE (D1–D4 blank — B additionally excludes
nerve aplasia from eligibility while keeping it in the denominator,
correctly, but no fraction can be computed); disparity caps
unratified. The unexplained 2014–2026 silence caps timeline
credibility (candidate §3). Same sensitivity as A applies to
element (1) alone, but element (2) keeps G6 FAIL under either
reading. FTO: Not assessed (UNSW affiliation-level only).

## Kill criterion — tonotopy (T2) + lifetime/refill

Verbatim (§8B): *"neurite growth without tonotopic order at T2, or
no credible lifetime burden plan (refill/revision count to
adolescence scored in G5/G6; a <5 y reservoir without refill is an
automatic kill)."* Refined arms (candidate §11) checked separately:

| Arm | Test | Result on inspected evidence |
|---|---|---|
| (i) Tonotopy at T2 | Regrowth with §3 order metric degraded vs frozen-array control, or ectopic rate leaving spread no narrower | **UNEVALUABLE → not triggered, not cleared.** Regrowth occurred *with localized ectopic branching* (abstract), but no order metric exists in any inspected record: no place-pitch/best-frequency rank correlation, no ectopic-rate denominator, no pre/post spread vs frozen-array control, and numeric tonotopy margins are UNPINNABLE (no same-model frozen distributions). "Tonotopic order not established" (D3b) is not the same as "order shown degraded," so arm (i) cannot kill on this record — and cannot pass either |
| (ii) Lifetime / refill | Duration/refill accounting to adolescence stateable from inspected kinetics; <5 y reservoir without refill = automatic kill | **TRIGGERED.** B-E: transgene-expression duration unknown (abstract silent; short-deafness model cannot ground a congenital-lifetime claim, candidate §3). B-L: no agent, release kinetics, reservoir volume or duration source inspected at all. Branch undeclared on top. No duration is *asserted*, so the "<5 y" sub-case is not separately instantiated — the trigger is the parent clause: **no credible lifetime burden plan exists or can be stated** |
| (iii) Stimulation–outgrowth interaction adverse at T2 | Retraction/loss with chronic stimulation | **UNEVALUABLE** — interaction unmeasured (also forces G1 INSUFFICIENT) |

**Disposition: Candidate B is KILLED as specified (arm ii).**
Stated sensitivity: under a lenient reading that defers kill
assessment until a handoff design is filed, B would instead sit at
"kill pending — unevaluable on all arms, G4/G5/G6 INSUFFICIENT by
the undeclared-branch rule." That reading is rejected here because
the candidate file itself pre-commits the accounting test in the
present tense ("cannot be stated from inspected kinetics" → kill)
and twelve years post-Pinyon there is still no kinetics source to
state it from; but the disagreement is recorded so a human judge
can reverse it without re-litigating the evidence. Either way, B
cannot advance: resurrection requires a **new candidate** with (a)
one declared branch, (b) inspected kinetics/duration with refill
accounting to adolescence (≥5 y or a refill plan), (c) a T2
tonotopy protocol with margins frozen before data are seen, and
(d) the owed multi-registry silence census (candidate §3 i–ii) —
if that census surfaces a ≥Moderate safety/durability explanation
for the silence, it enters the FMEA and may kill any redesign too.

## What would change these verdicts (ranked)

1. A declared branch + inspected duration/kinetics source (Pinyon
   full text with N/arms/duration is necessary but not sufficient;
   elution needs its own primary) — un-triggers arm (ii) only via a
   new candidate.
2. Non-inventor T2 replication in a mature/**long-deafness** model
   with pre-frozen tonotopy metrics + stimulation ON/OFF arms and
   full denominators — decides arms (i)/(iii) and any G1 signal.
3. Multi-registry + post-2014 literature census of the translation
   silence (bounded-search wording until done).
4. Human dual extraction (lifts abstract cap; Pinyon stays design-side).
5. Shared blockers: G5 P0 harm rates/margins (U13), frozen G2/G3a
   ranges (U10), numeric timeline, G3b co-design (B01).
