# Step 0 adversarial skeptic — falsification pass over verify-*.md

> **Route:** GOAL §9 xhigh tier (adversarial skeptic).
> **Actual runtime model:** `muse-wonder-full-1.0` fallback — recorded;
> not the §9 xhigh model.
> **Date of checks:** 2026-11-02.
> **Status:** agent skeptic pass only. This does not replace human-led
> dual extraction; nothing here makes any row gate-deciding.
> **Files read in full:** `verify-epidemiology-q0.md`,
> `verify-devices-biology.md`, `verify-otof-fda.md`,
> `verify-channels-development.md` (plus the four workers' submitted
> result handoff).
> **Spot-check method:** `web_fetch` of NCBI E-utilities PubMed
> abstract/MEDLINE records (12 PMIDs), the live FDA OTARMENI product
> page, the Crossref record for the 2026 oCI DOI, and the
> ClinicalTrials.gov API v2 record for NCT05821959. Every value below
> was compared character-for-character against the fetched record.

## Headline

No fabricated DOI/PMID and no invented N/% was found among the
spot-checked load-bearing rows — every checked identifier resolves to
exactly the paper, journal, and numbers claimed. The real weaknesses
are (1) systematic **abstract-only evidence carrying the unqualified
label VERIFIED**, (2) absence claims ("no human data/trial") labelled
VERIFIED on single bounded registry queries, (3) one date error
(NEJM issue year), (4) one resolved-but-missed 2026 DOI, and (5) an
unreconciled contradiction between two workers on whether the
Otarmeni label PDF was inspectable.

Outcomes: **UPHELD** = challenge failed, claim stands as written ·
**DOWNGRADE** = claim probably right but verdict strength exceeds the
inspected evidence · **REFUTED** = inspected record contradicts the
claim as written.

---

## A. Identifier / N / % spot-checks (falsification attempts)

| # | Challenged claim (file) | My check (2026-11-02) | Outcome |
|---|---|---|---|
| A1 | PMID 37441990 = Friis Danish CI cohort, N=100, SLC26A4 14%, cCMV-DNA 23%, unknown 31%, DOI 10.1016/j.ijporl.2023.111640 (epi §1, §3a) | Fetched PubMed MEDLINE record. Title, journal *Int J Pediatr Otorhinolaryngol* 2023;171:111640, N=100 (54F/46M, 2020–2022), and every cited % match the abstract exactly, including the 13%+1% Pendred split in Conclusions | **UPHELD** |
| A2 | Danish cohort completeness (epi §1) | Same abstract: "Twenty-three… congenital severe to profound bilateral… In the remaining 47 cases, the HL was progressive" — 23+47=70, not 100; the other 30 children are unexplained in the abstract (the 70 = NHS-diagnosed subset, inferable but unstated). Neither worker flagged this internal gap; overlap warning is present but the arithmetic gap is not | **DOWNGRADE** (add gap note; do not quote "remaining 47" against N=100) |
| A3 | April 2026 FDA approval: Apr 23 2026 letter, STN 125874, lunsotogene parvec-cwha (otof 1a; epi 4d) | Fetched live FDA OTARMENI product page (fda.gov): STN 125874 ✓, Proper Name lunsotogene parvec-cwha ✓, "April 23, 2026 Approval Letter" ✓, "April 22, 2026 Summary Basis for Regulatory Action" ✓. The single most fabricable-looking claim in Step 0 is real | **UPHELD** |
| A4 | NEJM DB-OTO: PMID 41085057, DOI 10.1056/NEJMoa2400521, 12 enrolled, 9/12=75% (95%CI 43–95, P=1.1×10⁻¹³), 7.2×10¹² vg/ear (otof 2a–2d) | Fetched PubMed abstract: all numbers exact (12 enrolled; 9/12 both endpoints; 67 AEs; NCT05788536). **But** the journal issue is *N Engl J Med* **2026 Mar 12;394(11):1074–1083**, Epub 2025 Oct 12, ©2025. Worker's "NEJM 2025 first report" uses the epub year without saying so | Numbers **UPHELD**; "NEJM 2025" as issue date **REFUTED** — cite as "epub Oct 2025; issue Mar 2026" |
| A5 | Label efficacy 16/20=80%, ABR 14/20=70%, N=24 treated, wk-48 10/12 (otof 2b–2e) | These live only in the USPI PDF the worker text-extracted; they cannot be cross-checked against NEJM (different cut, A4) or the FDA landing page (no numbers). Worker cross-checked glyph artefacts only against indication *wording*, not numbers. Single-source PDF extraction = one transcription error away from a wrong gate input | **DOWNGRADE** to "label-extracted, single-source; human PDF re-read required" (not refuted — internally consistent: 16/20, 9/20=45%, 3/20=15%, 14/20 arithmetic all correct) |
| A6 | Two workers contradict each other on the same label PDF: epi 4d "fetched as binary and could not be text-inspected… exact locus NOT verified" vs otof 1b quoting exact USPI §1 wording from "text-extracted and inspected" 5-pp PDF | Both dated 2026-11-02. Different hosts (Regeneron `otarmeni_fpi.pdf` vs FDA media) may explain it, but neither file acknowledges the other, and a reader of epi alone would wrongly conclude the prior-CI locus is unknown. FDA page I fetched lists the Package Insert (media 192098) as retrievable | **DOWNGRADE** epi 4d (superseded by otof 1b); files must cross-reference and state which PDF/host each used |
| A7 | Dieter μLED *EMBO Mol Med* 2020: PMID 32596983, 16 μLEDs, adult gerbils, acute (devices 1a) | Fetched PubMed abstract: exact match (2020;12(8):e12387; 16 microscale thin-film LEDs; adult Mongolian gerbils; acute; hearing+deaf) | **UPHELD** |
| A8 | ChReef: PMID 40721511, DOI 10.1038/s41551-025-01461-1, "issue 2026 Feb;10(2):277–292", rodent+NHP auditory, nanojoule thresholds (devices 1d-i) | Fetched PubMed abstract: exact match including the odd 2025-DOI/2026-issue split (Epub 2025 Jul 28). Dual-dating in the worker file is correct, not an error | **UPHELD** |
| A9 | 2026 *EMBO Mol Med* oCI paper "reported DOI 10.1038/s44321-026-00541-2 — UNVERIFIED; DOI esearch returned 3 non-matching PMIDs" (devices 1d-ii) | (i) I reproduced the worker's esearch artifact: unfielded DOI query parses to `"10.1038"[All Fields]` + phrase-not-found — a query-syntax failure, not evidence of absence. (ii) Proper `[AID]` esearch: 0 PubMed hits (not yet indexed — that part is true). (iii) Crossref record for the DOI resolves cleanly: "Multichannel optical cochlear implants enable spectrally distinct auditory activity", *EMBO Molecular Medicine*, published **2026-10-22**, Albrecht/Koert/… (Moser group), abstract: ChReef in SGNs + oCIs of **5–10 green LEDs in gerbils**, ICC thresholds <200 nJ. The paper and DOI are real and match the claimed title/journal. Worker's "AAV-PHP.S" detail appears in neither the Crossref abstract nor any record I inspected | Existence/DOI/title: worker's implied doubt **REFUTED** (paper is verified to Crossref-abstract level). Worker's refusal to cite its numbers: **UPHELD** (still no PubMed/full-text N). "AAV-PHP.S" detail: **DOWNGRADE** — unverified, delete or source it |
| A10 | Friesen 2001 corrected authors + Ns (5 NH / 10 Nucleus-22 / 9 Clarion), plateau 7–8, low performers >4 no gain, NH ≥20 channels (channels 1a) | Fetched PubMed abstract (PMID 11519582): authors Friesen/Shannon/**Baskent/Wang** — no Cruz ✓; every N and channel count verbatim ✓ | **UPHELD** |
| A11 | Sharma 2002 P1: N=104+3, 3.5 y / 7 y wording (channels §5) | Fetched PubMed abstract (PMID 12476090): exact, including "within 6 mo" and graded-to-7 conclusions | **UPHELD** |
| A12 | Kral 2025 nine-months paper identity + "~3 y critical period" co-claim (channels §4) | Fetched PubMed abstract (PMID 40907462): *Hear Res* 2025 Nov;467:109401, Epub Aug 13 2025 ✓; abstract says "well-possible within an early critical period of 3 years" and "We propose…" ✓. But the file's Fig.1 sales-data stat (F(6,68)=0.39, p=0.88; <20% implanted in year 1) and received/accepted dates are not in the abstract — they rest on "journal PDF inspected, pp.1–3 + Summary" of a 14-pp paper, i.e. partial full text | Identity/thesis **UPHELD**; Fig.1 statistics **DOWNGRADE** (partial-PDF extraction, unverified here) |
| A13 | Madgar 2025: 24 studies, 567 patients, 78% (71–85%), I²=79.96%, mean age 9.68 y, PTA 60.48→70.95 (epi 4c) | Fetched PubMed abstract (PMID 40052291): every figure exact | **UPHELD** |
| A14 | Grosse 2008 cCMV: ~14% any SNHL, 3–5% bilateral mod–profound, 15–20% attributable (epi 3a-iii) | Fetched PubMed abstract (PMID 17959414): exact | **UPHELD** |
| A15 | Downie 2020: 106/156 consented, exome 59/106=56% vs GJB2/6-only 22/106=21% (epi 3a-i) | Fetched PubMed abstract (PMID 31827275): exact. (Abstract also carries two errata notices, 2021 — worker did not mention them; errata contents not checked here, human extractor should confirm they don't touch these numbers) | **UPHELD** with errata caveat |
| A16 | Liu "2025" nearest anchor = Liu *Hear Res* 2024, PMID 38103445, ectopic MyVIIa+ cells, no ABR claim (devices 4a) | Fetched PubMed abstract: exact — 2024 Jan;441:108916 (Epub Nov 2023), cells "under the FE… rather than within", "larger N at two months" with no numeric N, no threshold outcome in abstract | **UPHELD** |
| A17 | ANI concept paper: PMID 41131644, *Bioelectron Med* 2025;11:26, "validated in chronic animal studies" as future work, erratum 11:31 (devices 2a) | Fetched PubMed abstract: exact, including erratum DOI 10.1186/s42234-025-00197-2. Supports worker's REFUTED verdict on GOAL's "chronic cat" framing | **UPHELD** |
| A18 | AK-OTOF registry now PHASE3, RECRUITING, est. N=48, last update 2026-09-29 (otof 3a) — most surprising registry claim | Fetched ClinicalTrials.gov API v2 NCT05821959: phases `["PHASE3"]` ✓, RECRUITING ✓, enrollment 48 ESTIMATED ✓, lastUpdatePost 2026-09-29 ✓, sponsor Eli Lilly ✓. Worker is right that "Phase 1/2" descriptions are stale | **UPHELD** |

## B. Verdict-strength challenges (abstract-only / snippet / absence)

| # | Challenged pattern | Evidence from the files themselves | Outcome |
|---|---|---|---|
| B1 | **Abstract-only VERIFIED, system-wide.** Epi: all VERIFIED rows (Danish, Fortnum, Grosse, Seyyedi 27/28, Kamakura 17/17, Hodge, Madgar) rest on PubMed abstracts; PMC full texts "located, not line-inspected". Channels: Friesen, Berg, all four focusing studies, Sharma ×2 — abstracts; file admits journal full texts paywalled (Unresolved #3) yet summary carries VERIFIED/CORRECTED without an "abstract-level" qualifier. Devices: Pinyon findings "VERIFIED at abstract level" (honest), but Dieter/Keppeler/Liu/McGovern rows carry plain CORRECTED/VERIFIED | Workers disclose the method in headers, so this is not concealment — but the verdict vocabulary overpromises vs GOAL §9's full-record standard. Abstracts omit exactly what gates need: per-arm Ns, attrition, definitions (e.g. "hearing preservation" variants in Madgar; channel sets per device in Friesen) | **DOWNGRADE** all abstract-only VERIFIED → "VERIFIED (abstract-level)"; none may pin a frozen-baseline number until full-text human extraction. Numbers themselves: none refuted (Section A) |
| B2 | Kral 2023 sign-language claims rest on "publisher PDF, pp.377–378" — 2 pages of a 377–393 review (channels §3) | Introduction quotes are load-bearing for §8H. Partial-PDF inspection is better than abstract-only but is not the "full text inspected" the header implies for "the two Kral reviews" | **DOWNGRADE** to partial-full-text; human extractor to confirm no qualifying passage later in the review reverses the intro framing |
| B3 | Absence labelled VERIFIED: "no human ANI data" (devices 2d), "no human trial 2014–2026" Pinyon (3c), "no human optogenetic oCI data" (1e) | Each rests on one term-based ClinicalTrials.gov query on one date + absence in inspected abstracts. Workers caveat this in prose ("provisional", "no record found") but the verdict cell says VERIFIED. A single-registry English-term search cannot verify a universal negative (EU CTIS / ChiCTR / ANZCTR unsearched; device trials may register under sponsor/product names) | **DOWNGRADE** verdict wording to "no record found in bounded search (2026-11-02)" everywhere; keep the workers' own caveats as the operative claim |
| B4 | Bibliographic-only rows carrying CORRECTED: Keppeler 2020 (devices 1b — DOI→PMID mapping only, abstract "not separately quoted"); Dieter review e11618 (1c — locator = a Springer chapter reference list); McGovern *PNAS Nexus* (4c-ii — locator = foundation HRP list + located PDF, PMID "not asserted") | These are one step above search snippets, which all four files' methods forbid as evidence. For 1b/1c the claim is purely "this distinct paper exists with this title" — a reference-list/registry hit does support that narrow claim. For 4c-ii, substantive findings ("1-/2-factor insufficient") are quoted from "located abstract text" via a secondary list | 1b/1c: **UPHELD** narrowly (existence claims only). 4c-ii findings: **DOWNGRADE** to pointer-level until PubMed/PMC record is directly inspected |
| B5 | Epi 4b post-CI AAV sequencing claim ("inoculated prior to implant insertion", PMC4674315) rests on "located full-text excerpts" while "abstract-level MEDLINE inspection… was not completed" | The CORRECTED verdict for the whole Q0 animal question leans on a paper the worker states was not inspected to standard, plus a negative search result. Worker correctly withholds its numbers but not its sequencing conclusion | **DOWNGRADE**: sequencing claim = UNVERIFIABLE-pending-inspection; the negative half (no post-CI AAV study located) stands as bounded-search result per B3 |
| B6 | MED-EL 7-month minimum CORRECTED on an SSED fetched via "fda.innolitics mirror" (otof 4b) | Worker flags the re-pull need in-row. A mirror of an FDA PDF is probably faithful, but by the file's own method rule ("inspected authoritative records") a third-party mirror is not authoritative; this correction changes the §3.4 comparator, so the bar matters | **DOWNGRADE** to mirror-verified; treat 7 mo as provisional until re-pulled from accessdata.fda.gov |
| B7 | Future-dated registry fields accepted without comment: NCT05788536 "last update 2026-08-05", SENS-501 "2026-07-08", CHORD completion 2032, NCT05110183 "status verified 2026-05" (otof 2a/3b; devices 1e) | All precede the 2026-11-02 verification date, so none is impossible; A18 confirms this registry's 2026 dates are genuine. No date error found — but note NCT05110183's enrollment N is quoted from a truncated fetch in neither file (worker correctly withholds it) | **UPHELD** (no action; recorded because these were prime fabrication suspects) |
| B8 | Workers' own UNVERIFIABLE rows re-check: CDC EHDI ≥70 dB cut, OTOF fraction, 30–40% additional disabilities, ANI bench pulses, "Qiao 2024", AB labelling, Sensorion discontinuation | Each states what was tried (403s, binary PDFs, reCAPTCHA, timed-out fetch) and refuses snippet numbers. I found no case where a snippet number leaked into a VERIFIED cell. "Liu 2025"/"Qiao 2024" deletion recommendation is correct per A16 and the absence of any matching record | **UPHELD** — the UNVERIFIABLE discipline is the strongest part of all four files |

## C. Net assessment for the holder

1. **Trust the identifiers and headline numbers; discount the verdict
   labels one notch.** 15 of 18 Section-A challenges failed outright
   (UPHELD). No DOI/PMID/N/% fabrication was detected.
2. **Fix before Step 1 pins anything:** (a) NEJM citing year → 2026
   issue (A4); (b) reconcile epi-4d vs otof-1b on the USPI (A6, A5);
   (c) relabel abstract-only and absence VERIFIEDs (B1, B3);
   (d) upgrade the 2026 oCI paper to "exists (Crossref, 2026-10-22);
   numbers still unscored" and drop "AAV-PHP.S" (A9);
   (e) re-pull MED-EL SSED from FDA (B6); (f) note Danish 23+47≠100
   gap (A2) and Downie errata (A15).
3. **Still genuinely missing** (workers and skeptic agree): CDC
   ≥70 dB bilateral table, OTOF fraction with named denominator,
   post-CI patency/AAV evidence, ANI bench/chronic primaries, AB
   label, full-text Ns for the animal/device canon. Human dual
   extraction remains pending on every row.

*Checks performed 2026-11-02 via web_fetch: PubMed E-utilities
records for PMIDs 37441990, 41085057, 32596983, 40721511, 11519582,
40907462, 40052291, 41131644, 17959414, 38103445, 31827275, 12476090;
FDA OTARMENI product page; Crossref 10.1038/s44321-026-00541-2;
ClinicalTrials.gov NCT05821959. Springer full text for the 2026 oCI
DOI was auth-redirected and not inspected — its Crossref abstract is
the record relied on in A9.*
