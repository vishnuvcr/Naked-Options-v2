"""Forecast scores, HAC paired-loss test, block confidence interval, and Holm correction."""
import numpy as np
from scipy.stats import norm
from sklearn.metrics import accuracy_score,balanced_accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,brier_score_loss,log_loss
def regmetrics(y,p,b):
 y,p,b=map(lambda z:np.asarray(z,float),(y,p,b)); m=np.isfinite(y)&np.isfinite(p)&np.isfinite(b); y,p,b=y[m],p[m],b[m]
 if not len(y): return {"n":0}
 mse=np.mean((y-p)**2); bm=np.mean((y-b)**2); den=np.sum((y-y.mean())**2)
 return {"n":len(y),"mae":float(np.mean(abs(y-p))),"rmse":float(np.sqrt(mse)),"oos_r2_vs_baseline":float(1-mse/bm) if bm else None,"mse_baseline":float(bm),"mse_skill_vs_baseline":float(1-mse/bm) if bm else None}
def clsmetrics(y,p,b):
 y=np.asarray(y,int); p=np.clip(np.asarray(p,float),1e-7,1-1e-7); b=np.clip(np.asarray(b,float),1e-7,1-1e-7)
 if not len(y): return {"n":0}
 yp=(p>=.5).astype(int); base=brier_score_loss(y,b)
 o={"n":len(y),"accuracy":float(accuracy_score(y,yp)),"balanced_accuracy":float(balanced_accuracy_score(y,yp)),"precision":float(precision_score(y,yp,zero_division=0)),"recall":float(recall_score(y,yp,zero_division=0)),"f1":float(f1_score(y,yp,zero_division=0)),"brier":float(brier_score_loss(y,p)),"brier_skill":float(1-brier_score_loss(y,p)/base) if base else None,"log_loss":float(log_loss(y,np.c_[1-p,p],labels=[0,1])),"baseline_log_loss":float(log_loss(y,np.c_[1-b,b],labels=[0,1]))}
 o["roc_auc"]=float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None
 return o
def hac_test(d,lag):
 d=np.asarray(d,float); d=d[np.isfinite(d)]; n=len(d)
 if n<10:return {"mean_loss_diff":float(d.mean()) if n else None,"z":None,"p_value":None}
 x=d-d.mean(); lrv=np.dot(x,x)/n; L=min(max(5,int(lag)),n-1)
 for k in range(1,L+1):lrv+=2*(1-k/(L+1))*np.dot(x[k:],x[:-k])/n
 se=np.sqrt(max(lrv,0)/n); z=float(d.mean()/se) if se else None
 return {"mean_loss_diff":float(d.mean()),"z":z,"p_value":float(2*norm.sf(abs(z))) if z is not None else None}
def block_ci(x,block,seed=20261014,reps=300):
 x=np.asarray(x,float); x=x[np.isfinite(x)]; n=len(x)
 if n<10:return (None,None)
 rng=np.random.default_rng(seed); b=max(5,min(int(block),n)); means=[]
 for _ in range(reps):
  starts=rng.integers(0,n,size=int(np.ceil(n/b)))
  means.append(np.mean(np.concatenate([x[(s+np.arange(b))%n] for s in starts])[:n]))
 return tuple(float(v) for v in np.quantile(means,[.025,.975]))
def holm(ps):
 out=[None]*len(ps); v=sorted([(i,float(p)) for i,p in enumerate(ps) if p is not None and np.isfinite(p)],key=lambda z:z[1]); run=0.
 for j,(i,p) in enumerate(v):run=max(run,min(1.,(len(v)-j)*p));out[i]=run
 return out

def qlike_loss(actual_variance, forecast_variance):
    """Nonnegative QLIKE-equivalent loss for positive realized/forecast variance.

    loss = ratio - log(ratio) - 1, where ratio = realized variance / forecast variance.
    It differs from log(forecast variance) + realized/forecast by a term constant
    with respect to the forecast for a given realized observation, so paired losses
    are equivalent while the score itself is nonnegative.
    """
    actual=np.maximum(np.asarray(actual_variance,dtype=float),1e-12)
    forecast=np.maximum(np.asarray(forecast_variance,dtype=float),1e-12)
    ratio=actual/forecast
    return ratio-np.log(ratio)-1.0
