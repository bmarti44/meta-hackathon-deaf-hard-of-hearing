"""Spatial-cue bench tests. Run: /tmp/gen9env/bin/python -m pytest research/bench-n6/test_spatial.py -q"""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import FS  # noqa: E402
from spatial import ild_per_band, itd_samples, render_at  # noqa: E402


def _tone(n=FS):
    t = np.arange(n) / FS
    return (0.1 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)


def test_front_is_symmetric():
    L, R = render_at(_tone(), 0.0)
    assert np.allclose(L, R, atol=1e-6)
    assert abs(itd_samples(L, R)) <= 1


def test_right_source_right_ear_louder_and_earlier():
    L, R = render_at(_tone(), 60.0)
    ild = ild_per_band(L, R)
    assert float(np.mean(ild)) < -1.0, "ILD defined L-R dB; right source must be negative"
    assert itd_samples(L, R) > 3, "left ear must lag for a right-side source"


def test_ild_sign_flips_with_side():
    Ll, Rl = render_at(_tone(), -60.0)
    assert float(np.mean(ild_per_band(Ll, Rl))) > 1.0
