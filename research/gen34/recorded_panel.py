"""Gen34 frozen real-recording audit (Astra's Gen33 review, rank 1): what do Gen19 and the fixed Gen32 candidate do
to ACOUSTICALLY RECORDED bilateral speech in reverberation? Evaluation only: no training, selection or gate change,
and no model advancement.

Asset: BRUDEX (Fejgin, Middelberg, Doclo, Univ. Oldenburg; MIT; doi 10.5281/zenodo.8340195), one laboratory with
three reverberation settings (T60 ~ 0.31 / 0.51 / 1.3 s; DRR ~ 3.5 / -0.5 / -4.0 dB). Talkers SPK1-2 female, SPK3-4
male, recorded from loudspeakers 2 m from a KEMAR dummy head; channel 1 = front-left and channel 3 = front-right
hearing-aid microphone; one recording run (eMicRun 1) for speech and noise. Azimuth 0 deg = front, negative = left.

Grid (fixed): 4 talkers x 3 settings x target azimuth {-60,-30,+30,+60} x SNR {-5,0,+5,+10} dB = 192 noisy items, plus
48 target-only items. Mixtures are DIGITAL SUMS of separately recorded components (labelled as such): the recorded
talker plus the recorded babble (played from four corner loudspeakers) of the same setting and run. The SNR is set
from summed bilateral energy over the scoring window with ONE noise multiplier shared by both ears, so interaural
level and time differences are preserved. 48 kHz -> 16 kHz (resample_poly 1:3). Each stereo input is scaled by one
gain to RMS 0.14 (the published enhance.py convention), also shared by both ears.
Scoring window: from 1 s to the end of each file (BRUDEX short files are <= 10 s and vary, e.g. SPK1 7.65 s; Astra's
11 s spec assumed longer files, see prereg). Reference for each ear = that ear's recorded isolated talker (reverberant): this tests
noise removal and speech preservation, NOT dereverberation.

Systems: bypass; Gen19 seed 17 independent per ear; Gen32 alpha=0.7 independent per ear (both frozen).
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / "gen24")); sys.path.insert(0, str(R / "gen33")); sys.path.insert(0, str(R / "bench-n6"))
from train13 import _si_sdr_np  # noqa: E402  established, mean-removed

DATA = Path("/tmp/brudex_dl/data")
TALKERS = (1, 2, 3, 4)
SETTINGS = ("low", "medium", "high")
AZ = (-60, -30, 30, 60)
SNRS = (-5.0, 0.0, 5.0, 10.0)
CH_L, CH_R = 0, 2           # front-left, front-right hearing-aid microphones (README channel order)
FS_IN, FS = 48000, 16000
T0 = FS                     # scoring starts at 1 s
RMS_IN = 0.14


def _read_mat(path):
    """Largest 2-D numeric dataset in a MAT v7.3 (HDF5) file, as (channels, samples) float64. Data only."""
    import h5py
    best = None
    with h5py.File(path, "r") as f:
        def visit(name, obj):
            nonlocal best
            if isinstance(obj, h5py.Dataset) and obj.ndim == 2 and obj.dtype.kind == "f":
                if best is None or obj.size > best[1].size:
                    best = (name, obj[()])
        f.visititems(visit)
    assert best is not None, f"no 2-D float dataset in {path}"
    a = np.asarray(best[1], dtype=np.float64)
    return (a if a.shape[0] < a.shape[1] else a.T), best[0]


def speech_path(t, s, az):
    return DATA / f"SPK{t}short_{s}_eMicRun_1_DOA_{az}deg.mat"


def noise_path(s):
    return DATA / f"noiseBabbleShort_{s}_eMicRun_1.mat"


def load_pair(path):
    a, key = _read_mat(path)
    assert a.shape[0] == 18, f"{path.name}: {a.shape[0]} channels, expected 18"
    L, Rr = (resample_poly(a[c], 1, 3) for c in (CH_L, CH_R))
    return L.astype(np.float64), Rr.astype(np.float64), key


def make_item(sL, sR, nL, nR, snr):
    """Digital sum of recorded components. SNR from summed bilateral energy over the scoring window, with ONE noise
    multiplier for both ears; then ONE gain for both ears to stereo RMS 0.14. snr=None -> target only."""
    if snr is None:
        mL, mR = sL.copy(), sR.copy()
    else:
        es = np.sum(sL[T0:] ** 2) + np.sum(sR[T0:] ** 2)
        en = np.sum(nL[T0:] ** 2) + np.sum(nR[T0:] ** 2)
        g = np.sqrt(es / (en * 10 ** (snr / 10)))
        mL, mR = sL + g * nL, sR + g * nR
    k = RMS_IN / (np.sqrt(0.5 * (np.mean(mL ** 2) + np.mean(mR ** 2))) + 1e-12)
    return {"mL": (k * mL).astype(np.float32), "mR": (k * mR).astype(np.float32),
            "rL": (k * sL).astype(np.float32), "rR": (k * sR).astype(np.float32)}


def build():
    """All 240 items, deterministic. Returns (items, material_sha256, meta)."""
    noise = {s: load_pair(noise_path(s))[:2] for s in SETTINGS}
    items, h, meta = [], hashlib.sha256(), {"datasets": {}}
    for t in TALKERS:
        for s in SETTINGS:
            for az in AZ:
                sL, sR, key = load_pair(speech_path(t, s, az))
                meta["datasets"][speech_path(t, s, az).name] = key
                n = min(len(sL), len(noise[s][0]))
                for snr in SNRS + (None,):
                    it = {"talker": t, "setting": s, "az": az, "snr": snr, "cond": "target_only" if snr is None else "noisy",
                          **make_item(sL[:n], sR[:n], noise[s][0][:n], noise[s][1][:n], snr)}
                    h.update(f"{t}|{s}|{az}|{snr}".encode())
                    for x in ("mL", "mR", "rL", "rR"):
                        h.update(it[x].tobytes())
                    items.append(it)
    return items, h.hexdigest(), meta


METRICS = ("sisdr_L", "sisdr_R", "stoi_L", "stoi_R", "wave_err_L", "wave_err_R",
           "ild_target_err_db", "ild_mixture_dist_db", "itd_err_samples")


def metrics(rL, rR, oL, oR, mL, mR):
    """Per-ear SI-SDR/STOI and gain-sensitive waveform error vs each ear's recorded isolated talker; target-ILD error
    (output vs isolated talker) and mixture-ILD distortion (output vs input mixture); ITD error. Window: 1 s to end."""
    from pystoi import stoi
    from spatial import ild_per_band, itd_samples
    w = slice(T0, None)
    out = {}
    for e, r, o in (("L", rL, oL), ("R", rR, oR)):
        out[f"sisdr_{e}"] = _si_sdr_np(r[w], o[w])
        out[f"stoi_{e}"] = float(stoi(r[w].astype(np.float64), o[w].astype(np.float64), FS, extended=False))
        r64, o64 = r[w].astype(np.float64), o[w].astype(np.float64)
        out[f"wave_err_{e}"] = float(10 * np.log10((np.sum((o64 - r64) ** 2) + 1e-20) / (np.sum(r64 ** 2) + 1e-20)))
    ild_t, ild_o = ild_per_band(rL[w], rR[w]), ild_per_band(oL[w], oR[w])
    out["ild_target_err_db"] = float(np.mean(np.abs(ild_o - ild_t)))
    out["ild_mixture_dist_db"] = float(np.mean(np.abs(ild_o - ild_per_band(mL[w], mR[w]))))
    out["itd_err_samples"] = float(abs(itd_samples(oL[w], oR[w]) - itd_samples(rL[w], rR[w])))
    return out


def run_system(items, name, ckpt=None):
    """Rows for one system. bypass returns the input unchanged."""
    import linked
    fn = (lambda L, R_: (L, R_)) if ckpt is None else linked.pair_fn(ckpt, "independent")
    rows = []
    for it in items:
        oL, oR = fn(it["mL"].copy(), it["mR"].copy())
        oL, oR = np.asarray(oL, dtype=np.float32), np.asarray(oR, dtype=np.float32)
        rec = {"system": name, **{k: it[k] for k in ("talker", "setting", "az", "snr", "cond")}}
        rec.update(metrics(it["rL"], it["rR"], oL, oR, it["mL"], it["mR"]))
        if ckpt is None:
            rec["bypass_identical"] = bool(np.array_equal(oL, it["mL"]) and np.array_equal(oR, it["mR"]))
        rows.append(rec)
    return rows
