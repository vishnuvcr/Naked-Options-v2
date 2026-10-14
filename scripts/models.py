"""Fixed candidate models for NIFTY forecasting."""
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, ElasticNet, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, HistGradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
SEED=20261014
def scaled(m): return make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),m)
def tree(m): return make_pipeline(SimpleImputer(strategy="median"),m)
def regression_models():
    return {"ridge":scaled(Ridge(alpha=10.0)),
      "elastic_net":scaled(ElasticNet(alpha=.0005,l1_ratio=.2,max_iter=3000,random_state=SEED)),
      "svr":scaled(SVR(C=1.0,epsilon=.01)),
      "random_forest":tree(RandomForestRegressor(n_estimators=150,min_samples_leaf=5,n_jobs=-1,random_state=SEED)),
      "extra_trees":tree(ExtraTreesRegressor(n_estimators=150,min_samples_leaf=5,n_jobs=-1,random_state=SEED)),
      "hist_gradient":tree(HistGradientBoostingRegressor(max_iter=150,max_leaf_nodes=15,random_state=SEED)),
      "mlp":scaled(MLPRegressor(hidden_layer_sizes=(32,16),max_iter=150,early_stopping=True,random_state=SEED))}
def classification_models():
    return {"logistic":scaled(LogisticRegression(C=.1,max_iter=1500,class_weight="balanced",random_state=SEED)),
      "svm":scaled(SVC(C=.5,probability=True,class_weight="balanced",random_state=SEED)),
      "random_forest":tree(RandomForestClassifier(n_estimators=150,min_samples_leaf=5,class_weight="balanced",n_jobs=-1,random_state=SEED)),
      "extra_trees":tree(ExtraTreesClassifier(n_estimators=150,min_samples_leaf=5,class_weight="balanced",n_jobs=-1,random_state=SEED)),
      "hist_gradient":tree(HistGradientBoostingClassifier(max_iter=150,max_leaf_nodes=15,random_state=SEED)),
      "mlp":scaled(MLPClassifier(hidden_layer_sizes=(32,16),max_iter=150,early_stopping=True,random_state=SEED))}
