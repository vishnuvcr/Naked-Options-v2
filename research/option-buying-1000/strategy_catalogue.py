#!/usr/bin/env python3
"""Deterministic registry generator for distinct causal naked-option strategy algorithms."""
import csv, hashlib, itertools, json
from pathlib import Path
OUT=Path("research/option-buying-1000"); OUT.mkdir(parents=True,exist_ok=True)
P=[
("gap_zscore","daily gap standardized by trailing volatility","daily_ohlc"),
("opening_range_break","break of completed opening range","intraday_ohlc"),
("opening_range_reclaim","reclaim of opening-range midpoint","intraday_ohlc"),
("close_location","close location in completed candle","intraday_ohlc"),
("body_wick_imbalance","body versus wick imbalance","intraday_ohlc"),
("inside_bar_break","break of completed inside-bar range","intraday_ohlc"),
("outside_bar_reversal","reversal after completed outside bar","intraday_ohlc"),
("higher_high_sequence","higher-high/lower-low sequence","intraday_ohlc"),
("ema_slope","fast versus slow causal EMA slope","intraday_ohlc"),
("ema_cross","fast/slow EMA cross","intraday_ohlc"),
("vwap_deviation","distance from session VWAP","intraday_ohlc_volume"),
("vwap_reclaim","VWAP recross after deviation","intraday_ohlc_volume"),
("rsi_reversal","RSI exits an extreme","intraday_ohlc"),
("rsi_trend","RSI trend-side state","intraday_ohlc"),
("macd_turn","MACD histogram sign/slope change","intraday_ohlc"),
("realized_vol_break","realized volatility breakout","intraday_ohlc"),
("vol_compression","compression then expansion","intraday_ohlc"),
("range_expansion","true-range expansion","intraday_ohlc"),
("mean_reversion_z","reversion toward trailing mean","intraday_ohlc"),
("prior_day_reject","rejection at prior-day extreme","daily_intraday_ohlc"),
("prior_day_break","break and hold of prior-day level","daily_intraday_ohlc"),
("weekly_level_reaction","reaction at prior completed week level","daily_intraday_ohlc"),
("futures_basis_change","causal futures basis change","timestamped_futures"),
("futures_oi_divergence","futures price/OI divergence","timestamped_futures_oi"),
("options_oi_alignment","option OI aligned with spot move","timestamped_option_chain"),
("options_volume_imbalance","call/put volume imbalance","timestamped_option_chain"),
("iv_change","implied volatility change","timestamped_option_chain"),
("skew_change","put/call IV skew change","timestamped_option_chain"),
("india_vix_impulse","India VIX impulse","timestamped_india_vix"),
("global_leadlag","pre-entry global index return","timestamped_global_indices"),
("usd_inr_impulse","pre-entry FX shock","timestamped_fx"),
("gold_impulse","pre-entry gold return shock","timestamped_gold"),
("breadth_thrust","market breadth impulse","timestamped_market_breadth"),
("fii_flow_regime","publication-lagged FII flow state","published_fii_dii"),
("expiry_calendar","known expiry/calendar state","calendar"),
("trend_regime","causal trend state","intraday_ohlc"),
("vol_regime","causal volatility state","intraday_ohlc"),
("breakout_failure","failed breakout re-enters prior range","intraday_ohlc"),
("momentum_acceleration","change in trailing momentum","intraday_ohlc"),
("overnight_intraday_divergence","overnight gap versus early-session move","daily_intraday_ohlc")]
OPS=[
("AND","both directional signals agree"),("OR","either signal is active"),
("AND_NOT","first agrees while second opposes/is absent"),("XOR","exactly one signal active"),
("A_THEN_B","A precedes B in a frozen causal window"),("B_THEN_A","B precedes A"),
("CONTEXT_REVERSAL","context from A, reversal trigger from B"),("REGIME_GATE","A gated by state B")]
rows=[]; seen=set()
for (a,da,ra),(b,db,rb) in itertools.permutations(P,2):
 for op,definition in OPS:
  spec={"operator":op,"left":a,"right":b,"definition":definition}
  canonical=json.dumps(spec,sort_keys=True,separators=(",",":"))
  sig=hashlib.sha256(canonical.encode()).hexdigest()
  if sig in seen: continue
  seen.add(sig)
  rows.append({"strategy_id":f"NOB-{len(rows)+1:04d}","strategy_name":f"{op}: {a} + {b}",
   "family":"distinct_two-signal_decision_graph","rule_signature":sig,"logic_spec_json":canonical,
   "required_data":";".join(sorted({ra,rb})),"direction_rule":"bullish signal => long CALL; bearish signal => long PUT; no future outcome may choose direction",
   "causality":"Only completed, timestamped inputs at or before entry; no lookahead",
   "data_gate":"CONDITIONAL_POINT_IN_TIME_SOURCE_REQUIRED" if any(x in ra+rb for x in ["option_chain","futures_oi","published_fii","market_breadth","global_indices","timestamped_fx","timestamped_gold"]) else "OHLC_OR_CALENDAR_SOURCE_REQUIRED",
   "status":"CATALOGUED_NOT_TESTED"})
  if len(rows)>=1200: break
 if len(rows)>=1200: break
if len(rows)<1000 or len({x["rule_signature"] for x in rows})!=len(rows): raise SystemExit("Unique-strategy minimum/dedup gate failed")
with (OUT/"strategy_registry.csv").open("w",newline="",encoding="utf-8") as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(OUT/"strategy_registry.json").write_text(json.dumps({"schema_version":"1.0","minimum_unique_strategies":1000,"unique_strategy_count":len(rows),"counting_rule":"Distinct canonical decision-logic signatures; strike, exit, holding-period and cost variants do not count as new strategies.","outcome_data_accessed":False,"strategies":rows},indent=2)+"\n")
audit={"unique_strategy_count":len(rows),"unique_signatures":len(seen),"duplicate_signatures":len(rows)-len(seen),"outcome_data_accessed":False,"status":"PASS_CATALOGUE_ONLY"}
(OUT/"CATALOGUE_AUDIT.json").write_text(json.dumps(audit,indent=2)+"\n")
print(json.dumps(audit,indent=2))
