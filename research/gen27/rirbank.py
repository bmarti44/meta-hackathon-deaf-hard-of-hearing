"""Gen 27 RIR bank: frozen-manifest loader and acoustic helpers.

Shared by build_rir_bank.py (freezes the manifest), train14.py (training
augmentation) and panel_rev.py (reverberant screen). RIR audio lives
outside git under /tmp/rirs/RIRS_NOISES; the manifest pins every file by
sha256 and every derived number used downstream.

Preprocessing, identical everywhere and fixed before any training:
  1. read channel 0 of the wav (OpenSLR 28 is 16 kHz), as float64;
  2. truncate to L_MAX samples with a 10 ms raised-cosine fade at the cut
     (applied only when the file is longer than L_MAX);
  3. multiply by the room's single gain constant (manifest `room_gain`),
     chosen so the mean RIR energy in that room is 1. One constant per room
     keeps the relative source levels within a room physical.
The early (training-reference) RIR is the preprocessed RIR times
early_window(): 1 up to direct arrival + 45 ms, a half-cosine taper over
the final 5 ms, 0 from direct arrival + 50 ms on. Direct arrival:
direct_index() (superseding rule: first sample within 20 dB of the peak,
refined to the local max within 1 ms; the v1 argmax rule is kept as
direct_index_peak for the versioned v1 evidence only).
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np
import scipy.fft as sfft

FS = 16000
L_MAX = 16000            # 1.0 s RIR cap (RT60 <= 0.8 s strata)
FADE = int(0.010 * FS)   # 10 ms fade at the truncation point
EARLY_MS = 50.0          # target keeps direct + reflections through 50 ms
TAPER_MS = 5.0           # final 5 ms of the early window tapered
RIR_ROOT = Path("/tmp/rirs/RIRS_NOISES")
FILE_ROOT = RIR_ROOT.parent  # manifest "file" paths are relative to this


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_rir(path):
    import soundfile as sf
    x, sr = sf.read(str(path), dtype="float64", always_2d=True)
    assert sr == FS, (path, sr)
    return np.ascontiguousarray(x[:, 0])


def truncate(h):
    if len(h) <= L_MAX:
        return h.copy()
    h = h[:L_MAX].copy()
    h[-FADE:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(1, FADE + 1) / FADE)
    return h


ONSET_DB = -20.0          # direct-arrival onset threshold re max|h| (ISO 3382-1 onset convention)
ONSET_REFINE = int(0.001 * FS)  # refine to the local max within 1 ms after the onset


def direct_index_peak(h):
    """Superseded v1 rule (2026-11-04 registration): largest absolute sample.
    Wrong for multi-peak RIRs where a reflection exceeds the direct path."""
    return int(np.argmax(np.abs(h)))


def direct_index(h):
    """Direct arrival (superseding rule, Astra pre-launch review blocking 1).
    onset = first sample with |h| >= 10**(ONSET_DB/20) * max|h| (-20 dB re
    peak: the ISO 3382-1 impulse-response start convention; it sits above
    measured noise floors and the image-method fractional-delay ripple, and
    below any physically plausible direct path in this bank, see
    audit_arrival.py). The arrival is then the largest |h| in
    [onset, onset + 1 ms], so the index lands on the direct pulse's peak
    rather than its first rising sample."""
    a = np.abs(h)
    onset = int(np.argmax(a >= 10 ** (ONSET_DB / 20) * a.max()))
    return onset + int(np.argmax(a[onset:onset + ONSET_REFINE + 1]))


def early_window(n, d):
    """1 through d + 45 ms, half-cosine over (d+45 ms, d+50 ms], 0 after."""
    w = np.zeros(n)
    end = d + int(round(EARLY_MS * FS / 1000))
    tap = int(round(TAPER_MS * FS / 1000))
    flat = end - tap
    w[:min(n, flat + 1)] = 1.0
    i = np.arange(flat + 1, min(n, end))
    w[i] = 0.5 + 0.5 * np.cos(np.pi * (i - flat) / tap)
    return w


def rt60_schroeder(h):
    """RT60 by Schroeder backward integration from direct arrival.
    Least-squares line on the energy decay curve between -5 and -25 dB (T20),
    falling back to -5..-15 dB (T10) when the decay never reaches -25 dB;
    RT60 = -60 / slope (s). Returns (rt60_s, method)."""
    d = direct_index(h)
    e = h[d:] ** 2
    edc = np.cumsum(e[::-1])[::-1]
    edc_db = 10 * np.log10(edc / edc[0] + 1e-300)
    t = np.arange(len(edc_db)) / FS
    for lo, hi, name in ((-5.0, -25.0, "T20"), (-5.0, -15.0, "T10")):
        sel = (edc_db <= lo) & (edc_db >= hi)
        if sel.sum() >= 10 and edc_db.min() < hi:
            slope, _ = np.polyfit(t[sel], edc_db[sel], 1)
            if slope < 0:
                return float(-60.0 / slope), name
    return float("nan"), "none"


def drr_c50(h):
    """DRR: energy within +-2.5 ms of direct arrival vs the rest.
    C50: energy up to direct + 50 ms vs after (both dB)."""
    d = direct_index(h)
    w = int(0.0025 * FS)
    e = h ** 2
    direct = e[max(0, d - w):d + w + 1].sum()
    drr = 10 * np.log10(direct / max(e.sum() - direct, 1e-300))
    c = d + int(0.050 * FS)
    c50 = 10 * np.log10(e[:c].sum() / max(e[c:].sum(), 1e-300))
    return float(drr), float(c50)


def stratum_of(rt60):
    if 0.2 <= rt60 < 0.4:
        return "short"
    if 0.4 <= rt60 < 0.6:
        return "medium"
    if 0.6 <= rt60 <= 0.8:
        return "long"
    return None


def manifest_sha(path):
    return sha256_file(path)


class Bank:
    """Preprocessed RIRs for one manifest split, with cached rfft at nfft.

    rooms[stratum] -> list of room dicts; each room dict has 'room_id',
    'stratum', 'h' (list of full RIRs), 'he' (early RIRs), and when
    nfft is given 'H'/'HE' (complex rfft, cached once)."""

    def __init__(self, manifest, splits, nfft=None, root=FILE_ROOT, verify=True):
        man = json.loads(Path(manifest).read_text())
        self.manifest_sha256 = sha256_file(manifest)
        self.nfft = nfft
        self.ctx = L_MAX
        self.rooms = {"short": [], "medium": [], "long": []}
        self.by_id = {}
        for r in man["rooms"]:
            if r["split"] not in splits:
                continue
            hs, hes, Hs, HEs, metas = [], [], [], [], []
            for f in r["rirs"]:
                p = Path(root) / f["file"]
                if verify:
                    assert sha256_file(p) == f["sha256"], f"RIR hash mismatch {p}"
                h = truncate(read_rir(p)) * r["room_gain"]
                he = h * early_window(len(h), f["direct_idx"])
                hs.append(h); hes.append(he); metas.append(f)
                if nfft:
                    # complex64 cache halves memory; products are formed in complex128
                    Hs.append(sfft.rfft(h, nfft).astype(np.complex64)); HEs.append(sfft.rfft(he, nfft).astype(np.complex64))
            room = {"room_id": r["room_id"], "stratum": r["stratum"], "split": r["split"],
                    "h": hs, "he": hes, "H": Hs, "HE": HEs, "meta": metas}
            self.rooms[r["stratum"]].append(room)
            self.by_id[r["room_id"]] = room

    def n_rirs(self):
        return sum(len(r["h"]) for v in self.rooms.values() for r in v)
