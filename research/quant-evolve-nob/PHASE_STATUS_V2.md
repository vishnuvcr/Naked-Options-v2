# Phase status — QE-NOB-2.0

Last updated: 2026-10-22
Governance: developer-led; user explicitly said “No tester.” No tester branch/report will be created or awaited.

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 1. Protocol amendment and structural novelty specification | COMPLETE | [Open discovery plan](OPEN_STRATEGY_DISCOVERY_PLAN.md) freezes research questions, candidate budget, statistical gates and stop condition. |
| 2. Data and feature feasibility | IN PROGRESS — feature-builder unit tests pass; bounded cache acquisition still running | Static source catalogue is documented in [feature feasibility](FEATURE_FEASIBILITY_V2.md). First audit found zero local files, which is not evidence that Dhan or other public sources are unavailable. [Bounded acquisition/cache workflow](../../.github/workflows/qe-nob-v2-data-audit.yml); current run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257). Require a non-empty, quality-audited source cache or a documented source blocker before moving on. |
| 3. Typed strategy grammar and tests | IMPLEMENTED; last verified run passed | Typed predicates, numeric/categorical validation, structural signatures, novelty distance, deterministic mutation/crossover and lineage. [Grammar tests](test_strategy_grammar_v2.py), [successful CI #39802894371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894371). |
| 4. Signal timing and simulator | PARTIAL — unit tests pass; empirical validation blocked | [Signal evaluator](signal_evaluator_v2.py) maps a signal to the next actual market bar and rejects unsupported entry modes. [Option simulator](option_simulator_v2.py) pre-indexes bars, enforces no-overlap per candidate, uses modeled costs/slippage and supports only time exit / premium stop / premium target; conservative same-bar priority is stop first. [Simulator tests #39801813009](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801813009) and [signal tests #39801804759](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801804759) passed. Rolling OHLC still cannot prove exact contract identity, historical bid/ask/depth or executable fills. |
| 5. Bounded novelty-aware discovery | IMPLEMENTED; EMPIRICAL RUN BLOCKED | `run_discovery_v2.py` now wires four fixed-seed islands to training-only multi-objective fitness, validation-based finalist selection, sealed chronological OOS, block bootstrap, Holm correction and cost stresses. Feature eligibility is now frozen from training-only coverage/variation. Automated runner/statistical-utility tests passed in #39807638261 and training-fitness/candidate tests passed in #39807602936; no market-data fitness result is claimed until the acquisition/cache gate passes. [Discovery runner](run_discovery_v2.py); [candidate generator](evolve_candidates_v2.py). |
| 6. Frozen out-of-sample validation and robustness | NOT STARTED | Must use frozen chronological splits, Holm correction, session-block bootstrap, multiple slippage/brokerage stresses, regime/time-block stability and baselines. Do not tune or select against the final OOS period. |
| 7. Manuscript and bounded decision | NOT STARTED | Complete manuscript, reproducibility/supplementary outputs, tables/charts, limitations and a final GO / NO-GO / DATA-LIMITED decision. Stop after this phase; no live-trading approval. |

## Current verified checkpoint

- Grammar tests: 15 passed in combined grammar + feature-audit workflow #39802894371.
- Standalone feature-audit tests passed in #39802894311.
- Candidate generator, signal evaluator and option simulator workflows passed in #39802753682, #39801804759 and #39801813009, respectively.
- Initial cache audit artifact from run #39803204747 reported `BLOCKED_NO_LOCAL_CACHE`, zero underlying/option files, no verified exact contract IDs and no bid/ask/depth. A new bounded acquisition job was added and automatically triggered as run #39803647257; its outcome must be checked before updating the Phase 2 decision.
- No QE-NOB-2.0 candidate has been backtested for fitness or shown profitable. The old QE-NOB-1.0 no-go decision is unchanged and its fitness/OOS results are not reused.

## Mandatory constraints

- Only verified features may enter discovery; missing values are never silently fabricated.
- No short-option legs, live order placement, synthetic quotes, or OOS tuning.
- Model Paytm Money brokerage assumptions and date-effective statutory/exchange fees, plus adverse slippage; quote/fill evidence is still required for an execution pass.
- The simulator fails closed on unsupported exits. Implement and test each new entry/exit semantic before enabling it in candidates.
- No tester branch/report, per user's explicit instruction. Developer-side automated regression tests remain mandatory.
- Stop at Phase 7 or an explicit data blocker; do not run an unbounded search.


## Additional verification checkpoint — 2026-10-22 21:05 IST

- Point-in-time feature builder tests passed in run #39805843560.
- Same-session signal timing tests passed in run #39806277479; simulator same-session handling passed in run #39806376781.
- Expiry-family normalization and the focused regression test passed in simulator workflow #39806477859 (12 tests).
- Bounded source acquisition run #39803647257 remains in progress. Phase 2 stays open until its audit artifact is inspected. Phase 5 discovery stays blocked: no fitness run or candidate P&L has been verified.


## Discovery runner checkpoint — 2026-10-22 21:10 IST

- Phase 5 code path is implemented but has not been run on market data. The runner enforces training-only fitness, validation selection, and a sealed final OOS block; OOS statistical gates include a 5-session moving-block bootstrap, Holm correction, and 0/25/50/100/200 bps slippage with ₹10/₹20 brokerage stresses.
- Feature allowlist eligibility is computed on the training period only; full-sample feature coverage is diagnostic only.
- Statistical utility regression tests passed in runner workflow #39807638261; candidate/training fitness tests passed in #39807602936.
- Runtime source acquisition run #39803647257 remains in progress. Phase 2 and the empirical Phase 5 run are blocked pending its sanitized audit result.


## Automation handoff checkpoint — 2026-10-22

The bounded acquisition workflow now automatically invokes the v2 discovery runner after successful acquisition and cache audit, and uploads sanitized candidate/validation/OOS/stress reports. Workflow #39808171927 is queued behind acquisition run #39803647257, so no manual user workflow action is required. Phase 2 remains open until the acquired cache report is inspected; Phase 5 is implemented and test-verified but not yet empirically completed.


## Cache-gate regression — 2026-10-22

The discovery-runner CI passed after adding the stricter cache audit gate: [run #39808407294](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808407294). It now rejects any cache with JSON parse failures or without both underlying and option files. A later CI run #39808626484 uses a leaner dependency set to reduce unrelated installation time.


## Continuation check — 2026-10-22 21:24 IST

- Discovery-runner CI #39808626484 completed successfully; this is software-test evidence only.
- Acquisition run #39803647257 remains in progress at the source-acquisition step. Cache audit, cache save, and report upload are still pending.
- Automatic follow-up #39808171927 remains pending; no jobs or discovery results have been produced by that run yet.
- No phase gate changed: Phase 2 remains in progress, Phase 5 empirical discovery remains blocked, Phases 6–7 remain not started, and execution remains FAIL pending exact contract and executable quote/fill evidence.


## External source catalogue checkpoint — 2026-10-22

- Completed a public-source review and recorded source capabilities, provenance concerns, licensing decisions and composite-data rules in [SOURCE_CATALOG_V2.md](SOURCE_CATALOG_V2.md).
- Confirmed official/free source candidates for daily NIFTY index / India VIX and provisional FII/DII series; global daily volatility/macro candidates; and independent NIFTY underlying OHLC cross-check candidates.
- Public option datasets were not imported: one Hugging Face listing gives only license 'other', and another is CC BY-NC 4.0; both remain unapproved for this trading-oriented evidence pipeline until rights are resolved.
- The code-defined Dhan request loop implies approximately 1,708 option requests before retries for two expiry families across the five-year window. This is a request-count estimate, not evidence that the calls have completed.
- **No gate change:** Phase 2 remains IN PROGRESS until live acquisition and cache audit evidence is available. Phase 5 empirical discovery remains blocked. No external dataset was added to candidate fitness, and the execution gate remains FAIL.


## Acquisition stall remediation — 2026-10-23

- Diagnosis: the previous acquisition client had no periodic progress output and could spend 50 seconds per HTTP attempt across three attempts. Its source loop requested seven relative-strike offsets, while the v2 simulator/grammar supports only ATM through OTM2. The live run #39803647257 has remained in the source-acquisition step since 2026-10-22 15:18:51 UTC; logs are not accessible while the job is active, so the exact last request cannot be confirmed.
- Developer correction committed to the active branch: source client now requests offsets -2 through +2 (five offsets, both sides), uses 25-second option-request timeouts / two attempts, limits underlying request attempts to two, prints progress every 25 requests, and halts after ten consecutive request failures. Approximate configured request count falls from 1,708 to 1,220 for two expiry families, before retries; this is an estimate, not completed-call evidence.
- Empty option responses are no longer written as reusable cache files; any old cached empty response encountered will be deleted and re-requested. Acquisition must complete all planned response groups without failures and have at least 80% non-empty option responses; incomplete acquisition or incomplete underlying data exits non-zero so discovery is not run on an incomplete acquisition.
- Regression tests added for the reduced supported offset domain, bounded retries, stop-on-consecutive-failure behavior, empty-data coverage gating, and the fail-closed acquisition gate. The acquisition workflow's push-path filter will be updated to run automatically when its source client/tests change.
- **Phase gate is unchanged until a corrected workflow run produces evidence:** Phase 2 remains IN PROGRESS, Phase 5 empirical discovery remains BLOCKED, Phase 6–7 remain NOT STARTED, and execution remains FAIL. The existing active run uses its original checked-out code; the already-queued follow-up will be the first eligible run to use the repaired client. No test/market result is claimed before CI executes.


## Latest recovery CI queue checkpoint — 2026-10-23 00:13 IST

- The previous pending run #39808171927 was cancelled at 2026-10-22 18:41:39 UTC when later branch updates replaced the pending concurrency slot. Do not use that run as verification.
- Current source/test checkpoint commit [9ef5f663](https://github.com/vishnuvcr/Naked-Options-v2/commit/9ef5f663122a8b802445a618e3bf91f022590d65) has GitHub Actions check suite [107963790987](https://github.com/vishnuvcr/Naked-Options-v2/commit/9ef5f663122a8b802445a618e3bf91f022590d65/checks), which is pending and has no check runs yet. It was created at 18:43:46 UTC on 2026-10-22.
- Original acquisition run #39803647257 remained in progress at the latest check, with no update since 15:18:56 UTC. The corrected check suite is waiting for the concurrency slot. Its exact timeout/completion must be observed; do not assume it timed out or succeeded.
- Source review caught and corrected a progress-accounting defect and an unchanged underlying timeout in the first patch. The correction is logged as QE-NOB2-E025, with a regression test in `test_run_research.py`. CI outcome remains pending.
- **Current gate:** Phase 2 remains IN PROGRESS; empirical Phase 5 is BLOCKED pending the runtime cache gate; Phases 6–7 are NOT STARTED; execution remains FAIL. No strategy outcome is available.


## Independent source-client CI checkpoint — 2026-10-23 00:17 IST

- Added [independent source-client regression workflow](../../.github/workflows/qe-nob-v2-source-client-tests.yml), with automatic push triggers and a manual dispatch button. It compiles the acquisition client/tests and runs pytest independently of the long acquisition workflow's concurrency group.
- The new workflow check suite [107965316843](https://github.com/vishnuvcr/Naked-Options-v2/commit/8241ef05cea41a75a309f2cec979f0b69587a2e7/checks) entered IN PROGRESS at 18:46:58 UTC on 2026-10-22. No test conclusion has been observed yet.
- The original acquisition run #39803647257 was still reported IN PROGRESS at the most recent poll, last updated at 15:18:56 UTC. The recovery workflow suite is still pending behind its concurrency group; the independent test workflow does not share that lock.
- No empirical result has been produced. Phase 2 is IN PROGRESS, Phase 5 discovery remains BLOCKED, Phases 6–7 remain NOT STARTED, and execution remains FAIL.


## Independent source-client test outcome — 2026-10-23 00:18 IST

- Independent workflow check suite [107965316843](https://github.com/vishnuvcr/Naked-Options-v2/commit/8241ef05cea41a75a309f2cec979f0b69587a2e7/checks) completed with conclusion SUCCESS at 18:47:42 UTC. This includes Python compilation and the source-client pytest suite; the number of individual tests is not independently exposed by the summary we retrieved.
- The old acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was still reported IN PROGRESS with an unchanged update timestamp of 15:18:56 UTC at the same check. The corrected acquisition check suite remains PENDING behind its concurrency group. This is a workflow scheduling/runtime block, not a passing or failing market-data result.
- The independent tests pass, but no verified cache audit, candidate fitness, OOS statistics, or P&L is available. Phase 2 stays IN PROGRESS; Phase 5 discovery stays BLOCKED; Phases 6–7 stay NOT STARTED; execution remains FAIL.


## Runtime evidence and protocol amendment — 2026-10-23

- The old acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) ended CANCELLED, not success, after it had exceeded the configured 210-minute job budget without progress. The always-run audit/cache-save/artifact steps ran successfully on cancellation.
- Its uploaded audit artifact [#12450341572](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) shows 720 parseable JSON files overall: 719 option-folder files (716 historical weekly option files plus three probes), one underlying probe, zero JSON parse failures, **zero historical underlying files, and zero historical monthly option files**. Historical weekly option files only cover 52 chunks and include partially missing strike-offset groups. These values are from the audit artifact and are not a completed acquisition summary.
- The cancelled run's cache-save step succeeded. The corrected workflow should restore the partial cache through its cache restore-prefix and resume missing groups; do not discard or re-download valid cached data.
- **Protocol amendment:** based strictly on observed cache coverage and runtime, not strategy/P&L outcomes, the active research universe is narrowed to ATM and one-step OTM. The allowed moneyness set and seed generation now exclude OTM2, the downloader requests only offsets -1, 0, +1, and tests enforce this. The updated protocol is [OPEN_STRATEGY_DISCOVERY_PLAN.md](OPEN_STRATEGY_DISCOVERY_PLAN.md); external source/cache details are in [SOURCE_CATALOG_V2.md](SOURCE_CATALOG_V2.md).
- Estimated full option request grid is 732 groups (two expiry families × 61 chunks × three offsets × two sides). Approximately 307 historical weekly files in the amended offsets appear reusable, leaving roughly 425 option groups plus up to 23 underlying-history chunks and source probes. This is a planning estimate; only resumed workflow logs/audits establish actual acquisition status.
- Independent source-client CI passed at check suite [#107965316843](https://github.com/vishnuvcr/Naked-Options-v2/commit/8241ef05cea41a75a309f2cec979f0b69587a2e7/checks) before the latest scope narrowing. Latest grammar/source changes must pass their own subsequent CI before being treated as verified.
- Current gate is still **Phase 2 IN PROGRESS**, Phase 5 empirical discovery BLOCKED pending the resumed cache audit, Phases 6–7 NOT STARTED, and execution FAIL. No candidate scores or strategy profitability have been established.


## Scope-amendment regression checkpoint — 2026-10-23

- Grammar CI passed on [check suite #107968717033](https://github.com/vishnuvcr/Naked-Options-v2/commit/ada4d63039e4449465d6c7c4bb23230b844df240/checks), including the explicit test that OTM2 is rejected and mutations remain within ATM/OTM1.
- Source-client CI initially failed because the fail-fast fixture only provided six request failures in one chunk, below the ten-failure threshold. The corrected fixture now supplies two chunks in commit [e9982ddc](https://github.com/vishnuvcr/Naked-Options-v2/commit/e9982ddc1ee7cabb0a5aa3a581c1441df16b5cfb). The re-run [#39836310701](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310701) passed: 18 tests in 1.24 seconds.
- The in-progress data-workflow check at this checkpoint still originates from recovery commit [706a27fa](https://github.com/vishnuvcr/Naked-Options-v2/commit/706a27fa6c1d464eebd06b50b54894ec6da97e64), which predates the ATM/OTM1 amendment. It must be replaced by the specifically gated recovery commit so the restarted acquisition uses the current amended code and retained cache.


## Latest recovery handoff checkpoint — 2026-10-23

- Independent source-client workflow [#39836310701](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310701) completed SUCCESS on commit [e9982ddc](https://github.com/vishnuvcr/Naked-Options-v2/commit/e9982ddc1ee7cabb0a5aa3a581c1441df16b5cfb): Python compile passed and all 18 pytest cases passed (1.24s).
- The acquisition workflow triggered by the same push, [#39836310700](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310700), is pending behind the in-progress old recovery run from commit #706a27fa, which predates the strike-scope amendment.
- Next action: make one final recovery handoff commit that satisfies the workflow's explicit commit-message guard; it should cancel the stale in-progress data run and run the latest ATM/OTM1 code. The partial cache from #39803647257 was saved and should be restored. No strategy or market-data result is implied by the passing unit tests.
- Gates remain: Phase 2 IN PROGRESS, Phase 5 empirical discovery BLOCKED pending new cache audit, Phases 6–7 NOT STARTED, execution FAIL.


## Resume checkpoint — cancellation-target correction

- The amended acquisition run [#39836599391](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836599391) was cancelled at 318/732 planned option request groups by the one-time cancellation workflow. Its cache save and sanitized artifact upload succeeded. The log showed 313 cache hits, one newly downloaded valid option file, and four timed-out requests before cancellation; no historical underlying data was acquired.
- Root cause: the cancellation workflow default target was mistakenly set to run #39836599391, the new acquisition, instead of the original stale run #39803647257. This was logged as QE-NOB2-E029. The default target is now corrected to #39803647257, which is already cancelled; any future manual cancellation requires an explicit run ID.
- New data workflow commit [e02851ad](https://github.com/vishnuvcr/Naked-Options-v2/commit/e02851ad7736c111398bb7d2903cc3f0cb9891c0) triggers a fresh acquisition under the amended ATM/OTM1 scope and will restore cached data. Source-client CI has passed (18/18); acquisition completeness remains unverified.
- Audit PASS means files parse and expected field names exist; it does not establish sufficient non-empty historical underlying bars or monthly/weekly option coverage. Keep Phase 2 open until acquisition summary and feature availability prove source coverage.
- Current gates: Phase 2 IN PROGRESS, Phase 5 discovery BLOCKED, Phases 6–7 NOT STARTED, execution FAIL.


## Weekly-only cache-recovery amendment — 2026-10-23

- Both previous long acquisition attempts are now completed with conclusion CANCELLED (run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) and run [#39834802715](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39834802715)); their always-run audit/cache-save/artifact steps succeeded. A third ATM/OTM1 recovery run [#39836599391](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836599391) was also cancelled to save its cache and update scope. Its partial artifact is [#12452390413](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836599391).
- The latest artifact must be interpreted carefully: 728 historical WEEK1 option files, 314 historical option files at offsets -1/0/+1 across 53 observed date chunks, zero historical underlying bars (one probe only), zero historical monthly options, and zero JSON parse failures. The artifact's acquisition_summary.json contained an old CACHED_PASS/1,708-request summary from the v1 report namespace; it is stale and explicitly rejected as evidence of a completed run. Fresh outputs are now redirected to reports/quant_evolve_nob_v2.
- Active scope amended before resumption: WEEK1 weekly expiry only and ATM/OTM1 only. Month1 is excluded because no historical monthly cache exists in the inspected artifacts. Expected weekly option grid is 366 groups (about 61 chunks × 3 offsets × 2 sides); 314 eligible files are present in cache, so around 52 option groups plus roughly 23 underlying-history chunks and probes remain. These are file-count estimates; live progress/audit is authoritative.
- Updated the strategy grammar, candidate seeder, client source gate, source-client tests, v2 config and artifact paths. Added a workflow step that checks active v2 grammar/candidate/feature/simulator/discovery tests before acquisition. Report namespace changes and weekly-only protocol amendment are documented in [OPEN_STRATEGY_DISCOVERY_PLAN.md](OPEN_STRATEGY_DISCOVERY_PLAN.md), [FEATURE_FEASIBILITY_V2.md](FEATURE_FEASIBILITY_V2.md) and [SOURCE_CATALOG_V2.md](SOURCE_CATALOG_V2.md).
- **Gate remains blocked until the new workflow passes and a fresh acquisition/audit run shows historical underlying and weekly option coverage:** Phase 2 IN PROGRESS, Phase 5 empirical discovery BLOCKED, Phases 6–7 NOT STARTED, execution FAIL. No candidate fitness or P&L has been accepted from these cancelled artifacts.


## Weekly-only expiry scope and CI checkpoint — 2026-10-23

- The active data run [#39837698610](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39837698610) started before the weekly-only configuration was committed and still uses the earlier two-expiry request grid. It remains IN PROGRESS at the latest poll; job logs are not available while the job is running. It is not eligible to satisfy the amended weekly-only protocol.
- Latest weekly-only code changes are committed: config restricts expiry buckets to WEEK1, grammar/mutations reject MONTH1, and the source gate filters MONTH1 out. This is grounded in the earlier audit showing no historical monthly cache, not in candidate performance. The amended plan and source catalogue now estimate 366 request groups (weekly only), around 307 reusable files, roughly 59 remaining option groups plus up to 23 underlying chunks.
- CI on recent protocol commits: source-client workflow #39838112165 SUCCESS; candidate generator #39838066721 SUCCESS; discovery runner #39838066761 SUCCESS; option simulator #39838060682 SUCCESS; signal evaluator #39838060728 SUCCESS; grammar workflow #39838074982 SUCCESS. The full data workflow's pre-acquisition gate now also runs source-client, grammar, candidate-generator, feature-builder, option-simulator and discovery-runner tests.
- Next safe step is a guarded handoff: cancel only the older two-expiry run (which will save its cache/artifact), then let the newest pending data workflow restore cache and run the WEEK1-only request grid. The cancellation workflow default remains the original stale run #39803647257; this handoff must use the explicit data-workflow commit guard rather than the cancellation helper.
- Phase 2 remains IN PROGRESS; Phase 5 discovery remains BLOCKED until the new weekly-only source gate passes with historical underlying data; Phases 6–7 remain NOT STARTED; execution remains FAIL.


## Weekly-only handoff execution — 2026-10-23

- The pre-amendment two-expiry run [#39837698610](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39837698610) was explicitly cancelled via the cancellation helper after the WEEK1-only protocol and pre-acquisition regression gate were committed. Its cancellation request returned HTTP 202; the run then reported CANCELLED. Its always-run cache-save/artifact steps are expected to preserve partial cache; verify the artifact once final run status is available.
- The latest data run [#39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) is IN PROGRESS on the weekly-only branch head. It has restored cache, completed checkout and Python setup, and is installing dependencies; it will run source-client and full grammar/feature/simulator/discovery regression gates before acquisition. This is the eligible run for the amended protocol.
- Duplicate pending run #39838710148 was cancelled using an explicit temporary target; the recovery helper default was restored to the original already-cancelled run #39803647257. No further cancellation commits should be made while #39838508682 is active.
- Regression CI on the amended code passed: source client #39838112165, candidate generator #39838066721, discovery runner #39838066761, option simulator #39838060682, signal evaluator #39838060728, and grammar #39838074982. The active data workflow repeats those gates before acquisition.
- Gates: Phase 2 IN PROGRESS; Phase 5 empirical discovery BLOCKED pending the weekly-only source audit and historical underlying series; Phases 6–7 NOT STARTED; execution FAIL.
