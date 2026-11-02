# Score F — W0 bridge, F1 only (Track P pathway) — Step 3 screening

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
> promotion possible at v1.
>
> **Binding caps applied:** PASS requires ≥Moderate GRADE
> (human-verified) + Appendix A minimum tier + decision-time
> analysis under the treatment-policy estimand. Abstract-level /
> agent-only evidence caps at PROVISIONAL-SIGNAL (never PASS).
> F1 claims audibility / time-to-CI only — never HA-as-substitute
> at ≥70 dB (§8F). Vibrotactile (F-vib) is exploratory and never
> pooled with F1. Bone-conduction-as-bridge excluded.

## Summary gate table (candidate × gate)

Worst applicable window per gate. `gate_table.py` (via
`adapt_extraction.py`, 46 F/G/H rows adapted, run 2026-11-02)
collapses PROVISIONAL-SIGNAL → INSUFFICIENT and returns F:
`G1 NA, G2/G3a/G3b/G4/G5/G6 INSUFFICIENT`, promoted FALSE.
The one provisional signal below is preserved here per-row;
it does not change the collapsed gate cell.

| Gate | Verdict proposed | Tier / GRADE | One-line reason |
|---|---|---|---|
| G1-spectral | NA-prereg | RECORD | Pathway NA; any channel claim = FAIL of NA rule (none made) |
| G2 W0–W1 | INSUFFICIENT (mechanism only) | T4 / Low–VeryLow | P1 data start ≥1.3 y or ~27 mo fitting; no W0 evidence; no PASS exists W0–W1 |
| G2 W2 | PROVISIONAL-SIGNAL (row) → INSUFFICIENT (gate) | T4 / VeryLow | Retrospective P1 null vs *unilateral* CI; wrong comparator, surrogate only |
| G2 W3 / G2-music | INSUFFICIENT | T4 / UNASSESSED | No same-test delta vs concurrent frozen; CAMP capped provisional anyway |
| G3a W1–W3 | INSUFFICIENT | T4 / UNASSESSED | Instruments uncited (U11), frozen SS blank (U10), no F1 cohort |
| G3b W1–W3 | INSUFFICIENT (BLOCKED) | — | No instrument/MCID (B01) |
| G4 | INSUFFICIENT | RECORD | No cochlear alteration by design; numeric PASS impossible (U17) |
| G5 | INSUFFICIENT | T4 / UNASSESSED | Delay/harm rates UNPINNABLE (U13); no ≥Moderate signal either way |
| G6 | INSUFFICIENT | T4/RECORD / UNASSESSED | Audibility/time-to-CI unmeasured vs concurrent frozen; coverage blank |

## Per-gate evidence

**G1 — NA-prereg.** Pre-declared (GOAL §4.2). The portfolio
inherits its device G1 verdict. F makes no channel claim.

**G2 W0–W1 — INSUFFICIENT, mechanism only.** Sharma 2002
(PMID 12476090, N=104+3, abstract inspected): P1 normalises
within 6 mo if deprivation ≲3.5 y. Earliest implant 1.3 y —
it says nothing direct about 0–9 mo (Step 0 Ch5), and P1 is
never a sole G2/G3 pass (protocol §7 proxy chain). No
inspected study tests F1's actual W0 dose (fitting ≤1 mo after
diagnostic ABR, verified aided SII, datalogged wear-time,
CAEP-guided referral) against the frozen HA trial.

**G2 W2 row — PROVISIONAL-SIGNAL (VeryLow).** Tumuklu &
Gunsoy 2026 (PMID 42194183, abstract inspected 2026-11-02;
late-found design, validation set still 0): retrospective
N=85, unilateral CI (42) vs bilateral HA (43), fitted <48 mo
(mean ≈27 mo), aided thresholds selected to 30–50 dB HL; P1
latencies do not differ (/m/ p=1.00, /g/ p=0.55, /t/ p=0.48).
Why it cannot go further: (a) comparator is unilateral CI,
not `frozen_bilateral_eCI_v1`; (b) fitting age is W2, not W0;
(c) children who achieve 30–50 dB aided thresholds at
≥70 dB unaided are a selected subset — the F1 precondition
(audibility often insufficient at ≥70 dB) is exactly what this
selection hides; (d) P1 has no validated mediation to W2/W3
language in this record; (e) abstract-level, agent-only.
Read honestly, it is a mechanism-consistency signal that
*adequate early audibility* tracks cortical maturation — not
evidence that F1 delivers audibility or shortens time-to-CI
in P0. Decision-time / treatment-policy analysis: absent
(retrospective, device-use duration differs by group).

**G2 W3, G2-music — INSUFFICIENT.** No same-test SRT/word
delta vs a concurrently measured frozen cohort was inspected.
Frozen absolutes are UNPINNABLE (U10); the ≥3 dB / ≥10 pp
deltas are unratified conventions. Music (UW-CAMP) is capped
at provisional in v1 regardless (App. A §4.3).

**G3a W1–W3 — INSUFFICIENT.** W1 allows NI+trajectory only.
For W2/W3 the spoken instruments (PLS-5-class, CELF, spoken
CDI, IT-MAIS/LittlEARS) are uncited (U11) and frozen
within-stratum SS ranges are blank (U10), so no spoken PASS
is constructible. F's pre-registered falsifying W2 endpoint
(candidate-F §7) has no inspected result. Mediation
(W0 CAEP → W2/W3 language in linked children): UNRESOLVED.

**G3b — INSUFFICIENT (BLOCKED).** W1, W2, W3 print BLOCKED.

**G4 — INSUFFICIENT.** F1/F-vib implant nothing and alter no
cells, so residual-hearing / fibrosis (Seyyedi & Nadol 0–3) /
SGN / patency are downstream-CI quantities scored under the
device and G. That justifies *no attributable-loss claim by
design* — it does not earn a numeric G4 PASS, which is
impossible in v1 (U17). Any F-caused delay that erodes future
options is scored in G5/G6, never hidden.

**G5 — INSUFFICIENT.** No rate-NI PASS is possible in v1
(margins U13). The load-bearing harm — false reassurance /
delayed CI — has a pre-registered rescue rule in the
candidate (audibility floor + latest referral date) but zero
observed event counts. F-vib: bounded PubMed search
2026-11-02 (`vibrotactile AND infant/child AND deaf/hearing
loss`, 25 hits; PubMed only, Embase gap disclosed) produced
no inspected abstract reporting a P0 W0 vibrotactile dose
with a somatosensory cross-modal harm or benefit outcome.
Counts are logged; snippets were never used as evidence.
Harm is therefore INSUFFICIENT in both directions — F-vib
stays exploratory with the candidate's named monitoring
(delay events, fNIRS/CAEP cross-modal index as mechanism
only, skin checks, caregiver burden).

**G6 — INSUFFICIENT.** F1's only permitted wins are aided
audibility (SII/thresholds) and time-to-CI-decision. Neither
was inspected against a concurrently measured frozen
pathway, and the frozen HA-trial dose / criterion /
turnaround is UNPINNABLE (U09): a challenger cannot beat an
unmeasured baseline (Step 1 §6). Coverage % needs D1–D4
(blank); disparity caps are unratified conventions
(sensitivity-only). Timeline *is* stated (available-now,
marketed HAs + CAEP), so the missing-timeline FAIL does not
apply — that is completeness, not a G6 PASS. Evolving-standard
sensitivity: no inspected record separates F1 from good
current audiology practice, so even a future frozen win would
need the implementation-gap check (§3.4 claim cap).

## Kill-criterion check (§8F, refined in candidate-F §12)

Kill requires, vs a concurrently measured frozen pathway,
**both** no audibility gain **and** no time-to-CI shortening,
or a null/harmful falsifying W2 G3a endpoint at ≥Moderate
GRADE. **Verdict: NOT KILLED, NOT PASSED — indeterminate.**
No concurrent comparison exists at any GRADE, so neither
conjunct can be evaluated; absence of a test is not a failed
test. F-vib kill (harm signal at ≥Moderate GRADE): not
triggered and not excluded — no eligible harm study inspected.

## Search log (new inspection, 2026-11-02)

Frozen S-F (protocol §3) + audibility/wear-time/CAEP narrowing
(logged amendment, results reported separately above): PubMed
43 hits; abstracts inspected via E-utilities for PMIDs
42194183, 41895171 (narrative review — framing only, not
extracted as effect), 12476090. Embase inaccessible — gap
disclosed in every synthesis sentence that depends on yield.
All other F rows rest on Step 0/1 design evidence (Ch5, U09–
U13, P07) at abstract level; validation set = 0, so every
would-be pass is design-only and capped provisional by rule.

## What would change this score

A prospective T4 pathway study in W0-identifiable P0 children:
decision-time origins (birth/3/6/9 mo, genotype-pending as a
state), treatment-policy denominators (non-wear, rescue-to-CI,
LTFU retained), datalogged wear-time + aided SII, concurrent
frozen-pathway time-to-CI-decision, and the pre-registered W2
G3a endpoint on cited instruments — with human dual extraction.
Until then F1 is an untested, low-regret care-pathway proposal,
and F-vib remains harm-uncharacterised.
