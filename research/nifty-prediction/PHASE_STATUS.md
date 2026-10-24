# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Data provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly, but neither is exchange-certified and they may share upstream data. |
| P1 Baseline benchmark | COMPLETE | [Workflow run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) succeeded. |
| P2 Baseline statistical evaluation | COMPLETE FOR INITIAL BENCHMARK | On 1,157 holdout rows (2022-02-14 to 2026-10-22), previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy. Logistic regression, random forest and histogram gradient boosting did not establish an improvement. |
| P3 Simple candidate rules | SCREENING COMPUTED; AUTOMATED RUN PENDING | Added a bounded rule experiment for 3/5-session momentum, 1/3-session reversal, 20-session trend and a training-calibrated volatility-conditioned rule. Cached-data calculations show the simple previous-direction rule remains strongest overall; no candidate yet justifies a strategy claim. [Latest workflow run #37](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40142722883) was pending at last check and must finish to validate script execution and persist the report. |
| P4 Volatility model / uncertainty | GARCH EXPERIMENT IMPLEMENTED; AUTOMATED RUN PENDING | Added `evaluate_volatility_forecast.py` using `arch` GARCH(1,1), with daily recursive one-step variance updates and a QLIKE comparison against rolling and expanding variance baselines. Workflow updated to persist the output; latest workflow run is pending/queued behind the current benchmark. MAPIE calibration remains unrun. |
| P5 Seven repository integrations | SUBMODULES VERIFIED; AUDIT COMPLETE; OPTIONAL EXPERIMENTS QUEUED | All seven pinned submodules are present. Added `audit_repository_integrations.py` and [integration audit workflow](../../.github/workflows/repository-integration-audit.yml); run [#1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143973082) succeeded and persisted the package/submodule audit. Added a bounded chronological MAPIE experiment plus PySR/tick compatibility checks in [optional model workflow](../../.github/workflows/nifty-optional-models.yml); await its report before assigning model-level outcomes. `arch` has GARCH experiment results; MAPIE/PySR/tick still require dedicated predictive experiments. Quantevolve/TradingAgents remain research orchestration only; AstraQuant execution excluded. |
| P6 Costs and decision | NOT READY | Daily index proxy is not executable P&L. Any candidate must be evaluated with turnover, futures/options basis, brokerage, slippage, taxes/charges and realistic execution before a net strategy conclusion. |

## First candidate-rule screening (cached data; pending automated reproduction)

Common test interval: 2022-02-14 to 2026-10-22, 1,157 rows. These diagnostics use a daily long/short sign proxy and are **gross, before costs**.

| Rule | Accuracy | Balanced accuracy | Gross compounded index proxy |
|---|---:|---:|---:|
| Previous-session direction | 54.19% | 54.10% | +81.39% |
| 3-session momentum | 53.33% | 53.18% | +16.30% |
| 5-session momentum | 51.60% | 51.42% | +8.59% |
| 1-session mean reversion | 45.89% | 45.99% | -47.78% |
| 3-session mean reversion | 46.67% | 46.82% | -21.03% |
| 20-session trend filter | 54.19% | 53.90% | +20.64% |
| Volatility-conditioned momentum/reversal | 50.82% | 50.71% | -28.85% |

The gross proxy compounds daily direction-signed spot returns and is **not** a realizable futures/options return. Its numbers are not a claim of profit. Candidate screening does not identify a better directional rule than previous-session direction. The trend filter's directional accuracy ties the baseline but has lower balanced accuracy and weaker gross proxy performance.

## Next steps

1. Confirm workflow #37 completes and inspect the persisted `candidate_rules.json`.
2. Add deterministic tests for the candidate script and date alignment if the run reveals issues.
3. Use `arch` to forecast volatility (volatility score only), then test no more than one predeclared regime-conditioned direction rule.
4. Attempt PySR, `tick`, and MAPIE only through their documented compatibility gates; preserve failed attempts in the error log.
5. Verify the candidate-rule workflow output, then inspect the GARCH QLIKE results. Volatility forecast quality is not directional skill. Do not select a strategy until a candidate beats simple comparators on a fresh untouched forward period and net costs are modeled.

No tester review or tester branch is part of this work.
