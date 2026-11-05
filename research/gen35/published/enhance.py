"""Enhance speech in a wav file with the causal Before-the-Implant enhancer.

CLI:
    python enhance.py input.wav output.wav [--weights model.safetensors] [--device cpu]

Python:
    from enhance import load_model, enhance
    model = load_model("model.safetensors")
    clean = enhance(noisy, sr, model=model)   # same length and rate as noisy

What it does: mono mix-down, resample to 16 kHz, scale the file to the level
of a 0 dB training mixture (RMS 0.14), run the strictly causal model over the
whole file, remove its fixed 63-sample content delay so output lines up with
input, set the output to the input's RMS level, and resample back to the input
rate and length. The two level steps use whole-file RMS (offline); the model
itself never looks ahead.
"""
from __future__ import annotations

import argparse
import os
import sys
from math import gcd

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from model_causal import DELAY, FS, CausalTasNetEnh  # noqa: E402

# Training mixtures: clean speech at RMS 0.1 plus noise at -5..10 dB SNR,
# so mixtures span RMS ~0.10-0.19. 0.14 is a 0 dB mixture.
MIX_RMS = 0.14
_DEFAULT = {}


def load_model(path: str | None = None, device: str = "cpu") -> CausalTasNetEnh:
    """Load weights (.safetensors, or a training .pt with a "state_dict")."""
    path = path or os.path.join(HERE, "model.safetensors")
    if path.endswith(".safetensors"):
        from safetensors.torch import load_file
        sd = load_file(path)
    else:
        ck = torch.load(path, map_location="cpu", weights_only=True)
        sd = ck["state_dict"] if isinstance(ck, dict) and "state_dict" in ck else ck
    model = CausalTasNetEnh()
    model.load_state_dict(sd, strict=True)
    return model.to(device).eval()


def _resample(x: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return x
    try:
        from scipy.signal import resample_poly
    except ImportError as e:
        raise RuntimeError(f"input is {sr_in} Hz; install scipy to resample, "
                           f"or provide {sr_out} Hz audio") from e
    g = gcd(sr_in, sr_out)
    return resample_poly(x, sr_out // g, sr_in // g).astype(np.float32)


def enhance(audio: np.ndarray, sr: int, model: CausalTasNetEnh | None = None,
            device: str | None = None) -> np.ndarray:
    """Enhance a waveform. audio: (T,) or (T, channels) float array at rate sr.

    Returns a mono float32 array with the same length and sample rate.
    """
    if model is None:
        if "m" not in _DEFAULT:
            _DEFAULT["m"] = load_model(device=device or "cpu")
        model = _DEFAULT["m"]
    device = device or next(model.parameters()).device
    x = np.asarray(audio, dtype=np.float32)
    if x.ndim == 2:
        x = x.mean(axis=1)
    n_in = len(x)
    x16 = _resample(x, sr, FS)
    level = float(np.sqrt(np.mean(x16.astype(np.float64) ** 2)))
    if level < 1e-6:                       # silence in, silence out
        return np.zeros(n_in, dtype=np.float32)
    gain = MIX_RMS / level
    n16 = len(x16)
    # Pad DELAY zeros at the end so the last input samples are emitted too.
    # The model is causal, so this padding cannot change any earlier output.
    inp = np.concatenate([x16 * gain, np.zeros(DELAY, np.float32)])
    with torch.no_grad():
        y = model(torch.from_numpy(inp)[None].to(device))[0].cpu().numpy()
    y16 = y[DELAY:DELAY + n16]             # align with input
    # The model was trained with a scale-invariant loss, so its output gain is
    # arbitrary: give the output the same RMS as the input.
    y16 = y16 * (level / (float(np.sqrt(np.mean(y16.astype(np.float64) ** 2))) + 1e-12))
    out = _resample(y16, FS, sr)
    if len(out) >= n_in:
        out = out[:n_in]
    else:
        out = np.pad(out, (0, n_in - len(out)))
    return out.astype(np.float32)


def main():
    import soundfile as sf
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--weights", default=None,
                    help="default: model.safetensors next to this script")
    ap.add_argument("--device", default="cpu", help="cpu, cuda or mps")
    a = ap.parse_args()
    audio, sr = sf.read(a.input, dtype="float32", always_2d=False)
    model = load_model(a.weights, a.device)
    out = enhance(audio, sr, model=model, device=a.device)
    sf.write(a.output, np.clip(out, -1.0, 1.0), sr)
    print(f"wrote {a.output} ({len(out) / sr:.2f} s, {sr} Hz, mono)")


if __name__ == "__main__":
    main()
