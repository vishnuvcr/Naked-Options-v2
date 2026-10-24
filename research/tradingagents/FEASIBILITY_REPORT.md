# TradingAgents Compatibility and Test Report

**Status:** Initial static review complete; executable CI test requested by repository workflow; NIFTY 50 adapter not yet validated.  
**Review date:** 2026-10-25  
**Upstream repository:** https://github.com/TauricResearch/TradingAgents  
**Pinned upstream commit:** `e8f5503e9b86d5c2710b0c76b1f686703968c9df` (v0.7.0 release merge)  
**License:** Apache-2.0 (reviewed upstream LICENSE).

## Scope

Evaluate whether TradingAgents can serve as a separate prediction benchmark for the existing NIFTY 50 weekly-expiry UP/DOWN study. The ZigZag++ experiment remains unchanged. No options strategy or trading recommendation is in scope.

## Static checks completed

1. Inspected upstream README, package metadata, CI workflow, backtest harness, Yahoo OHLCV source, ticker normalization, and representative point-in-time/date-boundary tests.
2. Confirmed Python >=3.11 and package dependencies are declared in `pyproject.toml`.
3. Confirmed upstream CI runs unit tests across Python 3.11–3.14, a non-UTC timezone case, clean-install import smoke test, and Ruff lint.
4. Confirmed the framework has a grid-based decision-quality backtest and memory log, but upstream `tradingagents/backtest.py` explicitly states it is not a portfolio simulator and has no execution, fees, or equity curve.
5. Confirmed the upstream suite contains explicit point-in-time protections for news, fundamentals, date boundaries, OHLCV freshness and tool dates. These are useful controls, not proof that every vendor/path is leakage-free.
6. Found Yahoo Finance is the default OHLCV path; the reviewed symbol-normalization table does not explicitly list `^NSEI`. It may pass through unchanged, but actual symbol/data support must be tested instead of assumed.

## Compatibility findings

### Positive
- Modular analyst/researcher architecture could generate a separate directional forecast.
- Existing chronological/date-grid backtest harness and point-in-time tests provide useful starting points.
- Apache-2.0 permits reuse subject to its license conditions and retaining applicable notices.
- Upstream CI already provides meaningful software quality checks.

### Blocking / risks for our research
- TradingAgents' normal task is multi-agent trading-decision support, not our exact target: NIFTY spot at 10:00 IST on the first session after an actual weekly expiry versus the next actual expiry close.
- Default Yahoo OHLCV is not yet demonstrated to provide the required Indian index intraday history, correct timezone/bar timestamps, or enough coverage. Dhan data must be connected through a controlled adapter if Yahoo fails.
- A daily backtest result cannot establish a forecast made at 10:00 IST.
- LLM outputs and web/news retrieval must be frozen, logged, and point-in-time filtered. A current report about historical dates is not admissible.
- Existing backtest metrics are decision ratings/realized returns, not the preregistered UP/DOWN balanced-accuracy protocol. A dedicated forecast-output adapter and evaluator are required.
- Upstream tests have not been executed inside this research environment. The new GitHub Actions workflow is intended to run them against the pinned upstream commit; results must be checked before declaring pass/fail.

## Required test gates

1. **Upstream software gate:** install at pinned SHA; run upstream unit tests, Ruff, and clean import.
2. **Instrument/data gate:** prove `^NSEI` or custom NIFTY data adapter returns reproducible, timestamped index data; compare overlapping dates with Dhan/official sources.
3. **Point-in-time gate:** every input (OHLCV, news, macro, sentiment) must be restricted to information published/available by the exact prediction cutoff; exclude undated historical news.
4. **Forecast contract gate:** each expiry interval produces one machine-readable `UP`, `DOWN`, or `ABSTAIN` forecast, with timestamp, model/provider/version, prompt/config hash, input provenance and rationale.
5. **Evaluation gate:** reuse the existing preregistered expiry target labels and primary metric (balanced accuracy); compare with majority and 50% baselines on identical eligible dates. Do not tune on the final holdout.
6. **Reproducibility/cost gate:** cache permissible inputs, cap model calls, log retries/errors, and record model/API costs and nondeterminism.
7. **Decision:** add TradingAgents to formal comparison only if gates 1–5 pass. Otherwise record a no-go or a constrained adaptation; do not replace the ZigZag study.

## Current decision

**CONDITIONAL CANDIDATE — NOT YET A VALID NIFTY FORECASTER.** Static review indicates the framework is worth testing as a separate benchmark. It is not yet suitable for generating scientific scores for the current NIFTY expiry target. No forecast accuracy has been measured in this review.

## Sources
- Upstream repository: https://github.com/TauricResearch/TradingAgents
- Pinned reviewed commit: https://github.com/TauricResearch/TradingAgents/commit/e8f5503e9b86d5c2710b0c76b1f686703968c9df
- Package metadata: https://github.com/TauricResearch/TradingAgents/blob/e8f5503e9b86d5c2710b0c76b1f686703968c9df/pyproject.toml
- CI workflow: https://github.com/TauricResearch/TradingAgents/blob/e8f5503e9b86d5c2710b0c76b1f686703968c9df/.github/workflows/ci.yml
- Backtest implementation: https://github.com/TauricResearch/TradingAgents/blob/e8f5503e9b86d5c2710b0c76b1f686703968c9df/tradingagents/backtest.py
- License: https://github.com/TauricResearch/TradingAgents/blob/e8f5503e9b86d5c2710b0c76b1f686703968c9df/LICENSE

## Developer → next step
Run the pinned upstream CI suite, then build the smallest isolated NIFTY data/forecast adapter and validate the exact timestamp/point-in-time contract. Do not score until the original study's session-calendar and target-data gates pass.
## CI result update — 2026-10-25

Pinned upstream software checks succeeded in GitHub Actions run [#40129883044](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129883044): upstream dependency installation, pytest unit suite, Ruff lint, and clean-install import smoke test all completed successfully against the configured upstream checkout. This establishes software-test compatibility for that run, not predictive validity.

A live-data diagnostic probe was added at `research/tradingagents/probe_nifty_yahoo.py` to inspect Yahoo Finance `^NSEI` daily and 5-minute bars. The new probe has not yet completed in a workflow run. Even if it succeeds, current availability will not establish historical coverage, exact 10:00 IST bar semantics, or point-in-time news integrity.

User instruction confirmed: **no independent tester role, branch, or approval gate**. Developer will inspect automated logs and fix issues directly.
## Live Yahoo data probe — 2026-10-25

The compatibility workflow's live `^NSEI` probe passed in [run #40130052739](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130052739). The run returned:
- Daily: 21 rows for the requested one-month window; first timestamp 2026-09-23 00:00:00+05:30; last timestamp 2026-10-23 00:00:00+05:30.
- Five-minute: 375 rows for the requested five-day window; first timestamp 2026-10-16 09:15:00+05:30; last timestamp 2026-10-23 15:25:00+05:30.
- Both responses had OHLC columns, no missing close values in the tested sample, and timezone-aware indexes.

**Interpretation:** Yahoo can currently return a usable-shaped NIFTY spot series for daily and intraday exploratory use. This is not a historical coverage certification: the probe checks only a short live window and does not establish robust past 10:00 IST cutoffs, historical intraday availability, official session-calendar correctness, corporate/action adjustments, or frozen point-in-time news/fundamentals. It therefore does not authorize the formal expiry-label evaluation.

## Updated decision

**Conditional candidate for an isolated benchmark; not yet approved as a validated predictor.** The pinned upstream software checks and current Yahoo data-shape check passed. The next implementation should use frozen/cached NIFTY bars and a deterministic, structured UP/DOWN/ABSTAIN output contract; exclude news/social/fundamentals unless historically timestamped snapshots are available. Compare against naïve/base-rate and simple price-momentum baselines on the same expiry dates. Do not interpret LLM narrative confidence as calibrated probability.

## Phase D — forecast contract and framework integration risk

A machine-readable forecast contract has been implemented with a deterministic validator. It forces explicit cutoff/target timestamps, UP/DOWN/ABSTAIN, model and prompt identity, an input-manifest hash, and an input as-of timestamp. Unit tests cover key temporal and schema failures; CI execution is pending.

**Important integration risk found in source audit:** the pinned framework's standard market tool takes date-based start/end values, routes to Yahoo, and the Yahoo OHLCV formatter removes timezone information from its index. That is not sufficient by itself for the project's 10:00 IST intraday cutoff. In addition, the standard graph defaults to market, social, news, and fundamentals analysts; historical news/fundamental context cannot be assumed point-in-time. For the benchmark, use only market analysis initially and a custom prefiltered frozen-data adapter; disable unrestricted vendor retrieval and exclude undated ancillary inputs. A record validator alone cannot prove the model actually used only the declared inputs.

This is a blocking design constraint, not a prediction result. No forecast has been scored.



## Latest CI and frozen-snapshot gate — 2026-10-25

The latest completed run [#40130735394](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130735394) passed every listed step: forecast-contract tests, upstream install, upstream pytest, Ruff, clean-install import and Yahoo probe. A second layer, `market_snapshot.py`, was added to reject future bars, non-monotonic timestamps, naive timestamps, instrument mismatch and inconsistent OHLC. Its CI run is pending.

The snapshot validator does not yet certify source timestamps or official sessions, and is not wired to the TradingAgents graph. It must be paired with immutable data provenance and a market-only graph/tool configuration that prevents unfiltered vendor calls. No historical model outputs or accuracy scores exist.



## Verified snapshot-validator CI result

[Workflow run #40131047411](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131047411) completed successfully, including the new snapshot tests. The validator correctly passes/rejects its synthetic cases. This is software validation only. It does not prove historical source correctness, session completeness, or causal isolation inside TradingAgents. No live model invocation or out-of-sample prediction score has been produced.

