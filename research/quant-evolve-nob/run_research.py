#!/usr/bin/env python3
"""Fresh QuantEvolve-style NIFTY long-option strategy study (QE-NOB-1.0).

The script writes sanitized reports only. Raw licensed Dhan responses remain in a
separate runtime cache and are never committed or uploaded as artifacts.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "quant_evolve_nob_v1"
OPT_CACHE = CACHE / "options_rolling"
IDX_CACHE = CACHE / "underlying_intraday"
OUT = ROOT / "reports" / "quant_evolve_nob_v1"
SEED = 20261022
SEBI_RATE = 0.000001
STAMP_RATE = 0.00003
GST_RATE = 0.18
CONFIG_PATH = ROOT / "research" / "quant-evolve-nob" / "config.json"
TIME_ZONE = "Asia/Kolkata"

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ensure_dirs():
    for p in (OPT_CACHE, IDX_CACHE, OUT):
        p.mkdir(parents=True, exist_ok=True)

def safe_detail(response, token=""):
    try:
        body = json.dumps(response.json(), ensure_ascii=True)
    except Exception:
        body = str(getattr(response, "text", ""))
    if token:
        body = body.replace(token, "[REDACTED]")
    return body.replace("\n", " ")[:240]

def chunks(start, end_exclusive, days):
    current = start
    while current < end_exclusive:
        nxt = min(current + timedelta(days=days), end_exclusive)
        yield current, nxt
        current = nxt

def series_part(payload, side):
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise ValueError("data is not an object")
    part = data.get("ce" if side == "CALL" else "pe")
    if part is None:
        return None
    if not isinstance(part, dict) or "timestamp" not in part:
        raise ValueError("option series schema invalid")
    n = len(part["timestamp"])
    for key in ("open", "high", "low", "close", "strike", "spot"):
        if key not in part or len(part[key]) != n:
            raise ValueError("option array missing or length mismatch: " + key)
    return part

def validate_option_payload(payload, side):
    part = series_part(payload, side)
    if part is None or len(part.get("timestamp", [])) == 0:
        return "EMPTY"
    for key in ("open", "high", "low", "close", "strike", "spot"):
        arr = pd.to_numeric(pd.Series(part[key]), errors="coerce")
        if arr.isna().all():
            raise ValueError("no numeric values in " + key)
    return "PASS"

def api_post(endpoint, body, token, timeout=50):
    response = requests.post("https://api.dhan.co/v2/" + endpoint,
        headers={"Accept":"application/json", "Content-Type":"application/json", "access-token":token},
        json=body, timeout=timeout)
    if response.status_code in (401, 403):
        raise PermissionError("Dhan auth HTTP " + str(response.status_code) + ": " + safe_detail(response, token))
    if not response.ok or "json" not in response.headers.get("content-type", "").lower():
        raise RuntimeError("Dhan HTTP/content-type " + str(response.status_code) + ": " + safe_detail(response, token))
    return response.json()

def option_request_body(expiry_flag, expiry_code, offset, side, start, end):
    label = "ATM" if offset == 0 else ("ATM+" + str(offset) if offset > 0 else "ATM" + str(offset))
    return {"exchangeSegment":"NSE_FNO", "interval":"5", "securityId":13,
        "instrument":"OPTIDX", "expiryFlag":expiry_flag, "expiryCode":expiry_code,
        "strike":label, "drvOptionType":side,
        "requiredData":["open","high","low","close","iv","volume","strike","oi","spot"],
        "fromDate":start.isoformat(), "toDate":end.isoformat()}

def probe_sources(token):
    """Small schema/credential probe; never inferred from prior report/cache."""
    end = date.today()
    start = end - timedelta(days=14)
    report = {"research_id":"QE-NOB-1.0", "probed_at_utc":utc_now(),
              "fresh_cache_namespace":str(CACHE.relative_to(ROOT)), "sources":[], "supported_expiries":[]}
    if not token:
        report["status"] = "BLOCKED_NO_DHAN_ACCESS_TOKEN"
        report["notes"] = ["No token was present in the action environment; credentials were not logged."]
        return report
    for flag, code in (("WEEK",1), ("WEEK",2), ("MONTH",1)):
        record = {"source":"Dhan rolling expired options", "expiry_flag":flag, "expiry_code":code}
        try:
            body = option_request_body(flag, code, 0, "CALL", start, end)
            payload = api_post("charts/rollingoption", body, token)
            state = validate_option_payload(payload, "CALL")
            part = series_part(payload, "CALL")
            record.update({"status":state, "rows":0 if part is None else len(part.get("timestamp",[]))})
            cache_path = OPT_CACHE / ("probe_" + flag.lower() + str(code) + ".json")
            cache_path.write_text(json.dumps(payload, separators=(",",":")), encoding="utf-8")
            if state == "PASS" and record["rows"] > 0:
                record["supported"] = True
                if (flag,code) in (("WEEK",1),("MONTH",1)):
                    report["supported_expiries"].append({"flag":flag,"code":code})
            else:
                record["supported"] = False
        except Exception as exc:
            record.update({"status":"FAIL","error_type":type(exc).__name__,"error_summary":str(exc)[:200]})
        report["sources"].append(record)
        time.sleep(0.2)
    body = {"securityId":"13", "exchangeSegment":"IDX_I", "instrument":"INDEX",
            "interval":"5", "oi":False, "fromDate":start.strftime("%Y-%m-%d 09:15:00"),
            "toDate":end.strftime("%Y-%m-%d 15:30:00")}
    try:
        payload = api_post("charts/intraday", body, token)
        n = len(payload.get("timestamp", []))
        if n and all(len(payload.get(k, [])) == n for k in ("open","high","low","close")):
            report["underlying_probe"] = {"status":"PASS","rows":n}
            cache_path = IDX_CACHE / "probe_underlying.json"
            cache_path.write_text(json.dumps(payload, separators=(",",":")), encoding="utf-8")
        else:
            report["underlying_probe"] = {"status":"FAIL","error_summary":"OHLC/timestamp lengths invalid"}
    except Exception as exc:
        report["underlying_probe"] = {"status":"FAIL","error_type":type(exc).__name__,"error_summary":str(exc)[:200]}
    report["status"] = "PASS" if report["supported_expiries"] and report.get("underlying_probe",{}).get("status") == "PASS" else "BLOCKED_SOURCE_PROBE"
    return report

def retrieve_options(token, supported, refresh=False):
    end = date.today()
    start = max(date(2021,10,22), end - timedelta(days=365*5))
    reqs, failures = [], []
    pairs = [(offset, side) for offset in range(-3,4) for side in ("CALL","PUT")]
    planned = 0
    for expiry in supported:
        flag, code = expiry["flag"], int(expiry["code"])
        for d0,d1 in chunks(start,end,30):
            for offset,side in pairs:
                planned += 1
                name = f"{flag.lower()}{code}_{d0:%Y%m%d}_{d1:%Y%m%d}_{offset:+d}_{side.lower()}.json"
                path = OPT_CACHE / name
                if path.exists() and not refresh:
                    try:
                        payload = json.loads(path.read_text(encoding="utf-8"))
                        state = validate_option_payload(payload,side)
                        reqs.append({"expiry_flag":flag,"expiry_code":code,"from":d0.isoformat(),"to_exclusive":d1.isoformat(),
                                     "offset":offset,"side":side,"status":"CACHED_"+state,"path":str(path.relative_to(ROOT))})
                        continue
                    except Exception:
                        pass
                body = option_request_body(flag,code,offset,side,d0,d1-timedelta(days=1))
                error = None
                for attempt in range(3):
                    try:
                        payload = api_post("charts/rollingoption",body,token)
                        state = validate_option_payload(payload,side)
                        path.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8")
                        reqs.append({"expiry_flag":flag,"expiry_code":code,"from":d0.isoformat(),"to_exclusive":d1.isoformat(),
                                     "offset":offset,"side":side,"status":state,"path":str(path.relative_to(ROOT))})
                        error = None
                        break
                    except PermissionError as exc:
                        error = str(exc)
                        failures.append({"expiry_flag":flag,"expiry_code":code,"from":d0.isoformat(),"offset":offset,"side":side,"error":error})
                        return {"status":"BLOCKED_AUTH","requests_planned":planned,"requests":reqs,"failures":failures}
                    except Exception as exc:
                        error = type(exc).__name__ + ": " + str(exc)[:180]
                        if attempt < 2:
                            time.sleep(2**attempt)
                if error:
                    failures.append({"expiry_flag":flag,"expiry_code":code,"from":d0.isoformat(),"offset":offset,"side":side,"error":error})
                time.sleep(0.15)
    return {"status":"PASS" if reqs and not failures else ("PARTIAL" if reqs else "BLOCKED_NO_OPTION_DATA"),
            "range_start":start.isoformat(),"range_end_exclusive":end.isoformat(),
            "requests_planned":planned,"requests_recorded":len(reqs),"failures_count":len(failures),
            "request_status_counts":pd.Series([x["status"] for x in reqs]).value_counts().to_dict(),
            "requests":reqs,"failures":failures}

def retrieve_underlying(token, refresh=False):
    end = date.today()
    start = max(date(2021,10,22), end - timedelta(days=365*5))
    records, failures = [], []
    for d0,d1 in chunks(start,end,80):
        name = f"nifty_5m_{d0:%Y%m%d}_{d1:%Y%m%d}.json"
        path = IDX_CACHE / name
        if path.exists() and not refresh:
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
                n = len(obj.get("timestamp",[]))
                if n and all(len(obj.get(k,[])) == n for k in ("open","high","low","close")):
                    records.append({"status":"CACHED","path":str(path.relative_to(ROOT)),"rows":n})
                    continue
            except Exception:
                pass
        body = {"securityId":"13","exchangeSegment":"IDX_I","instrument":"INDEX","interval":"5","oi":False,
                "fromDate":d0.strftime("%Y-%m-%d 09:15:00"),
                "toDate":(d1-timedelta(days=1)).strftime("%Y-%m-%d 15:30:00")}
        error = None
        for attempt in range(3):
            try:
                obj = api_post("charts/intraday",body,token,timeout=80)
                n = len(obj.get("timestamp",[]))
                if n == 0 or any(len(obj.get(k,[])) != n for k in ("open","high","low","close")):
                    raise ValueError("underlying intraday response schema invalid or empty")
                path.write_text(json.dumps(obj,separators=(",",":")),encoding="utf-8")
                records.append({"status":"PASS","path":str(path.relative_to(ROOT)),"rows":n})
                error = None
                break
            except PermissionError as exc:
                error = str(exc)
                failures.append({"from":d0.isoformat(),"error":error})
                return {"status":"BLOCKED_AUTH","requests":records,"failures":failures}
            except Exception as exc:
                error = type(exc).__name__ + ": " + str(exc)[:180]
                if attempt < 2:
                    time.sleep(2**attempt)
        if error:
            failures.append({"from":d0.isoformat(),"error":error})
        time.sleep(0.15)
    return {"status":"PASS" if records and not failures else ("PARTIAL" if records else "BLOCKED_NO_UNDERLYING"),
            "range_start":start.isoformat(),"range_end_exclusive":end.isoformat(),"requests":records,"failures":failures}

def payload_rows(payload, flag, code, offset, side):
    part = series_part(payload, side)
    if part is None:
        return []
    n = len(part["timestamp"]); out = []
    for i in range(n):
        try:
            ts = int(part["timestamp"][i])
            row = {"timestamp":ts,"expiry_flag":flag,"expiry_code":int(code),"offset":int(offset),"side":side}
            for name in ("open","high","low","close","iv","volume","strike","oi","spot"):
                vals = part.get(name)
                try: val = float(vals[i]) if vals is not None and vals[i] is not None else np.nan
                except (ValueError,TypeError,IndexError): val = np.nan
                row[name] = val if math.isfinite(val) else np.nan
            if row["open"] > 0 and row["close"] >= 0 and row["strike"] > 0 and row["spot"] > 0:
                out.append(row)
        except (ValueError,TypeError,IndexError):
            continue
    return out

def load_frames():
    bars=[]
    for path in sorted(IDX_CACHE.glob("nifty_5m_*.json")):
        try: obj=json.loads(path.read_text(encoding="utf-8"))
        except Exception: continue
        n=len(obj.get("timestamp",[]))
        if not n: continue
        for i,ts in enumerate(obj["timestamp"]):
            try:
                row={"timestamp":int(ts)}
                for k in ("open","high","low","close","volume"):
                    v=obj.get(k,[np.nan]*n)[i]
                    row[k]=float(v) if v is not None and math.isfinite(float(v)) else np.nan
                bars.append(row)
            except (ValueError,TypeError,IndexError):
                continue
    if not bars:
        return pd.DataFrame(),pd.DataFrame()
    u=pd.DataFrame(bars).drop_duplicates("timestamp").sort_values("timestamp")
    u["dt"]=pd.to_datetime(u.timestamp,unit="s",utc=True).dt.tz_convert(TIME_ZONE)
    u["date"]=u.dt.dt.date.astype(str); u["time"]=u.dt.dt.strftime("%H:%M")
    u=u[(u["time"] >= "09:15") & (u["time"] <= "15:25")].copy()
    valid=(u[["open","high","low","close"]]>0).all(axis=1) & (u.high>=u[["open","close","low"]].max(axis=1)) & (u.low<=u[["open","close","high"]].min(axis=1))
    u=u[valid].sort_values("timestamp").reset_index(drop=True)
    opts=[]
    for path in sorted(OPT_CACHE.glob("*_*.json")):
        if path.name.startswith("probe_"): continue
        # Filename: flag_code_YYYYMMDD_YYYYMMDD_offset_side.json
        parts=path.stem.split("_")
        if len(parts) != 5: continue
        try: flag=parts[0][:-1].upper(); code=int(parts[0][-1]); d0=parts[1]; d1=parts[2]; off=int(parts[3]); side=parts[4].upper()
        except Exception: continue
        if flag not in ("WEEK","MONTH") or side not in ("CALL","PUT"): continue
        try: obj=json.loads(path.read_text(encoding="utf-8"))
        except Exception: continue
        opts.extend(payload_rows(obj,flag,code,off,side))
    o=pd.DataFrame(opts)
    if not o.empty:
        o["dt"]=pd.to_datetime(o.timestamp,unit="s",utc=True).dt.tz_convert(TIME_ZONE)
        o["date"]=o.dt.dt.date.astype(str)
        o["strike_key"]=o.strike.round(2)
        # A key with conflicting prices is discarded rather than arbitrarily chosen.
        key=["expiry_flag","expiry_code","side","timestamp","strike_key"]
        dup=o.groupby(key).open.nunique(dropna=True)
        bad=set(dup[dup>1].index.tolist())
        if bad:
            idx=pd.MultiIndex.from_frame(o[key])
            o=o.loc[~idx.isin(bad)].copy()
        o=o.drop_duplicates(key,keep="first").reset_index(drop=True)
    return u,o

def lot_size_proxy(day):
    # Exploratory proxy only: no result is strategy-approved without expiry-level lot master.
    d=pd.Timestamp(day).date()
    if d < date(2024,11,20): return 25
    if d < date(2025,11,20): return 75
    return 65

def exchange_rate(day):
    # Conservative date-effective NSE option-premium fee estimates, including IPFT where applicable.
    # The pre-Oct-2024 schedule was monthly-turnover dependent; this uses conservative high-side rates.
    d=pd.Timestamp(day).date()
    if d < date(2023,4,1): return 0.000535
    if d < date(2024,4,1): return 0.000505
    if d < date(2024,10,1): return 0.000500
    # NSE 27-Sep-2024 true-to-label revision plus IPFT; 27-Feb-2026 revision retains approx total outflow.
    return 0.0003553

def cost_and_pnl(legs, day, slip_bps, brokerage):
    # Each leg is dict(entry, exit); one lot per leg; long-option transaction charges.
    lots=lot_size_proxy(day)
    gross=0.0; turnover=0.0; buy_turnover=0.0; sell_turnover=0.0
    for leg in legs:
        buy=leg["entry"]*(1+slip_bps/10000.0)
        sell=max(0.0,leg["exit"]*(1-slip_bps/10000.0))
        gross+=(sell-buy)*lots
        buy_turnover+=buy*lots; sell_turnover+=sell*lots
        turnover+=buy*lots+sell*lots
    d=pd.Timestamp(day).date()
    stt_rate=0.000625 if d < date(2024,10,1) else (0.001 if d < date(2026,4,1) else 0.0015)
    brokerage_total=brokerage*2*len(legs)
    exchange_rate_value=exchange_rate(day)
    exchange=turnover*exchange_rate_value
    sebi=turnover*SEBI_RATE
    stamp=buy_turnover*STAMP_RATE
    stt=sell_turnover*stt_rate
    gst=GST_RATE*(brokerage_total+exchange+sebi)
    fees=brokerage_total+exchange+sebi+stamp+stt+gst
    return {"gross_pnl_rupees":gross,"net_pnl_rupees":gross-fees,"entry_debit_rupees":buy_turnover,
            "brokerage_rupees":brokerage_total,"exchange_fee_rupees":exchange,"sebi_fee_rupees":sebi,
            "stamp_rupees":stamp,"stt_rupees":stt,"gst_rupees":gst,"total_cost_rupees":fees,
            "lot_size_proxy":lots,"stt_rate":stt_rate,"exchange_rate":exchange_rate_value,"turnover_rupees":turnover}

def signal_events(frame, candidate):
    # Return one signal event per session; signal is evaluated using the just-closed bar.
    if frame.empty: return []
    fast, slow = candidate.get("fast",8), candidate.get("slow",21)
    bydate=[]
    prior_close=None
    for day,g in frame.groupby("date",sort=True):
        g=g.sort_values("timestamp").reset_index(drop=False)
        n=len(g)
        if n<8:
            prior_close=float(g.close.iloc[-1]); continue
        typ=(g.high+g.low+g.close)/3
        vol=g.volume.fillna(0).clip(lower=0)
        g["vwap"]=(typ*vol).cumsum()/vol.cumsum().replace(0,np.nan)
        g["ema_fast"]=g.close.ewm(span=fast,adjust=False).mean()
        g["ema_slow"]=g.close.ewm(span=slow,adjust=False).mean()
        sig=None
        family=candidate["family"]
        if family in ("orb","orb_straddle","orb_strangle"):
            nr=int(candidate["range_bars"])
            if n>nr+1:
                rh=float(g.high.iloc[:nr].max()); rl=float(g.low.iloc[:nr].min()); width=max(rh-rl,1.0)
                buff=float(candidate["buffer"])*width
                for i in range(nr,n-1):
                    close=float(g.close.iloc[i])
                    if close>rh+buff: sig=(i,1); break
                    if close<rl-buff: sig=(i,-1); break
        elif family=="trend":
            for i in range(1,n-1):
                up=g.ema_fast.iloc[i]>g.ema_slow.iloc[i] and g.ema_fast.iloc[i-1]<=g.ema_slow.iloc[i-1]
                dn=g.ema_fast.iloc[i]<g.ema_slow.iloc[i] and g.ema_fast.iloc[i-1]>=g.ema_slow.iloc[i-1]
                vwap_ok=True if not candidate.get("vwap_filter",True) else (g.close.iloc[i]>g.vwap.iloc[i] if up else g.close.iloc[i]<g.vwap.iloc[i])
                if up and vwap_ok: sig=(i,1); break
                if dn and vwap_ok: sig=(i,-1); break
        elif family in ("gap_cont","gap_fade"):
            if prior_close and prior_close>0:
                gap=float(g.open.iloc[0])/prior_close-1.0
                threshold=float(candidate["gap"])
                if abs(gap)>=threshold and n>4:
                    sign=1 if gap>0 else -1
                    if family=="gap_fade": sign=-sign
                    # The signal becomes actionable after three completed bars.
                    sig=(3,sign)
        elif family=="pullback":
            for i in range(3,n-1):
                uptrend=g.ema_fast.iloc[i]>g.ema_slow.iloc[i] and g.ema_fast.iloc[i-1]>g.ema_slow.iloc[i-1]
                downtrend=g.ema_fast.iloc[i]<g.ema_slow.iloc[i] and g.ema_fast.iloc[i-1]<g.ema_slow.iloc[i-1]
                if uptrend and g.close.iloc[i-1]<=g.vwap.iloc[i-1] and g.close.iloc[i]>g.vwap.iloc[i]:
                    sig=(i,1); break
                if downtrend and g.close.iloc[i-1]>=g.vwap.iloc[i-1] and g.close.iloc[i]<g.vwap.iloc[i]:
                    sig=(i,-1); break
        prior_close=float(g.close.iloc[-1])
        if sig:
            idx, direction=sig
            if idx+1<n:
                bydate.append({"date":day,"signal_idx":int(g["index"].iloc[idx]),"direction":int(direction),
                               "signal_timestamp":int(g.timestamp.iloc[idx]),"entry_timestamp":int(g.timestamp.iloc[idx+1]),
                               "entry_time":str(g.time.iloc[idx+1]),"day_index":int(idx)})
    return bydate

def candidates_for(expiry_flags):
    result=[]
    holds=(1,3,6,12,24)
    for fam in ("orb","orb_straddle","orb_strangle"):
        for nr in (1,3,6):
            for buf in (0.0,0.1,0.25):
                for hold in holds:
                    for ef in expiry_flags:
                        for money in ((0,1) if fam=="orb" else (0,)):
                            result.append({"family":fam,"range_bars":nr,"buffer":buf,"hold":hold,"expiry":ef,"money":money})
    for fast,slow in ((5,13),(8,21),(9,34)):
        for vwap in (True,False):
            for hold in holds:
                for ef in expiry_flags:
                    for money in (0,1):
                        result.append({"family":"trend","fast":fast,"slow":slow,"vwap_filter":vwap,"hold":hold,"expiry":ef,"money":money})
    for gap in (0.0025,0.005,0.0075):
        for fam in ("gap_cont","gap_fade"):
            for hold in (3,6,12,24):
                for ef in expiry_flags:
                    for money in (0,1):
                        result.append({"family":fam,"gap":gap,"hold":hold,"expiry":ef,"money":money})
    for fast,slow in ((5,13),(8,21)):
        for hold in (3,6,12,24):
            for ef in expiry_flags:
                for money in (0,1):
                    result.append({"family":"pullback","fast":fast,"slow":slow,"hold":hold,"expiry":ef,"money":money})
    # deterministic cap; exact parameter universe is persisted with the run.
    return result[:600]

def metrics(daily, trades):
    x=np.asarray(daily,dtype=float)
    n=len(x)
    if n==0: return {"n_sessions":0,"trade_count":0}
    mean=float(np.mean(x)); med=float(np.median(x))
    # Newey-West HAC standard error with Bartlett weights, 5-session lag.
    z=x-mean; lr=float(np.dot(z,z)/n)
    lag=min(5,n-1)
    for k in range(1,lag+1):
        lr+=2*(1-k/(lag+1))*float(np.dot(z[k:],z[:-k])/n)
    se=math.sqrt(max(lr,0)/n)
    t=mean/se if se>0 else 0.0
    p=float(norm.sf(t)) if se>0 else 1.0
    rng=np.random.default_rng(SEED)
    boots=[]
    block=min(5,n)
    for _ in range(1500):
        starts=rng.integers(0,n,size=int(math.ceil(n/block)))
        sample=np.concatenate([x[(s+np.arange(block))%n] for s in starts])[:n]
        boots.append(float(sample.mean()))
    lo,hi=np.quantile(boots,[.025,.975])
    profits=sum(max(0,float(t["net_pnl_rupees"])) for t in trades)
    losses=sum(min(0,float(t["net_pnl_rupees"])) for t in trades)
    ret=[float(t["net_pnl_rupees"]) for t in trades]
    return {"n_sessions":n,"trade_count":len(trades),"mean_daily_net_rupees":mean,
        "median_daily_net_rupees":med,"daily_net_ci95_low":float(lo),"daily_net_ci95_high":float(hi),
        "hac_one_sided_p":p,"win_rate":float(np.mean(np.asarray(ret)>0)) if ret else None,
        "mean_net_per_trade":float(np.mean(ret)) if ret else None,"median_net_per_trade":float(np.median(ret)) if ret else None,
        "profit_factor":(profits/abs(losses)) if losses<0 else None,"total_net_rupees":float(sum(ret)),
        "positive_trade_count":int(sum(v>0 for v in ret)),"negative_trade_count":int(sum(v<0 for v in ret))}

def adjust_holm(pvals):
    arr=np.asarray(pvals,float); out=np.full(len(arr),np.nan)
    idx=np.flatnonzero(np.isfinite(arr)); order=idx[np.argsort(arr[idx])]
    run=0.0
    for rank,j in enumerate(order):
        run=max(run,min(1.0,(len(order)-rank)*arr[j])); out[j]=run
    return out.tolist()

def backtest(u,o,expiry_flags):
    if u.empty or o.empty:
        return {"status":"BLOCKED_NO_VALID_BARS","reason":"No fresh-source underlying or option bars"}
    # Exact timestamp alignment is required; no nearest-bar substitution.
    opt_entries={}
    opt_exits={}
    conflicted_entries=set()
    conflicted_exits=set()
    for r in o.itertuples(index=False):
        fam=r.expiry_flag
        entry_key=(fam,r.side,int(r.offset),int(r.timestamp))
        val=(float(r.strike),float(r.open),float(r.iv) if math.isfinite(r.iv) else np.nan)
        if entry_key not in conflicted_entries:
            if entry_key not in opt_entries:
                opt_entries[entry_key]=val
            else:
                prev=opt_entries[entry_key]
                if prev[0]!=val[0] or abs(prev[1]-val[1])>0.001:
                    opt_entries.pop(entry_key,None)
                    conflicted_entries.add(entry_key)
        exit_key=(fam,r.side,int(r.timestamp),round(float(r.strike),2))
        if exit_key not in conflicted_exits:
            if exit_key not in opt_exits:
                opt_exits[exit_key]=float(r.open)
            elif abs(opt_exits[exit_key]-float(r.open))>0.001:
                opt_exits.pop(exit_key,None)
                conflicted_exits.add(exit_key)
    days=sorted(u.date.unique())
    split1=days[int(len(days)*0.60)] if len(days)>20 else days[-1]
    split2=days[int(len(days)*0.80)] if len(days)>20 else days[-1]
    all_results=[]
    candidates=candidates_for(expiry_flags)
    for cidx,c in enumerate(candidates):
        events=signal_events(u,c)
        trades=[]
        for ev in events:
            day=ev["date"]
            if ev["entry_time"]<"09:25" or ev["entry_time"]>"14:00": continue
            daybars=u[u.date==day].sort_values("timestamp").reset_index(drop=True)
            # Use day-local index derived from timestamp; enter next bar and exit after holding bars.
            local_idx=daybars.index[daybars.timestamp==ev["entry_timestamp"]]
            if len(local_idx)==0: continue
            entry_idx=int(local_idx[0]); exit_idx=entry_idx+int(c["hold"])
            if exit_idx>=len(daybars): continue
            exit_ts=int(daybars.timestamp.iloc[exit_idx])
            if str(daybars.time.iloc[exit_idx])>"15:15": continue
            legs=[]
            structures=["CALL","PUT"] if c["family"] in ("orb_straddle","orb_strangle") else (["CALL"] if ev["direction"]>0 else ["PUT"])
            entry_missing=False
            for side in structures:
                offset=0
                if c["family"]=="orb_strangle":
                    offset=1 if side=="CALL" else -1
                elif c["family"] not in ("orb_straddle","orb_strangle") and int(c.get("money",0))==1:
                    offset=1 if side=="CALL" else -1
                ek=(c["expiry"],side,offset,int(ev["entry_timestamp"]))
                ent=opt_entries.get(ek)
                if ent is None:
                    entry_missing=True; break
                strike,entry,iv=ent
                xt=opt_exits.get((c["expiry"],side,exit_ts,round(strike,2)))
                if xt is None or not (entry>0 and xt>0):
                    entry_missing=True; break
                legs.append({"side":side,"strike":strike,"entry":entry,"exit":xt,"iv":iv})
            if entry_missing or not legs: continue
            result=cost_and_pnl(legs,day,50,10)
            trades.append({"date":day,"family":c["family"],"expiry":c["expiry"],"entry_timestamp":int(ev["entry_timestamp"]),
                "exit_timestamp":exit_ts,"direction":ev["direction"],"hold_bars":int(c["hold"]),
                "structure":"straddle" if c["family"]=="orb_straddle" else ("strangle" if c["family"]=="orb_strangle" else ("CALL" if ev["direction"]>0 else "PUT")),
                "gross_pnl_rupees":result["gross_pnl_rupees"],"net_pnl_rupees":result["net_pnl_rupees"],
                "total_cost_rupees":result["total_cost_rupees"],"entry_debit_rupees":result["entry_debit_rupees"],
                "brokerage_rupees":result["brokerage_rupees"],"stt_rupees":result["stt_rupees"],
                "exchange_fee_rupees":result["exchange_fee_rupees"],"stamp_rupees":result["stamp_rupees"],
                "gst_rupees":result["gst_rupees"],"slippage_bps_per_side":50,"brokerage_per_order":10,
                "lot_size_proxy":result["lot_size_proxy"],"expiry_code":1})
        # All-calendar-session daily series; no signal is zero P&L.
        result_rec={"candidate_id":cidx,"candidate":c,"event_count":len(events),"trade_count":len(trades)}
        for splitname,mask in (("train",lambda d:d<split1),("validation",lambda d:split1<=d<split2),("oos",lambda d:d>=split2)):
            st=[t for t in trades if mask(t["date"])]
            splitdays=[d for d in days if mask(d)]
            arr=[sum(float(t["net_pnl_rupees"]) for t in st if t["date"]==d) for d in splitdays]
            for k,v in metrics(arr,st).items(): result_rec[splitname+"_"+k]=v
        result_rec["trades"]=trades
        result_rec["candidate_key"]=json.dumps(c,sort_keys=True)
        all_results.append(result_rec)
    # Holm correction across complete OOS candidate family; do not rank by OOS alone.
    raw=[x.get("oos_hac_one_sided_p",np.nan) for x in all_results]
    adj=adjust_holm(raw)
    for item,p in zip(all_results,adj): item["oos_holm_p"]=p
    # Preselect by validation only; OOS confirms candidates but never tunes parameters.
    ranked=sorted(all_results,key=lambda x:(x.get("validation_mean_daily_net_rupees",-1e99),x.get("validation_daily_net_ci95_low",-1e99)),reverse=True)
    finalists={x["candidate_id"] for x in ranked[:20]}
    for item in all_results:
        item["selected_by_validation"]=item["candidate_id"] in finalists
        item["promotion_gate_pass"]=bool(
            item.get("oos_trade_count",0)>=150 and
            item.get("oos_mean_daily_net_rupees",0)>0 and item.get("oos_median_daily_net_rupees",0)>=0 and
            item.get("oos_daily_net_ci95_low",0)>0 and item.get("oos_holm_p",1)<0.05 and
            item.get("validation_mean_daily_net_rupees",0)>0
        )
    flat=[]
    for item in all_results:
        for t in item.pop("trades"):
            t["candidate_id"]=item["candidate_id"]; t["candidate_key"]=item["candidate_key"]
            t["selected_by_validation"]=item["selected_by_validation"]
            flat.append(t)
    return {"status":"PASS_ANALYZED","start_date":min(days),"end_date":max(days),"sessions":len(days),
            "underlying_rows":len(u),"option_rows":len(o),"expiry_flags":expiry_flags,
            "split_train_end":split1,"split_validation_end":split2,"candidate_count":len(all_results),
            "results":all_results,"ledger":flat,
            "notes":["Historical contract lot size is a date-based proxy pending exact expiry-level contract-master reconciliation.",
                     "Rolling-option OHLC has no historical best bid/ask; slippage is stress modeled, not observed spread.",
                     "Primary metrics use one-lot after-cost P&L, but not all execution quality can be proven with OHLC.",
                     "Only the latest 20% chronology is OOS; its full candidate-family p-values are Holm-adjusted."]}

def write_outputs(probe, acquisition, underlying, summary, errors):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"source_probe.json").write_text(json.dumps(probe,indent=2,default=str),encoding="utf-8")
    (OUT/"acquisition_summary.json").write_text(json.dumps(acquisition,indent=2,default=str),encoding="utf-8")
    (OUT/"underlying_summary.json").write_text(json.dumps(underlying,indent=2,default=str),encoding="utf-8")
    pd.DataFrame(errors).to_csv(OUT/"source_failures.csv",index=False)
    if summary is None:
        report={"research_id":"QE-NOB-1.0","run_status":"DATA_BLOCKED","generated_at_utc":utc_now(),
                "source_probe_status":probe.get("status"),"acquisition_status":acquisition.get("status"),
                "summary":"No profitability result because source acquisition/coverage did not pass."}
        (OUT/"run_summary.json").write_text(json.dumps(report,indent=2,default=str),encoding="utf-8")
        (OUT/"RESULTS.md").write_text("# QE-NOB-1.0 fresh run\n\n**Decision: DATA-LIMITED / NOT RUN.**\n\nNo valid full dataset was available, so no profitability result is claimed. See source_probe.json, acquisition_summary.json and source_failures.csv.\n",encoding="utf-8")
        return
    candidates=pd.DataFrame([{k:v for k,v in r.items() if k not in ("candidate","trades")} for r in summary["results"]])
    candidates.to_csv(OUT/"candidate_results.csv",index=False)
    pd.DataFrame(summary["ledger"]).to_csv(OUT/"trade_ledger_sanitized.csv",index=False)
    selected=candidates[candidates.selected_by_validation==True].sort_values("oos_mean_daily_net_rupees",ascending=False)
    keep=["candidate_id","candidate_key","validation_mean_daily_net_rupees","oos_trade_count","oos_mean_daily_net_rupees","oos_median_daily_net_rupees","oos_daily_net_ci95_low","oos_daily_net_ci95_high","oos_win_rate","oos_profit_factor","oos_total_net_rupees","oos_holm_p","promotion_gate_pass"]
    for col in keep:
        if col not in selected.columns: selected[col]=np.nan
    selected[keep].to_csv(OUT/"validation_finalists_oos.csv",index=False)
    report={k:v for k,v in summary.items() if k not in ("results","ledger")}
    passing=int(candidates.promotion_gate_pass.fillna(False).sum())
    best=selected.iloc[0].to_dict() if not selected.empty else {}
    report.update({"research_id":"QE-NOB-1.0","generated_at_utc":utc_now(),"passing_candidates":passing,
                   "decision":"PASS_FOR_FURTHER_PAPER_TEST_ONLY" if passing else "NO_PROMOTION",
                   "data_gate":"LIMITED — rolling OHLC only; no historic bid/ask; lot-size proxy requires contract-master validation",
                   "best_validation_finalist":{k:(v.item() if hasattr(v,"item") else v) for k,v in best.items() if k in keep}})
    (OUT/"run_summary.json").write_text(json.dumps(report,indent=2,default=str),encoding="utf-8")
    title="# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying"
    body=[title,"",f"**Run status:** {report['status']}  ",f"**Date range:** {report.get('start_date')} to {report.get('end_date')}  ",
          f"**Candidates tested:** {report.get('candidate_count')}  ",f"**Candidates passing the preliminary statistical gate:** {passing}  ",
          f"**Decision:** {report['decision']}","",
          "## Important execution-quality limitation",
          "The Dhan rolling endpoint supplies OHLC/IV/OI/volume/spot in an ATM-relative layout, not historical bid/ask depth. P&L therefore uses next-bar open with prespecified adverse slippage; this is not proof of executable fills. Historical expiry-level lot-size mapping still requires a contract-master reconciliation. A candidate does not qualify for live trading from this report.",
          "## Top candidates selected on validation only","",
          "|ID|Family|Validation mean daily net (₹)|OOS trades|OOS mean daily net (₹)|OOS 95% block CI low (₹)|OOS Holm p|Preliminary gate|",
          "|---:|---|---:|---:|---:|---:|---:|---|"]
    for _,r in selected.head(20).iterrows():
        body.append("|"+ "|".join(str(r.get(k,"")) for k in ["candidate_id","candidate_key","validation_mean_daily_net_rupees","oos_trade_count","oos_mean_daily_net_rupees","oos_daily_net_ci95_low","oos_holm_p","promotion_gate_pass"])+"|")
    body += ["","## Files","- source_probe.json and acquisition_summary.json: source status, range, cache and request outcomes",
             "- candidate_results.csv: all candidates, all chronology splits, full-family Holm correction",
             "- trade_ledger_sanitized.csv: sanitized per-trade P&L and fee decomposition",
             "- validation_finalists_oos.csv: finalists selected on validation and evaluated on the untouched OOS block",
             "- source_failures.csv: failed source requests; credentials are never written",
             "", "## Notes"] + ["- "+x for x in summary.get("notes",[])]
    (OUT/"RESULTS.md").write_text("\n".join(body)+"\n",encoding="utf-8")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--stage",choices=["probe","acquire","full","analyze","status"],default="full")
    parser.add_argument("--refresh-data",action="store_true")
    args=parser.parse_args()
    ensure_dirs()
    token=os.getenv("DHAN_ACCESS_TOKEN","").strip()
    probe_path=OUT/"source_probe.json"
    if args.stage=="status":
        print(json.dumps({"cache_exists":OPT_CACHE.exists(),"underlying_cache_exists":IDX_CACHE.exists(),"report_dir":str(OUT)},indent=2))
        return
    probe=probe_sources(token) if args.stage in ("probe","acquire","full") else (json.loads(probe_path.read_text()) if probe_path.exists() else {"status":"BLOCKED_NO_PRIOR_PROBE"})
    if args.stage=="probe":
        (OUT/"source_probe.json").write_text(json.dumps(probe,indent=2),encoding="utf-8")
        print(json.dumps(probe,indent=2)); return
    acquisition={"status":"NOT_REQUESTED"}
    underlying={"status":"NOT_REQUESTED"}
    errors=[]
    if args.stage in ("acquire","full"):
        if not probe.get("supported_expiries") or probe.get("underlying_probe",{}).get("status")!="PASS":
            acquisition={"status":"BLOCKED_SOURCE_PROBE","reason":"No verified expiry source or 5m underlying bars."}
            underlying={"status":"BLOCKED_SOURCE_PROBE"}
        else:
            acquisition=retrieve_options(token,probe["supported_expiries"],args.refresh_data)
            underlying=retrieve_underlying(token,args.refresh_data)
        (OUT/"source_probe.json").write_text(json.dumps(probe,indent=2,default=str),encoding="utf-8")
        # Public manifest intentionally excludes raw payloads, credentials and per-response content.
        acq_public={k:v for k,v in acquisition.items() if k not in ("requests","failures")}
        (OUT/"acquisition_summary.json").write_text(json.dumps(acq_public,indent=2,default=str),encoding="utf-8")
        (OUT/"underlying_summary.json").write_text(json.dumps({k:v for k,v in underlying.items() if k not in ("requests","failures")},indent=2,default=str),encoding="utf-8")
        failures=acquisition.get("failures",[])+underlying.get("failures",[])
        pd.DataFrame(failures).to_csv(OUT/"source_failures.csv",index=False)
        if args.stage=="acquire":
            print(json.dumps({"probe":probe.get("status"),"acquisition":acq_public,"underlying_status":underlying.get("status")},indent=2,default=str)); return
    if args.stage in ("full","analyze"):
        u,o=load_frames()
        expiry_flags=sorted(o.expiry_flag.dropna().unique().tolist()) if not o.empty else []
        if len(u)<500 or len(o)<1000:
            write_outputs(probe,acquisition,underlying,None,acquisition.get("failures",[])+underlying.get("failures",[]))
            print(json.dumps({"status":"DATA_BLOCKED","underlying_rows":len(u),"option_rows":len(o),"probe":probe.get("status")},indent=2))
            return
        summary=backtest(u,o,expiry_flags)
        write_outputs(probe,acquisition,underlying,summary,acquisition.get("failures",[])+underlying.get("failures",[]))
        print(json.dumps({k:v for k,v in summary.items() if k not in ("results","ledger")},indent=2,default=str))
if __name__=="__main__":
    main()
