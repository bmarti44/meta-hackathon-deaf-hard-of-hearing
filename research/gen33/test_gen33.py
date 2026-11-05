"""Gen33 engineering checks (Astra's Gen32 review): identical-ear parity with the mono output, ear-swap symmetry,
causal prefixes, mono rebuild == model(x), legacy reproduction in independent mode, and the decision script's
subset coverage (a 'linked' document that is really the independent one must be REJECTED on L2)."""
import copy, importlib.util, json, sys
from pathlib import Path
import pytest, torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import linked  # noqa: E402

CK = {"gen19": REPO / "research/gen19/weights/causal_seed20261117.pt",
      "gen32": REPO / "research/gen32/weights/wiseftpd_seed20261117.pt"}


@pytest.mark.parametrize("which", ["gen19", "gen32"])
def test_parity_swap_causality(which):
    m = linked.load(CK[which]); g = torch.Generator().manual_seed(3)
    x, y = torch.randn(2, 24000, generator=g) * 0.1, torch.randn(2, 24000, generator=g) * 0.1
    with torch.no_grad():
        mono = m(x)
        assert torch.equal(linked.forward_mono(m, x), mono)
        l, r = linked.forward_linked(m, x, x)
        assert torch.equal(l, mono) and torch.equal(r, mono)
        a, b = linked.forward_linked(m, x, y); c, d = linked.forward_linked(m, y, x)
        assert torch.equal(a, d) and torch.equal(b, c)
        x2 = x.clone(); x2[:, 15000:] += torch.randn(2, 9000, generator=g)
        e, f = linked.forward_linked(m, x2, y)
        assert torch.equal(e[:, :15000], a[:, :15000]) and torch.equal(f[:, :15000], b[:, :15000])


def test_legacy_reproduction_independent():
    import spatial_linked as S
    for ck, ref in ((CK["gen32"], REPO / "research/gen32/spatial_wiseftpd_s17.json"),
                    (CK["gen19"], REPO / "research/gen27/selftest/spatial_gen19_s17.json")):
        L = json.loads(ref.read_text())
        d = S.run(ck, "independent", L["meta"]["candidate"], extras=False)
        assert d["existing"]["rows"] == L["existing"]["rows"] and d["existing"]["summary"] == L["existing"]["summary"]
        assert d["crossed_rows"] == L["crossed_rows"]


def test_judge_rejects_fake_linked(tmp_path):
    import spatial_linked as S
    spec = importlib.util.spec_from_file_location("judge_link_t", HERE / "judge_link.py")
    J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
    g32 = S.run(CK["gen32"], "independent", "wiseftpd"); g19 = S.run(CK["gen19"], "independent", "gen19")
    fake = copy.deepcopy(g32); fake["meta"]["mode"] = "linked"
    for p, d in (("lk", fake), ("g32", g32), ("g19", g19)):
        (tmp_path / f"{p}.json").write_text(json.dumps(d))
    doc = J.judge(tmp_path / "lk.json", tmp_path / "g32.json", tmp_path / "g19.json",
                  REPO / "research/gen27/selftest/spatial_gen19_s17.json")
    assert doc["checks"]["L2_mean_ILD_below_independent_gen32"] is False and doc["verdict"] == "REJECTED"
    assert len(doc["L3"]) == 16 and len(doc["L4"]) == 40
    assert all(v == 0.0 for k, v in doc["L4"].items() if k.startswith("gen32_indep"))


def test_judge_refuses_incomplete_or_duplicate_grids(tmp_path):
    """Astra pre-launch blocking 1: a missing or duplicated row must stop the judge, never change its verdict."""
    import spatial_linked as S
    spec = importlib.util.spec_from_file_location("judge_link_t2", HERE / "judge_link.py")
    J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
    g32 = S.run(CK["gen32"], "independent", "wiseftpd"); g19 = S.run(CK["gen19"], "independent", "gen19")
    base = copy.deepcopy(g32); base["meta"]["mode"] = "linked"
    ctrl = REPO / "research/gen27/selftest/spatial_gen19_s17.json"
    (tmp_path / "g32.json").write_text(json.dumps(g32)); (tmp_path / "g19.json").write_text(json.dumps(g19))
    def drop(d, cond):
        i = next(j for j, r in enumerate(d["extra_rows"]) if r["system"] == "wiseftpd" and r["cond"] == cond); d["extra_rows"].pop(i); return d
    def dup(d, cond):
        r = next(r for r in d["extra_rows"] if r["system"] == "wiseftpd" and r["cond"] == cond); d["extra_rows"].append(dict(r)); return d
    for mk in (lambda d: drop(d, "noisy"), lambda d: drop(d, "target_only"), lambda d: dup(d, "noisy")):
        (tmp_path / "lk.json").write_text(json.dumps(mk(copy.deepcopy(base))))
        with pytest.raises(SystemExit, match="INVALID"):
            J.judge(tmp_path / "lk.json", tmp_path / "g32.json", tmp_path / "g19.json", ctrl)


def test_sisdr_is_the_established_implementation():
    import spatial_linked as S
    sys.path.insert(0, str(REPO / "research/gen24"))
    import train13
    import numpy as np
    rng = np.random.default_rng(0); x = rng.normal(size=8000) + 0.5; y = x + 0.01 * rng.normal(size=8000)
    assert S._sisdr is train13._si_sdr_np and S._sisdr(x, y) == train13._si_sdr_np(x, y)
