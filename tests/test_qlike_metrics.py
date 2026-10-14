import numpy as np
from forecast_metrics import qlike_metrics


def test_qlike_improvement_uses_score_difference_even_when_scores_negative():
    actual = np.array([0.01, 0.02, 0.015, 0.012])
    pred = actual.copy()
    baseline = np.full(4, 0.02)
    out = qlike_metrics(actual, pred, baseline)
    assert np.isfinite(out["qlike"])
    assert np.isfinite(out["qlike_baseline"])
    assert out["qlike_baseline"] < 0
    assert out["qlike_improvement_vs_baseline"] > 0
    assert "qlike_skill_vs_baseline" not in out


def test_qlike_improvement_sign_reverses_for_worse_forecast():
    actual = np.array([0.01, 0.02, 0.015, 0.012])
    good = actual.copy()
    bad = np.full(4, 0.04)
    out = qlike_metrics(actual, bad, good)
    assert out["qlike_improvement_vs_baseline"] < 0


def test_qlike_empty_finite_overlap_is_null():
    out = qlike_metrics([np.nan], [0.01], [0.02])
    assert out == {
        "qlike": None,
        "qlike_baseline": None,
        "qlike_improvement_vs_baseline": None,
    }
