"""Forecast metrics and dependence-aware paired loss tests."""
import numpy as np
from scipy.stats import norm
from sklearn.metrics import accuracy_score, balanced_accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, brier_score_loss, log_loss

def regmetrics(y,p,b):
    y=np.asarray(y,float); p=np.asarray(p,float); b=np.asarray(b,float)
    m=np.isfinite(y)&np.isfinite(p)&np.isfinite(b); y,p,b=y[m],p[m],b[m]
    if not len(y): return {"n":0}
    mse=np.mean((y-p)**2); bmse=np.mean((y-b)**2); den=np.sum((y-y.mean())**2)
    return {"n":len(y),"mae":float(np.mean(abs(y-p))),"rmse":float(np.sqrt(mse)),
      "oos_r2_vs_mean":float(1-np.sum((y-p)**2)/den) if den>0 else None,
      "mse_baseline":float(bmse),"mse_skill_vs_baseline":float(1-mse/bmse) if bmse>0 else None}

def clsmetrics(y,p,b):
    y=np.asarray(y,int); p=np.clip(np.asarray(p,float),1e-7,1-1e-7); b=np.clip(np.asarray(b,float),1e-7,1-1e-7)
    if len(y)==0: return {"n":0}
    yp=(p>=.5).astype(int)
    out={"n":len(y),"accuracy":float(accuracy_score(y,yp)),"balanced_accuracy":float(balanced_accuracy_score(y,yp)),
      "precision":float(precision_score(y,yp,zero_division=0)),"recall":float(recall_score(y,yp,zero_division=0)),
      "f1":float(f1_score(y,yp,zero_division=0)),"brier":float(brier_score_loss(y,p)),
      "brier_skill":float(1-brier_score_loss(y,p)/brier_score_loss(y,b)) if brier_score_loss(y,b)>0 else None,
      "log_loss":float(log_loss(y,np.c_[1-p,p],labels=[0,1])),"baseline_log_loss":float(log_loss(y,np.c_[1-b,b],labels=[0,1]))}
    out["roc_auc"]=float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None
    return out

def hac_test(diff,lag):
    d=np.asarray(diff,float); d=d[np.isfinite(d)]; n=len(d)
    if n<10: return {"mean_loss_diff":float(d.mean()) if n else None,"z":None,"p_value":None}
    x=d-d.mean(); lrv=np.dot(x,x)/n
    L=min(max(0,int(lag)),n-1)
    for k in range(1,L+1): lrv+=2*(1-k/(L+1))*np.dot(x[k:],x[:-k])/n
    se=np.sqrt(max(lrv,0)/n); z=float(d.mean()/se) if se>0 else None
    return {"mean_loss_diff":float(d.mean()),"z":z,"p_value":float(2*norm.sf(abs(z))) if z is not None else None}

def block_ci(x,block,seed=20261014,reps=300):
    x=np.asarray(x,float); x=x[np.isfinite(x)]; n=len(x)
    if n<10: return (None,None)
    rng=np.random.default_rng(seed); b=max(1,min(int(block),n)); means=[]
    for _ in range(reps):
        starts=rng.integers(0,n,size=int(np.ceil(n/b)))
        means.append(np.mean(np.concatenate([x[(s+np.arange(b))%n] for s in starts])[:n]))
    return tuple(float(v) for v in np.quantile(means,[.025,.975]))

def holm(ps):
    out=[None]*len(ps); v=sorted([(i,float(p)) for i,p in enumerate(ps) if p is not None and np.isfinite(p)],key=lambda x:x[1]); run=0.0
    for j,(i,p) in enumerate(v): run=max(run,min(1.0,(len(v)-j)*p)); out[i]=run
    return out
