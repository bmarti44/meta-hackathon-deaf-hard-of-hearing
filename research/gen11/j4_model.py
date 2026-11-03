"""J4-A1: frame-causal filterbank mask front-end (Gen10 candidate-J4-causal.md S2).

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.

Causality by construction:
  * Right-aligned framing only: frame j = samples [j*H, j*H+W-1], emitted
    only when its last sample exists. No centre padding, no left/right pad
    of the waveform at all (input shorter than W yields zero frames).
  * Features F_j are log filterbank energies of frame j alone (no deltas).
  * Normalisation is per-frame layer norm over the band axis of F_j alone
    (no affine parameters, no cross-frame statistic of any kind).
  * Recurrence is a 2-layer unidirectional LSTM stepped strictly forward;
    state (h, c) at frame j is a function of frames <= j only. There is no
    other temporal operation in the graph: no convolution, no attention,
    no pooling over time, no mask smoothing.
  * Output is a sigmoid mask M_j in [0,1]^B applied to frame j's own
    filterbank envelopes. No waveform resynthesis / overlap-add stage.

Context K=5 (frames j-4..j): the LSTM state summarises past frames, so the
mask for frame j is computed from F_{j-4..j} (and, via carried state, earlier
frames too -- still strictly causal; see build-report.md for the note on
spec S3.2's finite-span wording vs. persistent-state recurrence). Priming:
frames j < K-1 run from zero state with partial context, per spec S3.2.

Parameter accounting matches spec S3.4 exactly. That formula counts ONE
bias vector per LSTM layer (4h*(in+h+1)), whereas torch.nn.LSTM carries two
(bias_ih and bias_hh, +512 params/layer). This module therefore implements
the LSTM cell directly with a single fused bias so the built graph -- not
just the arithmetic -- has exactly 238,656 parameters at B=64, h=128.
"""
from __future__ import annotations

import math

import torch
import torch.nn.functional as F
from torch import nn

FS = 16_000          # sample rate (Hz), spec S2.2
W = 128              # window, samples = 8.0 ms
H = 64               # hop, samples = 4.0 ms (250 frames/s)
K = 5                # past+current context frames j-4..j
B = 64               # filterbank bands (PROPOSED in spec, pinned here)
HIDDEN = 128         # LSTM units per layer
N_LAYERS = 2
EPS = 1e-8


# --------------------------------------------------------------------------
# Framing / filterbank (all operations read frame j's samples only)
# --------------------------------------------------------------------------
def num_frames(n_samples: int, win: int = W, hop: int = H) -> int:
    """Number of complete right-aligned frames in a signal. No padding."""
    if n_samples < win:
        return 0
    return (n_samples - win) // hop + 1


def frame_bounds(j: int, win: int = W, hop: int = H) -> tuple[int, int]:
    """Inclusive [first, last] input-sample indices frame j may read."""
    return j * hop, j * hop + win - 1


def frame_signal(x: torch.Tensor, win: int = W, hop: int = H) -> torch.Tensor:
    """x: (batch, n_samples) -> (batch, n_frames, win), right-aligned."""
    if x.dim() != 2:
        raise ValueError(f"expected (batch, n_samples), got {tuple(x.shape)}")
    n = num_frames(x.shape[1], win, hop)
    if n == 0:
        return x.new_empty((x.shape[0], 0, win))
    return x.unfold(dimension=1, size=win, step=hop)


def mel_filterbank(n_fft: int, n_bands: int, fs: int = FS,
                   f_min: float = 50.0, f_max: float | None = None) -> torch.Tensor:
    """Triangular mel-spaced filterbank, (n_bands, n_fft//2+1), non-negative.

    Fixed analysis matrix (a buffer, not a parameter): it mixes frequency
    bins within one frame only and cannot move information across time.
    """
    f_max = fs / 2.0 if f_max is None else f_max
    n_bins = n_fft // 2 + 1
    freqs = torch.linspace(0.0, fs / 2.0, n_bins)

    def hz_to_mel(f: float) -> float:
        return 2595.0 * math.log10(1.0 + f / 700.0)

    def mel_to_hz(m: float) -> float:
        return 700.0 * (10.0 ** (m / 2595.0) - 1.0)

    edges_hz = torch.tensor(
        [mel_to_hz(m) for m in torch.linspace(hz_to_mel(f_min), hz_to_mel(f_max), n_bands + 2).tolist()]
    )
    fb = torch.zeros(n_bands, n_bins)
    for b in range(n_bands):
        lo, ctr, hi = edges_hz[b].item(), edges_hz[b + 1].item(), edges_hz[b + 2].item()
        rise = (freqs - lo) / max(ctr - lo, 1e-12)
        fall = (hi - freqs) / max(hi - ctr, 1e-12)
        fb[b] = torch.clamp(torch.minimum(rise, fall), min=0.0)
    # Guard against an empty band at 128-pt FFT resolution: give any all-zero
    # band the single nearest bin so every band carries signal.
    empty = fb.sum(dim=1) == 0
    for b in torch.nonzero(empty).flatten().tolist():
        nearest = int(torch.argmin(torch.abs(freqs - edges_hz[b + 1])))
        fb[b, nearest] = 1.0
    return fb


# --------------------------------------------------------------------------
# Unidirectional LSTM cell with a single fused bias (spec S3.4 accounting)
# --------------------------------------------------------------------------
class UniLSTMCell(nn.Module):
    """One forward-only LSTM layer. Params = 4h*(in + h + 1), exactly."""

    def __init__(self, input_size: int, hidden_size: int):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        bound = 1.0 / math.sqrt(hidden_size)
        self.weight_ih = nn.Parameter(torch.empty(4 * hidden_size, input_size))
        self.weight_hh = nn.Parameter(torch.empty(4 * hidden_size, hidden_size))
        self.bias = nn.Parameter(torch.empty(4 * hidden_size))
        for p in (self.weight_ih, self.weight_hh, self.bias):
            nn.init.uniform_(p, -bound, bound)
        # Forget-gate bias +1 (standard init; a constant, reads no data).
        with torch.no_grad():
            self.bias[hidden_size:2 * hidden_size] += 1.0

    def forward(self, x: torch.Tensor, state: tuple[torch.Tensor, torch.Tensor]):
        h, c = state
        gates = F.linear(x, self.weight_ih) + F.linear(h, self.weight_hh) + self.bias
        i, f, g, o = gates.chunk(4, dim=-1)
        i, f, o = torch.sigmoid(i), torch.sigmoid(f), torch.sigmoid(o)
        g = torch.tanh(g)
        c_new = f * c + i * g
        h_new = o * torch.tanh(c_new)
        return h_new, (h_new, c_new)


# --------------------------------------------------------------------------
# J4-A1 model
# --------------------------------------------------------------------------
class J4A1(nn.Module):
    """2x128 unidirectional LSTM -> sigmoid filterbank mask (spec S2.3)."""

    def __init__(self, n_bands: int = B, hidden: int = HIDDEN,
                 n_layers: int = N_LAYERS, win: int = W, hop: int = H,
                 fs: int = FS):
        super().__init__()
        self.n_bands, self.hidden = n_bands, hidden
        self.n_layers, self.win, self.hop, self.fs = n_layers, win, hop, fs
        self.context_frames = K
        self.register_buffer("window", torch.hann_window(win, periodic=True))
        self.register_buffer("filterbank", mel_filterbank(win, n_bands, fs))
        cells = [UniLSTMCell(n_bands, hidden)]
        cells += [UniLSTMCell(hidden, hidden) for _ in range(n_layers - 1)]
        self.cells = nn.ModuleList(cells)
        self.fc = nn.Linear(hidden, n_bands)  # sigmoid mask head, spec S2.3

    # -- feature extraction: frame j's samples -> F_j, envelope_j -----------
    def extract_features(self, waveform: torch.Tensor):
        """waveform (batch, n) -> (log features, linear envelopes).

        Both outputs are (batch, n_frames, B); entry [:, j] depends only on
        samples [j*H, j*H+W-1].
        """
        frames = frame_signal(waveform, self.win, self.hop)       # (b,T,W)
        if frames.shape[1] == 0:
            empty = waveform.new_empty((waveform.shape[0], 0, self.n_bands))
            return empty, empty
        spec = torch.fft.rfft(frames * self.window, dim=-1)       # per frame
        power = spec.real ** 2 + spec.imag ** 2                    # (b,T,nbins)
        band_energy = power @ self.filterbank.t()  # (batch,T,bands), per-frame
        envelopes = torch.sqrt(band_energy + EPS)                  # linear env
        features = torch.log(band_energy + EPS)                    # log energy
        return features, envelopes

    @staticmethod
    def causal_norm(features: torch.Tensor) -> torch.Tensor:
        """Per-frame layer norm over the band axis only (no affine params).

        The statistic set for frame j is {F_j} -- a subset of frames <= j.
        """
        return F.layer_norm(features, (features.shape[-1],), eps=1e-5)

    # -- recurrent core ------------------------------------------------------
    def init_state(self, batch: int, device=None, dtype=None):
        return [(torch.zeros(batch, self.hidden, device=device, dtype=dtype),
                 torch.zeros(batch, self.hidden, device=device, dtype=dtype))
                for _ in range(self.n_layers)]

    def step(self, f_j: torch.Tensor, state):
        """One frame in, one mask out. f_j: (batch, B) raw log features."""
        x = self.causal_norm(f_j)
        new_state = []
        for cell, st in zip(self.cells, state):
            x, st_new = cell(x, st)
            new_state.append(st_new)
        mask = torch.sigmoid(self.fc(x))
        return mask, new_state

    def forward_features(self, features: torch.Tensor) -> torch.Tensor:
        """features (batch, T, B) -> masks (batch, T, B), stepped in order."""
        state = self.init_state(features.shape[0], features.device, features.dtype)
        masks = []
        for j in range(features.shape[1]):
            m_j, state = self.step(features[:, j], state)
            masks.append(m_j)
        if not masks:
            return features.new_empty(features.shape)
        return torch.stack(masks, dim=1)

    def forward(self, waveform: torch.Tensor):
        """waveform (batch, n) -> (masks, masked_envelopes), (batch, T, B).

        Envelope-mask output only: masked_envelopes[:, j] = M_j * env_j.
        There is deliberately no waveform (overlap-add) synthesis path.
        """
        features, envelopes = self.extract_features(waveform)
        masks = self.forward_features(features)
        return masks, masks * envelopes

    # -- accounting (spec S3.4) ---------------------------------------------
    def count_parameters(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def macs_per_frame(self) -> int:
        """Multiply-accumulates per frame = 4h(B+h) + 4h(2h) + hB (spec S3.4).

        Counts the two LSTM layers' input+recurrent matmuls and the FC head
        for one frame step. Bias adds, elementwise gates, norm, and the
        fixed FFT/filterbank analysis are not MACs of learned matmuls and
        are excluded, matching the spec formula's scope.
        """
        h, b = self.hidden, self.n_bands
        return 4 * h * (b + h) + 4 * h * (2 * h) + h * b


def spec_param_count(n_bands: int = B, hidden: int = HIDDEN) -> int:
    """Spec S3.4 closed form: L1 + L2 + FC with layer = 4h*(in+h+1)."""
    l1 = 4 * hidden * (n_bands + hidden + 1)
    l2 = 4 * hidden * (2 * hidden + 1)
    fc = (hidden + 1) * n_bands
    return l1 + l2 + fc


def spec_macs_per_frame(n_bands: int = B, hidden: int = HIDDEN) -> int:
    return 4 * hidden * (n_bands + hidden) + 4 * hidden * (2 * hidden) + hidden * n_bands


if __name__ == "__main__":
    torch.manual_seed(0)
    model = J4A1()
    print(f"params={model.count_parameters()} spec={spec_param_count()}")
    print(f"MACs/frame={model.macs_per_frame()} spec={spec_macs_per_frame()}")
    masks, masked = model(torch.randn(2, FS))
    print(f"1 s in -> masks {tuple(masks.shape)}, masked env {tuple(masked.shape)}")
