# A decisive next study: qualify an accessible G3b measure

**Design proposal, 2026-11-03; not registered, funded, approved or executed.** Existing G/H/P4 pathway specifications are context, not new treatment candidates. G3b remains BLOCKED. This is a measurement study outside the generation clock. No participant data are collected or stored in this repository.

The falsifiable question is: **Can an existing or minimally adapted instrument measure communication autonomy and family outcomes across the declared P0 windows and communication modalities, with acceptable measurement error and a defensible NI margin?** A negative answer is useful: it prevents a convenient but invalid questionnaire from creating a false pathway win.

This is the highest-leverage *next* study because every Track-P promotion depends on its result, whereas a positive Q0 result addresses only preservation. It is not the most direct test of C0; the eventual prospective Ga/P4 comparison remains that test. Selection here is a dependency/tractability judgment, not an empirical expected-value calculation.

## Decisions, people and scope

| Responsibility | Owner to appoint | Required deliverable |
|---|---|---|
| Funding, independent appointments | Holder | Named PI, protected stakeholder budget, sites/accessibility resources, calendar and budget ceiling |
| Construct and acceptable loss | Paid Deaf-community and parent decision panel; independent chair | Plain-language/ASL construct map, decision rights, dissent record, NI and superiority decisions |
| Instrument development | Measurement scientist with DHH experience | Versioned instrument, translation/accessibility plan, analysis plan |
| Independent validation | Separate psychometrician/statistician and clinical research team | Locked validation analysis, no access to treatment comparisons during endpoint selection |
| Consent, recruitment, data handling | Qualified institution/ethics board | Appropriate approvals, accessible consent, secure study system; no changes to care |
| Source retrieval, forms, reproducible analysis | Agent, supervised by the above | U3/U4 evidence packets, item-review worksheet, scripts, missingness/floor/ceiling reports |

No invitations or messages have been sent. Roles are deliberately not represented as recruited people.

## Stage A: select or reject the ruler before validation

1. Start with U3 QoL-CI and U4 HIP-QL in [the inspected-source ledger](inspected-sources.md). Retrieve U4 full text/corrigendum and actual item sets/permissions first. Search other existing instruments with a librarian; this bounded shortlist is not exhaustive. Respect age ranges; a CI-specific instrument cannot be assumed to work in children receiving no CI or a gene therapy.
2. Panel defines separately: communication agency, participation/family inclusion, burden, and broader QoL. It decides which are required domains and whether a total score could hide a loss. Hearing detection or spoken speech alone cannot define success. An added ASL translation is not, by itself, evidence of measurement equivalence.
3. Minimum initial cognitive-interview sample: **18 families**, two in each of nine cells formed by W1/W2/W3 and signed/spoken/bimodal communication. These are proposed recruitment cells, not normative classifications of children. Oversample additional disabilities, hearing and Deaf parents, and underserved/home-language groups. Continue interviews if new material construct problems appear; 18 is a starting workload, not proof of saturation. Unsupported languages/windows remain explicitly unsupported.
4. Obtain prospective derivation data in a separate sample, initially **20 families per cell (180 total)**, with baseline, stable-state retest at approximately two weeks, and six-month reassessment. This is an instrument/margin development pilot, not an efficacy comparison. It may be too small for a credible window-specific anchor estimate; such a cell does not advance automatically.
5. Use stakeholder-defined, accessible change anchors for minimally worse, unchanged and minimally improved functioning. Examine anchor relevance and association, response shift and proxy limitations. Report raw units and uncertainty. Estimate a minimal-important-change range; the panel chooses the largest acceptable loss for NI, with rationale. **No default 0.2 SD or reliability coefficient becomes an MCID.** Measurement error may make the desired margin unresolvable; that is a stop/revise finding, not permission to enlarge the margin.
6. Lock instrument/version, scoring, age/window rules, required domains, missing-item handling, translations, longitudinal anchors, superiority MCID and NI margins before opening Stage B. Lock confirmatory hypotheses for content/construct validity, test–retest precision, responsiveness and modality invariance, including numerical equivalence bounds chosen by the measurement team/panel from Stage A. No underived equivalence bound is supplied here.

**Stage-A exit:** signed, testable measurement specification with no blank deciding threshold. Otherwise revise or stop; no Stage-B enrollment under an incomplete specification. This is the unavoidable human value/measurement decision, not an agent permission ritual.

## Stage B: independent prospective qualification

**Planning target:** 100 evaluable families in each of the same nine cells: **900 evaluable, 1,125 recruited assuming 20% attrition**. These are planning assumptions, not estimated eligible counts or power. Recruit across sites; pre-specify how age-window transitions and changing communication exposure are handled. Include disabilities; inaccessible assessments count as instrument feasibility failures rather than silent exclusions. Recruitment counts and reasons for nonparticipation remain visible.

At n=100 per cell and a hypothetical 10% missing-response rate, a simple independent-binomial 95% half-width is about **5.9 percentage points**. Zero observed failures among 100 gives a one-sided exact 95% upper bound of **2.95%**, not zero risk. Arithmetic is executed in [audit.py](audit.py) and [audit-results.json](audit-results.json). Site clustering and attrition can worsen precision. The pilot must support a separate simulation-based sample-size calculation for the chosen responsiveness/invariance model; increase sample size or retain an unresolved cell if it cannot. These calculations do not establish adequate MCID precision or ≥90% joint promotion probability.

Collect baseline and six-month scores/anchors; obtain two-week stable-state retests from a preselected subset (initial target 50 per cell, with stability reported). Analysts evaluating construct hypotheses and item functioning are blinded to pathway preference and treatment-effect comparisons. Test all required domains; do not use a favorable total score to hide a domain loss. Compare modalities within age bands using the prelocked equivalence criteria, not a nonsignificant difference test. Report differential item functioning, floor/ceiling, item missingness, administration burden and accessibility failures. Any data-driven alteration creates a new instrument version requiring fresh validation for affected claims.

**Qualification decision per cell:**

- QUALIFIED only if stakeholder content approval, accessible administration, prelocked validity/reliability/responsiveness criteria, margin justification and validation precision all hold.
- REVISE if a remediable item/accessibility issue is found; revised items do not inherit validation automatically.
- UNRESOLVED if anchors, change events or precision are inadequate. Extend under a prospective amendment or record the failure.
- REJECT if the construct cannot be measured without systematically privileging a modality or excluding required children, or the chosen score obscures a required domain's loss.

GOAL's >20% bound rule is applied to each predeclared instrument/window. A replacement selected after seeing validation results becomes a new derivation choice; it does not rescue that validation sample.

## What completion would and would not establish

A positive study supplies a prospectively ratifiable Appendix A G3b specification and permits **future G3b scoring** in supported cells. It does not supply a candidate-versus-frozen NI effect, make historical exploratory scores gate-deciding, prove C0, or earn a G3b PASS. An unsupported W3 or modality cell remains unresolved; qualifying W1 alone is not a universal unblock.

After qualification, the downstream Ga/P4 trial must compare the assigned pathway with a measured, ethically permissible comparator, retain crossovers/rescue in denominators, collect G2/G3a/G3b and relevant harms/burden together, and retain early-to-later cohort linkage. Its power must address the joint gates and rare harms; the measurement sample above cannot be recycled as that trial's sample-size justification.

The agent-executable preparation completed in this commission is the source shortlist, correction/access audit, decision structure and precision calculation. Recruitment, interviews, margin choice and validation remain human/institutional work. Calling the study already executed would be false.
