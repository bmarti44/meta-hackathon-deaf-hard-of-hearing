# Appendix A v1 — Gate operationalization (PROPOSED pin, Step 1)

> **Status: PROPOSED PIN — NOT FROZEN.** Holder + independent
> co-approver freeze (GOAL §3.4, §12) is **PENDING**. Human dual
> extraction (§9) is **PENDING**. Stakeholder co-design of G3b
> instrument + MCID and stakeholder elicitation of fitness order
> (§7) and MCIDs are **PENDING-STAKEHOLDER**. Nothing in this file
> is gate-deciding until those steps are done. This file proposes
> pins only where inspected evidence supports them; everything
> else is **PROVISIONAL (human extraction pending)** or
> **UNPINNABLE** + what would pin it.
>
> **Date:** 2026-11-02. **GOAL:** v2.2 (§3–§6, Appendices A/D read
> in full). **Step 0 source:** `research/step0/Step0-verified-bibliography.md`
> (read in full; rows cited as E/O/D/Ch + number). Companion:
> `frozen_bilateral_eCI_v1.md` (P0, D1–D4, frozen contents).
>
> **Model routing (GOAL §9):** Step 1 worker requested
> **Sol 6.1, high**; actual runtime model
> **`muse-wonder-full-1.0` fallback** (Sol 6.1 unavailable in
> this runtime) at the same effort split. Substitution disclosed
> per §9 rule 3. No claim in this file is Sol 6.1 work.
>
> **Evidence rule applied:** pins come ONLY from Step-0-verified
> rows or NEW sources inspected in this Step 1 pass via
> `web_fetch` of PubMed E-utilities MEDLINE full-abstract records
> (listed as N1–N8 below). Search snippets were never used as
> evidence. Abstract-level evidence pins as PROVISIONAL. Missing
> evidence is UNPINNABLE + what would pin it. No number, DOI,
> PMID, or NCT in this file was invented. GOAL defaults carried
> forward as *stated conventions* are labelled as such — they are
> not re-described as literature findings.

## New sources inspected in this pass (2026-11-02, MEDLINE abstracts)

| ID | Source | What it pins / fails to pin |
|---|---|---|
| N1 | Henry, Turner & Behrens 2005, *JASA* 118(2):1111–21, PMID 16158665, DOI 10.1121/1.1944567 | Ripple task defined (0.13–11.31 rip/oct adaptive); ~4 rip/oct needed for accurate vowel/consonant in quiet; poorer than ~1–2 rip/oct = highly degraded. No ripple→channels conversion stated |
| N2 | Jeon et al. 2015, *JASA* 138(4):2350–8, PMID 26520316, DOI 10.1121/1.4932020 | Recent CI recipients better ripple resolution than 15–20-y-ago recipients; ≈ hearing-impaired acoustic listeners. Era/array drift matters for any ripple baseline |
| N3 | Ehlers et al. 2017, *JASA* 141(6):4264, PMID 28618809, DOI 10.1121/1.4983824, PMC5464955 | 16 BiCI children 9–17 y, synchronized research processors, 100 pps: all sensitive to ILD; congenitally deaf weak/absent ITD sensitivity; prior acoustic exposure → ITD sensitivity. Clinical processors do not reliably deliver binaural cues (abstract framing) |
| N4 | Seyyedi & Nadol 2014, PMID 25122600, DOI 10.1097/MAO.0000000000000540 (= Step 0 E4a) | **Named fibrosis scale: 0–3 severity** (eosinophil/lymphocyte, giant-cell, new bone, fibrosis) at three 1-mm segments (cochleostomy, mid, tip−1 mm); granulomatous reaction 27/28; basal > distal |
| N5 | Nimmons et al. 2008, *Otol Neurotol* 29(2):149–55, PMID 18309572, DOI 10.1097/mao.0b013e31812f7244; Kang et al. 2009 UW-CAMP, PMID 19474735 | CAMP: pitch-direction discrimination (adaptive threshold) + 12-melody ID + 8-timbre ID; adults, N=8 in 2008; <45 min. Pediatric validity NOT established by inspected abstracts |
| N6 | Holder, Sheffield & Gifford 2016, *Otol Neurotol* 37(2):e50–5, PMID 26756155, DOI 10.1097/MAO.0000000000000907 | NH children 5–12 y (N=41): BabyBio 86% at −5 dB → 99.3% at +10 dB SNR; BKB-SIN mean SNR-50 1.6 dB; QuickSIN 6.6 dB. Norms are NH, not CI — test *choice* evidence, not frozen CI values |
| N7 | Caselli, Lieberman & Pyers 2020, *Behav Res Methods* 52(5):2071–84, PMID 32180180, DOI 10.3758/s13428-020-01376-6 | ASL-CDI 2.0: normed (120 deaf children of deaf parents, 9–73 mo), receptive+expressive vocab + Gestures/Phrases. Norm population ≠ P0 hearing-parent population — applicability caveat |
| N8 | Kamakura & Nadol 2016, PMID 27371868 (= Step 0 E4a, re-fetched) | Fibrous tissue + new bone 17/17; new-bone % volume negatively correlated with CNC. Volumetric complement to N4 ordinal scale |

Failed/limited inspections are in §9. Step 0 rows relied on:
Ch1a (Friesen plateau), Ch1b (Berg 16>8), Ch2a/b (focusing),
E4a–E4c (histopathology, preservation 78%), O4a–O4d (age labels).

## Contents

1. Decisions on GOAL defaults (confirm / amend / delete)
2. Master gate table (normative once frozen)
3. G1 — functional resolution (+ ripple conversion verdict)
4. G2 — functional hearing (SRT per age, music, localization)
5. G3a — language (per-modality instruments, bimodal hierarchy)
6. G3b — BLOCKED + co-design protocol owed
7. G4 / G5 / G6
8. PENDING-STAKEHOLDER register
9. Inspection log + what would pin every UNPINNABLE cell

Windows: **W0** 0–9 mo, **W1** 9–24 mo, **W2** 2–3.5 y,
**W3** 3.5–7 y (§3.3). Tiers T0–T4 per §5.3. Scoring states
PASS / FAIL / INSUFFICIENT per §4.2; INSUFFICIENT never passes.

## 1. Decisions on GOAL defaults

| # | GOAL default | Decision | One-line reason (detail in §§3–7) |
|---|---|---|---|
| D-G1a | Point anchor 8 effective channels | **KEEP as stated convention**, re-labelled | Step 0 Ch1a: Friesen plateau is 7–8 on 2001 arrays; Ch1b (Berg): modern perimodiolar 16 > 8. "8" cannot be defended as *the* contemporary frozen value — keep it only as an explicit, versioned convention with sensitivities |
| D-G1b | Sensitivities 4 and 10 (GOAL §4.2) | **AMEND to 4 / 10 / 16** | 16 is the Berg-relevant stress: if frozen already delivers ~16 usable channels/maxima on the anchor task, Track P PASS (≥12) is trivial and Track R (≥16) is at parity — that must be visible, not hidden |
| D-G1c | PASS ≥12 (P) / ≥16 (R) = 1.5× / 2× point | **KEEP numbers, CHANGE meaning** | Keep as multiples of the *convention* 8 for continuity; add binding rule: PASS must also exceed the *measured* frozen-array value on the same task/array class (see §3.2). A ratio to a convention alone never passes |
| D-G1d | Ripple→channels conversion model "published Step 1" | **UNPINNABLE — do not publish a conversion** | N1/N2 give ripple thresholds (rip/oct), not a validated map to "effective channels". Inventing `channels = f(rip/oct)` would fabricate the G1 ruler. Dual-report instead (§3.3) |
| D-G1e | Timing NI +20% ITD error | **DELETE** | N3: congenitally deaf BiCI children show weak/absent ITD sensitivity even on synchronized research processors; clinical processors do not reliably deliver ITD. A +20% margin on a near-absent, processor-dependent baseline is arithmetically meaningless. Replace with descriptive reporting + localization (§3.4) |
| D-G2a | PASS ≥3 dB SRT (W3); quiet NI −5 pp | **KEEP as provisional conventions** | No inspected source validates 3 dB as MCID in P0 children; retain as pre-registered deltas, flagged PENDING-STAKEHOLDER for MCID confirmation. Tests now named per age (§4); frozen absolute SRT remains UNPINNABLE (companion file §4) |
| D-G2b | Music ≥10 pp; localization ≥10° | **KEEP deltas as conventions; music instrument PROVISIONAL** | UW-CAMP named (N5) but adult-validated only in inspected abstracts → W3 music cells capped at provisional signal until pediatric validation is inspected (§4.3) |
| D-G3a | ≥0.4 SD within stratum; NI −0.2 SD | **KEEP as provisional conventions** | Instruments fixed per modality (§5); SDs must come from each instrument's own norming SD — never pooled. MCID status PENDING-STAKEHOLDER |
| D-G3b | BLOCKED until co-design | **KEEP BLOCKED** | §4.2 is explicit. No instrument/MCID invented here. Co-design protocol specified in §6 |
| D-G4 | Fibrosis "0–4 scale named Step 1" | **CORRECT to Seyyedi & Nadol 0–3** | The inspected Nadol-lab scale is 0–3 (N4), not 0–4. GOAL's "0–4" must be corrected at freeze; rescaling 0–3→0–4 by arithmetic is forbidden (§7.1) |
| D-G5 | Per-harm NI margins "from registry ranges" | **UNPINNABLE per harm (table in §7.2)** | No registry harm-rate range was inspected to standard in Step 0 or this pass. Margins cannot be derived from unpinned base rates. Structure pinned; numbers blank |
| D-G6 | Disparity "within Appendix A bound" | **Propose bound as convention, PENDING-STAKEHOLDER** | §7.3: challenger burden/equity gaps must not exceed frozen gaps by stated absolute/relative caps. The caps are value choices, not literature findings |

## 2. Master gate table (proposed v1)

Frozen ref = value under `frozen_bilateral_eCI_v1` once pinned.
"UNPINNABLE" in that column means the *cell cannot PASS* at v1
(it can only read INSUFFICIENT) — challengers report deltas
against concurrently measured frozen-device/cohort data instead,
with the UNPINNABLE flag travelling with the score.

| Gate–window | Measure / instrument (unit) | Frozen ref | PASS delta | NI margin | Min tier | NA rules |
|---|---|---|---|---|---|---|
| G1-spectral W1–W3* | (a) Spectral-ripple discrimination threshold (rip/oct), Henry paradigm N1; (b) effective channels on channel-count task (count), Friesen/Berg paradigm; (c) spread of excitation (mm and octaves). All three reported; none converted into another | (a) UNPINNABLE point (era/array-dependent, N1/N2); (b) convention **8**, sensitivities **4/10/16** | Devices A/B (P): **≥12**; Track R: **≥16** on (b) *and* ripple (a) better than frozen array measured head-to-head; STRETCH = 16 (P) — see §3.2 | — (superiority gate) | T2/T3 + proxy chain (§5.3); non-inventor replication to PASS (§5.2) | F/G/H: **NA pre-declared**. Infants cannot do ripple tasks: W1–W3 cells are adult/animal-proxy scores, discounted; never a direct infant G1 PASS |
| G1-temporal W1–W3* | Rate/envelope/TFS proxy as pre-specified per candidate (units named in App. B); ITD/ILD JND (µs / dB) on synchronized processors where claimed | UNPINNABLE | No numeric PASS in v1: candidate must not degrade its own pre-specified temporal metric vs frozen device head-to-head (FAIL if degraded; INSUFFICIENT if unmeasured) | ~~+20% ITD~~ **DELETED** (D-G1e); replacement margin UNPINNABLE | T2/T3 | NA if candidate makes no temporal claim *and* declares it; silent omission = INSUFFICIENT, not NA |
| G2 SRT W3 (primary) | SRT-in-noise (dB SNR-50): **BKB-SIN** primary ≥5 y; **BabyBio (Pediatric AzBio)** % at fixed SNRs as co-report; HINT-C acceptable alternative if pre-declared (see §4.1) | UNPINNABLE absolute (companion §4) | **≥3 dB better** than frozen (convention, PROVISIONAL) | Quiet word/sentence %: **−5 pp** (convention) | T4 (T3 = provisional signal only) | Untestable child (developmental) = INSUFFICIENT with reason, never excluded silently (estimand §4.3) |
| G2 W2 | Word recognition in quiet/noise (%); localization RMS error (°) when testable | UNPINNABLE | ≥10 pp; ≥10° better (conventions) | −5 pp; +5° (conventions) | T4 | Localization NA if no valid bilateral test session; reason logged |
| G2-music W2–W3 | **UW-CAMP** (N5): pitch-direction threshold (semitones), melody ID (%), timbre ID (%) — **PROVISIONAL instrument for children** | UNPINNABLE | ≥10 pp on melody ID (convention); pitch threshold reported, no PASS delta in v1 | −5 pp melody (convention) | T4, but **capped at provisional signal** until pediatric CAMP validity inspected | W2 (<3.5 y): presumptive NA unless a validated toddler music task is pre-registered — none named in v1 |
| G2 W0–W1 | CAEP detection, VRA thresholds | — | **No PASS** (mechanism/chain input only) | — | T4 | Always applicable as chain evidence; never scored PASS |
| G3a W2/W3 spoken | PLS-5-class receptive+expressive SS + CDI (spoken norms); exact battery fixed §5.1 | UNPINNABLE bilateral-P0 range | **≥+0.4 SD within spoken stratum** (convention; SD = instrument norm SD) | **−0.2 SD** in every measured stratum/window | T4 (reconciled rule §5.3: T3+chain = provisional only) | Stratum defined by family-chosen modality at window (time-varying, §3.2) |
| G3a W2/W3 signed | ASL-CDI 2.0 (N7) vocab (W2); ASL-normed language battery for W3 — **UNPINNABLE instrument beyond 73 mo** (§5.1) | UNPINNABLE | ≥+0.4 SD within signed stratum (ASL norms) | −0.2 SD every stratum/window | T4 | Children with no signed exposure are not in this stratum; do not test-and-pool |
| G3a W1 | IT-MAIS / LittlEARS (auditory function) + CDI / ASL-CDI 2.0 | UNPINNABLE | NI + trajectory (no superiority PASS in W1) | −0.2 SD-equivalent (instrument-specific mapping pre-stated) | T4 | — |
| G3a bimodal | Hierarchy fixed §5.2: (1) highest-modality score, (2) total conceptual vocabulary | UNPINNABLE | Same 0.4/−0.2 SD rules applied to hierarchy level 1; level 2 NI required | −0.2 SD | T4 | Modality of "highest" pre-declared per child-window before seeing challenger data |
| G3b W1–W3 | **BLOCKED — no instrument** | — | **BLOCKED** | **BLOCKED** | T4 once unblocked | All cells **INSUFFICIENT** until §6 protocol completes. No exceptions, no judge imputation |
| G4 all (+adolesc. sensitivity) | Residual-hearing preservation (% ears, definition §7.1); fibrosis/new-bone **Seyyedi & Nadol 0–3** (N4) + volumetric % (N8); SGN density (cells/mm² or count, animal); scala patency (defined §7.1); G4-AAV re-dose demo | RH: UNPINNABLE for P0 infants (E4c is older/better-hearing ears); histology: adult archival only | Track P: **all applicable components ≥ frozen** (veto) | Per-component: §7.1 (mostly UNPINNABLE numbers; direction + veto pinned) | T2 minimum; T4 for residual hearing | Track R: G4 disclosed-traded, never PASS-claimed. AAV challengers: presumptive FAIL until G4-AAV met |
| G5 all + adolescence | Per-harm rates (App. C list), % per child, horizon stated | UNPINNABLE per harm | NI per harm (no superiority PASS needed) | **UNPINNABLE per harm** (§7.2) | T2/T4 per harm | Harm NA only if mechanism cannot cause it, with written justification (App. C) |
| G6 all | Stratum coverage (% of P0, App. D); burden (hrs/wk, visits/yr); equity (miles, insurance, rurality, home-language, EHDI LTFU); timeline (y to infant use) | Coverage denominator UNPINNABLE (D1); burden UNPINNABLE (companion §3) | Table complete + timeline stated + disparity within §7.3 bound | — | Literature/registry | No NA for coverage table: unknown stratum = "unknown", counted incomplete |

\* G1 windows denote the *child-age claim* the proxy evidence is
asked to support, not the age of tested listeners (§5.3 chain).

Missing-data, floor/ceiling (>20% at bound → pre-stated
alternative), and estimand rules carry over from GOAL
Appendix A / §4.3 unchanged.

## 3. G1 — functional resolution

### 3.1 Why "8" survives only as a convention

Step 0 Ch1a (Friesen, Shannon, Baskent & Wang 2001, PMID
11519582): CI speech plateau at **7–8 electrodes** for most
materials on 2001-era Nucleus-22/Clarion arrays (low performers:
no gain beyond 4; word/sentence marginal 7→10 in Nucleus-22
only); NH vocoder improved to ≥20 channels. The paper never
states "4–10 effective channels" — that span is a gloss.

Step 0 Ch1b (Berg et al. 2019, PMID 31067952): in imaging-verified
scala-tympani perimodiolar recipients, 16-channel CIS beat
8-channel CIS in quiet and 16 maxima beat 8/10 across tasks
including noise; benefit tracked electrode–modiolus distance.
Modern frozen arrays therefore plausibly already exceed the
2001 plateau on some tasks. Defending "frozen = 8" as an
empirical contemporary value would ignore Ch1b. Discarding 8
entirely would also be wrong: GOAL needs a stable, pre-registered
ruler, and 7–8 remains the best-inspected plateau estimate for
the older/lateral-wall end of the frozen mix.

**Resolution (D-G1a/b/c):** 8 is retained and explicitly
re-labelled a **stated convention** (versioned, changeable only
by re-freeze), with mandatory sensitivity scoring at **4, 10,
and 16**. Every G1 report shows the verdict under all four
anchors. If a candidate passes at 8 but fails at 16, the report
says so in the headline — the sensitivity is not a footnote.

### 3.2 PASS rule (binding once frozen)

A device candidate passes G1-spectral only if **both** hold:

1. **Convention bar:** ≥12 effective channels (Track P) or ≥16
   (Track R; also the Track P STRETCH) on a pre-specified
   channel-count task (channels vs maxima defined in App. B —
   Berg's distinction is mandatory; undisclosed maxima-counting
   = INSUFFICIENT), **and**
2. **Head-to-head bar:** ripple threshold (rip/oct, N1 paradigm)
   and spread of excitation better than a named frozen array
   (type, era, fitting stated) measured in the same study/model.
   A candidate tested only against a vocoder or a degraded
   comparator (cf. Ch2b Srinivasan caveat) cannot PASS.

Allegiance rule (§5.2) applies: inventor-lab-only G1 evidence
starts one GRADE level lower and needs non-inventor replication
to PASS. F/G/H remain **G1 = NA (pre-declared)**; portfolios
inherit the device verdict and may not claim a G1 win their
components did not earn (§4.2). Regenerative/bridge candidates
use their App. B functional anchor (frequency discrimination /
SRT benefit) — never hair-cell counts as "channels".

### 3.3 Ripple→channels conversion: UNPINNABLE

GOAL §4.2 promised a "ripple-to-channels conversion model
published Step 1". Inspected evidence does not support one:

- N1 reports thresholds in **ripples/octave** (adaptive range
  0.13–11.31) and benchmarks (~4 rip/oct for accurate quiet
  vowel/consonant recognition; <~1–2 rip/oct highly degraded).
  It states no map from rip/oct to a count of effective channels.
- N2 shows ripple thresholds drift with implant era/pre-op
  speech perception — any fixed conversion would bake in an
  era confound.
- Friesen/Berg "channels" are counts of active electrodes/maxima
  in a speech task — a different operational quantity from a
  ripple threshold. Equating them needs a validation study
  (same listeners, both tasks, pre-stated model) that was not
  inspected in Step 0 or this pass.

**v1 therefore publishes no conversion.** G1 dual-reports
rip/oct and channel-count as separate, non-convertible rulers
(master table). *What would pin a conversion:* an inspected
study measuring both in the same CI listeners with a stated
functional form + fit uncertainty, human-extracted in full;
until then any `channels ≈ k × rip/oct` claim scores
INSUFFICIENT. Status: **PROVISIONAL dual-report rule**
(abstract-level basis N1/N2; full texts owed).

### 3.4 Timing sub-gate: +20% DELETED

GOAL flagged +20% ITD NI as underived. N3 (Ehlers et al. 2017)
is decisive against deriving it as a percentage: with
synchronized research processors at 100 pps, all 16 BiCI
children showed ILD sensitivity but congenitally deaf children
had **weak or absent ITD sensitivity**, while children with
prior acoustic exposure retained it — and the abstract notes
clinical processors cannot reliably deliver binaural cues. A
frozen baseline that is near-absent and processor-dependent has
no stable denominator for "+20% error". Keeping the number
would let a candidate "pass" timing while delivering no usable
ITD at all.

**Replacement in v1:** (i) ITD/ILD JNDs reported descriptively
(µs / dB, processor + rate stated) whenever a bilateral-timing
claim is made; (ii) functional consequence scored via G2
localization RMS error (testable in children); (iii) degrading
a pre-specified temporal metric vs frozen head-to-head = G1
FAIL; (iv) a numeric timing NI margin is **UNPINNABLE**.
*What would pin it:* a pinned frozen ITD-JND distribution in
congenitally deaf BiCI children on *clinical* processors
(mean/SD/N by age), human-extracted — then a margin can be set
in absolute µs, never as a bare percentage of an unstable mean.

## 4. G2 — functional hearing

### 4.1 SRT test per age (named)

| Age / window | Primary | Co-report / alternative | Basis + status |
|---|---|---|---|
| W3, ≥5 y | **BKB-SIN SNR-50 (dB)** | BabyBio % correct at +10/+5/0/−5 dB SNR; HINT-C SRT if pre-declared (never switched post hoc) | N6 (NH norms, ages 5–12): BKB-SIN field data consistent with manual norms; BabyBio at ceiling in NH (≥86% even at −5 dB) → in CI children BabyBio % is the sensitive co-report, BKB-SIN the threshold. **PROVISIONAL** (abstract-level; CI-child norms UNPINNABLE) |
| W3, 3.5–5 y | **BabyBio (Pediatric AzBio) % at fixed SNRs** | Closed-set word recognition pre-declared per cohort | N6's youngest band is 5–6 y. Below 5 y no inspected normative source exists → scores are **within-study deltas only**, flagged PROVISIONAL; absolute norms UNPINNABLE |
| W2 (2–3.5 y) | Word recognition % (age-valid closed/open set, named in App. B per study) | Localization RMS° when testable | No single test can be pinned from inspected evidence; requiring BKB-SIN sentences at 2 y would guarantee floor effects. Test must be pre-declared; >20% at floor triggers the pre-stated alternative |
| W0–W1 | CAEP / VRA (mechanism only) | — | GOAL: no G2 PASS in W0–W1. Unchanged |

The ≥3 dB PASS applies to BKB-SIN SNR-50 (or HINT-C SRT if that
was the pre-declared test) — deltas across *different* tests are
never pooled into one "SRT gain". Quiet NI −5 pp applies to the
same test's quiet condition. Both numbers remain **conventions**
(D-G2a): no inspected source establishes 3 dB as the minimal
important difference for P0 children. They are retained because
GOAL pre-specified them and changing deltas without evidence is
worse than flagging them — PENDING-STAKEHOLDER MCID review (§8).

### 4.2 Localization

RMS error (°), bilateral condition, speaker array described in
App. B. PASS ≥10° better, NI +5° (GOAL conventions, kept).
Localization is also the v1 functional readout for bilateral
timing (§3.4). Frozen absolute RMS: UNPINNABLE.

### 4.3 Music: UW-CAMP named, PROVISIONAL for children

Battery: **University of Washington CAMP** (N5): pitch-direction
discrimination threshold, 12 isochronous-melody identification,
8-timbre identification. The 2008 abstract (N=8 adult CI users)
and 2009 validation title support CAMP as *the* standardized
adult CI music battery; neither inspected abstract establishes
validity, norms, or feasibility in 3.5–7-y-old congenitally deaf
children (melody ID presumes familiar-melody knowledge — a
cultural/exposure confound in W3).

**v1 ruling:** CAMP is the named battery for W3, melody ID
carries the ≥10 pp / −5 pp convention deltas, pitch threshold
is report-only — but **every W2–W3 music cell is capped at
"provisional signal" (never PASS)** until a pediatric CAMP (or
successor) validation is inspected in full. If no such source
exists at Gen 0 freeze, music downgrades to exploratory and the
gate table says so. *What would uncap it:* inspected pediatric
validation (age range covering W3, test–retest, floor/ceiling
in CI children). W2 music: NA (no validated toddler battery
named) — honest NA beats an invented one.

## 5. G3a — language, any modality

### 5.1 Instruments per modality (fixed)

| Stratum | W1 (9–24 mo) | W2 (2–3.5 y) | W3 (3.5–7 y) |
|---|---|---|---|
| Spoken | MacArthur-Bates CDI (spoken) + IT-MAIS/LittlEARS* | CDI + PLS-5-class receptive/expressive SS | PLS-5-class (or CELF-class where age-valid, pre-declared) SS |
| Signed (ASL) | **ASL-CDI 2.0** (N7; normed 9–73 mo) | ASL-CDI 2.0 | ASL-CDI 2.0 to 73 mo; **beyond 73 mo: UNPINNABLE** — no inspected ASL-normed battery for 6–7 y |
| Auditory function (not language) | IT-MAIS / LittlEARS | IT-MAIS/LittlEARS trajectory co-report | Not a G3a PASS instrument in W3 (ceiling; auditory ≠ language) |

\* IT-MAIS/LittlEARS measure early *auditory* function. They are
W1 chain/trajectory measures and never substitute for a language
score in either modality.

Caveats that travel with every G3a score: (i) N7's norming sample
is 120 deaf children **of deaf parents** — most P0 children have
hearing parents and later/variable ASL exposure. ASL-CDI scores
in P0 therefore measure *ASL vocabulary given exposure*, and EI
dose/exposure must be reported alongside (§3.2 context strata);
a low score with near-zero exposure is an exposure finding, not
a device finding. (ii) "PLS-5-class" means a named, normed
spoken-language battery with receptive+expressive standard
scores; the exact instrument per cohort is fixed in App. B
before scoring — v1 pins the *class + norm requirement*, not a
brand, because no instrument-comparison source was inspected.
That class-level pin is **PROVISIONAL**. (iii) Non-ASL signed
languages (e.g. BSL) need their own normed CDI-equivalent;
ASL norms must never be applied to another sign language.
For U.S. P0 (companion §1.1) ASL is the signed default; other
home sign languages = named stratum, instrument UNPINNABLE
until inspected. (iv) P1 CAEP / fNIRS remain mechanism measures
(§5.3 surrogate criteria), never sole G3a passes.

PASS/NI: ≥+0.4 SD within stratum (that instrument's norming SD),
NI −0.2 SD in *every* measured stratum/window (GOAL conventions,
PENDING-STAKEHOLDER MCID review). **No pooled SD across norms —
ever.** Adjustment set per §4.2 (modality, home language, SES
proxy, EI dose, additional disabilities). Family H causality
needs its stated identification strategy; adjustment alone
never claims causality (§8H).

### 5.2 Bimodal hierarchy (fixed)

For children with material exposure to both modalities in a
window, pre-declared per child-window before challenger data
are seen:

1. **Primary: highest-modality language score** — the better of
   the child's spoken-SS and signed-SS, each on its own norms.
   The 0.4/−0.2 SD rules apply here. Rationale: GOAL scores
   *language access*, not loyalty to one modality; penalizing a
   bimodal child for splitting exposure would punish exactly
   what Family H tests.
2. **Required NI co-check: total conceptual vocabulary** —
   concepts known in *either* modality counted once (CDI +
   ASL-CDI item mapping pre-stated). NI (−0.2 SD-equivalent on
   the pre-stated mapping) required; superiority on level 1 with
   a conceptual-vocabulary loss does not PASS.
3. Each single-modality score is still reported (no hiding a
   spoken loss behind a signed gain or vice versa), and the
   every-stratum NI rule applies to the child's assigned
   single-modality strata as well.

*What would strengthen this:* stakeholder confirmation that
"highest-modality" matches family goals (some families may value
both-modality growth over max) — flagged PENDING-STAKEHOLDER;
if stakeholders reject max-scoring, the hierarchy is amended by
re-freeze, not by scorer discretion.

## 6. G3b — BLOCKED (co-design protocol owed)

**State in v1: BLOCKED. All G3b cells INSUFFICIENT for every
candidate, including frozen.** Per GOAL §4.2, G3b scoring is
blocked until the instrument + MCID are co-designed with
Deaf/parent stakeholders (§9) and committed. This file invents
neither. Track P promotion (§4.2 requires G3b PASS) is therefore
**impossible until unblocking** — that is the intended
consequence, stated plainly so no Gen 0 report can imply a
promotable winner while G3b is blocked. Candidates may collect
candidate G3b-relevant data *exploratorily* (labelled as such);
exploratory data never retroactively become the gate.

**Co-design protocol needed to unblock (Step 1 debt, owner:
holder + stakeholder panel, before any G3b scoring):**

1. **Panel:** Deaf adults (incl. Deaf parents of deaf children),
   hearing parents of P0-like children (signed/spoken/bimodal
   families), older DHH youth where feasible, plus a
   measurement specialist. Recruitment, compensation, ASL
   interpretation, and decision rights (consensus vs majority +
   recorded dissent, cf. §9 judge rules) documented *before*
   deliberation. Holder participates as one parent voice, never
   as chair-with-veto (COI, §1.1/§12).
2. **Construct definition:** what "communication autonomy"
   means per window (W1: parent–child communicative success;
   W2/W3: child-initiated communication, family inclusion,
   frustration/behaviour correlates) — written, in plain
   language and ASL, before any instrument is shortlisted.
3. **Instrument selection:** panel reviews candidate family-
   reported autonomy/QoL instruments against the construct
   (existing-instrument systematic search first; new items only
   for demonstrated gaps). Criteria pre-stated: validity in DHH
   families, availability in ASL + home languages, burden,
   floor/ceiling in W1–W3, sensitivity to modality (an
   instrument that only credits spoken communication fails
   by construction and must be rejected on that ground).
4. **MCID elicitation:** stakeholder-defined minimal important
   difference (anchor-based where possible: what score change
   corresponds to a family-noticeable change), separately for
   the NI margin and any superiority claim. No MCID borrowed
   from a spoken-language SD rule.
5. **Pilot + psychometrics:** cognitive interviews (signed +
   spoken families), test–retest, missing-data plan. Results
   published with the instrument, including failures.
6. **Commit by re-freeze:** instrument, scoring, MCID, NI
   margin, and windows entered as Appendix A v2 via holder +
   independent co-approver (§12). Only then do G3b cells leave
   INSUFFICIENT — prospectively, never retroactively.

Until step 6, any document in this repo that needs a G3b verdict
must print **"G3b: BLOCKED (INSUFFICIENT) — co-design pending"**.

## 7. G4 / G5 / G6

### 7.1 G4 — biology preservation (Track P veto)

**Fibrosis scale named: Seyyedi & Nadol 0–3** (N4, PMID
25122600). Severity of eosinophil/lymphocytic infiltration,
giant-cell reaction, new bone formation, and fibrosis each
scored **0–3** at three 1-mm segments (first 1 mm at
cochleostomy, midway, last 1 mm from tip). GOAL Appendix A's
"0–4 histopath scale" does not match the inspected Nadol-lab
scale and is **corrected to 0–3** in v1 (GOAL.md text fix owed
at freeze). Scores must be reported **per segment** (basal >
distal is the N4 finding — averaging segments away hides the
insertion-trauma signal). Complement: volumetric % new bone /
fibrous tissue per Kamakura & Nadol (N8) where 3D reconstruction
exists. Status: **PROVISIONAL** (abstract-level; full-text
scoring rubric — what distinguishes 1 vs 2 vs 3 — owed by human
extraction; the abstract names the scale range and segments,
not the per-grade criteria).

Per-component rules (Track P: **all applicable must pass**;
any FAIL = G4 FAIL = veto):

| Component (unit) | Frozen ref | NI / PASS rule in v1 | Min tier |
|---|---|---|---|
| Residual-hearing preservation (% ears meeting pre-stated PTA-shift definition; definition + timepoint in App. B) | UNPINNABLE for P0 ≥70 dB infants. Step 0 E4c (78% of ears, Madgar 2025) is mean age 9.68 y, mean pre-op PTA ~60 dB — **must not** be used as the infant frozen ref | Direction pinned: challenger rate ≥ frozen rate measured with the *same* preservation definition. Numeric NI margin (pp): **UNPINNABLE** | T4 human (animal RH = signal only) |
| Fibrosis / new bone (0–3 per segment, N4; + % volume, N8) | Adult archival human (N=28/17 bones, older devices) + animal. No pediatric/modern-array frozen distribution inspected | Challenger median grade per segment ≤ frozen comparator grade in same model; any segment worse by ≥1 grade at ≥Moderate GRADE = FAIL. Finer margin: UNPINNABLE until per-grade rubric extracted | T2 (mature/deafened animal); human histology T4-descriptive only |
| SGN / hair-cell survival (density or count, method stated) | UNPINNABLE point | NI direction pinned (no survival loss vs frozen/sham in same model); numeric margin UNPINNABLE | T2 |
| Scala patency (% scalae patent/cannulable for later infusion, by time-since-implant) | **UNPINNABLE** — Step 0 E4a: no inspected source reports this %. This is Q0's core missing number | No PASS/FAIL possible in v1 → INSUFFICIENT. Step 2 must pre-define the patency threshold *and* the evidence type that could supply it (§8G) before Q0 is scored | T2 + human imaging/histology |
| G4-AAV (re-dosing / later-AAV efficacy after capsid exposure) | — | **Presumptive FAIL** for any AAV-using challenger until capsid-switch / non-viral re-dose or post-exposure efficacy shown (GOAL §4.2, unchanged). Anti-capsid immunity explicitly scored in App. C | T2 minimum |

Supporting-cell consumption (Family D) = alteration, not
preservation. Track R reports G4 as knowingly traded with the
same component table filled in — disclosure, never a PASS.

### 7.2 G5 — safety & durability: margins UNPINNABLE per harm

GOAL requires NI within margins "from registry ranges", with
stress scenarios at the 90th percentile / upper 95% CI bound
(§6). Neither Step 0 nor this pass inspected a CI registry or
cohort harm-rate range to the required standard (this pass's
registry queries returned no pinnable record; see §9). Deriving
margins now would invent base rates. **v1 therefore pins the
structure and leaves every number blank:**

| Harm (App. C; % per child, horizon stated) | Frozen base rate/range | NI margin | Stress (90th pct / upper CI) |
|---|---|---|---|
| Anesthesia adverse event, <12 mo surgery | UNPINNABLE | UNPINNABLE | UNPINNABLE |
| Meningitis (specify vaccination era) | UNPINNABLE | UNPINNABLE | UNPINNABLE |
| Facial-nerve injury (transient vs persistent split) | UNPINNABLE | UNPINNABLE | UNPINNABLE |
| CSF leak / gusher (**malformation-specific** — never pooled with normal anatomy) | UNPINNABLE per malformation | UNPINNABLE | UNPINNABLE |
| Vestibular loss (test + symptom definition stated) | UNPINNABLE | UNPINNABLE | UNPINNABLE |
| Device failure / revision / reimplantation (hard vs soft failure split; to 7 y + adolescence) | UNPINNABLE | UNPINNABLE | S-revision scenario (§6) UNPINNABLE |
| Residual-hearing loss (see G4 — scored once, cross-ref) | UNPINNABLE | See G4 | — |
| Stimulation injury: charge density / thermal / phototoxic (candidate-specific limits, not rates) | Frozen-device limits: manufacturer specs owed | Challenger must state limit + margin to tissue-damage threshold in App. B; no rate NI in v1 | — |
| MRI incompatibility events | UNPINNABLE | UNPINNABLE | — |
| Tumor / misrouting (neurotrophin, reprogramming); opsin immunogenicity; AAV shedding/immunity | No frozen comparator rate (frozen eCI does not carry these mechanisms) | Scored as **absolute** App. C severity × probability with persistent-harm stopping rule; any ≥major-severity signal at ≥Moderate GRADE = FAIL in Track P. NI-vs-frozen is category-wrong here and is not used | — |
| False reassurance / delayed standard care (F/H); genomic mis-triage / VUS distress (G); binaural deprivation from delayed 2nd ear | UNPINNABLE rates | Time-to-CI / time-to-access deltas scored in G6 + event reporting in App. C; numeric NI UNPINNABLE | S-access (§6) UNPINNABLE |

Consequence: **no G5 cell can PASS in v1** on rate-NI grounds;
cells read INSUFFICIENT (or FAIL on an absolute-signal rule
above). *What would pin each row:* named registry/cohort
full-text human extraction giving rate + N + era + definition
+ age band per harm (pediatric, bilateral where relevant), then
margin-setting as a stated fraction/absolute pp of that range
with stakeholder input on acceptable trade-offs (§6 decision
rule) — margins are partly value choices and are flagged
PENDING-STAKEHOLDER once base rates exist. FMEA filing
(App. C, severity 1–4 × probability bands) is required in v1
regardless: absence of a rate never excuses absence of an FMEA.

### 7.3 G6 — deliverability + proposed disparity bound

PASS (GOAL): stratum coverage table complete (App. D D4 — itself
UNPINNABLE until D1–D3, companion §2) + burden disparity within
bound + earliest-plausible infant timeline stated (§10 staging).
Portfolio union coverage reported separately.

**Proposed disparity bound (CONVENTION, PENDING-STAKEHOLDER —
not a literature finding).** For each burden/equity metric
(therapy+mapping hrs/week; visits/year; travel miles to centre;
EHDI loss-to-follow-up %; coverage % by insurance/rurality/
home-language subgroup), define the *gap* as worst-subgroup
minus best-subgroup (or P0-mean) value. Challenger PASSES the
disparity element only if for every reported metric:

```text
gap_challenger ≤ gap_frozen + 5 percentage points   (rate metrics)
gap_challenger ≤ 1.25 × gap_frozen                  (hrs, visits, miles)
AND no subgroup's absolute coverage falls below its frozen
    coverage by more than 5 pp (no leveling-down by harming
    the best-served group either: report absolutes, not gaps alone)
```

Rationale for proposing numbers at all: without a pre-registered
bound, "disparity within bound" is unscorable; 5 pp / 1.25× are
tight enough that a challenger serving only well-resourced
families fails, loose enough that measurement noise alone does
not. They are **value choices for stakeholder ratification or
replacement** (§8), sensitivity-reported at 2 pp / 10 pp and
1.1× / 1.5×. While frozen burden/equity values are UNPINNABLE
(companion §3), the bound can only be applied to concurrently
measured frozen-cohort data, flagged PROVISIONAL. Timeline
element is scorable now: no stated adult-first staging timeline
(§10) = G6 FAIL; Track R families unable to reach infants in
~15 y are watch-list by definition.

## 8. PENDING-STAKEHOLDER register

Defaults below are **provisional conventions**. They govern
scoring only until stakeholder elicitation replaces/confirms
them by re-freeze; every score report must re-run headline
verdicts under the stated sensitivities.

| Item | v1 provisional default | Sensitivity to report | Owner |
|---|---|---|---|
| Fitness order (§7 lexicographic: FAILs → INSUFFICIENT → G2 → G3a → G3b → G1 → burden) | GOAL §7 order as written | Rank-sensitivity to order (§7 already requires it); at minimum: G3a↔G2 swap, G3b moved above G3a | Stakeholder panel (§9) |
| G2 MCID 3 dB; quiet NI −5 pp; music/localization deltas | GOAL numbers | 2 dB and 5 dB SRT; ±5 pp bands | Stakeholders + clinicians |
| G3a 0.4 SD / −0.2 SD; bimodal max-hierarchy | GOAL numbers; §5.2 hierarchy | 0.3/0.5 SD; both-modality-growth alternative to max | Stakeholders (Deaf + parent) |
| G3b instrument + MCID + NI | **None — BLOCKED** (§6) | n/a until co-designed | Co-design panel (§6) |
| G5 trade-off rule (added revision risk accepted only if G2 gain ≥ threshold and G3b NI holds, §6) | Rule shape kept; threshold = G2 PASS delta | Threshold varied with G2 MCID sensitivity | Stakeholders + clinicians |
| G6 disparity caps (§7.3) | 5 pp / 1.25× | 2 pp / 10 pp; 1.1× / 1.5× | Stakeholders |

## 9. Inspection log + what would pin the UNPINNABLE cells

Inspected this pass via `web_fetch` (2026-11-02): PubMed
E-utilities MEDLINE records for PMIDs 16158665 (N1), 26520316
(N2, abstract truncated in fetch — era finding read, per-group
threshold numbers **not** relied on), 28618809 (N3), 25122600
(N4), 27371868 (N8, re-fetch; Step 0 E4a wording relied on for
the correlation direction), 18309572 + 19474735 (N5; 2009
record read to title/identity level in truncated fetch —
pediatric claims deliberately **not** asserted from it),
26756155 (N6, full abstract), 32180180 (N7, full abstract).
Two initial `pubmed.ncbi.nlm.nih.gov` HTML fetches returned
wrong/truncated records and were discarded; all relied-on
records above are the E-utilities MEDLINE versions. Registry
harm-rate `esearch` queries (revision/meningitis/registry
combinations) returned zero pinnable records under the strings
used — recorded as "no record pinned", never as "rate is zero".
HTTP 429 throttling hit twice; queries were retried with
changed strings, not repeated unchanged.

**Pinning checklist (human extraction, in blocking order):**
(1) G5 registry per-harm rates → margins (§7.2). (2) Frozen
absolute G2/G3a ranges for bilateral P0 by window (companion
§4). (3) Full-text N1/N2/N4 (ripple per-group values;
Seyyedi–Nadol per-grade rubric) + ripple↔channels validation
study if one exists (§3.3). (4) Clinical-processor ITD-JND
distribution in congenitally deaf BiCI children (§3.4).
(5) Pediatric CAMP validation (§4.3); CI-child BKB-SIN/BabyBio
norms + <5 y SRT norms (§4.1). (6) ASL-normed battery beyond
73 mo + non-ASL sign CDIs (§5.1). (7) Scala-patency % by
time-since-implant, modern arrays (§7.1, Q0). (8) G3b
co-design (§6) and §8 elicitations. (9) GOAL.md text fixes:
fibrosis 0–4→0–3; timing +20% deletion; ripple-conversion
promise → dual-report (holder + co-approver, §12 — listed here,
not made here).

*No DOI, PMID, N, or percentage in this file was invented:
every identifier appears in Step 0 or in an N1–N8 MEDLINE
record fetched 2026-11-02. Holder + independent co-approver
freeze: PENDING. Human dual extraction: PENDING. This is a
proposed pin — nothing here is gate-deciding.*




