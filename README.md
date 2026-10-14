# Fresh NIFTY 50 Prediction Research

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Phase 5 is running under a bounded, auditable execution plan; first full model fits completed, but the results merge is being repaired.

## Repository audit

The repository was empty at project start: no readable README, files, branches, commits, datasets, experiment logs, or workflows. This project therefore starts a new research record without overwriting prior repository work. Relevant prior literature available in the ChatGPT Project library is cited in `research/LITERATURE_REVIEW.md`; it is not treated as this project's validated experimental output.

## Research navigation

- [Research plan](research/RESEARCH_PLAN.md)
- [Research questions and hypotheses](research/RESEARCH_QUESTIONS.md)
- [Literature review](research/LITERATURE_REVIEW.md)
- [Data catalog](research/DATA_CATALOG.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Results](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](research/TESTER_REPORT.md)
- [Scientific manuscript](research/MANUSCRIPT.md)
- [Reproducibility guide](research/REPRODUCIBILITY.md)
- [Execution policy and phase-branch rules](research/EXECUTION_POLICY.md)

## Phase branches

Historical checkpoint branches for completed setup phases and the active model branch are available: [Phase 1](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-1-audit), [Phase 2](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-2-literature), [Phase 3](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-3-data), [Phase 4](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-4-baselines), and [Phase 5](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-models). The resource-bounded execution branch is [research/phase-5-bounded](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-bounded). Future phase branches will be created only after their predecessor gate passes.

## Scientific integrity

No model will be declared best from training fit, shuffled validation, price-level R² alone, or a reused test set. Return, directional, volatility, and level targets will be evaluated separately with chronological walk-forward evaluation, simple benchmarks, uncertainty estimates, and multiplicity control. Results unavailable because of data, credentials, compute, or workflow restrictions will be marked **blocked/not run**, never imputed or fabricated.

## Current summary

- Repository bootstrap and protocol: complete for NIFTY-PRED-1.0; original repository was empty at audit.
- Daily target data: Dhan cache verified with 4,901 rows (2007-01-02 to 2026-10-13), SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. Weekend-dated bars are now warnings, not automatically removed.
- Data-quality tests and feature matrix: passed on the latest inspected workflow steps; feature/test build is verified.
- Model experiments: Actions run [#41](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38526229786) completed technical and global model fitting (278 technical and 210 global experiment records) but failed while merging because an empty error CSV was parsed. Per-run CSVs were not included in its artifact, so no model ranking is accepted. The corrected run [#45](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38527508857) includes safe empty-file handling, per-run artifact uploads, and a QLIKE correction; it is pending.
- Known defect correction: benchmark-relative out-of-sample R-squared has been fixed on the phase-5 branch; that branch's corrected run must be the canonical result.
- External inputs: seven public daily series were validated in run #41 (S&P 500, Nasdaq, Nikkei 225, Hang Seng, CBOE VIX, India VIX proxy, U.S. 10-year yield proxy). USD/INR, gold and WTI failed OHLC checks and were not used. Historical options, FII/DII, breadth, point-in-time constituents and news/sentiment data are not verified as acquired.
- Independent tester report is available on `research/independent-tester`; it identified the partial-forward-window volatility-label defect. Phase 5/7 remain open until the developer fix passes CI and a corrected model run is independently rechecked.
- Provisional ARIMA(1,0,0) metrics did not show statistically significant improvement over zero-return forecasts at 1/5/20 sessions (raw p = 0.492/0.935/0.842; loss-difference intervals include zero). These are not final until the corrected merge rerun reproduces the outputs and Holm-adjusted comparisons are available. No best model is declared yet.

See [phase status](research/PHASE_STATUS.md) for the authoritative gate state.

- [Run 45 results and evidence register](research/RESULTS.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)
- [Developer correction branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/developer-review)
