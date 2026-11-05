"""Gen36 sealed fresh evaluation manifest: LibriSpeech test-other (OpenSLR 12, CC-BY-4.0), never used in this repo.

Deterministic choice (no listening, no scores):
- targets: the 4 lowest-numbered female and 4 lowest-numbered male test-other speakers; crowd voices: the next 6 female
  and 6 male; the remaining speakers are untouched;
- per speaker, the first two utterances (sorted by file name) at least 6 s long; a 5 s crop starting at 0.5 s;
- targets scaled to RMS 0.1 (training convention); crowd = mean of 8 crowd utterances drawn with
  np.random.default_rng(20261136), each a 5 s crop at a drawn offset, then scaled to the SNR;
- F1 noisy: 8 targets x 2 utterances x SNR {-5, 0, +5, +10} = 64 items; each mixture and its clean target are scaled by
  ONE gain so the mixture peaks at 0.5 (-6 dBFS): every F1 input is representable in a file (amendment 1, Astra);
- F2 target-only: the 16 target crops at input RMS 0.035 and 0.14 (representable) and at peak 1.5 x full scale
  (OVERLOAD stress, labelled; inputs beyond full scale cannot come from a file and are reported, not level-gated).
Representability (input peak <= 1 after resampling to each registered rate) is sealed per item and rate.
The material hash covers source-file sha256s, parameters and every rendered array.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path("/tmp/gen36dl/LibriSpeech/test-other")
SEED = 20261136
SNRS = (-5.0, 0.0, 5.0, 10.0)
LEVELS = (0.035, 0.14, "overload")
FS = 16000
RATES = (16000, 44100, 48000)


def peak_at(x, sr):
    from math import gcd
    from scipy.signal import resample_poly
    y = np.asarray(x, np.float64) if sr == FS else resample_poly(np.asarray(x, np.float64), sr // gcd(FS, sr), FS // gcd(FS, sr))
    return float(np.max(np.abs(y)))


def speakers():
    sex = {}
    for line in (ROOT.parent / "SPEAKERS.TXT").read_text().splitlines():
        if line.startswith(";"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and parts[2] == "test-other":
            sex[parts[0]] = parts[1]
    F = sorted([s for s, x in sex.items() if x == "F"], key=int); M = sorted([s for s, x in sex.items() if x == "M"], key=int)
    return F[:4] + M[:4], F[4:10] + M[4:10], sex


def utterances(spk, n=2, min_s=6.0):
    files = sorted((ROOT / spk).rglob("*.flac"))
    out = []
    for f in files:
        info = sf.info(str(f))
        if info.duration >= min_s:
            out.append(f)
        if len(out) == n:
            break
    assert len(out) == n, f"speaker {spk}: not enough long utterances"
    return out


def _load(f, start, n):
    x, fs = sf.read(str(f), dtype="float64"); assert fs == FS
    return x[start:start + n]


def build():
    targets, crowd, _ = speakers()
    rng = np.random.default_rng(SEED)
    h = hashlib.sha256(); n = 5 * FS
    pool = [f for s in crowd for f in utterances(s, n=2)]
    for f in pool:
        h.update(hashlib.sha256(f.read_bytes()).hexdigest().encode())
    items = []
    for spk in targets:
        for ui, f in enumerate(utterances(spk)):
            h.update(hashlib.sha256(f.read_bytes()).hexdigest().encode())
            clean = _load(f, FS // 2, n); clean = clean / (np.sqrt(np.mean(clean ** 2)) + 1e-12) * 0.1
            idx = rng.choice(len(pool), size=8, replace=False)
            babble = np.zeros(n)
            for j in idx:
                x, _ = sf.read(str(pool[j]), dtype="float64")
                off = int(rng.integers(0, max(1, len(x) - n)))
                seg = x[off:off + n]; seg = np.pad(seg, (0, n - len(seg)))
                babble += seg / (np.sqrt(np.mean(seg ** 2)) + 1e-12)
            babble /= 8
            for snr in SNRS:
                noise = babble / (np.sqrt(np.mean(babble ** 2)) + 1e-12) * np.sqrt(np.mean(clean ** 2)) * 10 ** (-snr / 20)
                mix = clean + noise; gg = 0.5 / np.max(np.abs(mix))
                it = {"panel": "F1", "spk": spk, "utt": ui, "snr": snr, "clean": (gg * clean).astype(np.float32),
                      "mix": (gg * mix).astype(np.float32)}
                it["representable"] = {r: bool(peak_at(it["mix"], r) <= 1.0) for r in RATES}
                h.update(f"F1|{spk}|{ui}|{snr}".encode()); h.update(it["mix"].tobytes()); h.update(it["clean"].tobytes())
                items.append(it)
            for lv in LEVELS:
                g = (1.5 / np.max(np.abs(clean))) if lv == "overload" else lv / 0.1
                x = (g * clean).astype(np.float32)
                it = {"panel": "F2", "spk": spk, "utt": ui, "level": lv, "clean": x, "mix": x,
                      "representable": {r: bool(peak_at(x, r) <= 1.0) for r in RATES}}
                h.update(f"F2|{spk}|{ui}|{lv}".encode()); h.update(x.tobytes())
                items.append(it)
    return items, h.hexdigest(), {"targets": targets, "crowd": crowd, "seed": SEED}


if __name__ == "__main__":
    items, mh, meta = build()
    print(json.dumps({"n_items": len(items), "material_sha256": mh, **meta,
                      "nonrepresentable_item_rates": sum(1 for i in items for r in RATES if not i["representable"][r])}, indent=1))
