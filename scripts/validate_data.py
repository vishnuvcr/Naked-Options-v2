#!/usr/bin/env python3
"""Validate a cached NIFTY session series and write a secret-free data audit."""
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/cache/nifty50_daily.csv")
    a=p.parse_args()
    src=(ROOT/a.input).resolve()
    if not src.exists():
        raise SystemExit(f"BLOCKED: expected data file not found: {a.input}")
    df=pd.read_csv(src)
    required={"date","open","high","low","close","volume","source_id"}
    missing=sorted(required-set(df.columns))
    errors=[]
    if missing: errors.append("missing columns: "+",".join(missing))
    if errors: raise SystemExit("; ".join(errors))
    df["date"]=pd.to_datetime(df["date"],errors="coerce")
    if df.date.isna().any(): errors.append("invalid dates")
    if df.date.duplicated().any(): errors.append(f"duplicate date rows={int(df.date.duplicated(keep=False).sum())}")
    if not df.date.is_monotonic_increasing: errors.append("dates are not sorted ascending")
    if df[["open","high","low","close"]].isna().any().any(): errors.append("missing required OHLC values")
    if (df[["open","high","low","close"]]<=0).any().any(): errors.append("nonpositive OHLC values")
    bad=(df.high < df[["open","close","low"]].max(axis=1)) | (df.low > df[["open","close","high"]].min(axis=1))
    if bad.any(): errors.append(f"OHLC inconsistency rows={int(bad.sum())}")
    weekend=(df.date.dt.dayofweek>=5)
    if weekend.any(): errors.append(f"weekend observations={int(weekend.sum())}")
    if len(df)<500: errors.append(f"insufficient sample rows={len(df)}; >=500 required for the planned multi-horizon study")
    # Dates absent between observations are reported, not assumed to be errors: NSE holidays exist.
    dates=df.date.sort_values().reset_index(drop=True)
    gaps=dates.diff().dt.days.dropna()
    report={
      "checked_at_utc":datetime.now(timezone.utc).isoformat(),
      "file":str(src.relative_to(ROOT)),
      "sha256":hashlib.sha256(src.read_bytes()).hexdigest(),
      "rows":int(len(df)),
      "first_date":None if df.empty else df.date.min().date().isoformat(),
      "last_date":None if df.empty else df.date.max().date().isoformat(),
      "source_ids":sorted(df.source_id.dropna().astype(str).unique().tolist()),
      "missing_volume_rows":int(df.volume.isna().sum()),
      "missing_volume_fraction":None if len(df)==0 else float(df.volume.isna().mean()),
      "nontrading_day_rows":int(weekend.sum()),
      "observed_gap_days_gt_4":int((gaps>4).sum()),
      "largest_calendar_gap_days":None if gaps.empty else int(gaps.max()),
      "validation":"FAIL" if errors else "PASS",
      "errors":errors,
      "notes":["Calendar gaps are reported only; weekends and exchange holidays are not imputed.",
               "Missing volume may reflect a source limitation; it is not silently replaced with zero."]
    }
    out=ROOT/"reports"/"data_quality.json"; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    return 0 if not errors else 3

if __name__=="__main__":
    raise SystemExit(main())
