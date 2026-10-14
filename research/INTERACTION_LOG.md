# Auditable activity / interaction log

Record user-facing decisions, concrete operations, results and links. This is not a verbatim transcript and must never contain private internal reasoning or hidden chain-of-thought.

## 2026-10-14 — initialization

- User requested fresh NIFTY 50 prediction research; no trading-strategy development; nine fixed phases; broad model comparison; robust statistics; separate developer/tester branches; manuscript; automated workflows and logs.
- Checked GitHub metadata for vishnuvcr/Naked-Options-v2. Repository is public, default branch main, initially reported size 0. README retrieval returned not found. Branch search returned no branches.
- Initialized README.md; first commit SHA returned by GitHub was e0b634fdb98da9a2ed136320a24afb7fdda8afb9.
- Searched the Project Library for previous studies and literature. Found a NIFTY ML paper in Cureus Journal of Computer Science (published 2026-10-01) and prior manuscripts from other research repositories. Read selected methods/results/limitations/reference pages. Treated these as contextual literature, not fresh output from this repository.
- Researched official NSE NIFTY 50 and India VIX pages, NSE historical reports, Dhan API support docs, NIFTY forecasting papers, Diebold-Mariano and Clark-West tests, White's Reality Check and data-snooping / PBO literature.
- Created the frozen research plan, questions, literature matrix, data catalog, experiment log, preliminary results register, phase status, error log, tester checklist, manuscript shell and reproducibility guide.
- At this checkpoint no source data API has been called, no market dataset has been acquired, no model has been trained, and no Actions run or Pages deployment is claimed.

## Interaction summary policy

Log actions and outcomes rather than private reasoning or a word-for-word chat transcript. If a workflow later runs, record its actual run ID / URL and status. If it fails or is not observable, state that honestly.

## 2026-10-14 — bounded run #41, source outcome, and merge repair

- Verified Actions run #41 at commit 277758e43cadcef819672f4c1567660c683b5a2e. Dhan daily target manifest: 4,901 observations, 2007-01-02 through 2026-10-13, SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. Target quality gate passed with 20 weekend-dated records preserved as flagged possible special sessions.
- Dhan vs Yahoo NIFTY cross-check overlapped on 4,679 dates; median absolute close difference 0.0001953, maximum 0.0007813 in the normalized data representation. No rows were silently blended.
- The acquisition manifest reported seven validated external sources: S&P 500 (4,976 rows), Nasdaq (4,976), Nikkei 225 (4,833), Hang Seng (4,870), CBOE VIX (4,978), India VIX (4,560), and U.S. 10-year yield proxy (4,974), with histories extending from 2007 (India VIX from 2008) to 2026-10-13. USD/INR failed on 237 OHLC-range rows; gold failed on 149 OHLC-range rows; WTI failed the generic positive-price check. These three were not used as predictors.
- Feature matrix passed: 4,901 rows and 106 feature columns. Tests passed. Technical run JSON reported COMPLETE, 278 experiment rows and 72,253 OOS prediction rows; sequence status PASS for LSTM/GRU/TCN/Transformer restricted to one-session return and direction at three epochs. Global-augmented run JSON reported COMPLETE, 210 experiment rows and 64,413 OOS predictions.
- ARIMA(1,0,0) benchmark completed. The retained generated file reports OOS n = 980/976/961 for 1/5/20 sessions, OOS R² vs zero return of -0.003482/0.001095/0.010657, and raw HAC p-values 0.4917/0.9351/0.8420; all loss-difference CIs include zero. These figures are provisionally recorded in RESULTS.md.
- The final step of Actions run #41 failed in merge_results.py with pandas EmptyDataError. The available artifact contained 10 files (manifests/run JSON and ARIMA files) but omitted technical/global per-run CSVs, so a best-model ranking cannot be recovered from that artifact. The merge failure appears to be a blank no-error table, not an absence of global features; earlier explanatory wording was corrected in this log.
- Fixed merge empty-file parsing/status; workflow artifact paths now include per-run CSVs, predictions, errors, and research logs. Reviewed volatility metric math and corrected the QLIKE skill formula to a nonnegative equivalent loss, with an arithmetic unit test.
- Corrected run #45 is pending at commit c11ee9b408473cb2279e76a7e8a2b98a8a88b011. No technical/sequence model ranking is accepted until that run completes and its CSV artifact is checked. No hidden reasoning or verbatim private transcript is stored.
