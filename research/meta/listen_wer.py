"""Exploratory: does the Gen 19 enhancer help a Meta model (Muse Spark, audio input) transcribe the
target talker in bench crowd mixtures? Plan: research/meta/plan.md (written before results).

Run: /tmp/gen9env/bin/python research/meta/listen_wer.py
Calls the beforetheimplant-muse Lambda (mode "listen") by direct invoke; the API key never leaves AWS.
Audio: LibriSpeech dev-clean (Panayotov et al. 2015, CC BY 4.0), test speakers only.
"""
from __future__ import annotations
import base64, io, json, re, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
R = HERE.parent
for p in ["bench-n6", "gen13", "gen15"]:
    sys.path.insert(0, str(R / p))
from common import FS, bootstrap_ci  # noqa: E402
from bench import load_gen15  # noqa: E402
from train2 import babble, load_pool, rms  # noqa: E402

LS = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
TEST_SPK = ["1988", "1993", "5895", "6241", "6295", "6313"]
INTERF = ["8297", "8842", "6319", "6345", "7850", "7976"]
CKPT = R / "gen19/weights/causal_seed20261117.pt"
SNRS = [-5.0, 0.0]
SITE_AUDIO = R.parent / "site/assets/audio/meta-lab"
SITE_DATA = R.parent / "site/data/meta"


def transcripts(spk):
    out = {}
    for t in (LS / spk).rglob("*.trans.txt"):
        for line in t.read_text().splitlines():
            uid, txt = line.split(" ", 1)
            out[uid] = txt
    return out


def pick_utts():
    rng = np.random.default_rng(20261104)
    utts = []
    for spk in TEST_SPK:
        tx = transcripts(spk)
        files = sorted((LS / spk).rglob("*.flac"))
        ok = [f for f in files if 4.0 <= sf.info(str(f)).duration <= 10.0]
        for i in rng.choice(len(ok), size=2, replace=False):
            f = ok[int(i)]
            utts.append({"spk": spk, "uid": f.stem, "path": f, "text": tx[f.stem]})
    return utts


def norm(s):
    s = s.lower().replace("’", "'")
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return [w.strip("'") for w in s.split() if w.strip("'")]


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp.replace("[unintelligible]", " "))
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(len(r), 1)


def word_hits(ref, hyp):
    """Reference words the transcript got right (matches on one minimum-edit alignment)."""
    r, h = norm(ref), norm((hyp or "").replace("[unintelligible]", " "))
    D = [[i + j if i * j == 0 else 0 for j in range(len(h) + 1)] for i in range(len(r) + 1)]
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1, D[i - 1][j - 1] + (r[i - 1] != h[j - 1]))
    i, j, hits = len(r), len(h), 0
    while i > 0 and j > 0:
        if r[i - 1] == h[j - 1] and D[i][j] == D[i - 1][j - 1]:
            hits += 1; i -= 1; j -= 1
        elif D[i][j] == D[i - 1][j - 1] + 1:
            i -= 1; j -= 1
        elif D[i][j] == D[i][j - 1] + 1:
            j -= 1
        else:
            i -= 1
    return hits, len(r)


def strip_spill(hyp):
    """Remove a leading tail of the check sentence that Spark wrote on line 2 instead of line 1 (amendment 3)."""
    c, raw = norm(check_clip()["text"]), (hyp or "").split()
    for L in range(len(c), 0, -1):
        if [w for t in raw[:L] for w in norm(t)] == c[-L:]:
            rest = " ".join(raw[L:]).strip(" .,;")
            return rest or "[unintelligible]"
    return hyp


def rebuild_demo():
    """Rebuild the site demo from results.json without API calls: per speaker, the first clip (utterance order, then
    0 dB before -5 dB) whose unprocessed and Gen 19 transcripts both exist. Chosen on availability, not on outcome."""
    res = json.loads((HERE / "results.json").read_text())
    T = {(r["cond"], r["uid"], r["snr_db"]): r for r in res["rows"]}
    utts, pool, enh = pick_utts(), load_pool(INTERF), load_gen15(str(CKPT))
    rng = np.random.default_rng(20261117)
    audio = {}
    for u in utts:  # identical rng sequence to main()
        clean, _ = sf.read(str(u["path"]), dtype="float32")
        clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
        for snr in SNRS:
            noise = babble(rng, pool, INTERF, k=int(rng.integers(8, 13)), n=len(clean))
            noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
            audio[(u["uid"], snr)] = (clean + noise).astype(np.float32)
    for f in SITE_AUDIO.glob("*.mp3"):
        f.unlink()
    demo = []
    for spk in TEST_SPK:
        cands = [(u, snr) for u in utts if u["spk"] == spk for snr in [0.0, -5.0]]
        full = [c for c in cands if T[("unproc", c[0]["uid"], c[1])]["hyp"] is not None and T[("gen19", c[0]["uid"], c[1])]["hyp"] is not None]
        if not full:
            continue
        u, snr = full[0]
        mix = audio[(u["uid"], snr)]
        item = {"id": f"{u['uid']}_{int(snr)}", "speaker": spk, "utterance": u["uid"], "snr_db": snr,
                "seconds": round(len(mix) / FS, 1), "reference": u["text"].capitalize()}
        for cond, x in [("unproc", mix), ("gen19", enh(mix)[: len(mix)])]:
            name = f"{item['id']}_{cond}.mp3"
            _, x = wav_b64(x)
            with tempfile.NamedTemporaryFile(suffix=".wav") as tf:
                sf.write(tf.name, x, FS, subtype="PCM_16")
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tf.name, "-ac", "1", "-b:a", "48k", str(SITE_AUDIO / name)], check=True)
            r = T[(cond, u["uid"], snr)]
            item[cond] = {"audio": f"assets/audio/meta-lab/{name}", "transcript": r["hyp"], "wer": round(r["wer"], 3)}
        demo.append(item)
    site = json.loads((SITE_DATA / "listen.json").read_text())
    site["clips"] = demo
    site["meta"]["demo_selection"] = rebuild_demo.__doc__.split(":", 1)[1].strip().replace("\n    ", " ")
    (SITE_DATA / "listen.json").write_text(json.dumps(site, indent=1))
    for c in demo:
        print(c["id"], "|U", c["unproc"]["transcript"][:60], "|G", c["gen19"]["transcript"][:60])


def rescore():
    """Amendment 3: re-score run 3 from saved transcripts after stripping check-sentence spill. No new API calls."""
    res = json.loads((HERE / "results.json").read_text())
    for r in res["rows"]:
        r.setdefault("hyp_raw", r["hyp"])
        r["hyp"] = None if r["hyp_raw"] is None else strip_spill(r["hyp_raw"])
        r["wer"] = None if r["hyp"] is None else wer(r["ref"], r["hyp"])
    summ = res["summary"]
    ok = [r for r in res["rows"] if r["cond"] == "clean" and r["wer"] is not None]
    summ["clean"] = {"n": len(ok), "mean_wer": float(np.mean([r["wer"] for r in ok]))}
    for snr in SNRS:
        g = {(r["cond"], r["uid"]): r["wer"] for r in res["rows"] if r["snr_db"] == snr}
        uids = sorted({r["uid"] for r in res["rows"] if r["snr_db"] == snr})
        pairs = [(g[("unproc", u)], g[("gen19", u)]) for u in uids if g[("unproc", u)] is not None and g[("gen19", u)] is not None]
        d = [b - a for a, b in pairs]
        summ[f"{snr:+.0f} dB"] = {"n": len(pairs), "unproc_mean_wer": float(np.mean([a for a, _ in pairs])),
                                  "gen19_mean_wer": float(np.mean([b for _, b in pairs])),
                                  "delta_gen19_minus_unproc": bootstrap_ci(d),
                                  "better": int(sum(x < 0 for x in d)), "worse": int(sum(x > 0 for x in d)),
                                  "tied": int(sum(x == 0 for x in d))}
    res["meta"]["rescored"] = "amendment 3: check-sentence spill stripped from line 2 (hyp_raw keeps the original)"
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    site = json.loads((SITE_DATA / "listen.json").read_text())
    T = {(r["cond"], r["uid"], r["snr_db"]): r for r in res["rows"]}
    for c in site["clips"]:
        for cond in ["unproc", "gen19"]:
            r = T[(cond, c["utterance"], c["snr_db"])]
            c[cond]["transcript"] = r["hyp"]; c[cond]["wer"] = None if r["wer"] is None else round(r["wer"], 3)
    site["summary"] = {k: ({kk: (vv if not isinstance(vv, float) else round(vv, 3)) for kk, vv in v.items()} if isinstance(v, dict) else v)
                       for k, v in summ.items()}
    site["meta"]["rescored"] = res["meta"]["rescored"]
    (SITE_DATA / "listen.json").write_text(json.dumps(site, indent=1))
    print(json.dumps(summ, indent=1))


def summarize_site():
    """Plain-language totals for the site (share of the reader's words heard right), from results.json."""
    res = json.loads((HERE / "results.json").read_text())
    site = json.loads((SITE_DATA / "listen.json").read_text())
    plain = {}
    for key, snr in [("clean", None)] + [(f"{x:+.0f} dB", x) for x in SNRS]:
        for cond in (["clean"] if snr is None else ["unproc", "gen19"]):
            sel = [r for r in res["rows"] if r["cond"] == cond and r["snr_db"] == snr and r["hyp"] is not None]
            hr = [word_hits(r["ref"], r["hyp"]) for r in sel]
            plain.setdefault(key, {})[cond] = {"words_right": sum(a for a, _ in hr), "words_total": sum(b for _, b in hr),
                                               "unintelligible": sum("[unintelligible]" in r["hyp"] for r in sel), "n": len(sel)}
    site["plain"] = plain
    (SITE_DATA / "listen.json").write_text(json.dumps(site, indent=1))
    print(json.dumps(plain, indent=1))


def wav_b64(x):
    x = np.asarray(x, np.float32)
    pk = float(np.max(np.abs(x)) + 1e-9)
    if pk > 0.95:
        x = x * (0.95 / pk)
    b = io.BytesIO()
    sf.write(b, x, FS, format="WAV", subtype="PCM_16")
    return base64.b64encode(b.getvalue()).decode(), x


CHECK_PROMPT = ("This audio has two parts separated by a short pause. Part 1 is one short sentence read clearly. "
                "Part 2 is a recording of a person reading, sometimes in a noisy crowd. Write exactly what you hear, as two lines. "
                "Line 1: the words of part 1. Line 2: the words the main reader says in part 2. In part 2 write only words you "
                "actually hear; never guess, complete or continue a sentence; if you cannot make out any words in part 2, write "
                "[unintelligible] on line 2. Output only the two lines.")
CHECK = {}


def check_clip():
    """Delivery check: first 2.5-5 s clean utterance of validation speaker 5536 (sorted), not a test speaker."""
    if not CHECK:
        tx = transcripts("5536")
        f = next(f for f in sorted((LS / "5536").rglob("*.flac")) if 2.5 <= sf.info(str(f)).duration <= 5.0)
        x, _ = sf.read(str(f), dtype="float32")
        CHECK.update(uid=f.stem, text=tx[f.stem], audio=(x / (rms(x) + 1e-9) * 0.1).astype(np.float32))
    return CHECK


def with_check(x):
    c = check_clip()
    return np.concatenate([c["audio"], np.zeros(int(0.8 * FS), np.float32), np.asarray(x, np.float32)])


def split_reply(text):
    """Return (line1, rest) or None if the delivery check failed."""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    lines = [re.sub(r"^(line|part)\s*[12]\s*[:.-]\s*", "", l, flags=re.I) for l in lines]
    if len(lines) < 2 or wer(check_clip()["text"], lines[0]) > 0.5:
        return None
    return lines[0], " ".join(lines[1:])


def listen(b64, tries=4):
    for k in range(tries):
        with tempfile.TemporaryDirectory() as td:
            ev, out = Path(td) / "ev.json", Path(td) / "out.json"
            ev.write_text(json.dumps({"mode": "listen", "wav_b64": b64, "prompt": CHECK_PROMPT}))
            p = subprocess.run(["aws", "lambda", "invoke", "--function-name", "beforetheimplant-muse",
                                "--cli-binary-format", "raw-in-base64-out", "--cli-read-timeout", "300",
                                "--payload", f"file://{ev}", str(out)], capture_output=True, text=True)
            try:
                d = json.loads(out.read_text())
                sp = split_reply(d.get("text"))
                if sp:
                    return sp[1], (d.get("attempts") or 0) + 6 * k
                err = {"check_failed": (d.get("text") or "")[:160], "attempts": d.get("attempts")}
            except Exception as e:  # noqa: BLE001
                err = f"{e} {p.stderr[:200]}"
        print("  retry", k, str(err)[:200], flush=True)
        time.sleep(2 + 2 * k)
    return None, None


def main():
    t0 = time.time()
    utts = pick_utts()
    pool = load_pool(INTERF)
    enh = load_gen15(str(CKPT))
    rng = np.random.default_rng(20261117)
    jobs = []  # (key, audio)
    clips = []
    for u in utts:
        clean, sr = sf.read(str(u["path"]), dtype="float32")
        assert sr == FS
        clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
        u["clean"] = clean
        jobs.append((("clean", u["uid"], None), clean))
        for snr in SNRS:
            noise = babble(rng, pool, INTERF, k=int(rng.integers(8, 13)), n=len(clean))
            noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
            mix = (clean + noise).astype(np.float32)
            out = enh(mix)[: len(mix)]
            clips.append({"spk": u["spk"], "uid": u["uid"], "snr_db": snr, "ref": u["text"], "mix": mix, "gen19": out})
            jobs.append((("unproc", u["uid"], snr), mix))
            jobs.append((("gen19", u["uid"], snr), out))
    print(f"built {len(jobs)} clips in {time.time()-t0:.0f}s; transcribing", flush=True)
    enc = [(k, *wav_b64(with_check(x))) for k, x in jobs]
    with ThreadPoolExecutor(4) as ex:
        texts = list(ex.map(lambda j: listen(j[1]), enc))
    T = {k: t for (k, _, _), (t, _) in zip(enc, texts)}
    ATT = {k: a for (k, _, _), (_, a) in zip(enc, texts)}
    print(f"transcribed in {time.time()-t0:.0f}s; failures={sum(t is None for t, _ in texts)}", flush=True)

    rows = []
    for u in utts:
        rows.append({"cond": "clean", "spk": u["spk"], "uid": u["uid"], "snr_db": None, "ref": u["text"],
                     "hyp": T[("clean", u["uid"], None)],
                     "wer": None if T[("clean", u["uid"], None)] is None else wer(u["text"], T[("clean", u["uid"], None)])})
    for c in clips:
        for cond in ["unproc", "gen19"]:
            h = T[(cond, c["uid"], c["snr_db"])]
            rows.append({"cond": cond, "spk": c["spk"], "uid": c["uid"], "snr_db": c["snr_db"], "ref": c["ref"],
                         "hyp": h, "wer": None if h is None else wer(c["ref"], h)})

    for r in rows:
        r["attempts"] = ATT[(r["cond"], r["uid"], r["snr_db"])]
    summ = {"attempts_total": int(sum(a or 0 for _, a in texts)), "transcripts_failed": int(sum(t is None for t, _ in texts)),
            "clean": {"n": sum(r["wer"] is not None for r in rows if r["cond"] == "clean"),
                      "mean_wer": float(np.mean([r["wer"] for r in rows if r["cond"] == "clean" and r["wer"] is not None]))}}
    for snr in SNRS:
        g = {(r["cond"], r["uid"]): r["wer"] for r in rows if r["snr_db"] == snr}
        pairs = [(g[("unproc", u["uid"])], g[("gen19", u["uid"])]) for u in utts
                 if g[("unproc", u["uid"])] is not None and g[("gen19", u["uid"])] is not None]
        d = [b - a for a, b in pairs]
        summ[f"{snr:+.0f} dB"] = {"n": len(pairs), "unproc_mean_wer": float(np.mean([a for a, _ in pairs])),
                                  "gen19_mean_wer": float(np.mean([b for _, b in pairs])),
                                  "delta_gen19_minus_unproc": bootstrap_ci(d),
                                  "better": int(sum(x < 0 for x in d)), "worse": int(sum(x > 0 for x in d)),
                                  "tied": int(sum(x == 0 for x in d))}
    import hashlib
    meta = {"recognizer": "muse-spark-1.3 (Meta), /v1/responses input_audio via /v1/files file_id",
            "checkpoint": str(CKPT.relative_to(R.parent)), "checkpoint_sha256": hashlib.sha256(CKPT.read_bytes()).hexdigest(),
            "plan": "research/meta/plan.md (run 3, with delivery check)", "delivery_check_utterance": check_clip()["uid"], "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "audio_credit": "LibriSpeech, Panayotov et al. 2015, CC BY 4.0"}
    (HERE / "results.json").write_text(json.dumps({"meta": meta, "summary": summ, "rows": rows}, indent=1))
    print(json.dumps(summ, indent=1))

    # Site demo: one clip per speaker (first utterance), alternating 0 / -5 dB. Small mp3s.
    SITE_AUDIO.mkdir(parents=True, exist_ok=True)
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    demo = []
    for i, spk in enumerate(TEST_SPK):
        snr = SNRS[1] if i % 2 == 0 else SNRS[0]
        c = next(c for c in clips if c["spk"] == spk and c["snr_db"] == snr)
        item = {"id": f"{c['uid']}_{int(snr)}", "speaker": spk, "utterance": c["uid"], "snr_db": snr,
                "seconds": round(len(c["mix"]) / FS, 1), "reference": c["ref"].capitalize()}
        for cond in ["unproc", "gen19"]:
            name = f"{item['id']}_{cond}.mp3"
            _, x = wav_b64(c["mix"] if cond == "unproc" else c["gen19"])
            with tempfile.NamedTemporaryFile(suffix=".wav") as tf:
                sf.write(tf.name, x, FS, subtype="PCM_16")
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tf.name, "-ac", "1", "-b:a", "48k",
                                str(SITE_AUDIO / name)], check=True)
            h = T[(cond, c["uid"], snr)]
            item[cond] = {"audio": f"assets/audio/meta-lab/{name}", "transcript": h,
                          "wer": None if h is None else round(wer(c["ref"], h), 3)}
        demo.append(item)
    site = {"meta": {**meta, "n_clips_in_study": len(clips)},
            "summary": {k: ({kk: (vv if not isinstance(vv, float) else round(vv, 3)) for kk, vv in v.items()} if isinstance(v, dict) else v)
                        for k, v in summ.items()}, "clips": demo}
    (SITE_DATA / "listen.json").write_text(json.dumps(site, indent=1))
    print(f"DONE {time.time()-t0:.0f}s")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        rebuild_demo()
        summarize_site()
    elif "--rescore" in sys.argv:
        rescore()
        summarize_site()
    elif "--summarize" in sys.argv:
        summarize_site()
    else:
        main()
        summarize_site()
