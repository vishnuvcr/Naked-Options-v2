# NIFTY prediction research error log

Updated: 2026-10-25. Preserve historical issues; mark resolutions explicitly rather than deleting entries.

## NP-001 — Daily source not exchange-certified (OPEN)
Primary source is Yahoo Finance; second source is a third-party parquet mirror. Both match OHLC exactly over 4,686 sessions, but may share upstream data. Seek official Nifty Indices/NSE cross-check before strong claims.

## NP-002 — Initial benchmark CI (RESOLVED)
Workflow [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) completed successfully, including tests, acquisition, parity audit, benchmark and artifact persistence.

## NP-003 — Scope mismatch with expiry study (RESOLVED BY NEW TRACK; expiry evidence pending)
The original study was daily next-session spot direction, not expiry-specific/intraday options prediction. A dedicated weekly-expiry experiment runner and workflow are now present. No weekly-expiry results are yet validated.

## NP-004 — External repositories are not all empirically executed (OPEN)
All seven READMEs have been reviewed and roles/guardrails recorded in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md). Review is not equivalent to installation or an experiment. Do not claim results for libraries without artifacts.

## NP-005 — Source agreement is not independent validation (OPEN)
Yahoo and public parquet mirror match exactly. Identical data does not prove accuracy or independence. Official source cross-check remains outstanding.

## NP-006 — Initial benchmark ML models do not beat the simple direction baseline (OPEN RESEARCH QUESTION)
Previous-session direction scored 54.10% balanced accuracy on the 1,157-row holdout; logistic regression 52.53%, random forest 50.44%, histogram gradient boosting 52.82%. Do not promote these fitted models as winners.

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
The new weekly-expiry runner detects Thursdays before 2025-09-01 and Tuesdays thereafter from daily OHLC dates. It does not ingest the authoritative contract-by-contract expiry calendar or holiday-shift records. This can miss holiday-adjusted expiry sessions and mislabel observations. The report must keep this limitation visible; before any strong claim, integrate official expiry dates and test the mapping. Source for the schedule change: NSE circular FAOP/68747, https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAOP68747.pdf.

## NP-016 — Weekly-expiry workflow execution and report review pending (OPEN)
Added `evaluate_weekly_expiry.py` and `.github/workflows/nifty-weekly-expiry.yml`. The workflow is configured for manual dispatch and relevant code changes. At this log update, no successful workflow run/report has been inspected, so no weekly-expiry metric is claimed. After execution, fix any script or workflow failures and record the actual results.

## NP-017 — Historical point-in-time feature data not yet integrated (OPEN)
Options-chain snapshots, intraday data, breadth/constituent history, global markets, FII/DII flows and event/news inputs are not yet validated as timestamped historical datasets. Do not infer historical features from current snapshots or claim these feature families were tested. Start with the data already available and add sources only when point-in-time integrity can be established.
