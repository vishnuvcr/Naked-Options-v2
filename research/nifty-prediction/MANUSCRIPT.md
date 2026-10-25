# NIFTY 50 Next-Session Direction Prediction — Research Manuscript (Living Draft)

**Updated:** 2026-10-25  
**Status:** Core benchmarks, candidate-rule screen, GARCH volatility comparison, and optional-model compatibility workflow completed. No strategy is validated.  
**Scope:** Daily next-session NIFTY 50 spot direction. No live trading or options profitability is established.

## Abstract

The baseline daily prediction workflow completed successfully in [GitHub Actions run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710). The third-party dataset has 4,686 daily rows from 2007-09-17 to 2026-10-23. The chronological holdout has 1,157 observations from 2022-02-14 to 2026-10-22. Previous-session direction achieved 54.19% accuracy and 54.10% balanced accuracy; logistic regression, random forest and histogram gradient boosting did not establish an improvement. A first screen of simple momentum, reversal, trend and volatility-conditioned rules also fails to identify a clearly superior candidate. The candidate-rule output is persisted in [candidate_rules.json](../../reports/nifty-prediction/candidate_rules.json); the gross proxy is not executable performance. All gross return proxies are pre-cost diagnostics, not executable strategy returns.

## 1. Research questions and objectives

1. Can daily OHLC-derived features predict next-session NIFTY 50 direction better than naive rules?
2. Do simple momentum, short-horizon reversal, trend and volatility-conditioned rules improve directional accuracy?
3. Does any surviving candidate retain value after realistic execution costs?
4. Which of the seven specified research repositories provides a method that can be adapted and empirically validated for this task?

## 2. Data and provenance

Primary source is Yahoo Finance daily NIFTY 50 (`^NSEI`), 4,686 rows from 2007-09-17 through 2026-10-23, SHA-256 `8d73f2b98d2109a5ccf6bfc6e85927de9f5c59ced889c188f6aa59a340079ab0`. A public parquet mirror matched all OHLC fields exactly across the same 4,686 dates. This is a parity check, not independent validation; both sources are third-party and may share upstream data. Neither is exchange-certified.

## 3. Methods

The target is the sign of next-session close-to-close return. The benchmark uses chronological expanding walk-forward fitting and evaluates a common 1,157-row final-quarter holdout. Candidate rules use information available at the current close: prior-session sign, 3- and 5-session momentum, 1- and 3-session reversal, close relative to a 20-session moving average, and a 20-session rolling-volatility regime. The regime cutoff is the 70th percentile of training-period volatility and is fixed before test scoring. Candidate screening is performed on the same date interval as the baseline.

Primary metric is balanced accuracy; accuracy and a simple daily long/short sign-of-return proxy are secondary diagnostics. The latter multiplies the next-session spot-index return by +1 or -1 according to predicted direction. It is gross and non-executable; it excludes instrument basis, costs, turnover, leverage, and execution constraints.

## 4. Verified initial model benchmark

| Model/rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority-class baseline | 52.20% | 50.00% |
| Previous-session direction | 54.19% | 54.10% |
| Logistic regression | 52.46% | 52.53% |
| Random forest | 50.56% | 50.44% |
| Histogram gradient boosting | 53.15% | 52.82% |

The previous-session direction rule has a 95% block-bootstrap balanced-accuracy interval of 51.30–56.81%. The learned models do not establish reliable improvement over that simple comparator.

## 5. First simple-rule screen

The automated candidate workflow computed and persisted these results on the common 1,157-row test interval.

| Rule | Accuracy | Balanced accuracy | Gross compounded sign proxy |
|---|---:|---:|---:|
| Previous-session direction | 54.19% | 54.10% | +81.39% |
| 3-session momentum | 53.33% | 53.18% | +16.30% |
| 5-session momentum | 51.60% | 51.42% | +8.59% |
| 1-session mean reversion | 45.89% | 45.99% | -47.78% |
| 3-session mean reversion | 46.67% | 46.82% | -21.03% |
| 20-session trend filter | 54.19% | 53.90% | +20.64% |
| Volatility-conditioned momentum/reversal | 50.82% | 50.71% | -28.85% |

Interpretation: neither momentum variant beats the previous-session direction baseline; reversal rules perform poorly; the trend filter ties raw accuracy but has lower balanced accuracy and lower gross sign-proxy performance. The volatility-conditioned rule does not help. The large gross proxy number for the baseline is not a trading result and cannot be used as evidence of profitability.

## 6. Volatility and optional-model experiments\n\nThe GARCH(1,1) forecast experiment used recursive daily variance updates with parameter refits every 20 sessions. QLIKE was -8.64595 for GARCH(1,1), -8.57379 for rolling 20-session variance, and -8.22293 for expanding unconditional variance (lower is better). This is a modest relative volatility-score improvement only; realized squared returns are noisy, and this result is not directional prediction skill. See [volatility forecast report](../../reports/nifty-prediction/volatility_forecast.json).\n\nA separate chronological 60/15/25 experiment on 4,626 valid feature rows scored logistic regression at 53.59% accuracy and 53.31% balanced accuracy over 1,157 test rows (2022-02-15 to 2026-10-23). The split differs slightly from the initial benchmark, so results should not be pooled. It does not establish a better model. MAPIE 1.6.0 conformal classification was skipped due to API mismatch; PySR 2.7.2 was importable but intentionally not fitted without a predeclared regression target; tick 0.8.0.2 imported only. See [optional-model report](../../reports/nifty-prediction/optional_model_experiments.json) and [workflow #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40144386537).\n\n## 7. Repository integration

Roles and compatibility guardrails for all seven named repositories are in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md): Quantevolve, TradingAgents, AstraQuant, PySR, `arch`, `tick`, and MAPIE. README review is complete; not every repository has been installed or empirically executed. Next experiments are a sepThe GARCH-family volatility forecast was scored separately using `arch`; optional MAPIE, PySR and tick experiments were bounded by compatibility and target-definition constraints.

## 9. Weekly-expiry direction experiment — implementation status

The user's primary target is NIFTY 50 spot direction into the upcoming weekly options expiry. The new dedicated runner defines an expiry-to-expiry forecast: at the close of one observed weekly expiry session, estimate whether the next weekly expiry close will be higher or lower. It compares a majority baseline, previous expiry direction, logistic regression, random forest, and histogram gradient boosting using a chronological split and expanding refits.

The experiment uses daily spot OHLC only. It does not yet test options-chain implied volatility/open interest, intraday opening pressure, global-market lead-lag, breadth, FII/DII flows, or event/news signals because validated point-in-time historical inputs have not been integrated. The weekday rule is approximate (Thursday before September 2025, Tuesday from September 2025); official holiday-adjusted expiry dates are not fully reconstructed. The script and unit tests are committed, and an automated/manual workflow is configured. **Results are pending workflow execution; no weekly-expiry accuracy or edge is claimed in this manuscript yet.**

- [Weekly-expiry experiment protocol](WEEKLY_EXPIRY_DIRECTION_EXPERIMENTS.md)
- [Weekly-expiry experiment runner](evaluate_weekly_expiry.py)
- [Weekly-expiry alignment tests](../../tests/test_nifty_weekly_expiry.py)
- [Weekly-expiry workflow](../../.github/workflows/nifty-weekly-expiry.yml)
- [Weekly-expiry result report, when produced](../../reports/nifty-prediction/weekly_expiry_experiments.json)
- [NSE circular FAOP/68747 on expiry schedule](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAOP68747.pdf)

## 10. Strengths and limitations

**Strengths:** reproducible baseline workflow; source hashes and parity audit; chronological evaluation; predeclared, interpretable rules; same test interval across comparators.

**Limitations:** third-party data not exchange-certified; exact source parity is not independent validation; candidate results use one holdout and are now screening results rather than untouched confirmation; gross index proxies are not executable P&L; no fees/slippage/execution model yet; daily bars do not validate intraday or expiry-specific options predictions.

## 11. Conclusion and next work

The current evidence does not identify a better simple direction rule than previous-session direction. No strategy is recommended at this stage. The daily next-session experiment set is complete for the currently available daily data and compatible tools. A separate weekly-expiry research track has now been added because daily next-session scores do not answer the user's weekly-expiry question. Its code and workflow are implemented, but no weekly-expiry results are claimed until the workflow has run successfully and its report has been inspected. The daily holdout has already been screened and is not an untouched confirmation set. Before any trading study, model Paytm Money/NSE-NFO brokerage, statutory charges, slippage, liquidity, instrument basis, turnover, sizing, and execution. No live trading is authorized or recommended.

## Reproducibility links

- [Initial benchmark run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710)
- [Optional-model experiment workflow #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40144386537)\n- [Repository integration audit #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143973082)
- [Benchmark JSON](../../reports/nifty-prediction/daily_benchmark.json)
- [Candidate rules JSON](../../reports/nifty-prediction/candidate_rules.json)
- [Source parity audit](../../reports/nifty-prediction/source_parity_audit.json)
- [Integration ledger](REPOSITORY_INTEGRATION.md)
- [Error log](ERROR_LOG.md)
