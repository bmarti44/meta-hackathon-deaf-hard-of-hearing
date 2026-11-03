"""Bench-n6 runner: no-implant validation of causal NR front-ends.

Requested model Sol 6.1 / actual muse-wonder-full-1.0 (session runtime).
Stages per PROTOCOL.md. Everything here is T0 in-silico plus files for
normal-hearing vocoder screening. NO implant, NO listener claim.

Eval crops: identical construction to gen13/eval2.py build_eval_crops
(RNG 777, held-out targets 1988/1993, held-out babble 8842/8297,
SNR -5/0/+5/+10, 4 s). Systems are waveform-in/waveform-out so any
future causal model can be dropped in behind --gen15.

Run: /tmp/gen9env/bin/python research/bench-n6/bench.py --n-per-cell 4 \
       [--gen15 research/gen15/weights/<ckpt>.pt]
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "gen13"))
sys.path.insert(0, str(HERE.parent / "gen15"))

from common import FS, bootstrap_ci, envelope_correlation, limit_signal, rms, si_sdr  # noqa: E402
from baselines import CausalSpectralGate, oracle_irm_waveform  # noqa: E402
from vocoder import extract_envelopes, vocode  # noqa: E402

TRAIN_SPK = ["84", "174", "251", "422", "652", "777", "1272", "1462", "1673", "1919"]
TEST_SPK = ["1988", "1993"]
TEST_BABBLE_SPK = ["8842", "8297"]


def build_crops(n_per_cell):
    """Same draw order/RNG as gen13 eval2.build_eval_crops."""
    from train2 import babble, crop, load_pool, make_ssn_fast, rms as _rms
    pool = load_pool(TEST_SPK + TEST_BABBLE_SPK)
    rng = np.random.default_rng(777)
    SEG = 4 * FS
    crops = []
    for kind in ["babble-heldout-spk", "ssn", "white-heldout", "quiet"]:
        snrs = [999.0] if kind == "quiet" else [-5.0, 0.0, 5.0, 10.0]
        for snr in snrs:
            for i in range(n_per_cell):
                spk = TEST_SPK[i % len(TEST_SPK)]
                clean = crop(rng, pool[spk][rng.integers(0, len(pool[spk]))], SEG)
                clean = (clean / (_rms(clean) + 1e-9) * 0.1).astype(np.float32)
                if kind == "quiet":
                    noise = np.zeros_like(clean)
                elif kind.startswith("babble"):
                    noise = babble(rng, pool, TEST_BABBLE_SPK, n=SEG)
                elif kind == "ssn":
                    noise = np.concatenate([make_ssn_fast(rng, SEG // 2),
                                            make_ssn_fast(rng, SEG - SEG // 2)])
                else:
                    noise = rng.standard_normal(SEG).astype(np.float32)
                if kind != "quiet":
                    noise = (noise / (_rms(noise) + 1e-9) * _rms(clean)
                             * 10 ** (-snr / 20)).astype(np.float32)
                crops.append({"kind": kind, "snr_db": float(snr), "spk": spk,
                              "clean": clean, "noise": noise,
                              "mix": (clean + noise).astype(np.float32)})
    return crops


def load_gen15(path):
    import torch
    from model_causal import CausalTasNetEnh, undelay
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    m = CausalTasNetEnh()
    m.load_state_dict(ckpt["state_dict"] if isinstance(ckpt, dict) and "state_dict" in ckpt else ckpt)
    m.eval()

    def run(mix):
        with torch.no_grad():
            y = m(torch.from_numpy(np.asarray(mix)[None].astype(np.float32)))[0].numpy()
        return undelay(y).astype(np.float32)
    return run


def metrics_for(clean, est):
    tr = slice(256, -256)
    ref_env = extract_envelopes(clean)
    est_env = extract_envelopes(est)
    ref_el = extract_envelopes(clean, n_of_m=True)
    est_el = extract_envelopes(est, n_of_m=True)
    T = min(len(ref_env), len(est_env), len(ref_el), len(est_el))
    try:
        from pystoi import stoi
        st = float(stoi(clean[tr].astype(np.float64), est[tr].astype(np.float64), FS, extended=False))
    except Exception:
        st = float("nan")
    return {"sisdr": si_sdr(clean[tr], est[tr]), "stoi": st,
            "ace_env_corr": envelope_correlation(est_env[:T], ref_env[:T]),
            "ace_electro_corr": envelope_correlation(est_el[:T], ref_el[:T]),
            "peak": float(np.max(np.abs(est))), "rms": rms(est)}


def evaluate_go_nogo(summary):
    """PROTOCOL Stage-B gates for the best non-oracle causal system.

    A system earns NH vocoder listening time (Stage C) only if babble
    improves on BOTH waveform and ACE readouts without harming quiet
    or held-out white noise beyond tolerance. Thresholds are screening
    bars set in PROTOCOL.md, not clinical claims.
    """
    verdicts = {}
    for name, by_kind in summary.items():
        if name in ("unproc", "oracle_noncausal"):
            continue
        b, q, w = by_kind.get("babble-heldout-spk", {}), by_kind.get("quiet", {}), by_kind.get("white-heldout", {})
        # Quiet is judged ABSOLUTELY, not as delta vs unprocessed:
        # unprocessed quiet scores ~148 dB (clean vs itself), so any
        # processing shows a meaningless ~-127 dB delta (bench run 1).
        gate_babble = summary.get("causal_gate", {}).get("babble-heldout-spk", {})
        gates = {
            "babble_d_sisdr_ci_lo_gt_0": b.get("d_sisdr", {}).get("ci_lo", -9) > 0,
            "babble_sisdr_gt_classical_gate": b.get("sisdr", -9) > gate_babble.get("sisdr", -9),
            "babble_d_ace_electro_corr_ci_lo_gt_0": b.get("d_ace_electro_corr", {}).get("ci_lo", -9) > 0,
            "quiet_abs_sisdr_gt_15db": q.get("sisdr", -9) > 15.0,
            "quiet_d_stoi_gt_-0.05": q.get("d_stoi", {}).get("mean", -9) > -0.05,
            "white_d_sisdr_gt_-1db": w.get("d_sisdr", {}).get("mean", -9) > -1.0,
        }
        verdicts[name] = {"gates": gates,
                          "earns_vocoder_listening": bool(all(gates.values())),
                          "earns_implant_consideration": False,
                          "note": "Implant consideration additionally requires Stage C + D per PROTOCOL.md; never from this bench alone."}
    return verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-cell", type=int, default=4)
    ap.add_argument("--gen15", default=None, help="optional Gen15 causal checkpoint")
    ap.add_argument("--out", default=str(HERE / "bench_results.json"))
    a = ap.parse_args()
    t0 = time.time()
    crops = build_crops(a.n_per_cell)
    systems = {"unproc": lambda c: c["mix"],
               "causal_gate": lambda c: CausalSpectralGate().process(c["mix"]),
               "oracle_noncausal": lambda c: oracle_irm_waveform(c["clean"], c["noise"], c["mix"])}
    if a.gen15:
        systems["gen15_causal"] = lambda c, r=load_gen15(a.gen15): r(c["mix"])
    rows = []
    for ci, c in enumerate(crops):
        for name, fn in systems.items():
            est = fn(c)
            rows.append({"crop": ci, "kind": c["kind"], "snr_db": c["snr_db"],
                         "spk": c["spk"], "system": name, **metrics_for(c["clean"], est)})
        print(f"crop {ci+1}/{len(crops)} {c['kind']} elapsed={time.time()-t0:.0f}s", flush=True)
    summary = {}
    base = {(r["crop"]): r for r in rows if r["system"] == "unproc"}
    for name in systems:
        summary[name] = {}
        for kind in sorted({r["kind"] for r in rows}):
            sel = [r for r in rows if r["system"] == name and r["kind"] == kind]
            e = {"n": len(sel),
                 "sisdr": float(np.nanmean([r["sisdr"] for r in sel])),
                 "stoi": float(np.nanmean([r["stoi"] for r in sel])),
                 "ace_env_corr": float(np.nanmean([r["ace_env_corr"] for r in sel])),
                 "ace_electro_corr": float(np.nanmean([r["ace_electro_corr"] for r in sel])),
                 "max_peak": float(np.max([r["peak"] for r in sel]))}
            for k, dk in [("sisdr", "d_sisdr"), ("ace_env_corr", "d_ace_env_corr"),
                          ("ace_electro_corr", "d_ace_electro_corr"), ("stoi", "d_stoi")]:
                e[dk] = bootstrap_ci([r[k] - base[r["crop"]][k] for r in sel])
            summary[name][kind] = e
    verdicts = evaluate_go_nogo(summary)
    # Example listening files: first babble 0 dB crop, raw + vocoded, limited.
    import soundfile as sf
    ex = next(c for c in crops if c["kind"].startswith("babble") and c["snr_db"] == 0.0)
    (HERE / "examples").mkdir(exist_ok=True)
    sf.write(HERE / "examples" / "babble0db_clean.wav", limit_signal(ex["clean"]), FS)
    sf.write(HERE / "examples" / "babble0db_mix.wav", limit_signal(ex["mix"]), FS)
    for name, fn in systems.items():
        est = limit_signal(fn(ex)) if name != "unproc" else limit_signal(ex["mix"])
        sf.write(HERE / "examples" / f"babble0db_{name}.wav", est, FS)
        sf.write(HERE / "examples" / f"babble0db_{name}_vocoded.wav", vocode(est, seed=1), FS)
    sf.write(HERE / "examples" / "babble0db_clean_vocoded.wav", vocode(limit_signal(ex["clean"]), seed=1), FS)
    payload = {"meta": {"n_per_cell": a.n_per_cell, "n_crops": len(crops), "gen15": a.gen15,
                        "seconds": round(time.time() - t0, 1),
                        "claim": "T0 in-silico only; no listener or implant claim"},
               "summary": summary, "go_nogo": verdicts, "rows": rows}
    Path(a.out).write_text(json.dumps(payload, indent=1))
    print(json.dumps({"summary": summary, "go_nogo": verdicts}, indent=1))
    print(f"BENCH DONE {time.time()-t0:.0f}s -> {a.out}")


if __name__ == "__main__":
    main()
