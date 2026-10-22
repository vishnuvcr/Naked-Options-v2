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
    if part is None and any(k in data for k in ("timestamp","open","close")):
        part = data
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
            row = {"timestamp":ts,"expiry_flag":f"{flag}{int(code)}","expiry_family":flag,"expiry_code":int(code),"offset":int(offset),"side":side}
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

def load_frames(return_quality=False):
    bars=[]
    underlying_rows_read=0
    for path in sorted(IDX_CACHE.glob("nifty_5m_*.json")):
        try: obj=json.loads(path.read_text(encoding="utf-8"))
        except Exception: continue
        n=len(obj.get("timestamp",[]))
        if not n: continue
        underlying_rows_read+=n
        for i,ts in enumerate(obj["timestamp"]):
            try:
                row={"timestamp":int(ts)}
                for k in ("open","high","low","close","volume"):
                    v=obj.get(k,[np.nan]*n)[i]
                    row[k]=float(v) if v is not None and math.isfinite(float(v)) else np.nan
                bars.append(row)
            except (ValueError,TypeError,IndexError):
                continue
    quality={"underlying_rows_read":underlying_rows_read,"option_rows_read":0,
             "duplicate_groups":0,"conflicting_duplicate_groups":0,"conflicting_duplicate_rate":None,
             "option_rows_dropped_conflicts":0,"option_rows_after_conflict_filter":0,
             "option_timestamp_coverage":0.0,"row_grid_coverage":0.0}
    if not bars:
        return (pd.DataFrame(),pd.DataFrame(),quality) if return_quality else (pd.DataFrame(),pd.DataFrame())
    u=pd.DataFrame(bars).drop_duplicates("timestamp").sort_values("timestamp")
    u["dt"]=pd.to_datetime(u.timestamp,unit="s",utc=True).dt.tz_convert(TIME_ZONE)
    u["date"]=u.dt.dt.date.astype(str); u["time"]=u.dt.dt.strftime("%H:%M")
    u=u[(u["time"] >= "09:15") & (u["time"] <= "15:25")].copy()
    valid=(u[["open","high","low","close"]]>0).all(axis=1) & (u.high>=u[["open","close","low"]].max(axis=1)) & (u.low<=u[["open","close","high"]].min(axis=1))
    u=u[valid].sort_values("timestamp").reset_index(drop=True)
    opts=[]
    for path in sorted(OPT_CACHE.glob("*_*.json")):
        if path.name.startswith("probe_"): continue
        # Filename: expiry-family/code + inclusive dates + ATM offset + option type.
        parts=path.stem.split("_")
        if len(parts) != 5: continue
        try: flag=parts[0][:-1].upper(); code=int(parts[0][-1]); off=int(parts[3]); side=parts[4].upper()
        except Exception: continue
        if flag not in ("WEEK","MONTH") or side not in ("CALL","PUT"): continue
        try: obj=json.loads(path.read_text(encoding="utf-8"))
        except Exception: continue
        opts.extend(payload_rows(obj,flag,code,off,side))
    o=pd.DataFrame(opts)
    quality["option_rows_read"]=int(len(o))
    if not o.empty:
        o["dt"]=pd.to_datetime(o.timestamp,unit="s",utc=True).dt.tz_convert(TIME_ZONE)
        o["date"]=o.dt.dt.date.astype(str)
        o["strike_key"]=o.strike.round(2)
        key=["expiry_flag","expiry_code","side","timestamp","strike_key"]
        group_size=o.groupby(key).size()
        unique_prices=o.groupby(key).open.nunique(dropna=True)
        duplicate_keys=set(group_size[group_size>1].index.tolist())
        bad=set(unique_prices[unique_prices>1].index.tolist())
        quality["duplicate_groups"]=int(len(duplicate_keys))
        quality["conflicting_duplicate_groups"]=int(len(bad & duplicate_keys))
        quality["conflicting_duplicate_rate"]=float(quality["conflicting_duplicate_groups"]/max(1,quality["duplicate_groups"]))
        quality["option_rows_dropped_conflicts"]=int(sum(int(group_size.get(k,0)) for k in bad))
        if bad:
            idx=pd.MultiIndex.from_frame(o[key])
            o=o.loc[~idx.isin(bad)].copy()
        o=o.drop_duplicates(key,keep="first").reset_index(drop=True)
    quality["option_rows_after_conflict_filter"]=int(len(o))
    if len(u):
        common=set(u.timestamp.astype(int)).intersection(set(o.timestamp.astype(int))) if len(o) else set()
        quality["option_timestamp_coverage"]=float(len(common)/len(set(u.timestamp.astype(int))))
        expiries=int(o.expiry_flag.nunique()) if len(o) else 0
        expected=len(set(u.timestamp.astype(int)))*max(1,expiries)*14
        observed=len(o[["expiry_flag","side","offset","timestamp"]].drop_duplicates()) if len(o) else 0
        quality["row_grid_coverage"]=float(min(1.0,observed/max(1,expected)))
    return (u,o,quality) if return_quality else (u,o)

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

def reprice_premium_turnovers(raw_buy_turnover, raw_sell_turnover, day, slip_bps, brokerage, leg_count):
    # Reprice aggregate un-slipped premium turnover under a different cost stress.
    slip=float(slip_bps)/10000.0
    buy=float(raw_buy_turnover)*(1+slip)
    sell=max(0.0,float(raw_sell_turnover)*(1-slip))
    gross=sell-buy
    turnover=buy+sell
    d=pd.Timestamp(day).date()
    stt_rate=0.000625 if d < date(2024,10,1) else (0.001 if d < date(2026,4,1) else 0.0015)
    exchange_rate_value=exchange_rate(day)
    brokerage_total=float(brokerage)*2*int(leg_count)
    exchange=turnover*exchange_rate_value
    sebi=turnover*SEBI_RATE
    stamp=buy*STAMP_RATE
    stt=sell*stt_rate
    gst=GST_RATE*(brokerage_total+exchange+sebi)
    fees=brokerage_total+exchange+sebi+stamp+stt+gst
    return {"gross_pnl_rupees":gross,"net_pnl_rupees":gross-fees,"entry_debit_rupees":buy,
            "exit_credit_rupees":sell,"brokerage_rupees":brokerage_total,"exchange_fee_rupees":exchange,
            "sebi_fee_rupees":sebi,"stamp_rupees":stamp,"stt_rupees":stt,"gst_rupees":gst,
            "total_cost_rupees":fees,"stt_rate":stt_rate,"exchange_rate":exchange_rate_value,
            "turnover_rupees":turnover,"slippage_bps_per_side":float(slip_bps),
            "brokerage_per_order":float(brokerage),"leg_count":int(leg_count)}

def cost_and_pnl(legs, day, slip_bps, brokerage):
    # One lot per long option leg; use the date-effective lot-size schedule as a labelled proxy.
    lots=lot_size_proxy(day)
    raw_buy=sum(float(leg["entry"])*lots for leg in legs)
    raw_sell=sum(float(leg["exit"])*lots for leg in legs)
    result=reprice_premium_turnovers(raw_buy,raw_sell,day,slip_bps,brokerage,len(legs))
    result.update({"lot_size_proxy":lots,"raw_buy_premium_turnover_rupees":raw_buy,
                   "raw_sell_premium_turnover_rupees":raw_sell})
    return result

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
        if family in ("always_call","always_put","always_straddle","always_strangle"):
            sig=(1,1 if family in ("always_call","always_straddle","always_strangle") else -1)
        elif family in ("orb","orb_straddle","orb_strangle"):
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
    # Fixed-time always-buy comparators are placed first so a hard catalogue cap cannot remove them.
    for fam in ("always_call","always_put","always_straddle","always_strangle"):
        for hold in (3,6,12,24):
            for ef in expiry_flags:
                monies=(0,1) if fam in ("always_call","always_put") else (0,)
                for money in monies:
                    result.append({"family":fam,"hold":hold,"expiry":ef,"money":money})
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

def metrics(daily, trades, bootstrap_reps=0, net_column="net_pnl_rupees"):
    x=np.asarray(daily,dtype=float)
    n=len(x)
    if n==0: return {"n_sessions":0,"trade_count":0}
    mean=float(np.mean(x)); med=float(np.median(x))
    # Newey-West HAC standard error with Bartlett weights, five-session lag.
    z=x-mean; lr=float(np.dot(z,z)/n)
    lag=min(5,n-1)
    for k in range(1,lag+1):
        lr+=2*(1-k/(lag+1))*float(np.dot(z[k:],z[:-k])/n)
    se=math.sqrt(max(lr,0)/n)
    t=mean/se if se>0 else 0.0
    p=float(norm.sf(t)) if se>0 else 1.0
    lo=hi=float("nan")
    if bootstrap_reps > 0 and n >= 10:
        rng=np.random.default_rng(SEED)
        block=min(5,n); nblocks=int(math.ceil(n/block))
        starts=rng.integers(0,n,size=(bootstrap_reps,nblocks))
        offsets=np.arange(block)
        indices=(starts[:,:,None]+offsets[None,None,:])%n
        samples=x[indices].reshape(bootstrap_reps,-1)[:,:n]
        means=samples.mean(axis=1)
        lo,hi=np.quantile(means,[.025,.975])
    profits=sum(max(0,float(t.get(net_column,0))) for t in trades)
    losses=sum(min(0,float(t.get(net_column,0))) for t in trades)
    ret=[float(t.get(net_column,0)) for t in trades]
    std=float(np.std(x,ddof=1)) if n>1 else 0.0
    downside=float(np.sqrt(np.mean(np.minimum(x,0.0)**2)))
    sharpe=float(mean/std*np.sqrt(252)) if std>0 else 0.0
    sortino=float(mean/downside*np.sqrt(252)) if downside>0 else 0.0
    capital=500000.0
    equity=capital+np.cumsum(x)
    peaks=np.maximum.accumulate(np.concatenate(([capital],equity)))[1:]
    drawdowns=np.maximum(peaks-equity,0.0)
    mdd=float(drawdowns.max()) if len(drawdowns) else 0.0
    mdd_fraction=float(np.max(drawdowns/np.maximum(peaks,1.0))) if len(drawdowns) else 0.0
    cvar95=float(np.mean(x[x<=np.quantile(x,.05)])) if np.any(x<0) else 0.0
    return {"n_sessions":n,"trade_count":len(trades),"mean_daily_net_rupees":mean,
        "median_daily_net_rupees":med,"daily_net_ci95_low":float(lo),"daily_net_ci95_high":float(hi),
        "hac_one_sided_p":p,"win_rate":float(np.mean(np.asarray(ret)>0)) if ret else None,
        "mean_net_per_trade":float(np.mean(ret)) if ret else None,"median_net_per_trade":float(np.median(ret)) if ret else None,
        "profit_factor":(profits/abs(losses)) if losses<0 else None,"total_net_rupees":float(sum(ret)),
        "sharpe_ratio":sharpe,"sortino_ratio":sortino,"max_drawdown_rupees":mdd,
        "max_drawdown_fraction":mdd_fraction,"daily_cvar95_median":cvar95,
        "positive_trade_count":int(sum(v>0 for v in ret)),"negative_trade_count":int(sum(v<0 for v in ret))}

def adjust_holm(pvals):
    arr=np.asarray(pvals,float); out=np.full(len(arr),np.nan)
    idx=np.flatnonzero(np.isfinite(arr)); order=idx[np.argsort(arr[idx])]
    run=0.0
    for rank,j in enumerate(order):
        run=max(run,min(1.0,(len(order)-rank)*arr[j])); out[j]=run
    return out.tolist()

def backtest(u,o,expiry_flags,candidates_override=None,include_oos=True,bootstrap_reps=0):
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
    candidates=candidates_override if candidates_override is not None else candidates_for(expiry_flags)
    for cidx,c in enumerate(candidates):
        events=signal_events(u,c)
        if not include_oos:
            events=[ev for ev in events if ev['date'] < split2]
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
            structures=["CALL","PUT"] if c["family"] in ("orb_straddle","orb_strangle","always_straddle","always_strangle") else (["CALL"] if ev["direction"]>0 else ["PUT"])
            entry_missing=False
            for side in structures:
                offset=0
                if c["family"] in ("orb_strangle","always_strangle"):
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
            stress100=reprice_premium_turnovers(result["raw_buy_premium_turnover_rupees"],result["raw_sell_premium_turnover_rupees"],day,100,20,len(legs))
            stress200=reprice_premium_turnovers(result["raw_buy_premium_turnover_rupees"],result["raw_sell_premium_turnover_rupees"],day,200,20,len(legs))
            trade_rec={"date":day,"family":c["family"],"expiry":c["expiry"],"entry_timestamp":int(ev["entry_timestamp"]),
                "exit_timestamp":exit_ts,"direction":ev["direction"],"hold_bars":int(c["hold"]),
                "structure":"straddle" if c["family"] in ("orb_straddle","always_straddle") else ("strangle" if c["family"] in ("orb_strangle","always_strangle") else ("CALL" if ev["direction"]>0 else "PUT")),
                "gross_pnl_rupees":result["gross_pnl_rupees"],"net_pnl_rupees":result["net_pnl_rupees"],
                "total_cost_rupees":result["total_cost_rupees"],"entry_debit_rupees":result["entry_debit_rupees"],
                "brokerage_rupees":result["brokerage_rupees"],"stt_rupees":result["stt_rupees"],
                "exchange_fee_rupees":result["exchange_fee_rupees"],"stamp_rupees":result["stamp_rupees"],
                "gst_rupees":result["gst_rupees"],"slippage_bps_per_side":50,"brokerage_per_order":10,
                "lot_size_proxy":result["lot_size_proxy"],"stt_rate":result["stt_rate"],
                "exchange_rate":result["exchange_rate"],
                "raw_buy_premium_turnover_rupees":result["raw_buy_premium_turnover_rupees"],
                "raw_sell_premium_turnover_rupees":result["raw_sell_premium_turnover_rupees"],
                "stress100_fee20_net_pnl_rupees":stress100["net_pnl_rupees"],
                "stress200_fee20_net_pnl_rupees":stress200["net_pnl_rupees"],"leg_count":len(legs),"expiry_code":1}
            trades.append(trade_rec)
        # All-calendar-session daily series; no signal is zero P&L.
        result_rec={"candidate_id":cidx,"candidate":c,"event_count":len(events),"trade_count":len(trades)}
        for splitname,mask in (("train",lambda d:d<split1),("validation",lambda d:split1<=d<split2),("oos",lambda d:d>=split2)):
            if splitname=="oos" and not include_oos: continue
            st=[t for t in trades if mask(t["date"])]
            splitdays=[d for d in days if mask(d)]
            arr=[sum(float(t["net_pnl_rupees"]) for t in st if t["date"]==d) for d in splitdays]
            for k,v in metrics(arr,st,bootstrap_reps=bootstrap_reps).items(): result_rec[splitname+"_"+k]=v
            for stress_name,net_col in (("stress100_fee20","stress100_fee20_net_pnl_rupees"),("stress200_fee20","stress200_fee20_net_pnl_rupees")):
                stress_arr=[sum(float(t.get(net_col,0)) for t in st if t["date"]==d) for d in splitdays]
                for k,v in metrics(stress_arr,st,bootstrap_reps=0,net_column=net_col).items():
                    result_rec[splitname+"_"+stress_name+"_"+k]=v
        if include_oos:
            oos_days=[d for d in days if d>=split2]
            midpoint=max(1,len(oos_days)//2)
            oos_segments=(("oos_part1",set(oos_days[:midpoint])),("oos_part2",set(oos_days[midpoint:])))
            for part_name,part_days in oos_segments:
                st=[t for t in trades if t["date"] in part_days]
                arr=[sum(float(t["net_pnl_rupees"]) for t in st if t["date"]==d) for d in sorted(part_days)]
                for k,v in metrics(arr,st,bootstrap_reps=0).items():
                    result_rec[part_name+"_"+k]=v
        result_rec["trades"]=trades
        result_rec["candidate_key"]=json.dumps(c,sort_keys=True)
        all_results.append(result_rec)
    # Holm correction across complete OOS candidate family; do not rank by OOS alone.
    if include_oos:
        raw=[x.get("oos_hac_one_sided_p",np.nan) for x in all_results]
        adj=adjust_holm(raw)
        for item,p in zip(all_results,adj): item["oos_holm_p"]=p
    # During evolution only training/validation values exist in results; the final block is not used.
    ranked=sorted(all_results,key=lambda x:(x.get("validation_mean_daily_net_rupees",-1e99),x.get("validation_sharpe_ratio",0.0)),reverse=True)
    finalists={x["candidate_id"] for x in ranked[:20]} if include_oos else set()
    for item in all_results:
        item["selected_by_validation"]=item["candidate_id"] in finalists
        item["promotion_gate_pass"]=False
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
                     "Only the latest 20% chronology is reserved for final confirmation; its full candidate-family p-values are Holm-adjusted."]}

def genome_key(candidate):
    return json.dumps(candidate,sort_keys=True)

EVOLVABLE_FAMILIES=("orb","trend","gap_cont","gap_fade","pullback","orb_straddle","orb_strangle")

def hypothesis_for(candidate):
    fam=candidate["family"]
    if fam=="orb":
        return f"Break the first {candidate['range_bars']*5}-minute range with a {candidate['buffer']:.2f} range-width buffer; buy the directional option and hold {candidate['hold']*5} minutes."
    if fam=="trend":
        return f"An EMA {candidate['fast']}/{candidate['slow']} cross, optionally confirmed by VWAP, predicts continuation over {candidate['hold']*5} minutes."
    if fam=="gap_cont":
        return f"An opening gap of at least {candidate['gap']:.2%} continues intraday; buy the gap-direction option after the opening bars."
    if fam=="gap_fade":
        return f"An opening gap of at least {candidate['gap']:.2%} mean-reverts; buy the opposite-direction option after the opening bars."
    if fam=="pullback":
        return f"A {candidate['fast']}/{candidate['slow']} EMA trend resumes after a VWAP reclaim/rejection; hold {candidate['hold']*5} minutes."
    if fam in ("orb_straddle","orb_strangle"):
        structure="ATM long straddle" if fam=="orb_straddle" else "one-step OTM long strangle"
        return f"An opening-range break predicts enough realized movement to cover the cost of a {structure} over {candidate['hold']*5} minutes."
    if fam=="always_call":
        return f"Fixed-time long-call benchmark, {candidate['hold']*5}-minute holding period, moneyness offset {candidate.get('money',0)}."
    if fam=="always_put":
        return f"Fixed-time long-put benchmark, {candidate['hold']*5}-minute holding period, moneyness offset {candidate.get('money',0)}."
    if fam=="always_straddle":
        return f"Fixed-time ATM long-straddle benchmark with {candidate['hold']*5}-minute holding period."
    if fam=="always_strangle":
        return f"Fixed-time one-step OTM long-strangle benchmark with {candidate['hold']*5}-minute holding period."
    return "Structured long-premium strategy hypothesis."

def random_genome(rng, expiry_flags, family=None):
    fam=family or str(rng.choice(EVOLVABLE_FAMILIES))
    expiry=str(rng.choice(expiry_flags))
    hold=int(rng.choice((1,3,6,12,24)))
    money=int(rng.integers(0,2))
    c={"family":fam,"hold":hold,"expiry":expiry,"money":money}
    if fam in ("orb","orb_straddle","orb_strangle"):
        c["range_bars"]=int(rng.choice((1,3,6)))
        c["buffer"]=float(rng.choice((0.0,0.1,0.25,0.4)))
        if fam in ("orb_straddle","orb_strangle"): c.pop("money",None)
    elif fam=="trend":
        fast,slow=((5,13),(8,21),(9,34),(13,34))[int(rng.integers(0,4))]
        c.update({"fast":fast,"slow":slow,"vwap_filter":bool(rng.integers(0,2))})
    elif fam in ("gap_cont","gap_fade"):
        c["gap"]=float(rng.choice((0.0015,0.0025,0.005,0.0075,0.01)))
    elif fam=="pullback":
        fast,slow=((5,13),(8,21),(9,34))[int(rng.integers(0,3))]
        c.update({"fast":fast,"slow":slow})
    return c

def crossover_genome(a,b,rng,expiry_flags):
    parent_families=[p["family"] for p in (a,b) if p["family"] in EVOLVABLE_FAMILIES]
    fam=str(rng.choice(parent_families)) if parent_families and rng.random()<0.45 else str(rng.choice(EVOLVABLE_FAMILIES))
    child=random_genome(rng,expiry_flags,fam)
    for key in ("hold","expiry","money","range_bars","buffer","fast","slow","vwap_filter","gap"):
        if key in child:
            candidates=[p[key] for p in (a,b) if key in p]
            if candidates and rng.random()<0.8: child[key]=candidates[int(rng.integers(0,len(candidates)))]
    if "fast" in child and "slow" in child and child["fast"]>=child["slow"]:
        child["fast"],child["slow"]=(5,13) if child["fast"]==5 else (8,21)
    return child

def mutate_genome(parent,rng,expiry_flags):
    c=dict(parent)
    if rng.random()<0.12:
        return random_genome(rng,expiry_flags)
    if rng.random()<0.08:
        fam=str(rng.choice(EVOLVABLE_FAMILIES))
        return random_genome(rng,expiry_flags,fam)
    c["hold"]=int(rng.choice((1,3,6,12,24))) if rng.random()<0.4 else c["hold"]
    c["expiry"]=str(rng.choice(expiry_flags)) if rng.random()<0.25 else c["expiry"]
    if "money" in c and rng.random()<0.25: c["money"]=1-int(c["money"])
    if c["family"] in ("orb","orb_straddle","orb_strangle"):
        if rng.random()<0.4: c["range_bars"]=int(rng.choice((1,3,6)))
        if rng.random()<0.4: c["buffer"]=float(rng.choice((0.0,0.1,0.25,0.4)))
    elif c["family"]=="trend":
        if rng.random()<0.5:
            c["fast"],c["slow"]=((5,13),(8,21),(9,34),(13,34))[int(rng.integers(0,4))]
        if rng.random()<0.3: c["vwap_filter"]=not bool(c["vwap_filter"])
    elif c["family"] in ("gap_cont","gap_fade"):
        if rng.random()<0.5: c["gap"]=float(rng.choice((0.0015,0.0025,0.005,0.0075,0.01)))
    elif c["family"]=="pullback":
        if rng.random()<0.5: c["fast"],c["slow"]=((5,13),(8,21),(9,34))[int(rng.integers(0,3))]
    if "fast" in c and "slow" in c and c["fast"]>=c["slow"]:
        c["fast"],c["slow"]=(5,13) if c["fast"]==5 else (8,21)
    return c

def fitness_from_validation(result):
    mean=float(result.get("validation_mean_daily_net_rupees",0.0) or 0.0)
    sharpe=float(result.get("validation_sharpe_ratio",0.0) or 0.0)
    pf=result.get("validation_profit_factor")
    pf=float(pf) if pf is not None and math.isfinite(float(pf)) else 0.1
    pf=max(0.05,min(pf,5.0))
    dd=float(result.get("validation_max_drawdown_fraction",0.0) or 0.0)
    n=int(result.get("validation_trade_count",0) or 0)
    score=0.45*math.tanh(sharpe/2.0)+0.25*math.tanh(mean/500.0)+0.20*math.tanh(math.log(pf))-2.0*dd
    if mean<=0: score-=0.8
    if float(result.get("train_mean_daily_net_rupees",0.0) or 0.0)<=0: score-=0.2
    if n<30: score-=1.0
    return float(score)

def niche_key(candidate,result):
    n=int(result.get("validation_trade_count",0) or 0)
    freq="low" if n<20 else ("mid" if n<80 else "high")
    dd=float(result.get("validation_max_drawdown_fraction",0.0) or 0.0)
    risk="low" if dd<0.02 else ("mid" if dd<0.08 else "high")
    return "|".join((candidate["family"],freq,risk))

def trim_island(keys,eval_cache,population_size):
    unique=[]
    for k in keys:
        if k in eval_cache and k not in unique: unique.append(k)
    unique.sort(key=lambda k:eval_cache[k]["fitness"],reverse=True)
    keep=[]; niches=set()
    for k in unique:
        niche=eval_cache[k]["niche"]
        if niche not in niches:
            keep.append(k); niches.add(niche)
        if len(keep)>=population_size: return keep[:population_size]
    for k in unique:
        if k not in keep: keep.append(k)
        if len(keep)>=population_size: break
    return keep[:population_size]

def run_quant_evolve(u,o,expiry_flags,data_quality=None):
    # QuantEvolve-inspired: four-island search, hypothesis templates, niche archive, crossover,
    # mutation, migration, validation-only fitness. The final chronological block is not touched here.
    cfg=json.loads(CONFIG_PATH.read_text())
    rng=np.random.default_rng(int(cfg["random_seeds"][1]))
    budget=int(cfg["candidate_budget_unique"]); max_gen=int(cfg["max_generations"])
    n_islands=int(cfg["islands"]); pop_size=int(cfg["population_size"])
    children_per_island=12
    all_genomes={}; meta={}; eval_cache={}; archive={}; trace=[]
    islands=[[] for _ in range(n_islands)]
    baselines=[x for x in candidates_for(expiry_flags) if x["family"].startswith("always_")]
    for i,cand in enumerate(baselines):
        key=genome_key(cand); all_genomes.setdefault(key,cand)
        meta.setdefault(key,{"generation_created":0,"island_created":i%n_islands,"parent_key":"","hypothesis":hypothesis_for(cand),"origin":"fixed_baseline"})
        islands[i%n_islands].append(key)
    for i in range(n_islands):
        attempts=0
        while len(islands[i])<pop_size and attempts<10000:
            attempts+=1
            cand=random_genome(rng,expiry_flags); key=genome_key(cand)
            all_genomes.setdefault(key,cand)
            if key not in islands[i]: islands[i].append(key)
            meta.setdefault(key,{"generation_created":0,"island_created":i,"parent_key":"","hypothesis":hypothesis_for(cand),"origin":"random_seed"})
    if len(all_genomes)>budget:
        all_genomes=dict(list(all_genomes.items())[:budget])
        allowed=set(all_genomes)
        islands=[[k for k in pop if k in allowed] for pop in islands]
    def evaluate_new(keys):
        todo=[k for k in dict.fromkeys(keys) if k not in eval_cache and k in all_genomes]
        if not todo: return
        candidates=[all_genomes[k] for k in todo]
        output=backtest(u,o,expiry_flags,candidates_override=candidates,include_oos=False,bootstrap_reps=0)
        if output.get("status")!="PASS_ANALYZED":
            raise RuntimeError("validation evaluation blocked: "+str(output.get("reason",output.get("status"))))
        for row in output["results"]:
            cand=row["candidate"]; key=genome_key(cand)
            fit=fitness_from_validation(row); niche=niche_key(cand,row)
            saved={k:v for k,v in row.items() if k not in ("candidate","trades")}
            saved.update({"candidate":cand,"fitness":fit,"niche":niche,"hypothesis":hypothesis_for(cand)})
            eval_cache[key]=saved
            current=archive.get(niche)
            if current is None or fit>current["fitness"]:
                archive[niche]={"candidate_key":key,"fitness":fit,"candidate":cand,
                    "validation_mean_daily_net_rupees":row.get("validation_mean_daily_net_rupees"),
                    "validation_sharpe_ratio":row.get("validation_sharpe_ratio"),
                    "validation_profit_factor":row.get("validation_profit_factor"),
                    "validation_max_drawdown_fraction":row.get("validation_max_drawdown_fraction"),
                    "validation_trade_count":row.get("validation_trade_count"),
                    "hypothesis":hypothesis_for(cand)}
    all_initial=list(all_genomes)
    evaluate_new(all_initial)
    for island_id in range(n_islands):
        islands[island_id]=trim_island(islands[island_id],eval_cache,pop_size)
    generations_done=0
    for generation in range(1,max_gen+1):
        if len(all_genomes)>=budget: break
        children=[]; child_origins=[]
        for island_id in range(n_islands):
            made=0; attempts=0
            while made<children_per_island and len(all_genomes)+len(children)<budget and attempts<children_per_island*30:
                attempts+=1
                local=[k for k in islands[island_id] if k in eval_cache]
                if not local: break
                if archive and rng.random()<0.65:
                    candidates_archive=list(archive.values())
                    # Uniform niche sampling preserves behavioral diversity; rank is only a secondary bias.
                    candidates_archive.sort(key=lambda a:a["fitness"],reverse=True)
                    top=candidates_archive[:max(1,int(len(candidates_archive)*0.7))]
                    p1=top[int(rng.integers(0,len(top)))]["candidate"]
                else:
                    p1=all_genomes[local[int(rng.integers(0,len(local)))]]
                same_family=[a for a in archive.values() if a["candidate"]["family"]==p1["family"]]
                cousin_pool=same_family or list(archive.values())
                if cousin_pool and rng.random()<0.75:
                    p2=cousin_pool[int(rng.integers(0,len(cousin_pool)))]["candidate"]
                else:
                    p2=all_genomes[local[int(rng.integers(0,len(local)))]]
                child=crossover_genome(p1,p2,rng,expiry_flags)
                child=mutate_genome(child,rng,expiry_flags)
                key=genome_key(child)
                if key in all_genomes or any(genome_key(x)==key for x in children): continue
                children.append(child)
                child_origins.append({"key":key,"island":island_id,"generation":generation,"parent":genome_key(p1)})
                made+=1
            for record in child_origins[-made:] if made else []:
                islands[island_id].append(record["key"])
                meta[record["key"]]={"generation_created":generation,"island_created":island_id,
                    "parent_key":record["parent"],"hypothesis":hypothesis_for(next(x for x in children if genome_key(x)==record["key"])),"origin":"mutation_crossover"}
        if not children: break
        # Enforce the unique-candidate budget at insertion, before any evaluation.
        inserted=[]
        for child in children:
            key=genome_key(child)
            if key not in all_genomes and len(all_genomes)<budget:
                all_genomes[key]=child; inserted.append(key)
        evaluate_new(inserted)
        for island_id in range(n_islands):
            islands[island_id]=trim_island(islands[island_id],eval_cache,pop_size)
        # Periodic island migration of the strongest current individual.
        if generation%5==0:
            champions=[max(pop,key=lambda k:eval_cache[k]["fitness"]) for pop in islands if pop]
            for source_id,champion in enumerate(champions):
                target=(source_id+1)%n_islands
                if champion not in islands[target]:
                    islands[target]=trim_island(islands[target]+[champion],eval_cache,pop_size)
        trace.append({"generation":generation,"unique_candidates_evaluated":len(eval_cache),
            "qd_archive_niches":len(archive),"new_children":len(inserted),
            "best_validation_fitness":max((x["fitness"] for x in eval_cache.values()),default=float("nan")),
            "best_validation_mean_daily_net_rupees":max((float(x.get("validation_mean_daily_net_rupees",0) or 0) for x in eval_cache.values()),default=0.0)})
        generations_done=generation
        if len(all_genomes)>=budget: break
    # Final locked evaluation: all generated candidates are scored against the untouched OOS block once.
    frozen_keys=list(all_genomes)
    final=backtest(u,o,expiry_flags,candidates_override=[all_genomes[k] for k in frozen_keys],include_oos=True,bootstrap_reps=0)
    if final.get("status")!="PASS_ANALYZED": return final
    selected=sorted(final["results"],key=lambda x:(float(x.get("validation_mean_daily_net_rupees",0) or 0),float(x.get("validation_sharpe_ratio",0) or 0)),reverse=True)[:20]
    finalist_candidates=[x["candidate"] for x in selected]
    if finalist_candidates:
        detail=backtest(u,o,expiry_flags,candidates_override=finalist_candidates,include_oos=True,bootstrap_reps=int(cfg["bootstrap_replicates"]))
        detail_map={x["candidate_key"]:x for x in detail["results"]}
        for row in final["results"]:
            detailed=detail_map.get(row["candidate_key"])
            if detailed and row["selected_by_validation"]:
                for k,v in detailed.items():
                    if k.startswith(("train_","validation_","oos_")) and k!="oos_holm_p":
                        row[k]=v
    # Preserve the all-candidate Holm adjustment from the single final OOS evaluation.
    finalist_keys={genome_key(x) for x in finalist_candidates}
    for row in final["results"]:
        key=row["candidate_key"]
        metadata=meta.get(key,{})
        row.update({"hypothesis":metadata.get("hypothesis",hypothesis_for(row["candidate"])),
                    "generation_created":metadata.get("generation_created",0),
                    "island_created":metadata.get("island_created",-1),
                    "parent_key":metadata.get("parent_key",""),
                    "origin":metadata.get("origin","random_or_baseline"),
                    "evolution_fitness":eval_cache.get(key,{}).get("fitness",float("nan")),
                    "qd_niche":eval_cache.get(key,{}).get("niche","")})
        row["selected_by_validation"]=key in finalist_keys
        # Statistical gate first; the stricter overall promotion gate is applied after source audit.
        row["statistical_gate_pass"]=bool(
            row.get("oos_trade_count",0)>=150 and
            row.get("oos_mean_daily_net_rupees",0)>0 and row.get("oos_median_daily_net_rupees",0)>0 and
            row.get("oos_daily_net_ci95_low",0)>0 and row.get("oos_holm_p",1)<0.05 and
            row.get("validation_mean_daily_net_rupees",0)>0 and
            row.get("oos_stress100_fee20_mean_daily_net_rupees",0)>0 and
            row.get("oos_part1_trade_count",0)>=40 and row.get("oos_part2_trade_count",0)>=40 and
            row.get("oos_part1_mean_daily_net_rupees",0)>0 and
            row.get("oos_part2_mean_daily_net_rupees",0)>0)
        # Strict execution gate: rolling relative-strike OHLC and a lot-size proxy are not
        # sufficient for strategy promotion, irrespective of a nominal statistical win.
        row["promotion_gate_pass"]=False
        row["execution_data_gate_pass"]=False
        row["execution_data_gate_reason"]="No historical bid/ask/depth validation; contract-expiry and lot-size mapping not reconciled to dated instrument master."
    archive_rows=sorted(archive.values(),key=lambda x:x["fitness"],reverse=True)
    final.update({"evolution":{"method":"bounded QuantEvolve-inspired quality-diversity island evolution",
        "generations_completed":generations_done,"islands":n_islands,"population_size_per_island":pop_size,
        "candidate_budget":budget,"unique_candidates":len(all_genomes),"evaluated_candidates":len(eval_cache),
        "qd_archive_niches":len(archive),"offspring_per_island_per_generation":children_per_island,
        "selection_metric":"validation-only composite of net P&L, Sharpe, profit factor and drawdown; no final OOS values used during discovery",
        "implementation_note":"Strategy generation is constrained and template-based, not arbitrary LLM-generated code. Multi-agent roles are implemented as deterministic research/hypothesis/coding/evaluation functions; no unverified LLM API key is required."},
        "evolution_trace":trace,"qd_archive":archive_rows,"candidate_metadata":meta,"data_quality":data_quality or {}})
    return final

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
    selected=candidates[candidates.selected_by_validation==True]
    if "validation_mean_daily_net_rupees" in selected.columns:
        selected=selected.sort_values("validation_mean_daily_net_rupees",ascending=False)
    keep=["candidate_id","candidate_key","family","hypothesis","generation_created","island_created","origin","evolution_fitness",
          "validation_mean_daily_net_rupees","validation_trade_count","oos_trade_count",
          "oos_mean_daily_net_rupees","oos_median_daily_net_rupees","oos_daily_net_ci95_low","oos_daily_net_ci95_high",
          "oos_part1_mean_daily_net_rupees","oos_part2_mean_daily_net_rupees","oos_win_rate","oos_profit_factor",
          "oos_sharpe_ratio","oos_sortino_ratio","oos_max_drawdown_fraction","oos_total_net_rupees","oos_holm_p",
          "oos_stress100_fee20_mean_daily_net_rupees","oos_stress200_fee20_mean_daily_net_rupees",
          "statistical_gate_pass","execution_data_gate_pass","execution_data_gate_reason","promotion_gate_pass"]
    for col in keep:
        if col not in selected.columns: selected[col]=np.nan
    selected[keep].to_csv(OUT/"validation_finalists_oos.csv",index=False)
    report={k:v for k,v in summary.items() if k not in ("results","ledger","candidate_metadata")}
    statistical_candidates=int(candidates.statistical_gate_pass.fillna(False).sum()) if "statistical_gate_pass" in candidates else 0
    promoted=int(candidates.promotion_gate_pass.fillna(False).sum()) if "promotion_gate_pass" in candidates else 0
    quality=summary.get("data_quality",{})
    coverage=float(quality.get("row_grid_coverage",0.0) or 0.0)
    conflict_rate=quality.get("conflicting_duplicate_rate")
    basic_quality_pass=bool(coverage>=0.90 and conflict_rate is not None and float(conflict_rate)<=0.005)
    execution_ready=bool(basic_quality_pass and quality.get("historical_bid_ask_available",False) and quality.get("exact_expiry_identity_validated",False) and quality.get("historical_lot_size_verified",False))
    if promoted and execution_ready:
        decision="PASS_FOR_FURTHER_PAPER_TEST_ONLY"
    elif statistical_candidates:
        decision="DATA_LIMITED — statistical candidate(s) found, but execution/contract gate remains unproven"
    else:
        decision="NO_STATISTICAL_CANDIDATE — profitability not established; execution data limitations remain"
    best=selected.iloc[0].to_dict() if not selected.empty else {}
    report.update({"research_id":"QE-NOB-1.0","generated_at_utc":utc_now(),
                   "statistical_candidate_count":statistical_candidates,"promotion_candidate_count":promoted,
                   "basic_data_quality_gate_pass":basic_quality_pass,"execution_data_gate_pass":execution_ready,
                   "decision":decision,
                   "data_gate":"Historical bid/ask/depth not validated; rolling ATM-relative OHLC and date-based lot-size proxy cannot prove executable fills.",
                   "best_validation_finalist":{k:(v.item() if hasattr(v,"item") else v) for k,v in best.items() if k in keep}})
    (OUT/"run_summary.json").write_text(json.dumps(report,indent=2,default=str),encoding="utf-8")
    title="# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying"
    body=[title,"",f"**Run status:** {report['status']}  ",f"**Date range:** {report.get('start_date')} to {report.get('end_date')}  ",
          f"**Candidates tested:** {report.get('candidate_count')}  ",f"**Candidates passing the preliminary statistical gate:** {passing}  ",
          f"**Decision:** {report['decision']}","",
          "## Important execution-quality limitation",
          "The Dhan rolling endpoint supplies OHLC/IV/OI/volume/spot in an ATM-relative layout, not historical bid/ask depth. P&L therefore uses next-bar open with prespecified adverse slippage; this is not proof of executable fills. Historical expiry-level lot-size mapping still requires a contract-master reconciliation. The full promotion gate cannot pass until historical execution quotes and contract identity are verified. Even a future PASS only permits prospective paper testing, never automatic live trading.",
          "## Top candidates selected on validation only","",
          "|ID|Hypothesis|Validation mean daily net (₹)|OOS trades|OOS mean daily net (₹)|OOS 95% block CI low (₹)|OOS Holm p|Statistical gate|",
          "|---:|---|---:|---:|---:|---:|---:|---|"]
    for _,r in selected.head(20).iterrows():
        body.append("|"+ "|".join(str(r.get(k,"")) for k in ["candidate_id","hypothesis","validation_mean_daily_net_rupees","oos_trade_count","oos_mean_daily_net_rupees","oos_daily_net_ci95_low","oos_holm_p","statistical_gate_pass"])+"|")
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
        u,o,data_quality=load_frames(return_quality=True)
        expiry_flags=sorted(o.expiry_flag.dropna().unique().tolist()) if not o.empty else []
        if len(u)<500 or len(o)<1000:
            write_outputs(probe,acquisition,underlying,None,acquisition.get("failures",[])+underlying.get("failures",[]))
            print(json.dumps({"status":"DATA_BLOCKED","underlying_rows":len(u),"option_rows":len(o),"probe":probe.get("status")},indent=2))
            return
        summary=run_quant_evolve(u,o,expiry_flags,data_quality)
        write_outputs(probe,acquisition,underlying,summary,acquisition.get("failures",[])+underlying.get("failures",[]))
        print(json.dumps({k:v for k,v in summary.items() if k not in ("results","ledger")},indent=2,default=str))
if __name__=="__main__":
    main()
