# Gap-attack skeptic — falsification pass on round-1 gap attacks

> **Requested route:** xhigh skeptic. **Actual runtime model:**
> `muse-wonder-full-1.0`, disclosed per GOAL §9 rule 3.
> **Date:** 2026-11-02. **Scope:** read `research/gaps/` in full
> (4 attack files + `a1_model/` code) and attempt to falsify four
> named corruption modes. Each attack below was re-executed
> independently (fresh PMC XML fetches, fresh CDC PDF extraction,
> fresh CTgov/PubMed API calls, A1 model + tests re-run by me).
> Agent work only; human dual extraction still PENDING. This file
> decides no gate and edits no earlier file.

## Verdict summary

| # | Skeptic attack | Outcome on the gap files |
|---|---|---|
| S1 | Denominator smuggled from wrong severity cut / block / denominator | **UPHELD** (attack file survives; one self-imposed caveat can be retired) |
| S2 | PMC numbers not actually in the XML | **UPHELD** on every spot-check I ran; **DOWNGRADE** only re: derived-vs-printed values and non-exhaustive re-verification |
| S3 | Registry absence overclaimed | **UPHELD** — the file does not overclaim; overclaim risk is downstream quoting, itemised below |
| S4 | A1 model parameters invented-as-cited; seeds/determinism | **Mixed: determinism UPHELD; cited σ/Greenwood UPHELD; Shannon §5 DOWNGRADE→withdraw; numeric width ranges DOWNGRADE (grid-dependent)** |

**Gate consequence (Step 3 PASS bar): zero gate cells may
legitimately change.** Detail in §5.

---

## S1 — Denominator: was 810 taken from the wrong cut, block, or denominator?

**Attempted falsifications:** (a) moderately-severe (56–70 dB) row
folded into the "severe+profound" numerator; (b) first p.3 block is
not Sensorineural (rotated-label inference attack); (c) births
denominator swapped for screened, or vice versa; (d) 810 quietly
used as N_P0 downstream of its own caveat.

**My re-extraction** (2026-11-02, `web_fetch` of the
`archive.cdc.gov` 12_2022 PDF, 297,712 B, `pypdf` 6.21.4 layout
mode, plus a `visitor_text` pass capturing rotated strings with
text-matrix positions):

- p.1 ASHA bands confirmed verbatim: Moderately severe 56–70,
  Severe 71–90, Profound 91+.
- p.3 first block bilateral rows confirmed: Severe 237 R / 259 L,
  Profound 567 R / 557 L, Moderately Severe 293/292. Ear-average
  severe+profound = 248.0 + 562.0 = **810** exactly as filed. Had
  the wrong (≥56) cut been used the number would be 1,102.5; it
  was not. **(a) fails.**
- Rotated labels **do** extract with `visitor_text`: `Sensorineural`
  at y≈575, `Conductive` y≈495, `Mixed` y≈421, `Type Unknown`
  y≈306, `Auditory Neuropathy` y≈225 — aligned top-to-bottom with
  the five blocks in the order the attack assumed. Block identity
  is therefore **directly inspected, not merely arithmetically
  inferred**: the attack's PROVISIONAL-on-label-inference caveat
  can be retired (agent-extraction + human-visual caveats remain).
  Block sums re-verified: SNHL 2,338 R / 2,327 L; Conductive
  ear-avg 288.0; Mixed 324.5; Type-Unknown 418.5 (vs p.6's
  duplicated 150.5 — the internal inconsistency the attack flags
  is real); AN 150.5 once its Unknown-Severity row (118 R / 113 L,
  the residual to the printed 3,518/3,510 totals) is included.
  **(b) fails, in the attack's favour.**
- Denominator: the frozen D1 formula (`verify/epi_arithmetic.py`
  `d1_incidence`, re-read) mandates HSFS screened births; the
  attack uses screened 3,547,774 for the headline rate
  (0.228/1,000) and reports per-birth 0.224 as a secondary. No
  swap. **(c) fails.**
- 810 is never entered as N_P0 in the file: §3.3's Fréchet bound
  (both-ears ≥71 SNHL ∈ [0, 804]; ear-avg 810 > 804 max) checked
  by hand and correct; `d2_n_e_p0` None-propagation respected;
  the forbidden 810 × 1–8% multiplication is shown only to forbid
  it. **(d) fails.**

**S1 verdict: UPHELD.** Residual downgrades, already self-stated
and binding on any quoter: pin P02 is better-ear ≥70 (0.5–4 kHz),
the HSFS cut is ≥71 by-ear — a real 1 dB seam plus an
unresolvable joint-distribution gap; §7's two-layer D1 is a
*proposal for human re-freeze*, not a pin. Any future sentence of
the form "810 U.S. P0 newborns/year" would be a new error, not
this file's claim.

## S2 — Full-text: are the extracted numbers actually in the PMC XML?

**Method:** re-fetched all 12 PMC XMLs fresh via efetch
(3639477, 5018452, 4674315, 7411546, 7611895, 7171096, 11641559,
11053021, 7801236, 4827009, 7136966, 5711943), stripped tags,
searched ~25 load-bearing values with surrounding context.
Fetched byte sizes match the attack's log to the byte
(93,563 / 121,524 / 76,778 / 144,537 / 130,004 / 14,176 / 118,822).

**Found verbatim in XML, sampling the claims most likely to be
hallucinated:**

- Srinivasan: mean improvement 3.01 dB (HINT), 2.71 dB (digits),
  Exp-MP 15.3 vs Exp-TP 12.29 dB, subjects C1…C14. ✓
- Kamakura: Table 2 Average row 36.15 / 20.13 / 56.29 … 36.08;
  R≒0.6230; "present in all seventeen temporal bones." ✓
- Pfingst: "deafened with neomycin and inoculated with AAV.Ntf3
  **prior to implant insertion**" (Fig. caption for Subject 451) —
  the B5 sequence claim is real, and it is the AAV animal, not a
  hearing-control caption (both wordings exist; the attack cites
  the right one). ✓
- Dieter: "15/35 animals (~43%)", "206/528", 0.95/1.93/2.94/3.06
  octaves, "pierced through the basilar membrane", 39 animals /
  4 controls / 12 IC datasets. ✓
- Keppeler: "4.1/6.9/6.9 octaves", "from four rats" caption vs
  5-animal text (discrepancy real, correctly un-resolved),
  ~80% hit rate, Fig. 5 caption "n = stimulation sites…/gerbils"
  with no numerals in XML text (Ns genuinely figure-only). ✓
- Downie PMC7171096: no `<body>`; raw XML contains the comment
  "does not allow downloading of the full text in XML form";
  abstract 106/156, 59/106 present. Blocked-status claim ✓.
- Errata: PMID 33293699 MEDLINE title re-fetched by me =
  "Correction: Immunity and mental illness…" — the PubMed
  mis-link finding is correct; only PMID 33168987 is genuine. ✓
- Pinyon: elink re-run by me returns only `pubmed_pmc_refs`
  (60 links), no `pubmed_pmc` — paywall confirmation ✓.
  Browne 2016 HEK293 / 219.0±37.7 in PMC4827009 ✓.
- Baux PMC5711943: "207 French families" ✓ (P0-attack cross-check).

**S2 verdict: UPHELD** for fabrication purposes — no tested number
was absent from its XML. **Downgrades that stand:** (i) two value
classes are *derived, not printed* — Kamakura per-case ranges
(computed from Table 2 rows) and "17/17" (a paraphrase of "all
seventeen") — both disclosed in-file, both must keep their
"computed from" label when quoted; (ii) my re-verification is a
~25-value spot check, not an exhaustive second extraction — the
un-spot-checked remainder keeps agent-pre-extraction status;
(iii) none of this touches the standing bars (Srinivasan remains
barred as PASS evidence; Dieter/Keppeler remain T2
single-programme rodent rows).

## S3 — Registries/Q0: is absence overclaimed?

**Independent spot replays (2026-11-02):**

- CTgov API `NCT07752888`: single-group, enrollment count 1
  (ACTUAL), ACTIVE_NOT_RECRUITING, `hasResults: false`, official
  title "…Who Have Received Cochlear Implantation" — exactly as
  filed, correctly scored class-(ii)-by-design / no estimand. ✓
- CTgov API `NCT05788536`: secondary IDs EUDRACT 2022-000079-38 +
  CTIS 2024-511342-40-00 present; eligibility exclusion of prior
  CI in treated ear as quoted. ✓
- PubMed esearch for N-Q0-2 re-run with the filed string:
  count **23**, including PMID 25843784 (Sterkers) and 37489512 —
  count and screening set reproduced. ✓

**S3 verdict: UPHELD** — read strictly, the file overclaims no
absence: EU-CTR zeros are labelled EU-CTR-legacy-only, CTIS-UI /
ANZCTR / ChiCTR absences are explicitly *not* claimed, the
101-hit ANI set is page-1-only with no absence drawn, and the
450-hit control is declared unscreened. **The overclaim hazard is
entirely in downstream compression.** Sentences that would become
DOWNGRADE-false if quoted without the file's bounds: "no EU OTOF
trial" (the `OTOF` term alone returns 0 while `otoferlin` returns
the CHORD record — term-sensitivity is the lesson), "no ANI human
trial anywhere," "no post-CI AAV study exists" (NCT07752888
refutes, n=1, no results), "no optical-CI human work" (must read
*optogenetic*; NCT05110183 infrared feasibility exists). Q0
disposition (UNDECIDABLE-no-data, Sterkers 42/45 refused as a
patency %, sensitivities "inapplicable, not failed") is the
correct reading of the frozen §2.1/§2.2 estimands; I could not
falsify it.

## S4 — A1 model: invented-as-cited parameters? seeds/determinism?

**Re-run by me (2026-11-02, this session):**

```text
$ cd research/gaps/a1_model && python3 test_model.py -v
Ran 6 tests in 1.625s — OK (6/6)
$ md5 results.csv            # pre-existing file
30cd31cecc5759e41e9f94f009c0c39a
$ python3 run_sweep.py (×2); md5 after each
30cd31cecc5759e41e9f94f009c0c39a  (identical both times; stdout diff-clean)
```

**Determinism: UPHELD but empty.** `results.csv` reproduces
bit-identically, and all 12 rows match attack §4. But `SEED =
20261102` is decoration: `grep` confirms no RNG anywhere in
`model.py`/`run_sweep.py` — the CG solver is a deterministic
linear solve, so determinism is a property of the arithmetic, not
of any seed discipline. "Seed filed" must carry zero weight as a
pre-registration act; what matters is that code+outputs were
produced in one exploratory session (attack §6 item 6 already
concedes this kills any frozen-kill-test reading).

**Cited parameters: UPHELD where checkable.** Perilymph 1.2 S/m,
bone 0.0334, healthy modiolus effective 0.2734 → fibrous-filled
0.0334 all found verbatim in my fresh PMC11053021 fetch;
Greenwood 165.4 / 2.1 / 0.88 and the 33.46 mm example found in
PMC7801236. The grade→(thickness, σ) map, contact spacing, strip
geometry, contact area, pulse width are all labelled ASSUMED in
both code and attack §3 table — I found no ASSUMED value wearing
a CITED label, with one exception that matters:

**S4a — Shannon units: DOWNGRADE, §5 illustration must be
withdrawn.** Attack §2 (X2) correctly quotes Li 2024 §2.2
(verified in my PMC11641559 fetch): *"charge per phase (unit:
nC ph−1) and charge density per phase (unit: µC cm−2 ph−1), were
used to calculate the k-values"*, with boundary k = 1.5–2.0 and
best 63.9% at k = 1.79. But `model.py` line 32 re-defines
`k = log10(Q[uC/ph]) + log10(D[…])`, `test_shannon_formula`
encodes the µC convention (Q=0.1 µC, D=100 → k=1.0), and
`absolute_charge_check` passes µC. Entering Q in nC adds exactly
+3.00 to k. Under the attack's own cited convention the §5 range
is therefore **k = +0.92 … +2.92, not −2.08 … −0.08** (my
recomputation: 0.2 mA×25 µs = 5 nC → 0.92; 2.0 mA → 50 nC →
2.92), i.e. the upper half *crosses* the 1.5–2.0 boundary before
any tripolar multiplier, and the multiplier adds
2·log₁₀(r) ≈ +0.60 at r = 2 (D scales with Q at fixed area),
not the implied +0.30. I do not assert Li's nC convention is the
historically correct Shannon convention — the 1992 primary was
inspected at abstract level only (no units) — which is precisely
the point: **the unit basis of the filed k values is unverified
against either source, and the two conventions disagree by 3
orders in log space.** Attack §5's "far below the boundary even
after the ≤2× multiplier" sentence is falsified under its cited
source and unproven under the other; it must not be quoted in
either direction. This strengthens, and does not change, the
UNEVALUABLE verdict (safe-charge limit was already formally
UNPINNABLE-input).

**S4b — Grid non-convergence: DOWNGRADE of §4 numeric ranges.**
`PARAMS` promises a convergence sensitivity (`domain_length_mm …
sens: convergence test`) but `run_sweep.py` contains no dx/dy
sensitivity. My probe at dx=dy=0.0625 mm (grade 0, dist 0.5):
mono 1.44 mm (was 1.62), tri 0.94 (was 0.88), **width reduction
34.8% (was 46.2%)**, Q ratio 1.43 (was 1.57), battery 2.72 (was
2.99). The filed "22–47% narrowing at 1.3–2.0× charge" is a
property of the 0.125 mm grid; only the *direction* (tripolar
narrower and costlier) is grid-robust so far. A dx-convergence
series is a round-2 requirement before any number from §4 is
quoted with decimals.

**S4c — Two code/text mismatches, logged not fatal:**
(i) `excitation_width` is described (attack §3) as the
*contiguous* extent ≥50% of peak but implements global
`max(above) − min(above)` span — my bimodal probe profile
`[0,10,0,0,9,0]` returns width 4.0, not the contiguous 1.0.
Benign for the unimodal profiles this model produces, wrong as
documented. (ii) `build_sigma` lays the fibrosis sheath as a
**full-length infinite layer** across all x (verified: sheath row
uniform σ_sheath at every column), not a capsule localised to the
array — so the headline "uniform sheath acts as series resistance
and loudness-balancing rescales it away" is substantially built
into the geometry, beyond what §4/§7's "uniform sheath"
disclosure conveys. The CG solver also returns silently at
`max_iter` with no residual/convergence flag; outputs are smooth
and monotone where expected, so non-convergence is unlikely, but
it is unproven, not checked, by any test.

**S4 verdict:** parameters-not-invented **UPHELD** (σ, Greenwood,
labelled assumptions); determinism **UPHELD but trivial**; §5
Shannon illustration **DOWNGRADE → withdraw pending a units pin
from the Shannon primary**; §4 numbers **DOWNGRADE to
direction-only pending grid-convergence**. Kill verdict
UNEVALUABLE **UPHELD**, with two items added to its missing-input
list: (7) Shannon unit convention pinned from primary text;
(8) dx/dy convergence series filed.

## 5. Which gate cells may legitimately change under the Step 3 PASS bar?

**The bar (as applied in Step 3/Step 5):** PASS requires
≥Moderate GRADE evidence at the Appendix A tier, human dual
extraction (GOAL §9), frozen pins, and — for any promotion —
G3b PASS, which is structurally BLOCKED. Agent pre-extraction,
T0 modelled sub-claims, PROVISIONAL rows, and proposals change
no cell. Against that bar:

| Candidate cell(s) | Would-be mover | Change legitimate? |
|---|---|---|
| **All G6 (coverage)** — INSUFFICIENT / A,B,C,E FAIL per Step 5 §2 | P0 attack's 810 / D1 §7 proposal | **No.** 810 is an ear-averaging convention, P0 cell stays UNPINNABLE; proposal is unfrozen; G6 stays INSUFFICIENT (FAILs, being completeness/staging, are likewise untouched by a denominator) |
| **GEN1-A1 G1, G6** | A1 model §4 narrowing | **No.** T0 modelled, UNEVALUABLE by its own §3 rule, now further downgraded (S4a/S4b); no infant timeline filed, so even the disputed A-G6 completeness FAIL has no new basis to flip |
| **C G1** | Keppeler within-animal 4.1 vs 6.9/6.9 octaves (full-text upgrade) | **No.** Acute T2 rodent, single inventor programme, Fig. 5 Ns figure-only — a provisional signal's paperwork improves, its GRADE does not |
| **Q0-dependent G4** (all candidates) | Registry round 2-in-1, NCT07752888, Kamakura Table 2, Pfingst B5 lift | **No.** Q0-P/Q0-A still cannot be zoned; tissue-% ≠ patency; class-(ii) design with n=1 and no results is not an estimand |
| **B (any)** | Pinyon paywall proof, Browne 2016 | **No.** Paywall proof is an absence-of-access fact; Browne is in-vitro HEK293 and explicitly non-substituting; B's retired status untouched |
| **A G2** | Srinivasan N=6 full-text | **No.** The row was already barred as PASS evidence (degraded comparator, acute, n=5–6); resolving N retires a qualifier, not the bar |

**Changes that ARE legitimate — all bookkeeping, none in the gate
matrix:** (1) delete the phantom Downie "second erratum"
(PMID 33293699) wherever it travels; (2) retire the five
"abstract-level / N UNVERIFIED" qualifiers and the Pfingst B5
sequence downgrade (fulltext §4 items 1–3, 6–7); (3) retire the
CDC rotated-label *inference* caveat per S1 (direct extraction
now on record — human visual check still owed); (4) adopt the
bounded registry sentences (post-CI AAV per NCT07752888;
candidate-C FIH read as *optogenetic*); (5) carry D1's two-layer
form into the next *human* re-freeze as a holder decision;
(6) strike or bracket A1 attack §5's Shannon sentence until the
unit convention is pinned (S4a). Step 5's no-winner decision,
every INSUFFICIENT/FAIL, and Q0-UNDECIDABLE-no-data all stand
unchanged after this skeptic pass.

## 6. What I executed (reproducibility)

Fresh efetch `db=pmc` for the 12 PMCIDs in S2 (sizes + `<body>`
presence + value-with-context greps); elink re-run for
PMID 24760189; MEDLINE re-fetch for PMID 33293699; CTgov API v2
full records NCT07752888 + NCT05788536; PubMed esearch replay of
N-Q0-2 (count 23); CDC 12_2022 PDF via `web_fetch` from
`archive.cdc.gov` + `pypdf` layout and `visitor_text`
re-extraction (pages 1/3/6, block sums, Fréchet arithmetic);
`verify/epi_arithmetic.py` re-read; A1 `test_model.py` 6/6 +
`run_sweep.py` ×2 with md5 `30cd31ce…` before/after; probes:
dx=0.0625 convergence case, bimodal `excitation_width`, sheath-row
uniformity, Shannon k under both unit conventions
(`/tmp/a1_probe.py`, scratch). `git status`: only untracked
`research/gaps/` — no frozen file was touched by any attack or
by me.

*Unresolved after this pass: everything the four attacks list as
unresolved (human dual extraction, G3b, microdata request, CTIS/
ANZCTR/ChiCTR human-browser searches, Downie/Pinyon human reads,
A1's six missing inputs) plus S4's two additions (Shannon units
pin, grid-convergence series). No gap is closed; round-1 attacks
survive falsification with the downgrades itemised above.*
