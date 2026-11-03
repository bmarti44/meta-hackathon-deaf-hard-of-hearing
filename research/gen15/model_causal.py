"""Gen15: strictly causal Conv-TasNet-style waveform enhancement (1 target).

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
T0 in-silico ONLY. No listener-benefit claim is made or implied.

New design axis after Gen14 closed the envelope-mask (J4) recipe family:
direct waveform masking in a learned basis, trained with waveform SI-SDR,
instead of a mel-envelope IRM regressed with mask-MSE.

Strict causality contract
-------------------------
* Every convolution has padding=0. All temporal padding is LEFT-ONLY
  (F.pad(x, (pad, 0))) inside CausalConv1d / the encoder. No symmetric
  padding anywhere (asserted in audit_causality()).
* Normalisation is cumulative layer norm (cLN, Luo & Mesgarani causal
  Conv-TasNet): statistics at frame t use frames <= t only. NO global
  layer norm (gLN), NO batch norm, no mean/variance over future frames.
* Encoder: left-pad (L-1) then Conv1d(kernel=L, stride=S). Frame t sees
  input samples [S*t-(L-1) .. S*t] -- i.e. <= S*t only.
* Decoder: ConvTranspose1d(kernel=L, stride=S) places frame t's basis
  vector at output samples [S*t .. S*t+L-1]. An output sample p therefore
  only receives frames t with S*t <= p, whose inputs are <= S*t <= p.
  Hence the RAW model output is sample-wise causal: y[p] depends only on
  x[<=p]. The price is a fixed content delay: frame t encodes the window
  ending at S*t but writes it starting at S*t, so the raw output is the
  enhanced waveform DELAYED by (L-1) samples. Training targets and eval
  alignment apply exactly that delay (see DELAY); it is latency, not
  lookahead.
* Algorithmic latency (excluding compute): content delay (L-1) samples
  plus frame-emit granularity <= (S-1) samples in a block-streaming
  implementation => <= (L-1)+(S-1) = 94 samples = 5.88 ms at 16 kHz
  (L=64, S=32). No other lookahead exists in the network.

Receptive field (past context of one mask frame)
-------------------------------------------------
TCN: R repeats x X dilated depthwise convs, kernel P=3, dilations
1,2,...,2^(X-1). Past span in frames = R * sum_x (P-1)*d_x
= 2 * 2 * (1+2+...+64) = 508 frames; x stride 32 samples (+ encoder
window reach L-1) = 16319 samples ~= 1.02 s of past context, 0 future.
Frame geometry (L=64, S=32: 4 ms window, 2 ms hop) was chosen so a
~2000-step screen fits a CPU budget; it is coarser than the 2 ms/1 ms
geometry of the original 8 kHz Conv-TasNet and is a stated limitation.
"""
from __future__ import annotations
import torch, torch.nn as nn, torch.nn.functional as F

FS = 16000
# Architecture constants (single source of truth for train/eval).
ENC_L = 64          # encoder/decoder kernel (samples) = 4.0 ms
ENC_S = 32          # encoder/decoder stride (samples) = 2.0 ms hop
N_ENC = 160         # encoder basis channels
B_BOT = 80          # bottleneck channels
H_TCN = 160         # TCN hidden channels
SC_TCN = 80         # skip channels
P_KER = 3           # depthwise kernel
X_BLOCKS = 7        # dilated blocks per repeat (dilations 1..64)
R_REPEATS = 2       # TCN repeats
DELAY = ENC_L - 1   # fixed output content delay (samples); see docstring


def cumulative_layernorm(x: torch.Tensor, weight, bias, eps=1e-8):
    """cLN over channels with cumulative (<=t) statistics. x: (B,C,T)."""
    c = x.shape[1]
    s1 = x.sum(dim=1, keepdim=True).cumsum(dim=-1)            # (B,1,T)
    s2 = (x * x).sum(dim=1, keepdim=True).cumsum(dim=-1)
    count = torch.arange(1, x.shape[-1] + 1, device=x.device,
                         dtype=x.dtype).view(1, 1, -1) * c
    mean = s1 / count
    var = (s2 / count - mean * mean).clamp(min=0.0)
    y = (x - mean) / torch.sqrt(var + eps)
    if weight is not None:
        y = y * weight.view(1, -1, 1) + bias.view(1, -1, 1)
    return y


class CLN(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(channels))
        self.bias = nn.Parameter(torch.zeros(channels))
    def forward(self, x):
        return cumulative_layernorm(x, self.weight, self.bias)


class CausalConv1d(nn.Module):
    """Conv1d with left-only padding (padding=0 in the conv itself)."""
    def __init__(self, cin, cout, kernel, dilation=1, groups=1, stride=1):
        super().__init__()
        self.left_pad = (kernel - 1) * dilation
        self.conv = nn.Conv1d(cin, cout, kernel, stride=stride,
                              padding=0, dilation=dilation, groups=groups)
    def forward(self, x):
        if self.left_pad:
            x = F.pad(x, (self.left_pad, 0))
        return self.conv(x)


class TCNBlock(nn.Module):
    def __init__(self, dilation):
        super().__init__()
        self.conv1 = nn.Conv1d(B_BOT, H_TCN, 1, padding=0)
        self.act1 = nn.PReLU()
        self.dw = CausalConv1d(H_TCN, H_TCN, P_KER, dilation=dilation,
                               groups=H_TCN)
        self.norm = CLN(H_TCN)
        self.act2 = nn.PReLU()
        self.res = nn.Conv1d(H_TCN, B_BOT, 1, padding=0)
        self.skip = nn.Conv1d(H_TCN, SC_TCN, 1, padding=0)
    def forward(self, x):
        y = self.act1(self.conv1(x))
        y = self.act2(self.norm(self.dw(y)))
        return x + self.res(y), self.skip(y)


class CausalTasNetEnh(nn.Module):
    """x (B,T) waveform -> enhanced waveform (B,T), delayed by DELAY.

    The raw output estimates clean shifted right by DELAY samples:
    out[..., DELAY + n] estimates clean[..., n]. Use delay_target() for
    training targets and undelay() for metric alignment.
    """
    def __init__(self):
        super().__init__()
        self.encoder = nn.Conv1d(1, N_ENC, ENC_L, stride=ENC_S, padding=0)
        self.bott_norm = CLN(N_ENC)
        self.bott = nn.Conv1d(N_ENC, B_BOT, 1, padding=0)
        self.blocks = nn.ModuleList(
            TCNBlock(dilation=2 ** i)
            for _ in range(R_REPEATS) for i in range(X_BLOCKS))
        self.mask_norm = CLN(SC_TCN)
        self.mask_act = nn.PReLU()
        self.mask_head = nn.Conv1d(SC_TCN, N_ENC, 1, padding=0)
        self.decoder = nn.ConvTranspose1d(N_ENC, 1, ENC_L, stride=ENC_S,
                                          padding=0)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)
        t_in = x.shape[-1]
        w = F.relu(self.encoder(F.pad(x, (ENC_L - 1, 0))))   # (B,N,Tf)
        y = self.bott(self.bott_norm(w))
        skip_sum = None
        for blk in self.blocks:
            y, sk = blk(y)
            skip_sum = sk if skip_sum is None else skip_sum + sk
        m = torch.sigmoid(self.mask_head(self.mask_act(
            self.mask_norm(skip_sum))))
        out = self.decoder(w * m)                            # starts at 0
        if out.shape[-1] >= t_in:
            out = out[..., :t_in]
        else:
            out = F.pad(out, (0, t_in - out.shape[-1]))
        return out.squeeze(1)

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def delay_target(clean):
    """Clean waveform shifted right by DELAY (training target)."""
    return F.pad(clean, (DELAY, 0))[..., :clean.shape[-1]]


def undelay(est):
    """Shift a raw model output left by DELAY back to clean timing."""
    import numpy as np
    est = np.asarray(est)
    out = np.zeros_like(est)
    out[..., :est.shape[-1] - DELAY] = est[..., DELAY:]
    return out


def receptive_field():
    frames = 1 + R_REPEATS * sum((P_KER - 1) * 2 ** i
                                 for i in range(X_BLOCKS))
    past_samples = (frames - 1) * ENC_S + (ENC_L - 1)
    return {"rf_frames_incl_current": frames,
            "past_context_samples": past_samples,
            "past_context_s": past_samples / FS,
            "future_samples": 0,
            "algorithmic_latency_samples_max": (ENC_L - 1) + (ENC_S - 1),
            "algorithmic_latency_ms_max":
                ((ENC_L - 1) + (ENC_S - 1)) / FS * 1000.0,
            "content_delay_samples": DELAY}


def audit_causality(model):
    """Static audit: every conv padding==0; no LN/BN other than CLN."""
    bad = []
    for name, m in model.named_modules():
        if isinstance(m, (nn.Conv1d, nn.ConvTranspose1d)):
            pad = m.padding if isinstance(m.padding, tuple) else (m.padding,)
            if any(p != 0 for p in pad):
                bad.append((name, "nonzero conv padding", m.padding))
        if isinstance(m, (nn.LayerNorm, nn.BatchNorm1d, nn.GroupNorm,
                          nn.InstanceNorm1d)):
            bad.append((name, "non-causal norm", type(m).__name__))
    return bad


@torch.no_grad()
def suffix_invariance_test(model, seed=0, splits=(8000, 16000, 24001),
                           total=32000):
    """Inputs identical for first P samples, differing after: raw outputs
    must be bit-identical for the first P samples (max|diff| == 0.0)."""
    model.eval()
    g = torch.Generator().manual_seed(seed)
    results = []
    for p in splits:
        base = torch.randn(1, total, generator=g) * 0.1
        alt = base.clone()
        alt[..., p:] = torch.randn(1, total - p, generator=g) * 0.5
        d = (model(base) - model(alt)).abs()
        results.append({"split_P": p, "max_diff_prefix_P":
                        float(d[..., :p].max()),
                        "max_diff_suffix": float(d[..., p:].max())})
    return results


if __name__ == "__main__":
    import json, time
    torch.manual_seed(0)
    m = CausalTasNetEnh()
    print("params:", m.count_parameters())
    print("receptive_field:", json.dumps(receptive_field(), indent=1))
    print("audit (empty=clean):", audit_causality(m))
    for r in suffix_invariance_test(m):
        print("suffix:", r)
        assert r["max_diff_prefix_P"] == 0.0, "CAUSALITY VIOLATED"
    x = torch.randn(8, 32000) * 0.1
    t0 = time.time(); y = m(x); print(f"fwd batch8x2s: {time.time()-t0:.2f}s")
    loss = y.pow(2).mean(); t0 = time.time(); loss.backward()
    print(f"bwd: {time.time()-t0:.2f}s")
    print("SELF-TEST OK")
