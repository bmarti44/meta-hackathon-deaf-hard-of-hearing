"""ACE-like noise vocoder: lets a normal-hearing listener hear an
approximation of what a 22-channel, 8-of-22 ACE strategy preserves.

This is a SCREENING PROXY for the (normal-hearing) father only.
It is not what his son hears: no current spread, loudness map,
neural survival, or device fitting is modelled. Parameters marked
CITED follow research/gen13/ace_sim.py (inspected sources there);
the exact band-edge split is ASSUMED there and here.

Offline resynthesis (for listening files) need not be causal; the
ENHANCER under test must be. The two are kept separate on purpose.
"""
from __future__ import annotations
import math
import numpy as np
from scipy.signal import butter, sosfilt

from common import FS, limit_signal

M_CHANNELS = 22   # CITED in gen13/ace_sim.py
N_MAXIMA = 8      # CITED default in gen13/ace_sim.py
N_FFT, HOP = 512, 128


def ace_edges():
    lin = np.linspace(188.0, 1312.0, 10)
    log = np.exp(np.linspace(math.log(1312.0), math.log(7938.0), 14))
    edges = np.concatenate([lin[:-1], log])
    assert len(edges) == M_CHANNELS + 1
    return edges


def _stft(x):
    x = np.asarray(x, dtype=np.float64)
    win = np.hanning(N_FFT)
    n_frames = 1 + max(0, (len(x) - N_FFT) // HOP) if len(x) >= N_FFT else 1
    pad = np.zeros(N_FFT + (n_frames - 1) * HOP)
    pad[:len(x)] = x
    frames = np.stack([pad[i * HOP:i * HOP + N_FFT] * win for i in range(n_frames)])
    return np.fft.rfft(frames, axis=-1)


def extract_envelopes(x, n_of_m=False):
    """Waveform -> (T, 22) ACE-band envelopes (sqrt band power)."""
    spec = _stft(x)
    power = np.abs(spec) ** 2
    freqs = np.linspace(0, FS / 2, power.shape[1])
    edges = ace_edges()
    env = np.zeros((power.shape[0], M_CHANNELS))
    for b in range(M_CHANNELS):
        sel = (freqs >= edges[b]) & (freqs < edges[b + 1])
        if not sel.any():
            sel[int(np.argmin(np.abs(freqs - math.sqrt(edges[b] * edges[b + 1]))))] = True
        env[:, b] = np.sqrt(power[:, sel].sum(axis=1) + 1e-12)
    if n_of_m:
        keep = np.zeros_like(env, dtype=bool)
        idx = np.argsort(-env, axis=1)[:, :N_MAXIMA]
        np.put_along_axis(keep, idx, True, axis=1)
        env = np.where(keep, env, 0.0)
    return env


def vocode(x, seed=0):
    """Waveform -> noise-vocoded waveform, same length, peak-limited."""
    x = np.asarray(x, dtype=np.float32)
    if float(np.max(np.abs(x))) < 1e-7:
        return np.zeros_like(x)
    env = extract_envelopes(x, n_of_m=True)          # (T, 22)
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(len(x) + N_FFT)
    edges = ace_edges()
    # Upsample envelopes to sample rate (zero-order hold per hop).
    env_s = np.repeat(env, HOP, axis=0)[:len(x)]
    if len(env_s) < len(x):
        env_s = np.pad(env_s, ((0, len(x) - len(env_s)), (0, 0)))
    out = np.zeros(len(x))
    for b in range(M_CHANNELS):
        lo, hi = max(edges[b], 20.0), min(edges[b + 1], FS / 2 - 20)
        if hi <= lo:
            continue
        sos = butter(4, [lo, hi], btype="band", fs=FS, output="sos")
        band = sosfilt(sos, noise)[:len(x)]
        band = band / (np.sqrt(np.mean(band ** 2)) + 1e-12)
        out += env_s[:, b] * band
    return limit_signal(out)
