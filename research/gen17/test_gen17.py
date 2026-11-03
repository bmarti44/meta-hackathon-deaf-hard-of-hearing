"""Gen17 trainer contract tests (no training run)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "bench-n6"))
from train6 import TEST_BABBLE_SPK, TEST_SPK, TRAIN_SPK, VAL_SPK  # noqa: E402
from bench_v2 import TEST_INTERFERERS, TEST_SPK_V2, TRAIN_SPK_V2, VAL_SPK as BV2_VAL  # noqa: E402


def test_splits_match_prereg():
    assert TRAIN_SPK == TRAIN_SPK_V2 and len(TRAIN_SPK) == 26
    assert TEST_SPK == TEST_SPK_V2 and TEST_BABBLE_SPK == TEST_INTERFERERS
    assert VAL_SPK == BV2_VAL
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK + VAL_SPK))
