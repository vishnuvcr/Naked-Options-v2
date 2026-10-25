# NIFTY 50 prediction — current research status

## Current status — 2026-10-25

The existing daily next-session benchmark, simple-rule screen, GARCH volatility comparison, seven-repository integration audit, and optional-model compatibility workflow are complete. They do not validate weekly-expiry prediction. The dedicated weekly-expiry protocol and experiment runner are now added; results remain pending execution.

- [Research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Weekly-expiry experiment protocol](research/nifty-prediction/WEEKLY_EXPIRY_DIRECTION_EXPERIMENTS.md)
- [Weekly-expiry experiment runner](research/nifty-prediction/evaluate_weekly_expiry.py)
- [Weekly-expiry experiment workflow](.github/workflows/nifty-weekly-expiry.yml)
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

## Existing daily benchmark (not expiry-specific)

Common holdout: 1,157 observations from 2022-02-14 through 2026-10-22; up-session rate 52.20%.

| Model/rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority baseline | 52.20% | 50.00% |
| Previous-session direction | 54.19% | 54.10% |
| Logistic regression | 52.46% | 52.53% |
| Random forest | 50.56% | 50.44% |
| Histogram gradient boosting | 53.15% | 52.82% |

No candidate has established a reliable edge. Existing gross index sign proxies are not executable strategy P&L and exclude realistic costs.

## Weekly-expiry research scope

The new experiment defines a separate expiry-day task using daily spot OHLC and an explicitly approximate historical weekday schedule: Thursday before September 2025 and Tuesday from September 2025, based on [NSE circular FAOP/68747](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAOP68747.pdf). The script flags the calendar as unverified because it does not yet ingest an authoritative contract-by-contract holiday-adjusted expiry calendar. It does not pretend to evaluate historical options-chain, intraday, breadth, global-market, FII/DII, or news features without point-in-time data.

The new workflow is configured for automatic runs on relevant code changes and manual dispatch. No weekly-expiry model is validated until the run and persisted JSON results are inspected. No tester branch or tester review is part of this project.
