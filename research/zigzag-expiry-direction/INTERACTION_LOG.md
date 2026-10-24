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


## 2026-10-25 — CI test coverage added
Added unit tests for Dhan response parsing, epoch timestamp conversion, invalid OHLC and array lengths, 30m aggregation, and incomplete-bar exclusion. The GitHub Actions workflow now executes these tests before acquisition. The commit should trigger the branch workflow, but I could not query the run directly with the available GitHub interface. No test-pass or data-acquisition success is claimed.


## 2026-10-25 — Diagnose failed Actions run from user screenshots
- Inspected the supplied screenshots: cache restore step reports `Key Validation Error`; validation then reports missing 5m/15m/60m/daily CSVs and failed 30m derivation.
- Removed the comma-separated interval list from the cache key in commit `907e05fc8de0363aecf9fa8e7790c9b63b683b9f` to address the observed key validation failure.
- Updated error log, phase status, and results ledger. Rerun outcome still pending; no successful acquisition or predictions claimed.


## 2026-10-25 — Retrieved failed workflow logs directly
- Queried GitHub Actions run #40126339052 and inspected job logs. Confirmed the cache-key correction succeeded and pipeline unit tests passed.
- Identified the actual blocking error: Dhan HTTP 401 `DH-901` across 1m/5m/15m/60m and daily requests; the token is invalid or expired. Validation then failed because no CSV datasets existed.
- No data or predictions were produced. Next step requires updating the repository secret `DHAN_ACCESS_TOKEN` with a valid token; do not ask user to paste token into chat.


## 2026-10-25 — Automated Dhan token generation implemented
- Inspected the workflow and confirmed the previous version only consumed the static `DHAN_ACCESS_TOKEN` secret.
- Updated `.github/workflows/zigzag-expiry-timeframes.yml` in commit `0705e9aeafec15949f55ebb983f1f77ec60b62ef` to generate a fresh token using `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET`, mask it, validate it through `/v2/profile`, and pass it to the data acquisition step in the same job without persisting it as a repository secret.
- GitHub Actions run [#40126973037](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40126973037): tests and token validation succeeded; acquisition was still running at log inspection. No prediction result claimed.


## 2026-10-25 — Session/timestamp audit of acquired artifact
- Audited the actual CSV files in artifact [12573423696](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696), beyond the workflow's basic structural validation.
- Found weekend-dated bars across intraday series and many 1m timestamps outside a broad 09:00–16:00 IST screen. These may mix legitimate special sessions and out-of-session observations; no automatic blanket deletion was applied.
- Logged ZZD-021 and updated phase status: official session calendar and Dhan timestamp/interval conventions must be audited before using the data for causal signals or target labels.
- No prediction metrics computed because source parity and target calendar remain unresolved.


## 2026-10-25 — 1-minute artifact audit
- Continued after user instruction “Ok proceed”.
- Downloaded/inspected the actual successful data artifact and independently checked raw 1-minute timestamps and OHLC consistency.
- Found 511,268 rows, 2,636 weekend-dated rows, 47,612 out-of-session rows, 12 OHLC-inconsistent rows, and exact 10:00 rows on 1,236 dates.
- Logged this as ZZD-021 and updated phase/results documentation. No signals were generated and no accuracy was calculated because exact ZigLib parity and historical expiry target mapping remain unverified.


## 2026-10-25 — Added non-destructive session diagnostic
- Added `audit_sessions.py` to inspect timestamps and OHLC for every acquired timeframe, flag weekend dates and broad clock-time anomalies without deleting observations.
- Updated the Actions workflow to run the diagnostic and upload `zigzag_session_audit.json` alongside other data reports.
- Added ZZD-022: this is not official exchange-calendar certification. Need authoritative NSE session calendar and Dhan bar timestamp convention before scoring. No prediction metrics generated.


## 2026-10-25 — CI test failure diagnosed and corrected
- Inspected run [#40127961418](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127961418) logs after adding session diagnostics.
- Found the 30m test incorrectly indexed the returned `Path` as if it were a dictionary. Corrected the assertion in commit `1b6845b3b0d81b333ede7be9071ecd6ebbff2d10`.
- Since the unit-test gate failed, the run skipped Dhan authentication and acquisition. Do not interpret its missing-file reports as a new data-provider failure. Check the next workflow result.


## 2026-10-25 — Corrected workflow path filters
The workflow did not rerun on the test/audit changes because the push path filters omitted `tests/test_zigzag_data_pipeline.py` and `audit_sessions.py`. Added both paths to the workflow in commit `2f2719e99f7159a2121d0d745b111c07249d3bd2`. Next action: inspect the new ZigZag run, verify tests and artifact generation, then continue official session/expiry calendar research. NSE official public results surfaced: 2026 holidays page and F&O circulars for 2024 and 2025; these are evidence leads, not yet a complete historical calendar dataset.
