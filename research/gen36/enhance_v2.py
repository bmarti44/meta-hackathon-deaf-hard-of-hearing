"""Gen36 candidate inference entry point (output-contract repair). NOT published; for the registered audit only.

Differences from the published enhance.py (research/gen35/published/enhance.py), and nothing else:
 1. Output contract per checkpoint, bound to the weights file's sha256 (OUTPUT_CONTRACT below): the decoder bias is
    subtracted and the registered polarity applied, right after the fixed-delay removal and before any level step.
    An unregistered weights file is refused.
 2. Level restoration uses the corrected (DC-free) output, so the level budget is not spent on a DC offset.
 3. One linear gain, capped by headroom AFTER the final resampling: out *= min(1, CEIL / max|out|) with
    CEIL = 10**(-1/20) (-1 dBFS). The output is never hard-clipped by this code; writers may still clip if given an
    input already beyond full scale (labelled overload stress inputs are reported separately).
Steps otherwise as published: mono mix-down, resample to 16 kHz, whole-file RMS 0.14 input gain (offline), delay flush.
"""
from __future__ import annotations
import hashlib, os, sys
from math import gcd
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "gen35", "published"))
from model_causal import DELAY, FS, CausalTasNetEnh  # noqa: E402  (the published model file)

MIX_RMS = 0.14
CEIL = 10 ** (-1 / 20)
# sha256 of the PUBLISHED safetensors files -> (polarity, decoder bias), audited against the training checkpoints
OUTPUT_CONTRACT = {}   # filled by contract.py at import (see bind_contract); empty means every file is refused


def bind_contract(table):
    OUTPUT_CONTRACT.clear(); OUTPUT_CONTRACT.update(table)


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_model(path):
    from safetensors.torch import load_file
    h = _sha(path)
    if h not in OUTPUT_CONTRACT:
        raise SystemExit(f"REFUSED: {path} sha256 {h} has no registered output contract")
    m = CausalTasNetEnh(); m.load_state_dict(load_file(path), strict=True); m.eval()
    pol, bias = OUTPUT_CONTRACT[h]
    if abs(float(m.decoder.bias[0]) - bias) > 1e-7:
        raise SystemExit(f"REFUSED: decoder bias in {path} does not match its registered contract")
    m._contract = (pol, bias)
    return m


def _resample(x, sr_in, sr_out):
    if sr_in == sr_out:
        return x
    from scipy.signal import resample_poly
    g = gcd(sr_in, sr_out)
    return resample_poly(x, sr_out // g, sr_in // g).astype(np.float32)


def enhance(audio, sr, model):
    """Returns (mono float32 output at sr, info dict with the headroom gain applied)."""
    x = np.asarray(audio, dtype=np.float32)
    if x.ndim == 2:
        x = x.mean(axis=1)
    n_in = len(x)
    x16 = _resample(x, sr, FS)
    level = float(np.sqrt(np.mean(x16.astype(np.float64) ** 2)))
    if level < 1e-6:
        return np.zeros(n_in, dtype=np.float32), {"headroom_gain": 1.0, "silence": True}
    n16 = len(x16)
    inp = np.concatenate([x16 * (MIX_RMS / level), np.zeros(DELAY, np.float32)])
    with torch.no_grad():
        y = model(torch.from_numpy(inp)[None])[0].numpy().astype(np.float64)
    pol, bias = model._contract
    y16 = pol * (y[DELAY:DELAY + n16] - bias)                    # output contract, before any level step
    y16 = y16 * (level / (float(np.sqrt(np.mean(y16 ** 2))) + 1e-12))
    out = _resample(y16.astype(np.float32), FS, sr).astype(np.float64)
    out = out[:n_in] if len(out) >= n_in else np.pad(out, (0, n_in - len(out)))
    peak = float(np.max(np.abs(out))) if len(out) else 0.0
    g = min(1.0, CEIL / peak) if peak > 0 else 1.0               # one linear gain, capped by headroom after resampling
    return (out * g).astype(np.float32), {"headroom_gain": g, "silence": False}
