import importlib.util
from pathlib import Path
SCRIPT=Path(__file__).with_name("entry_exit_backtest.py")
spec=importlib.util.spec_from_file_location("entry_exit",SCRIPT)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def test_lot_proxy_is_positive():
 assert mod.legacy.lot_size_proxy("2026-10-13")>0
def test_costs_include_four_executed_orders_for_straddle():
 t={"entry_prices":[100,100],"exit_prices":[110,90],"trade_date":"2026-10-13","lot_size":65,"structure":"straddle"}
 x=mod.legacy.calculate_trade(t,50,10)
 assert x["brokerage_rupees"]==40
def test_slippage_reduces_net_pnl():
 t={"entry_prices":[100,100],"exit_prices":[130,100],"trade_date":"2026-10-13","lot_size":65,"structure":"straddle"}
 assert mod.legacy.calculate_trade(t,100,10)["net_pnl_rupees"] < mod.legacy.calculate_trade(t,0,10)["net_pnl_rupees"]
