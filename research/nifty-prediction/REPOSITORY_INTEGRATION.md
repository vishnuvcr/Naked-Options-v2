# Repository integration plan — alternative NIFTY prediction stack

This file records the intended role of each project explicitly requested in the project instructions. It does not claim the projects have all been cloned, executed, or validated.

| Repository | Intended use | Current status / gate |
|---|---|---|
| [Quantevolve](https://github.com/tarsyang/quantevolve) | Optional evolutionary search over features/hyperparameters after the baselines; nested chronological validation only | Deferred until a valid benchmark and untouched holdout exist |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Research/agent orchestration for literature and event summaries; never the primary source of numeric forecast labels | Integration review pending; API keys and external data assumptions must be audited |
| [astra-quant-agent](https://github.com/0xethanq/astra-quant-agent) | Inspect quant-agent tools and data connectors for reuse | Integration review pending |
| [PySR](https://github.com/astroautomata/PySR) | Symbolic regression as an exploratory secondary model | Deferred; Julia/runtime setup and nested-validation safeguards required |
| [arch](https://github.com/bashtage/arch) | GARCH/ARCH conditional volatility forecasts, evaluated with volatility loss rather than direction accuracy | Optional dependency-version check added to workflow; not yet reported as installed or run |
| [tick](https://github.com/X-DataInitiative/tick) | Assess regularized models and survival/point-process tools where appropriate | Deferred pending maintenance and Python-version compatibility check |
| [MAPIE](https://github.com/scikit-learn-contrib/MAPIE) | Uncertainty sets/intervals only after a time-series-valid calibration protocol is selected | Optional dependency-version check added; not yet reported as installed or run |

## Initial implementation
- `acquire_daily_data.py`: cache-aware free-source daily NIFTY 50 data acquisition.
- `evaluate_daily_models.py`: chronological next-session direction evaluation with naive, logistic regression, random forest and histogram-gradient-boosting models.
- `tests/test_nifty_prediction_benchmark.py`: temporal alignment, invalid OHLC and bootstrap checks.
- `.github/workflows/nifty-prediction-benchmark.yml`: manual dispatch and code-change trigger, cached input data, tests, evaluation, artifact upload, optional ARCH/MAPIE dependency check.

## Guardrails
1. Daily Yahoo data is a starting point only, not exchange-certified.
2. This track predicts next-session daily direction; it does not answer expiry-specific or intraday questions.
3. No options/strategy/profitability claims are made.
4. No evolutionary search or model selection on the final holdout.
5. Report CI and actual workflow outcomes only after inspecting run artifacts.
