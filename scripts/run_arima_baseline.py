"""Frozen ARIMA(1,0,0) benchmark for cumulative forward returns."""
import json
from pathlib import Path
import numpy as np,pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from forecast_metrics import regmetrics,hac_test,block_ci
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/"data"/"cache"; R=ROOT/"reports"
def main():
 d=pd.read_csv(C/"model_matrix.csv"); cut=int(.8*len(d))
 r=pd.to_numeric(d.daily_log_return,errors="coerce"); train=r.iloc[1:cut].dropna()
 fit=ARIMA(train,order=(1,0,0),trend="c").fit()
 q=dict(zip(fit.param_names,fit.params)); phi=float(q.get("ar.L1",0)); const=float(q.get("const",0)); mu=float(train.mean())
 ms=[];ps=[]
 for h in (1,5,20):
  rows=d[(d.origin_i>=cut)&d[f"target_return_{h}"].notna()]
  y=rows[f"target_return_{h}"].to_numpy(float); p=[]
  for latest in rows.daily_log_return.to_numpy(float):
   total=0
   for _ in range(h):latest=const+phi*latest; total+=latest
   p.append(total)
  p=np.asarray(p); b=np.zeros(len(y)); meanb=np.full(len(y),mu*h)
  m=regmetrics(y,p,b); loss=(y-p)**2-(y-b)**2; ci=block_ci(loss,h); test=hac_test(loss,h-1)
  m.update({"task":"return","horizon":h,"model":"ARIMA(1,0,0)","status":"OOS_EVALUATED","n_test":len(y),
    "mse_skill_vs_mean":float(1-np.mean((y-p)**2)/np.mean((y-meanb)**2)) if np.mean((y-meanb)**2)>0 else None,
    "ci_loss_diff_low":ci[0],"ci_loss_diff_high":ci[1],**test}); ms.append(m)
  for (_,z),obs,pr in zip(rows.iterrows(),y,p):
   ps.append({"origin_date":str(z.date),"target_date":z.get(f"target_date_{h}"),"task":"return","horizon":h,"model":"ARIMA(1,0,0)","actual":obs,"prediction":pr,"baseline":0.})
 R.mkdir(exist_ok=True,parents=True)
 pd.DataFrame(ms).to_csv(R/"arima_metrics.csv",index=False);pd.DataFrame(ps).to_csv(R/"arima_predictions.csv",index=False)
 out={"status":"PASS","training_n":len(train),"phi":phi,"intercept":const,"training_end_index":cut-1}
 (R/"arima_run.json").write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=="__main__":main()
