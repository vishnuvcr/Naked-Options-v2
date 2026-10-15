#!/usr/bin/env python3
"""Sanitized source/weekly-expiry feasibility gate for VOL-REGIME-OPT-1.0."""
from __future__ import annotations
import hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "vol_regime_weekly_probe"
OUT = ROOT / "reports" / "vol_regime_options"
URL = "https://api.dhan.co/v2/charts/rollingoption"
TOKEN = os.getenv("DHAN_ACCESS_TOKEN", "").strip()
START, END = "2025-01-06", "2025-01-11"  # five-day, historical schema probe only

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_detail(resp):
    try:
        d = resp.json()
        if isinstance(d, dict):
            bits = [f"{k}={d[k]}" for k in ("errorCode","errorType","errorMessage","remarks","message","status") if k in d and not isinstance(d[k],(dict,list))]
            s = " ".join(bits) if bits else json.dumps(d)
        else: s = str(d)
    except Exception: s = resp.text
    s = s.replace(TOKEN, "[REDACTED]") if TOKEN else s
    s = re.sub(r"(?i)(access-token|authorization|token)\s*[:=]\s*[^\s,;]+", r"\1=[REDACTED]", s)
    return s.replace("\n"," ")[:300]

def validate(payload, option_type):
    data = payload.get("data", payload)
    if not isinstance(data, dict): return {"status":"FAIL","reason":"data_not_object"}
    key = "ce" if option_type == "CALL" else "pe"
    part = data.get(key, data if "timestamp" in data else None)
    if part is None: return {"status":"EMPTY","reason":"null_series"}
    if not isinstance(part,dict): return {"status":"FAIL","reason":"series_not_object"}
    required = ("timestamp","open","close","strike","spot","iv")
    missing = [k for k in required if k not in part]
    if missing: return {"status":"FAIL","reason":"missing_fields","missing_fields":missing}
    lens = {k:len(part[k]) for k in required if isinstance(part[k],list)}
    if len(lens) != len(required) or len(set(lens.values())) != 1:
        return {"status":"FAIL","reason":"array_length_mismatch","lengths":lens}
    n = lens["timestamp"]
    return {"status":"PASS" if n else "EMPTY","rows":n,"fields":list(required),
            "timestamps_monotonic":all(a<=b for a,b in zip(part["timestamp"],part["timestamp"][1:])),
            "sample_strikes":sorted(set(float(x) for x in part["strike"] if x is not None))[:8]}

def main():
    CACHE.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
    report={"study":"VOL-REGIME-OPT-1.0","phase":"2-source-audit","checked_at_utc":datetime.now(timezone.utc).isoformat(),
            "probe_window":{"from":START,"to_exclusive":END},"endpoint":URL,"credential_present":bool(TOKEN),
            "source_documentation":"https://dhanhq.co/docs/v2/expired-options-data/","requests":[]}
    if not TOKEN:
        report.update(status="BLOCKED_MISSING_DHAN_ACCESS_TOKEN", decision="No request made; credentials were not available to the workflow.")
    else:
        session=requests.Session()
        session.headers.update({"Accept":"application/json","Content-Type":"application/json","access-token":TOKEN})
        for flag,code in (("WEEK",0),("WEEK",1),("WEEK",2),("MONTH",1)):
            for typ in ("CALL","PUT"):
                body={"exchangeSegment":"NSE_FNO","interval":5,"securityId":13,"instrument":"OPTIDX",
                      "expiryFlag":flag,"expiryCode":code,"strike":"ATM","drvOptionType":typ,
                      "requiredData":["open","high","low","close","iv","volume","strike","oi","spot"],
                      "fromDate":START,"toDate":END}
                rec={"expiry_flag":flag,"expiry_code":code,"option_type":typ}
                try:
                    resp=session.post(URL,json=body,timeout=60)
                    rec["http_status"]=resp.status_code
                    if not resp.ok or "json" not in resp.headers.get("content-type","").lower():
                        rec.update(status="FAIL",error=safe_detail(resp))
                    else:
                        payload=resp.json(); rec.update(validate(payload,typ))
                        raw=CACHE/f"{START}_{END}_{flag}{code}_{typ}.json"
                        raw.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8")
                        rec["cache_file"]=str(raw.relative_to(ROOT)); rec["sha256"]=sha256(raw)
                except Exception as e:
                    rec.update(status="FAIL",error=f"{type(e).__name__}: {str(e)[:200]}")
                report["requests"].append(rec)
                time.sleep(0.35)
        weekly=[r for r in report["requests"] if r["expiry_flag"]=="WEEK"]
        monthly=[r for r in report["requests"] if r["expiry_flag"]=="MONTH"]
        # Code 0 can be rejected by the endpoint despite appearing in the annexure.
        # The bounded probe checks codes 0/1/2; require both call and put to pass
        # for at least one identical weekly expiry code, rather than requiring all
        # candidate codes to succeed or incorrectly expecting only two requests.
        weekly_codes=sorted({r["expiry_code"] for r in weekly})
        valid_weekly_codes=[
            code for code in weekly_codes
            if all(any(r["expiry_code"]==code and r["option_type"]==typ and r.get("status")=="PASS"
                       for r in weekly) for typ in ("CALL","PUT"))
        ]
        report["weekly_candidate_codes"]=valid_weekly_codes
        report["weekly_schema_pass"]=bool(valid_weekly_codes)
        report["monthly_control_pass"]=bool(len(monthly)==2 and all(r.get("status")=="PASS" for r in monthly))
        report["status"]="PASS_WEEKLY_SCHEMA" if report["weekly_schema_pass"] else ("BLOCKED_WEEKLY_SCHEMA" if report["monthly_control_pass"] else "BLOCKED_SOURCE_OR_AUTH")
        report["decision"]=("Weekly endpoint returned structurally valid data for candidate expiryCode(s); map each code to actual expiry dates and validate exact contract identity before any P&L work." if report["weekly_schema_pass"] else
            "Do not substitute monthly data. The bounded expiryCode probe did not find a valid weekly call/put pair; stop the weekly strategy and report the source gate as blocked.")
    p=OUT/"source_audit.json"; p.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    if report["status"] not in ("PASS_WEEKLY_SCHEMA",): sys.exit(2)

if __name__=="__main__": main()
