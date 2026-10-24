#!/usr/bin/env python3
"""Acquire/cache Dhan NIFTY 50 index OHLC for the ZigZag timeframe study.

Credentials are read only from DHAN_ACCESS_TOKEN. Raw licensed data is written to
an ephemeral workflow workspace and uploaded as a restricted-retention artifact;
never print credentials or commit raw market data to Git.
"""
from __future__ import annotations
import argparse, csv, datetime as dt, hashlib, json, os, pathlib, sys, time, urllib.error, urllib.request

BASE = "https://api.dhan.co/v2"
SECURITY_ID = "13"
SEGMENT = "IDX_I"
INSTRUMENT = "INDEX"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
ROOT = pathlib.Path("data/cache/zigzag_expiry_direction")
MANIFEST = pathlib.Path("reports/zigzag_data_manifest.json")

def api_post(path: str, payload: dict, token: str) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=body, method="POST", headers={
        "Accept": "application/json", "Content-Type": "application/json",
        "access-token": token, "User-Agent": "Naked-Options-v2-research/1.0",
    })
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
            if isinstance(data, dict) and data.get("status") == "failure":
                raise RuntimeError("Dhan API returned failure: " + str(data.get("remarks", "no details")))
            return data.get("data", data) if isinstance(data, dict) else {}
        except urllib.error.HTTPError as exc:
            # Do not print request headers or any credential material.
            detail = exc.read(500).decode("utf-8", "replace")
            if exc.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(2 ** attempt); continue
            raise RuntimeError(f"Dhan HTTP {exc.code}: {detail}") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < 4:
                time.sleep(2 ** attempt); continue
            raise RuntimeError(f"Dhan transport failure: {type(exc).__name__}") from None
    raise RuntimeError("Dhan retries exhausted")

def parse_timestamp(value):
    return dt.datetime.fromtimestamp(int(value), tz=dt.timezone.utc).astimezone(IST)

def get_rows(data: dict) -> list[dict]:
    keys = ("timestamp", "open", "high", "low", "close", "volume")
    if not all(k in data for k in keys[:5]):
        raise RuntimeError("Response missing one or more required OHLC/timestamp arrays")
    lengths = {k: len(data[k]) for k in keys if k in data}
    if len(set(lengths.values())) != 1:
        raise RuntimeError(f"Response arrays have mismatched lengths: {lengths}")
    rows=[]
    for i, epoch in enumerate(data["timestamp"]):
        stamp=parse_timestamp(epoch)
        rows.append({
            "timestamp_ist": stamp.isoformat(),
            "date_ist": stamp.date().isoformat(),
            "open": float(data["open"][i]), "high": float(data["high"][i]),
            "low": float(data["low"][i]), "close": float(data["close"][i]),
            "volume": int(data.get("volume", [0]*len(data["timestamp"]))[i] or 0),
        })
    return rows

def write_csv(path: pathlib.Path, rows: list[dict]) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows.sort(key=lambda x:x["timestamp_ist"])
    fields=["timestamp_ist","date_ist","open","high","low","close","volume"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    stamps=[r["timestamp_ist"] for r in rows]
    return {"path":str(path),"rows":len(rows),"sha256":digest,
            "first_timestamp_ist":stamps[0] if stamps else None,
            "last_timestamp_ist":stamps[-1] if stamps else None,
            "duplicate_timestamps":len(stamps)-len(set(stamps))}

def fetch_intraday(token: str, interval: int, start: dt.date, end: dt.date) -> list[dict]:
    rows=[]
    cursor=start
    while cursor <= end:
        stop=min(cursor+dt.timedelta(days=89), end)
        payload={"securityId":SECURITY_ID,"exchangeSegment":SEGMENT,"instrument":INSTRUMENT,
                 "interval":str(interval),"oi":False,
                 "fromDate":f"{cursor.isoformat()} 09:00:00",
                 "toDate":f"{stop.isoformat()} 16:00:00"}
        data=api_post("/charts/intraday", payload, token)
        part=get_rows(data)
        rows.extend(part)
        print(f"interval={interval} window={cursor}..{stop} rows={len(part)}", flush=True)
        cursor=stop+dt.timedelta(days=1)
        time.sleep(0.25)
    return rows

def fetch_daily(token: str, start: dt.date, end: dt.date) -> list[dict]:
    payload={"securityId":SECURITY_ID,"exchangeSegment":SEGMENT,"instrument":INSTRUMENT,
             "expiryCode":0,"oi":False,"fromDate":start.isoformat(),
             "toDate":(end+dt.timedelta(days=1)).isoformat()}
    return get_rows(api_post("/charts/historical",payload,token))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--start",default=(dt.date.today()-dt.timedelta(days=5*365)).isoformat())
    ap.add_argument("--end",default=dt.date.today().isoformat())
    ap.add_argument("--intervals",default="1,5,15,60",help="Dhan-supported intraday intervals")
    ap.add_argument("--refresh",action="store_true",help="Refetch even when a cached interval file exists")
    args=ap.parse_args()
    token=os.environ.get("DHAN_ACCESS_TOKEN")
    if not token:
        print("ERROR: DHAN_ACCESS_TOKEN secret is not configured; no data request made.",file=sys.stderr)
        return 2
    start=dt.date.fromisoformat(args.start); end=dt.date.fromisoformat(args.end)
    if start>end: ap.error("--start must be <= --end")
    intervals=[int(x.strip()) for x in args.intervals.split(",") if x.strip()]
    if any(x not in {1,5,15,25,60} for x in intervals):
        ap.error("Dhan intervals supported here are 1, 5, 15, 25 and 60")
    ROOT.mkdir(parents=True,exist_ok=True); MANIFEST.parent.mkdir(parents=True,exist_ok=True)
    manifest={"source":"DhanHQ v2 historical charts API","instrument":{"name":"NIFTY 50","security_id":SECURITY_ID,"segment":SEGMENT,"instrument":"INDEX"},
              "requested_start":start.isoformat(),"requested_end":end.isoformat(),"timezone":"Asia/Kolkata",
              "retrieved_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),"intraday_chunk_max_days":90,
              "intervals":{},"daily":None,"errors":[]}
    for interval in intervals:
        try:
            target=ROOT/f"nifty50_{interval}m.csv"
            if target.exists() and not args.refresh:
                raw=list(csv.DictReader(target.open(newline="",encoding="utf-8")))
                stamps=[row["timestamp_ist"] for row in raw]
                info={"path":str(target),"rows":len(raw),"sha256":hashlib.sha256(target.read_bytes()).hexdigest(),
                      "first_timestamp_ist":min(stamps) if stamps else None,
                      "last_timestamp_ist":max(stamps) if stamps else None,
                      "duplicate_timestamps":len(stamps)-len(set(stamps)),
                      "interval_minutes":interval,"reused_cache":True}
                manifest["intervals"][str(interval)]=info
                print(f"interval={interval} reusing cached file rows={len(raw)}",flush=True)
                continue
            rows=fetch_intraday(token,interval,start,end)
            info=write_csv(target,rows)
            info["interval_minutes"]=interval; info["reused_cache"]=False
            info["valid_ohlc_rows"]=sum(
                1 for r in rows if r["low"]<=min(r["open"],r["close"])<=max(r["open"],r["close"])<=r["high"])
            manifest["intervals"][str(interval)]=info
        except Exception as exc:
            manifest["errors"].append({"dataset":f"{interval}m","error":str(exc)})
            print(f"ERROR interval={interval}: {exc}",file=sys.stderr)
    try:
        daily_path=ROOT/"nifty50_daily.csv"
        if daily_path.exists() and not args.refresh:
            raw=list(csv.DictReader(daily_path.open(newline="",encoding="utf-8")))
            stamps=[row["timestamp_ist"] for row in raw]
            manifest["daily"]={"path":str(daily_path),"rows":len(raw),
                "sha256":hashlib.sha256(daily_path.read_bytes()).hexdigest(),
                "first_timestamp_ist":min(stamps) if stamps else None,
                "last_timestamp_ist":max(stamps) if stamps else None,
                "duplicate_timestamps":len(stamps)-len(set(stamps)),"reused_cache":True}
        else:
            daily=fetch_daily(token,start,end)
            manifest["daily"]=write_csv(daily_path,daily)
            manifest["daily"]["reused_cache"]=False
    except Exception as exc:
        manifest["errors"].append({"dataset":"daily","error":str(exc)})
        print(f"ERROR daily: {exc}",file=sys.stderr)
    MANIFEST.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps({"manifest":str(MANIFEST),"intervals":list(manifest["intervals"]),
                      "daily_rows":(manifest["daily"] or {}).get("rows",0),"errors":manifest["errors"]},indent=2))
    return 0 if manifest["intervals"] and manifest["daily"] and not manifest["errors"] else 1

if __name__=="__main__":
    raise SystemExit(main())
