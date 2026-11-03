# Gen 2 external adjudication

Model: gpt-6-astra via Muse  
Date: 2026-11-02  
Role: independent external judge — triage only

The header follows the requested commission; it does not independently authenticate backend routing. The inspected Gen 2 files and this execution are dated 2026-11-03, so the requested header date is not a claim that this review preceded those files. Reviewed repository HEAD: `46201f14263a9615d2d816d4b79dfd1227c75d57`. Human extraction, ratification and freeze authority remain unchanged.

**Adjudication: uphold the computational tie and NO PROMOTION; partially reject the four-new-designs account. P2 is a useful incremental repair, H2 introduces a distinct measurement question but misdefines its proposed NI endpoint, Q1 substantially repackages an already specified decider, and R1 adds a useful rule audit while overstating what the original rule claimed. PMID 42362868 is correctly fenced as late-found Design and non-deciding evidence. Continue with bounded gap attacks and human measurement work; do not launch another design-only Gen 3 now.**

I read the requested summary, score, sweep (including §5), and prior external review, then checked the four candidate files, fitness application, adaptation note, CSVs, scorer, parent specifications, Q0 thresholds/verdict, held-out rules, relevant GOAL provisions and prior gap plan. I also inspected the live PubMed record and publisher abstract for PMID 42362868. This is neither a new systematic search nor full-text human dual extraction. Only this review file was written; calculations and comparisons used stdout/in-memory objects with Python bytecode writes disabled.

**1. The tie is reproduced, with a candidate-class qualification.**

Executed:

```text
PYTHONDONTWRITEBYTECODE=1 python3 research/scoring/gate_table.py research/gen02/scoring/adapted-gen2.csv
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/scoring -v
```

The CLI exited 0. Its output agrees with the filed matrix, allowing for the CLI's extra terminal newline. Independently calling `render_markdown(summarize(rows, build_gate_matrix(rows)))` reproduces the filed matrix **byte-for-byte: 2,850 bytes**, SHA-256 `a9e45c1ff39e99f36f5a715970722be08e6cf00e6965ba3832e974d2ae9c3980`. All **18 scoring tests passed**, including the printed Astra probes.

| Object | Independent result |
|---|---|
| Gen 2 extraction | 33 rows: 19 INSUFFICIENT, 13 NA-prereg, 1 PROVISIONAL-SIGNAL; 0 PASS, 0 FAIL; all RECORD / UNASSESSED |
| Adaptation | Stock adapter returns 0 rows; applying the documented P2/H2 ID map in memory exactly reproduces all 16 filed records |
| P2 and H2 | Each: G1 NA; G2/G3a/G3b/G4/G5/G6 INSUFFICIENT; 0 FAIL, 6 INS; all numeric fitness inputs absent; promotion FALSE |
| Parent comparison | P2 equals P1 and Ga; H2 equals H1, on every gate and every fitness-key element except candidate name |
| Combined Gen 1 + Gen 2 | 57 rows; F1m/Ga/H1/P1/H2/P2 tie, followed by A1 with its carried 1 FAIL / 6 INS |
| Forced Q1/R1 inclusion | Reproduces the spurious R1 0/2 and Q1 0/3 lead caused by reduced applicable scope |

Alphabetical order is not fitness. The new grade/tier and G2 mechanism-row guards do nothing on these inputs. The prior review's broader aggregation concerns remain: required-cell completeness, evidence-body adjudication, compatible estimands and prospective human authorization are not proved by these passing tests. No FROZEN superiority or clinical equivalence follows from this all-insufficient tie.

Excluding Q1/R1 from pathway ranking is correct. **H2 deserves the same conceptual treatment:** its §§1/6/8 explicitly describe a measurement-only study with no frozen-care contrast and no ability to earn its own G3a PASS. Carrying H1's full footprint avoids an artificial improvement, so the filed tie is conservative, but calling H2 a “promotable survivor” is a category error. Keep its historical rows visible; prospectively place H2 beside measurement/attack deliverables and retain H/H1 as the intervention candidates. A cell manifest alone would not make Q1/R1/H2 commensurable with pathways.

The no-improvement ledger can remain **2/2 as disclosed exploratory bookkeeping**; reclassifying H2 supplies no improvement and cannot reset it. This is not certification of two compliant frozen generations. Gen 2 again lacked its promised protocol/checklist/manifest sequence, and counting four mixed-class documents does not establish four eligible new pathway candidates under GOAL §7. STOP remains unmet on the recorded gap conjunct; neither compulsory Gen 3 nor completed formal abandonment follows.

**2. Novelty is mixed; the anti-rewording audit is too self-certifying.**

| Filing | What is genuinely added | Judgment |
|---|---|---|
| P2 | A committed stepped-wedge design, unified audit ownership, and a zero-tolerance documented-hold rule replacing the defective median criterion | Useful operational mutation/recombination; accept incremental novelty, reject first-ever attributable-delay claims |
| H2 | A standalone investigation of scale-dependent classifications and an explicit discordance deliverable | New measurement question beyond H1's dual reporting, but its proposed NI endpoint needs substantive repair |
| Q1 | A more detailed integrated animal protocol outline, control arms, transport/FMEA provisions and named responsibility | Useful elaboration of an existing gap attack; does not establish a new falsification question |
| R1 | Separate contralateral and same-ear re-administration questions, evidence standards and a dependent-claims audit motivated by newly located evidence | Useful new audit structure; not discovery that G4-AAV can be falsified, and not a new treatment candidate |

**P2:** [P1 §3](../research/gen01/candidate-P1-sequenced-pathway.md) already required per-child genotype/timeline records and gene-first capture without triage-caused delay; I3 already killed protocol-attributable delay. P1 §10 expressly required one timeline per child, weekly delay audits and attributable-delay events. Therefore P2 §2's claims that attribution exists in neither parent and cannot be observed without fusion are false as written. Its actual advance is a better operational definition and ownership, not a new causal question. A logged genotype hold is a process violation, not necessarily an equal-length delay in final activation; undocumented holds and scheduling slack remain possible. Preserve the separate comparative time-to-activation analysis and finish attribution, missing-log, audit and precision rules before calling the kill executable. A design stop event also is not automatically a human-graded G4/G5 harm FAIL.

**H2:** [H1 §3](../research/gen01/candidate-H1-encouragement.md) already specified instrument-norm versus P0-sample SD reporting, dose/proficiency records and video validation. The distinct addition is testing disagreement rather than simply reporting both scales. However, [H2 §3](../research/gen02/candidate-H2-norming.md) proposes *per-child* NI classifications by comparing an individual score with −0.2 SD. GOAL §4.2 defines that margin for a **pathway-versus-frozen contrast within stratum/window**, not an individual developmental cut-off. Without the comparative estimand, H2's classification cannot stand in for gate NI.

Moreover, an exposure-conditional residual score changes the reference target, not merely the SD denominator; used downstream it could remove part of the exposure effect the pathway intends to estimate. Discordance proves non-interchangeability under the chosen rule, not invalidity of every possible signed-language measure; concordance alone establishes neither validity nor stakeholder ratification. The useful repair is to study scale properties and sensitivity of defined comparative effect estimates, keep individual descriptive scores separate, and precommit uncertainty and out-of-sample assessment. H2 remains valuable measurement work, not evidence clearing H's harm question or G3b.

**Q1:** the decisive counterexample is [Gen 0 Q0-verdict, lines 191–207](../research/gen00/Q0-verdict.md#L191): it already specifies an established-implant/fibrosis-course AAV decider, same-study unimplanted comparator, blinded A1/A2 readouts, per-arm denominators and independent replication, followed by a prospective cannulability n/N decider by time band. Q0-thresholds §§2.1–2.3 define those estimands; Round 2 W6a again requests their execution. Q1's “first primary generation” is only a plan, and “first candidate file” is not a scientific novelty criterion. Its integrated controls and large-animal commitment are useful refinements, but species, construct, dose, course and N are still deferred. Classify it as the elaborated Q0 attack, not a fourth new question. A functional rescue design also needs a model in which the selected construct can plausibly restore function; generic deafening plus a later choice of an OTOF construct does not establish that compatibility.

**R1:** GOAL §4.2 already contains the escape clause **“or post-exposure later-AAV efficacy is shown.”** R1 §1 truncates that clause, while §2 calls the rule an untested axiom and §3 targets universal impossibility claims. A precautionary default with an explicit evidentiary escape is not equivalent to “never again anywhere.” Mapping the actual dependent claims to the two re-dose sequences is worthwhile. Established-implant delivery belongs to the separate Q0/patency issue; R1's fence assigning it to Q1 is correct, but it should not be described as a biological leg actually asserted by the G4-AAV wording. Failure correlated with NAbs would not by itself establish NAbs as the cause or confirm a universal barrier. Same-ear studies must distinguish second-dose delivery/expression from persistence of first-dose transduction and benefit; endpoint ABR alone cannot do that.

These findings reject the assertion that exactly four genuinely new questions exhaust the design space. They do not make Gen 2 worthless: repair, measurement development and evidence auditing have value even when they are not new candidates or fitness gains.

**3. PMID 42362868: correct current disposition; overstrong retirement promise.**

The live record confirms publication on 26 June 2026, a single-arm contralateral re-administration study with four children aged 2.2–3.4 years and pre-existing NAbs. The reported second-ear 26-week ABR values are 43/63/80/53 dB from baselines above 95 dB. The abstract reports no six-week dose-limiting toxicity, one grade-3 neutrophil decrease, and no serious adverse events. Those figures match the sweep. [PubMed record](https://pubmed.ncbi.nlm.nih.gov/42362868/); [publisher abstract](https://www.nature.com/articles/s41591-026-04505-4).

Under the filed temporal/by-study manifest it is **late-found Design, not validation**. Full-text extraction cannot change that allocation. It supplies a relevant preliminary counterexample to categorical second-ear impossibility, not post-CI access, established-implant efficacy, same-ear re-dosing, a pathway effect, or general safety. The accessible abstract does not itself document every treated ear's implant history; confirm that detail in full text/registry. Regardless, it supplies no established-implant comparator or Q0 retention estimand. The narrow PROVISIONAL-SIGNAL → INSUFFICIENT treatment and unchanged formal applications are justified. The filed validation count remains zero; this spot check does not independently reproduce the entire sweep.

Two corrections are necessary:

- **Extraction alone does not meet R1's own retirement standard.** R1 §3 additionally requires ≥Moderate human-assessed GRADE and at least one non-inventor or held-out-side input. This same pre-freeze inventor-program report cannot acquire independence by being read more carefully; its registry is not an independent study. Gen2-summary §4(3) and score-gen2 §§4/6 overpromise the shortcut unless an additional qualifying input is located or humans prospectively amend that borrowed standard. Extraction can narrow rhetoric and complete a valuable attack without formally retiring the leg.
- **Do not transfer every promotion requirement to every rule question.** Lack of the G2/G3 surrogate chain prevents a listening/language promotion claim; it is not itself a reason to disregard ABR evidence of later-AAV activity when judging the narrow immunity proposition. Conversely, a credible counterexample to a universal claim does not establish transportable safety or lift all C/D G4 requirements. R1's added retirement rules are a proposal awaiting ratification, not silently binding GOAL text.

Keep the presumptive policy status separate from the biological narrative: the rule can remain operative while its strongest rhetorical interpretation is already challenged. “Unresolved under the decision standard” is more accurate than “untested” for a leg with relevant empirical observations. No new gate PASS or Q0 change follows here.

**4. Gen 3: attacks now, no new design generation now.**

My prior review did not require a changed verdict before any worthwhile design work. That remains true. Gen2-summary §4 turns a sensible resource recommendation into another excessive prohibition when it says a generation that can only tie should never be filed. A genuinely distinct, tractable future test could still merit consideration. Nothing here, however, justifies commissioning another batch now or proves that a fifth idea must be rewording.

The next work should be **a bounded attack/completion round outside the generation counter**. Do not rename gap attacks “Gen 3” to advance the clock. Prioritize:

1. **R1 evidence audit:** obtain the full report and ChiCTR record, reconcile cohort overlap and treated-ear history, extract sequences/NAbs/outcomes/harms, map actual dependent claims, and adjudicate the retirement rule with humans. This is the nearest document-based decision opportunity. It need not produce a retirement to count as a completed, well-defined attack; repeated readings of one study do not create independent evidence.
2. **G3b and measurement authority:** commission the Deaf/parent co-design deliverable identified in the prior review, with named measurement leadership, instrument/MCID/NI specifications and feasibility evidence. Repair H2's estimand alongside it. Filling signatures alone does not complete measurement development; co-design itself does not earn G3b PASS.
3. **Executable protocols:** finish P2's audit and comparative margins; obtain a feasible laboratory/model plan for Q1 and a second-dose-specific readout for R1(c). Execute only when the necessary people, parameters and resources exist. Keep A1's named-device/convergence prerequisites explicit. These are distinct dependencies, not a requirement to finish every human gate before any retrieval or model feasibility work can proceed.
4. **Prospective scoring readiness:** define candidate classes, required cells and evidence aggregation; commit the applicable protocol, analysis owner, margins and held-out allocation before opening deciding evidence. Do not retroactively repair the Gen 2 sequence or turn late-found Design into validation.

A later **Gen 3 candidate generation** is defensible if completed attacks or measurement decisions motivate a concrete new intervention/interface specification with an honest prospective comparison. Existing candidate evidence updates need not manufacture new candidate IDs merely to use results. If no such executable work is available, the appropriate decision is **no Gen 3 for now**, with an explicit deferred-work record and bounded monitoring cadence—not a third scored tie, not deletion of the debt, and not a claim that discovery is formally complete.

FROZEN remains the default, G3b remains blocked, Q0 remains undecidable, and no kill has been cleared by this review. The right next unit of progress is a completed decision-relevant attack or human measurement deliverable, not another document count.
