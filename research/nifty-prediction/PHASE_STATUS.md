# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25 (optional model run verified)

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Data provenance | COMPLETE WITH LIMITATION | 4,686 daily rows, 2007-09-17 to 2026-10-23. Yahoo and public parquet mirror OHLC match exactly, but neither is exchange-certified and they may share upstream data. |
| P1 Baseline benchmark | COMPLETE | [Workflow run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) succeeded. |
| P2 Baseline statistical evaluation | COMPLETE FOR INITIAL BENCHMARK | On 1,157 holdout rows (2022-02-14 to 2026-10-22), previous-session direction achieved 54.19% accuracy / 54.10% balanced accuracy. Logistic regression, random forest and histogram gradient boosting did not establish an improvement. |
| P3 Simple candidate rules | COMPUTED AND PERSISTED | The bounded rule experiment ran and its JSON report is persisted. Previous-session direction remains strongest among the tested simple rules; no candidate justifies a strategy claim. |
| P4 Volatility model / uncertainty | COMPUTED AND PERSISTED | The `arch` GARCH(1,1) forecast ran with recursive daily one-step variance updates and QLIKE comparison against rolling and expanding baselines. MAPIE calibration was attempted but skipped because of API mismatch. |
| P5 Seven repository integrations | SUBMODULES VERIFIED; AUDIT AND OPTIONAL RUN COMPLETE | All seven pinned submodules are present. Added `audit_repository_integrations.py` and [integration audit workflow](../../.github/workflows/repository-integration-audit.yml); run [#1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143973082) succeeded and persisted the package/submodule audit. The [optional model workflow](../../.github/workflows/nifty-optional-models.yml) completed successfully ([run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40144386537)) and persisted its report. Logistic regression on the same 60/15/25 split scored 53.59% accuracy / 53.31% balanced accuracy (1,157 test rows); this is below the 54.10% balanced accuracy of the previous-direction rule on the earlier benchmark and does not establish improvement. MAPIE 1.6.0 was skipped because the expected classifier entry point was not found; PySR 2.7.2 was importable but not fitted; tick 0.8.0.2 imported but has no predictive result. `arch` GARCH comparison is computed and persisted. Quantevolve/TradingAgents remain research orchestration only; AstraQuant execution excluded. |
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

1. Candidate-rule workflow output is persisted and the script ran successfully; keep its same-holdout numbers exploratory, not confirmation.
2. A new untouched forward interval and official data validation are needed before model promotion.
3. GARCH(1,1) QLIKE is -8.64595 versus -8.57379 for rolling 20-session variance and -8.22293 for expanding variance; modestly better volatility score, not direction skill.
4. MAPIE API mismatch and the deliberate PySR no-fit decision are logged; `tick` import succeeded only. No optional library has shown a directional gain.
5. Verify the candidate-rule workflow output, then inspect the GARCH QLIKE results. Volatility forecast quality is not directional skill. Do not select a strategy until a candidate beats simple comparators on a fresh untouched forward period and net costs are modeled.

No tester review or tester branch is part of this work.
