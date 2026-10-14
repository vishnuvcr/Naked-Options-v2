"""Explicit compute-budget rules for the preregistered model catalogue."""
FULL_CATALOGUE = {("return", 1), ("direction", 1)}
CORE_REGRESSION = {"ridge", "elastic_net", "random_forest", "hist_gradient"}
CORE_CLASSIFICATION = {"logistic", "random_forest", "hist_gradient"}

def allowed_candidates(task, horizon, kind, candidates):
    """Return model IDs allowed for a target/horizon and the policy label."""
    names=set(candidates)
    if (task, int(horizon)) in FULL_CATALOGUE:
        return names, "FULL_CATALOGUE"
    core=CORE_REGRESSION if kind=="reg" else CORE_CLASSIFICATION
    return names & core, "CORE_SCREEN"

def exclusion_reason(task, horizon, kind):
    return (
        "Bounded screening amendment: full model catalogue is compared for next-session "
        "return and direction; other target/horizon cells use Ridge/ElasticNet/RandomForest/"
        "HistGradientBoosting (regression) or Logistic/RandomForest/HistGradientBoosting "
        "(classification). Every excluded candidate is explicitly statused BLOCKED_COMPUTE_BUDGET."
    )
