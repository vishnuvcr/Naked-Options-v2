"""Optional compact LSTM, GRU, TCN and Transformer estimators for lagged returns."""
import importlib.util
import numpy as np
from sklearn.base import BaseEstimator
class SequenceEstimator(BaseEstimator):
 def __init__(self,arch="lstm",kind="reg",epochs=8,hidden=16,seed=20261014):
  self.arch=arch;self.kind=kind;self.epochs=epochs;self.hidden=hidden;self.seed=seed
 def fit(self,X,y):
  import torch
  from torch import nn
  torch.manual_seed(self.seed);torch.set_num_threads(2)
  a=np.asarray(X,float);mu=float(np.nanmean(a));sd=float(np.nanstd(a))+1e-8
  a=np.nan_to_num(a,nan=mu,posinf=mu,neginf=mu);a=(a-mu)/sd
  self.xmu_=mu;self.xsd_=sd; yy=np.asarray(y,float)
  self.ymu_=float(yy.mean()) if self.kind=="reg" else 0.
  self.ysd_=float(yy.std()+1e-8) if self.kind=="reg" else 1.
  yy=(yy-self.ymu_)/self.ysd_ if self.kind=="reg" else yy
  h=self.hidden;arch=self.arch;L=a.shape[1]
  class Net(nn.Module):
   def __init__(self):
    super().__init__();self.arch=arch
    if arch in ("lstm","gru"):
     self.rnn=(nn.LSTM(1,h,batch_first=True) if arch=="lstm" else nn.GRU(1,h,batch_first=True))
    elif arch=="tcn":
     self.conv=nn.Sequential(nn.Conv1d(1,h,3,padding=1),nn.GELU(),nn.Conv1d(h,h,3,padding=2,dilation=2),nn.GELU(),nn.AdaptiveAvgPool1d(1))
    else:
     self.input=nn.Linear(1,h);self.pos=nn.Parameter(torch.zeros(1,L,h))
     layer=nn.TransformerEncoderLayer(h,4,batch_first=True,dropout=0.1)
     self.trans=nn.TransformerEncoder(layer,2)
    self.head=nn.Linear(h,1)
   def forward(self,z):
    if self.arch in ("lstm","gru"):z=self.rnn(z)[0][:,-1,:]
    elif self.arch=="tcn":z=self.conv(z.transpose(1,2)).squeeze(-1)
    else:z=self.trans(self.input(z)+self.pos)[:,-1,:]
    return self.head(z).squeeze(-1)
  self.net_=Net();x=torch.tensor(a,dtype=torch.float32);t=torch.tensor(yy,dtype=torch.float32)
  opt=torch.optim.Adam(self.net_.parameters(),lr=.001,weight_decay=.0001)
  lossfn=nn.MSELoss() if self.kind=="reg" else nn.BCEWithLogitsLoss()
  rng=np.random.default_rng(self.seed)
  for _ in range(self.epochs):
   ix=rng.permutation(len(t));self.net_.train()
   for start in range(0,len(ix),128):
    ids=ix[start:start+128];opt.zero_grad();pred=self.net_(x[ids]);loss=lossfn(pred,t[ids])
    loss.backward();nn.utils.clip_grad_norm_(self.net_.parameters(),1.);opt.step()
  self.classes_=np.array([0,1]);return self
 def _raw(self,X):
  import torch
  a=np.asarray(X,float);a=np.nan_to_num(a,nan=self.xmu_,posinf=self.xmu_,neginf=self.xmu_)
  x=torch.tensor((a-self.xmu_)/self.xsd_,dtype=torch.float32);self.net_.eval()
  with torch.no_grad():return self.net_(x).numpy()
 def predict(self,X):
  p=self._raw(X)
  return p*self.ysd_+self.ymu_ if self.kind=="reg" else (p>=0).astype(int)
 def predict_proba(self,X):
  p=1/(1+np.exp(-np.clip(self._raw(X),-30,30)))
  return np.c_[1-p,p]
def sequence_models():
 if importlib.util.find_spec("torch") is None:return {},{}
 names=("lstm","gru","tcn","transformer")
 return ({f"seq_{n}":SequenceEstimator(n,"reg") for n in names},
         {f"seq_{n}":SequenceEstimator(n,"cls") for n in names})
