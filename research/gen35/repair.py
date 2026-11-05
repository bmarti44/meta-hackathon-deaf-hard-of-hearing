"""Gen35 frozen output-path repair audit (Astra's Gen34 review, choice c). No training, no selection.

Three predefined output arms for each frozen Gen19 checkpoint (seeds 17/18/19):
  A0 'existing'  : the Gen34 v1 research path, undelay(model(x)) (the last 63 output samples are zero padding);
  A1 'sign'      : polarity * flushed(model(x)), where flushed() runs the model on x + 63 zeros and keeps
                   out[63 : 63 + n] (the fixed delay removed with no padding, as in the published enhance.py);
  A2 'repair'    : polarity * (flushed(model(x)) - decoder_bias).
Polarity is a registered per-checkpoint constant bound to the checkpoint's sha256 (research/gen34/polarity_check.json);
it is never estimated per utterance or per ear. The decoder bias is read from the checkpoint. Nothing is fitted.
The exported entry point (the published Hugging Face enhance.py, mono mix-down + RMS restore) is audited separately,
as published and with the same repair inserted before its RMS restore.
"""
from __future__ import annotations
import hashlib, sys
from pathlib import Path
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
R = HERE.parent
REPO = R.parent
sys.path.insert(0, str(R / "gen15"))
from model_causal import CausalTasNetEnh, DELAY, undelay  # noqa: E402

CKPTS = {17: REPO / "research/gen19/weights/causal_seed20261117.pt",
         18: REPO / "research/gen19/weights/causal_seed20261118.pt",
         19: REPO / "research/gen19/weights/causal_seed20261119.pt"}
# Frozen sha256 -> polarity for all three registered Gen19 finals (Astra pre-launch blocking 4); any other file is refused.
POLARITY = {"80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367": -1,   # seed 17
            "ef098dfd429f20dcf7c199b6a534795c232a372a66af65e473fb5b6325a30916": 1,    # seed 18
            "89837737be430645441d577c44f277e2fee6b76ffb6865f613e8d72ae6fdcb32": -1}   # seed 19
ARMS = ("A0_existing", "A1_sign", "A2_repair")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def registered_polarity():
    """The frozen POLARITY table, cross-checked against the committed Gen34 evidence (signed projection on held-out
    speech) and against the files on disk; any mismatch raises."""
    import json
    doc = json.loads((R / "gen34" / "polarity_check.json").read_text())
    for seed, ck in CKPTS.items():
        h = sha(ck)
        if h not in POLARITY:
            raise SystemExit(f"REFUSED: {ck} sha256 {h} is not a registered checkpoint")
        row = next(r for r in doc["rows"] if r["ckpt"] == str(ck.relative_to(REPO)))
        if int(np.sign(row["alpha"])) != POLARITY[h]:
            raise SystemExit(f"REFUSED: polarity evidence for {ck} disagrees with the frozen table")
    return dict(POLARITY)


class Arms:
    def __init__(self, ckpt):
        self.model = CausalTasNetEnh()
        ck = torch.load(ckpt, map_location="cpu", weights_only=False)
        sd = ck["state_dict"] if "state_dict" in ck else ck
        self.model.load_state_dict(sd); self.model.eval()
        self.sha = sha(ckpt)
        if self.sha not in POLARITY:
            raise SystemExit(f"REFUSED: {ckpt} sha256 {self.sha} is not a registered checkpoint")
        self.polarity = POLARITY[self.sha]
        self.bias = float(sd["decoder.bias"][0])

    def _run(self, x):
        with torch.no_grad():
            return self.model(torch.from_numpy(np.asarray(x, np.float32)[None]))[0].numpy().astype(np.float64)

    def outputs(self, x):
        """dict arm -> float32 output, same length as x."""
        n = len(x)
        a0 = undelay(self._run(x)).astype(np.float32)
        flushed = self._run(np.concatenate([np.asarray(x, np.float32), np.zeros(DELAY, np.float32)]))[DELAY:DELAY + n]
        return {"A0_existing": a0, "A1_sign": (self.polarity * flushed).astype(np.float32),
                "A2_repair": (self.polarity * (flushed - self.bias)).astype(np.float32)}


EXPORT_ARMS = ("E0_published", "E1_sign", "E2_repair")


def export_arms(audio, A):
    """dict export arm -> output: as published, sign-only, and sign + bias removal (both before the RMS restore)."""
    return {"E0_published": export_enhance(audio, A.model), "E1_sign": export_enhance(audio, A.model, (A.polarity, 0.0)),
            "E2_repair": export_enhance(audio, A.model, (A.polarity, A.bias))}


def export_enhance(audio, model, repair=None, sr=16000):
    """The published enhance.py core, verbatim in its steps (mono, RMS 0.14 in, delay flush, RMS restore), at 16 kHz.
    repair=(polarity, bias) inserts polarity * (y - bias) right after delay removal, before the RMS restore."""
    MIX_RMS = 0.14
    x = np.asarray(audio, dtype=np.float32)
    if x.ndim == 2:
        x = x.mean(axis=1)
    level = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
    if level < 1e-6:
        return np.zeros(len(x), dtype=np.float32)
    n16 = len(x)
    inp = np.concatenate([x * (MIX_RMS / level), np.zeros(DELAY, np.float32)])
    with torch.no_grad():
        y = model(torch.from_numpy(inp.astype(np.float32))[None])[0].numpy()
    y16 = y[DELAY:DELAY + n16].astype(np.float64)
    if repair is not None:
        y16 = repair[0] * (y16 - repair[1])
    y16 = y16 * (level / (float(np.sqrt(np.mean(y16 ** 2))) + 1e-12))
    return y16.astype(np.float32)


def signed_alpha(ref, out, w):
    r = np.asarray(ref, np.float64)[w]; o = np.asarray(out, np.float64)[w]
    return float(np.dot(o, r) / (np.dot(r, r) + 1e-20))


def wave_err_db(ref, out, w):
    r = np.asarray(ref, np.float64)[w]; o = np.asarray(out, np.float64)[w]
    return float(10 * np.log10((np.sum((o - r) ** 2) + 1e-20) / (np.sum(r ** 2) + 1e-20)))


def peak_lag(ref, out, w, max_lag=80):
    """Lag (samples) maximising |sum ref[t] * out[t + d]|; 0 means the output is time-aligned."""
    r = np.asarray(ref, np.float64); o = np.asarray(out, np.float64)
    s, e = w.start + max_lag, (w.stop or len(r)) - max_lag
    return max(range(-max_lag, max_lag + 1), key=lambda d: abs(float(np.dot(r[s:e], o[s + d:e + d]))))
