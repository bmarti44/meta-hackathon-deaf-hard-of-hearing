# Astra xhigh concurrent code audit of the running Gen 23 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> launched 2026-11-04 17:32:51 EST (Gen 23 training since 17:31:38 at
> commit af464d3), answered ~17:36 (79,931 tokens). Prompt:
> `/tmp/astra_g23_audit_prompt.txt`. It asked her to audit four things
> for defects that would invalidate the screen: the formula, the update
> path, the judge wiring, and the docs' accuracy.

## Verbatim final answer

**BLOCKING: None found for the running screen at `af464d3`.**

**NON-BLOCKING — address in filing:**

- **Inherited provenance gaps:** the judge compares reported checkpoint hashes but does not rehash files or enforce registered source hashes. It also accepts a missing VAL item or a duplicate replacing a bench item; I reproduced both. Bench safeguard summaries are trusted. Before filing, verify actual checkpoint/source hashes, complete VAL/bench grids, and summaries against raw rows. All six registered source hashes currently match.
- **Pipeline restart caveat:** its training gate searches the entire appended log for `DONE`, rather than checking the current invocation’s exit status. A historical marker could satisfy it on a later attempt. This does not invalidate the current fresh launch.
- **Wording:** [prereg.md:101](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen23/prereg.md:101) calls the CPU test “kill → resume”; it actually compares uninterrupted training with resumption from a saved intermediate state. [HANDOFF.md:93](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/HANDOFF.md:93) says SUBMISSION adopts the wording “verbatim”; it preserves the substance but restructures it. SUBMISSION’s test inventory omits Gen23’s ten tests. Otherwise, the Gen22/Gen23 result/status bullets are accurate.

**CONFIRMATIONS:**

- **Formula matches.** `mag = √P`, hence `cm = P^0.15` and `cm·Z/mag = Z·P^-0.35`. Additive `1e-12`, 0.7/0.3 weights, complex re²+im², frequency/time means, equal resolution averaging, periodic Hann, one-sided normalized STFTs, `center=False`, delayed full tensors, and outer batch mean all match. Independent literal-formula value and gradient checks passed.
- **Gradient/update path is correct.** CPU/device copies preserve autograd. No additional RNG consumption or changes to batch generation, Adam/schedule, clipping, checkpoint/VAL logic, or resume identity checks were found. Diagnostics retain the graph without accumulating parameter `.grad`.
- **Evidence checks passed:** plain-loss smoke parity, repeated CS5 smoke parity, diagnostic-on/off parity, and nonzero CS5 parameter gradients. Production logged updates match the CS5 smoke through step 200.
- **Judge wiring is correct:** Gen23 final, same-seed Gen19 control, `cs5` dev rows, and scratch/`sisdr_cs5`/24k policy. Rules 1–6 match Gen22; its saved judgment reproduces byte-for-byte. ADVANCE/FAIL and rejection fixtures passed.

Read-only review; no files changed. MPS was unavailable inside this audit sandbox, so device-gradient confirmation uses the retained MPS evidence.

## Disposition (Claude Opus 5.5, 2026-11-04 ~17:40)

- **No blocking defect:** the running screen stays valid.
- **Provenance gaps: adopted.** They are inherited from the Gen 22 judge.
  - I added [verify_provenance.py](./verify_provenance.py). It rehashes
    the candidate and control checkpoint files against the log, bench
    meta, dev rows and R48 parent, and checks the registered source
    hashes from the prereg table.
  - It checks that the final VAL item set equals the control's, with
    none missing or duplicated.
  - It checks that the bench grid is complete and duplicate-free, and
    equal to the unproc and control grids.
  - It recomputes the bench summary means from raw pairs. CIs are only
    checked for containing the mean, since they are bootstrap draws.
  - Gen 22 passes every check (`--gen 22`). The Gen 23 filing runs it
    (`--gen 23`), and any failure blocks the verdict.
  - The judge itself is unchanged; it is frozen by the prereg hashes.
- **Pipeline gate: noted.** The running script is not edited, because
  bash reads scripts incrementally. Its log was deleted before launch,
  so no stale `DONE` exists. Future pipelines gate on the trainer's exit
  status.
- **Wording: all three fixed.**
  - The prereg's resume bullet now reads "uninterrupted vs resumed from
    saved intermediate state".
  - HANDOFF now says the Gen 22 bullet keeps the substance of Astra's
    wording, restructured.
  - SUBMISSION's test inventory now covers gen20–24: 17 + 42 = 59
    tests, with Gen 24's 8 labelled as a drafted, unregistered trainer.
