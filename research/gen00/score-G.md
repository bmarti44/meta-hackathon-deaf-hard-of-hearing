# Score G — Diagnosis & sequencing pathway (Track P, C0 core) — Step 3 screening

> **Model routing (GOAL §9).** Requested route: **Sol 6.1, high**
> (generation-execution worker). Actual runtime model:
> **`muse-wonder-full-1.0` fallback** (Sol 6.1 unavailable in this
> runtime). Substitution disclosed per §9 rule 3. No claim here is
> Sol 6.1 work. **Date: 2026-11-02.** GOAL v2.2.
>
> **Status: Step 3 screening output — sensitivity-only.** Human
> freeze PENDING; human dual extraction PENDING. Scores are
> `verdict_proposed` from agent pre-extraction in
> `extract-FGH.csv`; adjudicated verdicts require `gate_table.py`
> + human verification. Exploratory-after-seen: YES.
>
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.** No Track P
> promotion possible at v1 — including for the C0 portfolio.
>
> **Binding caps applied:** PASS requires ≥Moderate GRADE
> (human-verified) + Appendix A minimum tier + decision-time
> analysis under the treatment-policy estimand. Abstract-level /
> agent-only evidence caps at PROVISIONAL-SIGNAL (never PASS).
> Diagnostic yield alone is not pathway evidence. **G is scored
> against the frozen diagnostics contents (Step 1 P07) and cannot
> win by definition** — see below. The unilateral-CI +
> preserved-ear variant is excluded from Gen 0 (§8G) and is not
> scored here.

## Summary gate table (candidate × gate)

`gate_table.py` via `adapt_extraction.py` (run 2026-11-02)
returns G: `G1 NA, G2/G3a/G3b/G4/G5/G6 INSUFFICIENT`, promoted
FALSE. The one provisional signal (diagnostic yield) is
preserved per-row below; it collapses to INSUFFICIENT at gate
level and, by rule, could never PASS a pathway gate anyway.

| Gate | Verdict proposed | Tier / GRADE | One-line reason |
|---|---|---|---|
| G1-spectral | NA-prereg | RECORD | Pathway NA; standard array = frozen-equivalent, never a G1 win |
| G2 W2/W3 | INSUFFICIENT | T4 / UNASSESSED–Low | No triage-attributable delta vs concurrent frozen; CHORD ≠ G's win |
| G3a W2/W3 | INSUFFICIENT | T4 / UNASSESSED | No decision-time T4 result; instruments/frozen SS gaps (U10/U11) |
| G3b W1–W3 | INSUFFICIENT (BLOCKED) | — | No instrument/MCID (B01) |
| G4 (incl. patency/Q0) | INSUFFICIENT | T4 / UNASSESSED | Option-preservation % unmeasured; Q0 UNDECIDABLE (`Q0-verdict.md`) |
| G5 | INSUFFICIENT | T4 / UNASSESSED | Mis-triage/VUS/delay rates UNPINNABLE; no ≥Moderate signal either way |
| G6 | INSUFFICIENT (1 PROVISIONAL-SIGNAL row: yield) | T4 / Low | Yield ≠ turnaround/time-to-access; frozen turnaround unmeasured |

## Why G cannot win by definition (frozen contents test)

The deciding comparator already contains, per Step 1 P07 and
`frozen_bilateral_eCI_v1.md` §3: *standard etiologic workup as
routinely ordered — targeted genetics incl. GJB2 where ordered,
CMV testing, imaging — without guaranteed rapid turnaround,
without a pre-committed gene-first triage rule, without a
preserved-ear protocol.* G may therefore claim only the three
things frozen deliberately lacks: (1) **guaranteed rapid
turnaround** (days, decision-time), (2) a **pre-committed
gene-therapy-first-only-if-label-eligible rule** that changes
who reaches what, when, and (3) the resulting **measured
option-preservation / time-to-access consequences**. Showing
that exomes diagnose more than GJB2-only testing shows none of
the three — frozen clinicians can and do order exomes. Likewise
Otarmeni's own efficacy (evolving standard) is Regeneron's
result, not G's: G earns credit only for label-eligible ears it
*routes* to that therapy in time, without delaying everyone
else's CI. Every G cell below is judged on that basis. Beating
frozen but not centres where rapid sequencing is already routine
(evolving-standard sensitivity comparator) = implementation gap,
never a C0 win (§3.4 claim cap) — and no inspected record yet
lets either comparison be run.

## Per-gate evidence

**G1 — NA-prereg.** Portfolio G1 inherited from the standard
array as frozen-equivalent (GOAL §8 worked example).

**G6 yield row — PROVISIONAL-SIGNAL (Low, T4).** Downie et al.
2020 (PMID 31827275, abstract re-inspected 2026-11-02):
population-derived Australian cohort, moderate–profound
bilateral HI, births 2016–17; exome diagnosis 59/106 (56%) vs
GJB2/6-only 22/106 (21%); 106/156 consented. Downgrades:
abstract-level, design-set (seen before hypotheses, so never
validation); 2021 errata contents unchecked (A15); moderate–
profound ⊋ P0 ≥70 dB; non-U.S. pathway; and decisively — no
turnaround time, no time-to-first-access, no decision-origin
denominator, no VUS/return-of-results burden. Shearer 2024
(PMID 39146193, abstract inspected) reviews yields as 43%
overall, range 10–60% by features: REVIEW tier, framing only —
review numbers belong to their primaries and are not extracted
as effects (protocol §4). Targeted Step 3 search for hearing-
specific sequencing *with turnaround* (18 hits, § below)
produced no inspected abstract reporting sample-to-counselled-
result days against a frozen-contents comparator.

**G6 time-to-access / turnaround — INSUFFICIENT.** This is G's
primary endpoint and it is empty on both sides: G-side
turnaround variance uninspected (Step 0 §4 rapid-sequencing row
unverified — NSIGHT/Baby Bear lineage never inspected), frozen-
side turnaround UNPINNABLE (U09). Step 1 §6 is explicit:
turnaround wins vs an unmeasured baseline read INSUFFICIENT.
Decision-time discipline (origins birth/3/6/9/12 mo;
pending/VUS/negative as states; a 14-month genotype may not
justify a 6-month decision) is correctly pre-registered in
candidate-G §4 but has never been executed on data. Coverage:
D1 blank (U01), OTOF fraction UNVERIFIABLE (E3a-iv/O1d) —
"tens/year" is never an input. Timeline is stated
(available-now components), so no missing-timeline FAIL;
completeness only.

**G2 — INSUFFICIENT.** CHORD (NCT05788536 full registry record
inspected 2026-11-02; PMID 41085057 abstract) is single-arm,
open-label, no frozen contrast. Its Week-24 ≤70 dB results
(label 16/20; NEJM cut 9/12; 24 treated — three Ns never
conflated, Step 0 O2b/O2c; label numbers single-source pending
human re-read, A5) describe what the *label subset* achieves
when treated — G was not the intervention that produced them.
No same-test G2 delta attributable to faster/correct triage vs
a concurrent frozen cohort was inspected; absolutes are
UNPINNABLE (U10).

**G3a — INSUFFICIENT.** No decision-time, treatment-policy G3a
result at T4. An explanatory (etiology-known) analysis can
never PASS G (candidate-G §7) because it back-dates information
unavailable at the decision origin. Spoken-instrument citation
gap (U11), blank frozen SS (U10), signed >73 mo gap, and the
every-stratum NI rule all independently block a PASS.

**G3b — INSUFFICIENT (BLOCKED).** W1–W3. A favourable Q0 or
yield result cannot promote G while G3b is blocked
(Q0-thresholds header).

**G4 — INSUFFICIENT.** Two components. (a) *Measured* option
preservation — % of label-eligible ears (biallelic OTOF,
preserved OHC, no prior same-ear CI; USPI §1, Step 0 O1b)
reaching gene-therapy-first without CI-delay harm to others:
no numerator or denominator in any inspected record. The
registry record (NCT05788536, RECRUITING, est. N=36 target)
describes the therapy trial, not a triage pathway's capture
rate. (b) *Biological* preservation (scala patency for later
same-ear AAV): Q0 is **UNDECIDABLE-no-data** (`Q0-verdict.md`),
so this component reads INSUFFICIENT by Q0-thresholds §4
consequence 2. Claiming unstudied post-CI AAV efficacy as a
"preserved option" would be a FAIL of the Step 0 C13 rule;
candidate-G correctly does not claim it, so no FAIL is entered.
G4-AAV presumptive FAIL applies to AAV-*using* challengers; G
administers no AAV and is scored here on routing, while the
downstream therapy's re-dosing question stays with that therapy.

**G5 — INSUFFICIENT.** Mis-triage, VUS distress, incidental-
finding and delay rates are UNPINNABLE (U13); the candidate's
mitigations (parallel-track CI workup, VUS never delays CI,
LP/P-only gene-first rule, mis-triage audit) are design
commitments with zero observed compliance counts. No harm
signal at ≥Moderate GRADE was inspected in either direction.
FMEA filing (candidate-G §9) satisfies completeness; it is not
a rate-NI PASS, and no such PASS exists in v1 for any candidate.

## Kill-criterion check (§8G, refined in candidate-G §12)

Kill requires, vs concurrently measured frozen workup, **both**
(a) no time-to-first-access gain in decision-time analysis
**and** (b) no option-preservation gain — or a Q0 result showing
post-CI sequencing trivially preserves the option (retiring G's
preservation rationale via pivot). **Verdict: NOT KILLED, NOT
PASSED — indeterminate on both arms.** No concurrent comparison
exists for (a) or (b), and Q0 returned UNDECIDABLE, which by
pre-registered consequence neither supports nor refutes the
preservation premise: G may claim only measured cells (none yet
beyond yield), and may not be penalised as if foreclosure were
disproven. C0 therefore remains an untested portfolio claim;
frozen is kept by default, and that is reported plainly.

## Search log (new inspection, 2026-11-02)

Frozen S-G (protocol §3): PubMed 1,279 hits (broad yield
literature). Logged narrowing — hearing loss + (genomic
sequencing/exome) + (turnaround / time-to-diagnosis / diagnostic
yield) + infant/child: 18 hits; abstracts inspected via
E-utilities (Downie re-fetch; Shearer review; remaining hits
were non-pathway gene-spectrum/mitochondrial cohorts, excluded
with reason: no turnaround, no triage comparator). CTgov API v2
full record NCT05788536 inspected. Embase inaccessible — gap
disclosed. Validation set = 0; Downie is design evidence.

## What would change this score

A prospective decision-time pathway comparison (or stepped-wedge
rollout) reporting, by origin and stratum: sample-to-counselled-
result days with pending/VUS/negative states, time-to-first-
access (gene therapy or CI activation) under treatment-policy
(crossovers/rescue CI in denominators), % label-eligible ears
captured gene-first, mis-triage audit counts, and W2/W3 G3a on
cited instruments — against a concurrently measured P07 frozen
pathway *and* an already-rapid centre (evolving standard), with
human dual extraction. Plus, for the biological-preservation
arm, a Q0-decider study per `Q0-verdict.md`. Until then G is a
well-specified triage proposal whose only inspected number —
exome yield — is, by pre-registered rule, not pathway evidence.
