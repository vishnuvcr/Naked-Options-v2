#!/usr/bin/env python3
"""OPT-BUY-3.0 bounded cached quote screen. No raw option prices are exported."""
from pathlib import Path
import json,sys,hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"research"/"option-validation"))
import backtest as legacy
CACHE=ROOT/"data"/"cache"/"options_rolling"
OUT=ROOT/"reports"/"option_entry_exit"
SEED=20261014
def load():
 p=CACHE/"manifest.json"
 if not p.exists(): return pd.DataFrame(),{"status":"BLOCKED_NO_OPTION_MANIFEST"}
 m=json.loads(p.read_text()); rows=[]; errors=[]
 for r in m.get("requests",[]):
  if r.get("status") not in {"PASS","CACHED","EMPTY"}: continue
  f=ROOT/r.get("file","")
  if not f.exists(): errors.append("missing cached file"); continue
  try: rows.extend(legacy.payload_to_rows(json.loads(f.read_text()),r["option_type"],int(r.get("offset",0))))
  except Exception as e: errors.append(type(e).__name__)
 if not rows:return pd.DataFrame(),{"status":"BLOCKED_NO_VALID_QUOTES","parse_errors":errors}
 q=pd.DataFrame(rows); unit="ms" if q.timestamp.max()>10**12 else "s"
 t=pd.to_datetime(q.timestamp,unit=unit,utc=True,errors="coerce").dt.tz_convert("Asia/Kolkata")
 q["date"]=t.dt.strftime("%Y-%m-%d");q["time"]=t.dt.strftime("%H:%M")
 q=q.dropna(subset=["date","strike","spot"]);q=q[(q.strike>0)&(q.spot>0)&(q.open>0)&(q.close>0)]
 keys=["date","time","option_type","strike"]
 d=q.groupby(keys).agg(n=("close","size"),os=("open",lambda x:x.max()-x.min()),cs=("close",lambda x:x.max()-x.min())).reset_index()
 du=d[d.n>1]; co=du[(du.os>.01)|(du.cs>.01)]
 bad=set(map(tuple,co[keys].itertuples(index=False,name=None)))
 q=q.loc[[tuple(x) not in bad for x in q[keys].itertuples(index=False,name=None)]].drop_duplicates(keys).sort_values(keys)
 return q,{"status":m.get("status"),"manifest_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":len(q),"dates":int(q.date.nunique()),"first_date":str(q.date.min()) if len(q) else None,"last_date":str(q.date.max()) if len(q) else None,"duplicate_groups":len(du),"conflict_groups":len(co),"conflict_rate":len(co)/max(len(du),1),"parse_errors":errors}
def run():
 OUT.mkdir(parents=True,exist_ok=True);q,meta=load(); rows=[]; skips={}
 if not q.empty:
  for d,g in q.groupby("date",sort=True):
   times=sorted(g.time.unique())
   for tm in ["09:20","10:00","12:00"]:
    ix=next((i for i,t in enumerate(times) if t>=tm),None)
    if ix is None or ix+1>=len(times):continue
    et=times[ix+1]
    for side in ["CALL","PUT"]:
     x=g[(g.time==et)&(g.option_type==side)]
     if x.empty:skips["entry_missing"]=skips.get("entry_missing",0)+1;continue
     spot=float(x.spot.median()); ss=x.strike.to_numpy(float); strike=float(ss[np.argmin(abs(ss-spot))])
     en=x[np.isclose(x.strike.astype(float),strike)].iloc[0].open
     ei=times.index(et)
     for exit_id,delta in [("HOLD30",6),("HOLD60",12),("HOLD120",24),("EOD",None)]:
      xt="15:25" if delta is None else times[min(ei+delta,len(times)-1)]
      z=g[(g.time==xt)&(g.option_type==side)&np.isclose(g.strike.astype(float),strike)]
      if z.empty:skips["exit_missing"]=skips.get("exit_missing",0)+1;continue
      ex=float(z.iloc[0].close)
      trade={"entry_prices":[float(en)],"exit_prices":[ex],"trade_date":d,"lot_size":legacy.lot_size_proxy(d),"structure":"single"}
      c=legacy.calculate_trade(trade,50,10)
      rows.append({"date":d,"entry_id":"TIME_"+tm.replace(":","")+"_"+side,"exit_id":exit_id,"net_pnl_rupees":c["net_pnl_rupees"],"gross_pnl_rupees":c["gross_pnl_rupees"],"total_cost_rupees":c["total_cost_rupees"],"entry_debit_points":float(en),"exit_premium_points":ex,"lot_size_proxy":c["lot_size_proxy"]})
 out=[]
 if rows:
  df=pd.DataFrame(rows)
  rng=np.random.default_rng(SEED)
  for (e,x),g in df.groupby(["entry_id","exit_id"]):
   d=g.groupby("date").net_pnl_rupees.sum().sort_index().to_numpy(float);n=len(d)
   if n<2:lo=hi=p=float("nan")
   else:
    starts=rng.integers(0,n,size=(2000,int(np.ceil(n/5))))
    idx=((starts[:,:,None]+np.arange(5)[None,None,:])%n).reshape(2000,-1)[:,:n]
    sm=d[idx].mean(1); cen=(d-d.mean())[idx].mean(1)
    lo=float(np.quantile(sm,.025));hi=float(np.quantile(sm,.975));p=float((1+(cen>=d.mean()).sum())/2001)
   out.append({"entry_id":e,"exit_id":x,"trades":len(g),"sessions":n,"mean_net_pnl_per_session":float(d.mean()),"mean_net_pnl_per_trade":float(g.net_pnl_rupees.mean()),"win_rate":float((g.net_pnl_rupees>0).mean()),"ci95_low":lo,"ci95_high":hi,"p_positive_raw":p})
 finite=sorted([(i,z["p_positive_raw"]) for i,z in enumerate(out) if np.isfinite(z["p_positive_raw"])],key=lambda z:z[1]);runmax=0
 for rank,(i,p) in enumerate(finite):runmax=max(runmax,min(1,(len(finite)-rank)*p));out[i]["holm_p"]=runmax
 for z in out:z["approved"]=False
 gate=bool(meta.get("conflict_rate",1)<=.01 and not meta.get("parse_errors"))
 summary={"version":"OPT-BUY-3.0","status":"COMPLETED_EXPLORATORY" if rows and not gate else ("COMPLETED_DATA_GATE_PASS" if rows else meta.get("status","BLOCKED")),"data_gate_pass":gate,"strategy_approved":False,"data_quality":meta,"skips":skips,"candidate_count":len(out),"candidates":out,"note":"This first bounded implementation screens time-based CALL/PUT entries only. Rule-based entries, random controls, barrier/trailing exits and 100bp recalculation remain pending code validation; no strategy can be approved from this run."}
 if rows:
  safe=df.drop(columns=["entry_debit_points","exit_premium_points","gross_pnl_rupees","total_cost_rupees"])
  safe.to_csv(OUT/"trade_ledger_sanitized.csv",index=False);pd.DataFrame(out).to_csv(OUT/"candidate_metrics.csv",index=False)
 (OUT/"results_summary.json").write_text(json.dumps(summary,indent=2,allow_nan=True))
 lines=["# OPT-BUY-3.0 Results","","Status: "+str(summary["status"]),"","Data gate: "+str(gate),"","Strategy approved: false","","This first implementation is a bounded time-entry screen only; it is not the full registered catalogue. Do not interpret as final strategy selection.",""]
 lines += ["| Entry | Exit | Trades | Mean net ₹/session | 95% CI low | 95% CI high | Holm p |","|---|---|---:|---:|---:|---:|---:|"]
 for z in out:lines.append("| {entry_id} | {exit_id} | {trades} | {mean_net_pnl_per_session:.2f} | {ci95_low} | {ci95_high} | {holm_p} |".format(**z))
 (ROOT/"research"/"option-entry-exit"/"RESULTS.md").write_text("\n".join(lines)+"\n")
 print(json.dumps({k:summary.get(k) for k in ["status","data_gate_pass","strategy_approved","candidate_count"]},indent=2))
if __name__=="__main__":run()
