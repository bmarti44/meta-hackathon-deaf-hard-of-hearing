"""Listening clips for the site's "How an implant hears" section.

Builds one LibriSpeech test-speaker sentence and its crowd mixtures exactly the
way bench v2 does (clean at RMS 0.1, crowd of 8-12 held-out interferer voices
scaled to the requested SNR), runs the Gen 19 causal model on the mixture
(output re-aligned with undelay(), as in bench.load_gen15), and passes each
signal through the bench's ACE-like 8-of-22 noise vocoder (research/bench-n6/
vocoder.py). Every clip is then loudness-matched (ffmpeg ebur128), faded,
encoded to mp3, decoded again and checked for level and clipping.

It also writes electrodogram.json: for each signal the processor would
receive, the 22 ACE band envelopes (the page picks the 8 largest per frame,
as the vocoder does) and a 48-bin log spectrum, both at 16 ms frames, so the
page's animation is driven by the real sentence.

Speech: LibriSpeech dev-clean (Panayotov et al. 2015), CC BY 4.0. Test
speaker and test interferers only; no family or listening-pack audio.

Run: /tmp/gen9env/bin/python site/tools/make_implant_audio.py
"""
from __future__ import annotations
import base64, json, re, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[2]
for p in ["research/bench-n6", "research/gen13", "research/gen15"]:
    sys.path.insert(0, str(ROOT / p))

from common import FS, limit_signal, rms  # noqa: E402
from vocoder import extract_envelopes, vocode, N_FFT, HOP  # noqa: E402
from bench import load_gen15  # noqa: E402
from train2 import babble, load_pool  # noqa: E402

FFMPEG = "/opt/homebrew/bin/ffmpeg"
LS = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
OUT = ROOT / "site/assets/audio/implant"
WEIGHTS = ROOT / "research/gen19/weights/causal_seed20261117.pt"
UTT = "1988-147956-0026"          # test speaker 1988 (bench v2 TEST_SPK_V2)
INTERFERERS = ["8297", "8842", "6319", "6345", "7850", "7976"]  # bench v2 TEST_INTERFERERS
CROWD_K = 10                      # inside bench v2 CROWD_K = (8, 12)
LEAD, TAIL = 0.45, 0.55           # seconds of room around the sentence
TARGET_LUFS = -20.0
PEAK_CAP = 0.89                   # common.PEAK_LIMIT
FADE_IN, FADE_OUT = 0.12, 0.35
VIS_POOL = 2                      # 2 vocoder hops = 16 ms per visual frame
VOC_SEED = 7


def lufs(x):
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, x, FS, subtype="FLOAT")
        r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", f.name, "-af", "ebur128",
                            "-f", "null", "-"], capture_output=True, text=True)
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])


def fade(x):
    y = x.copy()
    a, b = int(FADE_IN * FS), int(FADE_OUT * FS)
    y[:a] *= np.sin(np.linspace(0, np.pi / 2, a)) ** 2
    y[-b:] *= np.cos(np.linspace(0, np.pi / 2, b)) ** 2
    return y


def master(x):
    """Loudness-match to TARGET_LUFS; a gentle soft-knee only if a peak would exceed PEAK_CAP."""
    y = fade(np.asarray(x, np.float64))
    y = y * 10 ** ((TARGET_LUFS - lufs(y.astype(np.float32))) / 20)
    knee = 0.75
    over = np.abs(y) > knee
    if over.any() and np.max(np.abs(y)) > PEAK_CAP:
        s = np.sign(y[over]); m = np.abs(y[over]) - knee
        y[over] = s * (knee + (PEAK_CAP - knee) * np.tanh(m / (PEAK_CAP - knee)))
    return y.astype(np.float32)


def visual_data(x):
    """22 ACE envelopes + 48-bin log spectrum, dB, 0..255, 16 ms frames."""
    x = limit_signal(x)
    env = extract_envelopes(x)                                  # (T, 22), vocoder analysis
    win = np.hanning(N_FFT)
    nfr = 1 + (len(x) - N_FFT) // HOP
    spec = np.abs(np.fft.rfft(np.stack([x[i * HOP:i * HOP + N_FFT] * win for i in range(nfr)]), axis=-1)) ** 2
    freqs = np.linspace(0, FS / 2, spec.shape[1])
    edges = np.geomspace(120, 7900, 49)
    bins = np.stack([spec[:, (freqs >= edges[i]) & (freqs < edges[i + 1])].sum(1) + 1e-12 for i in range(48)], 1)
    T = min(len(env), len(bins)) // VIS_POOL * VIS_POOL

    def q(a, rng_db):
        a = a[:T].reshape(-1, VIS_POOL, a.shape[1]).mean(1)
        d = 10 * np.log10(a + 1e-12)
        d = np.clip((d - (d.max() - rng_db)) / rng_db, 0, 1)
        return base64.b64encode((d * 255).round().astype(np.uint8).tobytes()).decode()
    return {"frames": T // VIS_POOL, "env": q(env ** 2, 50.0), "spec": q(bins, 60.0)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    spk, ch, _ = UTT.split("-")
    x, sr = sf.read(LS / spk / ch / f"{UTT}.flac", dtype="float32")
    assert sr == FS
    text = [l.split(" ", 1)[1].strip() for l in open(LS / spk / ch / f"{spk}-{ch}.trans.txt")
            if l.startswith(UTT)][0]
    clean = np.concatenate([np.zeros(int(LEAD * FS)), x, np.zeros(int(TAIL * FS))]).astype(np.float32)
    clean = clean[:N_FFT + (len(clean) - N_FFT) // HOP * HOP]                 # vocoder framing needs hop-aligned length
    clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)           # bench v2 scaling
    n = len(clean)

    pool = load_pool(INTERFERERS)
    rng = np.random.default_rng(20261104)
    crowd = babble(rng, pool, INTERFERERS, k=CROWD_K, n=n)
    enhance = load_gen15(str(WEIGHTS))

    sig = {"clean": clean}
    for snr, tag in [(0.0, "0db"), (-5.0, "m5db")]:
        noise = (crowd / (rms(crowd) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
        mix = (clean + noise).astype(np.float32)
        sig[f"mix_{tag}"] = mix
        sig[f"enh_{tag}"] = enhance(mix)

    clips = [  # id, source signal, vocoded?, label
        ("01-voice", "clean", False, "The voice, as recorded"),
        ("02-voice-ci", "clean", True, "The voice, through the implant simulation"),
        ("03-crowd-0db", "mix_0db", False, "The voice in a crowd, 0 dB"),
        ("04-crowd-0db-ci", "mix_0db", True, "That crowd, through the implant simulation"),
        ("05-cleaned-0db-ci", "enh_0db", True, "Cleaned by the Gen 19 model, then the implant simulation"),
        ("06-crowd-m5db", "mix_m5db", False, "The voice in a louder crowd, −5 dB"),
        ("07-crowd-m5db-ci", "mix_m5db", True, "That louder crowd, through the implant simulation"),
        ("08-cleaned-m5db-ci", "enh_m5db", True, "Cleaned by the Gen 19 model, then the implant simulation"),
    ]
    report = []
    for cid, src, voc, label in clips:
        y = vocode(limit_signal(sig[src]), seed=VOC_SEED) if voc else sig[src]
        y = master(y)
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            sf.write(f.name, y, FS, subtype="PCM_16")
            mp3 = OUT / f"{cid}.mp3"
            subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", f.name, "-ac", "1",
                            "-ar", str(FS), "-c:a", "libmp3lame", "-b:a", "64k", str(mp3)], check=True)
        dec = subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(mp3), "-f", "f32le",
                              "-ac", "1", "-ar", str(FS), "-"], capture_output=True, check=True).stdout
        d = np.frombuffer(dec, np.float32)
        row = {"id": cid, "label": label, "dur_s": round(len(d) / FS, 2),
               "rms_dbfs": round(float(20 * np.log10(rms(d))), 2),
               "peak_dbfs": round(float(20 * np.log10(np.max(np.abs(d)))), 2),
               "lufs": round(lufs(d), 2), "clipped_samples": int(np.sum(np.abs(d) >= 0.999)),
               "kb": round(mp3.stat().st_size / 1024, 1)}
        report.append(row)
        print(row)

    vis = {k: visual_data(sig[k]) for k in ["clean", "mix_0db", "enh_0db", "mix_m5db", "enh_m5db"]}
    meta = {"utterance": UTT, "text": text, "lead_s": LEAD, "frame_s": VIS_POOL * HOP / FS,
            "frame_offset_s": (N_FFT / 2) / FS, "crowd_talkers": CROWD_K, "interferers": INTERFERERS,
            "credit": "LibriSpeech (Panayotov et al. 2015), CC BY 4.0", "model": "Gen 19, seed 20261117",
            "clips": report, "signals": vis}
    (OUT / "electrodogram.json").write_text(json.dumps(meta, separators=(",", ":")))
    print("text:", text)
    print("electrodogram.json", round((OUT / "electrodogram.json").stat().st_size / 1024, 1), "KB")


if __name__ == "__main__":
    main()
