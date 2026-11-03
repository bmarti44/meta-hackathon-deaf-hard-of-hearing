# Gen 7 J3 — Stage-0 bench protocol for the causal DNN front-end (Appendix B)

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**, disclosed per §9
> rule 3. **Date: 2026-11-03. Gen 7 under GOAL v2.3**
> (no generation cap, no loop stop; PASS bar unchanged).
> Inputs: `gen06/Gen6-summary.md` §4 items 5, 7 (the only
> Gen 7 J work licensed: "a J Stage-0 bench build *if*
> HP-J1-4 signs — measured latency/power records, not
> another design generation"); `gen06/candidate-J2-ai-
> pediatric.md` §§2–6 in full (comparator C-J2, Stage 0
> definition, K1 desk-kill, HP-J2-1…6); `gen05/candidate-
> J1-ai-frontend.md` (HP-J1-1…4). **Inspected records
> only; no invented data.** Every number below is either
> (a) inherited from an inspected record and cited as
> such, or (b) a **PROPOSED design budget** that humans
> must ratify at HP-J3 freeze *before* the bench runs and
> may not loosen after seeing bench data. There is no
> third class. **G3b BLOCKED. No PASS claimed; scores
> nothing; files no manifest; J3 is not a scored
> candidate** — it is the executable form of J2's
> Stage 0. If it is ever scored as a candidate, that is
> a governance error, not a result.
>
> **Fielding fence (inherited in full).** J1 and J2 are
> unfielded pending **HP-J1-4** (G1 = NA for a denoiser-
> as-portfolio-component). This protocol may be drafted
> and ratified now; it **runs** only after HP-J1-4 signs
> and the HP-J3 pins (§B.9) are filed. Bench work exposes
> no human, but Gen6-summary §4.7 licenses the build
> conditionally on HP-J1-4, and this file does not widen
> that license. Bench output fills exactly one existing
> pin — **HP-J2-1** (measured latency/power/sync file) —
> and discharges HP-J1-1 in its measured form. It moves
> no G-cell: Stage-0 results are engineering data (T0),
> never G2 evidence (J2 §3, carried verbatim).

## B.0 What this bench decides, and what it cannot

Decides (J2 kill **K1**): whether a *causal* DNN build,
running on named C-J2-class hardware, meets filed
latency, power, bilateral-sync, and output-limiting
budgets measured end-to-end — i.e. whether J2 Stages 1–3
exist at all. Cannot decide: any intelligibility,
language, wear-time-in-children, or autonomy claim.
Objective intelligibility metrics (§B.6) are reported to
reject hopeless builds cheaply; a good objective score
on the bench is **not** a Stage-1 substitute, and the
≥3 dB SRT bar (App. A G2-W3) is never evaluated here —
no listeners sit at this bench.

## B.1 Builds under test (frozen at HP-J3-1)

| ID | Build | Role |
|---|---|---|
| **A0** | C-J2 passthrough: the child's-own-processor signal path (Nucleus 8 / Kanso 3, SmartSound iQ 2 + SCAN 2 feature state as filed per J2 §2.5) with DNN stage bypassed | Reference zero for every delta below. All latency/power claims are A1 − A0 *and* A1 absolute |
| **A1** | Causal DNN build (locked weights hash, HP-J2-3) inserted before sound coding; MAP, ACE-class coding, charge per phase unchanged | The only build that can pass this bench |
| **A2** | Non-causal / offline oracle (e.g. SepFormer-class, future-frame access) | Engineering ceiling reference **only**. Inadmissible for any pass; exists to price what causality costs. Any A1 design decision tuned against A2 on validation material is a held-out breach (§B.3 partition) |

Hardware strata, reported separately, never pooled:
**H-primary** = research build on actual Nucleus 8 /
Kanso 3 hardware (the only stratum whose latency/power
numbers can fill HP-J2-1); **H-dev** = development board
/ body-worn research front-end (results labeled
non-transferable to on-processor claims, J2 §3 carried);
**H-secondary** = MED-EL SONNET 3 / RONDO 3 (C-J2-M),
only if a research build exists for it — MED-EL numbers
are a separate stratum per J2 §2.5, never averaged with
Cochlear numbers. AB hardware: excluded until HP-J2-2
inspects IFU text (J2 §2.3, carried).

## B.2 Inherited inspected facts this bench is built on

1. The 2024 research DNNs (PMID 38853168, full text
   inspected Gen 6) were **non-causal**, and SepFormer
   inference took ~5× signal duration on a laptop CPU —
   "not suitable for real-time applications such as a CI
   audio processor" (paper's own statement). Hence
   causality and real-time factor are *measured* here,
   never asserted from architecture diagrams.
2. The same paper cites the real-time CI delay budget as
   **below ~10–20 ms** to avoid disturbing speech
   production / audio-visual integration. J2 pre-filed
   the stricter working budget **≤10 ms** (design budget,
   human-ratifiable at freeze). §B.7 keeps both numbers
   and assigns them different jobs.
3. Off-population support only: PMID 40657924 (abstract
   inspected, Gen 6 re-sweep §7) found human
   intelligibility essentially unchanged as a causal
   DNN's algorithmic latency fell 20 → 10/5 ms — in
   hearing-loss and normal-hearing listeners, **not
   stated to be CI users**, no N in abstract. It informs
   the budget choice; it is not CI latency evidence and
   cannot relax §B.7.
4. PMID 37030808 (Deep ACE, abstract inspected): "without
   sacrificing processing latency" is a design claim with
   **no ms figure, no power figure** in the inspected
   abstract. Filed as architecture precedent, never as a
   bench expectation.
5. Battery reference points (manufacturer, inspected
   Gen 6): Cochlear defines "all day hearing" as **16 h**
   (Kanso 3 footnote); MED-EL prints up to 60 h (2× 675
   zinc-air) / 17 h (Rechargeable Max) / 10 h (Standard)
   / **7 h** (Micro). **No battery capacity (mAh/Wh), no
   processor current draw (mA/mW), and no Nucleus-class
   power figure exists in any inspected record.** Every
   such cell in §B.5 is therefore a *measurement output
   of this bench*, and any version of this file that
   contains a pre-filled mW number is fabricated.
6. Shipped-comparator effect (PMID 41046328, adult,
   manufacturer-run, T3): SCAN 2 + automated ForwardFocus
   beat SCAN 2 alone by 4.2–4.3 dB SRT in rear/side-noise
   geometries. Bench consequence: §B.3 must include the
   spatial geometries where A0 is strongest, or the
   bench will certify a build whose only skill is
   re-implementing beamforming (J2 §2.1 warning).

## B.3 Test signals and diffuse-babble construction

### B.3.1 Signal inventory (all items filed by file-hash at HP-J3-1)

| # | Signal | Purpose |
|---|---|---|
| S1 | Digital silence, ≥60 s | Noise floor; idle power (§B.5) |
| S2 | Click / impulse train (isolated impulses ≥200 ms apart, ≥100 repetitions) | End-to-end latency (§B.4.2), causality shift test (§B.4.4) |
| S3 | Log swept sine 100 Hz–10 kHz | Group delay vs frequency (§B.4.3); rig calibration |
| S4 | Clean target speech, held-out sentence lists (corpus and lists pinned at HP-J2-4/HP-J3-1; **no norm or list-equivalency number is asserted in this file**) | Quiet-path distortion metrics; mixture target |
| S5 | Stationary speech-shaped noise, LTASS-matched to S4 corpus | Specificity control (J2 §3: smallest predicted DNN increment) |
| S6 | Diffuse multi-talker babble (§B.3.2) | Primary-geometry interferer |
| S7 | Spatial babble renderings, S0Nrearhalf- and S0N3-style geometries (mirroring the PMID 41046328 conditions as *geometry labels only*) | Non-degradation check where A0 is strongest |
| S8 | Two frontal talkers (target + frontal interferer, level-matched) | Wrong-talker stress (J1/J2 FMEA row); bench side = objective target/interferer energy attribution only |
| S9 | Alarm / environmental set as pinned at HP-J2-5 (smoke/CO alarm, caregiver call from behind, traffic cues are J2's pre-listed candidates; final set is a human pin, not chosen here) | Bench-side audibility proxy: output level of alarm band A1 vs A0. Detection-by-a-child is a Stage-2 endpoint, never a bench claim |
| S10 | Music excerpts (battery named at HP-J2-4) | Artefact/distortion proxy; music NI itself is human-tested later |

Levels (PROPOSED, HP-J3-1 ratifies): target speech at
55 / 65 / 75 dB SPL at the processor microphone
position; mixture SNR grid −10, −5, 0, +5, +10 dB
(SNR defined on active-speech level of target vs
interferer, measurement method named in the run file).
Calibration: SPL verified with a measurement microphone
at the device microphone inlet before every session;
calibration record (date, calibrator ID, measured
offset) is part of the run archive. A run without a
calibration record is void, not "close enough."

### B.3.2 Diffuse babble — construction recipe (executable)

"Diffuse" is a measured property of the rendered field,
not a label on a folder. Construction:

1. **Talker pool:** ≥8 simultaneous independent talkers
   (PROPOSED floor; talker count, sexes, and language of
   pool pinned at HP-J3-1), drawn from a corpus partition
   disjoint from S4 targets and from all A1 training
   material (partition by talker *and* by corpus, J2 §3
   held-out rule carried).
2. **Decorrelation:** each talker stream independently
   offset in time; no shared envelope source. Streams are
   rendered to the processor microphones through either
   (a) a loudspeaker ring/array in a treated room, or
   (b) measured/simulated binaural room impulse responses
   from ≥8 azimuths at ear height — rendering method is
   pinned at HP-J3-1 and the impulse-response set is
   hashed into the run file. Direct-to-reverberant ratio
   and reverberation time of the rendering are measured
   and reported, not assumed.
3. **Verification of diffuseness (accept/reject the
   stimulus, before any build is judged):** inter-
   microphone magnitude-squared coherence of the babble-
   only field is measured at the processor's own
   microphone spacing and compared against the
   spherically-isotropic diffuse-field reference
   (sinc(kd) form). Acceptance band around that reference
   is a PROPOSED tolerance pinned at HP-J3-1; a babble
   rendering outside the band is re-rendered, and builds
   are never scored against a failed stimulus. LTASS of
   the rendered babble (at the microphone) is reported
   alongside, so a "diffuse" field that is diffuse but
   spectrally unlike speech is visible as such.
4. **Co-located variant:** for the S0-target primary
   geometry, target speech is rendered from 0° azimuth
   over the diffuse babble field (J2 §3 frozen geometry:
   speech always from front for primary). A separate
   fully-co-located single-channel mix (target + babble
   summed electrically, no spatial rendering) is also
   filed, because it is the hardest case for any
   spatial cue and the cheapest to reproduce exactly.

### B.3.3 Held-out discipline on the bench

Two disjoint stimulus sets: **bench-dev** (may be used
while debugging the rig and the build) and **bench-
validation** (sealed until the single scored run of
§B.7; talkers, sentences, and babble seeds disjoint from
bench-dev and from A1 training). Any rebuild after
opening bench-validation re-seals a fresh validation set
or the run is labeled exploratory-after-seen: Y with the
consequences J2 §3 already states. Random seeds for all
rendering are recorded; an unseeded rendering is
unreproducible and therefore unscored.

## B.4 Latency measurement method

### B.4.1 Definition (the number HP-J2-1 will carry)

**End-to-end latency** = time from acoustic event at the
processor microphone inlet to the corresponding change
in the output presented to the implant-side interface
(electrodogram/RF-frame timestamp, exact tap point named
in the run file for H-primary; DAC output for H-dev).
Report **A1 absolute** and **A1 − A0 incremental**, each
decomposed where the hardware permits into: framing/
windowing, algorithmic look-ahead (must be 0 beyond the
filed budget, §B.4.4), compute, and I/O buffering. A
single unsourced "the model is causal, latency = frame
length" assertion fills nothing.

### B.4.2 Impulse method (primary)

S2 impulses are played through the calibrated rig;
input reference channel and output tap are recorded on a
common clock. Latency per impulse = output-event time −
input-event time (threshold-crossing at a filed fraction
of peak, cross-checked by cross-correlation peak).
Rig-only delay (loudspeaker → microphone → reference
chain, A0 replaced by straight-through reference) is
measured in the same session and subtracted; both the
raw and rig-corrected numbers are reported. Report
distribution over all repetitions: mean, p50, p95, p99,
max, and jitter (p99 − p50). Sample rate of the
measurement chain must resolve ≤0.1 ms (PROPOSED floor:
≥96 kHz measurement sampling or equivalent interpolated
timing, method filed).

### B.4.3 Frequency-dependent check

S3 swept-sine group delay reported in octave bands
250 Hz–8 kHz for A0 and A1. Purpose: a build whose
*average* latency passes while smearing delay across
frequency (or across time-varying gain states) is
visible here and invisible to §B.4.2 alone. Time-varying
behavior: repeat §B.4.2 with impulses embedded in S6
babble at 0 dB SNR, since separation builds may change
effective delay under load — quiet-only latency is not
the filed number.

### B.4.4 Causality audit (pass/fail, not a metric)

1. **Shift test:** an impulse inserted at time *t* in an
   otherwise fixed input must produce zero output change
   at all output times corresponding to input < *t*
   (within the filed framing quantisation). Any pre-echo
   = look-ahead = desk-kill of the build (J2 §3 carried).
2. **Static audit:** receptive-field / look-ahead of the
   locked network graph computed from the filed weights
   hash's architecture record; must agree with the shift
   test. Disagreement voids the run until resolved.
3. **Steady-state runs:** ≥10 min continuous S4+S6 at
   0 dB SNR; report frame-deadline misses (count of
   frames whose compute exceeds the frame period),
   accumulated clock drift vs reference, and latency
   distribution in minute 1 vs minute 10 (thermal/
   throttling drift is a bench finding, not a surprise
   reserved for children).

### B.4.5 Bilateral synchronisation

For bilateral configuration: same S2/S3 procedure run on
both processors driven from a common stimulus; report
**interaural latency difference** distribution (mean,
p95, max) and its drift over the §B.4.4 steady-state
run, A1 vs A0. This is HP-J1-3/HP-J2-1's bench half;
the localisation consequence is human-tested at
Stage 1/2 and is never inferred from bench timing alone.
Asymmetric-arm operation (one side A1, one side A0) is
measured to have its timing filed, and remains a
protocol deviation in any later human stage (J2 §3).

## B.5 Power measurement and the Nucleus-class battery budget

### B.5.1 Method

Power is measured **at the battery terminals of the
actual processor** (H-primary), not estimated from DSP
utilisation: series shunt / battery-emulator logging of
voltage and current at a filed sampling rate (PROPOSED
floor 1 kHz, so frame-rate current structure is
visible), integrated over each condition. Conditions,
each ≥10 min steady-state after warm-up (PROPOSED
duration floor): S1 silence; S4 quiet speech at 65 dB;
S4+S6 at −5 / 0 / +5 dB SNR; S4+S5 at 0 dB; S8; S9
alarms; S10 music — every condition run for A0 and A1
on the same unit, same MAP, same battery type, order
counterbalanced across sessions, ambient and case
temperature logged (a build that passes cold and
throttles warm is a §B.4.4/B.5 joint finding).
Reported per condition: mean current, mean power,
peak (p99) power, energy per hour, and Δ(A1−A0) in mW
and %. H-dev power is reported in its own column and
never fills an H-primary cell.

### B.5.2 Battery-life projection (formula filed; inputs measured)

For each filed battery type actually used with C-J2
hardware (battery types pinned at HP-J3-1; **no capacity
figure is asserted in this file** — §B.2 item 5):

```
projected hours(build, battery, condition-mix)
  = E_usable(battery)  /  P_mean(build, condition-mix)
```

- `E_usable` is **measured** by discharging the actual
  battery/pack type on the bench at the A0 load profile
  (or taken from a manufacturer record only if one is
  inspected and filed at HP-J3-1 — until then the cell
  is blank, not borrowed from MED-EL's printed hours).
- `condition-mix` = filed weights over §B.5.1 conditions
  representing a listening day (weights are a PROPOSED
  convention pinned at HP-J3-1, printed with the result;
  a single-condition "battery life" number is barred).
- Reported: projected hours for A0 and A1 on every filed
  battery type, absolute delta in hours, relative delta
  in %. The inspected conventions anchor interpretation
  only: Cochlear's 16 h "all day" definition is the
  reference day; MED-EL's 7 h smallest-battery stratum
  is the standing proof (J2 §2.2) that on small cells
  compute headroom is a wear-time question first. A
  projection is a bench estimate: take-home datalog
  confirmation is owed at Stage 2 (J2 §3) and a bench
  projection is never quoted as measured wear-time.

### B.5.3 Thermal and rollback checks (bench halves of J2 FMEA rows)

Case-temperature rise A1 vs A0 over the steadiest
§B.5.1 condition (numeric limit = hardware owner's
filed specification if inspected at HP-J3-1; otherwise
reported descriptively with the cell marked
no-inspected-limit — never judged against an invented
°C number). Rollback: A1 → A0 reversion executed and
timed on the bench (J2: rollback ≤1 fitting session,
pre-tested in Stage 0); a build that cannot be reverted
cleanly fails §B.7 regardless of its other numbers.

## B.6 Objective signal metrics (engineering screen only)

On bench-validation material (§B.3.3), for A0 / A1 / A2:
one intrusive intelligibility-prediction metric and one
quality/distortion metric, **named and version-pinned at
HP-J3-1** (this file deliberately asserts no metric's
validity for CI electrodogram-domain output — where the
metric requires acoustic output, the vocoder/electrode-
to-acoustic rendering used is filed and the result is
labeled simulation-class, cf. the T0 status Gen 6 gave
PMID 41511184's simulation-only record). Also filed:
quiet-path distortion on S4 (A1 vs A0), alarm-band level
preservation on S9 (dB, A1 vs A0), S8 target/interferer
attribution error rate under the frozen target-talker
rule (HP-J2-3), and output-limiting verification:
electrodogram charge per phase and maxima vs the filed
MAP on every condition — **any over-MAP output is a
build desk-kill** (J2 FMEA Sev-3 row, carried). These
metrics can only *reject* or *pass-to-Stage-1* a build;
none is an SRT, none enters a G-cell.

## B.7 Pass / kill thresholds (the scored run)

One scored run per build-freeze, on bench-validation
material, H-primary stratum. **All rows must pass; any
kill row firing = J2 K1 exercised = build desk-killed,
Stages 1–3 do not exist for that build.** Threshold
provenance is printed in every row; PROPOSED values are
void until humans ratify them at HP-J3 freeze, and no
threshold may be edited between opening bench-validation
and filing the run (re-powering/re-thresholding after
seeing the estimate is barred, J2 K3 logic applied to
the bench).

| # | Quantity (method) | PASS | KILL | Provenance |
|---|---|---|---|---|
| B1 | End-to-end latency, A1 absolute, p99 (§B.4.2, incl. in-babble) | ≤10 ms | >10 ms | J2 §3 filed working budget |
| B2 | End-to-end latency, A1 absolute, max under any §B.5.1 condition | ≤20 ms | >20 ms at any sample | Upper edge of the 10–20 ms disturbance bound cited in PMID 38853168 (inspected) — hard ceiling even if HP-J3 were to relax B1 |
| B3 | Look-ahead (§B.4.4 shift + static audit) | 0 samples beyond filed framing | any pre-echo / disagreement | J2 §3 causal-only rule |
| B4 | Frame-deadline misses, 10-min steady state (§B.4.4.3) | 0 | ≥1 unrecovered miss | PROPOSED (HP-J3-2 ratifies; a filed tolerance >0 must name the concealment behavior) |
| B5 | Real-time factor on H-primary (compute time / signal time, worst condition) | <1 with filed headroom margin | ≥1 | Definition of real-time; PMID 38853168's ~5× offline figure is the standing counterexample |
| B6 | Interaural latency difference, bilateral A1, p95 (§B.4.5) | ≤ HP-J3-2 value | > HP-J3-2 value | **Blank — no inspected numeric tolerance exists.** HP-J1-3/HP-J3-2 must file one from an inspected source class or a stated human ruling before the run; the bench may not run bilaterally with this cell empty |
| B7 | Projected battery life, A1, filed day-mix, smallest filed battery type (§B.5.2) | ≥16 h reference day **and** relative loss vs A0 ≤ HP-J3-2 value | <16 h, or loss > HP-J3-2 value | 16 h = inspected Cochlear "all day" convention (§B.2.5); relative-loss % = **PROPOSED blank** (candidate value for human debate: 10% — printed as a proposal, not evidence; HP-J3-2 ratifies or replaces) |
| B8 | Output limiting (§B.6): charge/phase and maxima vs MAP, all conditions | never exceeds MAP | any over-MAP sample | J2 §3/FMEA Sev-3 (level-creep = Stage-0 fail) |
| B9 | Quiet-path and alarm-band preservation (§B.6): S4 distortion metric and S9 alarm-band level, A1 vs A0 | within HP-J3-2 margins | outside margins | **Blank margins** — bench proxies for J2's human quiet NI (−5 pp) and alarm battery; the human margins do not convert to bench dB/metric units by any inspected record, so HP-J3-2 must file the translation or these rows run as report-only and B9 cannot pass the build alone |
| B10 | Rollback A1→A0 (§B.5.3) | clean reversion demonstrated | failed/partial reversion | J2 §3 (rollback pre-tested in Stage 0) |

Objective intelligibility/quality metrics (§B.6) have
**no pass threshold in this table by design**: no
inspected record maps a bench objective score to the
≥3 dB human SRT bar, so inventing a metric cut-off
would manufacture a gate. They are reported with A2 as
ceiling context; a build may be *voluntarily* withdrawn
by humans on a null objective screen, and that
withdrawal is filed as a human decision, not a kill
"survived/cleared" event (D10 language preserved).

## B.8 Run archive (what "measured, not modeled" means on disk)

Per scored run, filed before any human stage is
discussed: build weights hash + architecture record
(HP-J2-3); hardware unit IDs, firmware, MAP file hash;
battery type(s) + discharge curves (§B.5.2); stimulus
file hashes, rendering seeds, impulse-response set hash,
diffuseness verification output (§B.3.2.3); calibration
records; raw input/output timing captures (§B.4) and
V/I logs (§B.5) retained unprocessed alongside the
analysis scripts (version-pinned) that produced every
reported statistic; deviations log (any departure from
this appendix, with the run re-labeled exploratory if a
deviation touches a §B.7 row). Summary statistics
without the raw captures do not fill HP-J2-1.

## B.9 HOLDER-PINs

Carried, unchanged: **HP-J1-4** (run gate) · HP-J1-3
(bilateral-sync + environmental-sound scope; bench half
= §B.4.5/B6) · HP-J2-1 (this bench's output file) ·
HP-J2-2 (comparator feature-state file; A0 definition
depends on it) · HP-J2-3 (weights hash, target-talker
rule, held-out partition) · HP-J2-4 (test/list pinning
feeding S4/S10) · HP-J2-5 (alarm set feeding S9).
New: **HP-J3-1** bench freeze (builds, hardware units,
stimulus inventory + hashes, levels/SNR grid, rendering
method, metric names/versions, battery types,
condition-mix weights) · **HP-J3-2** threshold
ratification (every PROPOSED/blank cell in §B.7: B4
tolerance, B6 interaural value, B7 relative-loss %, B9
margins — signed by named humans before bench-validation
is opened; H-1…H-8 PENDING as throughout) · **HP-J3-3**
run-archive acceptance (a named human confirms §B.8
completeness before HP-J2-1 is marked filed).
Unpinned ⇒ the bench does not run, as ever.

## B.10 Standing state

J-lineage unfielded pending HP-J1-4. G3b BLOCKED.
FROZEN retained. Validation set 0. This appendix files
no candidate, moves no cell, and — until a scored run
exists under HP-J3-1/2 — contains no measured number of
any kind. K1 remains **unevaluated**: not triggered,
not cleared (D10).

*End. GEN7 J3 bench appendix = executable form of
GEN6-J2 Stage 0. Run gate: HP-J1-4 + HP-J3-1/2.*

