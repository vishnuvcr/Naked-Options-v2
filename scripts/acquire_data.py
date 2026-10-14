#!/usr/bin/env python3
"""Multi-source NIFTY daily history acquisition. Credentials are read only from env."""
import argparse, hashlib, json, os
from datetime import date, datetime, timezone
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache"
MANIFEST = ROOT / "reports" / "data_manifest.json"
EXT = {"^GSPC":"sp500", "^IXIC":"nasdaq", "^N225":"nikkei225", "^HSI":"hangseng",
       "^VIX":"cboe_vix", "^INDIAVIX":"india_vix", "INR=X":"usd_inr",
       "GC=F":"gold", "CL=F":"wti_crude", "^TNX":"us10y_yield"}

def now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def log_error(src, exc):
    p = ROOT / "research" / "ERROR_LOG.md"
    line = f"| {now()} | 3 | {src} | {type(exc).__name__}: {str(exc).replace('|','/').replace(chr(10),' ')[:250]} |\n"
    if not p.exists():
        p.write_text("# Error log\n\n| Time UTC | Phase | Source | Error |\n|---|---|---|---|\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write(line)

def normalise(frame, source):
    frame = frame.copy()
    if isinstance(frame.columns, pd.MultiIndex):
        frame.columns = frame.columns.get_level_values(0)
    colmap = {str(c).strip().lower().replace(" ","_"): c for c in frame.columns}
    datecol = next((colmap[x] for x in ("date","datetime","eod_timestamp","ch_timestamp","timestamp") if x in colmap), None)
    if datecol is None:
        raise ValueError(f"no date field in schema {list(frame.columns)[:15]}")
    out = pd.DataFrame()
    out["date"] = pd.to_datetime(frame[datecol], errors="coerce", utc=True).dt.tz_convert("Asia/Kolkata").dt.date.astype(str)
    for target, aliases in {
        "open":("open","eod_open_index_val"), "high":("high","eod_high_index_val"),
        "low":("low","eod_low_index_val"), "close":("close","adj_close","eod_close_index_val"),
        "volume":("volume","shares_traded","eod_tot_traded_qty","total_traded_qty")
    }.items():
        c = next((colmap[a] for a in aliases if a in colmap), None)
        out[target] = pd.to_numeric(frame[c], errors="coerce") if c is not None else float("nan")
    out["source_id"] = source
    out = out.dropna(subset=["date","open","high","low","close"]).sort_values("date")
    if out.empty:
        raise ValueError("source returned no valid OHLC rows")
    # Preserve weekend-dated rows: NSE can schedule special sessions. The validator
    # reports these dates as a warning instead of silently removing them.
    if out.date.duplicated().any():
        raise ValueError("duplicate session dates")
    if (out[["open","high","low","close"]] <= 0).any().any():
        raise ValueError("non-positive OHLC")
    bad = (out.high < out[["open","close","low"]].max(axis=1)) | (out.low > out[["open","close","high"]].min(axis=1))
    if bad.any():
        raise ValueError(f"invalid OHLC range in {int(bad.sum())} rows")
    return out[["date","open","high","low","close","volume","source_id"]].reset_index(drop=True)

def get_dhan(start, end):
    token = os.getenv("DHAN_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("DHAN_ACCESS_TOKEN is not configured")
    payload = {"securityId":os.getenv("DHAN_NIFTY_SECURITY_ID","13"),
       "exchangeSegment":os.getenv("DHAN_NIFTY_EXCHANGE_SEGMENT","IDX_I"),
       "instrument":os.getenv("DHAN_NIFTY_INSTRUMENT","INDEX"), "expiryCode":0, "oi":False,
       "fromDate":start,"toDate":end}
    r = requests.post("https://api.dhan.co/v2/charts/historical",
       headers={"Content-Type":"application/json","access-token":token}, json=payload, timeout=40)
    if not r.ok or "json" not in r.headers.get("content-type","").lower():
        raise RuntimeError(f"Dhan HTTP/content-type failure: {r.status_code}/{r.headers.get('content-type','unknown')}")
    obj = r.json()
    if not isinstance(obj,dict) or not all(k in obj for k in ("timestamp","open","high","low","close")):
        raise ValueError("Dhan response has an unrecognized schema; payload not logged")
    n = len(obj["timestamp"])
    if any(len(obj[k]) != n for k in ("open","high","low","close")):
        raise ValueError("Dhan arrays have unequal lengths")
    d = pd.to_datetime(obj["timestamp"], unit="s", utc=True).tz_convert("Asia/Kolkata").date
    return normalise(pd.DataFrame({"date":d,"open":obj["open"],"high":obj["high"],"low":obj["low"],
       "close":obj["close"],"volume":obj.get("volume",[None]*n)}), "dhan_daily")

def get_nse(start, end):
    s = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
       "Accept":"application/json,text/plain,*/*","Referer":"https://www.nseindia.com/reports-indices-historical-index-data"}
    s.get("https://www.nseindia.com/",headers=headers,timeout=25)
    r = s.get("https://www.nseindia.com/api/historicalOR/indicesHistory",
       params={"indexType":"NIFTY 50","from":pd.to_datetime(start).strftime("%d-%m-%Y"),
               "to":pd.to_datetime(end).strftime("%d-%m-%Y")},headers=headers,timeout=40)
    if not r.ok or "json" not in r.headers.get("content-type","").lower():
        raise RuntimeError(f"NSE HTTP/content-type failure: {r.status_code}/{r.headers.get('content-type','unknown')}")
    obj = r.json()
    rows = obj if isinstance(obj,list) else next((obj[k] for k in ("data","indexCloseOnlineRecords","historicalData","records") if isinstance(obj.get(k),list)),[])
    if not rows:
        raise ValueError("NSE response contains no recognized data rows")
    # Keep original keys; normalise() recognizes official NSE field names.
    return normalise(pd.DataFrame(rows), "nse_official")

def get_yahoo(ticker, start, end, src):
    import yfinance as yf
    frame = yf.download(ticker,start=start,end=end,auto_adjust=False,progress=False,threads=False)
    if frame.empty:
        raise ValueError(f"Yahoo returned no rows for {ticker}")
    frame = frame.reset_index()
    return normalise(frame,src)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start",default="2007-01-01")
    p.add_argument("--end",default=date.today().isoformat())
    p.add_argument("--external",action="store_true")
    a = p.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True); (ROOT/"reports").mkdir(parents=True,exist_ok=True)
    manifest={"research_version":"NIFTY-PRED-1.0","retrieved_at_utc":now(),"requested_start":a.start,
      "requested_end":a.end,"sources":[],"notes":["Raw data are cached at runtime; inspect source license before redistribution.",
      "Credentials are never included in the manifest."]}
    good=[]
    for name, fn in [("dhan_daily",lambda:get_dhan(a.start,a.end)),
                     ("nse_official",lambda:get_nse(a.start,a.end)),
                     ("yahoo_nifty",lambda:get_yahoo("^NSEI",a.start,a.end,"yahoo_nifty"))]:
        rec={"source_id":name,"attempted_at_utc":now()}
        try:
            df=fn(); rec.update({"status":"PASS","rows":len(df),"first_date":df.date.min(),"last_date":df.date.max(),
              "missing_volume":int(df.volume.isna().sum()),"weekend_rows_observed":int((pd.to_datetime(df.date,errors="coerce").dt.dayofweek>=5).sum()),"csv_sha256":hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()})
            good.append((name,df))
        except Exception as e:
            rec.update({"status":"FAIL","error_type":type(e).__name__,"error_summary":str(e)[:250]})
            log_error(name,e)
        manifest["sources"].append(rec)
    if good:
        priority={"dhan_daily":0,"nse_official":1,"yahoo_nifty":2}
        selected_name,selected=sorted(good,key=lambda x:priority[x[0]])[0]
        checks=[]
        for other_name,other in good:
            if other_name==selected_name: continue
            z=selected[["date","close"]].merge(other[["date","close"]],on="date",suffixes=("_primary","_secondary"))
            dif=(z.close_primary-z.close_secondary).abs()
            checks.append({"source_id":other_name,"overlap_rows":len(z),
              "median_abs_close_difference":float(dif.median()) if len(z) else None,
              "max_abs_close_difference":float(dif.max()) if len(z) else None})
        manifest["cross_source_checks"]=checks
        out=CACHE/"nifty50_daily.csv"; selected.to_csv(out,index=False)
        manifest.update({"status":"DATA_ACQUIRED","selected_target_source":selected_name,"target_file":str(out.relative_to(ROOT)),
          "target_rows":len(selected),"target_first_date":selected.date.min(),"target_last_date":selected.date.max(),"target_sha256":digest(out)})
    else:
        manifest.update({"status":"BLOCKED_NO_VALID_TARGET","selected_target_source":None,"target_rows":0})
    if a.external:
        manifest["external_sources"]=[]
        for ticker,label in EXT.items():
            rec={"ticker":ticker,"label":label,"attempted_at_utc":now()}
            try:
                df=get_yahoo(ticker,a.start,a.end,"yahoo:"+ticker)
                path=CACHE/"external"/(ticker.replace("^","").replace("=","_")+".csv")
                path.parent.mkdir(parents=True,exist_ok=True); df.to_csv(path,index=False)
                rec.update({"status":"PASS","rows":len(df),"first_date":df.date.min(),"last_date":df.date.max(),"sha256":digest(path),"file":str(path.relative_to(ROOT))})
            except Exception as e:
                rec.update({"status":"FAIL","error_type":type(e).__name__,"error_summary":str(e)[:200]})
                log_error("yahoo:"+ticker,e)
            manifest["external_sources"].append(rec)
    MANIFEST.write_text(json.dumps(manifest,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({k:manifest.get(k) for k in ("status","selected_target_source","target_rows","target_first_date","target_last_date")},indent=2))
    return 0 if good else 2

if __name__ == "__main__":
    raise SystemExit(main())
