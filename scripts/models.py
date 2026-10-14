"""Fixed forecast candidates plus optional gradient-boosting packages."""
import importlib
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge,ElasticNet,LogisticRegression
from sklearn.svm import SVR,SVC
from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor,HistGradientBoostingRegressor,RandomForestClassifier,ExtraTreesClassifier,HistGradientBoostingClassifier
from sklearn.neural_network import MLPRegressor,MLPClassifier
SEED=20261014
def sc(m):return make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),m)
def tr(m):return make_pipeline(SimpleImputer(strategy="median"),m)
def optional(kind):
 out={}
 configs=[
 ("xgboost","XGB"+kind,{"n_estimators":180,"max_depth":3,"learning_rate":.03,"subsample":.8,"colsample_bytree":.8,"reg_lambda":10,"n_jobs":2,"random_state":SEED}),
 ("lightgbm","LGBM"+kind,{"n_estimators":180,"num_leaves":15,"learning_rate":.03,"reg_lambda":10,"verbosity":-1,"n_jobs":2,"random_state":SEED}),
 ("catboost","CatBoost"+kind,{"iterations":180,"depth":4,"learning_rate":.03,"verbose":False,"thread_count":2,"random_seed":SEED})]
 for mod,cls,kw in configs:
  try:
   if mod=="xgboost" and kind=="Regressor":kw["objective"]="reg:squarederror"
   if mod=="xgboost" and kind=="Classifier":kw["eval_metric"]="logloss"
   if mod=="catboost" and kind=="Classifier":kw["verbose"]=False
   out[mod]=tr(getattr(importlib.import_module(mod),cls)(**kw))
  except Exception:pass
 return out
def regression_models():
 out={"ridge":sc(Ridge(alpha=10)),"elastic_net":sc(ElasticNet(alpha=.0005,l1_ratio=.2,max_iter=3000,random_state=SEED)),
 "svr":sc(SVR(C=1,epsilon=.01)),"random_forest":tr(RandomForestRegressor(n_estimators=150,min_samples_leaf=5,n_jobs=-1,random_state=SEED)),
 "extra_trees":tr(ExtraTreesRegressor(n_estimators=150,min_samples_leaf=5,n_jobs=-1,random_state=SEED)),
 "hist_gradient":tr(HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=15,random_state=SEED)),
 "mlp":sc(MLPRegressor(hidden_layer_sizes=(32,16),max_iter=150,early_stopping=True,random_state=SEED))}
 out.update(optional("Regressor"));return out
def classification_models():
 out={"logistic":sc(LogisticRegression(C=.1,max_iter=1500,class_weight="balanced",random_state=SEED)),
 "svm":sc(SVC(C=.5,probability=True,class_weight="balanced",random_state=SEED)),
 "random_forest":tr(RandomForestClassifier(n_estimators=150,min_samples_leaf=5,class_weight="balanced",n_jobs=-1,random_state=SEED)),
 "extra_trees":tr(ExtraTreesClassifier(n_estimators=150,min_samples_leaf=5,class_weight="balanced",n_jobs=-1,random_state=SEED)),
 "hist_gradient":tr(HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=15,random_state=SEED)),
 "mlp":sc(MLPClassifier(hidden_layer_sizes=(32,16),max_iter=150,early_stopping=True,random_state=SEED))}
 out.update(optional("Classifier"));return out
