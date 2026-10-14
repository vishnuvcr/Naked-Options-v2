"""Merge feature ablations and benchmark outputs with empty-file safety."""
import json
from pathlib import Path
import pandas as pd
from pandas.errors import EmptyDataError
from forecast_metrics import holm

R=Path(__file__).resolve().parents[1]/"reports"

def read_csv_safe(path):
    """Return an empty frame for an absent/zero-column CSV, not a pandas parser crash."""
    if path is None or not path.exists():
        return pd.DataFrame()
    raw=path.read_bytes()
    if not raw.strip():
        return pd.DataFrame()
    try:
        frame=pd.read_csv(path)
    except EmptyDataError:
        return pd.DataFrame()
    return frame if len(frame.columns) else pd.DataFrame()

def main():
    bags={"metrics":[],"predictions":[],"experiment_errors":[]}
    sources=[
        ("technical","metrics_technical.csv","predictions_technical.csv","experiment_errors_technical.csv"),
        ("global","metrics_global.csv","predictions_global.csv","experiment_errors_global.csv"),
        ("statistical_benchmark","arima_metrics.csv","arima_predictions.csv",None),
    ]
    status={}
    for tag,mf,pf,ef in sources:
        for key,name in (("metrics",mf),("predictions",pf),("experiment_errors",ef)):
            file=R/name if name else None
            data=read_csv_safe(file)
            if len(data):
                data["feature_set"]=tag
                bags[key].append(data)
        if tag=="statistical_benchmark" and (R/"arima_run.json").exists():
            try: status[tag]=json.loads((R/"arima_run.json").read_text())
            except Exception: status[tag]={"status":"UNREADABLE_ARIMA_MANIFEST"}
        else:
            meta=R/f"experiment_run_{tag}.json"
            if meta.exists():
                try: status[tag]=json.loads(meta.read_text())
                except Exception: status[tag]={"status":"UNREADABLE_EXPERIMENT_MANIFEST"}
            else:
                status[tag]={"status":"BLOCKED_OR_NOT_RUN"}
    metrics=pd.concat(bags["metrics"],ignore_index=True) if bags["metrics"] else pd.DataFrame()
    if len(metrics):
        if "p_value" not in metrics:
            metrics["p_value"]=float("nan")
        metrics["p_holm"]=float("nan")
        valid=metrics[metrics.status.eq("OOS_EVALUATED")]
        for _,ids in valid.groupby(["task","horizon"]).groups.items():
            metrics.loc[ids,"p_holm"]=holm(metrics.loc[ids,"p_value"].tolist())
    metrics.to_csv(R/"metrics.csv",index=False)
    for key in ("predictions","experiment_errors"):
        frame=pd.concat(bags[key],ignore_index=True) if bags[key] else pd.DataFrame()
        frame.to_csv(R/f"{key}.csv",index=False)
    output={
        "status":"COMPLETE" if len(metrics) else "BLOCKED_NO_METRICS",
        "runs":status,
        "metric_rows":len(metrics),
        "prediction_rows":sum(map(len,bags["predictions"])),
        "error_rows":sum(map(len,bags["experiment_errors"])),
        "empty_inputs_ignored":[key for key in ("technical","global") if not len(read_csv_safe(R/f"metrics_{key}.csv"))],
        "multiplicity":"Holm correction recalculated across all merged candidate models for each task/horizon.",
    }
    (R/"feature_ablation.json").write_text(json.dumps(output,indent=2))
    print(json.dumps(output,indent=2))
    return 0 if len(metrics) else 3

if __name__=="__main__":
    raise SystemExit(main())
