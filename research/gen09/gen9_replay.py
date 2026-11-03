"""Gen9 checkpoint replay: prefix/suffix future-dependence test.
cankeles/ConvTasNet_WHAMR_enhsingle_16k, hash-verified copy at /tmp/gen9_pytorch_model.bin
Synthetic audio only. Same 1.0s prefix, different 1.0s suffixes; measure output
change inside the common prefix (past). Causal system must give exactly 0 there
(up to any whole-segment framing boundary it declares; this model declares none).
"""
import hashlib, time
import numpy as np
import torch
from asteroid.models import ConvTasNet

SR = 16000
CKPT = "/tmp/gen9_pytorch_model.bin"
EXPECTED_SHA = "a96014fc1ddf9bf45bb43f2143799d9941907b8bbbbd833f69b27406d3b9026a"

sha = hashlib.sha256(open(CKPT, "rb").read()).hexdigest()
print(f"sha256={sha}")
print(f"sha_match={sha == EXPECTED_SHA}")
assert sha == EXPECTED_SHA

torch.manual_seed(0)
np.random.seed(0)
ckpt = torch.load(CKPT, map_location="cpu", weights_only=False)
args = dict(ckpt["model_args"])
print(f"model_args={args}")
model = ConvTasNet(**args)
res = model.load_state_dict(ckpt["state_dict"], strict=True)
print(f"load_state_dict_strict={res}")
model.eval()
print(f"params={sum(p.numel() for p in model.parameters())}")
print(f"torch={torch.__version__} threads={torch.get_num_threads()}")

# --- synthetic signals (deterministic) ---
rng = np.random.default_rng(1234)
t_pre = np.arange(SR) / SR          # 1.0 s prefix
t_suf = np.arange(SR, 2 * SR) / SR  # 1.0 s suffix
# speech-like-ish prefix: harmonic tone complex + noise, amplitude-modulated
prefix = (0.25 * np.sin(2 * np.pi * 180 * t_pre)
          + 0.12 * np.sin(2 * np.pi * 360 * t_pre)
          + 0.06 * np.sin(2 * np.pi * 720 * t_pre))
prefix = prefix * (0.7 + 0.3 * np.sin(2 * np.pi * 4 * t_pre))
prefix = prefix + 0.05 * rng.standard_normal(SR)
prefix = prefix.astype(np.float32)

suffix_zero = np.zeros(SR, dtype=np.float32)
suffix_loud = (0.6 * rng.standard_normal(SR)).astype(np.float32)
suffix_tone = (0.4 * np.sin(2 * np.pi * 1000 * t_suf)).astype(np.float32)
# suffix that continues the prefix generator (a 'natural continuation' control)
cont = (0.25 * np.sin(2 * np.pi * 180 * t_suf)
        + 0.12 * np.sin(2 * np.pi * 360 * t_suf)
        + 0.06 * np.sin(2 * np.pi * 720 * t_suf))
cont = cont * (0.7 + 0.3 * np.sin(2 * np.pi * 4 * t_suf))
suffix_cont = (cont + 0.05 * rng.standard_normal(SR)).astype(np.float32)

def run(x_np):
    x = torch.from_numpy(x_np[None, :])
    t0 = time.perf_counter()
    with torch.no_grad():
        y = model(x)
    dt = time.perf_counter() - t0
    y = y[0, 0].numpy() if y.ndim == 3 else y[0].numpy()
    return y.astype(np.float64), dt

def stats(name, a, b, lo, hi):
    d = a[lo:hi] - b[lo:hi]
    ref = a[lo:hi]
    rms_d = float(np.sqrt(np.mean(d ** 2)))
    rms_r = float(np.sqrt(np.mean(ref ** 2)))
    snr = float(20 * np.log10(rms_r / rms_d)) if rms_d > 0 else float("inf")
    print(f"{name:28s} win=[{lo/SR:.2f},{hi/SR:.2f})s maxabs={np.max(np.abs(d)):.6g} "
          f"rms_diff={rms_d:.6g} rms_ref={rms_r:.6g} rel={rms_d/rms_r if rms_r else float('nan'):.6g} "
          f"snr_prefix={snr:.2f}dB nonzero={int(np.count_nonzero(d))}/{hi-lo}")
    return rms_d, rms_r

x_zero = np.concatenate([prefix, suffix_zero])
x_loud = np.concatenate([prefix, suffix_loud])
x_tone = np.concatenate([prefix, suffix_tone])
x_cont = np.concatenate([prefix, suffix_cont])

y_zero, dt1 = run(x_zero)
y_zero2, dt2 = run(x_zero)   # determinism control: identical input twice
y_loud, dt3 = run(x_loud)
y_tone, dt4 = run(x_tone)
y_cont, dt5 = run(x_cont)
print(f"forward_times_s={[round(v,3) for v in [dt1,dt2,dt3,dt4,dt5]]} len_out={len(y_zero)}")
print(f"input_prefix_identical={bool(np.array_equal(x_zero[:SR], x_loud[:SR]))}")
print(f"out_rms zero={np.sqrt(np.mean(y_zero**2)):.6g} loud={np.sqrt(np.mean(y_loud**2)):.6g} "
      f"tone={np.sqrt(np.mean(y_tone**2)):.6g} cont={np.sqrt(np.mean(y_cont**2)):.6g}")

windows = [(0, SR), (0, int(0.2*SR)), (0, int(0.5*SR)), (int(0.5*SR), SR),
           (int(0.9*SR), SR), (0, int(0.235*SR))]
# 0-0.235s is >765ms before suffix onset at 1.0s: outside even the convolutional
# future reach recomputed in Gen8; only segment-wide gLN can affect it.
for lo, hi in windows:
    stats("CONTROL identical-input", y_zero, y_zero2, lo, hi)
for lo, hi in windows:
    stats("zero-vs-LOUD suffix", y_zero, y_loud, lo, hi)
for lo, hi in windows:
    stats("zero-vs-TONE suffix", y_zero, y_tone, lo, hi)
for lo, hi in windows:
    stats("cont-vs-LOUD suffix", y_cont, y_loud, lo, hi)

# First sample index where zero-vs-loud outputs differ at all / materially
d = np.abs(y_zero - y_loud)
nz = np.flatnonzero(d > 0)
mat = np.flatnonzero(d > 1e-4)
print(f"first_nonzero_diff_sample={int(nz[0]) if len(nz) else -1} ({(int(nz[0])/SR if len(nz) else -1):.4f}s)")
print(f"first_diff_gt_1e-4_sample={int(mat[0]) if len(mat) else -1} ({(int(mat[0])/SR if len(mat) else -1):.4f}s)")
print("DONE")
