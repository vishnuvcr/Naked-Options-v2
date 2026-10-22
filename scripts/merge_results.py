"""Merge model, feature ablation and ARIMA outputs; correct model multiplicity."""
import json
from pathlib import Path
import pandas as pd
from forecast_metrics import holm
R=Path(__file__).resolve().parents[1]/"reports"


def read_csv_if_populated(path):
    """Return a non-empty CSV DataFrame, or None for a missing/empty/headerless file."""
    path = Path(path)
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        frame = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return None
    return frame if len(frame) and len(frame.columns) else None


def main():
 bags={"metrics":[],"predictions":[],"experiment_errors":[]}
 skipped_empty_sources=[]
 sources=[("technical","metrics_technical.csv","predictions_technical.csv","experiment_errors_technical.csv"),
 ("global","metrics_global.csv","predictions_global.csv","experiment_errors_global.csv"),
 ("statistical_benchmark","arima_metrics.csv","arima_predictions.csv",None)]
 status={}
 for tag,mf,pf,ef in sources:
  for key,name in (("metrics",mf),("predictions",pf),("experiment_errors",ef)):
   f=R/name if name else None
   if f and f.exists():
    d=read_csv_if_populated(f)
    if d is not None:
     d["feature_set"]=tag;bags[key].append(d)
    else:
     skipped_empty_sources.append(str(f.relative_to(R)))
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
 obj={"status":"COMPLETE" if len(m) else "BLOCKED","runs":status,"metric_rows":len(m),"prediction_rows":sum(map(len,bags["predictions"])),"skipped_empty_sources":sorted(skipped_empty_sources)}
 (R/"feature_ablation.json").write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2))
if __name__=="__main__":main()
