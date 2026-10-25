# NIFTY 50 prediction — current research status

## Current status — 2026-10-25

The daily next-session benchmark, simple-rule screen, GARCH volatility comparison, seven-repository integration audit, optional-model compatibility workflow, and dedicated weekly-expiry direction screen have run. **No predictive edge has been established.**

- [Research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Weekly-expiry experiment protocol](research/nifty-prediction/WEEKLY_EXPIRY_DIRECTION_EXPERIMENTS.md)
- [Weekly-expiry experiment runner](research/nifty-prediction/evaluate_weekly_expiry.py)
- [Weekly-expiry experiment workflow](.github/workflows/nifty-weekly-expiry.yml)
- [Weekly-expiry result report](reports/nifty-prediction/weekly_expiry_experiments.json)
- [Phase status](research/nifty-prediction/PHASE_STATUS.md)
- [Living manuscript](research/nifty-prediction/MANUSCRIPT.md)
- [Error log](research/nifty-prediction/ERROR_LOG.md)
- [Daily data acquisition](research/nifty-prediction/acquire_daily_data.py)
- [Baseline model benchmark](research/nifty-prediction/evaluate_daily_models.py)
- [Candidate rule experiment](research/nifty-prediction/evaluate_candidate_rules.py)
- [GARCH volatility forecast experiment](research/nifty-prediction/evaluate_volatility_forecast.py)
- [Seven-repository integration ledger](research/nifty-prediction/REPOSITORY_INTEGRATION.md)
- [Repository integration audit](.github/workflows/repository-integration-audit.yml)
- [Optional model experiment workflow](.github/workflows/nifty-optional-models.yml)
- [Daily benchmark workflow](.github/workflows/nifty-prediction-benchmark.yml)

## Daily next-session benchmark (not expiry-specific)

Common holdout: 1,157 observations from 2022-02-14 through 2026-10-22; up-session rate 52.20%.

| Model/rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority baseline | 52.20% | 50.00% |
| Previous-session direction | 54.19% | 54.10% |
| Logistic regression | 52.46% | 52.53% |
| Random forest | 50.56% | 50.44% |
| Histogram gradient boosting | 53.15% | 52.82% |

## Weekly-expiry direction screen

[Workflow run #6 succeeded](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40145451144), including unit tests and report persistence. The model predicts next observed weekly-expiry NIFTY spot direction from the prior observed expiry close, using daily OHLC-derived features only. Dataset: 923 examples; chronological train/test split 692/231; test UP rate 54.98%.

| Method | Accuracy | Balanced accuracy |
|---|---:|---:|
| Training-majority baseline | 54.98% | 50.00% |
| Previous expiry direction | 50.65% | 50.16% |
| Logistic regression | 50.65% | 50.76% |
| Random forest | 50.22% | 47.67% |
| Histogram gradient boosting | 52.81% | 49.86% |

**Conclusion:** no model establishes an expiry-direction edge; balanced accuracy is near 50%. The approximate expiry calendar is not validated against official holiday-adjusted contract dates. The data is third-party and not exchange-certified. This is not an options-premium or strategy-profitability test; slippage, brokerage, taxes and execution costs have not been evaluated because no strategy has survived prediction screening.

The study does not claim testing options-chain, intraday, breadth, global-market, FII/DII or news features because validated point-in-time historical inputs are not integrated. See the [manuscript](research/nifty-prediction/MANUSCRIPT.md) for methods and limitations.
