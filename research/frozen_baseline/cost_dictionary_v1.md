# Cost dictionary v1 — proposed Step 1 pin (GOAL §6)

> **Status: PROPOSED PIN — NOT FROZEN.** Holder + independent
> co-approver freeze (§3.4/§12) is **PENDING**. Nothing in this
> file is gate-deciding until that freeze and human dual
> extraction (§9) are done. Where this file says PROVISIONAL,
> the number rests on an inspected PubMed abstract only and
> still needs full-text human extraction before it can pin
> `frozen_bilateral_eCI_v1`.
>
> **Worker / model routing (§9 rule 1, substitution disclosed
> per rule 3).** Requested: **Sol 6.1, high** (Step 1 worker).
> Actual runtime model: **`muse-wonder-full-1.0` fallback**
> (Sol 6.1 unavailable in this runtime), same effort tier
> intent. Inspection date: 2026-11-02.
>
> **G3b: BLOCKED.** Per §4.2, G3b scoring is BLOCKED (all cells
> INSUFFICIENT) until a stakeholder co-designed instrument +
> MCID are committed in Step 1. This file does **not** invent
> that instrument or MCID. See §7 for the co-design protocol
> that is still owed. The ex-ante decision rule in §7 is
> likewise **PENDING-STAKEHOLDER elicitation**, not an
> elicited result.
>
> **Evidence rule applied.** Every dollar figure and rate
> below comes from (a) a Step-0-verified row, or (b) a new
> PubMed MEDLINE record inspected in full via NCBI
> E-utilities (`efetch`) on 2026-11-02. Search snippets were
> pointers only and are never cited as evidence. Step 0
> (`research/step0/Step0-verified-bibliography.md`) contains
> **no cost, revision-rate, non-use-rate, or EHDI
> loss-to-follow-up pin** usable here (its E2a CDC EHDI row is
> UNVERIFIABLE at the needed cut; its harm-adjacent rows E4a–E4c
> concern fibrosis/hearing preservation, not costs) — so all
> §6 numbers below are NEW-source, abstract-level, and
> therefore at most PROVISIONAL. No DOI, PMID, N, dollar
> figure, or percentage in this file was invented; complements
> (100% − reported %) are labelled as arithmetic.

## 1. Scope: what §6 requires this dictionary to fix

Per §6 and §3.3, every candidate is costed against
`frozen_bilateral_eCI_v1` (bilateral electrical CI) on:

- **Components:** device; surgery; mapping (programming);
  EI/therapy (incl. education-placement offsets where a source
  reports them); travel; family time; revision/explant;
  non-use (sunk-cost + follow-on consequences).
- **Perspectives (all three reported, never pooled):**
  family (out-of-pocket + time), payer (health-plan /
  programme payments), societal (payer + family + education /
  productivity offsets as defined by each source — definitions
  differ by source and are stated per row, never harmonised
  silently).
- **Horizons:** primary birth–7 years (W0–W3); sensitivity to
  adolescence (growth, revision, battery, late events). Adult
  lifetime figures from cost-utility models are reported only
  as model outputs of their source horizon — they are **not**
  truncated or re-projected to 7 years here, because the
  abstracts do not carry the year-by-year cost streams needed
  to do that without inventing numbers.
- **Dollar year:** reported **as in source** (see §3). No
  common-dollar-year conversion is pinned in v1-proposed:
  the abstracts inspected do not consistently state a price
  year or index, so any inflation adjustment now would be
  invented. §8 states what pins it.
- **Discounting:** **3%/year** base case for costs (and, where
  a source discounts QALYs, as that source did), with **0%
  and 5% sensitivity** required of every Gen 0 costing that
  uses this dictionary (§6). Formula for any future stream:
  present value = Σ cost_t / (1+r)^t, t in years from the
  decision origin, r ∈ {0%, 3%, 5%}. This file pins the
  *rates*; it does not re-discount source totals whose
  internal discounting is already embedded (noted per row).
- **Preclinical combinations:** **burden units only, no
  invented dollars** (§6). See §5.
- **Terminal accounting (mandatory, §6/§4.3):** explants,
  failures, vestibular/meningitis events, deaths, and loss to
  follow-up stay in denominators (treatment-policy estimand).
  A costing that drops non-users or explants from the
  denominator does not conform to this dictionary.

## 2. Inspected new sources (all abstract-level → PROVISIONAL ceiling)

All records below were fetched as full PubMed MEDLINE records
(title, abstract, identifiers) via E-utilities on 2026-11-02.
Journal full texts were not line-inspected; per Step 0 §1
discipline, that caps every pin from them at PROVISIONAL
(human extraction pending).

| ID | Source (inspected record) | Design / N (as in abstract) | What it can / cannot support here |
|---|---|---|---|
| C1 | Cheng et al., *JAMA* 2000. PMID 10938174 | Cost-utility, US academic centre; parents of 78 profoundly deaf children (mean age 7.5 y; mean 1.9 y implant use); surveys Jul 1998–May 2000; costs+benefits discounted 3%/y | Bundled discounted direct-cost total + societal savings incl. education offset. Cannot disaggregate device vs surgery vs mapping; unilateral-era, pre-bilateral-standard cohort |
| C2 | Semenov et al. (CDaCI), *Ear Hear* 2013. PMID 23558665; DOI 10.1097/AUD.0b013e3182772c66 | Prospective longitudinal, 175 children, 6 US centres, recruited Nov 2002–Dec 2004, SNHL onset <1 y, CI <5 y, ≤6 y follow-up; costs stratified preop/operative/postop (stratum dollars not in abstract); societal perspective | Lifetime-model cost/QALY by age-at-implant + net societal savings incl. education. Stratum-level dollars, price year, and complication rates not in abstract → UNPINNABLE from this record alone |
| C3 | O'Neill et al., *Laryngoscope* 2000. PMID 10646733 | UK cost-utility; full purchaser costs incl. complications+maintenance from one large paediatric programme; implantation assumed age 4 y; 12-y / school-years horizon | GBP (+ USD as printed in abstract) bundled totals + education-cost difference. UK payer context — do not transplant as US payer pin; adult utility weights applied to children (authors' conservative assumption, stated) |
| C4 | Bond et al., *Health Technol Assess* 2009. PMID 19799825; DOI 10.3310/hta13440 | Systematic review (33 papers, 2 RCTs) + Markov model; severe-to-profound children+adults; searches to Jul 2007 | Model ICERs (£/QALY) for unilateral and bilateral (simultaneous/sequential) vs comparators. Component costs, price year, and failure/complication transition probabilities are in the full HTA report, not the abstract → UNPINNABLE here |
| H1 | Liu et al., *Ear Hear* 2023. PMID 35973054; DOI 10.1097/AUD.0000000000001266 | Systematic review/meta-analysis (144 articles; 85,851 initial implantations; 4,276 reimplantations) + single-centre series (1,718 initial, 57 reimplantations, 1999–2021) | Pooled reimplantation rates overall / pre-2000 / post-2000 + cause mix. Mixed adult+paediatric pool; no paediatric-only pooled rate or per-centre distribution in abstract |
| H2 | Andresen et al., *Otol Neurotol* 2023. PMID 37254261; DOI 10.1097/MAO.0000000000003910 | Single academic centre retrospective; 3,025 individuals, 3,934 operations, 1985–2022; 276 revisions after primary implant | Overall revision rate + indication mix; paediatric status = risk factor (no paediatric-only rate in abstract). Includes known vendor/field-action failure clusters — era/vendor confounding stated by authors |
| H3 | Contrera et al., *Otol Neurotol* 2014. PMID 24518403; DOI 10.1097/MAO.0000000000000243 | Consecutive case series + survey; ~474 first-CI patients <18 y (1999–2011), follow-up obtained 402 (85%); regular use = ≥8 h/day | Regular-use rates at 5/10 y. "<8 h/day" ≠ complete non-use; complete-non-use rate not in abstract. 15% without follow-up data — non-response bias direction unknown |
| H4 | Subbiah et al. (CDC HSFS), *J Early Hear Detect Interv* 2018. PMID 31745502; DOI 10.26077/6sj1-mw42; PMC6863447 | US EHDI surveillance summary, CDC Hearing Screening & Follow-up Survey 2006–2016, 3-y moving averages | National LTF/D (lost to follow-up/documentation) trends for diagnosis and EI. No CIs, no state distribution, no ≥70 dB bilateral split in abstract; LTF/D mixes true loss + missing paperwork (do not relabel as pure access failure) |
| H5 | Gowrishankar et al., *Otolaryngol Head Neck Surg* 2023. PMID 36864717; DOI 10.1002/ohn.309 | Systematic review/meta-analysis; 116 studies; 112 meningitis cases / 58,940 patients post-CI | Overall post-CI meningitis rate. Mixed ages/eras; subgroup CIs crossing 0% noted by authors (vaccinated, prophylaxis, <5 y implanted, etc.) — infant-specific rate not separately pinned in abstract |
| H6 | Gowrishankar et al., *Otol Neurotol* 2023 (inner-ear malformations). PMID 37317518; DOI 10.1097/MAO.0000000000003913 | Meta-analysis; 38 studies; 10 meningitis cases / 1,300 malformed ears | Malformation-subgroup meningitis rate for S-surgical. Ear-level denominator (cluster by child per §5.2 before any per-child use) |
| H7 | Farinetti et al., *Eur Ann Otorhinolaryngol Head Neck Dis* 2014. PMID 24889283; DOI 10.1016/j.anorl.2013.05.005 | Single-institution retrospective; 403 patients (235 children median 4.5 y, 168 adults), 1993–2013; major = surgical revision/hospital care | Global + major/minor complication rates (mixed adult+child). No CI and no child-only major rate in abstract; 1993-era cases included |
| H8 | Wu et al., *Front Neurol* 2022. PMID 36324374; DOI 10.3389/fneur.2022.996580 | Systematic review/meta-analysis, 20 studies, paediatric pre/post vestibular testing to Jul 2022 | Relative risks of abnormal vestibular tests post-CI (cVEMP/oVEMP/caloric) + BOT-2 difference. **No absolute pre/post percentages in abstract** → absolute vestibular-harm rate UNPINNABLE from this record |
| H9 | Yong et al., *J Otolaryngol Head Neck Surg* 2019. PMID 31118089; DOI 10.1186/s40463-019-0341-z | Systematic review/meta-analysis, 10 articles, children <18 y, pre/post vestibular testing | VEMP RR 1.8 post-op; calorics not similar; HIT/posturography insufficient (authors). Corroborates H8 direction; likewise no absolute-rate pin |

Bounded-search note (2026-11-02): a PubMed query for CI
mapping-visit / family-travel burden in children returned
**0 items** (`"No items found"`). That is a bounded-search
result for that query string, not proof that no such study
exists anywhere; travel/family-time cells are therefore
UNPINNABLE (see §3/§8), not "zero cost".

## 3. Cost dictionary: component × perspective (proposed pins)

**Reading rule.** `PROVISIONAL` = abstract-level number,
human full-text extraction pending; usable for Gen 0
*planning* arithmetic only if the PROVISIONAL label travels
with it, never as a frozen gate input. `UNPINNABLE` = no
inspected source supports a number; the cell must be carried
as a named gap (burden units per §5 where applicable), never
filled by analogy, doubling, or expert guess. Do **not**
derive bilateral costs by doubling unilateral totals, and do
not split bundled totals into components the source did not
itemise — both would invent numbers. `frozen_bilateral_eCI_v1`
is bilateral; C1/C3 are unilateral-era and C2/C4 abstracts do
not state a bilateral component split, so **no bilateral
component-level dollar pin exists in v1-proposed**. That is
the honest state, not an oversight.

| Component | Family | Payer | Societal | Horizon / dollar-year note |
|---|---|---|---|---|
| Device (implant + external processor, incl. replacement/battery where source includes it) | UNPINNABLE — no inspected source itemises family-borne device cost | UNPINNABLE as isolated component — see bundled row below; C2 operative stratum exists in full text, dollars not in abstract | UNPINNABLE as isolated component — see bundled row | Adolescence sensitivity (processor replacement, battery) UNPINNABLE: no inspected source reports replacement cadence/cost |
| Surgery (implantation procedure + anaesthesia + inpatient care) | UNPINNABLE (isolated) | UNPINNABLE (isolated) — bundled only | UNPINNABLE (isolated) — bundled only | Simultaneous vs sequential bilateral surgical-cost difference UNPINNABLE from abstracts (C4 models both; inputs in full report) |
| **Bundled direct cost (device + surgery + early follow-up as each source defines it) — the only dollar totals pinnable now** | UNPINNABLE — C1/C2 report direct/societal totals, not family out-of-pocket | PROVISIONAL (UK only): C3 discounted cost of creating + maintaining a paediatric CI user over first 12 y = **£48,757 ($78,011 as printed)**, full purchaser costs incl. complications+maintenance, implant at age 4 y assumed. US payer bundled total UNPINNABLE (C1/C2 do not report a payer-only split in abstract) | PROVISIONAL: C1 discounted direct costs **$60,228** per child (3% discount, 1998–2000 survey era; price year as reported, not restated). C2 mean lifetime implantation cost **≈$2,000/child/year** over 77.5-y life expectancy, similar across age-at-implant groups (price year not in abstract → UNPINNABLE) | C1/C2/C3 horizons exceed 7 y (lifetime / 12 y). **7-y truncated totals UNPINNABLE** without full-text annual streams. $/QALY model outputs (not costs): C1 $9,029 (TTO) / $7,500 (VAS) / $5,197 (HUI); C2 $14,996 (<18 mo) / $17,849 (18–36 mo) / $19,173 (>36 mo); C4 prelingual-child unilateral ICER £13,413/QALY, simultaneous bilateral £40,410/QALY, sequential bilateral £54,098/QALY (bilateral utility assumed same adults/children — authors' assumption). C3 discounted £10,341/QALY ($16,545.60 as printed) |
| Mapping / programming (visits × unit cost) | UNPINNABLE ($ and visit count) | UNPINNABLE | UNPINNABLE | Burden-unit placeholder only (§5): visits/year by window to be pinned from frozen-baseline schedule + full-text/registry extraction (§8) |
| EI / therapy + education offsets | UNPINNABLE — family-borne EI cost/time not reported in inspected abstracts | UNPINNABLE as EI line item (education-sector costs sit outside health payer in C1–C3 framing; do not reassign silently) | PROVISIONAL (offsets/savings only, each source's own definition): C1 incl. indirect (reduced educational) costs → **net savings $53,198/child**. C2 incl. lifetime educational savings → net societal savings **$31,252 (<18 mo) / $10,217 (18–36 mo) / $6,680 (>36 mo)**; mainstream-classroom rate at 6 y 81% / 57% / 63% respectively. C3 discounted education-cost difference (profound >95 dB vs severe 70–95 dB, 12 y) **£26,781 ($42,850 as printed)**; net cost over school years 4–16 y **£21,976 ($35,162)**. Gross EI/therapy spend (before offsets) UNPINNABLE | EI dose (hrs/week) is a §3.2 context variable + §5 burden unit; dollarising it needs a named fee schedule/claims source (§8). Modality (signed/spoken/bimodal) cost differences UNPINNABLE — no inspected source stratifies cost by modality; do not assume spoken-only EI (§3.4) |
| Travel (distance, transport, lodging to CI centre) | UNPINNABLE | UNPINNABLE (reimbursement policy varies; no inspected source) | UNPINNABLE | Report miles/visits as burden units (§5/G6). Zero-hit bounded search §2 |
| Family time (caregiver time off work, supervision, device management) | UNPINNABLE ($ and hours) | — (not a payer cost; report as family/societal only) | UNPINNABLE — productivity offsets in C1/C2 conclusions explicitly exclude or do not itemise caregiver time in abstract (C2: "even without considering improvements in lifetime earnings" refers to the child's earnings, not caregiver time) | Hours/week burden unit owed (§5); wage-rate dollarisation requires a pre-committed valuation rule + stakeholder input (§8) — do not apply an ad-hoc wage |
| Revision / explant (incl. reimplantation) | UNPINNABLE ($) | Rate PROVISIONAL (§4/§6), $ per revision UNPINNABLE — no inspected source costs a revision episode | Rate PROVISIONAL, $ UNPINNABLE (incl. education/time knock-ons) | Expected-cost form once $ exists: P(revision by horizon) × cost/revision, discounted at event time. Until then, carry revisions as **counts per 100 children** (§5), never dollars |
| Non-use (device placed, <regular use; incl. explant-without-reimplant where applicable) | UNPINNABLE ($) | Sunk bundled cost already counted above — **accounting rule: non-use does not refund device/surgery cost**; incremental $ (re-mapping attempts, explant, alternative pathway) UNPINNABLE | Same accounting rule; forgone-benefit handling belongs in gate scoring (G2/G3 treatment-policy), not as a negative cost. $ UNPINNABLE | Rates PROVISIONAL (§6, H3). Complete non-use (0 h/day) vs <8 h/day distinction must be preserved |

**Dollar-year pin (proposed).** v1-proposed carries each
figure in its **source currency and source price basis**
(C1: USD, 1998–2000 era, 3% discounted; C2: USD, price year
not stated in abstract; C3: GBP with USD equivalents as
printed in the abstract, UK ~2000; C4: GBP, HTA model to
2007 searches). A single common dollar year (e.g. 2026 USD)
is **UNPINNABLE** in this file: it requires (i) full-text
price-year extraction per source, (ii) a pre-committed index
(medical-care CPI vs general CPI vs PCE-health give
different answers), and (iii) a currency-conversion rule for
GBP sources. §8 lists the exact fill path. Any Gen 0 table
that restates these figures in a common year before that
work is done is non-conforming.

## 4. Harm / event base rates that feed costing (proposed pins)

Rates are per implanted child unless stated per ear/implant;
unit-of-analysis corrections (§5.2: child, ears clustered)
are owed at full-text extraction where a source is ear-level.

| Event | Base rate (PROVISIONAL, abstract-level) | Range in inspected record | Costing use now |
|---|---|---|---|
| Reimplantation (H1 definition: new electrodes after failure/abandonment of initial implant) | Pooled 1989–2021 **4.7%**; post-2000 **3.2%** (preferred base-case era for contemporary arrays, still mixed adult+child) | 95% CI 4.2–5.1% (overall); 2.7–3.7% (post-2000); pre-2000 6.8% (4.5–9.2%). Cause mix: device failure 67.6% (64.0–71.3%), medical 28.9% (25.7–32.0%) | Counts/100 children by horizon once time-to-event split exists (not in abstract → 7-y vs adolescence split UNPINNABLE). $ UNPINNABLE (§3) |
| Revision surgery after primary implant (H2, broader than H1 reimplantation) | **7.6%** over up to 37 y follow-up, single centre 1985–2022 | 95% CI 6.8–8.5%; hard/soft failure 73% of revisions; paediatric status ↑ risk (magnitude not in abstract) | Sensitivity bound for S-revision (§6). Do not average H1+H2 — different definitions/eras |
| Regular use ≥8 h/day (H3) | **93.2%** at 5 y; **87.7%** at 10 y post-implant (mean use 12.0 h/day, SD 4.1) | 95% CI 90.0–95.4% (5 y); 82.9–91.3% (10 y). Discontinuation hazard +18.2%/y of age at implant (7.2–30.4%) | Complement (<8 h/day) feeds S-nonuse (§6). Reasons <8 h/day: poor benefit 53.2%, social pressure 21.3%, coil displacement 17.0% (authors' survey) |
| Post-CI meningitis, overall (H5) | **0.07%** (112/58,940) | 95% CI 0.03–0.10%, I²=55% | S-surgical (§6). Infant (<12 mo) specific rate UNPINNABLE from abstract |
| Post-CI meningitis, inner-ear malformation subgroup (H6) | **0.12%** (10/1,300 malformed ears); 6/10 with intra-op CSF leak | 95% CI 0.006–0.380%, I²=0% | S-surgical malformation stratum (§6) |
| Any post-op complication; major (revision/hospital care) (H7) | Global **19.9%** (80/403); major **5.0%** (20/403); minor 14.9% (60/403) | No CI in abstract; adults higher than children overall (P=0.004); child-only major rate not in abstract | S-surgical point input only; upper bound UNPINNABLE (§6) |
| Vestibular dysfunction post-CI, children (H8/H9) | Absolute % UNPINNABLE. Relative: abnormal cVEMP **RR 2.20** (1.87–2.58), oVEMP **RR 2.10** (1.50–2.94), caloric **RR 1.62** (1.20–2.19) (H8, 20 studies); VEMP **RR 1.8** (1.57–2.02), I²=91.86 (H9, 10 studies). vHIT NS (H8); BOT-2 mean diff −7.26 (−10.82, −3.70) vs normal group (H8) | As stated; high heterogeneity (H9 VEMP I²≈92%) — do not over-read precision | Burden/harm counts UNPINNABLE until absolute pre/post risks extracted from full texts. RR must never be reported as "% of children harmed" |
| Surgical/medical complications by age at implant <18 mo vs older (C2) | UNPINNABLE rates — abstract states only "not significantly different among the three age groups" | — | Anaesthesia <12 mo harm rate UNPINNABLE (§6). "NS difference" ≠ zero risk and ≠ equivalence |
| Facial-nerve injury; CSF leak/gusher (non-malformation); explant without reimplant; death | UNPINNABLE — no inspected record above reports a pinnable paediatric rate for these Appendix C rows in its abstract | — | Each carried as named UNPINNABLE in §6 with fill path (§8). Absence here ≠ 0% |

## 5. Burden units for preclinical / combination candidates (no dollars)

Per §6, challengers without a marketed price or claims
history (all Track R, and any preclinical Track P combo)
report **only** the units below, per child, by window
(W0–W3 + adolescence sensitivity), treatment-policy
denominator. Dollarising any of these in Gen 0/1 scoring is
forbidden until §8 pins unit costs.

- Surgeries (count, incl. revisions/explants/rescue CI);
  anaesthesia exposures <12 mo (count).
- Mapping/programming visits per year; EI/therapy hours per
  week (by modality received, §3.4 mix — never assumed
  spoken-only); other clinic visits per year.
- Travel miles + trips per year to implant centre
  (distance-to-centre is also a G6 equity stratifier, §3.2).
- Caregiver hours per week (device management, therapy
  carryover, travel/waiting) — hours only.
- Device wear-time hours/day (datalogging where available;
  H3 ≥8 h/day threshold is the frozen-baseline comparator
  definition, PROVISIONAL).
- Harm counts per 100 children: revisions, explants,
  meningitis, major complications, vestibular events
  (absolute definition owed), non-regular use (<8 h/day)
  and complete non-use (separately, once definable).
- Time-to-first-access (months from decision origin) and
  delay-to-standard-CI under any sequencing/bridge design
  (false-reassurance harm, Appendix C) — in months, with
  rescue criteria stated (§10).

Frozen-baseline burden counts (visits/year, EI hrs/week for
`frozen_bilateral_eCI_v1`) are themselves **UNPINNABLE from
the abstracts inspected here** and must be pinned jointly
with the frozen-baseline table (mapping schedule + EI dose
ranges, §3.4) before any disparity-vs-frozen G6 judgement.
This file does not invent them.

## 6. Stress scenarios (§6: per harm, 90th pct / upper 95% CI — no ×2/×4)

**Rule restated.** Primary scenario = base rates (§4).
Each stress re-scores gates with that harm at its **90th
percentile / upper 95% CI bound** from published ranges.
Promotion must survive *each* stress. Where no inspected
record reports a CI or a cross-centre distribution, the
true 90th percentile is **UNPINNABLE**; the file then gives
the closest honest PROVISIONAL proxy (upper CI of a pooled
estimate, or worst inspected era) and labels the gap.
A pooled-estimate upper CI is **not** a 90th percentile of
centres/children and must not be relabelled as one.

| Scenario | Primary (base) input | Stress input (proposed) | Status + caveat |
|---|---|---|---|
| **S-revision** (device failure / reimplantation high) | H1 post-2000 pooled reimplantation **3.2%** | **3.7%** (upper 95% CI, post-2000). Era/vendor sensitivity (report alongside, do not substitute silently): H1 pre-2000 upper **9.2%**; H2 overall revision upper **8.5%** (includes field-action clusters) | PROVISIONAL. True 90th percentile across contemporary paediatric centres/manufacturers UNPINNABLE (no distribution in abstracts; H1/H2 mixed adult+child; H1 time horizon varies by study). Paediatric-only, manufacturer-specific, 7-y-cumulative rates owed (§8). $ impact UNPINNABLE — re-score as counts + G5, not dollars |
| **S-nonuse** (non-use / low wear-time high) | H3 <8 h/day (arithmetic complement): **6.8%** at 5 y (100−93.2); **12.3%** at 10 y (100−87.7) | Upper-bound complements: **10.0%** at 5 y (100−90.0, lower 95% CI of regular use); **17.1%** at 10 y (100−82.9) | PROVISIONAL for <8 h/day only. **Complete non-use (0 h/day) base+stress UNPINNABLE** (not in abstract). Adolescence (>10 y) wear-time UNPINNABLE from H3 abstract. Age-at-implant gradient (+18.2%/y hazard) must be applied by stratum, not pooled, at full-text stage |
| **S-access** (EHDI LTF + travel/insurance failure high) | H4 LTF/D latest-era (to 2016, 3-y moving avg): diagnosis **31.3%**; EI enrolment **20.3%**. Timeliness context (same source): diagnosed <3 mo 36.6%, EI <6 mo 47.2% (latest era) — do not confuse "ever received" with "on time" | Era-max proxy: diagnosis LTF/D **42.1%**, EI LTF/D **39.4%** (2006-era ends of H4 trends) | PROVISIONAL proxy only. **90th percentile UNPINNABLE**: H4 abstract gives no CI and no state/jurisdiction distribution; LTF/D includes loss-to-*documentation* (care received, paperwork missing) so stress overstates pure access failure by an unknown amount. Travel-distance / insurance-denial / rurality failure rates UNPINNABLE (no inspected source). P0 (≥70 dB bilateral) specific LTF UNPINNABLE (cf. Step 0 E2a) |
| **S-surgical** (major complication high, incl. malformation subgroup) — meningitis | H5 overall **0.07%**; H6 malformation ears **0.12%** | Upper 95% CI: overall **0.10%**; malformation **0.380%** | PROVISIONAL. Per-child (vs per-ear H6) conversion owed. Vaccination/prophylaxis-era stratification owed — H5 subgroups with CIs crossing 0% must not be read as proven zero risk |
| **S-surgical** — major complications (composite) | H7 major **5.0%** (20/403, mixed adult+child, 1993–2013) | **UNPINNABLE** (no CI, no child-only split in abstract) | Carry base as PROVISIONAL point; stress cell = INSUFFICIENT until a paediatric registry/cohort with CI is extracted (§8). Do not borrow H2 revision upper bound as a "major complication" stress — different event set |
| **S-surgical** — facial nerve, CSF leak/gusher, anaesthesia <12 mo, vestibular loss (absolute), death | UNPINNABLE (each; §4) | UNPINNABLE (each) | Every Appendix C harm without a rate stays a named gap. Gen 0 candidates must still file FMEA severity/probability-band rows (Appendix C bands) with source tier stated; a band asserted without a source is INSUFFICIENT, not a stress pass |

**Re-scoring instruction.** Under each stress, G5 (per-harm
NI vs frozen, Appendix A margins — themselves Step 1 pins)
and any cost/burden comparison are recomputed with **only**
that harm moved to its stress input; other inputs stay at
base. Joint worst-case (all harms stressed at once) may be
reported as an extra sensitivity but never replaces the
four per-harm tests (§6 forbids the uniform-multiplier
shortcut this replaces).

## 7. Ex-ante decision rule + G3b status (both pending stakeholders)

**Decision rule as stated in §6 (form pinned, thresholds
not elicited).** Added revision (or other G5 harm) risk of a
challenger vs frozen is acceptable **only if** both hold at
primary *and* stress scenarios, in decision-time analysis:

1. **G2 gain:** SRT-in-noise improvement meets the Appendix
   A PASS threshold (≥3 dB vs frozen at W3, with quiet NI
   −5 pp; §4.2/Appendix A) — threshold itself to be confirmed
   at Step 1 freeze; and
2. **G3b NI:** communication-autonomy / family-QoL is
   non-inferior to frozen within the stakeholder-defined
   MCID/NI margin.

If either fails, the added risk is not accepted regardless
of modelled channel counts (G1) or cost offsets. Cost
savings never override a G4 veto (Track P) or a G5 NI
failure. **Status: PENDING-STAKEHOLDER elicitation.** The
acceptable trade-off (how much added revision/surgical risk
per dB of SRT gain, if any) has **not** been elicited from
families/clinicians/Deaf-community stakeholders; no number
for it is pinned here, and Gen 0 scoring must report the
trade-off frontier (harm counts vs G2 gain) without applying
an assumed exchange rate.

**G3b remains BLOCKED (§4.2).** No instrument, MCID, or NI
margin for communication autonomy is named in this file,
because §4.2/§9 require co-design with Deaf-community and
parent stakeholders. Inventing one from the cost literature
above (none of C1–C4 measures communication autonomy; their
utilities are parent-proxy TTO/VAS/HUI or adult-derived —
a different construct, and allegiance/validity concerns for
G3b use) would violate that requirement.

**Co-design protocol still owed (Step 1, before any G3b
scoring).** Minimum contents, to be committed as a versioned
protocol with named stakeholder participants (§9):

1. Stakeholder panel composition: Deaf adults (incl. CI
   users and non-users), parents of deaf children across
   modality choices (signed/spoken/bimodal), paediatric
   otology/audiology, EI providers (incl. signed-language
   EI), trialist/biostatistician; conflict disclosures;
   holder does not sole-decide (§12 COI rule applies by
   analogy — co-approval recorded).
2. Construct definition: what "communication autonomy"
   means independent of modality (child's ability to
   communicate wants/needs/ideas with family/peers, family
   communication ease, participation) vs adjacent constructs
   (generic QoL, spoken-language proficiency) it must not
   collapse into. Candidate existing instruments reviewed
   against that definition; adaptation vs de-novo decision
   recorded with reasons. No instrument is pre-selected here.
3. Validation commitments: content validity with the panel,
   measurement invariance across modality/language groups
   (or explicit non-pooling, mirroring G3a §4.2), floor/
   ceiling check (>20% at bound triggers Appendix A
   alternative), respondent (parent-proxy vs child
   self-report by window).
4. MCID + NI margin: anchor-based (global-change anchors
   defined by panel) triangulated with distribution-based
   estimates; pre-committed before seeing Gen 0 scores;
   superiority claimable only at/above MCID (§4.2).
5. Trade-off elicitation for the §6 decision rule:
   pre-registered method (e.g. threshold/discrete-choice
   design — method chosen and justified in the protocol,
   not here), harm attributes stated in §5 burden units
   (revisions/100, surgeries, visits) as well as plain
   language, heterogeneity by stakeholder group reported
   (no single pooled exchange rate imposed if groups
   disagree; dissent preserved per §9 judging rule).
6. Freeze point: instrument + MCID + decision-rule
   thresholds committed with the Appendix A table *before*
   challenger scoring (§11 Step 1→2 order). Until then every
   G3b cell and every "acceptable risk" judgement reads
   INSUFFICIENT/BLOCKED.

## 8. What would pin each UNPINNABLE cell (fill paths, no new numbers)

Ordered by what blocks a frozen v1. Human dual extraction
(§9, extractor independent of holder + sampled error audit)
applies to every item; agent pre-extraction below does not
substitute for it.

1. **Component dollars (device / surgery / mapping) +
   bilateral split + 7-y truncation + common dollar year.**
   Full-text extraction of C2 (preop/operative/postop strata,
   price year, discounting, bilateral share — CDaCI era) and
   C4 full HTA report (Markov cost inputs, failure/
   complication transitions, price year, simultaneous vs
   sequential bilateral costs); C1 full text (direct-cost
   build-up, price year). Then: holder+co-approver pre-commit
   (a) price index + target dollar year, (b) GBP→USD rule
   (spot vs PPP, dated), (c) whether UK (C3/C4) figures are
   sensitivity-only for a US-default P0 (§3.1 jurisdiction
   pin interacts — resolve jointly). Contemporary US
   claims/registry costing (named database, code list,
   bilateral simultaneous/sequential flags) would supersede
   1998–2007-era totals if licensed/accessible — access gap
   disclosed if not (§9 Embase-style rule).
2. **Revision-episode unit cost + paediatric-only,
   time-varying revision hazard.** H1/H2 full texts
   (paediatric subgroups, manufacturer splits, Kaplan–Meier
   by years-since-implant for 7-y vs adolescence cumulative
   incidence, explant-without-reimplant rates); a costed
   revision episode from claims or a published micro-costing
   (device replacement terms/warranty stated — who pays is a
   perspective question, not an assumption). Centre-level
   distribution (for a true 90th percentile) requires a
   multi-centre registry extract — name registry + request
   in protocol; until then §6 proxies stand labelled.
3. **Complete non-use + adolescent wear-time.** H3 full
   text (0 h/day vs <8 h/day split, datalogging vs report,
   bilateral second-ear non-use, non-responder analysis);
   longitudinal datalogging cohort to adolescence with
   additional-disabilities / modality strata (§3.2).
4. **S-access 90th percentile + travel/insurance.** CDC
   HSFS state-level tables (human PDF extraction — cf.
   Step 0 E2a blocker) for jurisdiction distribution +
   P0-severity split if available; LTF vs LTD separated.
   Travel/insurance: pre-registered search (PubMed + grey
   per §9) with frozen strings beyond the single zero-hit
   query in §2, plus G6 primary burden survey design if
   literature stays empty (miles, trips, denials, wait
   times by rurality/home language — §3.2 stratifiers).
5. **S-surgical per-harm paediatric rates with CIs.**
   Registry/cohort extraction for: facial-nerve injury
   (transient vs permanent), CSF leak/gusher by anatomy
   (EVA/IP/common-cavity strata), anaesthesia events <12 mo
   (with contemporary anaesthetic protocol stated),
   vestibular absolute pre/post risks (H8/H9 full texts:
   per-test absolute abnormal % pre/post, symptomatic vs
   test-only, bilateral sequential risk), meningitis by
   vaccination/prophylaxis era + age <12 mo, deaths
   (any-cause in denominators per §6). Malformation-specific
   surgical risks must not be pooled into normal-anatomy
   rates (Appendix C).
6. **Family perspective (out-of-pocket, travel $, time).**
   Family-cost survey/claims linkage with pre-committed
   time-valuation rule from §7 panel (whose wage, if any;
   report hours alongside any $ so the valuation is
   auditable/reversible). Insurance-type stratification
   required — a single "family cost" averaged over coverage
   types would hide the G6 equity signal.
7. **Mapping/EI schedules (burden denominators).** Pin with
   `frozen_bilateral_eCI_v1` table: mapping visits/year by
   window, EI hrs/week range + modality mix actually
   received (§3.4), hearing-aid-trial duration — from named
   guideline/cohort/registry sources at full-text level.
   EI unit costs only from a named fee schedule; signed-
   language EI availability costed as access (G6), not
   assumed free/available.
8. **G3b + decision-rule thresholds.** §7 protocol executed
   and frozen. No literature extraction substitutes for it.

**Freeze checklist for v1 (all must hold).** (i) Human dual
extraction signed off for C1–C4/H1–H9 numbers actually used;
(ii) dollar-year/index/currency rules committed; (iii)
7-y + adolescence streams derived from extracted annual data
(with `verify/`-locked arithmetic, cf. Appendix D rule);
(iv) §7 co-design frozen or G3b explicitly carried BLOCKED
into Gen 0 (either is honest; silently scoring G3b is not);
(v) holder + independent co-approver signatures (§12).
Until then this file's status line stays PROPOSED.

## 9. Claims table (agent contract, §9)

| Claim | Source | Tier* | Gate / use | Effect + N |
|---|---|---|---|---|
| Discounted direct cost $60,228; net societal savings $53,198 incl. education offset | C1 PMID 10938174 | T4 (paediatric human, cost-utility survey) | §6 bundled societal (PROVISIONAL) | N=78 parents/children; 3% discount |
| Lifetime cost ≈$2,000/child/y; net savings $31,252/$10,217/$6,680 by implant-age group | C2 PMID 23558665, DOI 10.1097/AUD.0b013e3182772c66 | T4 | §6 bundled societal (PROVISIONAL) | N=175, 6 US centres; 77.5-y horizon |
| 12-y purchaser cost £48,757; education diff. £26,781 | C3 PMID 10646733 | T4 (programme costs + model) | §6 payer-UK sensitivity (PROVISIONAL) | Implant age 4 y assumed; programme N not in abstract |
| Bilateral ICERs £40,410 (simult.) / £54,098 (seq.) per QALY | C4 PMID 19799825, DOI 10.3310/hta13440 | Model (inputs mixed tiers) | §6 bilateral model output only (PROVISIONAL) | 33-paper review; Markov model |
| Reimplantation 3.2% post-2000 (2.7–3.7%) | H1 PMID 35973054, DOI 10.1097/AUD.0000000000001266 | T4 (meta-analysis, mixed ages) | G5 / S-revision base+stress (PROVISIONAL) | 85,851 initial; 4,276 reimplants (all eras) |
| Revision 7.6% (6.8–8.5%) | H2 PMID 37254261, DOI 10.1097/MAO.0000000000003910 | T4 (single-centre) | S-revision sensitivity (PROVISIONAL) | 3,025 people; 3,934 ops; 276 revisions |
| Regular use 93.2% (5 y) / 87.7% (10 y) | H3 PMID 24518403, DOI 10.1097/MAO.0000000000000243 | T4 | S-nonuse (PROVISIONAL, <8 h/day def.) | 402/474 with follow-up |
| LTF/D diagnosis 42.1%→31.3%; EI 39.4%→20.3% (2006–2016) | H4 PMID 31745502, DOI 10.26077/6sj1-mw42 | Surveillance (US HSFS) | G6 / S-access (PROVISIONAL proxy) | National survey; Ns not in abstract |
| Meningitis 0.07% (0.03–0.10%); malformation 0.12% (0.006–0.380%) | H5 PMID 36864717 DOI 10.1002/ohn.309; H6 PMID 37317518 DOI 10.1097/MAO.0000000000003913 | T4 (meta-analyses) | G5 / S-surgical (PROVISIONAL) | 112/58,940; 10/1,300 ears |
| Major complications 5.0% (20/403) | H7 PMID 24889283, DOI 10.1016/j.anorl.2013.05.005 | T4 (single-centre, mixed ages) | S-surgical base point (PROVISIONAL); stress UNPINNABLE | 235 children + 168 adults |
| Vestibular abnormal-test RRs 1.6–2.2 post-CI (children); absolute % unknown | H8 PMID 36324374 DOI 10.3389/fneur.2022.996580; H9 PMID 31118089 DOI 10.1186/s40463-019-0341-z | T4 (meta-analyses) | G5 harm present; rate UNPINNABLE | 20 + 10 studies |

\* Tier per §5.3 applied to the *cost/harm* claim (human
paediatric data = T4 where the cohort is paediatric;
mixed-age pools flagged in §2/§4 downgrade applicability to
P0 infants — GRADE/RoB scoring (§5.2) is Step 2/3 work with
human extractors, not asserted here).

*End of proposed pin. No Gen 0 candidate may cite a dollar
figure from this file without its PROVISIONAL/UNPINNABLE
label, perspective, horizon, and source price basis.*


