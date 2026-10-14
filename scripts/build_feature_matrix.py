"""Build lagged NIFTY predictors and strictly future targets."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data"/"cache"
def build(df):
    df=df.sort_values("date").copy().reset_index(drop=True)
    df["date"]=pd.to_datetime(df["date"],errors="raise")
    c=pd.to_numeric(df["close"],errors="raise"); r=np.log(c).diff()
    x=pd.DataFrame(index=df.index)
    x["log_close"]=np.log(c); x["intraday_return"]=np.log(df["close"]/df["open"])
    x["range"]=np.log(df["high"]/df["low"]); x["gap"]=np.log(df["open"]/df["close"].shift(1))
    x["log_volume"]=np.log1p(pd.to_numeric(df.volume,errors="coerce").clip(lower=0))
    for k in range(61): x[f"ret_{k}"]=r.shift(k)
    for w in (5,10,14,20,40,60):
        x[f"mom_{w}"]=np.log(c)-np.log(c).shift(w)
        x[f"vol_{w}"]=r.rolling(w,min_periods=w).std()
        x[f"absret_{w}"]=r.abs().rolling(w,min_periods=w).mean()
    gain=r.clip(lower=0).rolling(14,min_periods=14).mean()
    loss=-r.clip(upper=0).rolling(14,min_periods=14).mean()
    x["rsi_14"]=100-100/(1+gain/(loss+1e-12))
    # Global close observations are conservatively restricted to an earlier source date.
    extdir=CACHE/"external"
    if extdir.exists():
        left=pd.DataFrame({"nifty_date":df.date})
        for path in sorted(extdir.glob("*.csv")):
            try:
                e=pd.read_csv(path)
                e["date"]=pd.to_datetime(e["date"],errors="coerce")
                e["close"]=pd.to_numeric(e["close"],errors="coerce")
                e=e.dropna(subset=["date","close"]).sort_values("date")
                e["ext_log_close"]=np.log(e.close)
                e["ext_return"]=e.ext_log_close.diff()
                right=e[["date","ext_log_close","ext_return"]].rename(columns={"date":"ext_date"})
                joined=pd.merge_asof(left,right,left_on="nifty_date",right_on="ext_date",direction="backward",allow_exact_matches=False)
                x[f"ext_{path.stem}_log_close"]=joined.ext_log_close.to_numpy()
                x[f"ext_{path.stem}_return"]=joined.ext_return.to_numpy()
            except Exception:
                continue
    out=pd.concat([df[["date","open","high","low","close","volume","source_id"]],x],axis=1)
    out["origin_i"]=np.arange(len(out)); out["daily_log_return"]=r
    for h in (1,5,20):
        y=np.log(c.shift(-h))-np.log(c)
        out[f"target_date_{h}"]=out.date.shift(-h).dt.strftime("%Y-%m-%d")
        out[f"target_return_{h}"]=y
        out[f"target_direction_{h}"]=np.where(y.notna(),(y>0).astype(float),np.nan)
        out[f"target_close_{h}"]=c.shift(-h); out[f"target_log_close_{h}"]=np.log(c.shift(-h))
        fr=pd.concat([r.shift(-k) for k in range(1,h+1)],axis=1)
        if h==1:
            fv=r.shift(-1).abs()
        else:
            # Require a complete forward window; std otherwise skips missing tail returns.
            fv=fr.std(axis=1,ddof=1).where(fr.notna().sum(axis=1)==h)
        out[f"target_future_vol_{h}"]=fv
        out[f"target_vol_expansion_{h}"]=np.where(fv.notna() & x["vol_20"].notna(),(fv>x["vol_20"]).astype(float),np.nan)
    return out.replace([np.inf,-np.inf],np.nan)
def main():
    src=CACHE/"nifty50_daily.csv"; q=ROOT/"reports"/"data_quality.json"
    if not src.exists() or not q.exists() or json.loads(q.read_text()).get("validation")!="PASS":
        raise SystemExit("Blocked: acquire and validate data first")
    out=build(pd.read_csv(src)); dest=CACHE/"model_matrix.csv"; out.to_csv(dest,index=False)
    meta={"rows":len(out),"n_features":int(sum(c not in {"date","source_id"} and not c.startswith("target_") for c in out.columns)),"first_date":out.date.min().strftime("%Y-%m-%d"),"last_date":out.date.max().strftime("%Y-%m-%d"),"file":str(dest.relative_to(ROOT))}
    (ROOT/"reports"/"feature_matrix.json").write_text(json.dumps(meta,indent=2)); print(json.dumps(meta))
if __name__=="__main__": main()
