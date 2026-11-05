"""Gen25-only copy of research/gen23/verify_provenance.py (kept separate so the
shared checker stays byte-identical to the version Gen 24 registered; Astra
Gen25 pre-launch review, blocking item 3), plus Gen25 recipe checks:
every input matches input_manifest.json, and the saved weights equal the
uniform average of the 9 registered inputs exactly.

Filing-time provenance check (Astra Gen23 code audit, non-blocking item 1):
the screen judge trusts *reported* hashes and bench summaries; this
re-derives them from the actual files.

- Rehashes the candidate and control checkpoints, then compares them with
  the train log, the bench meta, the dev rows and the R48 parent hash.
- Verifies the registered source hashes in the prereg table.
- Checks the final VAL item set equals the control's (no missing or
  duplicate items).
- Checks the candidate bench grid is complete and duplicate-free and
  equals the unproc and control grids.
- Recomputes the bench summary means (crowd, SSN, white, quiet) from raw
  rows. CIs are bootstrap draws, so only ci_lo <= mean <= ci_hi is
  checked for them.

Usage:
  python research/gen23/verify_provenance.py --gen 22 --seed 17   # cap30
  python research/gen23/verify_provenance.py --gen 23 --seed 17   # cs5
Exit code 1 on any failure.
"""
import argparse, hashlib, json, re, statistics, sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
ROOT = R.parent
GENS = {
    22: dict(log="gen22/weights/train_log_cap30_scratch_seed{seed}.json", ckpt="gen22/weights/cap30_scratch_seed{seed}.pt",
             bench="bench-n6/benchv2_g22cap30s{s}.json", dev="gen22/dev_audit_s{s}.json", cand="cap30", prereg=None),
    23: dict(log="gen23/weights/train_log_sisdr_cs5_scratch_seed{seed}.json", ckpt="gen23/weights/sisdr_cs5_scratch_seed{seed}.pt",
             bench="bench-n6/benchv2_g23cs5s{s}.json", dev="gen23/dev_audit_s{s}.json", cand="cs5", prereg="gen23/prereg.md"),
    25: dict(log="gen25/weights/val_log_swa9_seed{seed}.json", ckpt="gen25/weights/swa9_seed{seed}.pt",
             bench="bench-n6/benchv2_g25swa9s{s}.json", dev="gen25/dev_audit_s{s}.json", cand="swa9", prereg="gen25/prereg.md"),
    24: dict(log="gen24/weights/train_log_sisdr_hard60_scratch_seed{seed}.json", ckpt="gen24/weights/sisdr_hard60_scratch_seed{seed}.pt",
             bench="bench-n6/benchv2_g24hard60s{s}.json", dev="gen24/dev_audit_s{s}.json", cand="hard60", prereg="gen24/prereg.md"),
}
CTRL_CKPT = "gen19/weights/causal_seed{seed}.pt"
CTRL_BENCH = {17: "bench-n6/bench_v2_gen19.json", 18: "bench-n6/benchv2_gen19s2.json", 19: "bench-n6/benchv2_gen19s3.json"}
CTRL_LOG = "gen21/weights/train_log_r48_seed{seed}.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()  # noqa: E731
fails = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def grid(rows, system):
    keys = [(r["kind"], r["snr_db"], r["spk"], r["crop"]) for r in rows if r["system"] == system]
    return keys, set(keys)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen", type=int, choices=sorted(GENS), required=True)
    ap.add_argument("--seed", type=int, default=17)
    a = ap.parse_args()
    g, seed, s = GENS[a.gen], 20261100 + a.seed, a.seed
    f = lambda k: R / g[k].format(seed=seed, s=s)  # noqa: E731
    log, bench, dev = (json.loads(f(k).read_text()) for k in ("log", "bench", "dev"))
    cbench = json.loads((R / CTRL_BENCH[s]).read_text())
    clog = json.loads((R / CTRL_LOG.format(seed=seed)).read_text())

    cand_sha, ctrl_sha = sha(f("ckpt")), sha(R / CTRL_CKPT.format(seed=seed))
    check(cand_sha == log["weights_sha256"] == bench["meta"]["checkpoint_sha256"]
          == next(iter({r["sha256"] for r in dev["rows"] if r["system"] == g["cand"]})),
          f"candidate file sha {cand_sha[:12]} == log == bench meta == dev rows")
    check({r["sha256"] for r in dev["rows"] if r["system"] == g["cand"]} == {cand_sha}, "dev candidate rows carry one hash")
    check(ctrl_sha == cbench["meta"]["checkpoint_sha256"] == clog["parent_sha256"]
          and {r["sha256"] for r in dev["rows"] if r["system"] == "control"} == {ctrl_sha},
          f"control file sha {ctrl_sha[:12]} == control bench == R48 parent == dev control rows")

    if g["prereg"]:
        table = re.findall(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", (R / g["prereg"]).read_text())
        check(len(table) >= 6, f"prereg lists {len(table)} source hashes")
        for name, h in table:
            check(sha(R / name) == h, f"source hash {name}")

    final = [e for e in log["val_log"] if e["lifetime_step"] == log["lifetime_steps"]]
    c0 = [e for e in clog["val_log"] if e["lifetime_step"] == 24000]
    check(len(final) == 1 and len(c0) == 1, "unique final VAL entry and control step-0 entry")
    ki = lambda e: [(it["idx"], it["spk"], it["snr"]) for it in e["items"]]  # noqa: E731
    check(len(ki(final[0])) == len(set(ki(final[0]))) and set(ki(final[0])) == set(ki(c0[0])),
          f"VAL item set complete/duplicate-free ({len(ki(final[0]))} items) and equal to control's")

    cand = bench["meta"]["candidate"]
    ck, cs = grid(bench["rows"], cand)
    uk, us = grid(bench["rows"], "unproc")
    ctk, cts = grid(cbench["rows"], cbench["meta"]["candidate"])
    check(len(ck) == len(cs) and cs == us == cts, f"bench grid: {len(ck)} candidate rows, duplicate-free, == unproc == control grid")
    U = {(r["kind"], r["snr_db"], r["spk"], r["crop"]): r for r in bench["rows"] if r["system"] == "unproc"}
    C = {(r["kind"], r["snr_db"], r["spk"], r["crop"]): r for r in bench["rows"] if r["system"] == cand}
    summ = bench["summary"][cand]
    for kind in ("crowd", "ssn", "white-heldout", "competing"):
        for m in ("sisdr", "stoi", "ace_electro_corr"):
            d = [C[k][m] - U[k][m] for k in C if k[0] == kind]
            row = summ[kind][f"d_{m}"]
            check(abs(statistics.fmean(d) - row["mean"]) < 1e-9 and row["ci_lo"] <= row["mean"] <= row["ci_hi"] and row["n"] == len(d),
                  f"summary {kind} d_{m} mean {row['mean']:+.4f} recomputed from {len(d)} raw pairs")
    q = [C[k] for k in C if k[0] == "quiet"]
    check(abs(statistics.fmean(r["sisdr"] for r in q) - summ["quiet"]["sisdr"]) < 1e-9, f"quiet abs SI-SDR {summ['quiet']['sisdr']:.2f} recomputed")
    if a.gen == 25:
        import torch
        man = json.loads((R / "gen25/input_manifest.json").read_text())
        ins = log.get("inputs", [])
        check(len(ins) == 9 and [i["step"] for i in ins] == list(range(20000, 24000, 500)) + [24000],
              "candidate built from exactly the 9 registered steps")
        check(all(man.get(i["path"]) == i["sha256"] == sha(ROOT / i["path"]) for i in ins),
              "every input file matches the committed manifest")
        sds = [torch.load(ROOT / i["path"], map_location="cpu", weights_only=False)["state_dict"] for i in ins]
        got = torch.load(f("ckpt"), map_location="cpu", weights_only=False)["state_dict"]
        exp = {k: torch.stack([sd[k].float() for sd in sds]).mean(0).to(sds[-1][k].dtype) for k in sds[-1]}
        check(set(got) == set(exp) and all(torch.equal(got[k], exp[k]) for k in exp),
              "saved weights == uniform average of the 9 inputs (bit-exact)")
    print("PROVENANCE " + ("PASS" if not fails else f"FAIL ({len(fails)})"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
