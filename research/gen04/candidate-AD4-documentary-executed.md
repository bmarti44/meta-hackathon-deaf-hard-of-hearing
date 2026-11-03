# Gen 4 Candidate AD4 — AD3 documentary protocol EXECUTED as far as agents can (A1 lineage) [Track P device-lineage, documentary]

> **Model routing (GOAL S9).** Requested: **Sol 6.1, xhigh**
> (ideation). Actual: **`muse-wonder-full-1.0`**. Date:
> **2026-11-03**. Authority: **holder Sisyphus directive**.
> GOAL v2.2. **Gen 4 = 4 of max 4 (4/4) — FINAL. After
> Gen 4 the clock is exhausted without new external
> evidence.** **Status: AD3's protocol run at agent-triage
> level on real documents — declares nothing, runs no
> model, clears no kill.** AD3 S3 reserves every "filed"
> declaration to human dual extraction; AD4 **cannot**
> declare EVALUABLE/UNEVALUABLE-documentary. What AD4
> adds is the first *executed* documentary result in the
> lineage: named documents, fetched, hashed, searched —
> and a per-pin triage state (S3). **G3b: BLOCKED. Same
> PASS bar. No invented specifications.** GEN1-A1's kill
> remains **UNEVALUABLE**; its disputed G6 FAIL stays on
> A1 (AD4 is not an A1 repair, ever).

## 1. ID / parentage / mutation

`GEN4-AD4`; manifest [`manifest-GEN4-AD4.csv`](./manifest-GEN4-AD4.csv)
= GEN3-AD3 (G1/G5 `true`, rest `false`, AD3 S8 reasons).
Parent GEN3-AD3. **One mutation:** AD3's protocol *as
procedure* → AD3's protocol *executed* (agent scope).
No new falsification question (disclosed). AD3 is the
one Gen-4 candidate whose motivating executed result
Gen3-summary S4.1 asked for *is this file's own S2* —
the execution was possible without new human acts
because documents, not children or animals, are its
substrate. That exception is AD4's alone; P4/QR4/W4
claim no equivalent licence.

## 2. What was actually done (2026-11-03, agent, triage)

Workspace held **no PDFs**. Fetched from
`accessdata.fda.gov` (URLs + bytes + SHA-256 in
[`ad4-extraction-record.csv`](./ad4-extraction-record.csv)):
3 SSEDs (MED-EL P000025/S134, 43 pp.; AB P960058/S167,
50 pp.; Cochlear P970051/S172, 24 pp. — MED-EL/AB byte
sizes match `gaps/round2-pdf-labels.md`'s manifest) +
labelling (Cochlear P970051/S172C Physician's Package
Insert bundle, 686 pp.; MED-EL P000025C, 26 pp.).
Searched with **pypdf 6.21.4** (scripts preserved at
`/tmp/ad4_extract.py`, `/tmp/ad4_labels.py`,
`/tmp/ad4_cochlear.py`; PDFs at `/tmp/ad4/`) for:
charge density, µC(/cm²/phase), charge per phase,
pulse width/duration, µs, max current, current level,
contact/surface area, compliance voltage, stimulation
rate/pps, battery (life/hours), impedance.

**Result: the FDA public SSED/label class, as inspected,
does not contain A1's electrical pins.** Across all 3
SSEDs: 0 hits for every charge/pulse/area/current term
("battery" hits = *Pediatric Minimum Speech Test
Battery* / *Charité Test Battery*). Cochlear's 686-pp.
insert: "charge" = rechargeable-battery warnings + ESD;
no µC charge values, no pulse-width or contact-area or
max-current numeric specs in sampled contexts; the only
electrical numbers are clinical programming ranges —
stimulation **720–2400 Hz/channel, total 5760–14400 Hz,
6–20 channels/maxima** (Nucleus 24 CIS/ACE study) —
which are *not* P-2 fields. MED-EL P000025C is a
scanned-image PDF (pypdf extracted **0 text**, 26 pp.) —
not agent-searchable without OCR/human eyes.

## 3. Per-pin triage state (AD3 S3 rules; NOT declarations)

| Pin | AD4 agent-triage state | Why |
|---|---|---|
| P-1 named device/contacts | **PARTIAL** | Devices/processors named in SSEDs (MED-EL SONNET/RONDO p.3; Cochlear/AB systems) but **per-contact areas absent** in every inspected doc → below AD3 filed bar |
| P-2 safe-charge limit | **NOT FILEABLE from inspected class** | No manufacturer max charge density in any SSED/label searched. The model's own `shannon_k_limit 1.85` (sens 1.5/1.79/2.0) + ASSUMED `contact_area 0.003 cm²`, `pulse_width 25 µs` (`gaps/a1_model/model.py` PARAMS, labelled ASSUMED in-source) remain exactly that — AD4 confirms no primary source in this class upgrades them. Remaining routes are *different source classes*, named for humans: manufacturer technical/clinical manuals per named array, original PMA device-description sections, consensus standards for margin divisor. Agent triage predicts — cannot declare — UNEVALUABLE-documentary on P-2 unless a human files from those classes |
| P-3 battery floor | **NOT FILED** | No hours-at-stated-levels anywhere inspected; battery text = safety warnings. Route: processor user manuals (hours) × stated map levels — human extraction |
| P-4 growing geometry | **UNTOUCHED by AD4** | Not an FDA-label object; literature extraction owed (ages per A1 S3). Model today: `cochlea_length 35 mm` ASSUMED (sens 28–35), strip domain 20×2 mm |
| P-5 fibrosis rubric | **ASSUMED map stands, now frozen-in-print** | `GRADE_PROXY` verbatim: g0 (0 mm, 1.2 S/m), g1 (0.125, 0.30), g2 (0.25, 0.10), g3 (0.375, 0.0334); sigma bounds cited, thickness map modeller's — so per AD3 S3 every grade sweep = **assumption-sensitivity**, kill evaluable only if verdict invariant across grades. Seyyedi & Nadol verbal 0–3 already located (AD3); per-grade cited mapping still owed |
| R-1 convergence | **Criterion PROPOSED** (S4) | No new solve licensed until holder signs it |
| R-2 in-sheath SGN | **HOLDER-PIN HP-AD4-2** | `sgn_in_sheath=True` at every grid (gen03 attack); refinement cannot answer it |

Model constants frozen-in-print for any future run
(`model.py`, SEED 20261102, deterministic): cited —
σ perilymph 1.2, bone 0.0334, modiolus-eff 0.2734 S/m;
Greenwood 165.4/2.1/0.88. ASSUMED — dx/dy 0.125,
electrode_y 0.375, modiolar wall 0.25, spacing 1.0 mm,
threshold_frac 0.5, frac-from-apex 0.65. Artefact split
verdict carried verbatim: grade-3/0.25 mm zero retired
as grid artefact; magnitudes unconverged, dx-bound;
**case not rehabilitated**.

## 4. R-1 proposed convergence criterion (PROPOSED-FROZEN)

Halving sequence dx = 0.125 → 0.0078125 on the primary
endpoint (excitation width, both modes, per grade×
distance): converged iff max relative change between
successive halvings ≤ **5%** at **two consecutive**
halvings, endpoints computed identically (`threshold_frac`
0.5, sens 0.3/0.7 reported). Unmet at finest feasible
grid ⇒ INSUFFICIENT-model-sensitive. HP-AD4-1 = sign or
replace **before** any solve; the ~40+ min dx=0.0078125
run stays unlicensed until then.

## 5. Remaining human steps (exact, complete)

1. Dual human extraction of the 5 fetched docs against
   `ad4-extraction-record.csv` (confirm/overturn triage)
   + visual/OCR extraction of MED-EL P000025C.
2. Source-class extension decision: request
   manufacturer technical manuals / PMA device sections
   for ONE named array (P-1 completion) — or accept
   P-2 as unfound. Regulatory reviewer (PENDING)
   confirms document status before any pin is primary.
3. Per-pin tolerances stated **before** extraction opens
   (AD3 S9 — HP-AD4-3); third-human adjudicator named.
4. HP-AD4-1 (R-1) + HP-AD4-2 (R-2) signed rulings.
5. Human evaluability declaration (AD3 S3 rule):
   EVALUABLE ⇒ A1 runs under freeze; UNEVALUABLE-
   documentary ⇒ A1 archives with pins named (P-2 first
   on current triage), resurrection only via the missing
   documentary object existing — **new evidence, not a
   new generation** (clock is 4/4).

FMEA: AD3 D-AD3-1…4 verbatim (pin-shopping, stale era,
evaluability overclaim, manufactured rubric) + AD4
delta: agent negative results quoted as human-verified
absences ⇒ breach (triage ≠ declaration, printed here).
Burden: 0 family; cheapest lineage by design.
**FTO: Not assessed.**

*End. AD3 executed to the agent boundary; the boundary
is the finding. G3b BLOCKED. Clock 4/4.*
