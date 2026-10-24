# TradingAgents NIFTY 50 Feasibility Plan

**Status:** Phase A static review completed; Phase B upstream executable tests pending.  
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

## Tester instruction
Independently inspect the workflow run, verify the checked-out SHA, test logs and artifact. Report failures with exact step/log evidence. Then audit any NIFTY adapter for timestamp, symbol, missing-data and point-in-time errors before authorizing evaluation.
