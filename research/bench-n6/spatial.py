"""Direction-cue (spatial) screening for bench-n6. T0 only.

Holder interest (2026-11-03): his son cannot tell where sounds come
from. Any front-end we build must at minimum not destroy the
direction cues the signal still carries. This module makes that
measurable before any implant is involved.

Head model is deliberately simple and ASSUMED (screening, not HRTF
measurement): Woodworth ITD (head radius 8.75 cm) + a smooth
frequency-dependent head-shadow on the far ear. Absolute degrees
are approximate; cue DISTORTION introduced by processing (the
quantity gated here) is what the comparisons rest on.
"""
from __future__ import annotations
import math
import numpy as np

from common import FS
from vocoder import extract_envelopes

HEAD_R = 0.0875   # m, Woodworth sphere approximation
C_SOUND = 343.0


def _frac_delay(x, delay):
    n = len(x)
    t = np.arange(n) - delay
    return np.interp(t, np.arange(n), x, left=0.0, right=0.0).astype(np.float32)


def render_at(x, azimuth_deg):
    """Mono -> (L, R) for a source at azimuth (deg, + = right)."""
    x = np.asarray(x, dtype=np.float64)
    th = math.radians(float(np.clip(azimuth_deg, -90, 90)))
    itd_s = (HEAD_R / C_SOUND) * (abs(th) + math.sin(abs(th)))
    itd = itd_s * FS
    # Head shadow on far ear (FFT-domain, ASSUMED smooth model):
    # attenuation grows with frequency and |azimuth|.
    X = np.fft.rfft(x)
    f = np.linspace(0, FS / 2, len(X))
    shadow = 1.0 - 0.75 * math.sin(abs(th)) * (f / (f + 800.0))
    near = np.fft.irfft(X, n=len(x))
    far = np.fft.irfft(X * shadow, n=len(x))
    far = _frac_delay(far.astype(np.float32), itd)
    if th >= 0:      # source right: R near, L far
        return far, near.astype(np.float32)
    return near.astype(np.float32), far


def ild_per_band(L, R):
    """Per-ACE-band ILD = 20log10(mean env L / mean env R), dB."""
    eL = extract_envelopes(L).mean(axis=0)
    eR = extract_envelopes(R).mean(axis=0)
    return 20.0 * np.log10((eL + 1e-9) / (eR + 1e-9))


def itd_samples(L, R, max_lag=48):
    """Lag (samples) by which L lags R (positive = source right)."""
    a = np.asarray(L, dtype=np.float64); b = np.asarray(R, dtype=np.float64)
    a = a - a.mean(); b = b - b.mean()
    best_lag, best = 0, -np.inf
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            v = float(np.dot(a[lag:], b[:len(b) - lag])) if lag < len(b) else -np.inf
        else:
            v = float(np.dot(a[:lag], b[-lag:]))
        if v > best:
            best, best_lag = v, lag
    return best_lag


class LinkedSpectralGate:
    """Stereo causal gate with a COMMON gain for both ears.

    Same min-tracked Wiener idea as baselines.CausalSpectralGate, but
    the gain applied to L and R is the geometric mean of the two
    per-ear gains, so per-bin ILD is preserved exactly at the gain
    stage. Block-causal like the mono version (hop-emit).
    """

    def __init__(self, n_fft=512, hop=128, floor=0.15, beta=0.8):
        self.n_fft, self.hop, self.floor, self.beta = n_fft, hop, floor, beta
        w = np.ones(n_fft); rise = n_fft - hop
        w[:rise] = 0.5 - 0.5 * np.cos(np.pi * np.arange(rise) / rise)
        self.win = w

    def process_stereo(self, L, R):
        xs = [np.asarray(L, dtype=np.float64), np.asarray(R, dtype=np.float64)]
        n, W, H = len(xs[0]), self.n_fft, self.hop
        outs = [np.zeros(n), np.zeros(n)]
        state = [None, None]  # per-ear (noise_psd, smooth_psd)
        gain_smooth = None
        for end in range(H, n + 1, H):
            gains, specs = [], []
            for e in range(2):
                frame = np.zeros(W)
                seg = xs[e][max(0, end - W):end]
                frame[W - len(seg):] = seg
                spec = np.fft.rfft(frame * self.win)
                specs.append(spec)
                psd = np.abs(spec) ** 2
                if state[e] is None:
                    noise_psd, smooth_psd = psd.copy(), psd.copy()
                else:
                    noise_psd, smooth_psd = state[e]
                    smooth_psd = 0.7 * smooth_psd + 0.3 * psd
                    noise_psd = np.minimum(smooth_psd, noise_psd * 1.02)
                state[e] = (noise_psd, smooth_psd)
                g = np.maximum(1.0 - self.beta * noise_psd / (psd + 1e-12), self.floor)
                gains.append(np.minimum(g, 1.0))
            common = np.sqrt(gains[0] * gains[1])
            gain_smooth = common if gain_smooth is None else 0.7 * gain_smooth + 0.3 * common
            for e in range(2):
                y = np.fft.irfft(specs[e] * gain_smooth, n=W)
                outs[e][end - H:end] = y[-H:]
        return outs[0].astype(np.float32), outs[1].astype(np.float32)
