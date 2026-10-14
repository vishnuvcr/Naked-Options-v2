import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from forecast_metrics import regmetrics,clsmetrics,hac_test,block_ci,holm

def test_regression_metrics_match_hand_values():
    m=regmetrics([1,2,3],[1,3,2],[0,0,0])
    assert m["mae"]==2/3
    assert np.isclose(m["rmse"],np.sqrt(2/3))
    assert m["mse_skill_vs_baseline"]==pytest.approx(1-(2/3)/(14/3))

def test_classification_probabilistic_metrics():
    m=clsmetrics([0,1,0,1],[.1,.9,.4,.6],[.5,.5,.5,.5])
    assert m["accuracy"]==1
    assert m["brier_skill"]>0
    assert m["roc_auc"]==1

def test_holm_is_monotone_and_bounded():
    a=holm([.01,.04,.03,None])
    assert a[0] <= a[2] <= a[1]
    assert a[3] is None
    assert all(x is None or 0<=x<=1 for x in a)

def test_block_bootstrap_is_reproducible():
    a=block_ci(np.arange(50),5,seed=17,reps=100)
    b=block_ci(np.arange(50),5,seed=17,reps=100)
    assert a==b


def test_oos_r2_is_relative_to_forecast_baseline():
    m=regmetrics([1,2,3],[1,3,2],[0,0,0])
    expected=1-(2/3)/(14/3)
    assert m["oos_r2_vs_baseline"]==pytest.approx(expected)
    assert m["mse_skill_vs_baseline"]==pytest.approx(expected)
