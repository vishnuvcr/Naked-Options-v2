# TradingAgents NIFTY 50 Feasibility Plan

**Status:** Phase A static review completed; corrected Phase B workflow has passed upstream unit tests and Ruff lint; clean-install import smoke test is running. No independent tester branch or review gate will be created, per user instruction.  
**Scope:** Evaluate TradingAgents as a separate NIFTY 50 weekly-expiry direction-prediction benchmark. This is not a trading-strategy phase.

## Questions
1. Does the pinned upstream package install and pass its own tests?
2. Can its data abstraction supply NIFTY 50 spot data at the required 10:00 IST cutoff with verified timestamp semantics?
3. Can it emit a structured UP/DOWN/ABSTAIN forecast without post-cutoff information?
4. Does it add out-of-sample predictive value beyond simple baselines and the existing ZigZag++ candidate?

## Phases
- **A — Static/source audit (COMPLETE):** inspect README, license, pyproject, CI, backtest harness, symbol mapping, data paths, and point-in-time tests. Findings in `FEASIBILITY_REPORT.md`.
- **B — Pinned upstream software tests (RUN VIA ACTIONS):** run tests, lint and clean-install import against SHA `e8f5503e9b86d5c2710b0c76b1f686703968c9df`. Capture logs/artifacts and distinguish test failure from environment failure.
- **C — NIFTY data adapter (NOT STARTED):** test Yahoo `^NSEI` data coverage and intraday resolution; if unsuitable, implement a narrow adapter over already validated Dhan data. Verify timezone, timestamp convention, missing bars, duplicate bars, and source overlap.
- **D — Forecast interface (NOT STARTED):** define strict machine-readable forecast schema with cutoff, target interval, output class, model/provider/version, configuration/prompt hash, input references and error status. Avoid trading-action semantics.
- **E — Leakage audit (NOT STARTED):** replay historical decisions with only data available by each cutoff; enforce dated news/macro inputs and no future values. Record all excluded/undated inputs.
- **F — Small pilot (NOT STARTED):** run a small chronological sample to test runtime, cost, reproducibility, and abstention/error behavior; pilot is not evidence of predictive performance.
- **G — Formal out-of-sample evaluation (BLOCKED):** only after upstream software, instrument/data, point-in-time and forecast-contract gates pass, use the same expiry labels and dates as the main research. Primary metric balanced accuracy; report coverage, accuracy, class metrics, confidence intervals, baselines and failures.
- **H — Decision/report (NOT STARTED):** recommend integrate, adapt, or reject. Do not expand into strategy design in this phase.

## Non-negotiable safeguards
- Keep this as a separate benchmark; do not alter ZigZag protocol or reuse scores from unrelated research.
- Pin upstream commit and dependency environment.
- No network/LLM result may be treated as historical evidence unless point-in-time provenance is established.
- Do not claim a test passed until the corresponding CI run is inspected.
- No final holdout tuning; account for multiple model/config variants.
- Do not generate brokerage/slippage-adjusted P&L in this prediction-only phase.
- Preserve upstream license and notices if source code is copied or modified.

## Developer self-check (no independent tester)
The user explicitly instructed: “No tester.” Do not create an independent tester branch, tester role, or tester approval gate. The developer will inspect CI logs, record defects, fix them, and continue the planned gates autonomously. Software CI remains a normal automated test suite, not a separate tester role.
## Execution update — 2026-10-25

- Phase A static review: COMPLETE.
- Phase B pinned upstream software checks: PASS in [run #40129883044](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129883044): dependency install, unit suite, Ruff, and clean-install import passed.
- Phase C NIFTY Yahoo data probe: ADDED, pending new workflow run. It probes `^NSEI` daily (1 month) and 5-minute (5 days) bars and records timestamps/timezone/row counts. It is diagnostic only.
- Phases D–G: NOT STARTED/BLOCKED until the data and point-in-time contract is validated.

No independent tester branch or tester approval gate will be created. Ordinary CI tests remain part of development quality control.
## Phase C result — 2026-10-25

**PASS for basic current data-shape availability only.** [Run #40130052739](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130052739) returned 21 daily rows and 375 five-minute rows for `^NSEI`, with timezone-aware timestamps and OHLC columns; close values were non-missing in the sampled output.

This is not a historical-data gate pass. The data probe does not validate historical 10:00 IST bars, the official trading calendar, or point-in-time ancillary inputs. Phase D must implement a structured forecast interface and freeze market-only inputs first. Formal evaluation remains blocked by the main research track's unresolved calendar/timestamp and causal ZigZag constraints.

- Phase A — COMPLETE.
- Phase B — PASS (upstream tests, lint, clean import).
- Phase C — PARTIAL PASS (short-window Yahoo shape only).
- Phase D — NEXT; no performance evaluation until data/causal gates pass.

## Phase D implementation update — 2026-10-25

A strict output contract was added in `forecast_contract.py`, with deterministic tests in `test_forecast_contract.py` and documentation in `FORECAST_CONTRACT.md`. CI now runs these local tests. Contract checks cover required fields, UP/DOWN/ABSTAIN classes, timezone-aware timestamps, target ordering, input-as-of not later than cutoff, record creation timing, and SHA-256 syntax.

- Phase D schema/validator: IMPLEMENTED; CI result pending for the newest commit.
- Phase D end-to-end model adapter: NOT COMPLETE.
- Phase E leakage audit: BLOCKED until a custom frozen-snapshot adapter prevents TradingAgents' regular market tools from fetching outside the cutoff.
- Formal evaluation: BLOCKED.

