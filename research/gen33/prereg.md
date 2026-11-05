# Gen 33 pre-registration: linked two-ear processing on frozen Gen 32 weights (feasibility, T0)

> Claude Opus 5.5, 2026-11-05 ~03:05 EST. Written before any linked
> output was computed.
> Source: both reviewers' Gen 32 choice (c). Astra's exact design is
> adopted (disposition in
> [../gen32/astra-review-gen32.md](../gen32/astra-review-gen32.md)).
> T0 only. `promoted FALSE`. **This is a feasibility check, never ADVANCE.**
> Gen 32 stays FAIL, and nothing here can rescue a verdict.

## Question

Every room-trained model (Gen 27–29, 32) made the direction cues (ILD)
slightly worse at easier SNRs when each ear was processed on its own. If
one cleanup mask is shared by both ears, do the direction cues stop
getting worse, without costing either ear's clarity?

## The one change: linked inference (no training, no selection)

`research/gen33/linked.py`, applied to the frozen Gen 32 α = 0.7
seed-17 checkpoint (`645a0623…`):

    zL = relu(encoder(L)), zR = relu(encoder(R))
    m  = mask_net((zL + zR) / 2)
    yL = decoder(zL · m),  yR = decoder(zR · m)

- It uses the model's own padding, cropping and fixed delay.
- It needs one mask-network evaluation per stereo frame.
- Inference stays one 602,510-parameter model.
- A learned-basis shared mask does not mathematically guarantee preserved
  acoustic ILD/ITD (Astra), so the cues are measured.

**Engineering checks** (`test_gen33.py`, 4/4 passing, Gen 19 and Gen 32
weights):
- identical-ear input reproduces the mono output bit-for-bit;
- swapping the ears swaps the outputs bit-for-bit;
- changing future input leaves earlier output unchanged;
- the mono rebuild equals `model(x)`;
- in `--mode independent`, the versioned runner `spatial_linked.py`
  reproduces the legacy spatial documents exactly (Gen 32's
  `spatial_wiseftpd_s17.json` and the registered Gen 19 self-test);
- the decision script rejects a fake "linked" document that is really
  the independent one.

## Evaluation (registered before running)

**Scenes:** the original spatial scenes, unchanged:
- the 4 existing-bench scenes;
- the 16 crossed scenes: 4 babble crops at −5 / 0 / 5 / 10 dB × target
  at −60 / −30 / 30 / 60°, with the crowd at the mirror azimuth.

They use the same references, metrics and head model (`spatial.py`,
assumed).

**Added measures:**
- per-ear SI-SDR and STOI against each ear's clean target, for every
  crossed scene;
- the same scenes with the crowd removed (target-only), with per-ear
  SI-SDR/STOI and ILD/ITD errors.

**Systems:**
- Gen 32 linked (the candidate);
- Gen 32 independent (isolates the linkage effect);
- Gen 19 independent (the preservation reference; it must reproduce the
  registered control exactly);
- bypass;
- Gen 19 linked, **descriptive only**: linkage applied to the accepted
  baseline, not gating.

## Decision rule (Astra's, prospective; `judge_link.py`)

"Linkage feasibility passed" requires all four checks:
- **L1:** the original SP gate passes for linked Gen 32 vs Gen 19.
  `judge_v3.spatial_gates` is used unchanged.
- **L2:** the crossed-scene mean target-ILD error (16 scenes) is
  **strictly** below independent Gen 32's.
- **L3:** in **every** SNR × mirrored-direction subset (4 × 2, two scenes
  each), mean ILD error and mean ITD error are each ≤ independent
  Gen 19's.
- **L4:** the mean per-ear (both ears pooled) SI-SDR and STOI differences,
  linked − control, are ≥ 0 against **both** independent Gen 32 and
  independent Gen 19, in every noisy SNR × direction subset and in each
  mirrored target-only subset.

Any failure rejects this specific wrapper. There is no tuning: no
alternative pooling, mask averaging or weighting after the result.

**If it passes:** further room advancement still needs every original
gate, replication and a fresh confirmation. Identical-ear parity means the
mono R1a and D failures of Gen 32 are unchanged.

**Hardware caveat (Astra):**
- This architecture is plausible for synchronised stereo software.
- Nucleus 6 input/output access, two-ear synchronisation and downstream
  processing are unverified.
- Linked-AGC studies give a rationale (localisation improved in one study,
  speech showed no significant change in another). They do not validate
  this enhancer.

Run: `research/gen33/pipeline.sh` (about 2 min, CPU).

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen33/linked.py` | `9351c9f5eaf054a4252a639fd869107d27bae9da6dab508e2965c71866ab8acd` |
| `research/gen33/spatial_linked.py` | `0f423f3a01b88db2bfec86a027a45fc215ec20e641fbbacac548b41787731d60` |
| `research/gen33/judge_link.py` | `5741968dfdb28a8ca38868d1b3096df2fac6ed62c135c591b8e65a6887511606` |
| `research/gen33/test_gen33.py` | `77c3c4fc263a3fae3d1cb9b7b3bed22ceb409440b642031b44c42ae0caff516b` |
| `research/gen33/pipeline.sh` | `fd01f4c3a5a1c54610e748bfda687158a2fc78427da86812c0edd0a01e8bc730` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/gen27/judge_v3.py` | `faa38995052d38de526fbc868baed6dab577bc0598c1c045dcb956023ba4beb7` |
| `research/bench-n6/spatial.py` | `1bd0e32b073fdbf228f518269953469e7e0b5c7c0ddef4c980a5af3509a68834` |
| `research/bench-n6/spatial_bench.py` | `9b5c89ed1d9e32e597dd67ed6cce58f727abf73ffe0c15c58342c12b7dfbb4f2` |
| `research/bench-n6/bench.py` | `e4bf2da436212456013524efc5357be170ea89e13f4cc32caaf1ab53db240711` |
| `research/bench-n6/baselines.py` | `62076332ca56f3283e5d4bd88102c91c234ecf45a83660a7d4b0e530f82136ae` |
| `research/gen27/selftest/spatial_gen19_s17.json` | `2337f65992a052ab83ef361cd7d49d1c1af429d203f64ec78a1bbd17fbedbbea` |
| `research/gen32/spatial_wiseftpd_s17.json` | `0c8a7bf2416485325df15136f6660c0929583319cb10500f4bf88a41d58f648d` |
| `research/gen32/weights/wiseftpd_seed20261117.pt` | `645a062323718958158f32af4398ce3759aae541168db08a3fe286dba57c90b3` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
