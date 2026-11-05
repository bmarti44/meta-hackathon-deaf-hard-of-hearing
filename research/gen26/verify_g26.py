"""Gen26 artifact check: inputs match the manifest and the saved weights equal the registered midpoint bit-exactly."""
import argparse, hashlib, json, sys
from pathlib import Path
import torch
HERE = Path(__file__).resolve().parent; R = HERE.parent; ROOT = R.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=17); a = ap.parse_args(); seed = 20261100 + a.seed
man = json.loads((HERE / "input_manifest.json").read_text())
ck = torch.load(HERE / "weights" / f"mid50_seed{seed}.pt", map_location="cpu", weights_only=False)
ok = len(ck["inputs"]) == 2 and all(man.get(i["path"]) == i["sha256"] == sha(ROOT / i["path"]) for i in ck["inputs"])
sds = [torch.load(ROOT / i["path"], map_location="cpu", weights_only=False)["state_dict"] for i in ck["inputs"]]
exp = {k: (0.5 * sds[0][k].float() + 0.5 * sds[1][k].float()).to(sds[0][k].dtype) for k in sds[0]}
ok2 = set(exp) == set(ck["state_dict"]) and all(torch.equal(exp[k], ck["state_dict"][k]) for k in exp)
print(f"inputs match manifest: {ok}; weights == registered midpoint (bit-exact): {ok2}")
print("G26 ARTIFACT " + ("PASS" if ok and ok2 else "FAIL")); sys.exit(0 if ok and ok2 else 1)
