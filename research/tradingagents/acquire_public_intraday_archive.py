"""Acquire a public five-year NIFTY spot intraday archive and normalize it.

Source: public GitHub release indices-v1.0.0 from voletiramu/nse-fno-1min-data.
The release describes NIFTY spot 5-minute bars from Apr 2021 to Apr 2026.
This is an independent source requiring provenance/session/price cross-checks.
"""
from __future__ import annotations
import csv, hashlib, io, json, urllib.request, zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

URL="https://github.com/voletiramu/nse-fno-1min-data/releases/download/indices-v1.0.0/nifty_indices_5yr.zip"
ROOT=Path("data/cache/zigzag_expiry_direction")
# Source-specific output: never overwrite the Dhan or Yahoo source file.
OUT=ROOT/"nifty50_5m_public_archive.csv"
MANIFEST=Path("reports/public_intraday_sources.json")
IST=ZoneInfo("Asia/Kolkata")

def keymap(headers):
    normalized={h.strip().lower().replace(" ","").replace("_",""):h for h in headers}
    def choose(*names):
        for n in names:
            if n in normalized:return normalized[n]
        return None
    ts=choose("timestamp","datetime","date_time","time")
    date=choose("date","tradedate")
    time=choose("clocktime","timeist","bar_time")
    o=choose("open","o");h=choose("high","h");l=choose("low","l");c=choose("close","c")
    v=choose("volume","vol")
    if not all([o,h,l,c]) or not (ts or (date and time)):
        raise RuntimeError("Unknown public archive CSV schema; headers="+repr(headers))
    return ts,date,time,o,h,l,c,v

def parse_dt(value, date_value=None, time_value=None):
    raw=value if value else str(date_value)+" "+str(time_value)
    raw=raw.strip().replace("Z","+00:00")
    for fmt in ("%Y-%m-%d %H:%M:%S","%Y-%m-%d %H:%M","%d-%m-%Y %H:%M:%S","%d-%m-%Y %H:%M","%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M"):
        try:return datetime.strptime(raw,fmt).replace(tzinfo=IST)
        except ValueError:pass
    d=datetime.fromisoformat(raw)
    return d.replace(tzinfo=IST) if d.tzinfo is None else d.astimezone(IST)

def main():
    req=urllib.request.Request(URL,headers={"User-Agent":"Naked-Options-v2-research/1.0"})
    with urllib.request.urlopen(req,timeout=120) as r: blob=r.read()
    ziphash=hashlib.sha256(blob).hexdigest()
    z=zipfile.ZipFile(io.BytesIO(blob))
    names=[n for n in z.namelist() if n.lower().endswith(".csv") and "5min_5yr" in n.lower()]
    if not names: raise RuntimeError("Expected five-year 5-minute NIFTY CSV missing from release ZIP")
    raw=z.read(names[0]).decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(raw))
    mapping=keymap(reader.fieldnames or [])
    rows=[]
    for row in reader:
        stamp=parse_dt(row.get(mapping[0]) if mapping[0] else None,
                       row.get(mapping[1]) if mapping[1] else None,
                       row.get(mapping[2]) if mapping[2] else None)
        vals={k:float(row[col]) for k,col in zip(("open","high","low","close"),mapping[3:7])}
        if not (vals["low"]<=min(vals["open"],vals["close"])<=max(vals["open"],vals["close"])<=vals["high"]):
            raise RuntimeError("Invalid OHLC encountered; archive retained only in workflow memory, not accepted")
        rows.append({"timestamp_ist":stamp.isoformat(),"date_ist":stamp.date().isoformat(),
          **vals,"volume":int(float(row[mapping[7]] or 0)) if mapping[7] else 0})
    rows.sort(key=lambda r:r["timestamp_ist"])
    if len(rows)<50000: raise RuntimeError(f"Unexpectedly few rows in five-year archive: {len(rows)}")
    ROOT.mkdir(parents=True,exist_ok=True);MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    fields=["timestamp_ist","date_ist","open","high","low","close","volume"]
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    filehash=hashlib.sha256(OUT.read_bytes()).hexdigest()
    result={"source_url":URL,"release":"indices-v1.0.0","archive_sha256":ziphash,
      "source_csv":names[0],"normalized_path":str(OUT),"normalized_sha256":filehash,
      "rows":len(rows),"first_timestamp_ist":rows[0]["timestamp_ist"],
      "last_timestamp_ist":rows[-1]["timestamp_ist"],
      "source_description":"Zerodha Kite-derived NIFTY 50 spot index 5-minute OHLC; public third-party release",
      "limitations":["third-party provenance not independently verified","official session calendar not yet reconciled","bar-start semantics described by publisher but not independently certified","spot index volume is not meaningful"]}
    MANIFEST.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
