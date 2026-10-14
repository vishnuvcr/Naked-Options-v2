import importlib.util
from pathlib import Path
import numpy as np
SCRIPT=Path(__file__).with_name("entry_exit_backtest.py")
spec=importlib.util.spec_from_file_location("entry_exit",SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def test_lot_proxy_is_positive():
    assert mod.legacy.lot_size_proxy("2026-10-13")>0

def test_legacy_straddle_costs_include_four_orders():
    t={"entry_prices":[100,100],"exit_prices":[110,90],"trade_date":"2026-10-13","lot_size":65,"structure":"straddle"}
    x=mod.legacy.calculate_trade(t,50,10)
    assert x["brokerage_rupees"]==40

def test_single_leg_costs_include_two_orders():
    x=mod.single_leg_cost("2026-10-13",100,110,65,0,10)
    assert x["brokerage_rupees"]==20
    assert x["net_pnl_rupees"] < x["gross_pnl_rupees"]

def test_slippage_reduces_single_leg_net_pnl():
    x0=mod.single_leg_cost("2026-10-13",100,130,65,0,10)
    x100=mod.single_leg_cost("2026-10-13",100,130,65,100,10)
    assert x100["net_pnl_rupees"] < x0["net_pnl_rupees"]

def test_higher_brokerage_reduces_net_pnl():
    x10=mod.single_leg_cost("2026-10-13",100,130,65,50,10)
    x20=mod.single_leg_cost("2026-10-13",100,130,65,50,20)
    assert x20["net_pnl_rupees"] < x10["net_pnl_rupees"]

def test_holm_is_monotone_in_sorted_p_values():
    adjusted=mod.holm([0.01,0.02,0.50])
    assert adjusted[0] <= adjusted[1] <= adjusted[2]
    assert all(0<=x<=1 for x in adjusted)

def test_block_ci_reproducible_and_ordered():
    a=mod.block_ci([1,-1,2,-2,3,-3,4,-4],42)
    b=mod.block_ci([1,-1,2,-2,3,-3,4,-4],42)
    assert a==b
    assert a[0] <= a[1]

def test_single_leg_rejects_invalid_premium():
    try:
        mod.single_leg_cost("2026-10-13",0,110,65,0,10)
    except ValueError:
        return
    raise AssertionError("invalid premium must be rejected")

def test_random_signal_is_reproducible():
    import pandas as pd
    rows=[]
    for i,t in enumerate(["09:%02d"%(i*5) for i in range(12)]):
        rows.append({"time":t,"spot":22000+i*5,"option_type":"CALL","strike":22000,"open":100,"high":105,"low":95,"close":101})
    g=pd.DataFrame(rows)
    assert mod.signals(g,123)==mod.signals(g,123)
