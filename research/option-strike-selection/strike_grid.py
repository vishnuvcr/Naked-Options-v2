#!/usr/bin/env python3
"""Frozen OPT-BUY-2.0 strike grid; sanitized aggregate outputs only."""
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/option-validation"))
import backtest as bt

OUT = ROOT / "reports/option_strike_selection"
CALL_OFFSETS = (0, 1, 2, 3)
PUT_OFFSETS = (0, -1, -2, -3)
HORIZONS = (5, 20)
SLIPPAGES = (0, 25, 50, 100)
BROKERAGE = (10, 20)
PRIMARY_SLIP, PRIMARY_BROKER = 50, 10

def candidate_trade(day, call_off, put_off, day_quotes, exit_lookup):
    q = day_quotes.get(str(day))
    if q is None or q.empty: return None, "NO_QUOTES"
    entry = q[q.time == bt.ENTRY_TIME]
    if entry.empty: return None, "MISSING_ENTRY"
    legs = []
    for typ, off in (("CALL", call_off), ("PUT", put_off)):
        z = entry[(entry.option_type == typ) & (pd.to_numeric(entry.relative_offset, errors="coerce") == off)]
        z = z.drop_duplicates("strike")
        strikes = pd.to_numeric(z.strike, errors="coerce").dropna().unique()
        if len(strikes) != 1: return None, f"MISSING_OR_AMBIGUOUS_{typ}_OFFSET_{off}"
        strike = float(strikes[0])
        premium = pd.to_numeric(z.loc[np.isclose(z.strike.astype(float), strike), "open"], errors="coerce").dropna()
        if premium.empty or premium.iloc[0] <= 0: return None, f"BAD_{typ}_ENTRY"
        exit_px = bt.match_exit_price(exit_lookup, str(day), typ, strike)
        if exit_px is None: return None, f"MISSING_{typ}_SAME_STRIKE_EXIT"
        legs.append((float(premium.iloc[0]), float(exit_px), strike))
    return {"trade_date": str(day), "structure": f"C{call_off}_P{put_off}",
            "entry_prices": [x[0] for x in legs], "exit_prices": [x[1] for x in legs],
            "lot_size": bt.lot_size_proxy(str(day)), "call_strike": legs[0][2], "put_strike": legs[1][2]}, "PASS"

def ci_mean(x, block):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 2: return [float("nan"), float("nan")]
    return list(bt.block_bootstrap_mean(x, block_len=block, n_boot=2000, seed=bt.SEED+block))

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = bt.OPTION_CACHE / "manifest.json"
    if not manifest_path.exists(): raise SystemExit("BLOCKED: option cache manifest missing")
    manifest = json.loads(manifest_path.read_text())
    quotes, qmeta = bt.load_quote_table(manifest)
    if quotes.empty:
        OUT.mkdir(parents=True, exist_ok=True)
        summary = {"study":"OPT-BUY-2.0","status":"BLOCKED_NO_USABLE_QUOTES",
          "quotes":qmeta,"acquisition_status":manifest.get("status"),
          "requests_planned":manifest.get("requests_planned"),
          "requests_successful_or_empty":manifest.get("requests_successful_or_empty"),
          "requests_cached":manifest.get("requests_cached"),
          "requests_failed":manifest.get("requests_failed"),
          "failure_summaries":manifest.get("failure_summaries", {}),
          "confirmatory_gate_pass":False,
          "decision":"No strike-performance analysis was run because the manifest contained no usable quote rows. No winner or P&L inference is permitted."}
        (OUT/"run_summary.json").write_text(json.dumps(summary,indent=2,default=str))
        pd.DataFrame([{"candidate":f"C{co}_P{po}","call_offset":co,"put_offset":po,
          "total_test_dates":0,"eligible_dates":0,"coverage":0.0,"skip_counts":"NO_USABLE_QUOTES"}
          for co in CALL_OFFSETS for po in PUT_OFFSETS]).to_csv(OUT/"coverage.csv",index=False)
        pd.DataFrame(columns=["candidate","call_offset","put_offset","horizon","mode","slippage_bps_per_side",
          "brokerage_per_order_rupees","eligible_dates","trade_count","coverage",
          "mean_net_pnl_per_eligible_date_rupees","ci95_low_rupees","ci95_high_rupees",
          "mean_net_pnl_per_trade_rupees","mean_net_return_per_trade","win_rate",
          "first_half_mean_pnl","second_half_mean_pnl"]).to_csv(OUT/"candidate_metrics.csv",index=False)
        pd.DataFrame(columns=["date","candidate","horizon","mode","alert","did_trade",
          "slippage_bps_per_side","brokerage_per_order","net_pnl_rupees","net_return_on_debit",
          "call_offset","put_offset"]).to_csv(OUT/"primary_ledger.csv",index=False)
        print(json.dumps(summary,indent=2,default=str))
        return
    frame = bt.read_daily_and_build_matrix()
    signals, classifier_meta = bt.build_signals(frame)
    days = sorted(signals.trade_date.astype(str).unique())
    day_quotes = {str(d): g.reset_index(drop=True) for d,g in quotes.groupby("date", sort=False)}
    exit_lookup = {(str(r.date), bt.EXIT_TIME, str(r.option_type), round(float(r.strike),6)):float(r.close)
        for r in quotes.loc[quotes.time == bt.EXIT_TIME].itertuples(index=False)
        if np.isfinite(float(r.close)) and float(r.close)>0}
    sig = {(str(r.trade_date), int(r.horizon)): (bool(r.alert), float(r.probability), float(r.threshold))
           for r in signals.itertuples(index=False)}
    rows=[]; ledger=[]; coverage=[]
    for co in CALL_OFFSETS:
      for po in PUT_OFFSETS:
        label=f"C{co}_P{po}"
        trades={}; skips={}
        for d in days:
          tr, reason=candidate_trade(d,co,po,day_quotes,exit_lookup)
          trades[d]=tr
          if tr is None: skips[reason]=skips.get(reason,0)+1
        elig=[d for d in days if trades[d] is not None]
        coverage.append({"candidate":label,"call_offset":co,"put_offset":po,"total_test_dates":len(days),
                         "eligible_dates":len(elig),"coverage":len(elig)/max(len(days),1),"skip_counts":json.dumps(skips,sort_keys=True)})
        for h in HORIZONS:
          for slip in SLIPPAGES:
           for broker in BROKERAGE:
            for mode in ("always_buy","model_filtered"):
             pnl_by_date=[]
             trade_count=0; win_count=0; trade_pnls=[]; trade_returns=[]
             for d in elig:
              alert=sig.get((d,h),(False,float("nan"),float("nan")))[0]
              take=(mode=="always_buy" or alert)
              if take:
               result=bt.calculate_trade(trades[d],slip,broker); pnl=float(result["net_pnl_rupees"])
               trade_count+=1; trade_pnls.append(pnl); trade_returns.append(float(result["net_return_on_debit"]))
               win_count += int(pnl>0)
              else: pnl=0.0
              pnl_by_date.append(pnl)
              if slip==PRIMARY_SLIP and broker==PRIMARY_BROKER:
               ledger.append({"date":d,"candidate":label,"horizon":h,"mode":mode,"alert":alert,"did_trade":take,
                 "slippage_bps_per_side":slip,"brokerage_per_order":broker,"net_pnl_rupees":pnl,
                 "net_return_on_debit":float(result["net_return_on_debit"]) if take else 0.0,
                 "call_offset":co,"put_offset":po})
             half=len(pnl_by_date)//2
             lo,hi=ci_mean(pnl_by_date,h)
             rows.append({"candidate":label,"call_offset":co,"put_offset":po,"horizon":h,"mode":mode,
               "slippage_bps_per_side":slip,"brokerage_per_order_rupees":broker,"eligible_dates":len(elig),
               "trade_count":trade_count,"coverage":len(elig)/max(len(days),1),
               "mean_net_pnl_per_eligible_date_rupees":float(np.mean(pnl_by_date)) if pnl_by_date else float("nan"),
               "ci95_low_rupees":lo,"ci95_high_rupees":hi,
               "mean_net_pnl_per_trade_rupees":float(np.mean(trade_pnls)) if trade_pnls else float("nan"),
               "mean_net_return_per_trade":float(np.mean(trade_returns)) if trade_returns else float("nan"),
               "win_rate":float(win_count/trade_count) if trade_count else float("nan"),
               "first_half_mean_pnl":float(np.mean(pnl_by_date[:half])) if half else float("nan"),
               "second_half_mean_pnl":float(np.mean(pnl_by_date[half:])) if len(pnl_by_date)-half else float("nan")})
    pd.DataFrame(coverage).to_csv(OUT/"coverage.csv",index=False)
    pd.DataFrame(rows).to_csv(OUT/"candidate_metrics.csv",index=False)
    pd.DataFrame(ledger).to_csv(OUT/"primary_ledger.csv",index=False)
    status={"study":"OPT-BUY-2.0","status":"EXPLORATORY_DATA_GATE_REVIEW_REQUIRED",
      "protocol_version":"frozen-1.0","quotes":qmeta,"classifier":classifier_meta,
      "candidate_count":len(CALL_OFFSETS)*len(PUT_OFFSETS),"horizons":list(HORIZONS),
      "cost_sensitivity_slippage_bps":list(SLIPPAGES),"brokerage_per_order":list(BROKERAGE),
      "primary_costs":{"slippage_bps_per_side":PRIMARY_SLIP,"brokerage_per_order_rupees":PRIMARY_BROKER},
      "date_count":len(days),"coverage_minimum":0.80,"conflict_maximum":0.01,
      "confirmatory_gate_pass":bool(qmeta.get("conflict_rate_among_duplicate_groups",1)<=0.01 and
        all(x["coverage"]>=0.80 for x in coverage)),
      "warning":"Descriptive strike-grid output is not strategy approval. Any failed quality gate makes all candidate ranking exploratory."}
    (OUT/"run_summary.json").write_text(json.dumps(status,indent=2,default=str))
    print(json.dumps(status,indent=2,default=str))
if __name__=="__main__": main()
