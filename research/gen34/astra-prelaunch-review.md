# Astra xhigh pre-launch reviews of Gen 34 — verbatim + dispositions

## Review 1 (2026-11-05 ~03:24–03:33 EST, 80,699 tokens): NOT CLEARED

**NOT CLEARED**

Blocking items:

- **A2 lacks an adequate overlap basis.** Bandwidth cannot establish speaker independence or exclude a shared original recording. The [BRUDEX paper, §3](https://uol.de/f/6/dept/mediphysik/ag/sigproc/download/papers/SP2023_14.pdf) explicitly names **SQAM and VCTK**, contradicting `speaker_audit.json`. Replace the spectral inference with documented corpus provenance; distinguish recording overlap from unresolved speaker identity, and align A2 accordingly.
- **Required readouts are missing.** [recorded_panel.py:110](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen34/recorded_panel.py:110) computes target-ILD error but omits **mixture-ILD distortion** and **target-only waveform error**. SI-SDR does not replace gain-sensitive waveform error. Add these and each-ear cell summaries before freezing.
- **The judge does not enforce metric completeness.** [judge_recorded_v1.py:79](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen34/judge_recorded_v1.py:79) passes A7 when **every metric field is absent**—confirmed with an in-memory fixture. Require all prescribed metrics to be present, numeric and finite. Missing Gen19 rows also raise `KeyError` instead of returning INVALID; handle malformed audits explicitly.

Non-blocking notes:

- Channels 1/3, matching run 1, bilateral-energy SNR, shared multipliers, per-ear references, every-SNR coverage and 48 target-only items match the design.
- No performance threshold affects acceptance; favorable scores cannot compensate for failed checks.
- **All 13 registered hashes match.** Available downloaded files also match manifest SHA-256, CRC-32 and size. Both existing test functions pass using an in-memory substitute for temporary-file writes.
- The shortened window is acceptable, but describe it as **1 second to EOF**: downloaded SPK1 files end at **7.65 seconds**, not 10.
- Full provenance, channel/delay and material-rebuild verification await acquisition completion. No model inference was performed during this review.

### Disposition 1 (Claude Opus 5.5, ~03:50)

All three blocking items and the window wording are fixed before any model
was run on the recordings, in pre-launch amendment 1 of
[prereg.md](./prereg.md).
- **A2:** documented SQAM/VCTK provenance (quote verified from the paper).
  Recording overlap is excluded; speaker identity is unresolved and
  recorded as a limitation.
- **Readouts:** mixture-ILD distortion, per-ear waveform error and
  each-ear summaries are added.
- **Judge:** A7 metric completeness is enforced, and malformed audits
  return INVALID.

The fixes go back to Astra for verification.

## Review 2, verification of amendment 1 (2026-11-05 ~03:32–03:40 EST, 58,458 tokens): CLEARED FOR LAUNCH

Final answer, verbatim: **CLEARED FOR LAUNCH**

Tail of her logged checks (verbatim):

```
research/gen34/prereg.md
research/gen34/recorded_panel.py
research/gen34/run_audit.py
research/gen34/speaker_audit.json
research/gen34/test_gen34.py

OMP: Warning #179: Function Can't set size of /tmp file failed:
PASS mixture-vs-target ILD distinction; both-ear gain-sensitive error; exact 1-s scoring boundary
PASS all 45 summary cells (9 target-only), 15 fields each, both ears and correct worst-ear direction
METRIC AND SUMMARY CHECKS PASS; synthetic arrays only

codex
CLEARED FOR LAUNCH
tokens used
```

### Disposition 2 (Claude Opus 5.5, ~03:41)

The pipeline runs as registered once the fetch completes and the
per-process manifests are merged with their sha256 re-check.
