"""Unit tests for time alignment and target construction."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_feature_matrix import build

def sample(n=140):
    dates=pd.bdate_range("2020-01-01",periods=n)
    c=100*np.exp(np.cumsum(np.linspace(-.002,.002,n)))
    return pd.DataFrame({"date":dates,"open":c*.999,"high":c*1.01,"low":c*.99,
      "close":c,"volume":np.arange(n)+100,"source_id":"synthetic_test"})

def test_forward_return_uses_future_close():
    d=sample()
    out=build(d)
    for i in (30,50,100):
        assert np.isclose(out.loc[i,"target_return_1"],np.log(d.close.iloc[i+1]/d.close.iloc[i]))
        assert np.isclose(out.loc[i,"target_return_5"],np.log(d.close.iloc[i+5]/d.close.iloc[i]))
        assert out.loc[i,"target_date_1"]==d.date.iloc[i+1].strftime("%Y-%m-%d")

def test_future_labels_are_not_filled_at_end():
    out=build(sample())
    assert pd.isna(out.iloc[-1]["target_return_1"])
    assert pd.isna(out.iloc[-5]["target_return_5"])
    assert pd.isna(out.iloc[-20]["target_return_20"])
    assert pd.isna(out.iloc[-1]["target_direction_1"])

def test_one_step_volatility_is_absolute_next_return():
    d=sample()
    out=build(d)
    expected=abs(np.log(d.close.iloc[51]/d.close.iloc[50]))
    assert np.isclose(out.loc[50,"target_future_vol_1"],expected)

def test_feature_values_do_not_depend_on_future_rows():
    d=sample()
    full=build(d)
    prefix=build(d.iloc[:80].copy())
    cols=["ret_0","ret_1","mom_20","vol_20","range","gap"]
    for col in cols:
        assert np.allclose(full.loc[:69,col],prefix.loc[:69,col],equal_nan=True)

def test_forward_volatility_requires_full_horizon_window():
    out=build(sample(140))
    assert out.target_future_vol_5.iloc[-5:].isna().all()
    assert out.target_future_vol_20.iloc[-20:].isna().all()
    assert out.target_future_vol_5.iloc[-6].notna()
    assert out.target_future_vol_20.iloc[-21].notna()
