#!/usr/bin/env python3
"""Bounded leakage-aware NIFTY hypotheses using cached OHLC; missing datasets are marked blocked."""
import json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, matthews_corrcoef, brier_score_loss, log_loss
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/cache/nifty-prediction/nifty50_daily.csv"
OUT=ROOT/"reports/nifty-prediction/new_hypothesis_experiments.json"
def model():
 return make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=2000,class_weight="balanced",random_state=41))
def score(y,p):
 z=(p>=.5).astype(int)
 return {"n":int(len(y)),"accuracy":float(accuracy_score(y,z)),"balanced_accuracy":float(balanced_accuracy_score(y,z)),"mcc":float(matthews_corrcoef(y,z)),"brier":float(brier_score_loss(y,p)),"log_loss":float(log_loss(y,np.clip(p,1e-6,1-1e-6),labels=[0,1]))}
def main():
 d=pd.read_csv(DATA); d.columns=[str(c).strip().lower().replace(" ","_") for c in d.columns]
 dc=next(c for c in d.columns if c in ("date","datetime","timestamp")); d["date"]=pd.to_datetime(d[dc],errors="coerce")
 for c in ("open","high","low","close"): d[c]=pd.to_numeric(d[c],errors="coerce")
 d=d.dropna(subset=["date","open","high","low","close"]).sort_values("date").drop_duplicates("date").reset_index(drop=True)
 r=d.close.pct_change(); d["ret1"]=r
 for h in (2,3,5,10,20,40): d[f"mom{h}"]=d.close.pct_change(h)
 for h in (5,10,20,40):
  d[f"vol{h}"]=r.rolling(h).std(); d[f"ma_gap{h}"]=d.close/d.close.rolling(h).mean()-1
 d["range_pct"]=(d.high-d.low)/d.close; d["gap_pct"]=d.open/d.close.shift(1)-1
 d["close_location"]=(d.close-d.low)/(d.high-d.low).replace(0,np.nan)
 d["vol_regime"]=(d.vol20>d.vol20.expanding(min_periods=100).median()).astype(int)
 d["target_return"]=d.close.shift(-1)/d.close-1; d["y"]=(d.target_return>0).astype(int); d.loc[d.target_return.isna(),"y"]=np.nan
 feats=["ret1","mom2","mom3","mom5","mom10","mom20","mom40","vol5","vol10","vol20","vol40","ma_gap5","ma_gap10","ma_gap20","ma_gap40","range_pct","gap_pct","close_location"]
 d=d.dropna(subset=feats+["y"]).reset_index(drop=True); n=len(d); a=int(n*.60); b=int(n*.75)
 tr,cal,te=d.iloc[:a],d.iloc[a:b],d.iloc[b:]; ytr=tr.y.astype(int); yt=te.y.astype(int)
 if len(te)<150: raise ValueError(f"Insufficient test sample: {len(te)}")
 m=model(); m.fit(tr[feats],ytr); pc=m.predict_proba(cal[feats])[:,1]; p=m.predict_proba(te[feats])[:,1]
 results={"train_majority_baseline":score(yt,np.full(len(te),ytr.mean())),"logistic_full_features":score(yt,p)}
 # Volatility-regime specialists: only fit on training rows; fall back to global model if subgroup is small.
 rp=[]
 for _,row in te.iterrows():
  sub=tr[tr.vol_regime==row.vol_regime]
  if len(sub)<150 or sub.y.nunique()<2: rp.append(float(p[len(rp)]))
  else:
   sm=model(); sm.fit(sub[feats],sub.y.astype(int)); rp.append(float(sm.predict_proba(row[feats].to_frame().T)[0,1]))
 results["volatility_regime_specialists"]=score(yt,np.array(rp))
 core=[x for x in feats if x not in ("range_pct","gap_pct","close_location")]
 cm=model(); cm.fit(tr[core],ytr); results["core_ohlc_features_ablation"]=score(yt,cm.predict_proba(te[core])[:,1])
 horizons={}
 for h in (1,3,5):
  q=d.copy(); q["yh"]=(q.close.shift(-h)/q.close-1>0).astype(int); q.loc[q.close.shift(-h).isna(),"yh"]=np.nan
  q=q.dropna(subset=feats+["yh"]).reset_index(drop=True); cut=int(len(q)*.75); x,y=q.iloc[:cut],q.iloc[cut:]
  hm=model(); hm.fit(x[feats],y.yh.astype(int)); horizons[f"{h}_session"]=score(y.yh.astype(int),hm.predict_proba(y[feats])[:,1])
 conf=np.maximum(pc,1-pc); threshold=float(np.quantile(conf,.80)); mask=np.maximum(p,1-p)>=threshold
 selective={"threshold_from_calibration":threshold,"coverage":float(mask.mean()),"n_selected":int(mask.sum())}
 if mask.sum()>=30: selective.update(score(yt.to_numpy()[mask],p[mask]))
 report={"study":"Bounded new NIFTY prediction hypotheses using daily OHLC","status":"COMPUTED_WITH_EXTERNAL_DATA_HYPOTHESES_BLOCKED","source_rows":n,"source_first_date":str(d.date.iloc[0].date()),"source_last_date":str(d.date.iloc[-1].date()),"split":{"method":"chronological 60/15/25 train/calibration/test","train":len(tr),"calibration":len(cal),"test":len(te),"test_first_date":str(te.date.iloc[0].date()),"test_last_date":str(te.date.iloc[-1].date())},"target":"next-session close-to-close direction; zero classified DOWN","results":results,"multi_horizon":horizons,"selective_prediction":selective,"blocked":{"global_lead_lag":"No synchronized point-in-time global index/FX/crude/gold inputs.","breadth_disagreement":"No point-in-time constituent and sector breadth history.","options_implied_expectations":"No timestamped historical option-chain, IV or OI snapshots.","opening_pressure":"No intraday bars or defined intraday forecast timestamp.","event_aware":"No point-in-time event calendar/history.","residual_correction":"Not run: chronological out-of-fold residual targets and incremental-value protocol must be implemented first."},"limitations":["Third-party daily OHLC is not exchange-certified.","Simple volatility regime proxy is not a validated latent-state model.","Single chronological screen is not untouched confirmation; no statistical-significance claim.","No options premium, execution or transaction-cost evaluation."]}
 OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,indent=2)+"\n"); print(json.dumps(report,indent=2))
if __name__=="__main__": main()
