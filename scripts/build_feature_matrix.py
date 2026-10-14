"""Build lagged predictors and forward targets from validated daily bars."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data"/"cache"
def build(df):
    df=df.sort_values("date").copy().reset_index(drop=True)
    df["date"]=pd.to_datetime(df["date"],errors="raise")
    c=pd.to_numeric(df["close"],errors="raise")
    r=np.log(c).diff()
    x=pd.DataFrame(index=df.index)
    x["log_close"]=np.log(c)
    x["intraday_return"]=np.log(df["close"]/df["open"])
    x["range"]=np.log(df["high"]/df["low"])
    x["gap"]=np.log(df["open"]/df["close"].shift(1))
    x["log_volume"]=np.log1p(pd.to_numeric(df.volume,errors="coerce").clip(lower=0))
    for k in (0,1,2,3,5,10,20,40,60):
        x[f"ret_{k}"]=r.shift(k)
    for w in (5,10,14,20,40,60):
        x[f"mom_{w}"]=np.log(c)-np.log(c).shift(w)
        x[f"vol_{w}"]=r.rolling(w,min_periods=w).std()
        x[f"absret_{w}"]=r.abs().rolling(w,min_periods=w).mean()
    gain=r.clip(lower=0).rolling(14,min_periods=14).mean()
    loss=-r.clip(upper=0).rolling(14,min_periods=14).mean()
    x["rsi_14"]=100-100/(1+gain/(loss+1e-12))
    out=pd.concat([df[["date","open","high","low","close","volume","source_id"]],x],axis=1)
    out["origin_i"]=np.arange(len(out))
    for h in (1,5,20):
        y=np.log(c.shift(-h))-np.log(c)
        out[f"target_date_{h}"]=out.date.shift(-h).dt.strftime("%Y-%m-%d")
        out[f"target_return_{h}"]=y
        out[f"target_direction_{h}"]=np.where(y.notna(),(y>0).astype(float),np.nan)
        out[f"target_close_{h}"]=c.shift(-h)
        out[f"target_log_close_{h}"]=np.log(c.shift(-h))
        fr=pd.concat([r.shift(-k) for k in range(1,h+1)],axis=1)
        fv=r.shift(-1).abs() if h==1 else fr.std(axis=1,ddof=1)
        out[f"target_future_vol_{h}"]=fv
        out[f"target_vol_expansion_{h}"]=np.where(fv.notna() & x["vol_20"].notna(),(fv>x["vol_20"]).astype(float),np.nan)
    return out.replace([np.inf,-np.inf],np.nan)
def main():
    src=CACHE/"nifty50_daily.csv"; q=ROOT/"reports"/"data_quality.json"
    if not src.exists() or not q.exists() or json.loads(q.read_text()).get("validation")!="PASS":
        raise SystemExit("Blocked: acquire and validate data first")
    out=build(pd.read_csv(src)); dest=CACHE/"model_matrix.csv"; out.to_csv(dest,index=False)
    meta={"rows":len(out),"first_date":out.date.min().strftime("%Y-%m-%d"),"last_date":out.date.max().strftime("%Y-%m-%d"),"file":str(dest.relative_to(ROOT))}
    (ROOT/"reports"/"feature_matrix.json").write_text(json.dumps(meta,indent=2)); print(json.dumps(meta))
if __name__=="__main__": main()
