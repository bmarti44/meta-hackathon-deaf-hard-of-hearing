"""Gen36 output-contract table: binds each PUBLISHED Hugging Face weights file (by sha256) to its registered polarity
and decoder bias, after verifying that its tensors equal the audited Gen19 training checkpoint exactly.

Published files (bmarti44/before-the-implant-causal-enhancer, downloaded to /tmp/gen36_release for the audit):
  model.safetensors  <- Gen19 seed 17;  seed18.safetensors <- seed 18;  seed19.safetensors <- seed 19.
Polarity comes from the frozen Gen35 table (research/gen35/repair.POLARITY, cross-checked with Gen34 evidence).
"""
from __future__ import annotations
import hashlib, sys
from pathlib import Path
import torch

HERE = Path(__file__).resolve().parent
R = HERE.parent
REPO = R.parent
sys.path.insert(0, str(R / "gen35"))
import repair as RP  # noqa: E402

RELEASE_DIR = Path("/tmp/gen36_release")
RELEASE = {"model.safetensors": 17, "seed18.safetensors": 18, "seed19.safetensors": 19}
RELEASE_SHA = {"model.safetensors": "3780d9f57148fb0fd3c4bc498bacb75377bb9bb83d6a4776a103f20e8bda1097",
               "seed18.safetensors": "36d56df87a13a7e096e3aebd3e5963a37d26f1de8d6c7534f40a224c352ee5f0",
               "seed19.safetensors": "9cf2c8fa65cc21a3719df50b8fd9e573a0ca2879ee27570dc04080e4d27c4c75"}
PUBLISHED_ENHANCE_SHA = "59b65cdaead7aca31d54fb73f1b1d2a7fcf6b3c1bb7feb07dcd42588d79611b5"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def build_table(release_dir=RELEASE_DIR):
    """Returns {release sha256: (polarity, bias)}; raises unless every release tensor equals the audited checkpoint."""
    from safetensors.torch import load_file
    pol = RP.registered_polarity()
    table = {}
    for name, seed in RELEASE.items():
        p = Path(release_dir) / name
        h = sha(p)
        if h != RELEASE_SHA[name]:
            raise SystemExit(f"REFUSED: {name} sha256 {h} != registered release {RELEASE_SHA[name]}")
        rel = load_file(str(p))
        ck = torch.load(RP.CKPTS[seed], map_location="cpu", weights_only=False)
        sd = ck["state_dict"] if "state_dict" in ck else ck
        if set(rel) != set(sd) or not all(torch.equal(rel[k].cpu(), sd[k].cpu()) for k in sd):
            raise SystemExit(f"REFUSED: {name} tensors differ from the audited {RP.CKPTS[seed].name}")
        table[h] = (pol[RP.sha(RP.CKPTS[seed])], float(sd["decoder.bias"][0]))
    if sha(Path(release_dir) / "enhance.py") != PUBLISHED_ENHANCE_SHA:
        raise SystemExit("REFUSED: published enhance.py differs from the audited snapshot")
    return table


if __name__ == "__main__":
    for h, (p, b) in build_table().items():
        print(h[:12], p, round(b, 6))
