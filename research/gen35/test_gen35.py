"""Gen35 checks: registered polarity per checkpoint; A0 is exactly the Gen34 v1 path; A1/A2 use the flushed delay;
A2 removes the decoder bias and is positively signed on held-out speech; export_enhance reproduces the published
enhance.py (snapshot in research/gen35/published/) and its repair changes only polarity and DC."""
import importlib.util, sys
from pathlib import Path
import numpy as np, pytest, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "gen33"))
import repair as RP  # noqa: E402
import linked  # noqa: E402


def _speech():
    import soundfile as sf
    f = sorted(Path("/tmp/gen12dl/LibriSpeech/dev-clean/5694").rglob("*.flac"))[0]
    x, _ = sf.read(f); x = x[:3 * 16000]
    return (x / np.sqrt(np.mean(x ** 2)) * 0.14).astype(np.float32)


def test_registered_polarity():
    pol = RP.registered_polarity()
    assert [pol[RP.sha(RP.CKPTS[s])] for s in (17, 18, 19)] == [-1, 1, -1]


@pytest.mark.parametrize("seed", [17, 18, 19])
def test_arms(seed):
    A = RP.Arms(RP.CKPTS[seed]); x = _speech(); o = A.outputs(x)
    v1, _ = linked.pair_fn(RP.CKPTS[seed], "independent")(x, x)
    assert np.array_equal(o["A0_existing"], np.asarray(v1, np.float32))           # exactly the Gen34 v1 path
    w = slice(256, -256)
    assert np.allclose(o["A2_repair"] + A.polarity * A.bias, o["A1_sign"], atol=1e-6)
    assert RP.signed_alpha(x, o["A2_repair"], w) > 0.5                             # positively signed on held-out speech
    assert abs(float(np.mean(o["A2_repair"][w]))) < abs(float(np.mean(o["A1_sign"][w])))
    assert np.array_equal(o["A0_existing"][-63:], np.zeros(63, np.float32))        # v1 pads the last 63 samples
    assert np.allclose(o["A1_sign"][:-63], A.polarity * o["A0_existing"][:-63], atol=1e-6)


def test_export_matches_published():
    spec = importlib.util.spec_from_file_location("pub_enh", HERE / "published" / "enhance.py")
    pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
    A = RP.Arms(RP.CKPTS[17]); x = (0.5 * _speech()).astype(np.float32)
    y_pub = pub.enhance(x, 16000, model=A.model)
    y_ours = RP.export_enhance(x, A.model)
    assert np.allclose(y_pub, y_ours, atol=1e-6)
    y_rep = RP.export_enhance(x, A.model, (A.polarity, A.bias)); w = slice(256, -256)
    assert RP.signed_alpha(x, y_rep, w) > 0 and RP.signed_alpha(x, y_pub, w) < 0
    assert abs(float(np.mean(y_rep[w]))) < abs(float(np.mean(y_pub[w])))
