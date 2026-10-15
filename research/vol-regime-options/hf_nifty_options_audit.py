#!/usr/bin/env python3
import hashlib, json, os
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/cache/hf_nifty_options/options/NIFTY"
OUT=ROOT/"reports/vol_regime_options/hf_nifty_options_audit.json"
REQ=["timestamp","open","high","low","close","volume","open_interest","trading_day","symbol","strike","option_type","expiry"]
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def main():
 OUT.parent.mkdir(parents=True,exist_ok=True)
 files=sorted(DATA.glob("*.parquet"))
 r={"study":"VOL-REGIME-OPT-1.0","phase":"C1-free-HF-source-audit","checked_at_utc":datetime.now(timezone.utc).isoformat(),"dataset":"thetrademarkk/india-index-options-1m","license":"CC-BY-NC-4.0","license_gate":"NONCOMMERCIAL RESEARCH ONLY; attribution required; no commercial redistribution","files_found":len(files),"file_records":[],"errors":[],"raw_data_policy":"Raw parquet remains in Actions cache; only aggregate metadata and hashes are committed."}
 if not files:
  r.update(status="BLOCKED_NO_NIFTY_OPTION_FILES",decision="No P&L permitted.")
  OUT.write_text(json.dumps(r,indent=2)); print(json.dumps(r,indent=2)); raise SystemExit(2)
 rows=0; dates=set(); expiries=set(); types=set(); strikes=set(); miss={c:0 for c in REQ}; badprice=badorder=mismatch=duprows=conflicts=0; tmin=tmax=None
 for p in files:
  try:
   d=pd.read_parquet(p); rec={"file":p.name,"sha256":sha(p),"rows":len(d),"columns":list(d.columns)}
   missing=[c for c in REQ if c not in d.columns]
   if missing:
    rec.update(status="SCHEMA_FAIL",missing_columns=missing); r["file_records"].append(rec); continue
   rows+=len(d)
   ts=pd.to_datetime(d.timestamp,errors="coerce")
   if getattr(ts.dt,"tz",None) is not None: ts=ts.dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
   ex=pd.to_datetime(d.expiry,errors="coerce").dt.normalize()
   td=pd.to_datetime(d.trading_day,errors="coerce").dt.normalize()
   st=pd.to_numeric(d.strike,errors="coerce")
   px=d[["open","high","low","close"]].apply(pd.to_numeric,errors="coerce")
   for c in REQ: miss[c]+=int(d[c].isna().sum())
   badprice+=int((px.isna().any(axis=1)|px.le(0).any(axis=1)).sum())
   badorder+=int(((px.high<px[["open","close","low"]].max(axis=1))|(px.low>px[["open","close","high"]].min(axis=1))).sum())
   expfile=pd.to_datetime(p.stem,errors="coerce")
   mm=ex.notna() & pd.notna(expfile) & (ex!=expfile); mismatch+=int(mm.sum())
   key=pd.DataFrame({"ts":ts,"ex":ex,"strike":st,"type":d.option_type.astype(str).str.upper()})
   dup=key.duplicated(["ts","ex","strike","type"],keep=False); duprows+=int(dup.sum())
   if dup.any():
    tmp=d.loc[dup,["open","high","low","close","volume","open_interest"]].copy()
    tmp["_ts"]=ts[dup].astype(str); tmp["_ex"]=ex[dup].astype(str); tmp["_st"]=st[dup]; tmp["_type"]=d.loc[dup,"option_type"].astype(str).str.upper()
    for _,g in tmp.groupby(["_ts","_ex","_st","_type"],dropna=False):
     if len(g[["open","high","low","close","volume","open_interest"]].drop_duplicates())>1: conflicts+=1
   vv=ts.dropna()
   if len(vv):
    lo=str(vv.min()); hi=str(vv.max()); tmin=min(tmin,lo) if tmin else lo; tmax=max(tmax,hi) if tmax else hi
   dates.update(td.dropna().dt.strftime("%Y-%m-%d").unique().tolist()); expiries.update(ex.dropna().dt.strftime("%Y-%m-%d").unique().tolist())
   types.update(d.option_type.dropna().astype(str).str.upper().unique().tolist()); strikes.update(str(x) for x in st.dropna().unique())
   rec.update(status="PASS_SCHEMA",timestamp_min=lo if len(vv) else None,timestamp_max=hi if len(vv) else None,expiry_values=sorted(ex.dropna().dt.strftime("%Y-%m-%d").unique().tolist()),filename_expiry_mismatch_rows=int(mm.sum()))
   r["file_records"].append(rec)
  except Exception as e: r["errors"].append({"file":p.name,"error":type(e).__name__+": "+str(e)[:250]})
 r.update(total_rows=rows,timestamp_min=tmin,timestamp_max=tmax,trading_days=len(dates),expiry_count=len(expiries),expiry_min=min(expiries) if expiries else None,expiry_max=max(expiries) if expiries else None,option_types=sorted(types),unique_strikes=len(strikes),missing_by_column=miss,nonpositive_or_missing_ohlc_rows=badprice,invalid_ohlc_order_rows=badorder,duplicate_key_rows=duprows,conflicting_duplicate_groups=conflicts,filename_expiry_mismatch_rows=mismatch,valid_files=sum(x.get("status")=="PASS_SCHEMA" for x in r["file_records"]),failed_files=sum(x.get("status")!="PASS_SCHEMA" for x in r["file_records"])+len(r["errors"]))
 r["status"]="PARTIAL_SOURCE_AUDIT" if r["errors"] or r["failed_files"] else ("SCHEMA_AND_EXPIRY_FIELD_PASS_REQUIRES_COVERAGE_RECONCILIATION" if rows and mismatch==0 and badprice==0 and badorder==0 else "SOURCE_AUDIT_WITH_DATA_QUALITY_FLAGS")
 r["decision"]="Exact expiry/strike/type fields can support follow-up identity checks. OHLC bars are not bid/ask quotes; reconcile coverage and sample records against official NSE evidence before P&L."
 OUT.write_text(json.dumps(r,indent=2)); print(json.dumps({k:v for k,v in r.items() if k!="file_records"},indent=2))
 if r["status"]=="PARTIAL_SOURCE_AUDIT": raise SystemExit(2)
if __name__=="__main__": main()
