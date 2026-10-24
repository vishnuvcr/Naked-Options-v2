#!/usr/bin/env python3
"""Compatibility-gated experiments for MAPIE, PySR and tick on the NIFTY target.

Chronological split only. No tuning against the final test set, no agent-generated
labels, and no trading claims. Missing/incompatible optional packages are recorded
as SKIPPED rather than breaking the core benchmark.
"""
from __future__ import annotations
import importlib
import importlib.metadata as md
import json
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/cache/nifty-prediction/nifty50_daily.csv"
OUT=ROOT/"reports/nifty-prediction/optional_model_experiments.json"

def features():
    d=pd.read_csv(DATA)
    d.columns=[str(c).strip().lower().replace(" ","_") for c in d.columns]
    date_col=next(c for c in d.columns if c in ("date","datetime","timestamp"))
    d["date"]=pd.to_datetime(d[date_col],errors="coerce")
    for c in ("open","high","low","close"):
        d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.dropna(subset=["date","open","high","low","close"]).sort_values("date").drop_duplicates("date").reset_index(drop=True)
    close=d.close; ret=close.pct_change()
    X=pd.DataFrame(index=d.index)
    for n in (1,2,3,5,10,20,60): X[f"ret_{n}"]=close.pct_change(n)
    for n in (5,10,20,60):
        X[f"vol_{n}"]=ret.rolling(n).std()
        X[f"ma_gap_{n}"]=close/close.rolling(n).mean()-1
    X["range_pct"]=(d.high-d.low)/close
    X["open_gap"]=d.open/close.shift(1)-1
    y=(close.shift(-1)/close-1>0).astype(int)
    valid=X.notna().all(axis=1)&y.notna()
    X=X.loc[valid].replace([np.inf,-np.inf],np.nan)
    y=y.loc[valid].astype(int)
    dates=d.loc[valid,"date"].dt.strftime("%Y-%m-%d")
    return X,y,dates

def version(name):
    try:return md.version(name)
    except md.PackageNotFoundError:return None

def main():
    X,y,dates=features()
    n=len(y); train_end=int(n*.60); calib_end=int(n*.75)
    # Final 25% is scored once; MAPIE calibration uses the immediately prior chronological block.
    X_train,y_train=X.iloc[:train_end],y.iloc[:train_end]
    X_cal,y_cal=X.iloc[train_end:calib_end],y.iloc[train_end:calib_end]
    X_test,y_test=X.iloc[calib_end:],y.iloc[calib_end:]
    result={"generated_at_utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETED_WITH_OPTIONAL_SKIPS",
      "target":"next-session NIFTY 50 spot direction","rows":n,
      "periods":{"train":[str(dates.iloc[0]),str(dates.iloc[train_end-1])],
        "calibration":[str(dates.iloc[train_end]),str(dates.iloc[calib_end-1])],
        "test":[str(dates.iloc[calib_end]),str(dates.iloc[-1])]},
      "split":"chronological 60% train / 15% calibration / 25% test; final block not used for tuning",
      "experiments":{},"guardrails":["No live orders","No transaction-cost or profitability claims",
      "Optional model failure does not fail the core pipeline","All fitted predictions use lagged daily OHLC features"]}
    # sklearn baseline on the same final block
    model=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=2000,class_weight="balanced",random_state=42))
    model.fit(X_train,y_train); pred=model.predict(X_test)
    result["experiments"]["sklearn_logistic_same_split"]={"status":"COMPUTED","accuracy":float(accuracy_score(y_test,pred)),
      "balanced_accuracy":float(balanced_accuracy_score(y_test,pred)),"n_test":len(y_test)}
    # MAPIE API compatibility: report symbols then use only the installed documented API if available.
    try:
      mapie=importlib.import_module("mapie")
      symbols=[s for s in ("SplitConformalClassifier","MapieClassifier","CrossConformalClassifier") if hasattr(mapie,s)]
      exp={"status":"API_CHECK_ONLY","version":version("mapie"),"top_level_candidate_symbols":symbols}
      # Avoid silently adapting to an unknown API. API mismatch is a recorded outcome.
      if not symbols: exp.update(status="SKIPPED_API_MISMATCH",reason="No recognized classifier entry point in installed MAPIE version.")
      else:
        try:
          from mapie.classification import SplitConformalClassifier
          conformal=SplitConformalClassifier(estimator=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=2000,class_weight="balanced",random_state=42)),confidence_level=0.9)
          conformal.fit(X_train,y_train)
          conformal.conformalize(X_cal,y_cal)
          sets=conformal.predict_set(X_test)
          # MAPIE versions can return ndarray or tuple; record shape only unless known.
          arr=np.asarray(sets[0] if isinstance(sets,tuple) else sets)
          if arr.ndim==2 and arr.shape[0]==len(y_test):
            membership=arr.astype(bool)
            covered=membership[np.arange(len(y_test)),y_test.to_numpy()]
            exp={"status":"COMPUTED","version":version("mapie"),"nominal_coverage":0.9,
              "empirical_coverage":float(np.mean(covered)),"mean_set_size":float(np.mean(membership.sum(axis=1))),
              "singleton_rate":float(np.mean(membership.sum(axis=1)==1)),"n_test":len(y_test),
              "warning":"Market time dependence weakens standard exchangeability guarantees; coverage is descriptive."}
          else: exp.update(status="SKIPPED_UNEXPECTED_OUTPUT",output_shape=list(arr.shape))
        except Exception as e: exp={"status":"SKIPPED_API_OR_FIT_ERROR","version":version("mapie"),"error":repr(e)}
      result["experiments"]["MAPIE_chronological_conformal"]=exp
    except Exception as e: result["experiments"]["MAPIE_chronological_conformal"]={"status":"SKIPPED_NOT_INSTALLED","error":repr(e)}
    # PySR package/runtime compatibility gate. Full symbolic search only runs when Julia backend imports.
    try:
      import pysr
      exp={"status":"RUNTIME_CHECK","version":version("PySR")}
      try:
        from pysr import PySRRegressor
        exp.update(status="AVAILABLE_NOT_FIT",reason="Symbolic regression is not fit on binary labels without a predeclared regression target and additional compute budget.")
      except Exception as e: exp.update(status="SKIPPED_API_OR_RUNTIME_ERROR",error=repr(e))
      result["experiments"]["PySR_compatibility"]=exp
    except Exception as e: result["experiments"]["PySR_compatibility"]={"status":"SKIPPED_NOT_INSTALLED","version":version("PySR")}
    # tick is often incompatible with newer Python/numpy; only test import, never hide failure.
    try:
      tick=importlib.import_module("tick")
      result["experiments"]["tick_compatibility"]={"status":"AVAILABLE_IMPORT_ONLY","version":version("tick"),"module_file":getattr(tick,"__file__",None)}
    except Exception as e:
      result["experiments"]["tick_compatibility"]={"status":"SKIPPED_IMPORT_OR_COMPATIBILITY_ERROR","version":version("tick"),"error":repr(e)}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
