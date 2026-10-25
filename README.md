# NIFTY 50 prediction — current research status

## Current status — 2026-10-25

The daily next-session benchmark, simple-rule screen, GARCH volatility comparison, seven-repository integration audit, optional-model compatibility workflow, dedicated weekly-expiry direction screen, and bounded OHLC hypothesis tranche have run. **No robust predictive edge has been established.**

- [Research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Weekly-expiry experiment protocol](research/nifty-prediction/WEEKLY_EXPIRY_DIRECTION_EXPERIMENTS.md)
- [Weekly-expiry experiment runner](research/nifty-prediction/evaluate_weekly_expiry.py)
- [Weekly-expiry experiment workflow](.github/workflows/nifty-weekly-expiry.yml)
- [Weekly-expiry result report](reports/nifty-prediction/weekly_expiry_experiments.json)
- [Weekly-expiry accuracy chart](reports/nifty-prediction/weekly_expiry_metrics.svg)
- [New hypothesis experiment runner](research/nifty-prediction/evaluate_new_hypotheses.py)
- [New hypothesis workflow](.github/workflows/nifty-new-hypotheses.yml)
- [New hypothesis results](reports/nifty-prediction/new_hypothesis_experiments.json)
- [Free historical data-source assessment](research/nifty-prediction/FREE_DATA_SOURCE_ASSESSMENT.md)
- [NSE options sample audit workflow](.github/workflows/nse-options-data-audit.yml)
- [NSE options sample audit report](reports/nifty-prediction/nse_options_sample_audit.json)
- [NSE options audit parser](research/nifty-prediction/audit_nse_options_sample.py)
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


## Free external-data source discovery

Official NSE report pages list daily derivatives bhavcopy, settlement, volatility, participant OI and FII derivatives reports; public archives and a Hugging Face dataset are additional candidates. These sources have **not yet been ingested or validated in this research**, so data-dependent hypotheses remain blocked. See the [source assessment](research/nifty-prediction/FREE_DATA_SOURCE_ASSESSMENT.md).

## New OHLC hypothesis tranche — completed screening

[Corrected workflow run #40146027941 succeeded](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40146027941). The full-feature logistic model scored 53.79% accuracy / 53.67% balanced accuracy on the reused chronological screening holdout. Volatility-regime specialists scored 52.60% balanced accuracy; core OHLC ablation scored 51.01%. Multi-horizon balanced accuracy was 52.58% (1 session), 48.03% (3 sessions), and 48.02% (5 sessions). Selective prediction retained 15.06% of cases at 53.37% balanced accuracy but had worse probability scores. These are exploratory results, not statistical confirmation or evidence of tradable edge.

- [Full machine-readable results](reports/nifty-prediction/new_hypothesis_experiments.json)
- [Research interpretation and limitations](research/nifty-prediction/MANUSCRIPT.md#8-new-ohlc-only-hypothesis-tranche-workflow-verified-2026-10-25)
- [Updated phase status](research/nifty-prediction/PHASE_STATUS.md)
- [Resolved workflow bug and open limitations](research/nifty-prediction/ERROR_LOG.md)


**Data-ingestion caution:** the initial NSE audit workflow successfully downloaded and parsed three official ZIP/CSV samples, but its first parser did not recognize several UDiFF column aliases. Treat this as transport/CSV-read success only; NIFTY option-row semantic validation remains pending (NP-022 in the error log).


## Weekly-expiry hypothesis suite — screening results

[Automated run #40163121234](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40163121234) completed. Added a dedicated weekly-expiry hypothesis runner and workflow. On the existing 231-observation test block, volatility-regime specialists scored 54.18% accuracy / 54.18% balanced accuracy; regularized logistic scored 52.38% / 52.69%; gradient boosting scored 51.52% / 49.11%. Selective prediction retained only 21/231 examples (9.1%) and scored 35.0% balanced accuracy. Residual probability correction reverted to the majority result (50.0% balanced accuracy). Multi-expiry horizon balanced accuracy: 48.40% (1 expiry), 50.11% (2), 53.26% (3). These are exploratory, repeated-screen results—not confirmatory evidence. The expiry calendar is still approximate.

- [Weekly-expiry hypothesis runner](research/nifty-prediction/evaluate_weekly_expiry_hypotheses.py)
- [Workflow](.github/workflows/nifty-weekly-expiry-hypotheses.yml)
- [Machine-readable results](reports/nifty-prediction/weekly_expiry_hypotheses.json)
