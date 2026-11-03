# Round-2 skeptic — independent re-checks and gate adjudication

> **Requested:** Sol 6.1, xhigh (skeptic tier, GOAL §9).
> **Actual:** `muse-wonder-full-1.0`, disclosed per
> GOAL §9 rule 3. **Date:** 2026-11-02.
> **Inputs read in full:** the three round-2 files
> (`round2-pdf-labels.md`, `round2-A1-fix.md`,
> `round2-cells-stress.md` + `round2-unrowed-cells.csv`),
> `searched-family-log.md` §§2.1–2.7, GOAL §§5.2/5.3/9/11/12
> + Appendix A. **Method:** nothing below rests on a
> round-2 child's say-so — the PDF claim, the A1 numbers,
> and the cell count were each re-derived by an
> independent route in this session (fresh downloads,
> a copied model tree, a from-scratch recount script,
> and a `gate_table.py` run). Scratch work in
> `/tmp/skep2/` (not deliverables). No earlier file was
> edited by this skeptic; `git status` shows only the
> round-2 children's own `a1_model/` v2 edits and the
> four untracked round-2 deliverables.

## 0. Verdict

**No gate cell is legitimately changeable under the
Step 3 bar. Zero cells change — upheld.** All three
round-2 files survive independent re-check on every
load-bearing number I re-derived. The closest call
(Q0-L, §4.1) still fails the bar. Round 2 retires
qualifiers and invisibility, exactly as filed; it
moves no PASS, no FAIL, no promotion, and the Step 5
no-winner decision is untouched.

## 1. PDF claim re-extracted by this skeptic (2 of 5 items)

Fresh `web_fetch` from the authoritative hosts this
session, extracted with `pypdf` 6.21.4
(`PYTHONPATH=/tmp/pylibs`); prior `/tmp` extractions
were not used.

**Otarmeni USPI** (`fda.gov/media/192098`): saved
1,610,337 B, **MD5 `512657d02b98e4723d12d445818de732`**
(matches the filed prefix), 16 pp. I confirm verbatim:
§1 (p.2) "…preserved outer hair cell function, and
**no prior cochlear implant in the same ear**"; **§4
CONTRAINDICATIONS "None."** (p.8) — the indication-vs-
contraindication correction is right; Table 2 (p.14)
**16 (80%), 95% CI 56%, 94%** and **14 (70%), 46%, 88%**
at N=20, footnote (a) better-ear, (b) one imputed
non-responder; Week 48 text **10/12 (83%)** with the
12/20 subset stated on the same page. Every load-bearing
string in `round2-pdf-labels.md` §3 checks out.

**Advanced Bionics SSED** (`accessdata.fda.gov/…
P960058S167B.pdf`): 672,091 B, **MD5
`790d0b93ee4b85ea0049d466bb9ac4d3`**, 50 pp. §I "Date of
FDA Notice of Approval: **July 22, 2026**"; §II bilateral
"**Children 12 months through 17 years** … Profound,
bilateral sensorineural deafness (**≥90 dB HL**)"
(pp.1–2); the AHL/SSD pediatric floor is separately
"**5 years through 17 years**" (pp.2–3). The filed
resolution of O4c (12 mo bilateral; do not import the
5-year SSD floor) is correct.

Not re-extracted by me (named gap, not silently
endorsed): MED-EL S134 byte-identity, WHO Table 1.3,
Seyyedi XML. The two PDFs I did re-pull match to the
byte (MD5), which raises — but does not prove —
confidence in the other three; human dual extraction
remains the owed check for all five.

## 2. A1 v2 re-run by this skeptic (tests + sweep + convergence)

Copied `a1_model/` to `/tmp/skep2/a1` and re-ran
everything (Python 3.14.8, stdlib only):

- `python3 test_model.py -v` → **Ran 10 tests, OK**
  (1.6 s), including the bimodal contiguous-vs-global
  and Shannon bracket tests. My own probe:
  `excitation_width([0,10,0,0,9,0],1,0.5)` → contiguous
  **1.0**, global **4.0**; `shannon_k_bracket(0.1,100)`
  → **(1.0, 4.0)** — the +3.00 offset is real in code,
  and the r-multiplier arithmetic (k + 2·log₁₀r; §2.5
  table at r=2) recomputes exactly.
- `python3 run_sweep.py` → `results_v2.csv` MD5
  **`b9ec23c5…`**, byte-identical to the filed file;
  v1 `results.csv` still **`30cd31ce…`** (untouched).
  I independently compared v1 vs v2 on all 9 shared
  columns × 12 rows: **max |Δ| = 0 exactly**.
- `python3 run_convergence.py` → 15 rows in 2 m 58 s.
  Excluding `wall_seconds`, **every physics column is
  string-identical to the filed `convergence.csv`**
  (0 diffs). Derived claims re-checked from the CSV:
  contiguous = global in all 27 produced rows
  (12 sweep + 15 convergence); all 54 solves converged,
  residuals 7.1e-10–9.9e-10 < 1e-9; tripolar < monopolar
  in all 15 case-grids; last-step width-reduction moves
  −2.9 / +4.3 / −0.6 / −0.8 / **+8.35 pp** (filed "+8.4"
  is the correctly rounded exact value; grade-3 series
  36.36 → 34.78 → 43.14 is non-monotone); sheathed-case
  Q still drifting (+0.040, +0.049).

So the filed assessment stands as written: **direction
only; magnitudes not grid-converged; Shannon bracketed
(+3.00), primary unpinned; verdict UNEVALUABLE.** Two
skeptic flags, neither new evidence: (i) "direction
grid-robust" is scoped to the 15 case-grids actually
run — the grade-3/0.25 mm zero-reduction artefact case
was not refined, so no direction claim covers it;
(ii) the contiguous-width choice can in principle hide
a separated side lobe, and is safe here only because
the global span is co-reported and equal on every
profile produced so far — that equality must keep
being printed, not assumed.

## 3. Unrowed-cell arithmetic re-counted from scratch

I rebuilt the expected set directly from
`searched-family-log.md` §§2.1–2.6 (fresh script
`/tmp/skep2/recount.py`, not the round-2 generator)
and parsed both CSVs. Every number in
`round2-cells-stress.md` §1.2 reproduces:

| Step | Filed | Mine |
|---|---|---|
| Level-1 cells | 162 | **162** |
| …as (candidate,gate,window) triples | 158 | **158** |
| v1 data rows / distinct triples | 199 / 123 | **199 / 123** |
| v1 triples at non-Level-1 addresses | 11 | **11** (same 11, listed in my run) |
| Covered / missing triples | 112 / 46 | **112 / 46** |
| + H G3a modality cells inside present triples | 2 | **2** |
| **Unrowed** | **48** | **48** |

The +2 is legitimate, not padding: v1 H G3a W2 rows are
signed×2 + bimodal (no **spoken**); W3 rows are
pooled-as-reported + signed + spoken (no **bimodal**) —
my stratum printout confirms both. The 46 missing
triples from my recount are set-identical to the
filed list; the CSV's 48 rows are exactly those 46
plus the 2 modality cells; distribution C12 D12 E11
H4 A3 B3 F2 G1 and gate split (G2 13, G3a 9, …) all
match; all 48 rows parse at 14 columns with
`verdict_proposed=INSUFFICIENT`. PMID-presence counts
behind §3.2 also reproduce (23467170×1, 27371868×3,
32596983×3, **26209185×0, 32718992×0**, 28776202×1,
24760189×7) — the Pfingst-2015/Keppeler exclusions are
correct. The stress count also checks: 17 C/D/E rows +
10 F/G/H table rows ungrouping to 19 reads = **36**,
36/36 UNPINNABLE for a named missing input each.

Decisive end-to-end check the round-2 file asserted
but did not run: I ran the real pipeline
(`adapt_extraction.py` → `gate_table.py`) on v1 alone
(185 adapted rows) and on v1 + the 48 rows (233).
**The two gate matrices are byte-identical**, and the
v1 run **reproduces the filed `gate-matrix-gen0.md`
exactly** (0 PASS; FAIL at A-G6, B-G6, C-G4, C-G6,
D-G4, E-G5, E-G6; G3b BLOCKED everywhere). "Joining
changes no gate cell" is now observed, not argued.

## 4. Adjudication under the Step 3 bar

The bar (GOAL §5.2, binding GRADE→score map; §5.3
tiers; §9; §12): PASS needs **≥Moderate GRADE *and*
the Appendix A minimum tier**, inventor-lab single
source starts one GRADE lower and G1 needs
non-inventor replication; **agent-only verification
is banned for gate-deciding claims** (human dual
extraction pending on everything round 2 touched);
gates are **never amended retroactively within a
frozen generation**. Every plausible change candidate,
tested:

| Candidate change | Why it fails the bar |
|---|---|
| Q0-L / G×G4 on the verified USPI §1 fact (**closest call**) | The label fact is now agent-verified twice (§1 above), but Q0-L sits INSUFFICIENT in frozen v1 and can only move via a human-frozen extraction_v2; it is a RECORD label fact, never gate evidence — G's G4 still needs a patency % that no source supplies. Bookkeeping, not a cell change. |
| Frozen comparator on MED-EL 7 mo / AB 12 mo | Label minima are baseline pins, not gate cells; re-freeze is a holder + co-approval decision (§12), and would still change no v1 matrix cell retroactively. |
| Any A1/GEN1-A1 G1 or G6 cell | T0 model (§5.3: mechanism only, never a pass); magnitudes not grid-converged (§2); named array, charge limit, safety divisor, battery floor, geometry, freeze all still missing. UNEVALUABLE upheld. |
| C–H G5/G6 via the filled stress template | 0 flips are *determinable*: no candidate rate, no U13/U17 margin, proxies PROVISIONAL/abstract-level. A FAIL-direction move would need a ≥major harm signal at ≥Moderate GRADE — no such signal was extracted. "Unchanged" means "already INSUFFICIENT/structural FAIL", never "stress survived" (language scan: the phrase appears only in negations). |
| extraction_v2 U1–U6 (Srinivasan, Kamakura, Dieter) | U1 is T3 adults, n=5–6, degraded experimental comparator → at most provisional, G2 PASS needs T4. U2/U3 add a tissue-% distribution, not the patency estimand → Q0-P stays INSUFFICIENT. U4/U5 are single-lab T2 rodent (allegiance downgrade, no non-inventor replication, no head-to-head vs named frozen array) → GRADE ceiling unchanged. Adoption is a human re-freeze act in any case. |
| G4 cells via the extracted Seyyedi rubric | The rubric is verbal anchors only — it *removes* a hoped-for input. Numeric G4 NI was already impossible at v1 (U17). Nothing to change. |
| Any cell via WHO grade bands | Adult epidemiology descriptors; the table itself forbids using them as intervention determinants. U02 paperwork only. |
| The 48 new rows themselves | `UNVERIFIABLE`/`UNASSESSED` placeholders asserting no effect and no N — INSUFFICIENT by construction; §3's matrix identity proves they move nothing. |

Residual disagreements with the round-2 files: **none
material.** Two wording cautions for synthesis: quote
D14 as **48 unrowed, now rowed-as-INSUFFICIENT** (not
~42, and Level-2's ≈527 reads remain mostly unrowed —
Level-1 completeness must never be quoted as family
completeness); and quote A1 widths only with their dx,
per the filed quoting rule.

## 5. Reproduce (this skeptic's runs, 2026-11-02)

```
cp -R research/gaps/a1_model /tmp/skep2/a1
cd /tmp/skep2/a1 && python3 test_model.py -v   # 10 OK
python3 run_sweep.py                            # md5 b9ec23c5…
python3 run_convergence.py                      # 15 rows, physics-identical
python3 /tmp/skep2/recount.py                   # 162→158→46+2=48
cd research/scoring
python3 adapt_extraction.py ../gen00/scoring/extraction_v1_2026-11-02.csv /tmp/skep2/adapted_v1_mine.csv
python3 gate_table.py /tmp/skep2/adapted_v1_mine.csv --out /tmp/skep2/matrix_v1.md   # == filed matrix
# v1+48-row join -> adapted_joined.csv -> matrix_joined.md  # == matrix_v1.md
```

*Unresolved after this skeptic pass: human dual
extraction of every round-2 number (the §9 gate no
agent file can satisfy); MED-EL/WHO/Seyyedi bodies not
independently re-pulled by me; Shannon 1992 primary
unit basis (licensed read owed); A1 §6 items 1–8;
U13/U17 margins, U09/U16 baselines, D1–D4 denominators
without which the stress template returns UNPINNABLE
by construction; the human decisions queued in
`round2-cells-stress.md` §1.3/§5 and
`round2-pdf-labels.md` §8. Adjudication: **zero gate
cells changeable; no PASS, no promotion, no-winner
stands.***
