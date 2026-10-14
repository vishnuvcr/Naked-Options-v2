"""Run preregistered chronological NIFTY forecast comparisons."""
import argparse, json, warnings
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, log_loss
from models import regression_models, classification_models
from sequence_models import sequence_models
from forecast_metrics import regmetrics, clsmetrics, hac_test, block_ci, holm

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/"data"/"cache"; REPORT=ROOT/"reports"
SEED=20261014
FEATURE_PREFIX=("ret_","mom_","vol_","absret_","ext_")
BASE_FEATURES={"log_close","intraday_return","range","gap","log_volume","rsi_14"}

def baseline(task,h,rows,base_rate):
    if task=="return": return np.zeros(len(rows))
    if task=="level": return pd.to_numeric(rows["log_close"]).to_numpy(float)
    if task=="volatility":
        scale=0.79788456 if h==1 else 1.0
        return pd.to_numeric(rows["vol_20"]).to_numpy(float)*scale
    return np.full(len(rows),np.clip(base_rate,1e-5,1-1e-5))

def prob1(model,x):
    prob=model.predict_proba(x)
    classes=list(model.classes_)
    if 1 not in classes: return np.zeros(len(x))
    return prob[:,classes.index(1)]

def append_error(label,exc):
    p=ROOT/"research"/"ERROR_LOG.md"
    row=f"| ERR-RUN | {datetime.now(timezone.utc).date()} | 5 | MEDIUM | {label}: {type(exc).__name__} | Fit/runtime failure | Recorded in reports/experiment_errors.csv; continue other experiments | pending |\n"
    with p.open("a",encoding="utf-8") as f: f.write(row)

def cv_score(model,X,y,origin,h,kind):
    splitter=TimeSeriesSplit(n_splits=2)
    scores=[]
    for tr,va in splitter.split(X):
        train=tr[origin[tr]+h<=origin[va[0]]]
        if len(train)<100: continue
        if kind=="cls" and len(np.unique(y[train]))<2: continue
        est=clone(model)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            est.fit(X[train],y[train])
        if kind=="reg":
            pred=est.predict(X[va]); scores.append(mean_absolute_error(y[va],pred))
        else:
            p=np.clip(prob1(est,X[va]),1e-6,1-1e-6)
            scores.append(log_loss(y[va],np.c_[1-p,p],labels=[0,1]))
    return float(np.mean(scores)) if scores else None

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--features",choices=["technical","global"],default="global")
    args=parser.parse_args()
    source=CACHE/"model_matrix.csv"
    if not source.exists(): raise SystemExit("Blocked: build validated feature matrix first")
    df=pd.read_csv(source)
    cols=[c for c in df.columns if c in BASE_FEATURES or c.startswith(FEATURE_PREFIX)]
    if args.features == "technical": cols=[c for c in cols if not c.startswith("ext_")]
    elif not any(c.startswith("ext_") for c in cols):
        REPORT.mkdir(parents=True,exist_ok=True)
        (REPORT/"experiment_run_global.json").write_text(json.dumps({"status":"BLOCKED_NO_GLOBAL_FEATURES","reason":"No validated auxiliary daily sources were available","features":[]},indent=2))
        pd.DataFrame().to_csv(REPORT/"metrics_global.csv",index=False)
        pd.DataFrame().to_csv(REPORT/"predictions_global.csv",index=False)
        pd.DataFrame().to_csv(REPORT/"experiment_errors_global.csv",index=False)
        print("BLOCKED: no verified global auxiliary features available")
        return 0
    if len(cols)<5: raise SystemExit("Blocked: too few recognized lagged feature columns")
    regmodels=regression_models(); clsmodels=classification_models()
    seqstatus={"status":"NOT_REQUESTED","reason":"Sequence estimators are run only in the technical-only ablation"}
    if args.features=="technical":
        sr,sc=sequence_models()
        for model in list(sr.values())+list(sc.values()): model.set_params(epochs=3)
        if len(df)<1000:
            seqstatus={"status":"BLOCKED_SAMPLE_SIZE","rows":len(df),"minimum_rows":1000}
        elif not sr:
            seqstatus={"status":"BLOCKED_NO_TORCH","reason":"PyTorch is not installed in this workflow"}
        else:
            regmodels.update(sr); clsmodels.update(sc)
            seqstatus={"status":"PASS","regression_models":list(sr),"classification_models":list(sc),"epochs":3}
    REPORT.mkdir(parents=True,exist_ok=True)
    (REPORT/"sequence_model_status.json").write_text(json.dumps(seqstatus,indent=2))
    tasks=[("return","target_return"),("level","target_log_close"),("volatility","target_future_vol"),
           ("direction","target_direction"),("vol_expansion","target_vol_expansion")]
    metric_rows=[]; pred_rows=[]; err_rows=[]
    for task,prefix in tasks:
      kind="cls" if task in ("direction","vol_expansion") else "reg"
      registry=clsmodels if kind=="cls" else regmodels
      for h in (1,5,20):
        target=f"{prefix}_{h}"
        if target not in df: continue
        cut=int(len(df)*.8)
        usable=df[df[target].notna()].copy()
        dev=usable[usable.origin_i<cut-h].copy()
        test=usable[usable.origin_i>=cut].copy()
        if len(dev)<300 or len(test)<30:
            err_rows.append({"task":task,"horizon":h,"model":"ALL","status":"BLOCKED","reason":f"too few rows: dev={len(dev)}, test={len(test)}"})
            continue
        Xd=dev[cols].to_numpy(float); yd=pd.to_numeric(dev[target]).to_numpy(float)
        Xt=test[cols].to_numpy(float); yt=pd.to_numeric(test[target]).to_numpy(float)
        seqcols=[f"ret_{k}" for k in range(60,-1,-1) if f"ret_{k}" in df.columns]
        Xds=dev[seqcols].to_numpy(float)[:,:,None] if len(seqcols)>=40 else Xd
        Xts=test[seqcols].to_numpy(float)[:,:,None] if len(seqcols)>=40 else Xt
        origins=dev.origin_i.to_numpy(int)
        if kind=="cls":
            yd=yd.astype(int); yt=yt.astype(int)
            if len(np.unique(yd))<2:
                err_rows.append({"task":task,"horizon":h,"model":"ALL","status":"BLOCKED","reason":"development target contains one class"})
                continue
        base_rate=float(np.mean(yd)) if kind=="cls" else 0.0
        b=baseline(task,h,test,base_rate)
        scored=[]
        for name,proto in registry.items():
            row={"task":task,"horizon":h,"model":name,"n_dev":len(dev),"n_test":len(test),"status":"PENDING"}
            if name.startswith("seq_") and not ((task=="return" and h==1) or (task=="direction" and h==1)):
                row.update({"status":"BLOCKED_COMPUTE_BUDGET","reason":"Sequence models restricted to next-session return/direction; other target/horizon combinations are not run under the preset compute budget."})
                metric_rows.append(row)
                continue
            try:
                is_seq=name.startswith("seq_")
                Xfit,Xeval=(Xds,Xts) if is_seq else (Xd,Xt)
                row["validation_score"]=cv_score(proto,Xfit,yd,origins,h,kind)
                row["status"]="PASS" if row["validation_score"] is not None else "BLOCKED"
                if row["status"]=="PASS": scored.append((row["validation_score"],name,proto))
            except Exception as e:
                row.update({"status":"FAIL","error":f"{type(e).__name__}: {str(e)[:180]}"})
                err_rows.append({"task":task,"horizon":h,"model":name,"status":"FAIL","reason":row["error"]})
                append_error(f"{task}/h{h}/{name}",e)
            metric_rows.append(row)
        if not scored: continue
        winner=min(scored,key=lambda z:z[0])[1]
        # Rebuild the feature tensor for each estimator: sequence candidates take 3-D
        # windows, while sklearn tabular models must always receive 2-D matrices.
        for score,name,proto in scored:
            try:
                is_seq=name.startswith("seq_")
                Xfit,Xeval=(Xds,Xts) if is_seq else (Xd,Xt)
                est=clone(proto)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore"); est.fit(Xfit,yd)
                if kind=="reg":
                    phat=np.asarray(est.predict(Xeval),float)
                    if task=="volatility": phat=np.maximum(phat,1e-8)
                    actual_eval,pred_eval,base_eval=yt,phat,b
                    if task=="level":
                        actual_eval,pred_eval,base_eval=np.exp(yt),np.exp(phat),np.exp(b)
                        met=regmetrics(actual_eval,pred_eval,base_eval)
                        met["log_scale_mae"]=float(np.mean(abs(yt-phat)))
                        met["log_scale_rmse"]=float(np.sqrt(np.mean((yt-phat)**2)))
                    else:
                        met=regmetrics(yt,phat,b)
                    if task=="return":
                        meanb=np.full(len(yt),float(np.mean(yd)))
                        mse=float(np.mean((yt-phat)**2)); mm=float(np.mean((yt-meanb)**2))
                        met["mae_bps"]=met["mae"]*10000
                        met["rmse_bps"]=met["rmse"]*10000
                        met["mse_skill_vs_historical_mean"]=float(1-mse/mm) if mm>0 else None
                    if task=="volatility":
                        av=np.maximum(yt,1e-8)**2; pv=np.maximum(phat,1e-8)**2; bv=np.maximum(b,1e-8)**2
                        ql=np.log(pv)+av/pv; qlb=np.log(bv)+av/bv
                        met["qlike"]=float(np.mean(ql)); met["qlike_baseline"]=float(np.mean(qlb))
                        met["qlike_skill_vs_baseline"]=float(1-np.mean(ql)/np.mean(qlb)) if np.mean(qlb)>0 else None
                        loss=ql-qlb
                    else:
                        loss=(actual_eval-pred_eval)**2-(actual_eval-base_eval)**2
                    ci=block_ci(loss,h,SEED+h); tst=hac_test(loss,h-1)
                    common={"mae_baseline":float(np.mean(abs(actual_eval-base_eval))),"ci_loss_diff_low":ci[0],"ci_loss_diff_high":ci[1],**tst}
                    predprob=None
                else:
                    phat=np.clip(prob1(est,Xeval),1e-6,1-1e-6)
                    actual_eval,pred_eval,base_eval=yt,phat,b
                    met=clsmetrics(yt,phat,b)
                    loss=-(yt*np.log(phat)+(1-yt)*np.log(1-phat))+ (yt*np.log(np.clip(b,1e-6,1-1e-6))+(1-yt)*np.log(np.clip(1-b,1e-6,1-1e-6)))
                    ci=block_ci(loss,h,SEED+h); tst=hac_test(loss,h-1)
                    common={"ci_loss_diff_low":ci[0],"ci_loss_diff_high":ci[1],**tst}
                    predprob=phat
                metric_rows.append({"task":task,"horizon":h,"model":name,"status":"OOS_EVALUATED",
                    "selected_by_validation":name==winner,"validation_score":score,**met,**common})
                for j,(_,tr) in enumerate(test.iterrows()):
                    pr={"origin_date":pd.to_datetime(tr.date).date().isoformat(),"target_date":tr.get(f"target_date_{h}"),
                        "task":task,"horizon":h,"model":name,"actual":float(actual_eval[j]),"baseline":float(base_eval[j]),
                        "prediction":float(pred_eval[j]),"selected_by_validation":name==winner}
                    if predprob is not None: pr["probability_positive"]=float(phat[j])
                    pred_rows.append(pr)
            except Exception as e:
                err_rows.append({"task":task,"horizon":h,"model":name,"status":"FAIL_OOS","reason":f"{type(e).__name__}: {str(e)[:180]}"})
                append_error(f"OOS {task}/h{h}/{name}",e)
    # Holm-adjust paired-loss p-values within each task/horizon group.
    metrics=pd.DataFrame(metric_rows)
    if not metrics.empty:
        if "p_value" not in metrics: metrics["p_value"]=np.nan
        if "p_holm" not in metrics: metrics["p_holm"]=np.nan
        for _,idx in metrics[metrics.status.eq("OOS_EVALUATED")].groupby(["task","horizon"]).groups.items():
            ps=metrics.loc[idx,"p_value"].tolist()
            adj=holm(ps)
            metrics.loc[idx,"p_holm"]=adj
    REPORT.mkdir(parents=True,exist_ok=True)
    metrics.to_csv(REPORT/f"metrics_{args.features}.csv",index=False)
    pd.DataFrame(pred_rows).to_csv(REPORT/f"predictions_{args.features}.csv",index=False)
    pd.DataFrame(err_rows).to_csv(REPORT/f"experiment_errors_{args.features}.csv",index=False)
    metadata={"research_version":"NIFTY-PRED-1.0","seed":SEED,"models_regression":list(regmodels),
      "models_classification":list(clsmodels),"sequence_status":seqstatus,"features":cols,"experiments":len(metric_rows),
      "oos_predictions":len(pred_rows),"status":"COMPLETE" if pred_rows else "BLOCKED_NO_OOS_OUTPUT",
      "selection_rule":"validation CV loss only; final holdout used for one-time evaluation and no hyperparameter tuning"}
    (REPORT/f"experiment_run_{args.features}.json").write_text(json.dumps(metadata,indent=2))
    print(json.dumps(metadata,indent=2))
    return 0 if pred_rows else 3
if __name__=="__main__": raise SystemExit(main())
