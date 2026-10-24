# Interaction and Decision Log

## 2026-10-25 — User authorized execution
- User instruction: “Proceed”.
- Scope fixed by preceding user clarification: “Just use the indicator for nifty expiry up or down prediction”.
- Included: ZigZag++ signal research for NIFTY 50 expiry-to-expiry UP/DOWN prediction.
- Excluded: options-selling rules, delta selection, stop-loss, trading P&L and strategy recommendations.
- User explicitly said no tester review is needed; no independent tester branch/gate will be created for this task.
- Protocol rule: last confirmed and knowable low (LL/HL) => UP; last confirmed high (HH/LH) => DOWN; no eligible pivot => abstain.
- No private hidden reasoning is stored. This log preserves user-visible decisions and research actions, not hidden chain-of-thought.


## 2026-10-25 — Timeframe sensitivity authorized
- User instruction: “Test various timeframes”.
- Decision: avoid asking the user to choose a single timeframe; pre-register 5m, 15m, 30m, 60m and 1-day variants, with 1m conditional on validated data.
- Added TIMEFRAME_SENSITIVITY.md defining comparability, metrics, multiplicity controls, and the no-scoring-before-validation gate.
- No performance results have been generated; exact ZigLib behavior and validated intraday/expiry data remain blockers.


## 2026-10-25 — Acquisition workflow implemented
- Added `acquire_dhan_timeframes.py`: Dhan v2 NIFTY 50 spot index requests (security ID 13; `IDX_I`/`INDEX`), 1m/5m/15m/60m plus daily bars, <=90-day chunks, retry handling, local cache reuse unless `--refresh`, SHA-256 and timestamp manifests. Credentials are read from `DHAN_ACCESS_TOKEN` only; never logged.
- Added `prepare_timeframes.py`: OHLC/timestamp validation and session-anchored 30m resampling from six contiguous 5m bars; incomplete bars are excluded and counted.
- Added `.github/workflows/zigzag-expiry-timeframes.yml`: push/manual triggers, cache, optional refresh, and data/manifest artifact retention.
- Execution status remains unverified until a workflow run and artifact are inspected. No empirical score was produced. Source-faithful ZigLib causality remains a hard gate.


## 2026-10-25 — Causality control
Reviewed the publicly accessible ZigZag++ wrapper mirror. It defaults to `repaint=true`; the non-repaint branch draws only on direction changes and uses prior-bar point values. To avoid look-ahead in the prediction-only study, the pre-registered primary timeframe panel is now explicitly non-repaint mode, with signal availability assigned to the direction-change bar. This is a protocol amendment, not evidence of predictive performance; results must not be described as default-setting performance. The imported ZigLib v1 internals remain unverified.


## 2026-10-25 — Execution verification attempt
- Tried to clone the branch locally to run syntax checks; DNS/network to github.com failed. Logged as ZZD-016.
- Checked available GitHub actions tools; no direct workflow dispatch was available and no successful run artifact could be confirmed.
- Current outcome remains blocked: acquisition workflow is implemented but unverified; no empirical scores.
