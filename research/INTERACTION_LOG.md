# Auditable activity / interaction log

Record user-facing decisions, concrete operations, results and links. This is not a verbatim transcript and must never contain private internal reasoning or hidden chain-of-thought.

## 2026-10-14 — initialization

- User requested fresh NIFTY 50 prediction research; no trading-strategy development; nine fixed phases; broad model comparison; robust statistics; separate developer/tester branches; manuscript; automated workflows and logs.
- Checked GitHub metadata for vishnuvcr/Naked-Options-v2. Repository is public, default branch main, initially reported size 0. README retrieval returned not found. Branch search returned no branches.
- Initialized README.md; first commit SHA returned by GitHub was e0b634fdb98da9a2ed136320a24afb7fdda8afb9.
- Searched the Project Library for previous studies and literature. Found a NIFTY ML paper in Cureus Journal of Computer Science (published 2026-10-01) and prior manuscripts from other research repositories. Read selected methods/results/limitations/reference pages. Treated these as contextual literature, not fresh output from this repository.
- Researched official NSE NIFTY 50 and India VIX pages, NSE historical reports, Dhan API support docs, NIFTY forecasting papers, Diebold-Mariano and Clark-West tests, White's Reality Check and data-snooping / PBO literature.
- Created the frozen research plan, questions, literature matrix, data catalog, experiment log, preliminary results register, phase status, error log, tester checklist, manuscript shell and reproducibility guide.
- At this checkpoint no source data API has been called, no market dataset has been acquired, no model has been trained, and no Actions run or Pages deployment is claimed.

## Interaction summary policy

Log actions and outcomes rather than private reasoning or a word-for-word chat transcript. If a workflow later runs, record its actual run ID / URL and status. If it fails or is not observable, state that honestly.

## 2026-10-14 — first data validation, compute bound, and source expansion

- Actual GitHub Actions logs (run 29) showed the Dhan cache contained 4,901 NIFTY daily records dated 2007-01-02 through 2026-10-13, with SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. No API token value was printed.
- Run 29 reported 20 weekend-dated records and the first version of the validator rejected them. Review concluded that weekend dates can include special exchange sessions; the validator was changed to report the dates as a warning and preserve them rather than silently discard observations. Later run 30 and run 31 passed the target validation, tests and feature-matrix steps.
- Target-construction and metric tests passed 8/8 in the inspected Actions log. This is test evidence, not a forecast performance result.
- A full catalogue run remained in the technical-model step long enough to trigger the fixed plan's compute budget. Sequence comparisons were bounded to next-session return/direction, three training epochs, two chronological folds; all other sequence target/horizon pairs are explicitly marked not run under the budget.
- Independent code inspection found that the metric field called out-of-sample R-squared used the realized holdout sample mean rather than a forecast available at the origin. The phase-5 branch was corrected to report benchmark-relative R-squared (1 - candidate MSE / benchmark MSE). The corrected run and a unit-test confirmation remain required before adopting results.
- Public free-source review recorded official NSE index/India VIX/breadth/FII-DII/derivatives reports and two Hugging Face options collections. The collections are not ingested yet: one is CC-BY-NC-4.0 and ~4 GB, the other has 'other' licensing, ~2.5 GB and incomplete intraday OI/settlement fields. See DATA_CATALOG.md.
- At the last check, run 30 on main, run 31 on research/phase-5-models, and the corrected run 32 were respectively active/active/queued. No completed model metrics have yet been accepted.


## 2026-10-14 — separate option-buying validation initialized

- User approved extending the closed prediction-only study with a separate, bounded option-buying validation phase. The original NIFTY-PRED-1.0 plan/results remain unchanged.
- Audited README, the frozen plan, data catalog, execution policy, phase status, results register, error log, experiment log, original workflow, feature-construction code, classifier/model-selection implementation and source availability before initiating this track.
- DhanHQ v2 expired-options documentation describes historical rolling-option intraday OHLC/IV/OI/spot data, up to 30 calendar days per request and a rolling five-year window. The current option-chain endpoint is real-time, so it cannot substitute for historical option quotes.
- Scope chosen: same-session intraday entry/exit only. Rolling relative strikes/expiry data do not prove a stable contract can be tracked across multiple days; multi-day P&L is excluded unless contract identity and expiry are available and verified.
- Cost plan includes Paytm Money ₹10/order baseline, ₹20/order sensitivity, option-sale STT, stamp duty, SEBI/exchange charges and adverse 0/25/50/100 bps-per-side slippage sensitivity. Since the rolling OHLC source lacks historical bid/ask, this is a sensitivity analysis, not an observed-spread simulation.
- No historical option data has yet been downloaded and no option P&L has been computed at this point. The log records auditable actions and decisions, not hidden reasoning or verbatim internal chain-of-thought.


## 2026-10-14 — option source diagnostic update

- Verified official DhanHQ expired-options documentation and official DhanHQ-Py request construction. Dhan documents POST /charts/rollingoption, NSE_FNO, NIFTY securityId 13, instrument OPTIDX, intervals 1/5/15/25/60, MONTH/WEEK, and a maximum 30-day range; the published example uses MONTH and expiryCode=1. Sources: https://dhanhq.co/docs/v2/expired-options-data/ and https://github.com/dhan-oss/DhanHQ-py/blob/main/src/dhanhq/_historical_data.py
- Runs #4 and #5 failed at the first request with HTTP 400 and zero acquired option records. No option strategy result is claimed.
- Updated the adapter to use the published MONTH/1 example and capture a short redacted error detail. Run #6 is the retest for that request format.
- Verified official NSE costs: option-sale STT was 0.10% through 2026-03-31 and is 0.15% from 2026-04-01; option stamp duty is 0.003% on buyer turnover; SEBI turnover fee is ₹10/crore; NSE Circular 1 dated 2026-02-27 gives a combined equity-options charge outflow of approximately ₹3,553/crore from 2026-03-01. Sources: https://www.nseindia.in/static/products-services/equity-derivatives-securities-transaction-tax, https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies, https://nsearchives.nseindia.com/content/circulars/FA73061.pdf
- Paytm Money's current public F&O FAQ lists ₹10 brokerage per executed unique order: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web. ₹20/order remains the sensitivity case.
- No live order will be placed. The test is intraday-only and stays blocked until options quotes, cost accounting, statistics and independent review pass.

## 2026-10-14 — resume: option validation pilot and correction

- Resumed user-approved option-buying validation from GitHub state, inspected the current branch/workflow and previous pilot outputs.
- Run #6 successfully received 196/196 Dhan monthly-option responses, but only 171/980 candidate dates (17.45%) had valid fixed-strike entry/exit quotes. Four alert-filtered candidate variants had negative mean premium-normalized returns and fewer than 100 alert trades. Because the predeclared 80% coverage gate failed, the pilot p-values are not accepted as confirmatory strategy evidence.
- Run #7 failed one redaction test due to a fake response missing errorCode/errorMessage. The legacy ATM cache fallback also contained a date formatting typo; both are corrected in the current source and retest.
- The corrected source queries monthly ATM−3…ATM+3 series for both option types, reuses only verified MONTH/expiryCode=1 cache files, indexes exact-strike exits and vectorizes bootstrap draws.
- The primary comparison now tests daily net rupee P&L per one-lot-proxy slot on identical eligible dates, using zero on no-alert dates; premium-normalized returns are secondary due to the variable/undefined denominator when filtering trades.
- Current corrected Actions run: #9. No option-buying strategy is approved and no live order was placed.

## One-step OTM verification follow-up — 2026-10-14

- Static review of the active corrected-rerun code found that the strangle builder currently selects the nearest available call strike above ATM and put strike below ATM. If the exact adjacent quote is missing, it could accept a farther OTM strike while the plan describes a one-step OTM strangle.
- This was logged as ERR-OPT-004. The active run #9 is allowed to finish as a coverage pilot; its strangle results are preliminary until the next cached rerun enforces exact ATM+1 CALL and ATM−1 PUT relative offsets at entry, and exact numeric strike matching at exit. If either required entry series is absent, that date must be skipped rather than substituted.


## 2026-10-14 — wider-strike acquisition completed; analysis running

- Corrected run #9 passed the pre-acquisition unit-test gate and finished its expanded Dhan request step; its private market-data cache-save step succeeded. The P&L/statistical step is now active. The acquisition counts and quote-coverage outcome will be taken from the run manifest after the workflow writes it; step exit status alone is not treated as data-gate approval.
- The narrow-grid pilot and exact one-step OTM selection issue remain logged. No strategy recommendation is made until exact-entry matching, coverage, costs, primary P&L statistics and independent review pass.


## 2026-10-14 — final option-validation disposition

- Separate [developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-developer) and [independent tester](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-independent-tester) branches were created from the completed result state.
- Run #11 completed the corrected cached option acquisition, P&L analysis, manuscript/chart rendering and 13-test pre/post gates. Artifact SHA-256: 86e9d03c6c55c17d46348a8dc40b9a02f247f2f9bca38703110c74c030be889.
- Independent tester audited 48,032 trade-ledger rows; net P&L = gross P&L minus total costs to <2e-12 rupees, fee components to <5e-13, and the four paired means/intervals/p-values and Holm adjustments reproduced.
- Quality limits failed: strangle coverage 69.18%, duplicate-conflict rate 1.409%. All four filtered candidates have negative net daily P&L intervals, and every 100-bps/both-half profitability check fails.
- Developer accepted tester no-go. OPT-BUY-1.0 is closed for this protocol. No strategy, paper trading or live deployment is approved; broader hypothesis remains inconclusive due data-quality limitations.

## 2026-10-14 — OPT-BUY-2.0 continuation

- User instructed “Proceed”; initiated bounded strike-selection grid with fixed classifier, 16 prespecified call/put relative-offset pairs and 5/20-session horizons.
- Run #1: regression tests passed (13/13); strike grid blocked because no usable option quote rows were loaded. [Run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841).
- Corrected blocked-run diagnostics and added the prespecified block-bootstrap/Holm inference family. Follow-up [run #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551939491) and [run #3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552000337) were in progress/pending when logged.
- Developer branch: `research/option-strike-selection-developer`; independent tester branch: `research/option-strike-selection-independent-tester`. Tester disposition is blocked pending usable quotes. No strategy approval or fabricated P&L.

## 2026-10-14 — user instruction on OPT-BUY-2.0 review gate

- User instructed: “No tester review needed. Proceed.” Developer workflow continues without waiting for the separate tester sign-off. This changes the review requirement only; it does not waive data-quality, statistical, or execution-cost acceptance criteria, and does not authorize unsupported claims or live trading.
- Corrected workflow run: [38552144097](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097). Daily-data acquisition and validation steps completed; options-cache acquisition is still running at time of entry. Final status and bounded disposition will be recorded from the run's artifacts.


## 2026-10-14 — OPT-BUY-2.0 status request

- User asked for the current status. Checked live GitHub Actions run metadata, job-step state, artifact listing, branch workflow, phase-status file, error log, and research ledger.
- At 17:34 IST / 12:04 UTC, [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) remained active at “Acquire/reuse options cache”; that step started at 10:49:21 UTC. Steps 1–8 had completed, including daily-data validation and 13 regression tests. Strike grid, sanitized artifact upload and final regression tests were pending; the run had no artifacts at the time of check.
- Recorded the live status across README, phase status, error log, experiment log and this activity log. No conclusion was inferred from the still-running run.


## 2026-10-14 — subsequent live poll after status update

- Rechecked [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097), the latest job steps and artifact listing. Status progressed from options-cache acquisition to the frozen strike-grid step. Daily data validation and 13 pre-analysis tests had completed; sanitized artifacts were still absent because upload remained pending.
- Updated README, phase status, error log, experiment log and interaction log. The options step's success status was not treated as proof of adequate usable quotes because the step permits continuation on acquisition errors.


## 2026-10-14 — OPT-BUY-2.0 run #4 results and corrective retest

- User said “Proceed.” Retrieved the completed [run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) job logs and sanitized artifact. Workflow succeeded and 13 regression tests passed before and after analysis.
- Results: 1,055,699 raw / 1,023,541 usable quote rows; conflict rate 1.4256% (gate <=1%); candidate coverage 83.27% down to 16.94% (gate >=80%). Confirmatory gate failed.
- All 32 model-filtered candidate × horizon mean net P&Ls at 50 bps/side and ₹10/order were negative, with 95% block-bootstrap upper bounds below zero. Therefore no candidate is approved; the grid is exploratory only. Common-date sensitivity was not produced.
- All 32 p-values were NaN in the artifact. Committed a bounded correction to the p-value calculation (a543eed8059de79dbcc6b2dc53a3dd31f14298a9) and started [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651). No additional parameter grid will be run. User waived separate tester sign-off; the correction still needs to produce valid statistics.
- Updated README, phase status, error log, experiment log and activity log with actual run evidence and the no-go disposition.


## 2026-10-15 — OPT-BUY-3.0 entry/exit scope pivot

- User directed the project to pause prediction and test option-buying entries/exits from random to targeted rules.
- Audited the existing repository plan, phase status, error log, previous option-buying disposition, Dhan quote parser, cost model and Actions workflow.
- Created developer branch `research/option-entry-exit-developer`. Frozen plan commit: `8215bc71aee08b6563a3f58a4f441fdffed02fa3`; research questions commit: `7e4066c3151ee76ae4bf08ec0eb9179730f55ca7`.
- Added partial time-entry screen, helper tests and a manual/push-triggered workflow in commits `17bbf88c26734782af3fa4f0e3d1bbb166f8819d`, `9c3fedfecad60d9e24f5672a2c138fd120cb8a23`, `53029f81971b7adb395ac76a8b936830bbd6be7a`.
- The executable is not yet the full frozen catalogue. No Actions result was verified during this log update; no candidate is approved. Independent tester branch/report must wait until results are acquired.
- Log operational actions and outcomes, not hidden chain-of-thought or verbatim internal reasoning.


## 2026-10-15 — User removes independent reviews

- User explicitly instructed: “I don't want any independent reviews!”
- Confirmed no independent tester role, separate tester branch, or tester-report dependency will be used.
- Updated the OPT-BUY-3.0 protocol on research/option-entry-exit-developer (commit aa379a8099a3146ae6cde79886606b765d1fda01). Automated quality checks remain mandatory; this changes governance only, not data gates or statistical acceptance criteria.
- Current implementation is partial and latest saved results are blocked for lack of valid quotes. This is not a positive or negative strategy result. The repository status explicitly lists the outstanding full-catalogue, cost sensitivity, session accounting and exit-matching work.
- Only operational decisions and actions are logged; private hidden reasoning is not copied into repository files.


## 2026-10-15 — Continue OPT-BUY-3.0

- Inspected actual GitHub Actions run #3. It completed successfully at the workflow level, but the empirical result was BLOCKED_NO_VALID_QUOTES with zero candidates; 16 tests passed. This was not treated as a strategy result.
- Identified stale-manifest logic that skipped acquisition despite no usable quote rows; workflow changed to require a successful manifest plus at least one existing valid cache file before reusing cache, otherwise it attempts refresh.
- Identified single-leg backtest passing through a legacy two-leg-only cost helper. Replaced that path with explicit single-leg fee/slippage calculation and expanded tests.
- Expanded finite screen to seeded random direction/time, fixed-time CALL/PUT controls, causal spot-momentum/range-breakout entries; EOD, fixed-hold, premium TP/SL and trailing exits; 0/25/50/100 bps per-side and ₹10/₹20 per-order sensitivities. New run triggered; empirical results pending.
- No independent tester branch or review gate was created. Operational notes only; hidden reasoning is not logged.


## 2026-10-15 — Data acquisition dependency fix

- Run #6 completed successfully as a workflow, with the automated tests passing, but the output remained blocked. The sanitized option manifest showed BLOCKED_NO_VALID_DAILY_DATA, zero request records, and specifically `FileNotFoundError: Validated daily NIFTY cache is missing: data/cache/nifty50_daily.csv`.
- Added a workflow pre-step to acquire the daily target cache using the repository's existing Dhan/NSE/Yahoo fallback adapter if it is absent, then require a non-empty target file before rolling-option acquisition. Commit `0d9eb96d36316bf009f88e828d37812b2cd286cd`; run #7 queued.
- No strategy results are inferred from blocked runs. No independent review process is used.
