import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from experiment_budget import allowed_candidates

def test_full_catalogue_is_preserved_for_primary_horizons():
    names={"ridge","elastic_net","svr","random_forest","extra_trees","hist_gradient","mlp","xgboost","seq_lstm"}
    allowed,mode=allowed_candidates("return",1,"reg",names)
    assert allowed==names and mode=="FULL_CATALOGUE"
    allowed,mode=allowed_candidates("direction",1,"cls",names)
    assert allowed==names and mode=="FULL_CATALOGUE"

def test_other_regression_cells_use_explicit_core_budget():
    names={"ridge","elastic_net","svr","random_forest","extra_trees","hist_gradient","mlp","xgboost"}
    allowed,mode=allowed_candidates("volatility",5,"reg",names)
    assert allowed=={"ridge","elastic_net","random_forest","hist_gradient"}
    assert mode=="CORE_SCREEN"
    assert names-allowed=={"svr","extra_trees","mlp","xgboost"}

def test_other_classification_cells_use_explicit_core_budget():
    names={"logistic","svm","random_forest","extra_trees","hist_gradient","mlp","catboost"}
    allowed,mode=allowed_candidates("direction",20,"cls",names)
    assert allowed=={"logistic","random_forest","hist_gradient"}
    assert mode=="CORE_SCREEN"
