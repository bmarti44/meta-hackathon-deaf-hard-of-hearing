"""Shared utilities for the no-implant bench. T0/in-silico only."""
from __future__ import annotations
import numpy as np

FS = 16000
PEAK_LIMIT = 0.89
TARGET_RMS = 0.1


def rms(x) -> float:
    x = np.asarray(x, dtype=np.float64)
    return float(np.sqrt(np.mean(x ** 2) + 1e-12))


def si_sdr(ref, est) -> float:
    ref = np.asarray(ref, dtype=np.float64); est = np.asarray(est, dtype=np.float64)
    ref = ref - ref.mean(); est = est - est.mean()
    alpha = np.dot(est, ref) / (np.dot(ref, ref) + 1e-12)
    proj = alpha * ref
    return float(10 * np.log10((np.dot(proj, proj) + 1e-12) /
                                (np.dot(est - proj, est - proj) + 1e-12)))


def limit_signal(x, target_rms=TARGET_RMS, peak=PEAK_LIMIT):
    """Safety limiter for anything a person might later listen to.

    Silence stays silence. Non-silent input is scaled toward
    target_rms, then hard-capped so max|x| <= peak. Never amplifies
    a silent/near-silent input into audibility.
    """
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0 or float(np.max(np.abs(x))) < 1e-7:
        return np.zeros_like(x, dtype=np.float32)
    y = x / (rms(x) + 1e-12) * target_rms
    p = float(np.max(np.abs(y)))
    if p > peak:
        y = y / p * (peak - 0.001)  # margin so 16-bit wav rounding stays under peak
    return y.astype(np.float32)


def bootstrap_ci(values, seed=13, reps=2000):
    v = np.asarray(values, dtype=np.float64); v = v[np.isfinite(v)]
    if len(v) == 0:
        return {"mean": float("nan"), "ci_lo": float("nan"), "ci_hi": float("nan"), "n": 0}
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(reps, len(v)))
    means = v[idx].mean(axis=1)
    return {"mean": float(v.mean()), "ci_lo": float(np.percentile(means, 2.5)),
            "ci_hi": float(np.percentile(means, 97.5)), "n": int(len(v))}


def envelope_correlation(a, b) -> float:
    """Mean per-channel Pearson r (Fisher-z averaged). (T, M) inputs."""
    a = np.asarray(a, dtype=np.float64); b = np.asarray(b, dtype=np.float64)
    a = a - a.mean(axis=0, keepdims=True); b = b - b.mean(axis=0, keepdims=True)
    num = (a * b).sum(axis=0)
    den = np.sqrt((a ** 2).sum(axis=0) * (b ** 2).sum(axis=0)) + 1e-12
    r = np.clip(num / den, -0.999999, 0.999999)
    return float(np.tanh(np.arctanh(r).mean()))
