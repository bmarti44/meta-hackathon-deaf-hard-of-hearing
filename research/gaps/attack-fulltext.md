# Gap attack (round 1) — full-text upgrades via NCBI efetch

> **Requested model:** Sol 6.1. **Actual model:**
> `muse-wonder-full-1.0` (probe 2026-11-02: sol-6.1 route
> rejected / not in catalog). **Date:** 2026-11-02.
> **Scope:** promotion-blocking-gap attack round 1
> (GOAL §7 rule 4), Step 5 §6 item 7 ("full texts owed").
> **Evidence rule:** inspected records only. Every number
> below was read in a full NCBI E-utilities `efetch`
> response (`db=pmc` XML, or `db=pubmed` XML / `elink`
> JSON where stated). Search snippets were never evidence.
> PMC HTML pages were not used. No number was invented;
> where full text still does not state a value, this file
> says so.
>
> **Status:** agent pre-extraction. Human dual extraction
> (GOAL §9) is still PENDING. Nothing here is
> gate-deciding, and nothing here promotes any candidate.

## 1. Method

For each paper Step 0 left at abstract level
(`research/step0/Step0-verified-bibliography.md` §2, §5
items 3, 8, 9, 10), the PMC XML was fetched in full:

`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=<PMCID>`

PMCID resolution for papers Step 0 had not resolved used
`elink.fcgi?dbfrom=pubmed&db=pmc` (linkname
`pubmed_pmc` = the article's own PMC version;
`pubmed_pmc_refs` = citing articles, not used as the
target's full text). PubMed XML (`db=pubmed&rettype=xml`)
was used only for errata linkage and paywall
confirmation. Europe PMC REST `search?...&resultType=core`
was used once, as a second route to confirm open-access
status fields (`isOpenAccess`, `inPMC`,
`fullTextUrlList`) for the two paywall/blocked cases;
no efficacy number comes from it.

Fetched XML sizes are recorded per paper below. A
`<body>` element with section text = full-text upgrade.
Front matter only (no `<body>`) = still blocked, however
the article may be readable in a browser elsewhere.

## 2. Per-paper upgrade table

| # | Paper (Step 0 row) | PMC route tried | Result |
|---|---|---|---|
| 1 | Srinivasan et al. 2013, *Hear Res* 299:29–36, PMID 23467170 (Ch2b) | PMC3639477, 93,563 B, `<body>` present (NIH author manuscript NIHMS451523) | **UPGRADED to full text.** N resolved: 6 subjects (HINT n=5). See §3.1 |
| 2 | Kamakura & Nadol 2016, *Hear Res* 339:132–141, PMID 27371868 (E4a) | PMC5018452, 121,524 B, `<body>` present (NIHMS805471) | **UPGRADED to full text.** Per-case % volumes extracted (Table 2). See §3.2 |
| 3 | Pfingst et al. 2015, *Hear Res* 330:98–105, PMID 26209185 (E4b) | PMC4674315, 76,778 B, `<body>` present (NIHMS711907) | **UPGRADED to full text.** Skeptic B5 sequence downgrade lifted: AAV was pre-implant. See §3.3 |
| 4 | Downie et al. 2020, *Eur J Hum Genet* 28:587–596, PMID 31827275 (E3a-i/ii) | PMC7171096, 14,176 B, **no `<body>`**; XML carries the comment "The publisher of this article does not allow downloading of the full text in XML form" | **STILL BLOCKED via efetch.** Gene-level table not extracted. Abstract numbers unchanged. See §3.4 |
| 5 | Downie errata (skeptic A15: "two 2021 errata") | PMID 33168987 → PMC7868367 (13,195 B, no `<body>`, same publisher block); PMID 33293699 → PMC8385069 (full body, but a different paper) | **PARTLY RESOLVED, partly blocked.** Only one genuine Downie correction exists; its body is not in PMC XML. The "second erratum" is a PubMed mis-link. See §3.5 |
| 6 | Pinyon et al. 2014, *Sci Transl Med* 6:233ra54, PMID 24760189 (D3a/D3b) | `elink`: no `pubmed_pmc` link at all (only `pubmed_pmc_refs`); Europe PMC core: `pmcid=None`, `isOpenAccess=N`, only full-text URL is the subscription DOI | **PAYWALL CONFIRMED.** No PMC/Europe PMC version exists. N/arm and eABR numerics remain unextracted. Related OA follow-up extracted instead (§3.6) — it does not substitute |
| 7 | Dieter et al. 2020, *EMBO Mol Med* 12:e12387, PMID 32596983 (D1a) | `elink` → PMC7411546, 144,537 B, `<body>` present | **UPGRADED to full text.** Animal Ns and spread-of-excitation values extracted. See §3.7 |
| 8 | Keppeler et al. 2020, *Sci Transl Med*, PMID 32718992 (D1b) | `elink` → PMC7611895, 130,004 B, `<body>` present (author manuscript EMS136947) | **UPGRADED to full text** (was title-only in Step 0). Per-experiment Ns extracted; no single total N is stated. See §3.8 |
| 9 | Dieter, Keppeler & Moser 2020 review, *EMBO Mol Med* 12:e11618 (D1c) | Europe PMC core → PMID 32227585, PMC7136966, 247,248 B, `article-type="review-article"` | **UPGRADED as bibliographic record only.** Confirmed review; contains no primary N to extract. See §3.9 |

Score: 5 of 9 rows upgraded to inspected full text
(1, 2, 3, 7, 8), 1 confirmed as non-evidence review (9),
3 still blocked or paywalled (4, 5-body, 6).

## 3. Extractions (section locators are PMC XML section titles)

### 3.1 Srinivasan 2013 (PMC3639477) — N resolved

Step 0 Ch2b carried "N not in abstract (PMC3639477
blocked — do not cite N)". Full text resolves it.

- **N / design** (§2.1 Subjects; Table 1): **6**
  post-lingually deafened adult CI subjects (C1, C3, C7,
  C8, C9, C14), Advanced Bionics CII or HR90K, no
  positioners. Ages 45–78 y (Table 1: 78, 54, 61, 63,
  68, 45). Acute within-subject laboratory comparison:
  experimental monopolar (Exp-MP) vs partial tripolar
  σ=0.75 (Exp-TP), matched electrodes 2–15, 140 µs
  phase, 255 pps/channel, loudness-balanced; clinical
  map tested afterwards as reference (§2.2, §2.3).
  Adaptation was 40 min of audiobook listening only;
  experimenter not blinded (§2.3).
- **HINT sentences in babble** (§3 Results): n=**5**
  (C9 had no open-set recognition at 30 dB SNR on any
  strategy and has no HINT SRT). Mean SRT Exp-MP
  15.3 dB vs Exp-TP 12.29 dB; mean improvement
  **3.01 dB**, individual range 1.86–4.2 dB, all 5
  improved; paired t(4)=6.26, p<0.01; Cohen's d=2.8;
  percentile-t bootstrap CI 1.35–4.73, p<0.05.
- **Digits in babble** (§3): n=**6**. Mean SRT Exp-MP
  3.79 dB vs Exp-TP 1.08 dB; mean improvement
  **2.71 dB**, range −0.05 to 4.98 dB (5/6 improved;
  C14 did not); t(5)=3.86, p<0.05; d=1.6; bootstrap
  CI 0.77–4.67, p<0.05.
- **Vs clinical map** (§3): clinical mean HINT SRT
  10.6 dB — better than Exp-MP (t(4)=3.93, p<0.05),
  not significantly different from Exp-TP (t(4)=2.13,
  p=0.09, n=5). Digits: clinical 1.97 dB, no significant
  difference from either experimental strategy.
- **Predictor test** (§2.4, §3): Clean/Dirty index
  (single-channel focusing proxy) did **not**
  significantly correlate with speech improvement on
  any electrode or average, even without type-I
  correction.
- **What this changes:** the Step 0 "+2.7/+3 dB vs
  degraded comparator" reading is confirmed and now
  quantified at full-text level, including why the
  comparator is degraded (§2.2/§4: 14 vs 16 channels,
  255 vs >2700 pps/e, coil vs t-mic, 1.1 mm basalward
  shift, acute-only). It remains an acute adult
  SRT result in 5–6 subjects. It does not become
  take-home, pediatric, or PASS-grade evidence
  (Step 0/Step 3 barring of this row as PASS evidence
  is unaffected).

### 3.2 Kamakura & Nadol 2016 (PMC5018452) — % volumes extracted

Step 0 E4a left "absolute % volumes in PMC full text
(located, not line-inspected)". Now inspected
(§2.1 Subjects, §3.1–3.4, Tables 1–4).

- **N / design:** **17** human temporal bones (8F/9M,
  age at death 57–96 y, mean 82; 6 Advanced Bionics,
  11 Cochlear Nucleus; implantation duration 33–354
  months, mean 134; no re-implantations). 3-D
  volumetric reconstruction (Amira) of new fibrous
  tissue and new bone as % of scala volume.
- **Universality:** new bone **and** fibrous tissue
  present in **17/17** bones (§3.1). Exceptions are
  compartment-level only: no new bone in scala
  media/vestibuli in Cases 6, 7, 9, 17; no fibrous
  tissue there in Case 7.
- **% volumes (Table 2, mean of 17; ranges computed
  from the 17 per-case rows and checked against the
  table's own Average row):** scala tympani — fibrous
  36.15% (range 9.93–61.54), new bone 20.13%
  (2.69–45.90), total new tissue 56.29% (14.48–95.14).
  Whole cochlea (ST + scala media/vestibuli) — fibrous
  25.45%, new bone 10.63% (1.88–25.13), total 36.08%.
- **Correlations (§3.2, Tables 3–4):** CNC word score
  vs total spiral ganglion cell count R≈0.6230
  (p<0.01); vs % volume new bone (whole cochlea)
  R≈−0.5623 (p<0.05); vs electrode length in scala
  media/vestibuli or spiral ligament R≈−0.6191
  (p<0.01). By compartment, CNC correlated negatively
  **only** with new-bone % (ST −0.5265 p<0.05;
  SM/SV −0.6548 p<0.01), never with fibrous-tissue %.
- **Distribution (§3.4):** fibrous tissue ran the full
  electrode length in almost all cases and beyond the
  tip in most; to the round window in 7/17. New bone
  extended apical to the tip in 8/17 and to the round
  window in 6/17.
- **What this changes / does not:** Q0 still has **no**
  "% scala patent / cannulable for later AAV infusion"
  number. Table 2 measures tissue % of scala volume in
  adult archival bones with older devices, not residual
  lumen available to an infusion cannula, and not in
  infants. The upgrade replaces "presence 17/17" with a
  volume distribution (ST occupied ≈56% on average,
  up to ≈95% in one case) — relevant context for any
  future patency definition, still not a Q0 decider.

### 3.3 Pfingst et al. 2015 (PMC4674315) — B5 downgrade lifted

Step 0 E4b + skeptic B5: the "AAV before implant"
sequence was UNVERIFIABLE-pending-inspection and its
numbers were not to be cited. Full text now inspected
(Methods: Overview; Results; Table 1; Figs. 4–6
captions).

- **N / arms:** **9** adult male pigmented guinea pigs,
  3 per arm: (i) implant into a previously normal
  (hearing) ear, n=3; (ii) neomycin deafening +
  AAV2.Ntf3, n=3 (subjects 451, 455, 448); (iii)
  neomycin + AAV.Empty control, n=3 (449, 454, 457).
- **Sequence (the B5 point):** AAV was a **pre-implant**
  treatment. Locators: Overview — animals "were
  deafened prior to implantation"; ECAP changes were
  followed "in the context of several pre-implant
  treatments"; Table 1 caption — implant "following
  deafening and inoculation"; Fig. 4 caption — ear
  "had been deafened with neomycin and inoculated
  with AAV.Ntf3 **prior to implant insertion**".
  Dose (Overview): AAV2 at 1×10¹² pfu/ml, 5 µl into
  scala tympani via cochleostomy at 1 µl/min;
  neomycin 10 µl of 5% at 5 µl/min. The paper does
  **not** state an interval in days between
  inoculation and implantation, and no animal received
  AAV into an established/fibrosed implant.
- **Effect (Results; Table 1):** ECAP amplitude-growth
  slopes dipped in week 1 (minima ≈Day 5–11) then
  recovered over weeks (plateau ≈Day 41–120) in
  hearing-implanted animals. 2/3 AAV.Ntf3 animals
  (451, 455) showed the same recovery pattern; the
  third (448) did not recover and had very low SGN
  density. 0/3 AAV.Empty animals recovered slope.
  Pattern tracked SGN density near the implant
  (Table 1, cells/mm² in 3 sampled regions): hearing
  479–1015; AAV.Ntf3 34–484 (451 highest: 484/172/154);
  AAV.Empty 30–82. All deafened arms: 0% IHC survival.
  Survival 176–426 days post-implant (one hearing
  animal ongoing, no histology).
- **What this changes:** E4b may now cite the sequence
  and the 3/3/3 design from an inspected record.
  Substantive Q0 conclusion is unchanged and, if
  anything, sharpened: this is AAV **before** implant
  insertion in acutely deafened guinea pigs. It is
  not evidence about AAV delivery after an established
  implant, in either direction.

### 3.4 Downie et al. 2020 (PMC7171096) — still blocked via efetch

- **What efetch returned:** 14,176 B, front matter +
  abstract only, no `<body>`, with the in-XML comment
  "The publisher of this article does not allow
  downloading of the full text in XML form." Europe
  PMC core record agrees: `isOpenAccess=N` (free to
  read in HTML/PDF, not in the downloadable OA XML
  subset). Per this task's PMC-XML-not-HTML rule, the
  gene-level table Step 0 owed (E3a-ii: per-gene
  breakdown incl. any *SLC26A4* count) was **not**
  extracted, and no gene-level number is reported here.
- **What remains citable (unchanged, abstract in the
  same efetch record):** population cohort, bilateral
  moderate–profound HI, births 2016–2017; consented
  **106/156 (68%)**; exome diagnosis **59/106 (56%)**
  vs *GJB2/6*-only **22/106 (21%)**.
- **Human action still owed:** read the publisher/PMC
  HTML or PDF directly (human extractor), extract the
  per-gene table with a table locator, and re-check
  the 59/106 and 22/106 numerators there. Until then
  this row stays abstract-level and cannot pin an
  Appendix D fraction.

### 3.5 Downie errata — one genuine, one PubMed mis-link

PubMed XML for PMID 31827275 lists two `ErratumIn`
entries (the basis of skeptic A15). Inspecting both
targets (`db=pubmed` XML + `db=pmc` XML) shows they
are not both Downie corrections:

- **Genuine:** PMID **33168987**, "Correction: Exome
  sequencing in infants with congenital hearing
  impairment…", *Eur J Hum Genet* 2021;29(2):363,
  DOI 10.1038/s41431-020-00750-4 → PMC7868367.
  Its `ErratumFor` points only to Downie (PMID
  31827275). **But** PMC7868367 efetch (13,195 B) is
  front matter only, same publisher XML block, no
  `<body>`: **what the correction changes is not
  inspectable via PMC XML.** Whether it touches
  59/106 or 22/106 therefore remains UNVERIFIED —
  A15 is narrowed (one document to check, not two)
  but not closed. Human PDF/HTML read still owed.
- **Spurious:** PMID **33293699**, DOI
  10.1038/s41431-020-00772-y → PMC8385069. Its actual
  title (PubMed XML and PMC XML agree) is "Correction:
  Immunity and mental illness: findings from a Danish
  population-based immunogenetic study…" (Nudel et
  al.), and its PMC body corrects ICD-8/ICD-10 code
  lists for that psychiatry paper (correcting DOI
  10.1038/s41431-019-0402-9). The record carries a
  second, erroneous `ErratumFor` link to Downie
  (PMID 31827275), which is what Step 0 picked up.
  **It contains nothing about Downie and must be
  deleted from the project's errata list.** Step 0
  wording "two 2021 errata" should be corrected to
  one wherever it travels (bibliography E3a-i,
  frozen-baseline D2 notes, held-out manifest).

### 3.6 Pinyon 2014 — paywall confirmed; related OA does not substitute

- **Pinyon et al. 2014 (PMID 24760189, DOI
  10.1126/scitranslmed.3008177):** `elink`
  pubmed→pmc returns **no `pubmed_pmc` link** (60
  `pubmed_pmc_refs` citing articles only). Europe PMC
  core independently returns `pmcid=None`,
  `inPMC=N`, `inEPMC=N`, `isOpenAccess=N`, sole
  full-text URL = subscription DOI. Two-route
  conclusion: **no open-access full text exists in
  PMC/Europe PMC; paywall confirmed.** Step 0 D3b
  therefore stays abstract-level: N/arm, eABR
  threshold/dynamic-range numerics, histology
  denominators and follow-up duration remain
  UNEXTRACTED. Human paywalled-full-text extraction
  is the only route; nothing below replaces it.
- **Related OA follow-up (extracted so it is not
  mistaken for Pinyon efficacy data):** Browne,
  Pinyon et al. 2016, "Mapping of bionic array
  electric field focusing in plasmid DNA-based gene
  electrotransfer", *Gene Ther*, PMID 26826485,
  PMC4827009 (118,822 B, full body). This is an
  **in-vitro HEK293 monolayer** parameter study, not
  an animal hearing study (Results: validation n=3
  coverslips/configuration; configuration comparison
  n=4/configuration, ranked ANOVA p<0.001; tandem
  219.0±37.7 GFP+ cells vs no-electroporation control
  0.8±0.8, alternating 81.8±11.3, 1+8 7.0±3.1;
  voltage series n=9/group, 40 V 196.7±18.5 vs 10 V
  5.9±1.1 GFP+ cells; transduction efficiency ≈0.6%
  at 40 V). It confirms the same group's
  close-field mechanism work continued in vitro. It
  provides **no** SGN-regrowth, eABR, durability, or
  tonotopy data and upgrades no Family B gate cell.

### 3.7 Dieter et al. 2020 (PMC7411546) — Ns and spread extracted

Step 0 D1a: "N not in abstract". Full text
(Materials and Methods: Animals; Results) gives the
full animal accounting. Design is **acute,
anaesthetised** (isoflurane) inferior-colliculus
multi-unit recording — no chronic, behavioural, or
human arm.

- **N (Animals; Results: Multi-channel optical
  control):** **39** adult Mongolian gerbils total,
  6–14 months, either sex. Of these, 4 were
  non-injected controls (2 hearing, 2 deafened) and
  **35** were AAV-PHP.B-CatCh intramodiolar-injected
  (2–3 µl, 1.4–2.1×10¹⁰ genome copies; ≥4 weeks
  recovery). Only **15/35 (≈43%)** were oABR-positive;
  ICC datasets were obtained in **12/15** (Animals
  section: 9 hearing + 3 deafened). Subset notes that
  must not be summed with the 12: tonotopic-slope
  fits N=11 hearing (Fig. EV3), deafened electrode
  placements N=5, click-ABR deafening check n=5.
  Attrition 35→15→12 is part of the result, not a
  footnote: any response fraction must carry its
  denominator stage.
- **Device:** 16 individually addressable μLEDs
  (60×60 µm, 462 nm, pitch 100/150/250 µm); single-μLED
  max 0.76±0.21 mW at 10 mA; all-16 max ≈3.15 mW.
  Non-functional emitters: 158/560 μLEDs excluded
  (Fig. 1 caption).
- **Response strength (Results: ICC activation):**
  single μLED at max intensity evoked ICC responses
  (d′≥1 somewhere) for **206/528** μLEDs (≈1/3), mean
  max d′ 1.97±0.71 SD; blocks of 4 neighbours
  **89/132** (≈2/3), d′ 2.86±0.83; all 16, d′
  3.35±0.65; ≈35 mW optical fibre in same animals,
  d′ 4.27±0.52. Hearing vs deafened: no significant
  difference (Wilcoxon p=0.26/0.80/0.43/1 by mode).
  All-16 ICC threshold 0.35±0.25 mW vs fibre
  0.76±0.56 mW (p=0.015). Weak responses to all-16
  stimulation also occurred with 3/7 oCIs in 2
  non-injected hearing controls (attributed to an
  opto-acoustic effect; absent in deafened controls
  and post-sacrifice).
- **Spread of excitation (Results: SGN activation
  with high frequency selectivity)** — measured only
  for **blocks of 4 μLEDs** (single-μLED responses
  too weak/unreliable): at best-electrode d′
  1.5/2/2.5/3, spread was 0.95/1.93/2.94/3.06 octaves
  (100–150 µm pitch; ±SEM 0.75/0.20/0.26/0.23) and
  0.98/1.75/2.26/3.32 octaves (250 µm pitch), no
  pitch difference. Tonotopic shift: 1.75 ICC
  electrodes/mm cochlea (single, r=0.33,
  p=0.00066); 1.67/mm (blocks, r=0.58, p=1.96×10⁻⁷).
  The paper's electrical comparison values in
  Discussion (mono 2.06/4.92/6.91/7.29, bipolar
  0.67/3.90/5.89/6.96 octaves) are **quoted from
  Dieter et al. 2019**, not measured in this study —
  do not re-cite them as 2020 head-to-head data.
- **Harms/limits stated in-paper (Discussion):** in
  both X-ray-imaged implants (2/2 imaged) the oCI
  pierced the basilar membrane (scala tympani →
  vestibuli). Single-emitter selectivity "still
  remains to be elucidated". No chronic opsin
  safety, power-heat in vivo, or behavioural data.

### 3.8 Keppeler et al. 2020 (PMC7611895) — from title-only to full text

Step 0 D1b asserted existence/title only. The PMC
author manuscript (EMS136947) is now inspected in
full. **No single total animal N is stated anywhere
in the XML text**; experiments use three different
preparations and must be cited per-experiment:

- **Preparations (Materials and Methods: Animals):**
  (a) transgenic Thy1-ChR2-Venus rats (acute oABR);
  (b) wildtype rats and gerbils with postnatal-day
  6/7 intracochlear AAV-PHP.B-CatCh, tested as
  adults 5–6 months later (ICC selectivity in
  gerbils; chronic behaviour in rats); (c) naïve
  controls.
- **Acute rat oABR (Results: basic characterization;
  reproducibility):** round-window insertion typically
  placed only **up to 5 of 10 LEDs** inside scala
  tympani. Device-reproducibility series: 5 different
  oCIs sequentially in **1 rat** (Fig. 4A–D).
  Laser-vs-oCI series: text says **5 animals**
  (Fig. 4E–H) while the Fig. 4 caption says p1
  amplitudes in F–H come from **four rats** (E shows
  rats 1–5) — **in-paper N discrepancy, flagged, not
  resolved here**; cite as "4–5 rats (text/caption
  disagree)". OABRs absent with LED in bulla, after
  euthanasia, and in ChR2-negative rats; present
  after kanamycin deafening. In-vivo heating: no
  measurable intracochlear rise in **n=2** naïve rats
  during 6-LED parallel stimulation (1 ms×30 min +
  4 ms×17 min at max power).
- **Spectral selectivity (Results: spectral
  selectivity; Fig. 5):** acute ICC multi-unit
  recordings in CatCh gerbils, oCI vs 4-channel
  clinical-style eCI in the **same animal**
  (sequential implant swap). Animal/site Ns for
  Fig. 5 are given **only inside the figure image**
  (caption: "n = stimulation sites (LEDs or
  electrodes)/gerbils") and are **not present in the
  PMC XML text** — this file does not invent them;
  human extractor to read Fig. 5A–C/G image panels.
  Effect stated in text: at d′=3, mean spread
  optogenetic **4.1** vs monopolar **6.9** vs bipolar
  **6.9 octaves** (optogenetic 1.7-fold more
  selective above d′=2; mono vs bipolar n.s.,
  p=0.57/0.84/0.91/1 at d′ 1.5/2/2.5/3). Unlike
  Dieter 2020, this **is** a within-animal
  optical-vs-electrical comparison — acute and
  anaesthetised, with the figure-only N caveat above.
- **Chronic behaviour (Results: Behavioral
  analysis):** shuttle-box avoidance, AAV rats
  **n=2** + naïve rats **n=2**. CatCh rats hit rate
  ≈80% to wireless-triggered all-LED burst
  stimulation, stable >1 month; controls responded
  to sound, not light; sound-processor on/off
  control behaved as expected. This is the only
  behavioural/chronic element in either 2020 paper
  and it is n=2/arm, detection-level (burst
  presence), not spectral or speech-like testing.
- **Device numbers (Results: in-vitro
  characterization):** 10 LEDs (220×270 µm, pitch
  350 or 500 µm, 457 nm); 1.41±0.05 mW time-averaged
  at 30 mA (10% duty); worst-case simulated rise
  <1 K at ≈100 µm from the oCI. Bench longevity in
  saline >200 days for best encapsulation variant
  (without final silicone coat; Fig. 2I–J).

### 3.9 Dieter/Keppeler/Moser review (PMC7136966) — bibliographic only

efetch confirms `article-type="review-article"`,
PMID 32227585, DOI 10.15252/emmm.201911618 (Step 0
had only a publisher reference-list locator). It is
a narrative review: no animals, no N, no effect to
extract. Step 0's handling ("must not be cited as
experimental μLED evidence") stands, now with a
full-record locator.

## 4. What changes in Step 0–5 bookkeeping (proposed, not applied)

This attack file edits no earlier file (no-overwrite
rule). For the holder/human pass, the defensible
changes are:

1. **Ch2b (Srinivasan):** "N UNVERIFIED" →
   N=6 (HINT n=5, digits n=6), full-text level.
   Verdict substance unchanged (degraded-comparator
   acute result; still barred as PASS evidence).
2. **E4a (Kamakura):** add Table 2 volume
   distribution (§3.2). Q0 patency remains
   UNVERIFIABLE; no patency % may be derived.
3. **E4b (Pfingst):** skeptic B5 downgrade may be
   lifted — sequence (pre-implant AAV) and 3/3/3
   Ns are now inspected-record claims. Q0 verdict
   (UNDECIDABLE-no-data) unchanged.
4. **E3a-i (Downie):** "two 2021 errata" → **one**
   genuine correction (PMID 33168987, contents still
   unchecked) + one deleted PubMed mis-link
   (PMID 33293699). Row stays abstract-level.
5. **D3b (Pinyon):** add "paywall confirmed by
   elink + Europe PMC (2026-11-02); no OA version".
   Row stays abstract-level. Browne 2016
   (PMC4827009) may be logged as related in-vitro
   work, never as Pinyon efficacy.
6. **D1a (Dieter):** add Ns (39 total; 15/35
   oABR+; 12 ICC), 4-μLED-block spread values, and
   the 2/2 basilar-membrane piercing note. Tier
   unchanged (T2 acute gerbil).
7. **D1b (Keppeler):** upgrade from existence-only
   to full-text-extracted (per-experiment Ns in
   §3.8, incl. the Fig. 4 text/caption discrepancy
   and Fig. 5 figure-only Ns). Adds one acute
   within-animal optical-vs-electrical spread
   comparison (4.1 vs 6.9/6.9 octaves at d′=3) and
   one n=2/arm chronic detection-behaviour result.
   Tier unchanged (T2 rodent; inventor-programme
   single source).
8. **Gate impact: none.** Every upgraded row stays
   at its Step 3/4 disposition (INSUFFICIENT /
   provisional signal at best). No cell reaches
   ≥Moderate GRADE, no G3b, human-extraction, or
   pin-freeze blocker is touched, and Step 5's
   no-winner decision is unaffected. The value of
   this round is narrower: five "abstract-level"
   qualifiers can be retired, one phantom erratum
   deleted, and three dead ends (Downie XML, its
   correction XML, Pinyon OA) proven dead so no
   future agent re-tries them by this route.

## 5. Still unresolved after this attack

- Downie per-gene table + genuine correction
  contents — human HTML/PDF read (PMC7171096,
  PMC7868367). Do not re-attempt via efetch XML.
- Pinyon 2014 N/arm, eABR numerics, durability —
  human paywalled access (DOI
  10.1126/scitranslmed.3008177). No OA route exists
  in PMC/Europe PMC as of 2026-11-02.
- Keppeler Fig. 5 animal/site Ns (figure image
  only) and Fig. 4 N=4-vs-5 discrepancy — human
  figure read / author query.
- Everything else in Step 5 §6 (human gates, G3b
  co-design, P0 denominator, Q0 decider *new data*,
  frozen margins, registry completeness) is
  untouched by full-text upgrades and remains open.

*Fetch log (all 2026-11-02): efetch db=pmc IDs
3639477, 5018452, 4674315, 7171096, 7411546,
7611895, 7136966, 4827009, 7868367, 8385069;
efetch db=pubmed IDs 31827275, 33168987, 33293699,
24760189, 32596983, 32718992; elink pubmed→pmc for
24760189, 32596983, 32718992, 31827275, 33168987,
33293699; Europe PMC core search for EXT_ID
24760189 / 31827275 / 33168987 and DOI
10.15252/emmm.201911618 (OA-status fields only).
One transient NCBI rate-limit response was received
and retried; no data come from it. Human dual
extraction: PENDING.*

