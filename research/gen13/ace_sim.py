"""Gen13: simplified ACE-like electrodogram simulation -- T0 in-silico ONLY.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
NEVER listener evidence. This prices a mask as an ACE-like front-end would
consume envelopes; it models no neural response, loudness, or perception.

What is implemented (simplified ACE, after Cochlear Nucleus ACE descriptions):
  * M = 22 channels, N = 8 maxima selected per frame (n-of-m).
    [CITED: web sources inspected 2026-11-03 -- MDPI Technologies review
    (mdpi.com/2227-7080/13/8/331): "ACE ... 22 electrode contacts ...
    N is fixed most often at 8"; scite.ai report on Nogueira et al. ACE:
    "N=8 channels ... out of M=22 ... 900 pulses per second (pps) ...
    total 7200 pps". Default clinical maxima can be set 8-10 by the
    audiologist per other reviews; 8 is used here.]
  * Frequency allocation 188-7938 Hz, bands spaced linearly up to ~1312 Hz
    then logarithmically to 7938 Hz.
    [CITED rule: Loizou CI review excerpts + InTech chapter excerpts found
    by web search 2026-11-03: "filter bands in the ACE strategy ...
    spaced linearly from 188 to 1312 Hz and thereafter logarithmically
    up to 7938 Hz"; EURASIP JASMP 2011 (Semitone frequency mapping...):
    "standard ACE ... encodes signals between 188 and 7980 Hz onto
    maximally 22 intracochlear electrodes". The exact 23-edge table used
    below is a construction from that rule (9 linear + 13 log bands) --
    the split count and exact edges are ASSUMED, not a copied clinical
    frequency-allocation table.]
  * Envelope per channel = sqrt(band power), as in FFT-filterbank ACE
    descriptions (band envelopes from summed FFT-bin power).
    [Envelope low-pass cutoffs of 200-400 Hz are reported in the same
    excerpts; here the J4 frame rate (250 frames/s, 4 ms hop) is the
    envelope sample rate and no additional low-pass is applied -- ASSUMED.]

ASSUMED / explicitly NOT modelled (all labeled, none hidden):
  * Pre-emphasis and automatic gain control: omitted.
  * Loudness growth, threshold (T) / comfort (C) mapping to current
    units: omitted. Electrodogram values are linear envelope amplitudes.
  * Pulse timing, interleaved order (base-to-apex), pulse width/phase,
    channel interaction / current spread, refractory effects, neural
    survival: omitted. One electrodogram column per 4 ms J4 frame, not
    per 1.1 ms (900 pps) ACE cycle: the frame-rate mismatch is ASSUMED
    acceptable for a T0 mask-pricing screen and is a stated limit.
  * Waveform path uses a 128-pt FFT filterbank (J4's own framing) rather
    than Cochlear's proprietary implementation. ASSUMED simplification.

Consumption model (how J4 is priced here): J4-A1 emits masked 64-band mel
envelopes, not a waveform (gen11 spec S2.1). The primary ACE path therefore
maps 64 mel bands -> 22 ACE channels by frequency overlap (matrix built
from the two filterbanks' centre frequencies) and then applies n-of-m
selection. Unprocessed = mixture envelopes through the same map; oracle =
IRM-masked envelopes through the same map; reference = clean envelopes.
A waveform -> 22-channel path is also provided for standalone use/sanity.
"""
from __future__ import annotations

import math

import numpy as np
import torch

FS = 16_000
M_CHANNELS = 22      # CITED (see module docstring)
N_MAXIMA = 8         # CITED default (see module docstring)
F_LO = 188.0         # CITED allocation range
F_HI = 7938.0        # CITED allocation range
F_KNEE = 1312.0      # CITED linear->log knee
N_LINEAR_BANDS = 9   # ASSUMED split of the 22 bands (9 linear + 13 log)


def ace_band_edges(m: int = M_CHANNELS, f_lo: float = F_LO, f_hi: float = F_HI,
                   f_knee: float = F_KNEE, n_linear: int = N_LINEAR_BANDS) -> np.ndarray:
    """23 band edges (Hz): linear f_lo..f_knee, then log f_knee..f_hi. ASSUMED split."""
    lin = np.linspace(f_lo, f_knee, n_linear + 1)              # n_linear bands
    log = np.exp(np.linspace(math.log(f_knee), math.log(f_hi), m - n_linear + 1))
    edges = np.concatenate([lin[:-1], log])
    assert len(edges) == m + 1, (len(edges), m)
    assert np.all(np.diff(edges) > 0)
    return edges


def ace_centres(edges: np.ndarray | None = None) -> np.ndarray:
    edges = ace_band_edges() if edges is None else edges
    return np.sqrt(edges[:-1] * edges[1:])  # geometric centres (ASSUMED convention)


def waveform_filterbank(n_fft: int = 128, fs: int = FS,
                        edges: np.ndarray | None = None) -> torch.Tensor:
    """(22, n_fft//2+1) non-negative band matrix: bin -> ACE band by edge range.

    Each FFT bin is assigned to the ACE band whose [lo, hi) contains the bin
    frequency; bands narrower than the 125 Hz bin spacing (possible at low
    frequencies at 128-pt FFT) take their nearest bin so no channel is empty
    (same guard convention as gen11 mel_filterbank). ASSUMED simplification
    of Cochlear's proprietary filterbank.
    """
    edges = ace_band_edges() if edges is None else edges
    n_bins = n_fft // 2 + 1
    freqs = np.linspace(0.0, fs / 2.0, n_bins)
    fb = np.zeros((len(edges) - 1, n_bins), dtype=np.float64)
    for b in range(len(edges) - 1):
        sel = (freqs >= edges[b]) & (freqs < edges[b + 1])
        if b == len(edges) - 2:
            sel |= freqs == edges[b + 1]
        fb[b, sel] = 1.0
        if fb[b].sum() == 0:
            fb[b, int(np.argmin(np.abs(freqs - math.sqrt(edges[b] * edges[b + 1]))))] = 1.0
    return torch.as_tensor(fb, dtype=torch.float32)


def mel_to_ace_matrix(mel_fb: torch.Tensor, ace_fb: torch.Tensor | None = None) -> torch.Tensor:
    """(22, B) map from J4 mel-band energies to ACE channel energies.

    Built in the shared FFT-bin space: mel bands and ACE bands are both
    non-negative weightings of the same bins, so ACE energy is approximated
    by redistributing each mel band's energy across ACE bands in proportion
    to bin overlap: W = ace_fb @ pinv-ish(mel). We use the least-squares-free
    overlap construction W[a,b] = sum_k ace[a,k]*mel[b,k] / sum_k mel[b,k],
    which is exact when a mel band lies wholly inside one ACE band.
    ASSUMED consumption-map approximation (stated limit).
    """
    ace_fb = waveform_filterbank(n_fft=(mel_fb.shape[1] - 1) * 2) if ace_fb is None else ace_fb
    mel = mel_fb.to(torch.float64)
    ace = ace_fb.to(torch.float64)
    overlap = ace @ mel.t()                       # (22, B)
    denom = mel.sum(dim=1, keepdim=True).clamp(min=1e-12)  # (B, 1)
    w = overlap / denom.t()
    return w.to(torch.float32)


def ace_envelopes_from_mel(mel_env: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
    """mel_env (..., B) linear envelopes -> (..., 22) ACE linear envelopes.

    Energies are mapped (env^2) then sqrt, matching the band-power
    definition of both filterbanks.
    """
    energy = (mel_env.to(torch.float64) ** 2) @ w.to(torch.float64).t()
    return torch.sqrt(energy.clamp(min=0.0)).to(mel_env.dtype)


@torch.no_grad()
def ace_envelopes_from_waveform(model, waveform: torch.Tensor) -> torch.Tensor:
    """waveform (batch, n) -> (batch, T, 22) via model's framing + ACE fb.

    Uses the J4 model's own right-aligned 128/64 framing so frame counts
    match the envelope path exactly. Standalone/sanity path; the primary
    J4 consumption path is ace_envelopes_from_mel (no waveform synthesis).
    """
    from j4_model import frame_signal  # gen11, on sys.path in callers
    frames = frame_signal(waveform, model.win, model.hop)
    if frames.shape[1] == 0:
        return waveform.new_empty((waveform.shape[0], 0, M_CHANNELS))
    spec = torch.fft.rfft(frames * model.window, dim=-1)
    power = spec.real ** 2 + spec.imag ** 2
    fb = waveform_filterbank(n_fft=model.win).to(waveform.device)
    return torch.sqrt((power @ fb.t()).clamp(min=0.0) + 1e-12)


def n_of_m(envelopes: torch.Tensor, n: int = N_MAXIMA) -> torch.Tensor:
    """Electrodogram: keep the n largest channels per frame, zero the rest.

    envelopes (..., M) -> same shape. Ties broken by torch.topk order
    (deterministic). Values are linear envelope amplitudes (ASSUMED: no
    T/C loudness mapping, no pulse generation).
    """
    if envelopes.shape[-1] < n:
        raise ValueError(f"n={n} exceeds channels {envelopes.shape[-1]}")
    idx = torch.topk(envelopes, k=n, dim=-1).indices
    keep = torch.zeros_like(envelopes, dtype=torch.bool).scatter_(-1, idx, True)
    return torch.where(keep, envelopes, torch.zeros_like(envelopes))


def selected_sets(envelopes: torch.Tensor, n: int = N_MAXIMA) -> torch.Tensor:
    """(...) -> (..., n) indices of selected channels per frame."""
    return torch.topk(envelopes, k=n, dim=-1).indices


# ---------------------------------------------------------------------------
# Metrics (all T0, in-silico; computed per eval crop in eval2.py)
# ---------------------------------------------------------------------------
def envelope_correlation(sys_env: torch.Tensor, ref_env: torch.Tensor) -> float:
    """Mean per-channel Pearson r (Fisher-z averaged) over time. (T, M) inputs."""
    a = sys_env.to(torch.float64)
    b = ref_env.to(torch.float64)
    a = a - a.mean(dim=0, keepdim=True)
    b = b - b.mean(dim=0, keepdim=True)
    num = (a * b).sum(dim=0)
    den = torch.sqrt((a ** 2).sum(dim=0) * (b ** 2).sum(dim=0)).clamp(min=1e-12)
    r = (num / den).clamp(-0.999999, 0.999999)
    return float(torch.tanh(torch.arctanh(r).mean()))


def channel_snr_db(clean_comp: torch.Tensor, noise_comp: torch.Tensor) -> float:
    """Aggregate channel SNR: 10*log10(||clean||^2 / ||noise||^2) over (T, M).

    clean_comp / noise_comp are the system's ACE envelopes of the clean and
    noise components separately (mixture-derived mask applied to each).
    """
    pc = float((clean_comp.to(torch.float64) ** 2).sum())
    pn = float((noise_comp.to(torch.float64) ** 2).sum())
    return 10.0 * math.log10((pc + 1e-12) / (pn + 1e-12))


def maxima_overlap(sys_env: torch.Tensor, ref_env: torch.Tensor, n: int = N_MAXIMA) -> float:
    """Mean fraction of the reference's n selected channels also selected
    by the system, per frame (1.0 = identical n-of-m choices)."""
    s = selected_sets(sys_env, n)
    r = selected_sets(ref_env, n)
    hit = (s.unsqueeze(-1) == r.unsqueeze(-2)).any(dim=-1)  # (T, n) sys picks in ref set
    return float(hit.to(torch.float64).mean())


if __name__ == "__main__":
    edges = ace_band_edges()
    print(f"ACE edges ({len(edges)}): {[round(float(e)) for e in edges]}")
    fb = waveform_filterbank()
    print(f"waveform fb {tuple(fb.shape)} row sums min={float(fb.sum(1).min()):.1f}")
    torch.manual_seed(0)
    env = torch.rand(50, M_CHANNELS)
    el = n_of_m(env)
    nnz = (el != 0).sum(dim=-1)
    assert int(nnz.min()) == int(nnz.max()) == N_MAXIMA, nnz
    assert envelope_correlation(env, env) > 0.999999 - 1e-9
    assert maxima_overlap(env, env) == 1.0
    print(f"n-of-m keeps exactly {N_MAXIMA}/frame; identity corr/overlap OK")
    print(f"channel_snr self-test: {channel_snr_db(env, 0.1 * env):.1f} dB (expect 20.0)")
