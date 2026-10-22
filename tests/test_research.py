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


def test_merge_results_skips_empty_or_headerless_csv(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from merge_results import read_csv_if_populated

    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    assert read_csv_if_populated(empty) is None

    headerless = tmp_path / "headerless.csv"
    headerless.write_text("\n", encoding="utf-8")
    assert read_csv_if_populated(headerless) is None

    valid = tmp_path / "valid.csv"
    valid.write_text("metric,value\nmae,0.1\n", encoding="utf-8")
    frame = read_csv_if_populated(valid)
    assert frame is not None
    assert list(frame.columns) == ["metric", "value"]
    assert frame.iloc[0]["metric"] == "mae"

def test_future_volatility_requires_complete_forward_window():
    out=build(sample())
    # The h-session future-volatility target uses h forward daily returns;
    # every one of the final h origins is therefore ineligible.
    for h in (1,5,20):
        vol=out[f"target_future_vol_{h}"]
        expansion=out[f"target_vol_expansion_{h}"]
        assert vol.iloc[-h:].isna().all()
        assert expansion.iloc[-h:].isna().all()
        assert np.isfinite(vol.iloc[-h-1])
        assert pd.notna(expansion.iloc[-h-1])

