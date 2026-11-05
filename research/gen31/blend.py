"""Gen31 WiSE-FT step 2 of 3: weight-space blends of Gen19 and its room fine-tune.

theta(a) = (1 - a) * theta_Gen19 + a * theta_FT for every tensor (all 181 are float32 parameters; the model
has no buffers), computed in float64 and stored as float32. a = 0 reproduces Gen19 bit-for-bit and a = 1
reproduces the fine-tune bit-for-bit (tested). The registered grid is a in {0.1, 0.2, ..., 1.0}.

Usage:
  python research/gen31/blend.py --base <gen19.pt> --ft <ft.pt> --outdir research/gen31/weights/blends
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import torch

GRID = tuple(round(0.1 * i, 1) for i in range(1, 11))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_sd(p):
    ck = torch.load(p, map_location="cpu", weights_only=False)
    return ck["state_dict"] if "state_dict" in ck else ck


def blend_sd(sd0, sd1, a):
    assert sd0.keys() == sd1.keys(), "state dict keys differ"
    out = {}
    for k in sd0:
        x0, x1 = sd0[k], sd1[k]
        assert x0.shape == x1.shape and x0.dtype == x1.dtype == torch.float32, k
        if a == 0.0:
            out[k] = x0.clone()
        elif a == 1.0:
            out[k] = x1.clone()
        else:
            out[k] = ((1.0 - a) * x0.double() + a * x1.double()).float()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--ft", required=True)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    sd0, sd1 = load_sd(a.base), load_sd(a.ft)
    b_sha, f_sha = sha(a.base), sha(a.ft)
    index = {"base": a.base, "base_sha256": b_sha, "ft": a.ft, "ft_sha256": f_sha, "grid": list(GRID), "blends": {}}
    for al in GRID:
        p = out / f"blend_a{int(round(al * 100)):03d}.pt"
        torch.save({"state_dict": blend_sd(sd0, sd1, al), "mode": "wiseft_blend", "alpha": al,
                    "base_sha256": b_sha, "ft_sha256": f_sha, "seed": torch.load(a.ft, map_location="cpu", weights_only=False).get("seed")}, p)
        index["blends"][f"{al:.1f}"] = {"path": str(p), "sha256": sha(p)}
        print(f"alpha={al:.1f} -> {p} sha256={index['blends'][f'{al:.1f}']['sha256'][:12]}", flush=True)
    (out / "index.json").write_text(json.dumps(index, indent=1))
    print(f"WROTE {out / 'index.json'}")


if __name__ == "__main__":
    main()
