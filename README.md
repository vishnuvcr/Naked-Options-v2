# NIFTY 50 prediction — current research status

## Current status — 2026-10-25

The daily next-session direction benchmark, candidate-rule screen, GARCH volatility comparison, seven-repository integration audit, and optional-model compatibility workflow have completed. The optional experiment persisted its report in [workflow run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40144386537). No model or trading strategy is validated.

- [Research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Phase status](research/nifty-prediction/PHASE_STATUS.md)
- [Living manuscript](research/nifty-prediction/MANUSCRIPT.md)
- [Seven-repository integration ledger](research/nifty-prediction/REPOSITORY_INTEGRATION.md)- [Repository integration audit script](research/nifty-prediction/audit_repository_integrations.py)
- [Optional chronological model experiments](research/nifty-prediction/evaluate_optional_models.py)
- [Optional model experiment workflow](.github/workflows/nifty-optional-models.yml)
- [Repository integration audit results](reports/nifty-prediction/repository_integration_audit.json)
- [Optional model experiment results](reports/nifty-prediction/optional_model_experiments.json)\n- [Automated integration audit workflow](.github/workflows/repository-integration-audit.yml)\n- [Vendored upstream repositories](vendor/research-repositories)
- [Literature review](docs/research-literature/nifty_prediction_literature_review.md)
- [Daily data acquisition](research/nifty-prediction/acquire_daily_data.py)
- [Baseline model benchmark](research/nifty-prediction/evaluate_daily_models.py)
- [Candidate rule experiment](research/nifty-prediction/evaluate_candidate_rules.py)
- [GARCH volatility forecast experiment using `arch`](research/nifty-prediction/evaluate_volatility_forecast.py)
- [Volatility forecast results JSON](reports/nifty-prediction/volatility_forecast.json)
- [Source parity audit](research/nifty-prediction/audit_source_parity.py)
- [Error log](research/nifty-prediction/ERROR_LOG.md)
- [Baseline results JSON](reports/nifty-prediction/daily_benchmark.json)
- [Candidate results JSON](reports/nifty-prediction/candidate_rules.json)
- [Source parity JSON](reports/nifty-prediction/source_parity_audit.json)
- [Workflow](.github/workflows/nifty-prediction-benchmark.yml)

## Optional model and volatility results\n\n- Separate chronological 60/15/25 logistic experiment: 53.59% accuracy and 53.31% balanced accuracy on 1,157 test observations; no demonstrated improvement.\n- MAPIE 1.6.0: conformal classifier skipped due to API mismatch.\n- PySR 2.7.2: available but not fitted because no predeclared continuous target was specified.\n- tick 0.8.0.2: import succeeded only; no predictive model evaluated.\n- GARCH(1,1) QLIKE -8.64595 vs rolling 20-session variance -8.57379 and expanding variance -8.22293. Volatility forecast score only, not direction skill.\n\n## Baseline results

Common holdout: 1,157 observations from 2022-02-14 through 2026-10-22; up-session rate 52.20%.

| Model/rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority baseline | 52.20% | 50.00% |
| Previous-session direction | 54.19% | 54.10% |
| Logistic regression | 52.46% | 52.53% |
| Random forest | 50.56% | 50.44% |
| Histogram gradient boosting | 53.15% | 52.82% |

## First simple-rule screen (gross, provisional)

| Rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Previous-session direction | 54.19% | 54.10% |
| 3-session momentum | 53.33% | 53.18% |
| 5-session momentum | 51.60% | 51.42% |
| 1-session mean reversion | 45.89% | 45.99% |
| 3-session mean reversion | 46.67% | 46.82% |
| 20-session trend filter | 54.19% | 53.90% |
| Volatility-conditioned momentum/reversal | 50.82% | 50.71% |

No candidate has yet beaten the previous-session direction comparator. All gross return proxies exclude executable instrument basis, brokerage, taxes/charges, slippage, turnover and execution. They are not strategy P&L. Source is third-party and not exchange-certified. The GARCH(1,1) forecast and optional-model workflow have completed; results and skips are recorded in the linked JSON reports.

## Required repositories

All seven requested repositories and their scope restrictions are documented in the [integration ledger](research/nifty-prediction/REPOSITORY_INTEGRATION.md): [Quantevolve](https://github.com/tarsyang/quantevolve), [TradingAgents](https://github.com/TauricResearch/TradingAgents), [AstraQuant](https://github.com/0xethanq/astra-quant-agent), [PySR](https://github.com/astroautomata/PySR), [arch](https://github.com/bashtage/arch), [tick](https://github.com/X-DataInitiative/tick), [MAPIE](https://github.com/scikit-learn-contrib/MAPIE). All seven submodule pointers are confirmed. The integration audit workflow checked out all seven pinned sources, installed stable libraries, ran the audit, and persisted the report successfully in [run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143973082). A second automated workflow now attempts chronological MAPIE calibration and records PySR/tick compatibility outcomes. `arch` has an active GARCH volatility experiment; MAPIE was skipped due to API mismatch, PySR was not fitted, and tick was import-tested only; none has a predictive result. Quantevolve and TradingAgents are bounded research-orchestration references, while AstraQuant's crypto execution layer is explicitly excluded. See the integration ledger for exact status; checkout or dependency installation alone is not evidence of predictive value.

## Safeguards

- Chronological evaluation; no random splits or look-ahead.
- Do not tune against the final test interval; after screening on it, require a new untouched forward period for confirmation.
- Log failures and limitations in the error log.
- No profitable-strategy claim until realistic Paytm Money/NSE-NFO costs, slippage, liquidity and execution timing are included.
- No tester reviews or tester branches.
