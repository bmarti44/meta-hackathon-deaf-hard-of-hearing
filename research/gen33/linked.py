"""Gen33 linked two-ear inference for the frozen causal enhancer (Astra's Gen32 review, choice c).

The mono model (research/gen15/model_causal.py) is: w = relu(encoder(x)); mask m = mask_net(w); out = decoder(w * m).
Linked mode computes ONE mask from both ears and applies it to each ear's own encoding:

    zL = relu(encoder(L)), zR = relu(encoder(R))
    m  = mask_net((zL + zR) / 2)
    yL = decoder(zL * m),  yR = decoder(zR * m)

with the model's own padding, cropping and fixed delay. No weights change. Identical ears reproduce the mono output
bit-for-bit ((z + z) / 2 == z exactly in IEEE arithmetic); swapping the ears swaps the outputs; it stays causal.
A learned-basis shared mask does not mathematically guarantee preserved acoustic ILD/ITD (Astra), so the cues are measured.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
from model_causal import CausalTasNetEnh, ENC_L, undelay  # noqa: E402


def _encode(model, x):
    return F.relu(model.encoder(F.pad(x, (ENC_L - 1, 0))))


def _mask(model, w):
    y = model.bott(model.bott_norm(w))
    skip_sum = None
    for blk in model.blocks:
        y, sk = blk(y)
        skip_sum = sk if skip_sum is None else skip_sum + sk
    return torch.sigmoid(model.mask_head(model.mask_act(model.mask_norm(skip_sum))))


def _decode(model, w, t_in):
    out = model.decoder(w)
    out = out[..., :t_in] if out.shape[-1] >= t_in else F.pad(out, (0, t_in - out.shape[-1]))
    return out.squeeze(1)


def forward_linked(model, xL, xR):
    """xL, xR: (B, T) tensors. Returns (yL, yR), each (B, T), delayed exactly like model(x)."""
    if xL.dim() == 2:
        xL, xR = xL.unsqueeze(1), xR.unsqueeze(1)
    t_in = xL.shape[-1]
    zL, zR = _encode(model, xL), _encode(model, xR)
    m = _mask(model, (zL + zR) / 2)
    return _decode(model, zL * m, t_in), _decode(model, zR * m, t_in)


def forward_mono(model, x):
    """The model's own forward, rebuilt from the same parts (used to test parity with model(x))."""
    if x.dim() == 2:
        x = x.unsqueeze(1)
    t_in = x.shape[-1]
    w = _encode(model, x)
    return _decode(model, w * _mask(model, w), t_in)


def load(path):
    m = CausalTasNetEnh()
    ck = torch.load(path, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["state_dict"] if isinstance(ck, dict) and "state_dict" in ck else ck)
    return m.eval()


def pair_fn(path, mode):
    """Numpy stereo processor (L, R) -> (oL, oR), undelayed like bench.load_gen15. mode: 'independent' | 'linked'."""
    model = load(path)

    def run(L, R):
        tl = torch.from_numpy(np.asarray(L)[None].astype(np.float32))
        tr = torch.from_numpy(np.asarray(R)[None].astype(np.float32))
        with torch.no_grad():
            if mode == "independent":
                yL, yR = model(tl)[0].numpy(), model(tr)[0].numpy()
            elif mode == "linked":
                a, b = forward_linked(model, tl, tr)
                yL, yR = a[0].numpy(), b[0].numpy()
            else:
                raise ValueError(mode)
        return undelay(yL).astype(np.float32), undelay(yR).astype(np.float32)
    return run
