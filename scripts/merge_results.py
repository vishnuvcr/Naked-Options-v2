"""Merge feature ablations and correct paired tests across them."""
import json
from pathlib import Path
import pandas as pd
from forecast_metrics import holm
R=Path(__file__).resolve().parents[1]/"reports"
def get(tag,name):
 p=R/f"{name}_{tag}.csv"
 if not p.exists() or not p.stat().st_size:return pd.DataFrame()
 d=pd.read_csv(p)
 if len(d):d["feature_set"]=tag
 return d
def main():
 ms=[];ps=[];es=[];status={}
 for tag in ("technical","global"):
  m,p,e=(get(tag,x) for x in ("metrics","predictions","experiment_errors"))
  if len(m):ms.append(m)
  if len(p):ps.append(p)
  if len(e):es.append(e)
  f=R/f"experiment_run_{tag}.json"
  status[tag]=json.loads(f.read_text()) if f.exists() else {"status":"NOT_RUN"}
 m=pd.concat(ms,ignore_index=True) if ms else pd.DataFrame()
 if len(m):
  m["p_holm"]=float("nan")
  for _,ids in m[m.status.eq("OOS_EVALUATED")].groupby(["task","horizon"]).groups.items():
   m.loc[ids,"p_holm"]=holm(m.loc[ids,"p_value"].tolist())
 m.to_csv(R/"metrics.csv",index=False)
 for dest,parts in (("predictions.csv",ps),("experiment_errors.csv",es)):
  (pd.concat(parts,ignore_index=True) if parts else pd.DataFrame()).to_csv(R/dest,index=False)
 obj={"status":"COMPLETE" if len(m) else "BLOCKED","runs":status,"metric_rows":len(m),"prediction_rows":sum(map(len,ps))}
 (R/"feature_ablation.json").write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2))
if __name__=="__main__":main()
