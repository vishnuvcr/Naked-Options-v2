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

## 2026-10-22 — automatic post-acquisition discovery wiring
- Updated the bounded acquisition workflow so that, after successful acquisition and feature-cache audit, it automatically runs the bounded four-island discovery/validation runner with frozen seeds and limits.
- Expanded the downloadable artifact allowlist to include sanitized QE-NOB-2.0 candidate, validation, OOS, cost-stress and result summaries; raw licensed cache files remain excluded.
- GitHub Actions run #39808171927 is queued behind the current acquisition job using the workflow concurrency group. It should reuse the saved cache rather than require the user to start a workflow manually.


## 2026-10-22 — continuation audit at 21:24 IST
- Resumed from the latest handoff and inspected the QE-NOB-2.0 phase status, discovery plan, error log, activity log, acquisition workflow and current workflow states.
- Discovery-runner CI #39808626484 completed successfully. This verifies software tests only, not empirical strategy performance.
- Acquisition run #39803647257 is still in progress at source acquisition; cache audit and sanitized report upload have not executed. Automatic follow-up #39808171927 remains pending and has not produced discovery results.
- Updated the phase-status and error-log records. No data sufficiency, candidate fitness, OOS performance, or profitability result was inferred. Phase 2 remains open; empirical discovery and final validation remain blocked.
- No tester branch/report was created, as instructed.


## 2026-10-22 — external source catalogue review
- Checked current public source information for Dhan's official rolling-options and intraday endpoints, NSE/Nifty Indices historical daily reports, FII/DII activity, Cboe VIX history and FRED series access.
- Discovered public option datasets on Hugging Face, but did not download or merge them: one listing uses license 'other' and another is CC BY-NC 4.0. Their source lineage/permissions are not approved for this trading-oriented study without further rights review.
- Identified a GitHub NIFTY 1-minute OHLC set as a potential independent underlying-data cross-check only; repository MIT licensing is not treated as sufficient verification of market-data provenance, and its maintainer documents known missing/fixed-bar quirks.
- Added [SOURCE_CATALOG_V2.md](SOURCE_CATALOG_V2.md) and updated phase status. This is source research only. No new experimental rows, candidate scores or P&L were produced. Phase 2 remains open while runtime acquisition is still in progress.


## 2026-10-23 — stalled-acquisition remediation
- User authorized continuation after receiving a status diagnosis of the stale acquisition job.
- Re-inspected the current Actions run and source client. The source step had remained active since 2026-10-22 15:18:51 UTC; GitHub did not expose active job-log content through the available log endpoint, so the last API request could not be determined.
- Committed a bounded client correction: supported offsets -2..+2 only, explicit progress logs, shorter HTTP timeouts, two attempts, stop after ten consecutive failed request groups, and underlying acquisition progress. Empty cached payloads are invalidated, and option data must be non-empty at least 80% of request groups with zero failures before source status can pass.
- Made acquisition fail closed when either option or underlying source is partial/blocked so a successful prior step is required before candidate discovery can run.
- Added unit tests for limits, no-progress stop, empty payloads and source-completeness gate. The automatic workflow's push filter is being expanded to include the client and regression tests. The live original run cannot be patched mid-execution; its queued successor is expected to check out the latest branch code after the current concurrency slot ends.
- No cache was deleted wholesale, no parallel multi-year download was started, no tester branch/report was created, and no profitability conclusion was inferred from software tests.


## 2026-10-23 — pre-CI source review corrections
- Before treating the recovery patch as CI-ready, reviewed the final acquisition functions and caught an accounting defect: request progress was incremented both at loop entry and after processing. Also caught an underlying timeout replacement mismatch (the actual call used the variable name obj, not payload).
- Removed duplicate request counter increments, changed the actual underlying call timeout to 45 seconds, and added a unit test covering one valid cached payload plus nine fetched payloads. The expected request count is ten, with one cache reuse and nine source calls.
- Added entry QE-NOB2-E025 to the error log. Automated verification is pending on GitHub Actions; no test outcome is assumed.


## 2026-10-23 — cache fingerprint review
- Reviewed the shell retry loop before its first automated run and noticed the initial cache fingerprint included probe JSON files rewritten at every new source-probe pass. That could falsely count the probe rewrite as historical cache progress.
- Corrected the fingerprint to exclude probe_* metadata JSON, and logged the risk as QE-NOB2-E026. The run still stops after at most three acquisition passes and stops earlier if the historical data cache does not change.
- Updated workflow commit d55fa380. Its automatic check remains pending behind the old in-progress acquisition job; no recovery-run test result is available yet.


## 2026-10-23 — independent source-client CI
- Added a separate automatically triggered / manually dispatchable GitHub Actions workflow for source-client compilation and regression tests. This workflow does not use the data-acquisition concurrency group, so it can test fixes while the original acquisition job is stalled.
- Commit 8241ef05 created check suite 107965316843, which entered IN_PROGRESS. The actual test conclusion has not yet been retrieved; do not treat the run being started as a pass.


## 2026-10-23 — source-client CI passed
- Independent source-client workflow check suite 107965316843 completed SUCCESS (18:47:42 UTC) for commit 8241ef05. Python compilation and pytest steps therefore passed, though the summary endpoint did not expose the individual pytest test count.
- The data acquisition run #39803647257 still reports IN_PROGRESS with its last API update at 15:18:56 UTC; the current recovery workflow suite remains PENDING behind the concurrency group. Its status needs another live check; no acquisition outcome is inferred.


## 2026-10-23 — partial cache recovery and strike-scope amendment
- Old acquisition #39803647257 was cancelled through a one-time, commit-message-gated recovery change because it stayed in the same step for 211 minutes. Its cache-save and sanitized artifact steps nevertheless completed.
- Downloaded artifact #12450341572 and inspected feature_availability.json: 720 JSON files parse, 716 historical weekly-option files plus three probes, one underlying probe, no historical underlying cache, and no historical monthly-option cache. This evidence is documented as a partial cache state, not an acquisition PASS.
- To finish within the fixed bounded run without optimizing on P&L, formally narrowed the protocol from OTM2+ to ATM/OTM1. Updated strategy_grammar_v2.py, evolve_candidates_v2.py, run_research.py and their regression tests; updated the frozen plan, source catalogue and phase status. Expected grid is 732 option request groups; cache filename counts suggest about 425 option requests and up to 23 underlying-history chunks remain.
- Independent source-client CI on the earlier bounded-client revision passed; new tests for the current ATM/OTM1 version are expected to run automatically and must be checked again.
- The workflow now uses a one-time conditional concurrency handoff, short request timeouts/two attempts, progress logging, cache-resume passes, and fail-closed source gating. Do not mark Phase 2 complete until the resumed job's artifact proves historical underlying and option coverage.


## 2026-10-23 — corrected ATM/OTM1 progress-test expectation
- The first source-client regression check after the moneyness amendment failed because one progress-counter fixture still expected ten option requests, inherited from the earlier five-offset universe.
- Corrected the fixture to expect six groups and five API fetches after one cache hit. Recorded as QE-NOB2-E028. The automatic source-client CI was re-triggered by this test-file push; no pass is assumed until the latest check suite concludes.


## 2026-10-23 — pre-restart regression disposition
- Grammar regression suite #107968717033 passed after OTM2 was removed from the allowed moneyness set and seed generator.
- Exact CI logs revealed the source-client failure was not the stale request-count assertion originally suspected; it was the consecutive-failure test supplying only six failures in one chunk, below the ten-failure threshold. Corrected the fixture to supply two chunks, so the stop condition should fire on the tenth failure. The earlier diagnosis was amended in QE-NOB2-E028.
- The recovery handoff still needs a fresh workflow push with the exact one-time phrase so an in-progress workflow that checked out the older five-offset client is cancelled. The restarted run must test the latest branch state before attempting acquisition.



## 2026-10-23 — exact CI log reviewed
- Retrieved the failed source-client run #39835953946 job log. Python compilation succeeded; pytest had 17 passed and 1 failed: test_option_acquisition_stops_after_consecutive_failures_and_preserves_cache raised KeyError because the mocked source loop only had six requests in one chunk and therefore could not reach ten consecutive failures.
- Corrected the test's mocked chunks to provide two contiguous chunks, allowing the loop to reach ten consecutive failures. This is a test-fixture defect, not evidence that the real source client failed to stop in a multi-chunk failure sequence. Re-run CI is pending.


## 2026-10-23 — source-client recovery regression passed
- Automatic independent source-client workflow [#39836310701](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310701) passed after the two-chunk early-stop fixture correction. Its log shows 18 passed in 1.24 seconds; Python compilation also succeeded.
- The same push queued acquisition workflow [#39836310700](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310700), but it is behind the stale recovery workflow tied to commit 706a27fa. The stale run must be cancelled with the explicit one-time recovery commit so the queue executes the latest ATM/OTM1 scope.


## 2026-10-23 — cancellation-target mistake and restart
- The first ATM/OTM1 recovery run #39836599391 made measurable progress, but the cancellation workflow triggered by later recovery commits used its unsafe default target #39836599391 and cancelled the new acquisition after 318/732 planned option request groups. The workflow audit, cache-save, and artifact upload completed; it recorded 313 cached requests, one downloaded file, four timeouts, and no historical underlying series.
- Inspected .github/workflows/qe-nob-v2-recovery-cancel.yml, found its default RUN_ID pointed to the new acquisition rather than the original stale run. Corrected default to original run #39803647257; manual dispatch still takes an explicit ID. Logged as QE-NOB2-E029.
- Updated the data workflow marker and triggered a new run with commit e02851ad. The new run should restore the saved cache and continue from valid files; do not delete the cache. The source-client regression CI remains passing at 18 tests.
- The cache audit's parseability PASS is not an acquisition completeness pass. Phase 2 remains open until historical underlying and option data coverage are confirmed.


## 2026-10-23 — weekly-only acquisition scope and stale-report correction
- Downloaded and inspected the sanitized artifact from cancelled run #39836599391. It shows 728 historical WEEK1 files across seven offsets, 314 files in allowed ATM/OTM1 offsets, 53 historical weekly chunks with at least one file, no historical underlying candles, and no historical monthly option files. The artifact's v1 acquisition_summary was stale (all 1,708 requests marked CACHED_PASS despite the run's cancellation); this has been recorded as QE-NOB2-E029 and the v2 client is redirected to a clean report namespace.
- Amended the fixed protocol to weekly expiry only, ATM/OTM1 only. Estimated option request grid is 366 groups, with about 52 eligible option files missing and around 23 underlying-history chunks to fetch; these estimates come from filename auditing and must be replaced by actual fresh-run counts.
- Updated config.json (QE-NOB-2.0, reports/quant_evolve_nob_v2, weekly_near only, 1,200-candidate cap, 20 generations, four fixed seeds); grammar rejects MONTH1, seeder only creates WEEK1 candidates, source probe now probes only WEEK1, and the data workflow now tests the active grammar/simulator/discovery suites before acquisition.
- No new candidate metrics were created from the cancelled runs. The next fresh report must be inspected for its own run identifier/timestamp, source status, historical underlying count, and exact request counts before Phase 2 can close.


## 2026-10-23 — weekly-only expiry amendment
- Reviewed the branch's latest commits while the data run was active. A config/grammar/source-gate amendment had restricted expiry to WEEK1 only because the earlier audit found no historical monthly cache. This is a source-coverage-driven protocol change and had not yet been recorded in the plan; amended OPEN_STRATEGY_DISCOVERY_PLAN.md, SOURCE_CATALOG_V2.md, PHASE_STATUS_V2.md, and ERROR_LOG_V2.md accordingly (QE-NOB2-E030).
- The current run #39837698610 started before the weekly-only configuration was committed and therefore remains an older two-expiry acquisition. It should not satisfy the updated gate. A newer pending run exists on the weekly-only code.
- Regression checks on recent commits are passing: source client #39838112165, candidate generator #39838066721, discovery runner #39838066761, option simulator #39838060682, signal evaluator #39838060728, and grammar validation #39838074982. The weekly-only acquisition workflow has been expanded to run these tests before acquisition.
- Next action: cancel the older data run via the exact recovery commit phrase (its always-run cache save and sanitized artifact upload should preserve progress) and let the latest pending weekly-only workflow resume. Do not use the helper workflow's default target for this cancellation.
