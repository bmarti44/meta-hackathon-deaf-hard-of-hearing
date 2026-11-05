"""Gen26: fixed weight-space midpoint, 0.5 x Gen19 + 0.5 x Gen21-R48, per seed (no training, no alpha search).

Gen21-R48 is Gen19's own continuation (Gen19 final + a 24k restart), so the two share a
trajectory and their weights live in compatible coordinates (WiSE-FT-style). Registered in
research/gen26/prereg.md and judged under research/screen_v2/ (16-voice panel v2).

Guards: both inputs must match research/gen26/input_manifest.json; R48's recorded
parent_sha256 must equal this seed's Gen19 final; schemas must match; exact causality is
re-verified; CPU only; no overwrite without --force.
Usage: /tmp/gen9env/bin/python research/gen26/interp.py --seed 17
"""
import argparse, hashlib, json, sys
from pathlib import Path
import torch

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / "gen15"))
from model_causal import CausalTasNetEnh, suffix_invariance_test  # noqa: E402

ALPHA = 0.5  # registered; never swept
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=17); ap.add_argument("--force", action="store_true")
    a = ap.parse_args(); seed = 20261100 + a.seed
    man = json.loads((HERE / "input_manifest.json").read_text())
    pg, pr = R / "gen19" / "weights" / f"causal_seed{seed}.pt", R / "gen21" / "weights" / f"r48_seed{seed}.pt"
    for p in (pg, pr):
        rel = str(p.relative_to(R.parent))
        if man.get(rel) != sha(p):
            raise SystemExit(f"input {rel} does not match the registered manifest")
    g, r = (torch.load(p, map_location="cpu", weights_only=False) for p in (pg, pr))
    if r.get("parent_sha256") != sha(pg):
        raise SystemExit("R48 is not this seed's Gen19 continuation (parent_sha256 mismatch)")
    if set(g["state_dict"]) != set(r["state_dict"]) or any(g["state_dict"][k].shape != r["state_dict"][k].shape for k in g["state_dict"]):
        raise SystemExit("schema mismatch")
    mid = {k: ((1 - ALPHA) * g["state_dict"][k].float() + ALPHA * r["state_dict"][k].float()).to(g["state_dict"][k].dtype) for k in g["state_dict"]}
    model = CausalTasNetEnh(); model.load_state_dict(mid); model.eval()
    for t in suffix_invariance_test(model, seed=1):
        if t["max_diff_prefix_P"] != 0.0:
            raise SystemExit(f"causality violated: {t}")
    out = HERE / "weights" / f"mid50_seed{seed}.pt"
    if out.exists() and not a.force:
        raise SystemExit(f"REFUSED: {out} exists")
    meta = {k: v for k, v in g.items() if k != "state_dict"}
    meta.update({"gen": "gen26", "method": f"{1-ALPHA} x Gen19 + {ALPHA} x Gen21-R48", "alpha": ALPHA,
                 "inputs": [{"path": str(p.relative_to(R.parent)), "sha256": sha(p)} for p in (pg, pr)]})
    torch.save({"state_dict": model.state_dict(), **meta}, out)
    print(f"DONE seed {seed} mid50 sha {sha(out)}")


if __name__ == "__main__":
    main()
