"""Gen27 reverberant screen material and evaluation (draft for registration).

Spec: research/gen27/astra-agenda-review.md item 4. The screen-v2 draws
(research/screen_v2/panel_v2.py, seed 20261204: 16 targets x 4 clean 4 s
crops x 4 crowds of k ~ U{8..12} talkers from the other 15 voices) are
replayed with the SAME RNG calls, but each crowd talker is kept as its own
stem, with the 1 s of audio preceding each crop as convolution history.
The replay is checked: summing the stems reproduces the registered dry
material hash 557ad44f... bit-for-bit, else the build stops.

Each draw is crossed with:
- 'synthetic': the 6 held-out simulated rooms (2 per RT60 stratum,
  manifest split eval_synth) x SNR {-5, 0} dB  -> 3072 items;
- 'measured': the 6 measured rooms (split eval_measured), same grid
  -> 3072 items (a separate stratum, never pooled into the primary);
- 'target_only': each clean crop alone through each of the 12 rooms
  (no interferers) -> 768 items.
Per (target, crop, crowd, room) the source positions are drawn from
np.random.default_rng([20261127, room_index, target_index, crop, crowd]):
target position ~ U(room RIRs), each crowd talker its own position ~ U(the
other positions), with replacement. Positions are shared by both SNRs.
Every source is convolved with its own RIR before summation. Reference =
target through the direct + 50 ms early RIR (5 ms taper); mixture target =
full reverberant target; SNR = full reverberant target energy vs summed
reverberant crowd energy. Fixed model-delay alignment (model_causal.undelay),
no reference normalization, metrics on [256:-256] as in panel_v2.

Usage:
  python research/gen27/panel_rev.py --hash
  python research/gen27/panel_rev.py --system control=<ckpt> --system cand=<ckpt> --out <json>
Systems with the same checkpoint sha256 are evaluated once and their rows
copied under each name (the self-test uses this).
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from multiprocessing import get_context
from pathlib import Path
import numpy as np
import scipy.fft as sfft

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "gen24"))
sys.path.insert(0, str(HERE))
import train13 as t13  # noqa: E402
import rirbank  # noqa: E402
from train14 import crop_ctx, babble_stems, sum_stems  # noqa: E402

FS = 16000
SEG4 = 4 * FS
CTX = rirbank.L_MAX
NFFT4 = sfft.next_fast_len(SEG4 + CTX)
FEMALE = ["84", "1462", "1673", "1919", "3081", "3536", "3576", "3853"]
MALE = ["174", "251", "422", "652", "777", "1272", "2803", "2902"]
TARGETS = FEMALE + MALE
ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
SEED_V2 = 20261204
SEED_POS = 20261127
DRY_REGISTERED = "557ad44f3f874c25f6fe80c158844ce4a622f52db171f35c1f84464dbfb3eafb"
MANIFEST = HERE / "rir_manifest.json"
SNRS = (-5.0, 0.0)
TR = slice(256, -256)


def replay_draws():
    """Screen-v2 draws with stems. Returns (draws, dry_hash). draws[t][c] =
    {'clean','pre','crowds':[{'stems','pres','k'} x4]} at panel_v2 gains."""
    pool = t13.load_pool(TARGETS, root=ROOT)
    rng = np.random.default_rng(SEED_V2)
    h = hashlib.sha256()
    draws = {}
    for spk in TARGETS:
        others = [s for s in TARGETS if s != spk]
        draws[spk] = []
        for c in range(4):
            clean, pre = crop_ctx(rng, t13.pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), SEG4)
            g = t13.rms(clean) + 1e-9
            clean = (clean / g * 0.1).astype(np.float32); pre = (pre / g * 0.1).astype(np.float32)
            crowds = []
            for mix_ix in range(4):
                k = int(rng.integers(8, 13))
                stems, pres = babble_stems(rng, pool, others, k=k, n=SEG4)
                noise0 = sum_stems(stems, k)
                for snr in SNRS:  # panel_v2 material, recomputed for the hash check
                    noise = (noise0 / (t13.rms(noise0) + 1e-9) * t13.rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                    h.update(f"{spk}|{c}|{mix_ix}|{snr}".encode())
                    h.update(clean.tobytes()); h.update((clean + noise).astype(np.float32).tobytes())
                crowds.append({"stems": [s.astype(np.float32) for s in stems],
                               "pres": [p.astype(np.float32) for p in pres], "k": k})
            draws[spk].append({"clean": clean, "pre": pre, "crowds": crowds})
    return draws, h.hexdigest()


def rooms_from_manifest(manifest=MANIFEST):
    man = json.loads(Path(manifest).read_text())
    rooms = [r for r in man["rooms"] if r["split"] in ("eval_synth", "eval_measured")]
    order = {"eval_synth": 0, "eval_measured": 1}
    st = {"short": 0, "medium": 1, "long": 2}
    rooms.sort(key=lambda r: (order[r["split"]], st[r["stratum"]], r["room_id"]))
    return rooms


def _conv(x_full, H):
    return sfft.irfft(sfft.rfft(x_full.astype(np.float64), NFFT4) * H, NFFT4)[CTX:CTX + SEG4]


def build_room_items(spk, ti, draw_list, rooms, bank):
    """All items for one target voice, in canonical order."""
    items = []
    for ri, room in enumerate(rooms):
        b = bank.by_id[room["room_id"]]
        H = [sfft.rfft(h, NFFT4) for h in b["h"]]
        HE = [sfft.rfft(h, NFFT4) for h in b["he"]]
        stratum = "synthetic" if room["split"] == "eval_synth" else "measured"
        n_pos = len(H)
        for c, d in enumerate(draw_list):
            x = np.concatenate([d["pre"], d["clean"]])
            Xc = sfft.rfft(x.astype(np.float64), NFFT4)
            for m, cr in enumerate(d["crowds"]):
                prng = np.random.default_rng([SEED_POS, ri, ti, c, m])
                t = int(prng.integers(0, n_pos))
                others = [i for i in range(n_pos) if i != t]
                pos = [others[prng.integers(0, len(others))] for _ in range(cr["k"])]
                rev_t = sfft.irfft(Xc * H[t], NFFT4)[CTX:CTX + SEG4]
                ref = sfft.irfft(Xc * HE[t], NFFT4)[CTX:CTX + SEG4].astype(np.float32)
                acc = np.zeros(NFFT4 // 2 + 1, dtype=np.complex128)
                for s, p, j in zip(cr["stems"], cr["pres"], pos):
                    acc += sfft.rfft(np.concatenate([p, s]).astype(np.float64), NFFT4) * H[j]
                rev_n = sfft.irfft(acc, NFFT4)[CTX:CTX + SEG4] / cr["k"]
                for snr in SNRS:
                    noise = rev_n / (t13.rms(rev_n) + 1e-9) * t13.rms(rev_t) * 10 ** (-snr / 20)
                    items.append({"stratum": stratum, "room_id": room["room_id"], "rt60_stratum": room["stratum"],
                                  "spk": spk, "crop": c, "mix": m, "snr": snr, "target_pos": t,
                                  "ref": ref, "mix_wav": (rev_t + noise).astype(np.float32)})
            # reverberant target-only check (no interferers); position from crowd-0 stream index 4
            prng = np.random.default_rng([SEED_POS, ri, ti, c, 4])
            t = int(prng.integers(0, n_pos))
            rev_t = sfft.irfft(Xc * H[t], NFFT4)[CTX:CTX + SEG4].astype(np.float32)
            ref = sfft.irfft(Xc * HE[t], NFFT4)[CTX:CTX + SEG4].astype(np.float32)
            items.append({"stratum": "target_only", "room_stratum": stratum, "room_id": room["room_id"],
                          "rt60_stratum": room["stratum"], "spk": spk, "crop": c, "mix": None, "snr": None,
                          "target_pos": t, "ref": ref, "mix_wav": rev_t})
    return items


def item_hash(it):
    h = hashlib.sha256()
    h.update(f"{it['stratum']}|{it['room_id']}|{it['spk']}|{it['crop']}|{it['mix']}|{it['snr']}|{it['target_pos']}".encode())
    h.update(it["ref"].tobytes()); h.update(it["mix_wav"].tobytes())
    return h.hexdigest()


def _sisdr(ref, est):
    return t13._si_sdr_np(ref, est)


def _worker(args):
    spk, ti, draw_list, rooms, manifest, systems = args
    import torch
    from pystoi import stoi
    from model_causal import CausalTasNetEnh, undelay
    torch.set_num_threads(2)
    bank = rirbank.Bank(manifest, splits=("eval_synth", "eval_measured"), nfft=None)
    items = build_room_items(spk, ti, draw_list, rooms, bank)
    hashes = [item_hash(it) for it in items]
    rows = []
    if systems:
        models = {}
        for sha, path in systems.items():
            m = CausalTasNetEnh()
            ck = torch.load(path, map_location="cpu", weights_only=False)
            m.load_state_dict(ck["state_dict"] if "state_dict" in ck else ck)
            models[sha] = m.eval()
        with torch.no_grad():
            for it in items:
                r64, m64 = it["ref"][TR].astype(np.float64), it["mix_wav"][TR].astype(np.float64)
                b_s, b_t = _sisdr(it["ref"][TR], it["mix_wav"][TR]), float(stoi(r64, m64, FS))
                for sha, m in models.items():
                    est = undelay(m(torch.from_numpy(it["mix_wav"][None]))[0].numpy())
                    s_abs = _sisdr(it["ref"][TR], est[TR]); t_abs = float(stoi(r64, est[TR].astype(np.float64), FS))
                    rows.append({"sha256": sha, **{k: it[k] for k in ("stratum", "room_id", "rt60_stratum", "spk", "crop", "mix", "snr", "target_pos")},
                                 **({"room_stratum": it["room_stratum"]} if "room_stratum" in it else {}),
                                 "sisdr": s_abs, "stoi": t_abs, "d_sisdr": s_abs - b_s, "d_stoi": t_abs - b_t})
    return spk, hashes, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--system", action="append", default=[], metavar="NAME=PATH")
    ap.add_argument("--manifest", default=str(MANIFEST))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    t0 = time.time()
    draws, dry_hash = replay_draws()
    assert dry_hash == DRY_REGISTERED, f"stem replay does not reproduce screen-v2 material: {dry_hash}"
    rooms = rooms_from_manifest(a.manifest)
    assert sum(r["split"] == "eval_synth" for r in rooms) == 6
    print(f"dry replay == registered screen-v2 material {dry_hash[:12]}; rooms={[r['room_id'] for r in rooms]} {time.time()-t0:.0f}s", flush=True)
    names, by_sha = {}, {}
    for spec in a.system:
        name, path = spec.split("=", 1)
        sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        names[name] = sha; by_sha[sha] = path
    jobs = [(spk, ti, draws[spk], rooms, a.manifest, by_sha) for ti, spk in enumerate(TARGETS)]
    with get_context("spawn").Pool(a.workers) as p:
        res = {spk: (hs, rows) for spk, hs, rows in p.imap_unordered(_worker, jobs)}
    h = hashlib.sha256()
    for spk in TARGETS:
        for x in res[spk][0]:
            h.update(x.encode())
    mh = h.hexdigest()
    n_items = sum(len(res[s][0]) for s in TARGETS)
    print(f"items={n_items} material_sha256={mh} {time.time()-t0:.0f}s", flush=True)
    if a.hash or not a.system:
        return
    rows = []
    for name, sha in names.items():
        for spk in TARGETS:
            rows += [{"system": name, **r} for r in res[spk][1] if r["sha256"] == sha]
    summ = {}
    for name in names:
        for st in ("synthetic", "measured"):
            for snr in SNRS:
                rs = [r for r in rows if r["system"] == name and r["stratum"] == st and r["snr"] == snr]
                summ[f"{name}|{st}|{snr}"] = {"n": len(rs), "d_sisdr": float(np.mean([r["d_sisdr"] for r in rs])),
                                              "d_stoi": float(np.mean([r["d_stoi"] for r in rs]))}
        rs = [r for r in rows if r["system"] == name and r["stratum"] == "target_only"]
        summ[f"{name}|target_only"] = {"n": len(rs), "sisdr": float(np.mean([r["sisdr"] for r in rs])),
                                       "d_sisdr": float(np.mean([r["d_sisdr"] for r in rs])),
                                       "d_stoi": float(np.mean([r["d_stoi"] for r in rs]))}
    Path(a.out).write_text(json.dumps({"panel": "screen_rev_g27", "seed_v2": SEED_V2, "seed_pos": SEED_POS,
                                       "dry_material_sha256": dry_hash, "material_sha256": mh,
                                       "rir_manifest_sha256": rirbank.sha256_file(a.manifest),
                                       "rooms": [{k: r[k] for k in ("room_id", "split", "stratum", "rt60_s", "family")} for r in rooms],
                                       "targets": TARGETS, "n_items": n_items, "systems": names,
                                       "summary": summ, "rows": rows}, indent=0))
    for k, v in summ.items():
        print(k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()})
    print(f"WROTE {a.out} {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
