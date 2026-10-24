# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Scope/provenance | COMPLETE WITH LIMITATION | Primary daily dataset: 4,686 rows, 2007-09-17 through 2026-10-23. SHA-256 and provenance are recorded. Yahoo and public-parquet mirror OHLC match exactly, but the mirror is not independent validation and neither source is exchange-certified. Seek official-source cross-check before strong conclusions. |
| P1 Leakage-safe benchmark | COMPLETE | GitHub Actions run [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) succeeded, including tests, acquisition, source parity audit, benchmark and artifact persistence. |
| P2 Statistical evaluation | COMPLETE FOR INITIAL BASELINE; STRATEGY RESEARCH ACTIVE | Holdout: 1,157 observations, 2022-02-14 to 2026-10-22; up-rate 52.20%. Previous-session direction: 54.19% accuracy / 54.10% balanced accuracy (block-bootstrap CI 51.30–56.81%). Logistic regression: 52.46% accuracy / 52.53% balanced accuracy; random forest: 50.56% / 50.44%; histogram gradient boosting: 53.15% / 52.82%. Learned models do not establish a reliable improvement over the previous-direction rule. |
| P3 Volatility and uncertainty | NOT RUN | Repository review completed for `arch` and MAPIE. Next: one GARCH-family volatility forecast with appropriate volatility loss, and a chronological calibration/coverage experiment only if compatible dependencies and data contracts pass. |
| P4 Hypothesis-driven candidate rules | ACTIVE | Next: small predeclared momentum, short-horizon mean-reversion and one lagged-volatility-conditioned candidate. Compare on the same dates and against simple baselines; if any survives, evaluate realistic turnover and costs. |
| P5 External repository integration | REVIEW COMPLETE; EXECUTION PARTIAL/PENDING | README review completed for Quantevolve, TradingAgents, astra-quant-agent, PySR, arch, tick and MAPIE. Their concrete use and scope restrictions are documented in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md). Do not claim all repositories have been installed/executed; each has its own compatibility or suitability gate. |
| P6 Manuscript and decision | LIVING DRAFT | Manuscript needs benchmark results and the candidate-rule experiment added; no validated profitable strategy is claimed yet. |

## What the benchmark says

The initial models do not provide evidence of a reliable machine-learning edge over the previous-session direction rule. This does **not** prove that no strategy can work. It means the next bounded step is to test a small number of explicit, low-complexity rules and reject candidates that do not beat simple comparators after costs.

## Verified workflow

- Run: [GitHub Actions #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710)
- Outcome: success for both jobs.
- Output files: [daily benchmark JSON](../../reports/nifty-prediction/daily_benchmark.json), [source parity audit](../../reports/nifty-prediction/source_parity_audit.json), [source manifest](../../data/cache/nifty-prediction/source_manifest.json).

## Repository review gate

All seven repository READMEs have been inspected. Integration is not assumed to mean direct installation: AstraQuant's OKX-native crypto executor is unsuitable for NSE/NFO execution; Quantevolve's Binance-oriented collector is not a NIFTY data source; `tick`, PySR and MAPIE require compatibility/calibration checks; `arch` is for volatility modeling; TradingAgents is research orchestration, not numeric ground truth.

## Scope and safeguards

This track predicts daily next-session NIFTY spot direction first. It is not yet an expiry-specific or intraday evaluation. A candidate trading rule is not usable until point-in-time data, turnover, slippage, brokerage, taxes/charges and execution timing are evaluated. Do not optimize on the final holdout or report gross returns as net returns.
