#!/usr/bin/env python3
"""OPT-BUY-3.0 finite single-leg entry/exit screen; never exports raw quotes."""
from pathlib import Path
import json, sys, hashlib
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"research"/"option-validation"))
import backtest as legacy
CACHE=ROOT/"data"/"cache"/"options_rolling"
OUT=ROOT/"reports"/"option_entry_exit"
SEED=20261014
SLIPPAGE=(0,25,50,100)
BROKERAGE=(10,20)
SEBI=10/10_000_000
STAMP=.00003
EXCHANGE=.0003553
GST=.18
STT_OLD=.001
STT_NEW=.0015
BOOT=2000

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
    if not rows: return pd.DataFrame(),{"status":"BLOCKED_NO_VALID_QUOTES","parse_errors":errors,"manifest_status":m.get("status"),"request_count":len(m.get("requests",[]))}
    q=pd.DataFrame(rows)
    unit="ms" if q.timestamp.max()>10**12 else "s"
    t=pd.to_datetime(q.timestamp,unit=unit,utc=True,errors="coerce").dt.tz_convert("Asia/Kolkata")
    q["date"]=t.dt.strftime("%Y-%m-%d"); q["time"]=t.dt.strftime("%H:%M")
    required={"date","time","option_type","strike","spot","open","high","low","close"}
    if not required.issubset(q.columns): return pd.DataFrame(),{"status":"BLOCKED_SCHEMA","missing_columns":sorted(required-set(q.columns))}
    q=q.dropna(subset=["date","time","option_type","strike","spot","open","high","low","close"])
    q=q[(q.strike>0)&(q.spot>0)&(q.open>0)&(q.high>0)&(q.low>0)&(q.close>0)&(q.high>=q.low)]
    keys=["date","time","option_type","strike"]
    d=q.groupby(keys).agg(n=("close","size"),os=("open",lambda x:x.max()-x.min()),cs=("close",lambda x:x.max()-x.min())).reset_index()
    dup=d[d.n>1]; conflicts=dup[(dup.os>.01)|(dup.cs>.01)]
    bad=set(map(tuple,conflicts[keys].itertuples(index=False,name=None)))
    q=q.loc[[tuple(x) not in bad for x in q[keys].itertuples(index=False,name=None)]].drop_duplicates(keys).sort_values(keys).reset_index(drop=True)
    return q,{"status":m.get("status"),"manifest_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":len(q),"dates":int(q.date.nunique()),"first_date":str(q.date.min()) if len(q) else None,"last_date":str(q.date.max()) if len(q) else None,"duplicate_groups":len(dup),"conflict_groups":len(conflicts),"conflict_rate":len(conflicts)/max(len(dup),1),"parse_errors":errors,"manifest_status":m.get("status"),"request_count":len(m.get("requests",[]))}

def single_leg_cost(date, entry, exit, lot, slip_bps, brokerage):
    if not all(np.isfinite(x) and x>0 for x in (entry,exit)) or lot<=0: raise ValueError("invalid trade values")
    s=slip_bps/10000.0
    buy=entry*(1+s)*lot; sell=exit*(1-s)*lot
    stt_rate=STT_NEW if date>="2026-04-01" else STT_OLD
    br=float(brokerage)*2
    sebi=(buy+sell)*SEBI; exchange=(buy+sell)*EXCHANGE
    fees=br+sell*stt_rate+buy*STAMP+sebi+exchange+GST*(br+sebi+exchange)
    slip_cost=(entry+exit)*s*lot
    gross=(exit-entry)*lot
    return {"gross_pnl_rupees":gross,"total_cost_rupees":fees+slip_cost,"net_pnl_rupees":gross-fees-slip_cost,"brokerage_rupees":br,"slippage_cost_rupees":slip_cost,"entry_debit_rupees":buy,"lot_size_proxy":lot}

def signals(g, seed):
    """Each date yields prespecified controls and causal spot-only targeted signals."""
    times=sorted(g.time.unique())
    if len(times)<8: return []
    spot=g.groupby("time").spot.median().reindex(times)
    out=[]
    rng=np.random.default_rng(seed)
    # Fixed-time controls enter at next observed bar; random baseline is reproducible by date.
    for name, tm, side in [("TIME0920_CALL","09:20","CALL"),("TIME0920_PUT","09:20","PUT"),
                           ("TIME1000_CALL","10:00","CALL"),("TIME1000_PUT","10:00","PUT"),
                           ("TIME1200_CALL","12:00","CALL"),("TIME1200_PUT","12:00","PUT")]:
        ix=next((i for i,t in enumerate(times) if t>=tm),None)
        if ix is not None and ix+1<len(times): out.append((name,ix+1,side))
    eligible=np.arange(max(1,int(len(times)*.2)),max(2,len(times)-6))
    if len(eligible):
        ri=int(rng.choice(eligible)); out.append(("RANDOM_DIRECTION_TIME",ri,str(rng.choice(["CALL","PUT"]))))
    # Causal three-bar spot momentum and six-bar range breakout, evaluated at bar close and entered next bar.
    vals=spot.to_numpy(float)
    for i in range(3,len(times)-1):
        if not np.isfinite(vals[i]) or not np.isfinite(vals[i-3]): continue
        if vals[i]>vals[i-3]: out.append(("SPOT_MOMENTUM_CALL",i+1,"CALL"))
        elif vals[i]<vals[i-3]: out.append(("SPOT_MOMENTUM_PUT",i+1,"PUT"))
        if i>=6 and np.all(np.isfinite(vals[i-6:i])):
            if vals[i]>np.max(vals[i-6:i]): out.append(("SPOT_RANGE_BREAK_CALL",i+1,"CALL"))
            elif vals[i]<np.min(vals[i-6:i]): out.append(("SPOT_RANGE_BREAK_PUT",i+1,"PUT"))
    # Keep at most one signal per entry family/side/day, earliest valid signal after 09:30.
    seen=set(); unique=[]
    for e in out:
        if e[0].startswith("TIME") or e[0]=="RANDOM_DIRECTION_TIME":
            unique.append(e); continue
        k=(e[0],e[2])
        if k not in seen and times[e[1]]>="09:30": unique.append(e); seen.add(k)
    return unique

def execute_trade(g, times, entry_i, side, exit_id, slip, brokerage, date):
    et=times[entry_i]
    x=g[(g.time==et)&(g.option_type==side)].copy()
    if x.empty: return None
    spot=float(x.spot.median()); x["dist"]=(x.strike.astype(float)-spot).abs()
    strike=float(x.sort_values(["dist","strike"]).iloc[0].strike)
    er=x[np.isclose(x.strike.astype(float),strike)]
    if er.empty: return None
    entry=float(er.iloc[0].open)
    if entry_i>=len(times)-1: return None
    if exit_id.startswith("HOLD"):
        n=int(exit_id[4:])//5
        if entry_i+n>=len(times): return None
        exit_i=entry_i+n
    else: exit_i=len(times)-1
    if exit_id in {"TP20_SL15","TP30_SL20","TP50_SL25","TRAIL20"}:
        target={"TP20_SL15":.20,"TP30_SL20":.30,"TP50_SL25":.50,"TRAIL20":.20}[exit_id]
        stop={"TP20_SL15":.15,"TP30_SL20":.20,"TP50_SL25":.25,"TRAIL20":.20}[exit_id]
        peak=entry; exit_i=None; exit_price=None
        for j in range(entry_i+1,len(times)):
            z=g[(g.time==times[j])&(g.option_type==side)&np.isclose(g.strike.astype(float),strike)]
            if z.empty: continue
            lo=float(z.iloc[0].low); hi=float(z.iloc[0].high); close=float(z.iloc[0].close)
            peak=max(peak,hi)
            if lo<=entry*(1-stop): exit_i=j; exit_price=entry*(1-stop); break
            if hi>=entry*(1+target): exit_i=j; exit_price=entry*(1+target); break
            if exit_id=="TRAIL20" and close<=peak*(1-stop): exit_i=j; exit_price=close; break
        if exit_i is None: exit_i=len(times)-1
    z=g[(g.time==times[exit_i])&(g.option_type==side)&np.isclose(g.strike.astype(float),strike)]
    if z.empty: return None
    ex=float(exit_price if exit_id in {"TP20_SL15","TP30_SL20","TP50_SL25","TRAIL20"} and exit_price is not None else z.iloc[0].close)
    lot=legacy.lot_size_proxy(date)
    cost=single_leg_cost(date,entry,ex,lot,slip,brokerage)
    return {"date":date,"entry_id":None,"exit_id":exit_id,"side":side,"entry_time":et,"exit_time":times[exit_i],"net_pnl_rupees":cost["net_pnl_rupees"],"gross_pnl_rupees":cost["gross_pnl_rupees"],"total_cost_rupees":cost["total_cost_rupees"],"slippage_bps":slip,"brokerage_per_order":brokerage,"lot_size_proxy":lot}

def block_ci(values, seed):
    x=np.asarray(values,dtype=float); n=len(x)
    if n<2:return float("nan"),float("nan"),float("nan")
    rng=np.random.default_rng(seed); blocks=int(np.ceil(n/5))
    starts=rng.integers(0,n,size=(BOOT,blocks))
    idx=((starts[:,:,None]+np.arange(5)[None,None,:])%n).reshape(BOOT,-1)[:,:n]
    means=x[idx].mean(axis=1); centered=(x-x.mean())[idx].mean(axis=1)
    p=(1+int((centered>=x.mean()).sum()))/(BOOT+1)
    return float(np.quantile(means,.025)),float(np.quantile(means,.975)),float(p)

def holm(pvalues):
    vals=np.asarray(pvalues,float); out=np.full(len(vals),np.nan); ok=np.where(np.isfinite(vals))[0]
    order=ok[np.argsort(vals[ok])]; run=0.
    for rank,i in enumerate(order): run=max(run,min(1.,(len(order)-rank)*vals[i])); out[i]=run
    return out

def run():
    OUT.mkdir(parents=True,exist_ok=True); q,meta=load(); trades=[]; skips={}
    if not q.empty:
        for date,g in q.groupby("date",sort=True):
            times=sorted(g.time.unique())
            for entry_id,ix,side in signals(g,SEED+int(date.replace("-",""))):
                for exit_id in ["EOD","HOLD30","HOLD60","HOLD120","TP20_SL15","TP30_SL20","TP50_SL25","TRAIL20"]:
                    for slip in SLIPPAGE:
                        for brokerage in BROKERAGE:
                            try: t=execute_trade(g,times,ix,side,exit_id,slip,brokerage,date)
                            except (ValueError,IndexError,KeyError): t=None
                            if t is None: skips["incomplete_or_missing_quote"]=skips.get("incomplete_or_missing_quote",0)+1; continue
                            t["entry_id"]=entry_id; trades.append(t)
    out=[]
    if trades:
        df=pd.DataFrame(trades)
        # One daily result per candidate; no-trade eligible dates are explicitly zero-filled.
        all_dates=sorted(q.date.unique())
        for (e,x,slip,brokerage),g in df.groupby(["entry_id","exit_id","slippage_bps","brokerage_per_order"]):
            daily=g.groupby("date").net_pnl_rupees.sum().reindex(all_dates,fill_value=0.0).to_numpy(float)
            lo,hi,p=block_ci(daily,SEED+len(out))
            out.append({"entry_id":e,"exit_id":x,"slippage_bps":int(slip),"brokerage_per_order":int(brokerage),"trades":int(len(g)),"sessions":len(all_dates),"mean_net_pnl_per_session":float(daily.mean()),"mean_net_pnl_per_trade":float(g.net_pnl_rupees.mean()),"win_rate":float((g.net_pnl_rupees>0).mean()),"ci95_low":lo,"ci95_high":hi,"p_positive_raw":p})
        adj=holm([z["p_positive_raw"] for z in out])
        for z,a in zip(out,adj): z["holm_p"]=float(a); z["approved"]=False
    gate=bool(not q.empty and meta.get("conflict_rate",1)<=.01 and not meta.get("parse_errors") and meta.get("dates",0)>0)
    summary={"version":"OPT-BUY-3.0","status":"COMPLETED_EXPLORATORY" if trades and gate else ("COMPLETED_DATA_GATE_FAIL" if trades else meta.get("status","BLOCKED")),"data_gate_pass":gate,"strategy_approved":False,"data_quality":meta,"skips":skips,"candidate_count":len(out),"trade_count":len(trades),"candidates":out,"cost_sensitivities":{"slippage_bps":list(SLIPPAGE),"brokerage_per_order":list(BROKERAGE)},"note":"Finite screen covers fixed-time controls, seeded random direction/time, causal spot momentum/range-breakout entries, EOD/fixed-hold/premium barrier/trailing exits. Rolling relative-strike data and provider spot are proxies. Incompatible/missing quote trades are skipped and counted. No strategy is auto-approved."}
    if trades:
        safe=df.drop(columns=["gross_pnl_rupees","total_cost_rupees"],errors="ignore")
        safe.to_csv(OUT/"trade_ledger_sanitized.csv",index=False)
        pd.DataFrame(out).to_csv(OUT/"candidate_metrics.csv",index=False)
    (OUT/"results_summary.json").write_text(json.dumps(summary,indent=2,allow_nan=True))
    lines=["# OPT-BUY-3.0 Results","","Status: "+str(summary["status"]),"","Data gate: "+str(gate),"","Strategy approved: false","","Data note: "+str(meta),"","This report is generated only from observed cached/provider rows. Missing/incomplete trades are counted, no quotes are synthesized, and all results remain exploratory until every registered quality/statistical gate is met.","","| Entry | Exit | Slip bps/side | Brokerage/order ₹ | Trades | Mean net ₹/session | 95% CI low | 95% CI high | Holm p |","|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for z in out: lines.append("| {entry_id} | {exit_id} | {slippage_bps} | {brokerage_per_order} | {trades} | {mean_net_pnl_per_session:.2f} | {ci95_low:.2f} | {ci95_high:.2f} | {holm_p:.5f} |".format(**z))
    (ROOT/"research"/"option-entry-exit"/"RESULTS.md").write_text("\n".join(lines)+"\n")
    print(json.dumps({k:summary.get(k) for k in ["status","data_gate_pass","strategy_approved","candidate_count","trade_count"]},indent=2))
if __name__=="__main__": run()
