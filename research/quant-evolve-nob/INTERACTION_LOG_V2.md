# Interaction and activity log — QE-NOB-2.0

This is a concise audit log, not a verbatim conversation transcript and not a record of hidden reasoning.

## 2026-10-22 — new structural-discovery phase authorized
- User said “No tester” and “proceed”; no tester branch/report is created or awaited.
- Reviewed QE-NOB-1.0 research plan, phase status, results, config, workflow, error log, research questions and activity log before starting the next phase.
- Diagnosis: QE-NOB-1.0 used a bounded predefined grammar, mostly fixed-time exits, and no explicit structural novelty objective. Its 600 candidates were not 600 independent novel strategy structures.
- Created branch `research/quant-evolve-nob-v2-discovery-developer` from the completed QE-NOB-1.0 developer branch.
- Committed a new bounded plan with typed strategy trees, hypothesis cards, exit-state machines, novelty-aware multi-objective evolution, fixed budget, chronological OOS and cost/execution gates.
- Current state: Phase 1 complete; Phase 2 feature/source feasibility is next. No code implementation or strategy run is yet claimed.

## 2026-10-22 — first structural grammar implementation checkpoint
- Completed a static feature/source feasibility matrix from the existing pipeline and reports. Runtime cache coverage remains unverified, so several proposed features are conditional and must be gated.
- Added `strategy_grammar_v2.py`: typed candidate schema, validation, canonical signatures, structural novelty distance, bounded deterministic mutation and crossover with parent lineage.
- Added tests for canonical identity, structural exit novelty, feature allowlisting, invalid stop values, deterministic mutation and crossover.
- Added `.github/workflows/qe-nob-v2-grammar-tests.yml` for automatic tests on relevant pushes and manual dispatch.
- Updated phase status and implementation log. CI success has not yet been verified; this grammar is not integrated into the backtester and no new strategy has been backtested.
- User's instruction “No tester” remains in force. No tester branch/report was created or awaited.

## 2026-10-22 — test import defect corrected
- Static review identified that the study directory uses hyphens, so package imports using underscores could not resolve. Tests were switched to explicit file-path loading; the dataclass module is registered in `sys.modules` before execution.
- Added the defect and correction to `ERROR_LOG_V2.md`; updated phase status to avoid claiming a successful CI result before it is verified.
- The workflow is configured for push and manual dispatch. No run outcome is claimed in this checkpoint.

## 2026-10-22 — resumed implementation after user confirmation
- Added `feature_audit_v2.py` to inspect local JSON cache schema, timestamp counts, nulls, array lengths and SHA-256 hashes. It does not download licensed data or infer unavailable contract identity.
- Added feature-audit regression tests and a dedicated automatic/manual GitHub Actions workflow.
- Corrected tests to load Python files directly because the research directory name contains hyphens; registered dynamically loaded modules before dataclass initialization.
- Updated phase status and error log. These fixes are source-level only; workflow execution and full-cache audit results remain unverified.
- Still blocked from a discovery run: no integrated simulator, no confirmed Phase 2 feature matrix from runtime data, and no new strategy P&L. No tester branch/report created.

## 2026-10-22 — bounded candidate generator added
- Added `evolve_candidates_v2.py`, a deterministic candidate proposal generator with feature allowlist, unique structural signatures, mutation/crossover, lineage, novelty-based environmental selection, and hard 1,500-candidate / 20-generation ceilings.
- Added generator regression tests and a dedicated automatic/manual GitHub Actions workflow.
- The generator explicitly emits `CANDIDATES_GENERATED_NOT_BACKTESTED`; it does not compute fitness or reuse QE-NOB-1.0 outcomes. This is not yet the profitability search loop because a tested simulator/evaluator is not integrated.
- Updated phase status and error log. CI execution and tests remain unverified; no candidate P&L or strategy result is claimed.

## 2026-10-22 — leakage-aware signal evaluator added
- Added `signal_evaluator_v2.py` to evaluate allowlisted numeric/categorical predicates using current and past completed bars, reject duplicate/missing timestamps and emit next-market-bar entry timestamps.
- Added regression tests and an automatic/manual GitHub Actions workflow.
- Code review found a timing defect in the first draft: sparse signals were mapped to the next signal timestamp rather than the next market bar. Corrected the evaluator to map against the full timestamp grid and added a dedicated regression test. Logged as QE-NOB2-E008.
- No workflow test result has been verified; the evaluator generates signal timestamps only and does not simulate option fills or P&L.

## 2026-10-22 — OHLC option simulator added
- Added `option_simulator_v2.py` to align candidate signals with next-bar entries, select rolling option OHLC rows by expiry family/side/offset/timestamp, use same-strike exits, apply date/family lot-size proxies, modeled statutory/exchange fees, brokerage and adverse slippage, and block overlapping trades within one candidate.
- Execution gate is hard-coded false because rolling OHLC does not establish exact exchange contract identity, historical bid/ask/depth or broker fills.
- Added tests for lot-size transition assumptions, fee/slippage drag, negative-cost rejection, no-overlap behavior and the permanent execution gate.
- Code review found and corrected a first-draft overlap/lookup issue, recorded as QE-NOB2-E009. CI is not verified and no historical candidate backtest has been run.

## 2026-10-22 — implementation hardening and runtime acquisition gate
- User confirmed to proceed; developer-led workflow continued with no tester branch/report.
- Fixed a syntax defect in the signal evaluator and added fail-closed behavior for entry modes that have not been implemented. The evaluator now only accepts the tested `signal` entry mode rather than silently reinterpreting other modes.
- Added typed predicate validation and regression tests for categorical/numeric operators, threshold values and bucket-bound ordering. Mutation repairs invalid types and guarantees structural change after repair.
- Hardened the option simulator: rejects invalid timestamp/offset values, pre-indexes rolling option bars, supports only tested time exits and premium stop/target exits, uses stop-first ordering when OHLC could hit both stop and target, and corrects median calculation for even samples. Exact exchange contracts and executable quotes remain unverified, so execution gate stays false.
- Restricted candidate seeds and mutation to currently implemented entry/exit semantics; structural generator tests do not themselves establish fitness or profitability.
- GitHub Actions results verified: grammar + feature audit #39802894371 passed (15 tests); standalone feature audit #39802894311 passed; signal evaluator #39801804759 and option simulator #39801813009 passed; candidate generator #39802753682 passed.
- Earlier automated failures were inspected through job logs. Corrections addressed obsolete grammar-workflow test paths, external fixture paths, a mutation no-op, and null timestamps in audit min/max. These events and fixes are recorded in `ERROR_LOG_V2.md`.
- The first runtime audit artifact #39803204747 showed `BLOCKED_NO_LOCAL_CACHE` with zero cached data files. This only establishes the cache was not present on that runner; it does not establish that Dhan/free data sources are unavailable.
- Added `.github/workflows/qe-nob-v2-data-audit.yml` to run a bounded cache-first/acquisition-only stage using the existing Dhan source client and the configured `DHAN_ACCESS_TOKEN` / `HF_TOKEN` secrets, save a v2-namespaced local cache for future runs, and upload sanitized audit metadata without raw option payloads or credentials. Run #39803647257 was triggered automatically and is in progress at this log entry.
- No historical QE-NOB-2.0 candidate fitness/P&L run was started, and no strategy profitability is claimed.


## 2026-10-22 — session boundary and expiry-family corrections
- Reviewed new feature-builder and simulator workflows as the implementation advanced. The point-in-time feature builder now gates feature availability by observed coverage and variation; its latest workflow #39805843560 passed.
- Fixed the mismatch between candidate expiry names WEEK1/MONTH1 and cached source fields WEEK/MONTH plus expiry code by normalizing a canonical family key in the reusable option index. Added a targeted regression test; the run is pending at checkpoint.
- Added same-session timing safeguards to prevent intraday signals from silently opening positions on the next session. Signal evaluator #39806277479 and simulator #39806376781 passed.
- The bounded cache-acquisition workflow #39803647257 remains in progress. No candidate fitness, P&L, or profitability conclusion is claimed while it is running.

## 2026-10-22 — training-only fitness and bounded discovery runner
- Inspected the existing bounded discovery runner and confirmed it uses four fixed-seed islands, a separate validation block, a sealed chronological OOS block, a 5-session moving-block bootstrap, Holm correction and the declared slippage/brokerage stress grid.
- Corrected candidate feature eligibility to be based on training-period coverage/variation only; full-sample coverage remains diagnostic. This prevents OOS data from influencing which features enter the search grammar.
- Added a standalone chronological training-only fitness utility with leakage tests and ensured numeric diagnostics are not automatically treated as Pareto objectives. The production discovery runner retains its own multi-objective fitness implementation because it also scores stability across time blocks.
- Added automated tests for discovery statistical utilities and connected them to the candidate-generator CI workflow. CI result is pending at this checkpoint.
- The long-running bounded data acquisition job remains in progress; no market candidate has yet been scored or claimed profitable.
