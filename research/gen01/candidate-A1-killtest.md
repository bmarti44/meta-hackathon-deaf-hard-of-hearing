# Gen 1 Candidate A1 — Focal electrical, kill-test design child [Track P device]

> **Model routing (GOAL S9).** Requested: **Sol 6.1, xhigh**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-02**.
> GOAL v2.2. **Gen 1 pre-registration design — scores nothing.**
> Human freeze PENDING; post-freeze edits = new candidate.
> **Exploratory-after-seen: YES** (Step 3 score-A + judges seen).
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.** Same
> PASS bar as Step 3. Parent GEN0-A kill was **UNEVALUABLE** —
> never "survived" (D10). This child exists to make it evaluable.

## 1. ID / track / parentage + single-mutation log

- **ID:** `GEN1-A1`. **Track:** P (device; G1 applies).
- **Parent:** GEN0-A only (`candidate-A-focal-electrical.md`).
- **Single mutation (exactly one, S7):** REPLACE parent SS11's
  kill-criterion *statement* with the fully pre-specified
  in-silico kill-test study design in SS3 below (model,
  geometries, charge/battery limits procedure, endpoints,
  seeds, decision rule — frozen before any result is seen).
  **Everything else inherited verbatim:** mechanism, dose
  reporting, eligibility, timing, G1–G6 plan, power method,
  FMEA (except SS10 delta), burden, regulatory staging.
  Explicit non-mutations: the missing numeric G6 timeline is
  **not** fixed here (that would be a second mutation); A's
  disputed G6 completeness FAIL therefore **carries into A1
  unchanged** until a separate timeline child is filed. No
  new focusing mode, array, or claim is introduced.

## 2. Mechanism & target cells (inherited)

Scala-tympani array (named device/geometry/era in extraction
sheet) + pre-declared focusing mode (tripolar/partial-
tripolar/phased-array/dynamic; coefficient + channels-vs-
maxima fixed) + anatomy-based fitting. Target: SGN. Must
still explain prior translation failure (parent SS3: charge
cost PMID 17552721, −48% battery PMID 36279119, degraded-
comparator Srinivasan PMID 23467170 barred, take-home nulls,
Berg channels/maxima PMID 31067952). Dexam/ECochG/robotic =
evolving-standard comparator, never novelty.

## 3. THE MUTATION — pre-specified kill-test study design (T0)

**Question (parent kill, verbatim):** "no modeled spread
reduction at safe charge in fibrotic/growing-cochlea model."

| Design element | Pre-specification (frozen before results) |
|---|---|
| Model | Named finite-element (or equivalent volume-conduction + neural) cochlea model: name, version, mesh, tissue conductivities with sources, SGN population model — recorded in freeze addendum. No model shopping post-results |
| Geometries (both required) | (a) **Fibrotic:** scala tissue/new-bone shunting layer graded 0–3 (Seyyedi & Nadol scale, N4) per segment (basal/mid/tip), conductivity range pre-stated; (b) **Growing:** infant→child cochlear dimensions at pre-stated ages with electrode–modiolus distances re-derived per age. Adult non-fibrotic geometry = reference arm only, cannot pass the kill test alone |
| Arms | Pre-declared focusing mode vs monopolar clinical map on the *same named array*, loudness-balanced by pre-stated rule; factorial focusing×anatomy-fitting retained from parent SS3(4) |
| Safe-charge limit (procedure, pinned pre-unblinding) | Per-contact limit = min(manufacturer max charge density (µC/cm²/phase, contact area stated) for named contacts, tissue-damage threshold ÷ pre-stated safety margin) — both sources human-extracted and filed *before* model outputs are opened. No limit invented in this file (parent C9 gap). If no named-device limit can be filed, test stays UNEVALUABLE by design — reported as such, never passed |
| Battery floor | Pre-stated minimum processor hours/day at map levels; source: named-device spec. Focusing current overhead computed per arm (cf. −48% signal) |
| Primary endpoint | Spread of excitation (mm **and** octaves) at equal loudness, focusing − monopolar, per geometry×segment. Dual-report with ripple modelling if claimed; **no ripple→channels conversion** (UNPINNABLE) |
| Seeds / precision | Seed set pinned (S5.2); parameter-uncertainty sweep pre-listed (conductivities, fibrosis grade, distance); report endpoint distributions, not point picks. Labelled *modelled sub-claim, conditional on assumptions* (S5.1) |
| Decision rule (kill fires iff) | In **either** fibrotic or growing geometry: focusing shows no spread reduction at ≤ safe-charge limit, **or** reduction only above limit, **or** only below battery floor → **GEN1-A1 KILLED**. Reduction in both geometries within limits → kill *cleared for T0 only* (not a G1 PASS; T2/T3 non-inventor replication still owed). Any post-hoc geometry/limit/mode change = new candidate |
| Blinding discipline | Analysis code + decision thresholds committed before outputs opened (S7 rule 7 freeze checklist). Directional priors (charge cost, nulls) may not substitute for the run (J1/J3-4) |

## 4. Delivery route & dose / units (inherited)

Standard implantation as frozen; dose = charge/phase (nC),
charge density/contact, pps, focusing weights, channels +
maxima, T/C, datalogged wear. T0 stage adds no human dose.

## 5. Timing / decision origins (inherited)

Parent SS6 table unchanged. Kill test is pre-clinical (T0)
and gates any T2→adult→child staging; it consumes no W0–W3
window and may not delay any child's frozen care.

## 6. Model system / comparator

T0 model per SS3 → (only if kill cleared) T2 mature deafened
animal → T3 adult take-home vs clinical map (non-inventor)
→ T4 paediatric vs concurrent frozen. Vocoder/degraded
comparators cannot PASS (App. A SS3.2).

## 7. Eligibility by S3.2 stratum (inherited verbatim)

Parent SS5 table unchanged (ANSD stratified; CND aplasia no
efficacy claim; malformations per class; syndromic/host/
context rules). Model geometries must include malformation
sensitivity or mark those strata INSUFFICIENT — no silent
pooling. No coverage % (D1–D4 blank).

## 8. G1–G6 measurement plan (App. A v1; unchanged bars)

Identical to parent SS7. A1-specific scoring note: kill-test
output moves **only** the kill verdict and (at most) a T0
mechanism signal for G1-spectral/G5-C9. G1 PASS still needs
≥12 effective channels *and* head-to-head ripple/spread vs
named frozen array with non-inventor replication at anchors
4/8/10/16 — a model run alone can never PASS G1. G2 (≥3 dB,
T4), G3a (+0.4/−0.2 SD, T4), G4 veto, G5 (no rate-NI PASS v1),
G6 (disputed FAIL carried, SS1) unchanged. **G3b BLOCKED.**

## 9. Power / precision (inherited + T0 rule)

Parent SS9 unchanged (no invented N; U10/U12 blank). T0:
precision = pre-listed uncertainty sweep coverage; a kill
verdict must hold across the sweep's pre-stated plausible
range or read INSUFFICIENT-model-sensitive. No ≥90% claim.

## 10. FMEA delta rows (all other rows inherited verbatim)

| Delta row | Sev | Band / tier | Mitigation | Stopping rule |
|---|---|---|---|---|
| C9-delta: model understates in-vivo charge injury (conductivity/fibrosis mis-specification) → false kill-clearance | 3 | UNPINNABLE rate; T0 + filed device limits | Conservative limit procedure (SS3); kill-clearance labelled T0-only; T2 chronic-stimulation safety required before any human focusing | Any T2 charge-injury signal → focusing halted regardless of T0 result |
| (new) Model-result overclaim: T0 spread win narrated as channel/language win | 2 | Reporting risk | SS8 scoring note binding; modelled-sub-claim label on every output | Any G1/G2 PASS language from T0 alone = FAIL of reporting rule |

## 11. Burden (inherited)

Parent SS10 concurrent-delta counting unchanged. T0 stage:
compute/engineering burden only; zero family burden.

## 12. Regulatory & staging; FTO; kill

Class III PMA / PMA supplement per parent SS11; adult-first
staging binding; never delayed-CI control. **FTO: Not
assessed.** **Kill:** SS3 decision rule (sole Gen 1 change).
If killed, A1 archived with model + seeds + outputs
(S7 rule 2); resurrection with a different mode/geometry =
new candidate, never an edit.

*End. One mutation only. G3b BLOCKED.*
