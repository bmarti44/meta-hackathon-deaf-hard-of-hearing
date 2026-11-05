"""Gen25: weight-space checkpoint averaging (SWA-style), no training.

The registered recipe (prereg.md), fixed in advance with no selection:
- For one seed, take Gen19's checkpoints at steps 20000, 20500, ..., 23500
  plus the final 24000 checkpoint (9 checkpoints, the last 1/6 of the
  cosine schedule).
- Average every parameter tensor uniformly.
- Load the result into the same CausalTasNetEnh, re-verify exact causality,
  save it, and write a VAL log in the train-log format the Gen22 judge reads.

Parity guard: before averaging, the Gen19 final is re-evaluated on the VAL
panel with the same eval function and must reproduce the control VAL record
(the Gen21 R48 step-0 entry) item-for-item, so candidate and control VAL are
comparable.

Usage: /tmp/gen9env/bin/python research/gen25/swa.py --seed 17
"""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path

import torch

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / "gen15"))
from model_causal import CausalTasNetEnh, suffix_invariance_test  # noqa: E402

WINDOW = list(range(20000, 24000, 500)) + [24000]  # 9 checkpoints, registered


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ckpt(seed, step):
    return R / "gen19" / "weights" / (f"causal_seed{seed}.pt" if step == 24000 else f"causal_seed{seed}_step{step}.pt")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--device", default="cpu")
    a = ap.parse_args()
    seed = 20261100 + a.seed
    t11 = _load("train11_g25", R / "gen22" / "train11.py")
    panel = t11.build_val_panel()

    # parity guard: Gen19 final re-evaluated == control VAL record (R48 step 0)
    ctrl = json.loads((R / "gen21" / "weights" / f"train_log_r48_seed{seed}.json").read_text())
    c0 = [e for e in ctrl["val_log"] if e["lifetime_step"] == 24000][0]
    g19 = CausalTasNetEnh(); g19.load_state_dict(torch.load(ckpt(seed, 24000), map_location="cpu", weights_only=False)["state_dict"])
    _, items19 = t11.eval_val(g19.eval(), panel, a.device)
    key = lambda it: (it["idx"], it["spk"], it["snr"])  # noqa: E731
    want = {key(i): (i["d_sisdr"], i["d_stoi"]) for i in c0["items"]}
    got = {key(i): (i["d_sisdr"], i["d_stoi"]) for i in items19}
    worst = max(abs(want[k][0] - got[k][0]) for k in want)
    assert set(want) == set(got) and worst < 1e-4, f"VAL parity failed (max |diff| {worst})"
    print(f"VAL parity with control record: max |d_sisdr diff| {worst:.2e}")

    inputs, sds = [], []
    for st in WINDOW:
        p = ckpt(seed, st)
        d = torch.load(p, map_location="cpu", weights_only=False)
        assert d.get("steps") == st and d.get("seed") == seed, f"{p}: steps/seed {d.get('steps')}/{d.get('seed')}"
        sds.append(d["state_dict"]); inputs.append({"path": str(p.relative_to(R.parent)), "step": st, "sha256": sha(p)})
    avg = {k: torch.stack([sd[k].float() for sd in sds]).mean(0).to(sds[-1][k].dtype) for k in sds[-1]}

    model = CausalTasNetEnh(); model.load_state_dict(avg); model.eval()
    for r in suffix_invariance_test(model, seed=1):
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated: {r}"
    out = HERE / "weights" / f"swa9_seed{seed}.pt"; out.parent.mkdir(parents=True, exist_ok=True)
    base = torch.load(ckpt(seed, 24000), map_location="cpu", weights_only=False)
    meta = {k: v for k, v in base.items() if k != "state_dict"}
    meta.update({"gen": "gen25", "method": "uniform average of Gen19 checkpoints 20000..24000 (9)", "inputs": inputs})
    torch.save({"state_dict": model.state_dict(), **meta}, out)
    wsha = sha(out)

    v, items = t11.eval_val(model, panel, a.device)
    log = {"seed": seed, "mode": "swa", "loss": "sisdr", "steps": 24000, "lifetime_steps": 24000,
           "weights": str(out), "weights_sha256": wsha, "window": WINDOW, "inputs": inputs,
           "val_parity_max_abs_diff": worst,
           "val_log": [{"step": 24000, "lifetime_step": 24000, "val": v, "items": items}]}
    (HERE / "weights" / f"val_log_swa9_seed{seed}.json").write_text(json.dumps(log, indent=1))
    m5 = [i["d_sisdr"] for i in items if i["snr"] == -5.0]; c5 = [i["d_sisdr"] for i in c0["items"] if i["snr"] == -5.0]
    print(f"DONE seed {seed} swa9 sha {wsha[:12]}  VAL -5: {sum(m5)/len(m5):.4f} vs Gen19 {sum(c5)/len(c5):.4f}")


if __name__ == "__main__":
    main()
