# NIFTY 50 Prediction — Phase Status

Updated: 2026-10-25

| Phase | Status | Evidence / blocker |
|---|---|---|
| P0 Scope/provenance | PARTIAL | Added 4,954-row third-party historical CSV (2000-01-03 to 2019-12-02), with zero duplicate dates and zero basic OHLC invariant failures. It is not exchange-certified and is stale for current-market claims. Production cache/workflow verification remains pending. |
| P1 Leakage-safe benchmark | PARTIAL RESULTS | A custom Node.js expanding logistic diagnostic and naive baselines produced preliminary historical results. The production Python/scikit-learn benchmark, unit tests, random forest, and gradient boosting remain unverified. |
| P2 Statistical evaluation | PRELIMINARY RESULTS RECORDED | Preliminary historical diagnostic: logistic balanced accuracy 52.78% (95% block-bootstrap interval 50.11–55.36%), versus previous-direction baseline 52.60% (49.72–55.56%). Intervals overlap; no robust edge established. Production results remain pending. |
| P3 Volatility/uncertainty | DEFERRED | Optional ARCH/MAPIE dependency audit workflow added. No GARCH or conformal results yet. |
| P4 Regime robustness/integration | DEFERRED | PySR, Quantevolve, TradingAgents, astra-quant-agent and tick integration is explicitly staged; avoid tuning before baseline and holdout validation. |
| P5 Manuscript/decision | DRAFTED, EMPIRICAL DECISION PENDING | Structured manuscript is now in MANUSCRIPT.md; no conclusion or model winner until real artifacts are inspected. |

## Immediate next gate
Confirm workflow tests pass, inspect the source manifest and daily benchmark JSON, verify train/test chronology and sample counts, then record actual results. If the free source acquisition or benchmark fails, log the error and repair the code without inventing scores.

## Scope note
This is a daily next-session direction benchmark. It does not yet evaluate expiry-specific direction, intraday predictions, option returns, or trading profitability. Daily Yahoo data is a free baseline, not an exchange-certified series.


## CI check — 2026-10-25
The GitHub commit-status endpoint returned no status entries for the new benchmark workflow commits, and the available commit-associated workflow-run query returned no runs. This does not prove the workflow did not trigger; it means the run could not be verified with the available interface. Keep benchmark result status as pending until a real artifact is inspected.


## Work performed — 2026-10-25
- Added an explicit zero-return directional baseline to the benchmark.
- Added a structured manuscript draft with research question, methodology, statistical analysis, results-pending section, strengths, limitations, conclusion gate, future work and reproducibility commands.
- Updated README links and model list.
- Attempted direct repository clone for local execution, but this environment could not resolve github.com. No local test/data run is claimed.


## Preliminary results acquired — 2026-10-25
- Dataset: 4,954 daily rows, 2000-01-03 to 2019-12-02, from a public third-party CSV mirror; not exchange-certified.
- Eligible rows after rolling-feature construction: 4,893; chronological split 3,669 train / 1,224 test; test 2014-12-16 to 2019-11-29.
- Custom logistic regression: 52.86% accuracy, 52.78% balanced accuracy, Brier 0.2494, log loss 0.6919.
- Previous-session-direction baseline: 52.78% accuracy, 52.60% balanced accuracy.
- Logistic balanced-accuracy improvement over previous-direction baseline is about 0.18 percentage points; bootstrap intervals overlap substantially.
- This is a preliminary diagnostic from a custom Node.js implementation, not the production scikit-learn benchmark. No trading strategy or current-market edge is established.
- Reproducible script: [preliminary_historical_diagnostic.js](preliminary_historical_diagnostic.js); report: [preliminary_historical_diagnostic.md](../../reports/nifty-prediction/preliminary_historical_diagnostic.md); JSON: [preliminary_historical_diagnostic.json](../../reports/nifty-prediction/preliminary_historical_diagnostic.json).
