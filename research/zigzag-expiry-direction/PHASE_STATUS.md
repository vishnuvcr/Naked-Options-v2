# Phase Status — ZigZag Expiry Direction

Updated: 2026-10-25

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIALLY COMPLETE — BLOCKED | TradingView ZigLib page states the function returns direction and two chart points (library page dated Oct 9, 2023); TradingView's generic Zigzag documentation explicitly warns that confirmed labels are drawn into the past and the latest solid line is not final. A public GitHub mirror of the wrapper script confirms `repaint=true` is the default and that the non-repaint branch only draws on direction changes using prior-bar point values; however, it does not contain the imported ZigLib implementation and is not an authoritative source. Exact ZigLib v1 source semantics and signal-availability time remain unverified. NSE official contract page confirms current Tuesday expiry with previous-session holiday shift, but historical circular mapping remains incomplete. |
| 2. Data audit | BLOCKED | Official free source leads and acceptance criteria documented; no export has been acquired/validated, and intraday 10:00 data is required. | NSE/Nifty Indices public historical index-data portals are confirmed as free source leads; the actual export is not yet cached or validated in this branch. Existing NWCP data still has unresolved source overlap, timestamp/provenance and expiry-calendar issues and is not automatically admissible. |
| 3. Causal reconstruction | BLOCKED | Cannot safely substitute a generic ZigZag or guessed port for the exact imported library. |
| 4. Evaluation | NOT STARTED | No eligible ZigZag predictions scored. |
| 5. Robustness/inference | NOT STARTED | Depends on valid out-of-sample results. |
| 6. Manuscript/decision | PROTOCOL DRAFTED | Manuscript skeleton exists; results, figures, tables and conclusions cannot be populated without validated empirical output. |

## Evidence reviewed
- TradingView ZigLib library page: https://www.tradingview.com/script/NC3cgEcT-ZigLib/ — describes `zigzag(_low, _high, depth, deviation, backstep)` and its returned direction and two chart points, but the accessible page summary does not expose enough implementation detail to validate historical availability.
- TradingView ZigZag++ page: https://www.tradingview.com/script/lj8djt1n-ZigZag/ — release notes mention advanced repainting control; that does not prove this exact pasted script/library combination is non-repainting.
- TradingView general ZigZag explanation: https://www.tradingview.com/support/solutions/43000591664-zigzag-indicator/ — explains confirmation lag and that the latest displayed line may be revised. This is general background, not a substitute for ZigLib v1 source.

**Current decision:** DATA-LIMITED / NO PERFORMANCE CLAIM. This run did not produce an empirical accuracy estimate. No tester gate was added because the user explicitly waived independent tester review for this experiment.


## Timeframe sensitivity update — 2026-10-25
Phase 1 protocol amendment: user requested “Test various timeframes.” Added TIMEFRAME_SENSITIVITY.md with a predeclared 5m, 15m, 30m, 60m and 1-day panel; 1m is conditional on validated data completeness. This resolves the protocol ambiguity by testing variants rather than silently picking one. It does not resolve source parity or data blockers.

| Phase | Updated status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | TIMEFRAME PANEL PRE-REGISTERED; SOURCE BLOCKED | Multi-timeframe variants documented; exact ZigLib v1 causality remains unverified. |
| 2. Data audit | BLOCKED | Validated intraday spot data and date-specific expiry schedule still not acquired. |
| 3. Causal reconstruction | BLOCKED | Must verify exact imported-library semantics for each timeframe. |
| 4. Evaluation | NOT STARTED | No eligible forecasts scored. |
| 5. Robustness/inference | NOT STARTED | Multi-timeframe comparisons require multiple-testing controls. |
| 6. Manuscript/decision | PROTOCOL DRAFTED | No empirical results. |

Current result remains DATA-LIMITED / NO PERFORMANCE CLAIM.


## 2026-10-25 execution update — acquisition pipeline added
Added `acquire_dhan_timeframes.py` to request NIFTY 50 spot index bars from Dhan v2 (security ID 13, segment `IDX_I`, instrument `INDEX`) for 1m/5m/15m/60m and daily data, in chunks no longer than 90 days. Added `prepare_timeframes.py` for timestamp/OHLC/duplicate checks and a 30m series resampled from six contiguous 5m bars anchored at 09:15 IST. Added `.github/workflows/zigzag-expiry-timeframes.yml` with cache, manual inputs, optional refresh, and an artifact that includes data plus provenance/validation manifests.

| Phase | Status | Evidence / blocker |
|---|---|---|
| 1. Protocol/source audit | PARTIAL — BLOCKED | Timeframe variants registered; exact ZigLib source/timing still unverified. |
| 2. Data audit | PIPELINE ADDED — EXECUTION NOT VERIFIED | Dhan acquisition code/workflow committed; no successful workflow artifact or validated dataset is yet confirmed in this chat. |
| 3. Causal reconstruction | BLOCKED | No source-faithful ZigLib implementation yet. |
| 4. Evaluation | NOT STARTED | No predictions scored. |
| 5. Robustness/inference | NOT STARTED | Requires valid predictions and multiple-comparison control. |
| 6. Manuscript/decision | DRAFT ONLY | No empirical results. |

Important: adding the workflow is not evidence that Dhan authentication succeeded or that data was acquired. The next gate is inspect the workflow result/artifact, correct any logged API/data errors, then validate source parity before scoring.


## Wrapper timing finding — 2026-10-25
The accessible public wrapper mirror shows `repaint=true` as the default and a separate non-repaint branch that only draws when `direction != direction[1]`, using prior-bar points (`z1[1]`, `z2[1]`). This is useful wrapper-level evidence, not authoritative proof of the imported ZigLib implementation. To keep a causal prediction study, primary timeframe evaluation is now specified for `repaint=false`; its signal availability must be the direction-change bar, never the earlier pivot timestamp. Results must be labeled non-repaint-mode results and not default-setting results. Exact library internals and the successful Dhan acquisition artifact remain unverified.
