# External adjudication of the research loop

Model: gpt-6-astra via Muse  
Date: 2026-11-02  
Role: independent external judge (triage only per GOAL S9 - human experts decide freezes)

The model/transport label above follows the review commission and the route recorded in STATUS.md; repository evidence cannot independently authenticate backend model routing. This review is a separate adjudication, not human dual extraction or a freeze signature. Reviewed repository HEAD: `51252b3bf9e98f36ac709b6576c92c5d51bb9ac4`.

**Judgment: uphold NO WINNER / NO PROMOTION on the present record. No identifiable candidate × gate × window has been denied a legitimate PASS. Do not interpret this as evidence that C0 is false, that frozen care empirically dominates every alternative, or that the GOAL-compliant research program is complete.** The negative promotion decision is substantially better supported than the claims about completion, the scorer's general validity, or the exclusivity of the proposed future “win path.”

I read GOAL.md, STATUS.md, Step5-decision-no-winner.md, Step3-scoring-summary.md, Step4-gen1-summary.md, and both gap-round summaries in full. I additionally inspected the extraction tables, scorer and adapter, proposed Appendix A, relevant candidate specifications, source-verification records, held-out manifest, freeze checklist, gap attacks, and local primary-source caches. This is an audit of the supplied disk record, not a new literature search or certification that every bibliography entry is authentic. Historical files are evaluated with their dated qualifications and later corrections. Only this review was added to the repository; the requested regenerated matrix is in `/tmp/codex-matrix.md`.

**1. The no-winner verdict is correct under GOAL, independently of the matrix output.**

GOAL §4.2 requires every applicable Track-P promotion gate, including G3b, to pass. It expressly blocks all G3b cells until stakeholder co-design of the instrument and MCID. No such deliverable exists. Section 5.2 also requires at least Moderate GRADE and the appropriate evidence tier; §9 requires independent human verification of load-bearing evidence and human experts for freezes. The Gen0 extraction has 199/199 grades UNASSESSED, and the Gen1 extraction contains design records rather than measured effects. The signatures and expert roster in `research/gen00/freeze-checklist.md:116` remain pending. These are substantive and procedural reasons for no promotion, not merely a software flag.

The strongest substantive candidates also lack the necessary comparative endpoints, as detailed below. Accordingly, removing the hard-coded G3b block alone would not reveal a winner. No result establishes joint benefit under the treatment-policy estimand, all required windows/strata, and each stress scenario. C/D/E are ineligible for current infant promotion under their staging/watch conditions. Their signals cannot substitute for a Track-P preservation result.

Keeping the proposed frozen comparator as the default is therefore correct. Calling that default an experimentally demonstrated winner would be incorrect. C0 remains untested; Q0 remains undecidable on the required patency and established-implant AAV estimands. Seven Gen0 FAILs describe completeness, staging, or presumptive rules, not seven observed clinical harms.

I do **not** endorse STATUS.md:45's unqualified “Full loop Steps 0–5 complete” as compliance with §§9–11. Step 0 still lacks full-text verification of every load-bearing claim; Step 1 is not human-frozen; Gen1 lacked its required protocol/checklist/held-out update before scoring; the required named regulatory/trialist reviewer is absent. The documents disclose these failures, which is valuable. The accurate completion claim is **an exploratory agent screening loop and negative synthesis were delivered; required human and prospective-validation steps remain incomplete**. This distinction does not prevent issuing the negative triage decision.

**2. Reproduction succeeded; it establishes computational consistency, not evidentiary validity.**

Executed with Python 3.14.8, suppressing bytecode writes:

```text
python3 research/scoring/gate_table.py research/gen00/scoring/adapted_v1.csv --out /tmp/codex-matrix.md
diff -u research/gen00/scoring/gate-matrix-gen0.md /tmp/codex-matrix.md
python3 -m unittest discover -s research/scoring -v
python3 -m unittest discover -s verify -v
```

The matrix command and diff exited successfully; diff printed nothing. Both matrices are 5,395 bytes with SHA-256 `f256e1f212c92d61a0576f92bdf5dc8bf23d2b81f8eb33d09aa50702e2d91f74`. All **18 scoring tests and 13 verification tests passed**.

Independent CSV parsing and in-memory reconstruction produced:

| Object | Observed result |
|---|---|
| Gen0 original extraction | 199 rows: 170 INSUFFICIENT, 15 PROVISIONAL-SIGNAL, 7 NA-prereg, 7 FAIL; all grades UNASSESSED |
| Gen0 adaptation | 185 rows: 171 INSUFFICIENT, 7 NA, 7 FAIL; re-adapted records exactly match the filed adaptation |
| Gen0 aggregate matrix | 56 cells: 46 INSUFFICIENT, 3 NA, 7 FAIL, 0 PASS |
| Gen1 adaptation and matrix | 41 rows; regenerated matrix exactly matches the filed matrix; 35 cells: 30 INSUFFICIENT, 4 NA, 1 FAIL, 0 PASS |
| Round2 supplementation | 48 additional rows, distributed A3/B3/C12/D12/E11/F2/G1/H4; joining produces 233 adapted rows and the same Gen0 matrix bytes |

The 14 skipped Gen0 rows are the three FROZEN and eleven Q0 records. Provisional signals collapse to INSUFFICIENT as documented. These totals are internally consistent; the historical “~42 unrowed” estimate has been explicitly superseded by the 48-row reconciliation.

As an additional check relevant to the numerical claims, all **10 A1 model tests passed**, and I recomputed the 12-row v2 sweep in memory without invoking its file-writing script. It reproduces `results_v2.csv` byte-for-byte, MD5 `b9ec23c5ede0ceba47f538caafe9becb`. I inspected the filed convergence series, but did not rerun its finest-grid calculations. Solver convergence is not grid convergence or biological validation.

**3. No missed PASS: strongest counterclaims and exact cell dispositions.**

| Candidate / gate / window | Best evidence on disk | External adjudication |
|---|---|---|
| **A / G2 / W3** | Srinivasan 2013, PMID 23467170, DOI 10.1016/j.heares.2013.02.004; full text cached as `/tmp/fulltext/PMC3639477.xml`; HINT n=5, digits n=6 | The 3.01 dB HINT benefit is 15.30−12.29 against experimental monopolar. Clinical-map HINT is 10.60: the proposed strategy is **1.69 dB worse on the reported mean**, not ≥3 dB better against clinical care. Digits improvement against clinical is only 1.97−1.08 = **0.89 dB**. Clinical comparisons were not significant. Acute adult T3 evidence also cannot earn the required pediatric G2 PASS. Uphold INSUFFICIENT; these small comparisons do not establish a qualifying harm FAIL either. |
| **A / G1-spectral / W1–W3** | van den Honert/Kelsall, PMID 17552721, N=3; same study copied across child-age claim windows | Mechanistic focusing is not a demonstrated ≥12-effective-channel result with the required comparator, chain and non-inventor replication. Three window rows are one study. No PASS. |
| **GEN1-A1 / G1-spectral and G1-temporal / W3** | T0 fibrosis-proxy model, `results_v2.csv` and `convergence.csv`; Gen1 extraction rows 15–16 | Narrowing under assumptions does not establish G1 effective channels or safe-charge feasibility in the specified growing/fibrotic system. Named-device limits, growth specification and convergence criteria remain unresolved. No PASS and no kill clearance. |
| **B / G1-spectral / W1–W3; G4 / ALL** | Pinyon 2014, PMID 24760189, DOI 10.1126/scitranslmed.3008177 | Neurite-regrowth mechanism, abstract-level extraction, no verified tonotopic functional-channel result, lifetime plan or independent replication. No PASS. Deferring its specification kill would restore only an unresolved design. |
| **C / G1-spectral / W3** | Dieter 2020, PMID 32596983; Keppeler 2020, PMID 32718992, newly available full-text evidence absent from v1 rows | Keppeler's within-animal optical/electrical spread comparison is real additional mechanism evidence and deserves a future source row. It is not an overlooked PASS: acute inventor-program animal spread and n=2/arm chronic detection are not ≥16 independently discriminable channels with replication and the required chain. Sixteen emitters are not sixteen effective channels. |
| **G / G6 / W0** | Downie 2020, PMID 31827275: 59/106 versus 22/106 diagnoses | Diagnostic yield is neither a decision-time turnaround/time-to-access comparison nor the required coverage/burden/disparity result. No PASS. |
| **G / G2 / W3; G / G4 / ALL; Q0-L / G4 / ALL** | Otarmeni USPI §§1, 14: 16/20 Week-24 PTA responders; no prior CI in the treated ear | A therapy's single-arm threshold response is not the pathway's comparative SRT effect. A label eligibility restriction is not biological patency or post-CI AAV efficacy. The label fact is verified within the cached record; no candidate gate PASS follows. |
| **H / G3a / W2 signed** | ASL-CDI 2.0 norming, PMID 32180180, N=120 | Instrument availability/norming is not a +0.4 SD treatment effect attributable to the H pathway. The downgrade to INSUFFICIENT-for-effect is justified. |
| **A/B/Q0-P / G4 / ALL** | Seyyedi/Nadol and Kamakura/Nadol archival histology, PMIDs 25122600 and 27371868 | Tissue presence and volume do not provide the prespecified cannulability numerator. These are comparator-context observations, not challenger preservation comparisons. No PASS. |

F's P1/CAEP material likewise does not supply an intervention-attributable language effect. H's lack of an inner-ear intervention is not itself measured preservation across the assigned downstream pathway. Gen1 design specifications add no qualifying results. None of these conclusions relies solely on the pending human signature.

There are **classification disputes, not missed PASSes**. A/G6/ALL and GEN1-A1/G6/ALL have staging sequences but no committed numeric timeline; the candidate even defers the numeric year to handoff (`candidate-A-focal-electrical.md:340`). I favor separating “administrative timeline incomplete” from an efficacy/deliverability FAIL. The loop already carries the INSUFFICIENT sensitivity, which leaves A/A1 behind the pathways by the seven-versus-six applicable-gate count. B's retirement is defensible as a kill of the undeclared lifetime/refill specification; it is not empirical disproof of the biohybrid family, and the preserved lenient dissent remains material. Finally, A–E/G2-music/W2 are recorded INSUFFICIENT despite AppendixA-v1 §4.3's W2 NA language. That inconsistency needs prospective reconciliation, but NA is not PASS and changes no present aggregate result.

**4. Falsifiable errors and limits of the claimed verification.**

**Material evidence-tier error, still present:** `extraction_v1_2026-11-02.csv:72–73,106,199–200` codes five adult-archival histology rows as **T4**. GOAL §5.3 defines T4 as age-matched pediatric human evidence. Kamakura's cached full text explicitly reports 17 specimens from people aged **57–96**, mean age at death 82. The CSV itself calls these adult archival specimens. This is an objective source-population/tier inconsistency, not a matter of reviewer taste. They should retain adult-human descriptive status, with the appropriate transport limitation, rather than pediatric T4 eligibility. Appendix A's own “T4-descriptive” wording does not override GOAL's tier definition. All five rows remain INSUFFICIENT today; the error has not created a winner, but would matter if later grades were upgraded without correcting tiers.

**Citation misattribution, already caught downstream but retained in the historical bibliography:** Step0 bibliography E3a-i says Downie has two errata. The cached `/tmp/fulltext/PMC8385069.xml` identifies PMID **33293699**, DOI **10.1038/s41431-020-00772-y**, as a correction to a Danish psychiatric/immunogenetic paper; its body concerns ICD diagnostic codes. It is not a Downie hearing-loss correction. PMID **33168987** is the genuine Downie correction, but its cached XML has no body. Round1's correction is right. This is a real misattribution, not evidence that the cited article was fabricated; neither I nor the supplied cache can certify the uninspected genuine correction's implications for the diagnosis counts.

**Numerical safety inference withdrawn correctly:** `attack-A1-killtest.md:180` combines a displayed 5–50 nC charge range with k values calculated using µC and concludes they are far below the cited boundary. Its cited Li full text explicitly uses nC. Recalculation gives k = **−2.079…−0.079** under the µC convention and **+0.921…+2.921** under the printed nC convention. The +3 discrepancy is real; the original “far below” argument does not follow from that cited convention. Round2 properly withdraws it and leaves safe charge unresolved. A change of units also requires transformation of a calibrated intercept: the bracket is a report of unresolved source conventions, not two validated physical safety predictions.

**Confirmed arithmetic and local-source checks:** Kamakura Table 2's 17 rows reproduce the reported mean scala-tympani fibrous/new-bone/total percentages **36.15/20.13/56.29**, and whole-cochlea total **36.08** after rounding. The apparent 36.15+20.13 versus 56.29 difference is rounding, not falsification. CDC's supplied marginals give 804 right and 816 left severe/profound SNHL ears, mean **810**, and 810/3,547,774×1,000 = **0.228312**. That mean cannot be the observed both-ears severe/profound child count, whose upper bound from those marginals is 804. The [0,804] bound concerns those observed marginals, not all U.S. P0 children, unknown cases or the ≥70/≥71 boundary. Rejecting 810 as the P0 count was correct. The attack's MAR-adjusted approximately 1,468 is only a conditional illustration, not an identified upper population bound.

I re-extracted selected sections of the cached 16-page Otarmeni PDF: the indication restriction appears in §1; §4 says no contraindications; §14 reports **16/20 (80%)**, with **24 treated** and the bilateral better-treated-ear endpoint footnote. These denominators must remain distinct. MED-EL's cached SSED gives the seven-month expansion; the cached AB SSED states twelve months in its history. Cached FDA/WHO/Seyyedi file sizes and all five MD5 prefixes printed in Round2 match. This confirms local artifact consistency; it is not an independent online provenance check. No fabricated DOI or invented measured effect was established in these spot checks. Step5's blanket “zero fabrications” exceeds what either this sample or an agent-only audit can certify.

**5. The tested scorer is not yet an implementation of all GOAL promotion rules.**

This is the most consequential software finding for an eventual legitimate win. `gate_table.py:175–199` takes the worst verdict across every supplied row with the same candidate and collapsed gate. It does not distinguish outcome gates, mechanism-only chain inputs, study-level evidence, or required versus optional measurements. I executed these small contract probes in memory:

```text
G2 W3 PASS + G2 W0 INSUFFICIENT                       -> G2 INSUFFICIENT
G1 W3 PASS labelled T0 / VeryLow                      -> G1 PASS
Only one G4 W3 PASS supplied, other components absent -> G4 PASS
check_promotion(P, G1=NA and all other gates=PASS)     -> True
```

The first result exposes an extra structural obstacle: GOAL Appendix A says G2 W0–W1 are mechanism-only and **cannot PASS**, while G2's primary outcome is W3. Keeping applicable early rows INSUFFICIENT therefore prevents aggregate G2 from ever passing through this reducer, even with a valid W3 result and an adequately documented chain. Likewise, G3a needs superiority in at least one W2/W3 window plus NI elsewhere, not superiority in every row; this distinction is not represented. Old insufficient study rows also cannot simply be combined by worst-study voting to adjudicate a later evidence body.

The second and third probes expose permissiveness in the other direction: tier/grade are stored but not enforced, and absent required subcomponents/windows are not inferred from a manifest. Only an entirely absent gate is defaulted INSUFFICIENT. Thus the unchanged matrix after adding 48 rows is expected on this all-insufficient record; it does not validate missing-cell handling in a future mixed PASS/INSUFFICIENT record.

The fourth probe isolates the promotion helper from the intentional v1 G3b block. It admits a standalone pathway without checking portfolio membership, device disclosure, stress survival, decision-time eligibility, human verification, or held-out status. The actual v1 pipeline still forces G3b INSUFFICIENT, so it cannot currently promote this synthetic case. Additional concerns are `summarize()` selecting maxima across numeric effects without estimand compatibility, and the stock adapter silently dropping every Gen1 ID. The latter is disclosed and manually worked around; I independently reproduced the filed Gen1 matrix, so no Gen1 omission is alleged here.

These are limitations of a deterministic **verdict tabulator**, not evidence of a current concealed win. Human adjudication supplies much of what it does not check. Before using it to authorize promotion, a new protocol/scorer version needs a declared cell manifest and explicit aggregation rules, with tests for valid wins, missing required cells, prohibited tier/grade promotion and mechanism-only rows. None of the 31 passing tests establishes that broader contract.

**6. Gen2 is presently a poor use of resources, but the summaries invent a stronger prohibition than GOAL contains.**

I agree with **defer Gen2 now**. No child gained fitness, no new combination evidence supports a better portfolio, the A1 test remains unevaluable, and basic human/process prerequisites are still missing. Another renamed set of designs would add little decision value.

However, Round1 §4 and Round2 §4 say Gen2 is justified **only if a verdict or survivor set changes**. GOAL §7 does not impose that necessary condition. It explicitly permits recombination with a stated interface experiment and contemplates non-improving generations. A genuinely new, tractable falsification design could be worthwhile before a categorical verdict changes. Running a properly specified generation with a real new question would not inherently “dishonestly” advance the counter. Rewording existing designs or relabeling gap attacks as generations would.

The formal §7(b) stop condition is still unmet: one observed Gen0→Gen1 non-improvement transition, and several promotion-blocking gaps remain untouched. Two gap rounds are not two generations, nor do two revisions by themselves prove independent attacks. No budget-exhaustion or human non-viability decision is recorded. Therefore neither formal abandonment nor compelled endless agent generation follows. Defer discovery and seek the missing human decisions/data.

Several Round2 §6 assertions also need narrowing before anyone follows W1–W8 as binding instructions:

- “No agent step left” and “only [W6 new primary research] can create a PASS” overstate the evidence. Existing qualifying literature/public data could contribute after human verification and prospective evidence allocation; agents can still assist with retrieval, code repair and extraction. No qualifying missed result was identified here.
- W5 cannot unlock **unbounded absence claims**. Completing more registries makes absence claims better bounded by databases, terms and dates. It also lists C/D/E scorer runs as D15 debt even though Step3 §1 explicitly retired D15 and those candidates are in the reproduced matrix.
- W4 depends partly on W6e data; W6b refers forward to W7's pre-output freeze; W7 follows W6 and refers to changed evidence. A literal linear execution risks reusing seen results as validation. The text also says studies are preregistered, so leakage is not established; the dependency plan needs separate design, lock and unopened-validation milestones.
- Track R is barred **until** the required staging evidence exists under GOAL §4.1, not categorically forever. It still cannot count as a Track-P preservation win. Adult-first staging applies to novel devices/biologics, not automatically to every available-care pathway study.

There is a further unresolved protocol tension: §§4–5 require pediatric comparative outcomes for several promotion gates, while §11 describes the immediate successful output as an animal/adult study-design handoff. Useful early study-design prioritization must be distinguished from evidentiary promotion; otherwise the project demands the results of the downstream program before handing off its upstream design. This review does not waive either requirement. Humans must resolve that scope prospectively under §12, preserving the current no-winner record.

**7. Single highest-leverage next action toward an eventual legitimate win.**

**Commission a funded, independent G3b co-design and measurement project with Deaf-community and parent decision-makers, led by a named measurement/trial expert, to deliver a prospective Appendix A v2 instrument, scoring rule, window-specific MCID and NI margin.** Use the existing Ga/P1 pathway designs to specify the intended population and comparator context. The deliverable must document construct validity, feasibility/pilot evidence, accessible administration, missing-data handling and stakeholder dissent; selecting a convenient questionnaire or merely filling roster slots is insufficient.

This is the most direct tractable action against a universal, explicitly binding Track-P veto. More A1 numerical refinement or design generations cannot remove that veto. Co-design does not earn G3b PASS, supply the other outcomes, or freeze a candidate: subsequent human extraction, coherent aggregation rules, prospective validation and comparative data remain necessary. Ga remains the most relevant existing vehicle for testing C0 once those prerequisites are ready. The immediate legitimate achievement is a usable, stakeholder-authorized measurement specification.
