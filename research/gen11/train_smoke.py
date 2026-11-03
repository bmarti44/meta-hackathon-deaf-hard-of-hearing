"""J4-A1 training smoke test -- T0 ONLY, not efficacy evidence.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.

Synthetic speech-like signals (harmonic stacks with formant-ish spectral
tilt, amplitude modulation, random f0 tracks) mixed with white noise.
Target = ideal ratio mask in the model's own filterbank, computed offline
from the clean/noise components (admissible: spec S4 -- the deployed graph
is what S2.5 audits). 200 Adam steps; success = mask-MSE decreases.
This says nothing about SRT, listeners, or benefit. It only shows the
graph trains end-to-end and gradients flow through the causal path.
"""
from __future__ import annotations

import math
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from j4_model import EPS, FS, J4A1  # noqa: E402


def synth_batch(batch: int, seconds: float, gen: torch.Generator):
    n = int(FS * seconds)
    t = torch.arange(n) / FS
    clean = torch.zeros(batch, n)
    for i in range(batch):
        f0 = 90.0 + 160.0 * torch.rand(1, generator=gen).item()
        # slow f0 wander
        f0_track = f0 * (1.0 + 0.08 * torch.sin(2 * math.pi * 0.7 * t
                                                 + 6.28 * torch.rand(1, generator=gen).item()))
        phase = 2 * math.pi * torch.cumsum(f0_track, 0) / FS
        sig = torch.zeros(n)
        n_harm = max(1, int(4000 // f0))
        for h in range(1, n_harm + 1):
            tilt = 1.0 / h                                   # spectral tilt
            formant = 1.0 + 1.5 * math.exp(-((h * f0 - 800.0) ** 2) / (2 * 350.0 ** 2)) \
                          + 1.0 * math.exp(-((h * f0 - 2400.0) ** 2) / (2 * 500.0 ** 2))
            sig += tilt * formant * torch.sin(h * phase + 6.28 * torch.rand(1, generator=gen).item())
        # syllabic amplitude modulation (~4 Hz) with voicing gaps
        am = 0.5 + 0.5 * torch.sin(2 * math.pi * 4.0 * t + 6.28 * torch.rand(1, generator=gen).item())
        am = torch.where(am > 0.25, am, torch.zeros_like(am))
        clean[i] = sig * am
    clean = clean / (clean.abs().amax(dim=1, keepdim=True) + 1e-9) * 0.3
    noise = torch.randn(batch, n, generator=gen)
    noise = noise / (noise.abs().amax(dim=1, keepdim=True) + 1e-9) * 0.3
    snr_db = -5.0 + 15.0 * torch.rand(batch, 1, generator=gen)
    p_c = clean.pow(2).mean(dim=1, keepdim=True)
    p_n = noise.pow(2).mean(dim=1, keepdim=True)
    noise = noise * torch.sqrt(p_c / (p_n * 10 ** (snr_db / 10.0) + 1e-12))
    return clean, noise, clean + noise


def band_energy(model: J4A1, wav: torch.Tensor) -> torch.Tensor:
    _, env = model.extract_features(wav)
    return env ** 2  # envelope is sqrt(energy + eps); square for ratio mask


def main(steps: int = 200, seed: int = 2026) -> dict:
    torch.manual_seed(seed)
    gen = torch.Generator().manual_seed(seed)
    model = J4A1()
    opt = torch.optim.Adam(model.parameters(), lr=3e-3)
    losses: list[float] = []
    t0 = time.perf_counter()
    for step in range(steps):
        clean, noise, mix = synth_batch(batch=8, seconds=0.5, gen=gen)
        with torch.no_grad():
            e_c = band_energy(model, clean)
            e_n = band_energy(model, noise)
            irm = torch.sqrt(e_c / (e_c + e_n + EPS))        # target mask
        masks, _ = model(mix)
        loss = F.mse_loss(masks, irm)
        opt.zero_grad()
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step()
        losses.append(loss.item())
        if step % 50 == 0 or step == steps - 1:
            print(f"step {step:3d}  mask-MSE {loss.item():.5f}  |g| {grad_norm:.3f}")
    wall = time.perf_counter() - t0
    first10 = sum(losses[:10]) / 10
    last10 = sum(losses[-10:]) / 10
    out = {"steps": steps, "loss_first10": first10, "loss_last10": last10,
           "loss_step0": losses[0], "loss_final": losses[-1],
           "decreased": last10 < first10, "wall_s": wall}
    print(f"first10 mean {first10:.5f} -> last10 mean {last10:.5f} "
          f"({'DECREASED' if out['decreased'] else 'DID NOT DECREASE'}) in {wall:.1f}s")
    print("SMOKE " + " | ".join(f"{k}={v}" for k, v in out.items()))
    return out


if __name__ == "__main__":
    result = main()
    sys.exit(0 if result["decreased"] else 1)
