"""Gen16 loss tests. Run: /tmp/gen9env/bin/python -m pytest research/gen16/test_gen16.py -q"""
import sys
from pathlib import Path
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from train5 import ace_envelope_loss, ace_filterbank  # noqa: E402


def test_ace_filterbank_shape_and_coverage():
    fb = ace_filterbank()
    assert fb.shape == (22, 257)
    assert float(fb.sum(dim=1).min()) >= 1.0


def test_envelope_loss_zero_for_identical_and_positive_otherwise():
    torch.manual_seed(0)
    x = torch.randn(2, 16000) * 0.1
    fb = ace_filterbank()
    assert float(ace_envelope_loss(x, x, fb)) < 1e-6
    y = torch.randn(2, 16000) * 0.1
    assert float(ace_envelope_loss(x, y, fb)) > 0.01


def test_envelope_loss_backpropagates():
    x = (torch.randn(1, 8000) * 0.1).requires_grad_(True)
    ref = torch.randn(1, 8000) * 0.1
    loss = ace_envelope_loss(x, ref, ace_filterbank())
    loss.backward()
    assert x.grad is not None and torch.isfinite(x.grad).all()
