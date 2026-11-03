"""Gen13 eval: held-out objective metrics + ACE consumption + bootstrap CIs.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
T0 in-silico ONLY. No listener claim. ACE-sim numbers are NOT listening
evidence (ace_sim.py models no perception).

Protocol (paired: identical eval crops for every seed and system):
  * Held-out target speakers 1988/1993; eval RNG 777 (as Gen12).
  * Conditions: babble-heldout-spk (SEEN class, interferers 8842/8297 held
    out), ssn (trained class), white-heldout (HELD-OUT noise class), quiet.
  * SNR -5/0/+5/+10 dB, 4 s crops, --n-per-cell per SNR (default 8 ->
    32 crops per noisy condition, 104 total incl. quiet).
  * Systems: unprocessed, J4 per weight file (one per training seed),
    oracle mel-IRM (upper bound of this masking representation only).

Metrics per crop:
  * Native envelope domain: mask-MSE vs IRM; log-envelope MAE (unproc/J4/oracle).
  * Waveform T0 (Gen12 comparability only): SI-SDR/STOI/PESQ-WB through the
    identical noisy-phase mel-gain OLA path as gen12/eval.py (code copied
    verbatim in spirit; not part of J4-A1, not how ACE consumes envelopes).
  * ACE consumption (ace_sim.py, envelope path, no waveform synthesis):
    22-ch envelope correlation vs clean (pre-selection), electrodogram
    correlation vs clean electrodogram (post 8-of-22), maxima-selection
    overlap vs clean, and channel-SNR (clean/noise components through the
    same mask) for unproc/J4/oracle.

Statistics: per-seed means per condition; paired bootstrap over eval crops
(2000 resamples, seeded 13, percentile 95% CI) for differences J4-unproc
(and oracle-unproc) on the headline metrics. Seed-mean rows average the
per-seed crop metrics first, then bootstrap the same way. CIs quantify
eval-crop sampling uncertainty only (2 held-out speakers; not a
speaker-population CI) -- stated in results.md.

Run: /tmp/gen9env/bin/python research/gen13/eval2.py --n-per-cell 8
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen11")); sys.path.insert(0, str(HERE))
from j4_model import EPS, FS, H, W, J4A1, frame_signal  # noqa: E402
from train2 import TEST_BABBLE_SPK, TEST_SPK, babble, crop, load_pool, make_ssn_fast, rms  # noqa: E402
from ace_sim import (ace_envelopes_from_mel, channel_snr_db, envelope_correlation,  # noqa: E402
                     maxima_overlap, mel_to_ace_matrix, n_of_m)
from pystoi import stoi as _stoi
from pesq import pesq as _pesq


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


@torch.no_grad()
def reconstruct(model, mix_1d, masks_2d):
    """Gen12 T0 waveform path, unchanged (see gen12/eval.py for rationale)."""
    x = torch.from_numpy(mix_1d[None].astype(np.float32))
    frames = frame_signal(x)[0]
    win = model.window; spec = torch.fft.rfft(frames * win, dim=-1)
    fb = model.filterbank; fbsum = fb.sum(dim=0, keepdim=True)
    gain = (masks_2d @ fb) / torch.clamp(fbsum, min=1e-8)
    gain = torch.where(fbsum > 1e-6, gain, masks_2d.mean(dim=1, keepdim=True).expand_as(gain))
    gain = torch.clamp(gain, 0, 1)
    masked = torch.fft.irfft(spec * gain, n=W, dim=-1)
    n = len(mix_1d); out = np.zeros(n); norm = np.zeros(n); w1 = win.numpy(); mf = masked.numpy()
    for j in range(mf.shape[0]):
        s = j * H; out[s:s + W] += mf[j]; norm[s:s + W] += w1
    ok = norm > 0.05; out[ok] /= norm[ok]; out[~ok] = 0.0
    return out.astype(np.float32)


def build_eval_crops(pool, n_per_cell):
    """Deterministic paired crop list (RNG 777, Gen12 draw order & SNRs)."""
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


@torch.no_grad()
def eval_one_model(model, tag, crops, w_ace):
    rows = []
    for c in crops:
        clean, noise, mix = c["clean"], c["noise"], c["mix"]
        ct = torch.from_numpy(clean[None]); nt = torch.from_numpy(noise[None]); mt = torch.from_numpy(mix[None])
        _, ec = model.extract_features(ct); _, en = model.extract_features(nt)
        _, mixenv = model.extract_features(mt)
        irm = torch.sqrt(ec ** 2 / (ec ** 2 + en ** 2 + EPS))
        masks, masked = model(mt)
        oracle_masked = irm * mixenv
        logmae = lambda e: float(torch.mean(torch.abs(torch.log(e + 1e-6) - torch.log(ec + 1e-6))))  # noqa: E731
        # ACE consumption (envelope path). Components: mask applied to the
        # clean / noise mel envelopes separately for channel-SNR.
        ace_ref = ace_envelopes_from_mel(ec[0], w_ace)
        def ace_block(sys_mel_env, sys_mask):  # noqa: E306
            e = ace_envelopes_from_mel(sys_mel_env, w_ace)
            cc = ace_envelopes_from_mel(sys_mask * ec[0], w_ace)
            nn_ = ace_envelopes_from_mel(sys_mask * en[0], w_ace)
            return {"env_corr": envelope_correlation(e, ace_ref),
                    "electro_corr": envelope_correlation(n_of_m(e), n_of_m(ace_ref)),
                    "maxima_overlap": maxima_overlap(e, ace_ref),
                    "chan_snr_db": channel_snr_db(cc, nn_)}
        ace_un = ace_block(mixenv[0], torch.ones_like(masks[0]))
        ace_j4 = ace_block(masked[0], masks[0])
        ace_or = ace_block(oracle_masked[0], irm[0])
        # Waveform T0 (Gen12 comparability)
        wav_j4 = reconstruct(model, mix, masks[0]); wav_or = reconstruct(model, mix, irm[0])
        wav_un = reconstruct(model, mix, torch.ones_like(masks[0]))
        tr = lambda v: v[256:-256]  # noqa: E731
        rows.append({"system": tag, "kind": c["kind"], "snr_db": c["snr_db"], "spk": c["spk"],
                     "mask_mse": float(torch.mean((masks - irm) ** 2)),
                     "env_logMAE_unproc": logmae(mixenv), "env_logMAE_j4": logmae(masked),
                     "env_logMAE_oracleIRM": logmae(oracle_masked),
                     "sisdr_unprocOLA": si_sdr(tr(clean), tr(wav_un)), "sisdr_j4": si_sdr(tr(clean), tr(wav_j4)),
                     "sisdr_oracleIRM": si_sdr(tr(clean), tr(wav_or)),
                     "stoi_unprocOLA": stoi_v(tr(clean), tr(wav_un)), "stoi_j4": stoi_v(tr(clean), tr(wav_j4)),
                     "stoi_oracleIRM": stoi_v(tr(clean), tr(wav_or)),
                     "pesq_unprocOLA": pesq_v(tr(clean), tr(wav_un)), "pesq_j4": pesq_v(tr(clean), tr(wav_j4)),
                     "pesq_oracleIRM": pesq_v(tr(clean), tr(wav_or)),
                     **{f"ace_{k}_unproc": v for k, v in ace_un.items()},
                     **{f"ace_{k}_j4": v for k, v in ace_j4.items()},
                     **{f"ace_{k}_oracle": v for k, v in ace_or.items()}})
    return rows


# Headline paired differences (J4 - unproc); negative-is-better for logMAE (reported as improvement).
DIFFS = {"d_sisdr": ("sisdr_j4", "sisdr_unprocOLA"), "d_stoi": ("stoi_j4", "stoi_unprocOLA"),
         "d_pesq": ("pesq_j4", "pesq_unprocOLA"), "imp_logMAE": ("env_logMAE_unproc", "env_logMAE_j4"),
         "d_ace_envcorr": ("ace_env_corr_j4", "ace_env_corr_unproc"),
         "d_ace_electrocorr": ("ace_electro_corr_j4", "ace_electro_corr_unproc"),
         "d_ace_overlap": ("ace_maxima_overlap_j4", "ace_maxima_overlap_unproc"),
         "d_ace_chansnr": ("ace_chan_snr_db_j4", "ace_chan_snr_db_unproc")}


def bootstrap_ci(values, rng, reps=2000):
    v = np.asarray(values, dtype=np.float64); v = v[np.isfinite(v)]
    if len(v) == 0:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    idx = rng.integers(0, len(v), size=(reps, len(v)))
    means = v[idx].mean(axis=1)
    return {"mean": float(v.mean()), "ci_lo": float(np.percentile(means, 2.5)),
            "ci_hi": float(np.percentile(means, 97.5)), "n": int(len(v))}


def summarise(rows_by_system):
    rng = np.random.default_rng(13)
    out = {}
    systems = sorted(rows_by_system)
    kinds = sorted(set(r["kind"] for r in next(iter(rows_by_system.values()))))
    # seed-mean pseudo-system: average each metric across seeds per crop index
    if len(systems) > 1:
        base = rows_by_system[systems[0]]
        mean_rows = []
        numkeys = [k for k in base[0] if k not in ("system", "kind", "spk", "snr_db")]
        for i, r0 in enumerate(base):
            mr = {"system": "seed-mean", "kind": r0["kind"], "snr_db": r0["snr_db"], "spk": r0["spk"]}
            for k in numkeys:
                mr[k] = float(np.mean([rows_by_system[s][i][k] for s in systems]))
            mean_rows.append(mr)
        rows_by_system = dict(rows_by_system); rows_by_system["seed-mean"] = mean_rows
    for sysname, rows in rows_by_system.items():
        out[sysname] = {}
        for kind in kinds + ["ALL-NOISY"]:
            sel = [r for r in rows if r["kind"] != "quiet"] if kind == "ALL-NOISY" else [r for r in rows if r["kind"] == kind]
            if not sel:
                continue
            entry = {"n_crops": len(sel)}
            for name, (a, b) in DIFFS.items():
                entry[name] = bootstrap_ci([r[a] - r[b] for r in sel], rng)
            for k in ["mask_mse", "env_logMAE_unproc", "env_logMAE_j4", "env_logMAE_oracleIRM",
                      "sisdr_unprocOLA", "sisdr_j4", "sisdr_oracleIRM",
                      "ace_env_corr_unproc", "ace_env_corr_j4", "ace_env_corr_oracle",
                      "ace_chan_snr_db_unproc", "ace_chan_snr_db_j4", "ace_chan_snr_db_oracle",
                      "ace_maxima_overlap_unproc", "ace_maxima_overlap_j4", "ace_maxima_overlap_oracle"]:
                entry[k] = float(np.nanmean([r[k] for r in sel]))
            out[sysname][kind] = entry
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", nargs="+", default=None)
    ap.add_argument("--n-per-cell", type=int, default=8)
    ap.add_argument("--out", default=str(HERE / "eval_results.json"))
    a = ap.parse_args()
    weight_paths = [Path(p) for p in a.weights] if a.weights else sorted((HERE / "weights").glob("j4_seed*.pt"))
    if not weight_paths:
        raise FileNotFoundError("no weight files (train2.py first)")
    print(f"weights: {[str(p) for p in weight_paths]}", flush=True)
    pool = load_pool(TEST_SPK + TEST_BABBLE_SPK)
    crops = build_eval_crops(pool, a.n_per_cell)
    print(f"eval crops: {len(crops)} (paired across seeds/systems)", flush=True)
    proto = J4A1(); w_ace = mel_to_ace_matrix(proto.filterbank)
    rows_by_system = {}; metas = {}
    t0 = time.time()
    for wp in weight_paths:
        ckpt = torch.load(wp, map_location="cpu", weights_only=False)
        tag = f"seed{ckpt.get('seed', wp.stem)}"
        model = J4A1(); model.load_state_dict(ckpt["state_dict"]); model.eval()
        metas[tag] = {"weights": str(wp), "sha256": hashlib.sha256(wp.read_bytes()).hexdigest(),
                      "steps": ckpt.get("steps"), "seed": ckpt.get("seed")}
        rows_by_system[tag] = eval_one_model(model, tag, crops, w_ace)
        print(f"done {tag} elapsed={time.time()-t0:.0f}s", flush=True)
    summary = summarise(rows_by_system)
    all_rows = [r for rows in rows_by_system.values() for r in rows]
    Path(a.out).write_text(json.dumps({"metas": metas, "summary": summary, "rows": all_rows}, indent=1))
    print(json.dumps(summary, indent=1))
    print(f"EVAL DONE {time.time()-t0:.0f}s -> {a.out}")


if __name__ == "__main__":
    main()
