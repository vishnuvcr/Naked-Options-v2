# NIFTY prediction research error log

Updated: 2026-10-25. Preserve historical issues; mark resolutions explicitly rather than deleting entries.

## NP-001 — Daily source not exchange-certified (OPEN)
Primary source is Yahoo Finance; second source is a third-party parquet mirror. Both match OHLC exactly over 4,686 sessions, but may share upstream data. Seek official Nifty Indices/NSE cross-check before strong claims.

## NP-002 — Initial benchmark CI (RESOLVED)
Workflow [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) completed successfully, including tests, acquisition, parity audit, benchmark and artifact persistence.

## NP-003 — Scope mismatch with expiry study (RESOLVED BY NEW TRACK)
The original study was daily next-session spot direction, not expiry-specific/intraday options prediction. Dedicated weekly-expiry experiment is now computed; it did not establish an edge.

## NP-004 — External repositories are not all empirically executed (OPEN)
All seven READMEs have been reviewed and roles/guardrails recorded in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md). Review is not equivalent to installation or an experiment. Do not claim results for libraries without artifacts.

## NP-005 — Source agreement is not independent validation (OPEN)
Yahoo and public parquet mirror match exactly. Identical data does not prove accuracy or independence. Official source cross-check remains outstanding.

## NP-006 — Initial benchmark ML models do not beat the simple direction baseline (OPEN RESEARCH QUESTION)
Previous-session direction scored 54.10% balanced accuracy on the 1,157-row daily holdout; logistic regression 52.53%, random forest 50.44%, histogram gradient boosting 52.82%. Do not promote these fitted models as winners.

## NP-007 — Trading costs not modeled (OPEN)
All current results are prediction or gross index proxies. No strategy is viable until turnover, realistic execution, slippage, brokerage, taxes/charges and relevant futures/options basis are modeled.

## NP-008 — Optional package integration limitations (PARTIALLY RESOLVED)
The optional experiment workflow succeeded. GARCH scoring is persisted; MAPIE calibration was skipped due to API mismatch; PySR and tick were not fitted. Quantevolve and TradingAgents remain orchestration references. AstraQuant's OKX-native crypto executor is not an NSE/NFO adapter.

## NP-009 — Candidate workflow result persistence (RESOLVED)
The candidate-rule workflow completed and its JSON result is persisted. The screen remains exploratory and no rule establishes an edge.

## NP-010 — Gross index proxy can be mistaken for tradable performance (OPEN)
Candidate screen multiplies next-session spot-index return by a long/short direction sign. This ignores executable instrument basis, lot sizing, turnover, margin, slippage, brokerage, taxes and execution. It is only a diagnostic; never describe its compounded value as strategy P&L.

## NP-011 — Artifact persistence race during candidate workflow (RESOLVED IN WORKFLOW)
An earlier run failed during persistence after scientific calculations completed. Persistence was updated to fetch/rebase before staging and retry rejected pushes. Subsequent benchmark workflow completed and reports are persisted.

## NP-012 — Concurrent branch push rejected during persistence (RESOLVED IN WORKFLOW)
Workflow now fetches/rebases before staging and retries push up to three times. Reports from subsequent successful run are persisted.

## NP-013 — Optional-model experiment completion (RESOLVED AS REPORTED; no model promotion)
The optional workflow succeeded. Logistic regression achieved 53.59% accuracy and 53.31% balanced accuracy on its separate chronological test. MAPIE 1.6.0 did not expose the expected classifier entry point; PySR imported but was not fitted; tick import succeeded only. No optional model result demonstrates a directional edge.

## NP-015 — Weekly-expiry calendar is approximate (OPEN)
The weekday rule uses Thursday before September 2025 and Tuesday thereafter, but does not ingest authoritative holiday-adjusted contract-by-contract dates. This can skip holiday-shifted expiry sessions and mislabel intervals. Source: NSE circular FAOP/68747, https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAOP68747.pdf.

## NP-016 — Weekly-expiry workflow execution (RESOLVED; scientific limitations remain)
Workflow [#6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40145451144) succeeded, including unit tests, experiment calculation, report persistence and artifact upload. The initial failed runs uncovered an undefined counter variable; it was fixed and tests now pass. Results are in [weekly_expiry_experiments.json](../../reports/nifty-prediction/weekly_expiry_experiments.json). Results are exploratory because the expiry calendar is approximate.

## NP-017 — Historical point-in-time feature data not yet integrated (OPEN)
Options-chain snapshots, intraday data, breadth/constituent history, global markets, FII/DII flows and event/news inputs are not yet validated as timestamped historical datasets. Do not infer historical features from current snapshots or claim these feature families were tested.

## NP-018 — Weekly-expiry model performance is near chance (RESEARCH RESULT; NO EDGE)
On 231 chronological test examples, majority baseline accuracy was 54.98% (balanced accuracy 50.00%); previous expiry direction 50.65% accuracy / 50.16% balanced accuracy; logistic regression 50.65% / 50.76%; random forest 50.22% / 47.67%; histogram gradient boosting 52.81% / 49.86%. No model materially beats the majority baseline and balanced accuracy is near chance. Do not infer tradable or options-premium edge.

## NP-019 — Proposed novel prediction methods were not initially executed (RESOLVED BY IMPLEMENTATION; RESULTS PENDING)
The earlier response listed ten research ideas but did not implement them. A bounded OHLC-only runner and a manual/automatic workflow have now been added. The run must be inspected before reporting any performance. External-data methods remain explicitly blocked where point-in-time history is absent; residual correction is deferred pending leakage-safe OOF design.

## NP-020 — Multi-horizon training-label alignment bug (RESOLVED; rerun pending)
The first new-hypothesis workflow failed because each 1/3/5-session horizon fit paired training features with test labels (sample counts differed). The fit call now uses the matching training labels; the subsequent workflow run must confirm the full report and persistence. No model metrics were produced by the failed run.


## NP-020 — Multi-horizon label alignment bug (RESOLVED)
The first new-hypothesis workflow run failed because the multi-horizon estimator was fitted with training features paired to test labels (3,483 vs 1,161 rows). Corrected the fit target to the training frame's aligned horizon label and reran successfully in [workflow #40146027941](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40146027941). The report is persisted at [new_hypothesis_experiments.json](../../reports/nifty-prediction/new_hypothesis_experiments.json). The initial failed run is retained in [workflow #40145950780](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40145950780).

## NP-021 — New OHLC hypothesis tranche shows no clear predictive edge (OPEN RESEARCH LIMITATION)
The successful chronological screening run reports 53.79% accuracy / 53.67% balanced accuracy for full-feature logistic regression; volatility specialists scored 52.60% balanced accuracy; 3- and 5-session balanced accuracy were below 50%; selective prediction covered 15.06% at 53.37% balanced accuracy and worse Brier/log loss than the full-feature model. This is a reused screening holdout, not an untouched confirmation set; no statistical-significance or trading-edge claim is made.

## NP-022 — NSE schema smoke test overstated semantic validation (OPEN)
The initial NSE sample workflow downloaded and parsed three official ZIPs, but its first parser only scanned the first 10,000 rows and did not recognize UDiFF aliases such as `TckrSymb`, `OptnTp`, `StrkPric`, and `TradDt`. The persisted `ALL_SAMPLES_PARSED` status establishes ZIP/CSV readability only, not NIFTY options-row validation or canonical legacy-to-UDiFF mapping. Do not use this report as proof of semantic validity. Correct alias mapping, scan full files for NIFTY CE/PE rows, and require explicit semantic assertions. Workflow: [#40162669263](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40162669263).

## NP-023 — Weekly-expiry hypothesis suite has no confirmatory winner (OPEN RESEARCH LIMITATION)
The first dedicated hypothesis suite completed in [workflow #40163121234](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40163121234). On the existing 231-row test block, volatility-regime specialists achieved 54.18% balanced accuracy, logistic regression 52.69%, gradient boosting 49.11%, and 3-expiry horizon 53.26%. Selective prediction covered only 9.1% and had 35.0% balanced accuracy; residual probability correction had 50.0% balanced accuracy. The apparent regime result is screening-only: the test block has been reused, the expiry calendar is approximate, and no confidence interval or untouched confirmation is included. Global lead-lag, breadth, options-implied, opening-pressure and event-aware families remain blocked for lack of validated point-in-time datasets. Do not promote a winner or infer options profitability.
