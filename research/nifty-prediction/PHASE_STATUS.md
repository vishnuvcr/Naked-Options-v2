# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25

| Phase | Status | Evidence / next action |
|---|---|---|
| P0 Scope/provenance | COMPLETE WITH LIMITATION | Primary daily dataset: 4,686 rows, 2007-09-17 through 2026-10-23. SHA-256 and provenance are recorded. Yahoo and public-parquet mirror OHLC match exactly, but the mirror is not independent validation and neither source is exchange-certified. Seek official-source cross-check before strong conclusions. |
| P1 Leakage-safe benchmark | COMPLETE | GitHub Actions run [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) succeeded, including tests, acquisition, source parity audit, benchmark and artifact persistence. |
| P2 Statistical evaluation | COMPLETE FOR INITIAL BASELINE; STRATEGY RESEARCH ACTIVE | Holdout: 1,157 observations, 2022-02-14 to 2026-10-22; up-rate 52.20%. Previous-session direction: 54.19% accuracy / 54.10% balanced accuracy (block-bootstrap CI 51.30–56.81%). Logistic regression: 52.46% accuracy / 52.53% balanced accuracy; random forest: 50.56% / 50.44%; histogram gradient boosting: 53.15% / 52.82%. Learned models do not establish a reliable improvement over the previous-direction rule. |
| P3 Volatility and uncertainty | PENDING / OPTIONAL | Repository review completed for `arch` and MAPIE. Next: one GARCH-family volatility forecast with appropriate volatility loss, and a chronological calibration/coverage experiment only if compatible dependencies and data contracts pass. |
| P4 Hypothesis-driven candidate rules | AUTOMATED RUN PENDING | Added a fixed candidate set: 3-session momentum, 5-session momentum, 1-session reversal, 3-session reversal, 20-session trend filter, and lagged-volatility-conditioned rule. A preliminary diagnostic is saved at reports/nifty-prediction/candidate_rules_preliminary.json; automated Python confirmation is pending. |
| P5 External repository integration | REVIEW COMPLETE; EXECUTION PARTIAL/PENDING | README review completed for Quantevolve, TradingAgents, astra-quant-agent, PySR, arch, tick and MAPIE. Their concrete use and scope restrictions are documented in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md). Do not claim all repositories have been installed/executed; each has its own compatibility or suitability gate. |
| P6 Manuscript and decision | LIVING DRAFT | Baseline results are verified. Candidate-rule report is pending the new automated run; no validated profitable strategy is claimed yet. |

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


## Latest concrete update (2026-10-25)

- Verified Actions run #34 passed both jobs and all main benchmark steps; this supersedes older error-log entries saying that benchmark execution was unverified.
- Added `evaluate_candidate_rules.py` and wired it into the same workflow; the next run must generate `reports/nifty-prediction/candidate_rules.json`.
- No tester, tester branch, or tester review is part of this research.


## Preliminary candidate-rule result (same 1,157-session holdout)

| Rule | Accuracy | Balanced accuracy | Gross long/short index proxy, compounded |
|---|---:|---:|---:|
| Previous-session direction | 54.19% | 54.10% | +81.39% |
| 3-session momentum | 53.33% | 53.18% | +16.30% |
| 5-session momentum | 51.60% | 51.42% | +8.59% |
| 1-session reversal | 45.89% | 45.99% | -47.78% |
| 3-session reversal | 46.67% | 46.82% | -21.03% |
| 20-session trend filter | 54.19% | 53.90% | +20.64% |
| Volatility-conditioned rule | 51.34% | 51.22% | -21.10% |

These are preliminary calculations on the committed third-party CSV. Gross long/short index proxy returns are not executable net returns and exclude all trading costs. No new candidate beats the previous-session-direction baseline in balanced accuracy. The 20-session trend filter is the best of the new rules but is still below the baseline; it is not validated as a usable strategy. The automated Python report must confirm these numbers before final publication.
