# NIFTY prediction research error log

Updated: 2026-10-25. Preserve historical issues; mark resolutions explicitly rather than deleting entries.

## NP-001 — Daily source not exchange-certified (OPEN)
Primary source is Yahoo Finance; second source is a third-party parquet mirror. Both match OHLC exactly over 4,686 sessions, but may share upstream data. Seek official Nifty Indices/NSE cross-check before strong claims.

## NP-002 — Initial benchmark CI (RESOLVED)
Workflow [#34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710) completed successfully, including tests, acquisition, parity audit, benchmark and artifact persistence.

## NP-003 — Scope mismatch with expiry study (OPEN)
This study is daily next-session spot direction, not expiry-specific/intraday options prediction. Keep the scope explicit.

## NP-004 — External repositories are not all empirically executed (OPEN)
All seven READMEs have been reviewed and roles/guardrails recorded in [REPOSITORY_INTEGRATION.md](REPOSITORY_INTEGRATION.md). Review is not equivalent to installation or an experiment. Do not claim results for libraries without artifacts.

## NP-005 — Source agreement is not independent validation (OPEN)
Yahoo and public parquet mirror match exactly. Identical data does not prove accuracy or independence. Official source cross-check remains outstanding.

## NP-006 — Initial ML models do not beat the simple direction baseline (OPEN RESEARCH QUESTION)
Previous-session direction scored 54.10% balanced accuracy on the 1,157-row holdout; logistic regression 52.53%, random forest 50.44%, histogram gradient boosting 52.82%. Do not promote these fitted models as winners.

## NP-007 — Trading costs not modeled (OPEN)
All current results are prediction or gross index proxies. No strategy is viable until turnover, realistic execution, slippage, brokerage, taxes/charges and relevant futures/options basis are modeled.

## NP-008 — Optional package and integration runs pending (OPEN)
The baseline workflow only checks `arch` and MAPIE package availability. GARCH scoring, MAPIE calibration, PySR, `tick`, Quantevolve and TradingAgents have not yet produced empirical benchmark artifacts. AstraQuant's OKX-native crypto executor is not an NSE/NFO adapter.

## NP-009 — Candidate script added after baseline workflow (OPEN UNTIL VERIFIED)
Added `research/nifty-prediction/evaluate_candidate_rules.py` and updated the workflow to execute and persist `reports/nifty-prediction/candidate_rules.json`. Cached-data calculation indicates the previous-direction baseline remains stronger than the tested simple candidates. Automated run [#37](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40142722883) was pending at the last check; confirm success and persisted artifact before calling the code-path verified.

## NP-010 — Gross index proxy can be mistaken for tradable performance (OPEN)
Candidate screen multiplies next-session spot-index return by a long/short direction sign. This ignores executable instrument basis, lot sizing, turnover, margin, slippage, brokerage, taxes and execution. It is only a diagnostic; never describe its compounded value as strategy P&L.

## NP-011 — Artifact persistence race during candidate workflow (RESOLVED IN WORKFLOW; latest run pending)
- **Severity:** Medium.
- **Evidence:** Workflow run [#37](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40142722883) passed dependency setup, unit tests, acquisition, parity audit, baseline benchmark and candidate-rule execution, but failed at artifact persistence.
- **Cause:** An earlier run committed `candidate_rules.json` while this run was still executing from an older checkout. Its local generated artifact then conflicted during the later rebase/push.
- **Fix:** Updated the workflow to rebase the current branch **before** staging generated outputs, and included `volatility_forecast.json` in persistence. The newer workflow run #40 is in progress; verify it completes before marking this fix confirmed.
- **Important:** The scientific candidate calculation did run successfully in #37; the failure was in saving results, not in the benchmark or candidate-rule step.

## NP-012 — Concurrent branch push rejected during persistence (FIX APPLIED; rerun required)

- **Evidence:** Workflow [#40](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40142926621) completed benchmark, candidate-rule, and GARCH steps, but the persistence step failed because the remote branch advanced after the runner's checkout/rebase.
- **Scientific output:** Candidate rules were computed for 1,157 rows (2022-02-14 to 2026-10-22). GARCH(1,1) was computed on 1,157 observations (2022-02-15 to 2026-10-23). The run artifact uploaded successfully; branch JSON persistence did not.
- **GARCH result:** QLIKE was -8.64595 for GARCH(1,1), -8.57379 for rolling 20-session variance, and -8.22293 for expanding unconditional variance. Lower is better. This supports a modest volatility forecast comparison only; squared returns are noisy and it is not a direction or trading result.
- **Cause:** A concurrent branch update raced the push; pre-staging rebase alone did not eliminate the race window.
- **Fix:** Persistence workflow now includes volatility_forecast.json, fetches/rebases before staging, and retries the push up to three times after fetching/rebasing on rejection. Workflow-file change triggers an automated rerun. Verify that run and its persisted reports before closing this entry.


## NP-013 — Repository integration audit and optional model experiments (PARTIALLY RESOLVED)

- **Integration audit:** [run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40143973082) succeeded. All seven upstream repositories were checked out at pinned commits. Installed versions: arch 8.0.0, MAPIE 1.6.0, scikit-learn 1.9.1; PySR and tick were not installed in that audit environment.
- **Fix/progress:** Added `evaluate_optional_models.py` and [optional-model workflow](../../.github/workflows/nifty-optional-models.yml). It uses a chronological 60/15/25 train/calibration/test split; it records MAPIE API/coverage status and PySR/tick import compatibility. It does not permit agent labels, holdout tuning, or orders.
- **Pending:** Workflow has just been added; do not call MAPIE/PySR/tick empirically integrated until its JSON report is committed and inspected. Optional install failures are expected to be captured rather than hidden.
