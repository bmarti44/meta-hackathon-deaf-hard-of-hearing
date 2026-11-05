"""Gen36 candidate inference entry point (output-contract repair). NOT published; for the registered audit only.

Differences from the published enhance.py (research/gen35/published/enhance.py), and nothing else:
 1. Output contract per checkpoint, bound to the weights file's sha256 (OUTPUT_CONTRACT): right after the fixed-delay
    removal, before any level step, y <- polarity * (y - decoder_bias). An unregistered weights file is refused.
 2. Explicit DC handling, offline: after the final resampling to the input rate, the output's whole-file mean is
    removed. Levels are DC-free on both sides: the input level is the RMS of the mean-removed input.
 3. ONE final linear gain, after the final resampling: g = min(input_level / rms(out), CEIL / max|out|), CEIL = -1 dBFS.
    The output is never hard-clipped by this code.
The model input path is as published (mono mix-down, resample to 16 kHz, whole-file RMS 0.14 input gain, delay flush).
The model class is loaded from the PUBLISHED model_causal.py by file path (never from a module of the same name).
"""
from __future__ import annotations
import hashlib, importlib.util, os
from math import gcd
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLISHED_MODEL = os.path.normpath(os.path.join(HERE, "..", "gen35", "published", "model_causal.py"))
_spec = importlib.util.spec_from_file_location("gen36_published_model_causal", PUBLISHED_MODEL)
PM = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(PM)
DELAY, FS = PM.DELAY, PM.FS

MIX_RMS = 0.14
CEIL = 10 ** (-1 / 20)
OUTPUT_CONTRACT = {}


def bind_contract(table):
    OUTPUT_CONTRACT.clear(); OUTPUT_CONTRACT.update(table)


def model_module_sha():
    return hashlib.sha256(open(PUBLISHED_MODEL, "rb").read()).hexdigest()


def load_model(path):
    from safetensors.torch import load_file
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if h not in OUTPUT_CONTRACT:
        raise SystemExit(f"REFUSED: {path} sha256 {h} has no registered output contract")
    m = PM.CausalTasNetEnh(); m.load_state_dict(load_file(path), strict=True); m.eval()
    pol, bias = OUTPUT_CONTRACT[h]
    if abs(float(m.decoder.bias[0]) - bias) > 1e-7:
        raise SystemExit(f"REFUSED: decoder bias in {path} does not match its registered contract")
    m._contract = (pol, bias)
    return m


def _resample(x, sr_in, sr_out):
    if sr_in == sr_out:
        return np.asarray(x, np.float64)
    from scipy.signal import resample_poly
    g = gcd(sr_in, sr_out)
    return resample_poly(np.asarray(x, np.float64), sr_out // g, sr_in // g)


def enhance(audio, sr, model):
    """Returns (mono float32 output at sr, info). info: level_gain, headroom_gain, bound ('level' | 'headroom')."""
    x = np.asarray(audio, dtype=np.float64)
    if x.ndim == 2:
        x = x.mean(axis=1)
    n_in = len(x)
    in_level = float(np.sqrt(np.mean((x - x.mean()) ** 2)))          # DC-free input level
    x16 = _resample(x, sr, FS).astype(np.float32)
    level16 = float(np.sqrt(np.mean(x16.astype(np.float64) ** 2)))
    if in_level < 1e-6 or level16 < 1e-6:
        return np.zeros(n_in, dtype=np.float32), {"level_gain": 1.0, "headroom_gain": 1.0, "bound": "silence"}
    n16 = len(x16)
    inp = np.concatenate([x16 * (MIX_RMS / level16), np.zeros(DELAY, np.float32)])
    with torch.no_grad():
        y = model(torch.from_numpy(inp)[None])[0].numpy().astype(np.float64)
    pol, bias = model._contract
    y16 = pol * (y[DELAY:DELAY + n16] - bias)                       # output contract, before any level step
    out = _resample(y16, FS, sr)
    out = out[:n_in] if len(out) >= n_in else np.pad(out, (0, n_in - len(out)))
    out = out - out.mean()                                           # explicit DC handling (offline, whole file)
    rms, peak = float(np.sqrt(np.mean(out ** 2))), float(np.max(np.abs(out)))
    if rms < 1e-12:
        return np.zeros(n_in, dtype=np.float32), {"level_gain": 1.0, "headroom_gain": 1.0, "bound": "silence"}
    g_level, g_head = in_level / rms, CEIL / peak
    g = min(g_level, g_head)                                         # one final linear gain
    return (out * g).astype(np.float32), {"level_gain": g_level, "headroom_gain": g_head,
                                          "bound": "level" if g_level <= g_head else "headroom"}
