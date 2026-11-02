# Judge 1 — biophysics / device lens — Gen 0 Step 3 adjudication

> **Model routing (GOAL §9).** Requested: **xhigh judge**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-02**. GOAL v2.2.
>
> **Authority limit (GOAL §9 / protocol §9), stated plainly: this LLM
> judge is triage only. Human experts decide freezes.** This file may
> rank, flag and draft verdicts for human adjudication. It may not
> freeze a baseline or candidate, ratify a convention, unblock G3b,
> or convert INSUFFICIENT to PASS. Judge opinion is not evidence and
> imputes no missing cell. Human dual extraction, human freeze and
> the named-expert roster remain **PENDING**; everything below is
> sensitivity-only screening.
>
> **Blinding.** Blind to Judge 2 and Judge 3: their files were not
> opened. Read: `scoring/score-A.md`, `scoring/score-B.md`,
> `score-C..H.md`, `Q0-verdict.md`, `scoring/step3-skeptic.md`
> (downgrades D1–D17), candidate A/B/C/E device sections, protocol
> §9. CSVs re-parsed independently (#-headers skipped): 167 rows
> (AB 71, CDE 41, FGH 55), **0 PASS**, 17 PROVISIONAL-SIGNAL rows,
> 7 FAIL rows — matching the skeptic's arithmetic.
>
> **Lens.** Charge/charge-density and battery cost, spread of
> excitation and channel interaction, optical energy/thermal dose,
> dose–duration (expression/elution kinetics), mechano-electrical
> transduction chain, intraneural current spread, scala patency as
> a physical access/conductance quantity. Cells outside this lens
> (language, pathway turnaround, signed-stratum outcomes) are
> marked DEFER, not voted.

## Headline adjudication

**Agree with the skeptic's net judgment, with three written
dissents preserved below (J1-DISSENT-1/2/3).** No PASS anywhere is
defensible; G3b BLOCKED for all; no promotion; FROZEN retained by
default. Per-study provisional count (D8) is upheld as the only
honest arithmetic. The dissents change *labelling and counting
logic*, not any gate outcome: no cell moves to PASS, none of my
dissents rescues a candidate.

## Per-cell adjudication — disputed / provisional cells in lens

### A — focal electrical

| Cell | Judge 1 | Reason (device physics) |
|---|---|---|
| G1-spectral W1–W3, van den Honert & Kelsall PMID 17552721 ×3 rows, PROVISIONAL-SIGNAL | **AGREE provisional cap; AGREE D8** (one study, not three) | Tripolar/phased-array focusing narrows excitation only by spending more total current for equal loudness — a volume-conduction identity, not a free resolution gain. The signal itself reports the adverse side of the trade. N=3, originator lab, qualitative, no ripple/spread numerator vs a named frozen array. Window-triplication of one adult study into W1/W2/W3 adds no physics. |
| G1-spectral anchors 4/8/10/16, INSUFFICIENT | **AGREE** | No measured channel count for A at any anchor; Berg PMID 31067952 raises the frozen bar at 16. A missing numerator is INSUFFICIENT under every convention; no anchor choice is load-bearing. Ripple→channels conversion correctly forbidden. |
| G1-temporal, INSUFFICIENT (not NA) | **AGREE** | Focusing changes the spatial pattern, not a measured temporal-fidelity quantity. Unmeasured ≠ not-applicable; silent-omission rule correctly applied. |
| G2 W3 ×3 provisional nulls (van Groesen, Bierer & Litvak, Caswell-Midwinter); Srinivasan barred | **AGREE** | Srinivasan's degraded monopolar comparator inflates any focusing delta — correctly barred as PASS evidence. Chronic take-home nulls are the physically relevant condition (focusing must survive loudness balancing and battery cost in daily maps, incl. −48% battery, PMID 36279119). Nulls cannot FAIL G2 without an interval-estimated same-test delta at ≥Moderate GRADE; none exists. Treatment-policy denominator (13 fitted/9 completed) correctly retained. |
| G4 / G5, INSUFFICIENT; C9 no safe-charge limit | **AGREE — this is A's central device defect** | No per-contact charge-density limit, charge/phase, duty cycle, or margin to a tissue-damage threshold is stated for any named contact geometry. Without that number neither safety nor the kill test is even *statable*, let alone passed. Archival fibrosis series (PMIDs 25122600, 27371868) describe the comparator in older devices; they raise the prior that a fibrotic scala worsens focusing (higher impedance, altered current paths) but measure nothing about A. Correctly neither PASS nor FAIL. |
| G6 FAIL (timeline completeness) | **DISSENT from hard-FAIL presentation; AGREE with skeptic D17** | See J1-DISSENT-3. A stage sequence without times is incomplete, but this is an unratified-convention completeness reading, not a device measurement. Print only as disputed strict-reading sensitivity FAIL. A stated numeric timeline flips it to INSUFFICIENT and changes no physics. |
| Kill (spread at safe charge), UNEVALUABLE | **AGREE; AGREE D10** | The pre-specified test — modelled spread in a fibrotic/growing cochlea at pre-stated safe charge and battery floor, frozen seeds — has never been run. Adverse direction (current cost, battery, take-home nulls) is a prior, not a test result; substituting it would be the post-hoc move the protocol forbids. "Not killed" must never be printed as "survived". This model run is correctly ranked A's gating next step. |
| Stress re-scoring, no verdict change | **AGREE** | Stress proxies move comparator rates; A has no device-specific rate to move. "INSUFFICIENT-proxy-reported", never "stress survived", is correct. |

### B — biohybrid (electroporation / elution)

| Cell | Judge 1 | Reason |
|---|---|---|
| G1-spectral W1–W3, Pinyon PMID 24760189 ×3 rows, PROVISIONAL-SIGNAL | **AGREE cap; AGREE D8** (one study) | Sole inventor-lab (UNSW) primary, 2-week ototoxic atrophy ≠ congenital lifelong deafness, no per-arm N, no numeric thresholds/spread/channel count in abstract. eABR "low thresholds / expanded dynamic range" is not a spread or tonotopy measurement. One mechanism signal, triplicated by window. |
| Branch undeclared (B-E vs B-L) → G4/G5/G6 INSUFFICIENT by candidate's own rule | **AGREE — and it is stronger in this lens** | B-E and B-L are *different devices*: different dose units (plasmid µg + pulse V/width vs agent + release-rate µg/day + reservoir volume), different failure modes, different duration physics. An undeclared branch is not missing paperwork; there is no single device specification whose lifetime, charge interaction, or depletion could be tested. Pinyon supports electroporation only (Step 0 C12); scoring elution from it would be a category error. |
| Kill arm (i) tonotopy, UNEVALUABLE | **AGREE** | "Localized ectopic branching" with no order metric, no ectopic-rate denominator, and no pre/post spread vs frozen-array control cannot show order degraded *or* preserved. Regrowth toward contacts without place-order could in principle widen channel interaction — which is exactly why the metric, not the impression, must decide. |
| Kill arm (ii) lifetime/refill, TRIGGERED → B killed as specified | **AGREE TRIGGERED; lenient reversal preserved (D11)** | Dose–duration is constitutive for this device class. B-E expression duration is unknown; B-L has no inspected agent/kinetics/reservoir at all; branch undeclared on top. The candidate pre-committed the test in the present tense ("cannot be stated from inspected kinetics" → kill), so on the candidate-as-specified the parent clause — no credible lifetime burden plan — is met. **Recorded disagreement:** under the lenient reading (defer until a handoff design is filed) B sits at kill-pending/unevaluable. A human judge may reverse on that reading without re-litigating evidence; synthesis must print the reversal attached (D11), never a bare "B killed". Either reading: B cannot advance; resurrection = new candidate with one branch + inspected kinetics. The "<5 y reservoir" automatic sub-case is *not* separately instantiated (no duration is asserted) — correctly not claimed. |
| Kill arm (iii) stimulation–outgrowth interaction, UNEVALUABLE; G1-temporal INSUFFICIENT | **AGREE** | Whether chronic stimulation attracts/prunes/destabilises regrown neurites (ON vs OFF history) is the device's defining interaction and is wholly unmeasured. |
| G4-AAV INSUFFICIENT (not NA, not FAIL) | **AGREE** | Neither branch as written uses AAV, but an undeclared branch cannot certify NA. Presumptive FAIL correctly left armed. |
| G6 FAIL (timeline + lifetime count) | **AGREE FAIL stands** (unlike A) | Element (2) — the lifetime refill/revision count to adolescence — is a device-durability output, not a convention quibble, and it fails under either timeline reading. See J1-DISSENT-3 for the A/B asymmetry. |
| 2014–2026 translation silence carried as unexplained | **AGREE** | Bounded CTgov search only; multi-registry census (EU CTIS/ANZCTR/ChiCTR) owed (D9). No cause (safety/durability/IP/funding) may be asserted. |

### C — optical CI

| Cell | Judge 1 | Reason |
|---|---|---|
| G1-spectral, Dieter PMID 32596983 + Alekseev PMID 40721511, 2× PROVISIONAL-SIGNAL | **AGREE cap and outcome; DISSENT from skeptic D2's counting label** | See J1-DISSENT-1. Neither row is a channel-count or head-to-head ripple/spread result vs a named frozen array; no animal N in abstracts; no non-inventor replication. PROVISIONAL at every anchor, never PASS. The VeryLow 2026 EMBO record correctly INSUFFICIENT; "AAV-PHP.S" correctly deleted. |
| G1-temporal INSUFFICIENT | **AGREE** | Opsin kinetics (on/off time constants) are the temporal-fidelity bottleneck for oCI and no head-to-head temporal metric vs frozen was inspected. |
| G4 INSUFFICIENT (disclosed-traded); G4-AAV FAIL | **AGREE, with "presumptive" mandatory in every citation** | The *rule* is pre-registered; the AAV-use premise is abstract-level ("virus-mediated", capsid unasserted). In this lens the FAIL is about irreversibility of first capsid exposure, and opsin delivery is integral to the device — NA is not available. No chronic SGN-survival/fibrosis/patency data exist to move G4 either way. |
| G5 INSUFFICIENT (thermal/phototoxic UNVERIFIED) | **AGREE — no thermal adjudication is computable** | A <200 nJ ICC *threshold* is an efficacy number, not a safety margin. Without per-emitter energy/pulse, peak irradiance, pulse width/rate, duty cycle and a tissue temperature-rise model, cumulative thermal dose cannot be computed or compared with any limit. Absence of a computable dose is INSUFFICIENT, and is not evidence of safety. |
| G6 infant FAIL (pre-specified) | **AGREE** | Fires by the candidate's own staging rule (no adult FIH + immunogenicity/durability + power/heat). A staging FAIL, not a measured harm — must be labelled as such (D17 class). |
| Park 2028-11-02, not yet triggered | **AGREE; AGREE D12** | Date exists only under an assumed 2026-11-02 freeze that has not occurred (human freeze PENDING); it slides day-for-day. NCT05110183 (infra-red, no opsin) correctly never scored for C — different mechanism. |

#### J1-DISSENT-1 (preserved): C's two G1 rows are not "one signal"

Skeptic D2 counts Dieter + Alekseev as **one** inventor-ecosystem
signal. On outcome I agree: zero independent corroboration, zero
replication, nothing synthesis may call "multi-study". On counting
logic I dissent. Physically the rows test **different subsystems**:
Dieter tests the *emitter* side (16 thin-film μLEDs, spatial/
tonotopic selectivity of light delivery in acute gerbil); Alekseev
tests the *opsin* side (ChReef sensitivity/kinetics, nanojoule
thresholds, rodent + NHP). Two complementary subsystem-feasibility
signals from one ecosystem is not the same object as one duplicated
signal — and neither is a *system-level* result (emitter + opsin +
chronic array jointly delivering ≥16 effective channels head-to-head
vs frozen). Correct synthesis wording: **"C: 0 replications; 2
non-independent subsystem signals (emitter, opsin); 0 system-level
G1 results."** D2's prohibition on corroboration language stands in
full; only its numeral is replaced. No gate cell changes.

### D — reprogramming

| Cell | Judge 1 | Reason |
|---|---|---|
| G1-spectral, Liu PMID 38103445 + McGovern PMID 38266052, 2× PROVISIONAL-SIGNAL | **DISSENT from scorer's G1 provisional label; AGREE with skeptic D3 and go further** | See J1-DISSENT-2. |
| Advance criterion (5 conjuncts) UNMET | **AGREE** | Each inspected record fails multiple conjuncts independently: no replication, no ABR/DPOAE threshold restoration, ectopic/adjacent (not in organ of Corti), synapsis unquantified, guinea pig/mouse (not large-animal per the size/delivery justification). Bounded wording ("in inspected PubMed records, 2026-11-02"; Embase/CTIS/ChiCTR/ANZCTR unsearched) mandatory (D9). |
| G4-AAV FAIL (presumptive) | **AGREE as candidate-design verdict; scope note** | The presumptive FAIL attaches to the *candidate as specified* (AAV reprogramming, no re-dose demonstration). It must not be cited as a measured property of any inspected study's vector. Keep "presumptive" attached (D17 class). Q0-A RETAINED in future would not satisfy G4-AAV — correctly stated. |
| G4/G5/G6 INSUFFICIENT (watch-only) | **AGREE** | Supporting-cell consumption is alteration, never preservation. No human rates; FMEA filed is completeness, not a rate result. |

#### J1-DISSENT-2 (preserved): D's rows are not G1-spectral signals at all

A G1-spectral signal must bear, however weakly, on the transduction
chain that produces frequency-resolved hearing: mechanosensitive
bundles in the organ of Corti → synapsed SGN drive → threshold/
discrimination. Both rows fail at the first physical link as
inspected: MyVIIa+ cells *under* flat epithelium (Liu) and converted
cells *adjacent to* the organ of Corti (McGovern), with no ABR/DPOAE
in either abstract. Marker expression in the wrong place with no
threshold readout is a **cell-fate mechanism report**, not a
provisional spectral-function signal. Labelling it
PROVISIONAL-SIGNAL inside the G1-spectral cell invites exactly the
miscount D3 warns against, even with the failure sentence attached.
Judge 1's adjudication: **relabel both rows INSUFFICIENT-for-G1
(mechanism noted in claim text); D provisional-as-support count = 0**
— which is where D8 already lands arithmetically. The scorer's own
asterisk ("marker counts are NOT a G1 pass — anchor absent") shows
the label was doing no work. No gate outcome changes (gate already
collapses to INSUFFICIENT); the dissent is about not letting a
verdict vocabulary imply a functional signal where the physics chain
is absent at link one.

### E — penetrating ANI

| Cell | Judge 1 | Reason |
|---|---|---|
| G1-spectral INSUFFICIENT (VeryLow); bench numbers excluded | **AGREE** | Bypassing scala current spread does not by itself buy spectral resolution: intraneural current spread and the fibre topography of the nerve trunk (which is not the cochlea's orderly tonotopic sheet) become the limiting physics, and neither is measured in any inspected record. Lenarz PMID 41131644 is concept/review; no ripple/channel-count head-to-head exists at any anchor. Secondary bench pointers ("6.3B pulses", 3×5 shanks) correctly excluded — without a primary bench citation (N devices, failure definition) there is no charge-density or lifetime claim to score. At microelectrode tip areas, charge density per phase is *the* binding safety quantity; its absence alone caps E. |
| "Chronic cat 6-month" REFUTED (Thomas PMID 38379760 = surgical model) | **AGREE; keep REFUTED, never "unverified"** | All five chronic denominators (animals implanted, channels functional n/N per timepoint, migration mm, histology n/N, bench failure definition) are absent. Chronic channel survival and micromotion/migration in a pulsatile CPA environment are the known hard problems for penetrating arrays; a surgical-model paper answers none of them. |
| G4 INSUFFICIENT disclosed-traded; G4-AAV "NA" in text / INSUFFICIENT in CSV | **AGREE with narrative NA; CSV cell is an encoding artifact** | No AAV anywhere in the mechanism — physically NA is correct. Synthesis must cite the stated NA justification, not read the enum-forced INSUFFICIENT as an evidence gap or a hidden pass. "Cochlea bypassed ≠ preserved" correctly stated. |
| G5/G6 FAIL (presumptive, bilateral infants) | **AGREE as pre-registered staging FAIL** | Bilateral CPA neurosurgery in infants with a standard-CI alternative, absent adult feasibility, is correctly failed by rule. Not a rate-NI or measured-harm result (D17 class); per-harm rates separately INSUFFICIENT/UNPINNABLE. Infant CPA anatomy unverified — correctly owed, not assumed. |
| Park 0/3, remains parked | **AGREE** | (1) bench primary ✗, (2) T2 chronic ≥Moderate with denominators ✗, (3) adult feasibility ✗. No denominator-grade nerve-injury assessment is currently possible, so neither retirement-for-harm nor clearance is available. ABI correctly never scored from ANI rows. |

### Q0 — patency / post-CI AAV (in lens)

| Cell | Judge 1 | Reason |
|---|---|---|
| Q0-P cannot be zoned; UNDECIDABLE-no-data | **AGREE** | Tissue *presence/volume* (27/28 granulomatous; 17/17 fibrous + new bone) is not the §2.1 estimand. Patency for later infusion is a physical access + hydraulic-conductance property (can a cannula be placed, does infusate distribute) that no inspected study measures; fibrous-tissue volume fraction does not determine it. Madgar 78% (PMID 40052291, hearing preservation, mean age 9.68 y) correctly excluded — entering it into the ≥80% zone would be the exact conflation pre-registration exists to prevent. Thresholds verified unmoved (80/50%, sensitivities inapplicable without an estimate). |
| Q0-A cannot be zoned | **AGREE** | Fibrosis after an established implant changes both physical access and vector transport (diffusion/convection through fibrous tissue, altered perilymph pathways) — a *concurrent* AAV+implant study (Pfingst PMID 28776202, class i) therefore cannot answer post-establishment retention, on transport physics as well as on sequence rules. Duarte PMID 30017876 (neonatal, no implant) cannot form a retention ratio. No A1/A2 estimate exists; zones and sensitivities are inapplicable, not failed. |
| Q0-L as PROVISIONAL-SIGNAL row | **AGREE D4** | Label eligibility (Otarmeni USPI §1, no prior same-ear CI) is a RECORD regulatory fact, not a biophysics signal in either direction. Excluded from all tallies; A5 human PDF re-read still owed for label efficacy Ns. Biology ≠ permission and exclusion ≠ impossibility — correctly held apart. |

### F / G / H — lens boundary

| Cell | Judge 1 | Reason |
|---|---|---|
| F G2 W2 P1 row, PMID 42194183, PROVISIONAL-SIGNAL | **AGREE D7 (in-lens part only)** | The one device-physics point in F: at ≥70 dB HL unaided, hearing-aid gain/output and aided SII are frequently insufficient — that audibility precondition is F1's load-bearing physical question, and selecting children who achieved 30–50 dB aided thresholds hides precisely its failure mode. Wrong comparator (unilateral CI), ~27 mo fitting ≠ W0, retrospective. Mechanism-consistency only; forbidden as audibility/time-to-CI evidence. F's remaining cells: **DEFER** (pathway/language lens). |
| G yield row (Downie PMID 31827275); H ASL-CDI row (PMID 32180180) | **DEFER on substance; AGREE D5/D6 as labelling** | Neither is a device/biophysics signal (diagnostic yield; instrument existence). I record no independent device vote on G/H gates, kill arms, or pathway claims. Skeptic's exclusion of both from effect tallies is consistent with this lens. G/H kill status per D10 ("test never runnable") is a logic point I endorse without adjudicating their evidence. |

#### J1-DISSENT-3 (preserved): A G6 vs B G6 FAIL asymmetry

I dissent from printing A's and B's G6 FAILs at the same strength.
**A's FAIL rests entirely on one disputed reading** ("no numeric
timeline = FAIL" vs "stage sequence satisfies staging-stated") under
an unratified convention — scorer and skeptic (D17) both record the
flip. It should print only as *disputed strict-reading sensitivity
FAIL*. **B's FAIL survives that flip**, because its second element —
no lifetime refill/revision count, unstateable from any inspected
kinetics for either branch — is a device-durability failure, not a
reading. Synthesis that lists "A and B both FAIL G6" without this
asymmetry overstates A and understates why B fails. All seven FAIL
rows in the set remain completeness/staging/presumptive; none is a
≥Moderate measured harm, and none may be narrated as demonstrated
danger (nor any INSUFFICIENT as safety).

## Skeptic downgrades D1–D17 — Judge 1 disposition

- **Adopt in full:** D1 (agent Low/VeryLow → UNASSESSED; verified in
  CSVs: AB carries UNASSESSED, CDE/FGH print agent grades), D3
  (strengthened by J1-DISSENT-2), D4, D7, D8, D9 (all absence claims
  bounded to inspected PubMed/CTgov 2026-11-02), D10 (A kill
  unevaluable, never "survived"; F/G/H deferred but logic endorsed),
  D11, D12, D14 (~42 unrowed Level-1 cells; no completeness claim),
  D17 (per J1-DISSENT-3).
- **Adopt with relabelling:** D2 → per J1-DISSENT-1 (0 replications;
  2 subsystem signals; corroboration language still banned).
- **Adopt as labelling, defer on substance:** D5, D6, D13 (outside
  device lens; no device vote recorded).
- **Adopt with lens note:** D15 (C/D/E narrative-only until a
  `gate_table.py` run is evidenced — owed) and D16 (C–H
  stress-untested — owed as labelling; note for C/D/E no human
  device rate exists, so a stress run cannot move their cells from
  INSUFFICIENT in this lens; it is a completeness debt, not a
  hidden PASS/FAIL).
- **No PASS below Moderate/tier, G3b 24/24 INSUFFICIENT, Q0
  thresholds unmoved:** independently re-verified above. **CLEAN.**

## What would move cells in this lens (ranked, no new evidence invented)

1. **A:** the kill-test model itself — fibrotic + growing geometry,
   named model/version/seeds, pre-stated per-contact charge-density
   limit and battery floor. Until it exists A is untested, not alive.
2. **B (new candidate only):** one declared branch + inspected
   kinetics/duration; non-inventor T2 in a long-deafness model with
   pre-frozen tonotopy metrics, ectopic-rate denominators, and
   stimulation ON/OFF arms.
3. **C:** full-text dose extraction enabling a thermal-dose
   computation (energy/pulse, irradiance, duty cycle, ΔT model);
   chronic opsin durability + immunogenicity; adult FIH. Power/heat
   is currently not merely unpassed — it is uncomputable.
4. **E:** primary bench citation with charge-density limits and
   failure definitions; T2 chronic denominators (channel survival
   n/N, migration mm, histology n/N); then adult feasibility.
5. **Q0:** the two decider designs already specified in
   `Q0-verdict.md` (post-establishment AAV vs same-study unimplanted
   comparator with A1+A2; prospective patency n/N by time band with a
   pre-stated cannulation definition).
6. **All:** human dual extraction and full-text inspection (lifts
   the abstract cap only — design evidence stays design evidence),
   `gate_table.py` run for C/D/E, the ~42 unrowed cells, and the
   owed Embase/EU CTIS/ChiCTR/ANZCTR searches behind every absence
   claim.

**Judge 1 bottom line for the human panel:** the scoring discipline
holds where physics could most easily have been oversold — focusing
bought with current, optical thresholds mistaken for thermal
margins, marker-positive cells mistaken for hearing, bench folklore
mistaken for chronic data, tissue presence mistaken for patency.
With D1–D17 (as amended by J1-DISSENT-1/2/3) applied, the headline
is unchanged: **no candidate promotable (G3b BLOCKED), no gate PASS
anywhere, FROZEN retained by default, B killed-as-specified under a
recorded disagreement this judge upholds, every other kill test
unevaluable, Q0 UNDECIDABLE-no-data.** This is triage; the freeze
decision belongs to the named human experts, whose slots are still
PENDING.
