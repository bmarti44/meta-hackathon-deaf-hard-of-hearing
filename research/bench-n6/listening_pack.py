"""Stage C blinded NH vocoder listening pack (father, headphones).

Builds randomized, blinded vocoded items from held-out crops for the
systems named on the command line. Identity key is written to a
SEPARATE file (key.json) so the listener scores blind. Refuses to
run for a system unless bench_results.json shows it earned vocoder
listening (Stage B go/no-go) -- use --allow-unpassed only to build a
methods-shakedown pack, which is then labeled as such in the output
and must not be read as evidence.

This is an informal NH screen, not an SRT study and not CI evidence.
Every file passes the safety limiter. Headphones at a comfortable,
fixed level; stop if anything sounds harsh or painful.

Run: /tmp/gen9env/bin/python research/bench-n6/listening_pack.py \
       --systems unproc causal_gate [--gen15 <ckpt>]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from bench import build_crops, load_gen15  # noqa: E402
from baselines import CausalSpectralGate, oracle_irm_waveform  # noqa: E402
from common import FS, limit_signal  # noqa: E402
from vocoder import vocode  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", nargs="+", default=["unproc", "causal_gate"])
    ap.add_argument("--gen15", default=None)
    ap.add_argument("--n-per-cell", type=int, default=2)
    ap.add_argument("--allow-unpassed", action="store_true",
                    help="methods shakedown only; pack is labeled non-evidence")
    ap.add_argument("--out", default=str(HERE / "listening_pack"))
    a = ap.parse_args()

    results_path = HERE / "bench_results.json"
    passed = {}
    if results_path.exists():
        passed = {k: v.get("earns_vocoder_listening", False)
                  for k, v in json.loads(results_path.read_text()).get("go_nogo", {}).items()}
    unpassed = [s for s in a.systems if s != "unproc" and not passed.get(s, False)]
    if unpassed and not a.allow_unpassed:
        raise SystemExit(f"REFUSED: {unpassed} have not passed Stage B go/no-go "
                         f"(see bench_results.json). Re-run bench.py, or pass "
                         f"--allow-unpassed for a labeled methods shakedown.")
    label = "EVIDENCE SCREEN" if not unpassed else "METHODS SHAKEDOWN - NOT EVIDENCE"

    fns = {"unproc": lambda c: c["mix"],
           "causal_gate": lambda c: CausalSpectralGate().process(c["mix"]),
           "oracle_noncausal": lambda c: oracle_irm_waveform(c["clean"], c["noise"], c["mix"])}
    if a.gen15:
        fns["gen15_causal"] = lambda c, r=load_gen15(a.gen15): r(c["mix"])
    crops = [c for c in build_crops(a.n_per_cell) if c["kind"] != "ssn"]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20261103)
    items = [(ci, s) for ci in range(len(crops)) for s in a.systems]
    rng.shuffle(items)
    key, sheet = [], [f"# Listening pack ({label})", "",
                      "For each file: write every word you can make out,",
                      "then rate clarity 1 (nothing) to 5 (effortless).",
                      "One listen per file. Fixed headphone volume.", ""]
    for n, (ci, s) in enumerate(items, 1):
        c = crops[ci]
        audio = vocode(limit_signal(fns[s](c)), seed=int(rng.integers(0, 10 ** 6)))
        name = f"item_{n:03d}.wav"
        sf.write(out / name, audio, FS)
        key.append({"file": name, "system": s, "kind": c["kind"], "snr_db": c["snr_db"]})
        sheet.append(f"- {name}: words: ____________  clarity(1-5): __")
    (out / "key.json").write_text(json.dumps({"label": label, "key": key}, indent=1))
    (out / "scoresheet.md").write_text("\n".join(sheet) + "\n")
    print(f"PACK DONE ({label}): {len(key)} items -> {out} (key.json is sealed until scored)")


if __name__ == "__main__":
    main()
