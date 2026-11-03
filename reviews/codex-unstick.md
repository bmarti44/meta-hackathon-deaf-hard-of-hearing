# Codex unstick review

**Date:** 2026-11-03. **Reviewed HEAD:** `59a8798ede27cedf3da701ea009cc61da6f4a873`.
**Role:** agent research/audit, not human extraction or adjudication. Commissioned as Astra/GPT-6 through Codex; backend model identity and effort are not independently exposed by this workspace. The user's routing instruction governs this commission; no Muse or Sol execution is claimed. No sub-agents used.

**Concurrent amendment detected at final verification:** another workspace process committed `d719ea394c588b4dd96616e166db8ac4de116c5e`, changing GOAL to v2.3 and removing the generation cap/loop stops under recorded holder direction. I inspected that diff. The promotion gates and human-freeze requirements are unchanged. This commission did not edit GOAL or STATUS. The original audit records the v2.2 snapshot; [the current-state rerun](../research/unstick/audit-results-current.json) records v2.3. The requested v2.3 repair proposal below is therefore rebased as a **proposed v2.4/addendum**, not confused with the already committed cap-removal amendment.

**Finding: a legitimate next unit of work exists, but no legitimate clinical winner has been uncovered.** I located previously unfiled primary comparative evidence and measurement resources, reproduced the negative scores, executed scorer probes, and prepared an actionable measurement-study proposal. The strongest route out is to repair the distinction between **readiness to study** and **evidence of benefit**, qualify G3b, and evaluate the existing pathway on prospective comparative data. The live v2.3 amendment permits further generations; this review creates none and supplies no retroactive PASS. Removing the cap does not change the evidence verdict.

The holder's persistence directive authorizes continued useful work; it cannot supply missing participant outcomes, stakeholder decisions or independent human judgments. Describing any of those as completed would defeat the requested legitimacy test.

## 1. What I tried and executed

I read GOAL.md, STATUS.md, LOOP-EXHAUSTED.md, W1–W8, Step5-decision-no-winner.md and both `codex-astra-*.md` reviews, then inspected AppendixA-v1, the current scorer/manifests, Ga/P4/QR4 specifications, the G3b commissioning brief and the evidence partition. Historical documents are interpreted with their dates; W1–W8's references to a future Gen 2 are now stale.

| Attempt | Executed result | Artifact |
|---|---|---|
| New literature and registry access | Targeted searches, primary-source section inspection, correction checks and access failures recorded; new DESIGN inputs found, no validation allocation | [Inspected-source ledger](../research/unstick/inspected-sources.md) |
| Missed PASS / current computation | Gen0–4 main matrices reproduced byte-for-byte, including Gen3/4 manifests; 322 rows = 297 INSUFFICIENT, 17 NA, 8 FAIL; all grades UNASSESSED | [Audit code](../research/unstick/audit.py), [executed results](../research/unstick/audit-results.json) |
| Satisfiability and scorer audit | Nine synthetic contract probes, distinguishing repaired issues from remaining problems; no production scorer changed | Same audit/results |
| Decisive next study | Existing-instrument qualification design, staged decisions, independent validation, recruitment arithmetic, named owner roles and explicit no-go conditions | [G3b qualification study](../research/unstick/G3b-qualification-study.md) |
| Governance repair | Requested v2.3 repair text, rebased below as a proposed next amendment after the concurrent v2.3 commit; for holder plus independent co-approver | §5 of this review |

Executed `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/scoring -v`: **27 tests passed**, plus the existing printed Astra probes. This establishes software consistency, not complete gate implementation. The 322 count covers the main adapted candidate tables; it is not 322 independent studies or all auxiliary attack rows. No A1 simulation rerun was needed for these findings.

## 2. New evidence: a real lead, not a hidden win

The most consequential missed paper is the **2025 GT-versus-CI cohort**, now inspected at the publisher after PMC access failed. Its speech-in-noise comparison is against unilateral CI, so its apparent threshold-sized benefit cannot pass the frozen bilateral G2 contrast. The adverse localization direction also matters. Exact subgroup counts, units, correction and limitations are recorded once in U1/U1c. This is a meaningful comparative research lead, not an efficacy result attributable to Ga/P4. [Cheng et al., corrected primary article](https://jamanetwork.com/journals/jamaneurology/fullarticle/2836395).

Other newly located inputs are U2's pediatric channel-count experiment, U3's early-childhood QoL-CI development paper, U4's HIP-QL validation abstract/corrigendum pointer, and U5's 2026 OTOF follow-up abstract. U2 strengthens the comparator-definition concern; U3/U4 make the G3b work more concrete; U5 informs durability questions. Their scope and access limits are in the ledger. None supplies the full assigned-pathway comparison, human-reviewed Moderate GRADE, required outcomes and NI evidence.

The re-administration abstract U6 remains the already-known narrow challenge to categorical second-ear impossibility. The larger U5 report shares its registry/program and cannot be treated as independent replication without participant-overlap reconciliation. I did not obtain a new established-implant same-ear AAV comparison or the unavailable registry contents. I do not have a secret paywall route.

**Evidence disposition:** U1–U5 are late-found pre-freeze DESIGN, U6 remains DESIGN. No new source was inserted into historical extractions or re-sided as validation. Full-text inspection improves what can be assessed; it does not create human verification or independence. The source ledger separates inspected full-text sections from abstract-only pointers, as GOAL §9 requires.

## 3. What is actually broken, and what is merely demanding

### A. The handoff/promotion dependency is circular in the loop's interpretation

GOAL §5.1 promises synthesis and prioritized study designs; §11 Step 5 specifies an animal/adult study-design handoff. Sections 4–5 require pediatric comparative language and other outcomes for infant promotion. Historical LOOP-EXHAUSTED §1 nevertheless calls handoff impossible while G3b is blocked. If clinical promotion is a prerequisite to handing off the study that generates its evidence, the program cannot start. The concurrent v2.3 amendment makes handoff a milestone rather than a stop but does not yet define a separate readiness standard.

This does **not** make T4 wrong. T4 is appropriate for infant benefit claims. The repair is a separate, explicitly non-promotional readiness decision, with human expertise and ethical/study feasibility checks. It must never be represented as Branch A benefit, a clinical win, or proof of C0. The current no-winner record remains intact even if that process amendment is adopted.

### B. G3b is an intentional safeguard; its execution dependency needs work

An agent cannot replace co-design with a questionnaire nomination or waive autonomy because auditory measures improved. There are now concrete instruments to evaluate, but none inspected establishes this project's complete instrument/MCID/NI specification. The [qualification study](../research/unstick/G3b-qualification-study.md) turns W2 into a falsifiable work package. Qualified measurement would enable scoring, **not** earn a comparative G3b PASS.

### C. Several scoreability obstacles remain after the earlier repairs

| Executed synthetic probe | Observed current behavior | Implication |
|---|---|---|
| G2 W3 PASS plus W0 mechanism INSUFFICIENT | G2 PASS | Earlier structural mechanism-row bug is repaired; do not report it as still present |
| T0/Moderate G1 labelled PASS | INSUFFICIENT | Earlier gate-level tier bypass is repaired |
| Old INSUFFICIENT study and later qualifying PASS, same G2 cell | INSUFFICIENT | Scorer takes worst supplied verdict; it cannot adjudicate a growing body of evidence |
| G3a W1 no-superiority record encoded INSUFFICIENT plus W3 PASS | INSUFFICIENT | NI success needs a distinct criterion/role; lack of early superiority is not failed NI |
| T2 residual-hearing row labelled G4 PASS | G4 PASS | Whole-gate tier minimum fails to enforce the T4 residual-hearing requirement |
| One G4 component/stratum with whole-gate manifest | G4 PASS, zero missing cells | Manifest does not prove component/stratum completeness |
| G2 T4/Moderate PASS label with numeric gain 0 | G2 PASS | Verdict labels are trusted; numerical thresholds/estimands are not checked |
| G3b input PASS or FAIL while blocked | Both become INSUFFICIENT | Deliberate block on promotion; a future harm-veto record must not disappear behind an administrative status |

These probes use fictional rows, not evidence. In particular, the G3a probe does **not** demonstrate that actual W1 NI evidence exists: the current schema cannot distinguish successful NI from an unavailable superiority estimate. The scorer is a screening tabulator, not a complete authorization engine. A prospective successor needs criterion-specific adjudicated evidence bodies and an explicit readiness/authority layer. Simply changing `worst` to `best` would conceal contrary evidence and is unacceptable.

### D. The comparator ruler has errors, but correcting them does not create benefit

Eight configured channels, eight selected maxima and eight independently discriminable places are different quantities. AppendixA-v1 already acknowledges that the ripple-to-effective-channel conversion is unvalidated. U2 adds older-child comparator data, not a conversion or an infant device result. Replacing the frozen point with a conveniently weaker setting would create a false win; head-to-head comparison with actual contemporary settings must remain required.

AppendixA-v1 §2 also says an UNPINNABLE historical absolute prevents PASS even when a candidate reports a concurrent comparator contrast. That is an avoidable scoring obstacle: an appropriately locked, measured concurrent comparator can identify a contrast without a known historical mean. This does not excuse unmeasured comparator contents, unratified margins, a missing P0 coverage denominator, or an inadequate study.

G4 zero-loss directions, unknown safety margins, and the joint 3 dB / 0.4 SD requirements are stringent; stringency alone is not proof of logical impossibility. Margins require scientific and stakeholder justification, not adjustment until the favorite passes. The worked example in §8 is a hypothesis, not a proof of an empirically attainable joint result: it omits G2 in its list and supplies no effect data.

There is also a pathway accounting issue worth resolving before any freeze. Ga says it administers no AAV, but its assigned strategy includes gene-first treatment for eligible children. Under GOAL's treatment-policy estimand, downstream AAV exposure still belongs to that branch's G4/G5 assessment. No-AAV status at the decision origin does not establish future redosing preservation. Apply the existing later-AAV escape clause to the actual branch/construct/ear/sequence; neither automatic blanket failure of all children nor administrative exemption of all pathway-directed exposure is defensible.

### E. No on-disk PASS was mis-scored into the current tie

The current main tables contain no human-assessed qualifying evidence body. Earlier positive signals retain their comparator, tier, endpoint or replication limits; the new U1 paper does not cure those limits. No evidence found establishes every required gate for any candidate. Unblocking G3b, adding sources, fixing aggregation, or resolving the A/G6 administrative FAIL would not alone produce a winner.

## 4. Ranked unstuck plan and ownership

| Rank | Concrete next output | Agent work | Human owner / deciding act | Completion means |
|---|---|---|---|---|
| 1 | G3b measurement qualification, using the prepared study | Source packets, corrections/access log and planning arithmetic completed; support forms/analysis after protocol lock | Holder funds/names PI; paid Deaf/parent panel defines acceptable loss; measurement lead executes; independent validator adjudicates | Supported cells gain a ratified instrument and margins; no gate PASS yet |
| 2 | Resolve readiness versus promotion and comparator/aggregation semantics | This amendment and executed probes completed | Holder + independent co-approver, with §9 expert panel | A viable upstream study can be approved without pretending downstream outcomes already exist |
| 3 | Human dual extraction of U1 plus supplements; U3/U4 including corrections; U5/U6 cohort overlap | New search/section extraction and exact failure log completed | Independent extractor(s), adjudicator and GRADE/ROBINS-I lead | Reconciled DESIGN evidence body and explicit updated uncertainties; no automatic validation credit |
| 4 | Implement/test an opt-in successor to the tabulator | After semantics are ratified, implement criteria, component/stratum/stress completeness and provenance; preserve historical mode | Analysis owner and independent reviewer approve specification and acceptance cases | Demonstrably accepts synthetic eligible successes and rejects missing/low-tier/unsafe cases; still no empirical PASS |
| 5 | Execute the existing Ga/P4 prospective pathway comparison | Prepare data dictionary/SAP and held-out plan with trialist | Trial PI, statistician, clinicians, stakeholder panel and ethics board | Treatment-policy outcomes versus measured valid comparator; all applicable gates assessed, not surrogate-only gains |
| 6 | Q0 established-implant decider if its result would change a specified pathway decision | Retrieve model/construct evidence, support QR4 sizing and protocol | Translational PI/lab and ethics oversight | Actual patency/transduction/function data; a G4 input, not joint promotion |

Ranks 1–3 can proceed in parallel as workstreams without agent fan-out or a new generation. The dependency is **design/measurement derivation → ratified lock → unopened validation → adjudication**, not W6 data first and W7 freeze later. Do not demand every human appointment before ordinary source retrieval. Conversely, do not present a role table as a recruited team.

The single recommended study is Rank 1. Its proposal includes an initial 18-family cognitive-interview allocation, a separate derivation phase, and a proposed independent validation target of 100 evaluable families per window×modality cell. Those are explicit planning conventions with precision calculations and stop conditions, not enrollment forecasts or a claim that a small pilot can establish every margin. The resource commitment is substantial and must be assessed honestly. No experiment has been run here.

## 5. Requested GOAL v2.3 repair proposal — rebased as v2.4/addendum, NOT ADOPTED

The following text is proposed for prospective adoption by holder plus independent co-approver with the required expert/stakeholder participation. It neither changes GOAL.md nor authorizes current scores. The live v2.3 number now belongs to the concurrent continuation amendment; use v2.4 or an explicit addendum for this distinct repair. Record the adopted wording, votes/dissent, effective date, evidence already seen and affected protocol versions. Do not rewrite Gen0–4 history.

**Amendment A — add to §§4.2, 5.1 and 11; clarify §7(5)'s handoff milestone:**

> Three decisions are distinct: (i) open evidence synthesis, (ii) STUDY-READY handoff, and (iii) EVIDENCE-PROMOTED benefit. STUDY-READY requires named §9 human reviewers; a specific falsifiable question; a locked feasible design, comparator and analysis; justified measurement at the proposed study stage; resources, owner, ethics/regulatory route, harms/rescue rules and a declared route to resolving remaining gates. A measurement-development handoff may explicitly aim to establish an instrument or margin; that instrument may not authorize treatment-effect scoring until independently qualified and ratified. STUDY-READY does not require results that the proposed study is designed to generate, is not a clinical winner, and grants no PASS, C0 confirmation, ≥90% claim or infant-use permission. EVIDENCE-PROMOTED retains all existing applicable joint gates, tiers, evidence-quality, independence, stress and human-verification requirements. A human-approved STUDY-READY handoff is reported as a research milestone separately from evidentiary promotion; it does not terminate continuation under v2.3 §7(5). Historical no-promotion decisions remain no-promotion.

**Amendment B — add to §4.2 and the scoring contract:**

> Separate study records from adjudicated criterion-level evidence bodies. Define each required criterion by candidate class, gate/subcomponent, window, stratum, scenario, estimand, comparator, instrument, tier, grade and decision rule. Preserve all study records and contrary evidence; a new adjudication must explicitly account for them and preserve prior versions. Missing required evidence remains INSUFFICIENT. G2 W0/W1 mechanism records do not vote as outcome gates; their chain/mediation requirement remains explicit. G3a requires the stated superiority in at least one eligible W2/W3 comparison plus NI in every required measured stratum/window, using distinct superiority and NI criteria. Unvalidated secondary endpoints remain visibly unresolved and retain their predeclared required/exploratory status. No endpoint becomes optional after its results are seen. G4/G5 enforce all applicable component/harm tiers and margins; no whole-gate minimum substitutes for a component's stricter requirement. Human-approved synthesis, not best-study or worst-study voting, determines each criterion. The scorer verifies the complete declared evidence/authority contract before any promotion claim.

> G3b instrument readiness is recorded separately from efficacy/harm judgments. Until co-design and qualification are ratified, no G3b PASS is possible. Relevant adverse findings remain visible and require human safety adjudication; an administrative block must not erase them.

**Amendment C — reconcile §3.4 and Appendix A comparator measurement:**

> Freeze comparator contents, fitting, eligibility, timing, setting and measurement procedures before deciding evidence is opened. A valid within-study concurrent comparator may supply the reference estimate and its uncertainty when the historical absolute is unavailable. Historical UNPINNABLE status alone does not defeat an otherwise valid contrast; unmeasured comparator contents, inadequate overlap/identification, unratified margins or missing required outcomes still do. Keep the existing frozen-versus-evolving-standard claim cap: beating only lagging care is an implementation-gap finding, not a C0 win. Do not withhold currently indicated care to reproduce a historical comparator; where an ethical concurrent frozen arm is unavailable, prospectively specify an appropriate design and its limits or amend the comparator with co-approval.

> Retain the 8-channel convention and its disclosed sensitivities as historical reference, not an empirical universal ceiling. Distinguish electrodes, maxima, ripple performance and independently discriminable channels. A device G1 PASS still requires the stated ≥12/≥16 effective-channel criterion with a valid measurement definition, head-to-head functional advantage and required replication/translation. If the effective-channel ruler cannot be validated, leave G1 unresolved and commission measurement work; changing the G1 endpoint requires a separate justified prospective amendment, never a post hoc conversion.

**Amendment D — clarify pathway exposure and scope, without relaxing gates:**

> Apply treatment-policy accounting to all interventions assigned by a pathway, including externally delivered AAV and rescue CI. Predeclare branch-specific applicability and transport limits. AAV later-treatment preservation is assessed for the actual construct, ear and sequence; evidence of contralateral redosing does not establish same-ear or post-CI preservation. A branch-specific finding is not a P0-wide win. Preserve P0 denominators and report unrepresented strata explicitly. A portfolio cannot obtain a benefit claim by relabelling its components as measurement studies.

**Amendment E — add to §§7 and 12:**

> Preserve Gen1–4's historical exhaustion record, while applying v2.3's authorized continuation prospectively. Bounded retrieval, source correction, measurement qualification, scorer validation and new-evidence adjudication for existing specifications are not intervention generations and may continue with an owner, falsification/completion target, resource plan and dated record. New generations retain the remaining §7 candidate-specification, anti-rewording, evidenced-interface and prospective-lock requirements; document why each proposed experiment could resolve a live decision. Already seen evidence stays DESIGN; extraction upgrades, new model access and amendment approval do not turn it into validation. All future decisions distinguish declaration, specification lock, evidence opening and human adjudication. No agent can ratify its own gates or authorize a clinical winner.

These amendments fix scope and scoreability; they do **not** reduce 3 dB to a favorable observed effect, drop G3b, replace T4 with animal signals, relax the required grade, or undo the holder's live continuation instruction. Any later substantive endpoint/margin change must be justified and named as a new prospective claim with historical results preserved. They make valid future evidence representable; they do not promise that a candidate will achieve it.

## 6. What now legitimately works

The executed audit works and is reproducible. Previously unfiled comparative evidence and measurement resources are now inspectable in a bounded ledger. The highest-leverage human study is specified far enough to assess workload, decision rights, measurement failures and validation independence. That is substantive progress beyond another tied candidate generation.

**Current evidence decision remains NO PROMOTION.** G3b is BLOCKED; the proposed baseline is not yet human-frozen; validation count remains zero. The historical clock was 4/4, but live GOAL v2.3 has removed that cap. A treatment winner cannot honestly be declared on this record. No approval question is needed to deliver this commission: the requested review, source analysis, executed audit and amendment draft are complete. Adoption and the actual human research are separate future acts.

**Agent contract:** `complete = true` for this bounded commission; `evidence[]` = linked inspected-source ledger, current repository documents/code and executed audit outputs; `unresolved[]` = human instrument/margin qualification, human extraction/GRADE, source supplements/access, comparator and scorer ratification, prospective comparative outcomes, funding/team appointments and all existing unresolved promotion gates. The paper-only constraint is preserved.
