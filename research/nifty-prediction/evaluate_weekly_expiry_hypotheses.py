#!/usr/bin/env python3
"""Bounded weekly-expiry NIFTY prediction hypotheses; daily OHLC-only, leakage-aware.
External-data hypotheses are explicitly blocked until timestamped history is available.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, log_loss, matthews_corrcoef

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/cache/nifty-prediction/nifty50_daily.csv"
OUT=ROOT/"reports/nifty-prediction/weekly_expiry_hypotheses.json"
SEED=20261025

def pipe():
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(C=.5,max_iter=2000,class_weight="balanced",random_state=SEED))

def score(name,y,p):
    p=np.clip(np.asarray(p,dtype=float),1e-6,1-1e-6); y=np.asarray(y,dtype=int); pred=(p>=.5).astype(int)
    return {"method":name,"n":int(len(y)),"accuracy":float(accuracy_score(y,pred)),"balanced_accuracy":float(balanced_accuracy_score(y,pred)),"mcc":float(matthews_corrcoef(y,pred)),"brier":float(brier_score_loss(y,p)),"log_loss":float(log_loss(y,p,labels=[0,1]))}

def load():
    d=pd.read_csv(DATA); d.columns=[str(c).strip().lower().replace(" ","_") for c in d.columns]
    dc=next(c for c in d if c in ("date","datetime","timestamp"))
    d["date"]=pd.to_datetime(d[dc],errors="coerce")
    for c in ("open","high","low","close"): d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.dropna(subset=["date","open","high","low","close"]).sort_values("date").drop_duplicates("date").reset_index(drop=True)
    if len(d)<1000: raise ValueError("Insufficient daily data")
    if ((d.high<d[["open","low","close"]].max(axis=1))|(d.low>d[["open","high","close"]].min(axis=1))).any(): raise ValueError("Invalid OHLC")
    return d

def main():
    d=load(); d["ret1"]=d.close.pct_change()
    for h in (2,3,5,10,20,40,60): d[f"mom{h}"]=d.close.pct_change(h)
    for h in (5,10,20,40):
        d[f"vol{h}"]=d.ret1.rolling(h).std()
        d[f"ma{h}"]=d.close/d.close.rolling(h).mean()-1
    d["range_pct"]=(d.high-d.low)/d.close
    d["gap_pct"]=d.open/d.close.shift(1)-1
    d["close_location"]=(d.close-d.low)/(d.high-d.low).replace(0,np.nan)
    feats=[c for c in d if c.startswith(("mom","vol","ma")) or c in ("ret1","range_pct","gap_pct","close_location")]
    # Explicit weekday approximation; official holiday-adjusted expiry calendar is still a blocker.
    d["expiry_wday"]=np.where(d.date<pd.Timestamp("2025-09-01"),3,1)
    idx=[i for i in range(len(d)) if d.loc[i,"date"].weekday()==d.loc[i,"expiry_wday"]]
    rows=[]
    for j in range(1,len(idx)):
        a,b=idx[j-1],idx[j]
        if a<60: continue
        r={"cutoff_date":d.loc[a,"date"].date().isoformat(),"expiry_date":d.loc[b,"date"].date().isoformat(),"target_return":float(d.loc[b,"close"]/d.loc[a,"close"]-1),"y":int(d.loc[b,"close"]>d.loc[a,"close"])}
        r.update({f:d.loc[a,f] for f in feats})
        # State known at cutoff: vol20 vs trailing 100-observation median; shift avoids current-inclusive threshold.
        trailing=d.vol20.iloc[:a].dropna()
        r["high_vol"]=int(pd.notna(d.loc[a,"vol20"]) and len(trailing)>=50 and d.loc[a,"vol20"]>trailing.iloc[-100:].median())
        r["transition"]=int(pd.notna(d.loc[a,"vol20"]) and len(trailing)>=30 and d.loc[a,"vol20"]>2*trailing.iloc[-30:].median())
        rows.append(r)
    f=pd.DataFrame(rows).dropna(subset=feats+["y"]).reset_index(drop=True)
    if len(f)<300: raise ValueError(f"Too few expiry examples: {len(f)}")
    y=f.y.to_numpy(int); X=f[feats].replace([np.inf,-np.inf],np.nan)
    # 60/15/25 chronological train/calibration/test split, matching hypothesis protocol.
    a=int(len(f)*.60); b=int(len(f)*.75)
    if b-a<30 or len(f)-b<50: raise ValueError("Insufficient train/calibration/test sizes")
    tr,cal,te=X.iloc[:a],X.iloc[a:b],X.iloc[b:]; yt=y[b:]
    train_rate=float(y[:a].mean()); results=[score("training_majority",yt,np.full(len(yt),train_rate))]
    # Previous expiry direction baseline, known at cutoff.
    prev=(f.y.shift(1).iloc[b:].fillna(train_rate)>=.5).astype(int).to_numpy()
    results.append(score("previous_expiry_direction",yt,np.where(prev==1,.55,.45)))
    # Base logistic and shallow tree.
    base=pipe().fit(tr,y[:a]); pbase=base.predict_proba(te)[:,1]
    results.append(score("regularized_logistic",yt,pbase))
    tree=HistGradientBoostingClassifier(max_iter=100,learning_rate=.04,max_leaf_nodes=7,l2_regularization=2,random_state=SEED).fit(SimpleImputer(strategy="median").fit_transform(tr),y[:a])
    imp=SimpleImputer(strategy="median").fit(tr); ptree=tree.predict_proba(imp.transform(te))[:,1]
    results.append(score("hist_gradient_boosting",yt,ptree))
    # Regime specialists: use high/low volatility state determined at cutoff, train on matching regime only if support adequate.
    regime_p=[]
    for ix in range(b,len(f)):
        state=int(f.high_vol.iloc[ix]); mask=(f.high_vol.iloc[:ix].to_numpy()==state)
        if mask.sum()>=100 and len(np.unique(y[:ix][mask]))==2:
            m=pipe().fit(X.iloc[:ix].loc[mask],y[:ix][mask]); regime_p.append(float(m.predict_proba(X.iloc[[ix]])[0,1]))
        else:
            m=pipe().fit(X.iloc[:ix],y[:ix]); regime_p.append(float(m.predict_proba(X.iloc[[ix]])[0,1]))
    results.append(score("volatility_regime_specialists_fallback_global",yt,regime_p))
    # Change-point/transition awareness: compare confidence filtering on a past-only volatility shock flag.
    trans=f.transition.iloc[b:].to_numpy(dtype=bool)
    results.append(score("logistic_on_transition_subset",yt[trans],pbase[trans]) if trans.sum()>=20 else {"method":"logistic_on_transition_subset","status":"BLOCKED_INSUFFICIENT_TRANSITIONS","n":int(trans.sum())})
    # Calibrated selective output: calibration-only threshold; report coverage and quality, not just accuracy.
    mc=pipe().fit(tr,y[:a]); pcal=mc.predict_proba(cal)[:,1]; psel=mc.predict_proba(te)[:,1]
    confcal=np.abs(pcal-.5); threshold=float(np.quantile(confcal,.80)); keep=np.abs(psel-.5)>=threshold
    selective=score("selective_logistic_calibration_threshold",yt[keep],psel[keep]) if keep.sum()>=20 else {"method":"selective_logistic_calibration_threshold","status":"BLOCKED_INSUFFICIENT_COVERAGE","n":int(keep.sum())}
    selective["coverage"]=float(keep.mean()); selective["threshold_abs_probability_from_0_5"]=threshold
    results.append(selective)
    # Multi-horizon agreement: at cutoff predict next expiry and second-next expiry; second horizon evaluated separately.
    # Horizon target built from expiry-close series and same past-only features.
    multi={}
    for horizon in (1,2,3):
        yh=[]; Xh=[]; dates=[]
        for j in range(len(idx)-horizon):
            cut=idx[j]; end=idx[j+horizon]
            if cut<60: continue
            row=d.loc[cut,feats]
            if row.isna().any(): continue
            Xh.append(row); yh.append(int(d.loc[end,"close"]>d.loc[cut,"close"])); dates.append(d.loc[cut,"date"].date().isoformat())
        Xh=pd.DataFrame(Xh,columns=feats); yh=np.asarray(yh,int); split=int(len(yh)*.75)
        if split>=100 and len(yh)-split>=30:
            m=pipe().fit(Xh.iloc[:split],yh[:split]); ph=m.predict_proba(Xh.iloc[split:])[:,1]
            multi[f"{horizon}_expiry_horizon"]={"n_test":int(len(yh)-split),"accuracy":float(accuracy_score(yh[split:],ph>=.5)),"balanced_accuracy":float(balanced_accuracy_score(yh[split:],ph>=.5)),"brier":float(brier_score_loss(yh[split:],ph))}
    # Out-of-fold residual correction: chronological expanding base predictions on training segment only.
    # Fit second-stage correction on prior training predictions/errors, then score test without test-label fitting.
    oof_p=[]; oof_y=[]; oof_x=[]
    warm=max(100,int(a*.35))
    for i in range(warm,a):
        m=pipe().fit(X.iloc[:i],y[:i]); pp=float(m.predict_proba(X.iloc[[i]])[0,1])
        oof_p.append(pp); oof_y.append(int(y[i])); oof_x.append([pp, float(f.high_vol.iloc[i]), float(f.transition.iloc[i])])
    residual_status="BLOCKED_TOO_FEW_OOF_ROWS"
    residual_result=None
    if len(oof_y)>=80:
        # Second stage learns correction of baseline probability error using only historical OOF scores.
        corr=LogisticRegression(C=.5,max_iter=1000,random_state=SEED).fit(np.asarray(oof_x),np.asarray(oof_y))
        test_x=np.column_stack([pbase,f.high_vol.iloc[b:].to_numpy(),f.transition.iloc[b:].to_numpy()])
        pcorr=corr.predict_proba(test_x)[:,1]
        residual_result=score("out_of_fold_residual_probability_correction",yt,pcorr); residual_status="SCREENED_NOT_CONFIRMATORY"
        results.append(residual_result)
    # Methods requiring external point-in-time data remain blocked rather than fabricated.
    blocked={
      "global_to_india_lead_lag":"BLOCKED: point-in-time global index, FX, crude and gold history not joined",
      "breadth_disagreement":"BLOCKED: point-in-time constituent/sector breadth and historical constituents unavailable",
      "options_implied_expectations":"BLOCKED: timestamped historical option-chain IV/skew/OI not yet validated",
      "opening_pressure":"BLOCKED: intraday bars and fixed intraday cutoff not integrated",
      "event_aware_calendar":"BLOCKED: point-in-time event calendar/history not integrated"
    }
    payload={"study":"NIFTY 50 weekly-expiry prediction hypotheses","status":"SCREENING_COMPLETE_WITH_DATA_BLOCKERS","input_sha256":hashlib.sha256(DATA.read_bytes()).hexdigest(),"input_rows":int(len(d)),"examples":int(len(f)),"first_cutoff":f.cutoff_date.min(),"last_expiry":f.expiry_date.max(),"expiry_calendar":{"rule":"Thursday before 2025-09-01; Tuesday thereafter","official_holiday_adjusted_calendar_verified":False},"split":{"method":"chronological 60/15/25 train/calibration/test","train":a,"calibration":b-a,"test":len(f)-b,"test_start_cutoff":f.cutoff_date.iloc[b],"test_end_expiry":f.expiry_date.iloc[-1]},"features":feats,"results":results,"multi_horizon":multi,"residual_correction_status":residual_status,"blocked_hypotheses":blocked,"limitations":["Approximate expiry weekday rule may mislabel holiday-adjusted expiries.","Repeated research on the existing history is screening, not untouched confirmation.","No external data feature is fabricated.","Spot direction is not option premium direction or profitability."]}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"report":str(OUT),"examples":len(f),"results":results,"multi_horizon":multi,"blocked":blocked},indent=2))
if __name__=="__main__": main()
