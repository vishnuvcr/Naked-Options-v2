#!/usr/bin/env python3
"""Bounded public NSE F&O bhavcopy feasibility check; stores data and sanitized manifest."""
from __future__ import annotations
import csv, hashlib, io, json, time, zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports/quant_evolve_nob_v2/nse_bhavcopy_feasibility.json"
CACHE = ROOT / "data/cache/nse_fno_bhavcopy_probe"
BASES = [
    "https://archives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{date}_F_0000.csv.zip",
    "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{date}_F_0000.csv.zip",
]
HEADERS = {"User-Agent":"Mozilla/5.0 research feasibility check", "Accept":"*/*", "Referer":"https://www.nseindia.com/all-reports-derivatives"}
def sha256(data): return hashlib.sha256(data).hexdigest()
def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    sess=requests.Session(); sess.headers.update(HEADERS)
    # Last 10 calendar dates, bounded to at most 3 successful archive samples.
    candidates=[]
    d=date.today()-timedelta(days=1)
    while len(candidates)<10:
        if d.weekday()<5: candidates.append(d)
        d-=timedelta(days=1)
    records=[]; successes=0
    for day in candidates:
        stamp=day.strftime("%Y%m%d"); rec={"trade_date_candidate":day.isoformat(),"status":"NOT_FOUND"}
        for base in BASES:
            url=base.format(date=stamp)
            try:
                resp=sess.get(url,timeout=20)
                if resp.status_code!=200 or len(resp.content)<100 or not resp.content[:2]==b"PK":
                    rec["last_http_status"]=resp.status_code
                    continue
                blob=resp.content
                with zipfile.ZipFile(io.BytesIO(blob)) as zf:
                    names=[n for n in zf.namelist() if n.lower().endswith(".csv")]
                    if not names: raise ValueError("ZIP has no CSV")
                    raw=zf.read(names[0])
                text=raw.decode("utf-8-sig",errors="replace")
                reader=csv.DictReader(io.StringIO(text))
                columns=reader.fieldnames or []
                sample=[]
                for row in reader:
                    # Preserve only small sanitized NIFTY rows; no whole market data printed in logs.
                    row_norm={str(k or "").strip().upper():v for k,v in row.items()}
                    symbol=str(row_norm.get("TCKRSYMB",row_norm.get("SYMBOL",""))).strip().upper()
                    inst=str(row_norm.get("FININSTRMTP",row_norm.get("INSTRUMENT",""))).strip().upper()
                    if "NIFTY" in symbol and ("OPT" in inst or any(k in row_norm for k in ("OPTNTP","OPTIONTYPE"))):
                        sample.append(row_norm)
                cache_file=CACHE/f"BhavCopy_NSE_FO_0_0_0_{stamp}_F_0000.csv.zip"
                cache_file.write_bytes(blob)
                required_groups={
                  "symbol":("TCKRSYMB","SYMBOL"),
                  "trade_date":("TRADDT","TRADDT","TRADEDATE","TIMESTAMP"),
                  "expiry":("XPRYDT","EXPIRYDT","EXPIRYDATE"),
                  "strike":("STRKPRIC","STRIKEPRICE"),
                  "option_type":("OPTNTP","OPTIONTYPE"),
                  "open":("OPNPRIC","OPENPRICE","OPEN"),
                  "high":("HGHPRIC","HIGHPRICE","HIGH"),
                  "low":("LWPRIC","LOWPRICE","LOW"),
                  "close":("CLSPRIC","CLOSEPRICE","CLOSE"),
                  "volume":("TTLTRADGVOL","TOTTRDQTY","CONTRACTS","VOLUME"),
                  "open_interest":("OPNINTRST","OPENINT","OPENINTEREST"),
                }
                normalized={c.strip().upper() for c in columns}
                mapping={name:next((k for k in keys if k in normalized),None) for name,keys in required_groups.items()}
                rec.update({"status":"PASS","url":url,"http_status":resp.status_code,"zip_bytes":len(blob),
                    "zip_sha256":sha256(blob),"csv_name":names[0],"csv_rows":sum(1 for _ in io.StringIO(text))-1,
                    "column_names":columns,"column_mapping":mapping,"nifty_option_rows":len(sample),
                    "sample_nifty_rows":sample[:2],"cache_file":str(cache_file.relative_to(ROOT)),
                    "required_fields_complete":all(mapping[k] for k in ("symbol","trade_date","expiry","strike","option_type","open","high","low","close","volume","open_interest"))})
                successes+=1
                break
            except Exception as exc:
                rec["error_type"]=type(exc).__name__
        records.append(rec)
        if successes>=3: break
        time.sleep(0.25)
    pass_schema=successes>=1 and any(r.get("required_fields_complete") and r.get("nifty_option_rows",0)>0 for r in records)
    report={"research_id":"QE-NOB-3.0","source":"Official NSE F&O UDiFF bhavcopy archive","audited_at_utc":datetime.now(timezone.utc).isoformat(),
      "decision":"SCHEMA_SAMPLE_PASS_DAILY_ONLY" if pass_schema else "BLOCKED_NSE_ARCHIVE_OR_SCHEMA",
      "sampled_dates":records,"successful_archives":successes,
      "limitations":["Daily bhavcopy is not intraday data and has no historical bid/ask/depth.","A passing schema check does not by itself establish complete history, all expiries, corporate-action/contract transitions, or executable fills.","Only up to three daily archives are retained in this probe cache."],
      "next_action":"If schema sample passes, run a separate bounded coverage audit and test mapping against Dhan rolling option history; do not use daily bars as intraday fills."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({"decision":report["decision"],"successful_archives":successes,
      "dates":[{"date":r["trade_date_candidate"],"status":r["status"],"rows":r.get("csv_rows"),"nifty_option_rows":r.get("nifty_option_rows"),"required_fields_complete":r.get("required_fields_complete")} for r in records]},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
