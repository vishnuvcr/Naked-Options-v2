"""Recompute the 20-session volatility-expansion logistic result on the frozen split."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, brier_score_loss,
                             log_loss, precision_score, recall_score, confusion_matrix)

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data"/"cache"
REPORT=ROOT/"reports"
H=20
SEED=20261014

def score(y,p,threshold=.5):
    y=np.asarray(y,dtype=int); p=np.clip(np.asarray(p,float),1e-6,1-1e-6)
    pred=(p>=threshold).astype(int); cm=confusion_matrix(y,pred,labels=[0,1]); tn,fp,fn,tp=map(int,cm.ravel())
    prevalence=float(y.mean()); base=np.full(len(y),prevalence)
    bs=float(brier_score_loss(y,p)); bsb=float(brier_score_loss(y,base))
    return {"n":len(y),"positive_rate":prevalence,"accuracy_at_0_5":float(accuracy_score(y,pred)),
      "balanced_accuracy_at_0_5":float(balanced_accuracy_score(y,pred)),
      "precision_at_0_5":float(precision_score(y,pred,zero_division=0)),
      "recall_at_0_5":float(recall_score(y,pred,zero_division=0)),
      "specificity_at_0_5":float(tn/(tn+fp)) if tn+fp else None,
      "confusion_matrix":{"tn":tn,"fp":fp,"fn":fn,"tp":tp},
      "brier":bs,"base_rate_brier":bsb,"brier_skill_vs_holdout_prevalence":float(1-bs/bsb) if bsb else None,
      "log_loss":float(log_loss(y,p,labels=[0,1])),
      "base_rate_log_loss":float(log_loss(y,base,labels=[0,1]))}

def main():
    path=CACHE/"model_matrix.csv"
    if not path.exists(): raise SystemExit("BLOCKED: model_matrix.csv absent")
    df=pd.read_csv(path)
    target="target_vol_expansion_20"
    features=[c for c in df.columns if c in {"log_close","intraday_return","range","gap","log_volume","rsi_14"} or c.startswith(("ret_","mom_","vol_","absret_"))]
    cut=int(len(df)*.8)
    usable=df[df[target].notna()].copy()
    dev=usable[usable.origin_i < cut-H].copy()
    test=usable[usable.origin_i >= cut].copy()
    if len(dev)<300 or len(test)<30: raise SystemExit(f"BLOCKED: insufficient split sizes dev={len(dev)} test={len(test)}")
    Xd=dev[features].to_numpy(float); Xt=test[features].to_numpy(float)
    yd=dev[target].astype(int).to_numpy(); yt=test[target].astype(int).to_numpy()
    if len(np.unique(yd))<2 or len(np.unique(yt))<2: raise SystemExit("BLOCKED: only one class in train or holdout")
    model=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),
       LogisticRegression(C=.1,max_iter=800,class_weight="balanced",random_state=SEED))
    model.fit(Xd,yd); p=model.predict_proba(Xt)[:,list(model[-1].classes_).index(1)]
    overall=score(yt,p)
    # Equal-width calibration bins are descriptive; empty bins are omitted.
    bins=np.linspace(0,1,11); cal=[]
    for i in range(10):
        mask=(p>=bins[i]) & ((p<bins[i+1]) if i<9 else (p<=bins[i+1]))
        if mask.any(): cal.append({"bin_low":float(bins[i]),"bin_high":float(bins[i+1]),"n":int(mask.sum()),"mean_probability":float(p[mask].mean()),"observed_rate":float(yt[mask].mean())})
    # Training-only 75th percentile for the origin-volatility regime threshold.
    vol=pd.to_numeric(dev.vol_20,errors="coerce")
    threshold=float(vol.quantile(.75))
    regimes=[]
    for name,mask in [("high_volatility",pd.to_numeric(test.vol_20,errors="coerce").to_numpy()>=threshold),
                      ("not_high_volatility",pd.to_numeric(test.vol_20,errors="coerce").to_numpy()<threshold)]:
        if mask.sum()>=20 and len(np.unique(yt[mask]))==2: regimes.append({"regime":name,"n":int(mask.sum()),**score(yt[mask],p[mask])})
    yearly=[]
    years=pd.to_datetime(test.date).dt.year.to_numpy()
    for year in sorted(set(years)):
        m=years==year
        if m.sum()>=20 and len(np.unique(yt[m]))==2: yearly.append({"year":int(year),**score(yt[m],p[m])})
    report={"status":"DIAGNOSTICS_COMPLETE","method":"re-fit fixed logistic specification; no hyperparameter tuning; chronological holdout unchanged",
      "target_definition":"sample standard deviation of next 20 daily log returns > trailing 20-session standard deviation at forecast origin",
      "feature_set":"technical only; same feature prefixes as experiment runner","model":"median imputation + standardization + LogisticRegression(C=0.1,class_weight='balanced',max_iter=800,random_state=20261014)",
      "split":{"n_total_rows":len(df),"cut_origin_i":cut,"development_n":len(dev),"holdout_n":len(test),"development_last_origin":str(dev.date.iloc[-1]),"holdout_first_origin":str(test.date.iloc[0]),"holdout_last_origin":str(test.date.iloc[-1])},
      "overall":overall,"calibration_bins":cal,"training_only_volatility_75th_percentile":threshold,"regimes_descriptive":regimes,"yearly_descriptive":yearly,
      "limitations":["This is a focused refit, not a bit-for-bit reproduction of model-selection predictions; label differences and protocol details must be checked.","20-session labels overlap, so subgroup results are descriptive and dependent.","No independent new holdout, option-chain data, transaction costs, slippage or trading strategy test."]}
    REPORT.mkdir(parents=True,exist_ok=True); out=REPORT/"vol_expansion_20_validation.json"; out.write_text(json.dumps(report,indent=2))
    print(json.dumps({"status":report["status"],"overall":overall,"report":str(out)},indent=2))
if __name__=="__main__": main()
