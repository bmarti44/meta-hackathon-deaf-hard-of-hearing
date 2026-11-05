"""Freeze the Gen27 RIR bank (research/gen27/rir_manifest.json).

Source: OpenSLR 28 "Room Impulse Response and Noise Database"
(https://www.openslr.org/resources/28/rirs_noises.zip, Apache 2.0),
extracted to /tmp/rirs/RIRS_NOISES (outside git). The archive md5 is
checked against the published checksum.md5 and its sha256 recorded.

Simulated set (image method, Habets RIR generator): small/medium/large
room families, 200 rooms each, ONE receiver per room and 100 source
positions (source-receiver distance <= 5 m). So all RIRs of a room share
the microphone, and each talker can take its own source position.

Rules (fixed here, before any training or evaluation):
- Room RT60 = median Schroeder RT60 (rirbank.rt60_schroeder) over the
  room's first K_RT60 RIRs by filename. Stratum: short [0.2,0.4),
  medium [0.4,0.6), long [0.6,0.8] s; other rooms unused.
- Held-out synthetic screen rooms ('eval_synth'): 2 per stratum, drawn
  with RNG seed 20261127, the two from different size families when the
  stratum allows it.
- Training rooms ('train'): the same number per stratum (min over strata
  of the eligible rooms left after the eval draw, capped at N_TRAIN_CAP),
  in the same RNG permutation order, so strata are balanced.
- Each selected simulated room keeps its first K_POS RIRs by filename
  (measured rooms: first K_POS_MEASURED).
- Measured rooms ('eval_measured', evaluation only): real RIRs from the
  OpenSLR 28 real set (REVERB 2014 real rooms, AIR, RWCP), excluding the
  REVERB *simulated* rooms, anechoic RWCP rooms, AIR phone mock-ups and
  single-position entries. A room = one OpenSLR room-id (one microphone
  channel). Eligible when >= 3 positions and median RT60 in [0.2, 0.8];
  up to 2 per stratum, preferring more positions, then name.
- room_gain: one constant per room = 1/sqrt(mean RIR energy) after
  truncation, so mean RIR energy in each room is 1 and relative source
  levels within a room stay physical.

Usage: /tmp/gen9env/bin/python research/gen27/build_rir_bank.py
"""
from __future__ import annotations
import hashlib, json, re, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rirbank as rb  # noqa: E402

ARCHIVE = Path("/tmp/rirs/rirs_noises.zip")
URL = "https://www.openslr.org/resources/28/rirs_noises.zip"
PUBLISHED_MD5 = "e6f48e257286e05de56413b4779d8ffb"  # https://www.openslr.org/resources/28/checksum.md5
SEED = 20261127
K_RT60 = 8
K_POS = 16          # simulated: first 16 source positions per room
K_POS_MEASURED = 8
N_TRAIN_CAP = 40    # train rooms per stratum = min over strata of the rooms left after eval, capped
STRATA = ("short", "medium", "long")
FAMILIES = ("smallroom", "mediumroom", "largeroom")


def rir_record(root, rel, room_gain=None):
    p = root / rel
    h = rb.truncate(rb.read_rir(p))
    rt, how = rb.rt60_schroeder(h)
    drr, c50 = rb.drr_c50(h)
    return {"file": rel, "sha256": rb.sha256_file(p), "channel": 0, "n_samples_used": len(h),
            "direct_idx": rb.direct_index(h), "rt60_s": rt, "rt60_method": how,
            "drr_db": drr, "c50_db": c50, "energy": float((h ** 2).sum())}


def room_rt60(root, rels):
    vals = [rb.rt60_schroeder(rb.truncate(rb.read_rir(root / r)))[0] for r in rels[:K_RT60]]
    vals = [v for v in vals if np.isfinite(v)]
    return float(np.median(vals)) if vals else float("nan")


def finish_room(root, room_id, family, rels, stratum, split, rt60_room):
    recs = [rir_record(root, r) for r in rels]
    gain = 1.0 / np.sqrt(np.mean([r["energy"] for r in recs]))
    rts = [r["rt60_s"] for r in recs if np.isfinite(r["rt60_s"])]
    return {"room_id": room_id, "family": family, "stratum": stratum, "split": split,
            "rt60_s": rt60_room, "rt60_kept_rirs_median": float(np.median(rts)), "rt60_rirs_min": float(min(rts)), "rt60_rirs_max": float(max(rts)),
            "room_gain": float(gain), "rirs": recs}


def main():
    t0 = time.time()
    root = rb.RIR_ROOT.parent
    md5 = hashlib.md5(ARCHIVE.read_bytes()).hexdigest()
    assert md5 == PUBLISHED_MD5, f"archive md5 {md5} != published {PUBLISHED_MD5}"
    sha = rb.sha256_file(ARCHIVE)
    # --- simulated rooms
    sim = []
    for fam in FAMILIES:
        d = rb.RIR_ROOT / "simulated_rirs" / fam
        for room_dir in sorted(p for p in d.iterdir() if p.is_dir()):
            rels = [str(f.relative_to(root)) for f in sorted(room_dir.glob("*.wav"))]
            rt = room_rt60(root, rels)
            sim.append({"room_id": f"{fam}-{room_dir.name}", "family": f"simulated/{fam}",
                        "rels": rels[:K_POS], "rt60": rt, "stratum": rb.stratum_of(rt) if np.isfinite(rt) else None})
        print(f"{fam} scanned {time.time()-t0:.0f}s", flush=True)
    rng = np.random.default_rng(SEED)
    eligible = {s: [r for r in sim if r["stratum"] == s] for s in STRATA}
    chosen_eval, chosen_train, rests = [], [], {}
    for s in STRATA:
        pool = list(eligible[s])
        order = rng.permutation(len(pool))
        first = pool[order[0]]
        second = next((pool[i] for i in order[1:] if pool[i]["family"] != first["family"]), pool[order[1]])
        chosen_eval += [first, second]
        rests[s] = [pool[i] for i in order if pool[i] is not first and pool[i] is not second]
    n_train = min(N_TRAIN_CAP, *(len(v) for v in rests.values()))
    for s in STRATA:
        chosen_train += rests[s][:n_train]
    rooms = []
    for r in chosen_eval:
        rooms.append(finish_room(root, r["room_id"], r["family"], r["rels"], r["stratum"], "eval_synth", r["rt60"]))
    for r in chosen_train:
        rooms.append(finish_room(root, r["room_id"], r["family"], r["rels"], r["stratum"], "train", r["rt60"]))
    print(f"simulated rooms frozen {time.time()-t0:.0f}s", flush=True)
    # --- measured rooms (evaluation only)
    lst = (rb.RIR_ROOT / "real_rirs_isotropic_noises" / "rir_list").read_text().split("\n")
    by_room = {}
    for line in lst:
        m = re.search(r"--room-id (\S+) (\S+)", line)
        if m:
            by_room.setdefault(m.group(1), []).append(m.group(2))
    excl = re.compile(r"simroom|_ane$|air_phone|\.wav$")
    meas = []
    for rid, rels in sorted(by_room.items()):
        if excl.search(rid) or len(rels) < 3:
            continue
        rels = sorted(rels)[:K_POS_MEASURED]
        rt = room_rt60(root, rels)
        st = rb.stratum_of(rt) if np.isfinite(rt) else None
        meas.append({"room_id": rid, "rels": rels, "rt60": rt, "stratum": st})
    measured_scan = [{"room_id": m["room_id"], "rt60_s": m["rt60"], "n_pos": len(m["rels"]), "stratum": m["stratum"]} for m in meas]
    for s in STRATA:
        cand = sorted([m for m in meas if m["stratum"] == s], key=lambda m: (-len(m["rels"]), m["room_id"]))
        for m in cand[:2]:
            rooms.append(finish_room(root, m["room_id"], "measured/" + m["room_id"].split("_")[0], m["rels"], s, "eval_measured", m["rt60"]))
    eval_ids = {r["room_id"] for r in rooms if r["split"] != "train"}
    assert not (eval_ids & {r["room_id"] for r in rooms if r["split"] == "train"}), "room split leak"
    summary = {}
    for split in ("train", "eval_synth", "eval_measured"):
        for s in STRATA:
            sel = [r for r in rooms if r["split"] == split and r["stratum"] == s]
            rts = [r["rt60_s"] for r in sel]
            summary[f"{split}/{s}"] = {"n_rooms": len(sel), "n_rirs": sum(len(r["rirs"]) for r in sel),
                                       "rt60_min": min(rts) if rts else None, "rt60_median": float(np.median(rts)) if rts else None,
                                       "rt60_max": max(rts) if rts else None,
                                       "drr_db_median": float(np.median([f["drr_db"] for r in sel for f in r["rirs"]])) if sel else None,
                                       "c50_db_median": float(np.median([f["c50_db"] for r in sel for f in r["rirs"]])) if sel else None}
    man = {"what": "Gen27 frozen RIR bank (room-split); audio outside git under /tmp/rirs/RIRS_NOISES",
           "source": {"name": "OpenSLR 28 Room Impulse Response and Noise Database", "url": URL,
                      "licence": "Apache 2.0", "archive_md5": md5, "archive_md5_published": PUBLISHED_MD5,
                      "archive_sha256": sha, "archive_bytes": ARCHIVE.stat().st_size},
           "rules": {"seed": SEED, "k_rt60": K_RT60, "k_pos": K_POS, "k_pos_measured": K_POS_MEASURED, "n_train_cap": N_TRAIN_CAP, "n_train_per_stratum": n_train,
                     "strata_s": {"short": [0.2, 0.4], "medium": [0.4, 0.6], "long": [0.6, 0.8]},
                     "l_max": rb.L_MAX, "fade_samples": rb.FADE, "early_ms": rb.EARLY_MS, "taper_ms": rb.TAPER_MS,
                     "rt60": "Schroeder EDC from direct arrival, T20 fit (fallback T10), median over first k_rt60 RIRs",
                     "drr": "+-2.5 ms around argmax|h| vs rest", "c50": "<= direct+50 ms vs after",
                     "room_gain": "1/sqrt(mean truncated-RIR energy) per room"},
           "eligible_simulated_rooms": {s: len(eligible[s]) for s in STRATA},
           "simulated_rooms_scanned": len(sim),
           "simulated_rt60_scan": [{"room_id": r["room_id"], "rt60_s": r["rt60"]} for r in sim],
           "measured_scan": measured_scan,
           "summary": summary, "rooms": rooms}
    out = HERE / "rir_manifest.json"
    out.write_text(json.dumps(man, indent=1))
    print(json.dumps(summary, indent=1))
    print(f"WROTE {out} sha256={rb.sha256_file(out)} in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
