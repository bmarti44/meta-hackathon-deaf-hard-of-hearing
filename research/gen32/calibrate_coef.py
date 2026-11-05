"""Gen32 coefficient scale check (training-distribution batches only; no VAL or screen material).

Measures r = mean_t((f_FT - f_19)^2) / (mean_t(f_19^2) + 1e-8) on DRY training items (dry noisy + dry quiet), where FT
is Gen31's unregularised room fine-tune and 19 is its Gen19 parent, i.e. how far an unpenalised fine-tune drifts on
dry input. It also reports the mean SI-SDR loss on the same items. The registered coefficient rule uses only r.

Batches come from train19.make_batch(room="aug50") with main RNG seed 20261132 and augmentation RNG [20261132, 27]
(a fresh stream, not Gen19's handoff stream), 100 batches x 8 items, on the training speakers and training RIR split.
"""
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np, torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    t19 = load("train19_cal", HERE / "train19.py")
    from model_causal import CausalTasNetEnh, delay_target
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    paths = {"gen19": REPO / "research/gen19/weights/causal_seed20261117.pt",
             "ft": REPO / "research/gen31/weights/ft_aug50_seed20261117.pt"}
    m = {}
    for k, p in paths.items():
        net = CausalTasNetEnh(); ck = torch.load(p, map_location="cpu", weights_only=False)
        net.load_state_dict(ck["state_dict"]); m[k] = net.to(dev).eval()
    root = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
    spk = sorted(d.name for d in root.iterdir() if d.is_dir())
    pool = t19.t13.load_pool(spk, root=root)
    bank = t19.rirbank.Bank(t19.DEFAULT_MANIFEST, splits=("train",), nfft=t19.NFFT)
    rng, ra = np.random.default_rng(20261132), np.random.default_rng([20261132, 27])
    rs, ls = [], []
    with torch.no_grad():
        for _ in range(100):
            b = t19.make_batch(rng, pool, spk, batch=8, room="aug50", aug_rng=ra, bank=bank)
            mask = torch.tensor([x["cond"] != "rev_noisy" for x in b[5]])
            if not mask.any():
                continue
            mix, clean = b[2].to(dev), b[0].to(dev)
            f19, fft = m["gen19"](mix), m["ft"](mix)
            r = ((fft - f19) ** 2).mean(-1) / ((f19 ** 2).mean(-1) + 1e-8)
            rs += r.cpu()[mask].tolist()
            ls += t19.t13.LOSSES["sisdr"](delay_target(clean), fft).cpu()[mask].tolist()
    rec = {"n_dry_items": len(rs), "r_mean": float(np.mean(rs)), "r_median": float(np.median(rs)),
           "r_p90": float(np.percentile(rs, 90)), "neg_sisdr_mean_db": float(np.mean(ls)),
           "coef100_times_r_mean": 100 * float(np.mean(rs)),
           "ft_sha256": hashlib.sha256(paths["ft"].read_bytes()).hexdigest(),
           "gen19_sha256": hashlib.sha256(paths["gen19"].read_bytes()).hexdigest()}
    (HERE / "coef_calibration.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    sys.path.insert(0, str(REPO / "research/gen15"))
    main()
