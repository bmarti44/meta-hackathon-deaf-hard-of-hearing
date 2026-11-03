"""Waveform baselines for bench-n6.

Unprocessed = the sound processor's ACE selection acting on the raw
mixture (no front-end NR). CausalSpectralGate = a deliberately simple
classical, strictly causal NR stand-in for the *class* of processing
in current processors. It is NOT a replica of Cochlear's proprietary
SmartSound/N6 processing, which cannot be reproduced offline from
public sources; beating it is necessary, not sufficient, to claim
beating an N6 in a real ear.

OracleIRM = non-causal upper bound (uses true clean/noise). A ceiling,
never a competitor.
"""
from __future__ import annotations
import numpy as np

from common import FS


class CausalSpectralGate:
    """Frame-causal Wiener-like spectral gate.

    Frames END at the current block boundary (left context only);
    each hop block's output is the last `hop` samples of the masked
    frame, so output block k depends only on input samples up to its
    end. Noise PSD is a min-tracked estimate over PAST frames only.
    Suffix invariance on a shared prefix is exact (see tests).
    Algorithmic latency: one hop (8 ms at hop=128/16k) emit granularity
    plus compute; documented, not hidden.
    """

    def __init__(self, n_fft=512, hop=128, floor=0.15, beta=0.8):
        self.n_fft, self.hop, self.floor, self.beta = n_fft, hop, floor, beta
        # Analysis window: half-Hann rise, FLAT over the emitted last hop.
        # (A full Hann tail tends to 0 at the frame end, so emitting the
        # tail requires dividing by ~0 -- that amplitude modulation cost
        # ~4 dB SI-SDR in bench run 1. Flat tail emits without division.)
        w = np.ones(n_fft)
        rise = n_fft - hop
        w[:rise] = 0.5 - 0.5 * np.cos(np.pi * np.arange(rise) / rise)
        self.win = w

    def process(self, x):
        x = np.asarray(x, dtype=np.float64)
        n, W, H = len(x), self.n_fft, self.hop
        out = np.zeros(n)
        noise_psd, smooth_psd, gain_smooth = None, None, None
        for end in range(H, n + 1, H):
            frame = np.zeros(W)
            seg = x[max(0, end - W):end]
            frame[W - len(seg):] = seg
            spec = np.fft.rfft(frame * self.win)
            psd = np.abs(spec) ** 2
            if noise_psd is None:
                noise_psd = psd.copy(); smooth_psd = psd.copy()
            else:
                smooth_psd = 0.7 * smooth_psd + 0.3 * psd
                # Min-tracking with slow rise: past frames only.
                noise_psd = np.minimum(smooth_psd, noise_psd * 1.02)
            gain = np.maximum(1.0 - self.beta * noise_psd / (psd + 1e-12), self.floor)
            gain = np.minimum(gain, 1.0)
            # Causal temporal smoothing of gains (past frames only)
            # reduces musical-noise flicker between blocks.
            gain_smooth = gain if gain_smooth is None else 0.7 * gain_smooth + 0.3 * gain
            y = np.fft.irfft(spec * gain_smooth, n=W)
            out[end - H:end] = y[-H:]  # window is flat (1.0) on the tail
        return out.astype(np.float32)


def oracle_irm_waveform(clean, noise, mix, n_fft=512, hop=128):
    """Non-causal STFT ideal-ratio-mask ceiling (true components known)."""
    def stft(x):
        win = np.hanning(n_fft)
        frames = []
        for s in range(0, max(1, len(x) - n_fft + 1), hop):
            frames.append(x[s:s + n_fft] * win)
        return np.fft.rfft(np.stack(frames), axis=-1), win

    S, win = stft(np.asarray(mix, dtype=np.float64))
    C, _ = stft(np.asarray(clean, dtype=np.float64))
    Nz, _ = stft(np.asarray(noise, dtype=np.float64))
    irm = np.abs(C) / (np.abs(C) + np.abs(Nz) + 1e-12)
    frames = np.fft.irfft(S * irm, n=n_fft, axis=-1)
    out = np.zeros(len(mix)); norm = np.zeros(len(mix))
    for i, fr in enumerate(frames):
        s = i * hop
        out[s:s + n_fft] += fr * win; norm[s:s + n_fft] += win ** 2
    # Edge samples have near-zero OLA norm; dividing by them produced
    # peaks >100 in bench run 1. Zero anything not properly covered.
    ok = norm > 0.2
    out[ok] /= norm[ok]
    out[~ok] = 0.0
    return out.astype(np.float32)
