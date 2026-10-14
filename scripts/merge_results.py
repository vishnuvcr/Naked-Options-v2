"""Merge model, feature ablation and ARIMA outputs; correct model multiplicity."""
import json
from pathlib import Path
import pandas as pd
from forecast_metrics import holm
R=Path(__file__).resolve().parents[1]/"reports"
def main():
 bags={"metrics":[],"predictions":[],"experiment_errors":[]}
 sources=[("technical","metrics_technical.csv","predictions_technical.csv","experiment_errors_technical.csv"),
 ("global","metrics_global.csv","predictions_global.csv","experiment_errors_global.csv"),
 ("statistical_benchmark","arima_metrics.csv","arima_predictions.csv",None)]
 status={}
 for tag,mf,pf,ef in sources:
  for key,name in (("metrics",mf),("predictions",pf),("experiment_errors",ef)):
   f=R/name if name else None
   if f and f.exists() and f.stat().st_size:
    d=pd.read_csv(f)
    if len(d):d["feature_set"]=tag;bags[key].append(d)
  meta=R/f"experiment_run_{tag}.json"
  status[tag]=json.loads(meta.read_text()) if meta.exists() else ({"status":"PASS"} if tag=="statistical_benchmark" and (R/"arima_run.json").exists() else {"status":"BLOCKED_OR_NOT_RUN"})
 m=pd.concat(bags["metrics"],ignore_index=True) if bags["metrics"] else pd.DataFrame()
 if len(m):
  m["p_holm"]=float("nan")
  for _,ids in m[m.status.eq("OOS_EVALUATED")].groupby(["task","horizon"]).groups.items():
   m.loc[ids,"p_holm"]=holm(m.loc[ids,"p_value"].tolist())
 m.to_csv(R/"metrics.csv",index=False)
 for key in ("predictions","experiment_errors"):
  (pd.concat(bags[key],ignore_index=True) if bags[key] else pd.DataFrame()).to_csv(R/f"{key}.csv",index=False)
 obj={"status":"COMPLETE" if len(m) else "BLOCKED","runs":status,"metric_rows":len(m),"prediction_rows":sum(map(len,bags["predictions"]))}
 (R/"feature_ablation.json").write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2))
if __name__=="__main__":main()
