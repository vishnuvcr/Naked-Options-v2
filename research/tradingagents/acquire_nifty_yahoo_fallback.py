"""Free-source fallback acquisition for NIFTY 50 when Dhan credentials are unavailable.

Yahoo Finance intraday retention is limited; this script records actual coverage and
never represents a short intraday sample as a five-year archive.
"""
from __future__ import annotations
import csv, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
import yfinance as yf

ROOT=Path("data/cache/zigzag_expiry_direction")
MANIFEST=Path("reports/zigzag_data_manifest.json")
FIELDS=["timestamp_ist","date_ist","open","high","low","close","volume"]

def save(interval, period, filename, source_interval):
    frame=yf.Ticker("^NSEI").history(period=period, interval=source_interval, auto_adjust=False, actions=False)
    if frame.empty:
        raise RuntimeError(f"Yahoo returned no rows for {interval} period={period}")
    frame=frame[~frame.index.duplicated(keep="first")].sort_index()
    rows=[]
    for ts,row in frame.iterrows():
        if ts.tzinfo is None:
            raise RuntimeError(f"Yahoo returned timezone-naive timestamp for {interval}")
        local=ts.tz_convert("Asia/Kolkata")
        rows.append({"timestamp_ist":local.isoformat(),"date_ist":local.date().isoformat(),
            "open":float(row["Open"]),"high":float(row["High"]),"low":float(row["Low"]),
            "close":float(row["Close"]),"volume":int(row.get("Volume",0) or 0)})
    path=ROOT/filename
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    return {"path":str(path),"rows":len(rows),"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "first_timestamp_ist":rows[0]["timestamp_ist"],"last_timestamp_ist":rows[-1]["timestamp_ist"],
        "requested_period":period,"interval":source_interval,"source":"Yahoo Finance ^NSEI"}

def main():
    ROOT.mkdir(parents=True,exist_ok=True);MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    results={}
    # Yahoo daily is long-history; intraday windows are deliberately limited.
    results["daily"]=save("daily","5y","nifty50_daily.csv","1d")
    for key,period,interval,filename in [
        ("1m","7d","1m","nifty50_1m.csv"),
        ("5m","60d","5m","nifty50_5m.csv"),
        ("15m","60d","15m","nifty50_15m.csv"),
        ("60m","730d","60m","nifty50_60m.csv"),
    ]:
        try: results[key]=save(key,period,filename,interval)
        except Exception as exc: results[key]={"status":"FAILED","error":type(exc).__name__,"message":str(exc)}
    manifest={"source":"Yahoo Finance public fallback","instrument":"NIFTY 50 (^NSEI)",
      "retrieved_at_utc":datetime.now(timezone.utc).isoformat(),
      "warning":"Yahoo intraday retention is limited; these files are not a substitute for five years of Dhan intraday history.",
      "datasets":results}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))
    if results["daily"].get("rows",0)==0: raise SystemExit("Daily fallback acquisition failed")
if __name__=="__main__": main()
