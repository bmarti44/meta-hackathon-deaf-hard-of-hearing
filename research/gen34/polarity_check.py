"""Gen34 follow-up evidence: output polarity (signed projection alpha of the undelayed output onto the clean input,
target-only) for every committed Gen19 checkpoint (all steps, seeds 17/18/19), Gen31's fine-tune and Gen32, plus each
final checkpoint's decoder bias. Input: one LibriSpeech dev-clean utterance of VAL speaker 5536 (never a training
speaker), first 4 s, RMS 0.1; projection on [256:-256]. Usage: python research/gen34/polarity_check.py"""
from __future__ import annotations
import glob, hashlib, json, pathlib, re, sys
import numpy as np, soundfile as sf, torch
HERE = pathlib.Path(__file__).resolve().parent; R = HERE.parent
sys.path.insert(0, str(R / "gen33")); sys.path.insert(0, str(R / "gen15"))
import linked  # noqa: E402

f = sorted(pathlib.Path("/tmp/gen12dl/LibriSpeech/dev-clean/5536").rglob("*.flac"))[0]
x, fs = sf.read(f); x = x[: fs * 4]; x = (x / np.sqrt(np.mean(x ** 2)) * 0.1).astype(np.float32)
cks = sorted(glob.glob(str(R / "gen19/weights/causal_seed*.pt"))) + [str(R / "gen31/weights/ft_aug50_seed20261117.pt"),
                                                                    str(R / "gen32/weights/wiseftpd_seed20261117.pt")]
out = {"input": f.name, "rows": []}
for ck in cks:
    fn = linked.pair_fn(ck, "independent"); o, _ = fn(x, x)
    o = np.asarray(o, float)[256:-256]; r = x.astype(float)[256:-256]
    m = re.search(r"seed(\d+)(?:_step(\d+))?", ck)
    sd = torch.load(ck, map_location="cpu", weights_only=False)
    bias = float((sd["state_dict"] if "state_dict" in sd else sd)["decoder.bias"][0])
    out["rows"].append({"ckpt": str(pathlib.Path(ck).relative_to(R.parent)), "seed": int(m.group(1)),
                        "step": int(m.group(2)) if m.group(2) else None, "alpha": float(np.dot(o, r) / np.dot(r, r)),
                        "decoder_bias": bias, "output_mean": float(np.mean(o))})
fin = [r for r in out["rows"] if r["step"] is None]
out["summary"] = {r["ckpt"]: {"alpha": round(r["alpha"], 3), "decoder_bias": round(r["decoder_bias"], 6), "output_mean": round(r["output_mean"], 4)} for r in fin}
by = {}
for r in out["rows"]:
    if r["step"] is not None and "gen19" in r["ckpt"]:
        by.setdefault(r["seed"], []).append(np.sign(r["alpha"]))
out["sign_constant_from_step_500"] = {s: bool(len(set(v)) == 1) for s, v in by.items()}
(HERE / "polarity_check.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["summary"], indent=1)); print(out["sign_constant_from_step_500"])
