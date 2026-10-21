# QuantEvolve NIFTY prediction specification.
# Evaluator AST-parses STRATEGY_SPEC and never executes this source.
# EVOLVE-BLOCK-START
STRATEGY_SPEC = {
    "version": 1,
    "track": "prediction",
    "model": "linear",
    "features": ["ret_1", "ret_5", "ret_20", "vol_5", "vol_20"],
    "weights": {
        "ret_1": 0.0,
        "ret_5": 0.0,
        "ret_20": 0.0,
        "vol_5": 0.0,
        "vol_20": 0.0,
    },
    "intercept": 0.0,
    "clip": 0.02,
}
# EVOLVE-BLOCK-END
