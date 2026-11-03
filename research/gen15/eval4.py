"""Gen15 eval: causal TasNet vs unprocessed vs oracle-IRM waveform (T0).

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
T0 in-silico ONLY. No listener claim.

Eval crops are Gen13's protocol verbatim (gen13/eval2.py: RNG 777,
same draw order via train4's copied data functions): held-out targets
1988/1993, conditions babble-heldout-spk (interferers 8842/8297, k=3),
ssn, white-heldout (held-out CLASS), quiet; SNR -5/0/+5/+10 dB;
--n-per-cell 8 -> 32 crops/condition + 8 quiet, 4 s crops.

Systems:
  * unproc: the mixture waveform itself (NOTE vs Gen13: Gen13's
    unprocessed passed through its noisy-phase mel-OLA identity path;
    here there is no such path, the mixture is scored directly).
  * causal: model_causal.CausalTasNetEnh, raw output shifted back by
    DELAY=63 samples (its stated content delay / algorithmic latency
    <=94 samples = 5.88 ms) before scoring.
  * oracleIRM: STFT ideal ratio mask sqrt(|C|^2/(|C|^2+|N|^2))
    (n_fft 512, hop 128, Hann, centered) applied to the mixture STFT,
    iSTFT. Uses true clean/noise and centered framing => NON-causal
    oracle upper bound for magnitude-masking only, not a competitor.

Metrics per crop: SI-SDR / STOI / PESQ-WB on samples [256:-256] (Gen13
waveform trim), plus quiet RMS ratio (est/clean, level-identity check).
Paired bootstrap 95% CIs (2000 resamples, seed 13, as Gen13) for
causal-unproc and oracle-unproc differences. CIs cover eval-crop
sampling only (2 held-out speakers), not a speaker population.
Causality suffix-invariance is re-run on the loaded weights.

Run: /tmp/gen9env/bin/python research/gen15/eval4.py --n-per-cell 8
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from model_causal import (CausalTasNetEnh, audit_causality, receptive_field,  # noqa: E402
                          suffix_invariance_test, undelay)
from train4 import TEST_BABBLE_SPK, TEST_SPK, babble, crop, load_pool, make_ssn_fast, rms  # noqa: E402
from pystoi import stoi as _stoi
from pesq import pesq as _pesq

FS = 16000


def si_sdr(ref, est):
    ref = np.asarray(ref, dtype=np.float64); est = np.asarray(est, dtype=np.float64)
    ref = ref - ref.mean(); est = est - est.mean()
    alpha = np.dot(est, ref) / (np.dot(ref, ref) + 1e-12); proj = alpha * ref
    return float(10 * np.log10((np.dot(proj, proj) + 1e-12) / (np.dot(est - proj, est - proj) + 1e-12)))


def stoi_v(ref, est):
    try: return float(_stoi(ref.astype(np.float64), est.astype(np.float64), FS, extended=False))
    except Exception: return float("nan")


def pesq_v(ref, est):
    try: return float(_pesq(FS, ref.astype(np.float64), est.astype(np.float64), "wb"))
    except Exception: return float("nan")


def oracle_irm_waveform(clean, noise, mix):
    n_fft, hop = 512, 128
    win = torch.hann_window(n_fft)
    def stft(x):
        return torch.stft(torch.from_numpy(np.asarray(x, dtype=np.float32)),
                          n_fft, hop, window=win, return_complex=True)
    C, N, M = stft(clean), stft(noise), stft(mix)
    mask = torch.sqrt(C.abs() ** 2 / (C.abs() ** 2 + N.abs() ** 2 + 1e-12))
    y = torch.istft(M * mask, n_fft, hop, window=win, length=len(mix))
    return y.numpy().astype(np.float32)


def build_eval_crops(pool, n_per_cell):
    """Copied from gen13/eval2.py (RNG 777, same draw order)."""
    rng = np.random.default_rng(777)
    SEG = 4 * FS
    crops = []
    for kind in ["babble-heldout-spk", "ssn", "white-heldout", "quiet"]:
        snrs = [999.0] if kind == "quiet" else [-5.0, 0.0, 5.0, 10.0]
        for snr in snrs:
            for i in range(n_per_cell):
                spk = TEST_SPK[i % len(TEST_SPK)]
                clean = crop(rng, pool[spk][rng.integers(0, len(pool[spk]))], SEG)
                clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
                if kind == "quiet":
                    noise = np.zeros_like(clean)
                elif kind.startswith("babble"):
                    noise = babble(rng, pool, TEST_BABBLE_SPK, n=SEG)
                elif kind == "ssn":
                    noise = np.concatenate([make_ssn_fast(rng, SEG // 2), make_ssn_fast(rng, SEG - SEG // 2)])
                else:
                    noise = rng.standard_normal(SEG).astype(np.float32)
                if kind != "quiet":
                    noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                crops.append({"kind": kind, "snr_db": float(snr), "spk": spk,
                              "clean": clean, "noise": noise, "mix": (clean + noise).astype(np.float32)})
    return crops


def bootstrap_ci(values, rng, reps=2000):
    v = np.asarray(values, dtype=np.float64); v = v[np.isfinite(v)]
    if len(v) == 0:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    idx = rng.integers(0, len(v), size=(reps, len(v)))
    means = v[idx].mean(axis=1)
    return {"mean": float(v.mean()), "ci_lo": float(np.percentile(means, 2.5)),
            "ci_hi": float(np.percentile(means, 97.5)), "n": int(len(v))}


DIFFS = {"d_sisdr": ("sisdr_causal", "sisdr_unproc"),
         "d_stoi": ("stoi_causal", "stoi_unproc"),
         "d_pesq": ("pesq_causal", "pesq_unproc"),
         "d_sisdr_oracle": ("sisdr_oracleIRM", "sisdr_unproc"),
         "d_stoi_oracle": ("stoi_oracleIRM", "stoi_unproc"),
         "d_pesq_oracle": ("pesq_oracleIRM", "pesq_unproc")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default=str(HERE / "weights" / "causal_seed20261115.pt"))
    ap.add_argument("--n-per-cell", type=int, default=8)
    ap.add_argument("--out", default=str(HERE / "eval_results.json"))
    a = ap.parse_args()
    wp = Path(a.weights)
    ckpt = torch.load(wp, map_location="cpu", weights_only=False)
    model = CausalTasNetEnh(); model.load_state_dict(ckpt["state_dict"]); model.eval()
    bad = audit_causality(model); assert not bad, bad
    caus = suffix_invariance_test(model, seed=2)
    for r in caus:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated: {r}"
    print(f"weights={wp} steps={ckpt.get('steps')} seed={ckpt.get('seed')}", flush=True)
    print(f"causality on loaded weights: {caus}", flush=True)
    pool = load_pool(TEST_SPK + TEST_BABBLE_SPK)
    crops = build_eval_crops(pool, a.n_per_cell)
    print(f"eval crops: {len(crops)}", flush=True)
    rows = []; t0 = time.time()
    tr = lambda v: v[256:-256]  # noqa: E731
    with torch.no_grad():
        for c in crops:
            clean, noise, mix = c["clean"], c["noise"], c["mix"]
            est_raw = model(torch.from_numpy(mix[None].astype(np.float32)))[0].numpy()
            est = undelay(est_raw).astype(np.float32)
            ora = oracle_irm_waveform(clean, noise, mix)
            rows.append({"kind": c["kind"], "snr_db": c["snr_db"], "spk": c["spk"],
                         "sisdr_unproc": si_sdr(tr(clean), tr(mix)),
                         "sisdr_causal": si_sdr(tr(clean), tr(est)),
                         "sisdr_oracleIRM": si_sdr(tr(clean), tr(ora)),
                         "stoi_unproc": stoi_v(tr(clean), tr(mix)),
                         "stoi_causal": stoi_v(tr(clean), tr(est)),
                         "stoi_oracleIRM": stoi_v(tr(clean), tr(ora)),
                         "pesq_unproc": pesq_v(tr(clean), tr(mix)),
                         "pesq_causal": pesq_v(tr(clean), tr(est)),
                         "pesq_oracleIRM": pesq_v(tr(clean), tr(ora)),
                         "quiet_rms_ratio": float(rms(est) / (rms(clean) + 1e-12))})
    rng = np.random.default_rng(13)
    summary = {}
    for kind in sorted(set(r["kind"] for r in rows)) + ["ALL-NOISY"]:
        sel = [r for r in rows if r["kind"] != "quiet"] if kind == "ALL-NOISY" \
            else [r for r in rows if r["kind"] == kind]
        entry = {"n_crops": len(sel)}
        for name, (x, y) in DIFFS.items():
            entry[name] = bootstrap_ci([r[x] - r[y] for r in sel], rng)
        for k in ["sisdr_unproc", "sisdr_causal", "sisdr_oracleIRM",
                  "stoi_unproc", "stoi_causal", "stoi_oracleIRM",
                  "pesq_unproc", "pesq_causal", "pesq_oracleIRM", "quiet_rms_ratio"]:
            entry[k] = float(np.nanmean([r[k] for r in sel]))
        summary[kind] = entry
    out = {"meta": {"weights": str(wp), "sha256": hashlib.sha256(wp.read_bytes()).hexdigest(),
                    "steps": ckpt.get("steps"), "seed": ckpt.get("seed"),
                    "params": model.count_parameters(),
                    "receptive_field": receptive_field(), "causality": caus},
           "summary": summary, "rows": rows}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps(summary, indent=1))
    print(f"EVAL DONE {time.time()-t0:.0f}s -> {a.out}")


if __name__ == "__main__":
    main()
