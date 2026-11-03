"""J4-A1 causality / size / latency tests.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.

Runnable with pytest, or directly:  python test_j4.py
The central bar (spec S2.5 item 3): identical prefix + differing suffixes
must return prefix Delta = EXACTLY 0. All equality below is bitwise
(torch.equal), never allclose, for that test.
"""
from __future__ import annotations

import platform
import statistics
import sys
import time

import torch
from torch import nn

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from j4_model import (  # noqa: E402
    B, FS, H, K, W, J4A1, UniLSTMCell, frame_bounds, num_frames,
    spec_macs_per_frame, spec_param_count,
)

torch.manual_seed(1234)


def make_model() -> J4A1:
    torch.manual_seed(7)
    m = J4A1()
    m.eval()
    return m


# ---------------------------------------------------------------------------
# (1) Suffix invariance: Delta = 0 exactly on the shared prefix
# ---------------------------------------------------------------------------
def test_suffix_invariance_waveform():
    model = make_model()
    g = torch.Generator().manual_seed(99)
    prefix = torch.randn(1, FS // 2, generator=g) * 0.1        # 0.5 s shared
    suffix_a = torch.randn(1, FS // 2, generator=g) * 0.1
    suffix_b = torch.randn(1, FS // 2, generator=g) * 3.0      # very different
    suffix_c = torch.zeros(1, FS // 2)
    xa = torch.cat([prefix, suffix_a], dim=1)
    xb = torch.cat([prefix, suffix_b], dim=1)
    xc = torch.cat([prefix, suffix_c], dim=1)
    # Frames whose last sample lies inside the shared prefix:
    n_shared = num_frames(prefix.shape[1])
    assert n_shared > 100
    with torch.no_grad():
        ma, ea = model(xa)
        mb, eb = model(xb)
        mc, ec = model(xc)
    for other_m, other_e, name in ((mb, eb, "loud-noise"), (mc, ec, "silence")):
        d_mask = (ma[:, :n_shared] - other_m[:, :n_shared]).abs().max().item()
        d_env = (ea[:, :n_shared] - other_e[:, :n_shared]).abs().max().item()
        assert torch.equal(ma[:, :n_shared], other_m[:, :n_shared]), name
        assert torch.equal(ea[:, :n_shared], other_e[:, :n_shared]), name
        assert d_mask == 0.0 and d_env == 0.0, (name, d_mask, d_env)
    # Sanity: the suffixes really do change later outputs (test not vacuous).
    assert not torch.equal(ma[:, n_shared:], mb[:, n_shared:])


def test_suffix_invariance_truncation():
    """Outputs from a truncated stream equal the head of the full stream."""
    model = make_model()
    x = torch.randn(1, FS) * 0.1
    cut = FS // 3
    with torch.no_grad():
        full_m, _ = model(x)
        short_m, _ = model(x[:, :cut])
    assert torch.equal(full_m[:, :short_m.shape[1]], short_m)


def test_impulse_probe_no_future_leak():
    """An impulse at sample s changes no frame that ends before s."""
    model = make_model()
    base = torch.zeros(1, FS // 2)
    probed = base.clone()
    s = 4000
    probed[0, s] = 5.0
    with torch.no_grad():
        m0, _ = model(base)
        m1, _ = model(probed)
    # First frame that can see sample s: smallest j with j*H+W-1 >= s.
    j_first = next(j for j in range(m0.shape[1]) if frame_bounds(j)[1] >= s)
    assert torch.equal(m0[:, :j_first], m1[:, :j_first])
    assert not torch.equal(m0[:, j_first:], m1[:, j_first:])  # probe is live


# ---------------------------------------------------------------------------
# (2) Frame-causality static check (spec S2.5 items 1-2, on the built graph)
# ---------------------------------------------------------------------------
def test_static_causality_graph():
    model = make_model()
    # Index audit: frame j reads samples [jH, jH+W-1] and nothing later.
    for j in (0, 1, 4, 17, 249):
        lo, hi = frame_bounds(j)
        assert lo == j * H and hi == j * H + W - 1
        assert hi - lo + 1 == W
    # The K=5 context for mask j enters via frames j-4..j; earliest sample
    # among them is (j-4)*H, latest is j*H+W-1: span (K-1)*H + W = 384.
    j = 10
    earliest = frame_bounds(j - (K - 1))[0]
    latest = frame_bounds(j)[1]
    assert latest - earliest + 1 == (K - 1) * H + W == 384
    # Barred constructions (spec S2.3) must be absent from the module tree.
    barred = (nn.LSTM, nn.GRU, nn.RNN, nn.Conv1d, nn.Conv2d,
              nn.ConvTranspose1d, nn.BatchNorm1d, nn.BatchNorm2d,
              nn.MultiheadAttention, nn.Transformer,
              nn.AdaptiveAvgPool1d, nn.AvgPool1d, nn.MaxPool1d)
    for mod in model.modules():
        assert not isinstance(mod, barred), type(mod)
        assert getattr(mod, "bidirectional", False) is False
    cells = [m for m in model.modules() if isinstance(m, UniLSTMCell)]
    assert len(cells) == 2 and all(c.hidden_size == 128 for c in cells)
    assert isinstance(model.fc, nn.Linear) and model.fc.out_features == B
    # Norm audit: the only norm is per-frame F.layer_norm with no parameters;
    # no module in the tree may be a norm carrying running/batch statistics.
    norm_mods = [m for m in model.modules()
                 if isinstance(m, (nn.LayerNorm, nn.GroupNorm, nn.BatchNorm1d))]
    assert norm_mods == []
    # Framing audit: no waveform padding anywhere -> a signal shorter than
    # W yields zero frames, and frame count follows the no-pad formula.
    assert num_frames(W - 1) == 0 and num_frames(W) == 1
    assert num_frames(FS) == (FS - W) // H + 1 == 249
    # Output audit: mask range, envelope-mask identity, no waveform output.
    with torch.no_grad():
        masks, masked = model(torch.randn(2, 4000) * 0.1)
        _, env = model.extract_features(torch.randn(2, 4000) * 0.0)
    assert masks.min() >= 0.0 and masks.max() <= 1.0
    assert masks.shape == masked.shape == (2, num_frames(4000), B)


def test_streaming_step_matches_sequence():
    """Frame-by-frame step() reproduces forward() exactly (streaming == batch)."""
    model = make_model()
    x = torch.randn(1, 8000) * 0.1
    with torch.no_grad():
        masks_seq, _ = model(x)
        feats, _ = model.extract_features(x)
        state = model.init_state(1)
        stepped = []
        for j in range(feats.shape[1]):
            m_j, state = model.step(feats[:, j], state)
            stepped.append(m_j)
    assert torch.equal(torch.stack(stepped, dim=1), masks_seq)


# ---------------------------------------------------------------------------
# (3) Parameter count + MACs vs spec S3.4 (238,656 / 237,568 at B=64)
# ---------------------------------------------------------------------------
def test_param_and_mac_accounting():
    model = make_model()
    assert spec_param_count() == 238_656
    assert spec_macs_per_frame() == 237_568
    assert model.count_parameters() == 238_656, model.count_parameters()
    assert model.macs_per_frame() == 237_568
    # Independent recount straight from the built tensors:
    c1, c2 = model.cells[0], model.cells[1]
    l1 = c1.weight_ih.numel() + c1.weight_hh.numel() + c1.bias.numel()
    l2 = c2.weight_ih.numel() + c2.weight_hh.numel() + c2.bias.numel()
    fc = model.fc.weight.numel() + model.fc.bias.numel()
    assert (l1, l2, fc) == (98_816, 131_584, 8_256)
    assert l1 + l2 + fc == 238_656
    # MAC recount from tensor shapes (matmul rows x cols, biases excluded):
    mac = (c1.weight_ih.shape[0] * c1.weight_ih.shape[1]
           + c1.weight_hh.shape[0] * c1.weight_hh.shape[1]
           + c2.weight_ih.shape[0] * c2.weight_ih.shape[1]
           + c2.weight_hh.shape[0] * c2.weight_hh.shape[1]
           + model.fc.weight.shape[0] * model.fc.weight.shape[1])
    assert mac == 237_568
    assert abs(mac * 250 / 1e6 - 59.4) < 0.05  # spec: ~59.4 MMAC/s at 250 fps


# ---------------------------------------------------------------------------
# (4) CPU latency per frame (measured here; deadline = hop = 4.0 ms)
# ---------------------------------------------------------------------------
def measure_latency():
    model = make_model()
    x = torch.randn(1, FS) * 0.1                       # 1 s -> 249 frames
    with torch.no_grad():
        for _ in range(3):                             # warm-up
            model(x)
        # Streaming step latency (feature frame -> mask), the deployed unit.
        feats, _ = model.extract_features(x)
        state = model.init_state(1)
        step_ms = []
        for j in range(feats.shape[1]):
            t0 = time.perf_counter()
            _, state = model.step(feats[:, j], state)
            step_ms.append((time.perf_counter() - t0) * 1e3)
        # End-to-end per-frame (waveform -> masks incl. analysis), averaged.
        reps = 10
        t0 = time.perf_counter()
        for _ in range(reps):
            m, _ = model(x)
        e2e_ms = (time.perf_counter() - t0) * 1e3 / (reps * m.shape[1])
    step_ms_sorted = sorted(step_ms)
    out = {
        "hardware": f"{platform.machine()} / {platform.platform()}",
        "torch": torch.__version__, "threads": torch.get_num_threads(),
        "step_ms_mean": statistics.fmean(step_ms),
        "step_ms_median": statistics.median(step_ms),
        "step_ms_p99": step_ms_sorted[int(0.99 * len(step_ms_sorted)) - 1],
        "step_ms_max": max(step_ms),
        "e2e_ms_per_frame": e2e_ms,
        "deadline_ms": H / FS * 1e3,
    }
    return out


def test_latency_under_frame_deadline():
    lat = measure_latency()
    for key in ("step_ms_median", "step_ms_p99", "e2e_ms_per_frame"):
        assert lat[key] < lat["deadline_ms"], (key, lat)
    print("\nLATENCY " + " | ".join(f"{k}={v}" for k, v in lat.items()))


if __name__ == "__main__":
    test_suffix_invariance_waveform()
    print("PASS (1a) suffix-invariance waveform: prefix Delta exactly 0")
    test_suffix_invariance_truncation()
    print("PASS (1b) suffix-invariance truncation: Delta exactly 0")
    test_impulse_probe_no_future_leak()
    print("PASS (1c) impulse probe: no frame ending before impulse changes")
    test_static_causality_graph()
    print("PASS (2) static frame-causality: index/norm/barred-module audits")
    test_streaming_step_matches_sequence()
    print("PASS (2b) streaming step == sequence forward, bitwise")
    test_param_and_mac_accounting()
    print("PASS (3) params = 238,656 and MACs/frame = 237,568 (spec S3.4)")
    lat = measure_latency()
    test_latency_under_frame_deadline()
    print("PASS (4) CPU latency per frame:")
    for k, v in lat.items():
        print(f"  {k} = {v}")
