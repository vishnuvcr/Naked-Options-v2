# Phase status and gate decisions

Last updated: 2026-10-22  
Research version: NIFTY-PRED-1.0

| Phase | Branch | Status | Evidence / next action |
|---|---|---|---|
| 1. Repository audit and design | research/phase-1-audit | COMPLETE FOR CURRENT SCOPE | Repository initialization and execution policy are documented. Reopen only if scope changes. |
| 2. Literature review | research/phase-2-literature | PARTIAL, ACCEPTED LIMITATION | First-pass review and source register are included; exhaustive review across all media/source families was not completed and is stated as a limitation. |
| 3. Data collection/validation/cache | research/phase-3-data | PASS WITH LIMITATIONS | Run #49 validated cached NIFTY data and seven external series. Rejected series and unavailable options/FII-DII/PCR/breadth/news inputs are documented. Global timing/holiday alignment still needs audit. |
| 4. Baselines | research/phase-4-baselines | COMPLETE FOR CURRENT DATA | Zero-return, persistence, historical-prevalence and ARIMA benchmark artifacts generated. Tester must review ARIMA artifact separately. |
| 5. Model experiments | research/phase-5-models | CORRECTION RUN COMPLETE — RESULTS RECONCILED | Run #39699761966 has Corrective run #39704420478 completed; 277,633 rows and zero missing target dates. Return/direction edge not established; volatility proxy needs future replication and stability diagnostics. |
| 6. Feature/horizon/regime analysis | research/phase-6-features-regimes | PARTIAL, ACCEPTED LIMITATION | Technical/global and horizon comparisons are complete within acquired data; full regime segmentation and option/FII-DII/PCR/breadth/news families remain untested. |
| 7. Statistical validation | research/phase-7-validation | REOPENED — RECOMPUTATION REQUIRED | Recheck target-date completeness and selected volatility inference against the corrected artifact before final sign-off. |
| 8. Independent tester | research/fresh-prediction-independent-tester | PENDING CORRECTIVE-RUN REVIEW | Prior artifact audit confirmed 798 missing target-date rows; corrected run #39704420478 still requires review. |
| 9. Manuscript and conclusion | research/phase-9-publication | PROVISIONAL — FINAL SIGN-OFF HELD | Corrigendum records the defect; synchronize final results after independent review. No strategy approved. |

## Corrected workflow evidence

- [Run #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) succeeded on commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`.
- Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.
- Target-construction tests and feature matrix passed. OOS predictions have non-null target dates later than origin dates; available date pairs align with 1/5/20-session horizons.
- Preliminary interpretation: no robust return/direction edge; selected volatility forecasts are not statistically accepted after multiplicity correction; volatility-expansion classification is exploratory only.
- No strategy approval is implied. No options data or transaction-cost/slippage simulation was available.


## Tester disposition

The independent tester branch reports PASS WITH SCOPE LIMITATIONS for the bounded prediction-only study. This closes the execution/target-window and prespecified statistical checks for the scoped study; it does not approve a trading strategy or substitute for unacquired options, FII/DII, PCR, breadth, news or transaction-cost data.


## Closure

## VOL-REGIME-OPT-1.0 follow-on checkpoint — 2026-10-15

| Phase | Status | Evidence / next gate |
|---|---|---|
| 1. Protocol freeze | COMPLETE ON DEVELOPER BRANCH | Frozen plan at `research/VOL_REGIME_OPTIONS_PLAN.md`; separate from closed prediction study. |
| 2. Weekly source schema | PARTIAL PASS | Dhan weekly codes 1 and 2 returned structurally valid CALL/PUT arrays (375 rows per side) in a five-day probe. Code 0 failed with `DH-905: expiryCode is required`. Candidate code 3 was added to the bounded probe matrix; its latest run must be verified. |
| 2b. Expiry mapping / contract identity | NOT VERIFIED | Must establish actual expiry dates and exact numeric strike/expiry continuity before any P&L. |
| 3. Full historical coverage / data quality | NOT STARTED | No full-window coverage gate passed. |
| 4–9. Signal, P&L, costs, risk, developer tests, independent tester, manuscript | NOT STARTED | No profitability or deployment claim permitted. |

**Developer instruction:** check the latest workflow audit, map weekly expiry codes to verified actual expiry dates and contract identity; if this cannot be established within the bounded correction, stop as BLOCKED rather than substituting monthly data. **Tester instruction:** independently verify source timestamps, contract mapping, cost signs, lot sizes, missing-data handling and all later metrics; do not sign off before artifacts exist.


The nine-phase work is closed for the bounded prediction-only scope with accepted limitations. Phases 2 and 6 are partial by design/scope, not falsely marked complete. The final conclusion is that this model/data set did not establish a robust return/direction edge. No options strategy was tested or approved.


## Separate follow-on study (does not reopen NIFTY-PRED-1.0)

A user-approved scope amendment on 2026-10-14 created OPT-BUY-1.0 as a separate, bounded test. It does not alter the closed nine-phase NIFTY-PRED-1.0 study.

| Track | Branch | Status | Evidence / final gate |
|---|---|---|---|
| Intraday option-buying validation | research/option-buying-validation | CLOSED — NO-GO FOR TESTED CANDIDATES; BROADER HYPOTHESIS INCONCLUSIVE | [Run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed with 13 tests passing before and after analysis. Independent review: [TESTER_REPORT.md](research/option-validation/TESTER_REPORT.md). |

Acquisition succeeded from cache; the quote universe has 1,062,082 raw and 1,029,545 usable rows. The frozen data gate fails: strangle eligible-date coverage 69.18% (<80%) and conflicting duplicate groups 1.409% (>1%). All four filtered candidates have negative mean net daily P&L and negative 95% intervals; 100-bps and both-half profitability checks also fail. Significant paired improvement versus always-buy is loss reduction, not profitability.

The developer accepted the independent tester's no-go. No strategy, paper-trading candidate or live deployment is approved. Do not relax the frozen gates or run further parameter loops.

## OPT-BUY-2.0 — strike-selection grid

| Phase | Status | Evidence / next gate |
|---|---|---|
| Protocol and branch setup | COMPLETE | [Frozen plan](STRIKE_SELECTION_PLAN.md); [research branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection) |
| Daily target acquisition/validation and regression tests | PASS IN RUN #4 | Daily target validated; 13 pre-analysis and 13 final regression tests passed. [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) |
| Options data quality | FAIL FOR CONFIRMATORY USE | 1,023,541 usable rows; 452 conflict groups / 31,706 duplicate groups = 1.4256%, above the 1% gate. No parse failures. |
| Coverage | FAIL FOR GRID-WIDE CONFIRMATORY USE | Only ATM/ATM coverage clears 80%; coverage ranges from 83.27% to 16.94% over 980 dates. |
| Frozen grid outcomes | COMPLETE — EXPLORATORY ONLY | At primary costs (50 bps/side, ₹10/order), all 32 model-filtered candidate × horizon means are negative and their 95% block-bootstrap upper bounds are below zero. No candidate approved. |
| Primary p-values / Holm family | CORRECTIVE RETEST | Run #4 emitted NaN for all 32 p-values despite a nonempty ledger. Fixed with explicit null-centered circular block bootstrap in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. |
| Common-date sensitivity | NOT COMPLETED | Not present in run #4 artifact. Do not claim cross-candidate superiority; the failed quality gate already precludes confirmatory ranking. |
| Independent tester sign-off | WAIVED BY USER | User explicitly waived separate tester sign-off; data-quality and inference gates remain mandatory. |

**Disposition:** NO-GO for any strike-selection candidate. Keep OPT-BUY-1.0 no-go unchanged. The one bounded corrective rerun must confirm valid p-values; do not start further parameter loops or approve paper/live deployment.


## Uploaded-PDF method comparison — 2026-10-14

| Phase | Status | Evidence / next gate |
|---|---|---|
| PDF inventory | IN PROGRESS | 13 uploaded PDFs extracted; method register on [research/pdf-method-audit](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/pdf-method-audit) in [PDF_METHOD_AUDIT.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-method-audit/research/PDF_METHOD_AUDIT.md). |
| Classical method expansion | IMPLEMENTED; RUN PENDING | Added linear regression, Lasso, SGD, KNN, Decision Tree, Gradient Boosting and AdaBoost candidates. Empirical status requires completed workflow artifacts. |
| Sequence / hybrid expansion | IMPLEMENTED; RUN PENDING | Added RNN, CNN, and four literature hybrid candidates to existing LSTM/GRU/TCN/Transformer family; bounded to short CPU fit and one-session return/direction. |
| NLP / sentiment and specialized variants | BLOCKED OR NOT IMPLEMENTED | BERT requires verified point-in-time news; fuzzy NN, DBN, wavelet, Granger screening and backward elimination are not yet validated. These will not be reported as tested. |
| Option strategy papers | OUT OF SCOPE | Three PDFs describe options strategies. The active research question remains prediction-only; these need a separate protocol. |

The push-triggered workflow for branch `research/pdf-method-audit` is [run #55](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562973443), currently queued/pending at the last check. No expanded-model result has yet been accepted. The prior NIFTY-PRED-1.0 result remains valid only for its previously tested model/data scope.


## OPT-BUY-3.0 — entry/exit research (2026-10-15)

| Phase | Status | Evidence / next gate |
|---|---|---|
| 1. Audit and freeze | COMPLETE | [Frozen protocol](OPTION_ENTRY_EXIT_PLAN.md), [questions](OPTION_ENTRY_EXIT_QUESTIONS.md), branch `research/option-entry-exit-developer`. |
| 2. Data validation | PENDING WORKFLOW | Validate private cache, schema, duplicate conflicts and date coverage. Known inherited conflict rate exceeds the frozen 1% ceiling. |
| 3. Implementation | PARTIAL | Fixed-time CALL/PUT and fixed-duration/EOD exits implemented; broader random/rule-based and barrier/trailing catalogue not complete. |
| 4. Empirical run | PENDING | Require observed Actions run and sanitized outputs. |
| 5. Independent tester | NOT STARTED | Create tester branch only after results acquisition; independently check arithmetic, costs, quote matching, no-lookahead, bootstrap and Holm correction. |
| 6. Developer correction | NOT STARTED | Fix tester-confirmed defects without relaxing gates. |
| 7. Close | NOT STARTED | Finalize README, logs, manuscript and disposition after tester report. |

**Disposition:** IN PROGRESS; NO STRATEGY APPROVED. Earlier OPT-BUY-1.0/2.0 no-go results remain unchanged.


## OPT-BUY-3.0 — Entry × exit criteria (2026-10-15)

| Phase | Status | Evidence / next action |
|---|---|---|
| Scope amendment and protocol | COMPLETE | User explicitly removed independent review. [Frozen protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/OPTION_ENTRY_EXIT_PLAN.md) amended; no tester branch/report gate. |
| Data/cache validation | BLOCKED / RECHECK REQUIRED | Latest committed screen reports BLOCKED_NO_VALID_QUOTES; confirm cache restore/acquisition and preserve source errors. |
| Full catalogue implementation | INCOMPLETE | Existing implementation only tests fixed-time CALL/PUT entries and fixed holds/EOD. Random controls, signal rules, straddles, premium barriers/trailing exits, 100-bps recalculation remain outstanding. |
| Automated validation | NOT YET VERIFIED | Existing tests are committed but this session has not observed an Actions result. Check fee math, entry/exit matching, bootstrap/null, no-trade sessions, and time truncation. |
| Bounded empirical results | NOT YET AVAILABLE | Do not claim profitability until valid quotes, complete registered cells, after-cost sensitivity and multiplicity outputs exist. |
| Manuscript and final disposition | PENDING | Produce from actual completed artifacts; close within the frozen phase budget, even if inconclusive. |

Process rule: no independent review/tester branch. The single workflow must run automated tests and checks, correct defects, document outcomes, and avoid claiming tests passed unless an actual run confirms it.


### OPT-BUY-3.0 progress update — 2026-10-15

| Work item | Status | Evidence |
|---|---|---|
| User governance change | COMPLETE | No independent review, tester branch or tester-report gate. |
| Cache retry correction | COMMITTED; workflow verification pending | Workflow now treats a stale/non-success manifest as unusable and attempts refreshed Dhan acquisition. Commit `03ee91ba312977499544733dc1177b10f04d6feb`. |
| Entry/exit screen expansion | COMMITTED; automated run pending | Added seeded random direction/time control, fixed-time CALL/PUT controls, causal spot-momentum and range-breakout entries; EOD/fixed holds/premium barrier/trailing exits; single-leg costs; 0/25/50/100 bps and ₹10/₹20 per-order sensitivity. Commit `fc487511aa7aa82d33c71dc4fdeca2870be153cb`. |
| Automated checks | EXPANDED; run pending | Added tests for single-leg two-order brokerage, slippage monotonicity, brokerage sensitivity, Holm adjustment, bootstrap reproducibility, invalid premiums and seeded signal reproducibility. Commit `6c4f94e28c2dd88744071e5c7156a2397e55f4c1`. |
| Data and final results | PENDING | Last confirmed completed run #3 still had zero valid quotes and zero candidates; see [run #3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38620992395). Runs #4/#5 are now triggered by the fixes; do not treat them as complete until their final status and artifacts are read. |


### OPT-BUY-3.0 data acquisition correction — 2026-10-15

The completed [Actions run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621480232) passed all automated tests and the entry/exit runner, but remained BLOCKED_NO_VALID_QUOTES because its manifest explicitly said BLOCKED_NO_VALID_DAILY_DATA: the runtime cache lacked `data/cache/nifty50_daily.csv`. The acquisition step had therefore never made any option requests (request count 0). Workflow now runs `scripts/acquire_data.py` when the daily target cache is absent, using Dhan first and the existing NSE/Yahoo fallbacks, then proceeds to rolling-option acquisition. [Run #7](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621701520) is queued; no empirical P&L inference yet.


## Continuation audit checkpoint — 2026-10-15

The prediction study's model execution is recorded as complete, but the continuation audit identified a documentation/evidence mismatch in independent sign-off: the main README points to run #62 and says PASS WITH SCOPE LIMITATIONS, while the accessible report on research/pdf-audit-tester-final still reviews run #60 and says FAIL FOR FINAL SCIENTIFIC SIGN-OFF. Therefore, **scientific sign-off reconciliation is OPEN** until a current independent review of run #62 is located or completed. This is a documentation and verification gate, not permission to expand the frozen model catalogue. See [continuation audit](FRESH_PREDICTION_CONTINUATION_AUDIT.md) and [error log ERR-018](ERROR_LOG.md). No strategy development is in scope.

**Tester instruction:** reconcile the report/artifact to run #62, check target-date completeness, target horizon offsets, core metric signs, multiple-testing families and manuscript numbers, and only then issue an evidence-backed disposition. Preserve the run #60 failure findings in the audit trail.


## Run #62 independent artifact review — 2026-10-15

The tester directly inspected artifact [run #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792). The earlier run #60 null-target-date defect is resolved in run #62: all 471,735 prediction rows have target dates, and exported target offsets align exactly to the recorded 1/5/20-session horizons. The tester independently reproduced MAE/RMSE for all 485 OOS metric rows (maximum absolute discrepancies 4.66e-10 and 7.45e-9) and reproduced Holm adjustments (maximum discrepancy 1.11e-16).

**Gate status: target integrity and core arithmetic PASS; final statistical sign-off WITHHELD.** Some volatility rows have pathological QLIKE values (elastic-net h=5 approximately 1.31e9) and 34 zero actual volatility labels. QLIKE edge-case handling and full HAC/block-bootstrap inference remain to be independently verified. See the updated [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md), [error log ERR-019](ERROR_LOG.md), and [continuation audit](FRESH_PREDICTION_CONTINUATION_AUDIT.md).

**Developer instruction:** fix and test the bounded QLIKE edge case, recompute scores and the relevant inference, then resubmit the artifact for tester review. Do not expand the model catalogue or claim a universal winner.


## Final tester gate — run #62 (2026-10-15)

**Phase 8 disposition: PASS WITH SCOPE LIMITATIONS. Phase 9: COMPLETE WITH SCOPE LIMITATIONS for the frozen prediction-only screen.** The updated independent tester report on `research/pdf-audit-tester-final` verifies all 471,735 target dates and exact 1/5/20-session offsets, independently recomputes MAE/RMSE for 485 OOS rows, HAC p-values and block-bootstrap intervals, Holm adjustment, and 102 volatility QLIKE rows. The earlier run #60 target-date issue is resolved in run #62. Extreme QLIKE values are explained by near-floor predictions and the documented variance-form scoring rule. Remaining limitations: weekend-date source/calendar verification, strict global close-time availability, missing options/PCR, FII/DII, breadth, point-in-time news/corporate actions and unreplicated literature methods. Final conclusion: no robust return/direction winner established. See the [current tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). No strategy conclusion is authorized by this study.


## VOL-REGIME-OPT-1.0 — weekly volatility-regime options switch (opened 2026-10-15)

| Phase | Status | Gate / evidence |
|---|---|---|
| 1. Protocol and repository audit | COMPLETE — protocol frozen | [Plan](VOL_REGIME_OPTIONS_PLAN.md); developer branch research/vol-regime-options-developer. |
| 2. Weekly data / expiry / contract source audit | IN PROGRESS | Source probe tests Dhan WEEK and MONTH response schemas in a five-day historical window; [workflow](../.github/workflows/vol-regime-options.yml). No strategy P&L may be computed until weekly schema and contract identity are verified. |
| 3. Data acquisition and cache | NOT STARTED | Requires successful weekly source gate, private cached records and a sanitized manifest. |
| 4. Regime signal reconstruction | NOT STARTED | 5-session classifier primary; 20-session secondary. Thresholds from development-only OOF probabilities. |
| 5. Contract selection and backtest | NOT STARTED | Exact same-expiry, same-numeric-strike entry/exit; ATM long straddle in high regime; near-|delta| 0.07 short strangle in low regime. |
| 6. Costs, risk and statistical analysis | NOT STARTED | Historical applicable fees, slippage scenarios, drawdown/tail-risk, block bootstrap and Holm correction. |
| 7. Developer quality gate | NOT STARTED | Automated math/data/look-ahead/contract tests. |
| 8. Independent tester | NOT STARTED | Separate branch, independent reproduction and gate decision required before manuscript closure. |
| 9. Manuscript and closure | NOT STARTED | Structured report and final GO/NO-GO; stop after bounded gates. |

The prior OPT-BUY-1.0/2.0 data and profitability failures remain relevant risk warnings, but they are not results for this different weekly-to-expiry hypothesis. No trading strategy is approved.


### Phase 2 source-probe checkpoint — 2026-10-15

The first automated probe [run #38676211935](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676211935) failed at the weekly source gate: Dhan returned HTTP 400 / DH-905 “expiryCode is required” for WEEK with expiryCode=0; MONTH with expiryCode=1 returned valid call and put series (375 rows each). This does **not** establish that weekly data are unavailable because the provider docs enumerate WEEK and codes 0–2. One bounded correction now probes WEEK codes 0, 1 and 2. No monthly data are substituted for weekly data, and no strategy P&L has been computed.

## VOL-REGIME-OPT-1.0 update — 2026-10-15

| Phase | Status | Evidence / next action |
|---|---|---|
| 1. Protocol freeze | COMPLETE | Frozen plan on developer branch; unchanged. |
| 2. Weekly schema probe | PARTIAL PASS | Persisted Dhan audit shows candidate codes 1/2 structurally valid in a five-day window; code 0 rejected. Saved audit predates code-3 probe edit. |
| 2b. Expiry mapping and contract identity | BLOCKED — TESTER CHECK PENDING | [Source-gate disposition](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md). No P&L permitted until actual expiry dates and exact-strike continuity are verified. |
| 3. Full coverage/data quality | NOT STARTED | Do not begin before Phase 2b passes. |
| 4–9. Signals, costs, statistical inference, developer validation, tester, manuscript | NOT STARTED | No profitability result or strategy approval. |

Developer instruction: do not start P&L unless expiry mapping and fixed-contract identity are verifiable. Tester instruction: make one bounded independent source/provenance check; if unresolved, recommend BLOCKED closure without weakening gates.


## VOL-REGIME-OPT-1.0 latest source-gate checkpoint — 2026-10-15

| Gate | Latest status | Evidence / decision |
|---|---|---|
| Dhan weekly schema | PASS, bounded sample only | Workflow [#10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667) log confirms WEEK codes 1/2/3 return valid CALL/PUT arrays; code 3 returned 357 CALL and 349 PUT rows. Code 0 fails with DH-905. |
| Workflow completion / HF fallback | FAILED / NOT VERIFIED | Runner shutdown canceled the Hugging Face fallback probe; audit commit and artifact steps were skipped. The Dhan results were separately persisted in the developer branch's sanitized audit. No license/coverage pass is claimed for the HF dataset. |
| Expiry-code to actual-date mapping | BLOCKED | No verified mapping across historical holiday/weekday changes. |
| Exact numeric strike + expiry continuity | BLOCKED | Rolling schema does not itself prove a fixed-contract entry-to-expiry exit series. |
| Full coverage, costs, P&L, statistics | NOT RUN | No P&L or strategy conclusion permitted. |
| Independent tester | BLOCKED | Tester report confirms the source gate is insufficient; code 3 schema success does not remove the identity blocker. |

**Disposition:** close VOL-REGIME-OPT-1.0 as BLOCKED for the frozen protocol. This is a data-feasibility result, not evidence the hypothesis is profitable or unprofitable. A future attempt needs a verifiable expiry/contract source and a new versioned protocol; do not weaken gates or substitute monthly options.

## VOL-REGIME-OPT continuation — HF dataset reuse checkpoint (2026-10-16)

| Gate | Status | Evidence / next action |
|---|---|---|
| Reuse existing HF dataset | SOURCE IDENTIFIED | `vishnuvcr/Nifty` uses `thetrademarkk/india-index-options-1m`; dataset card documents expiry-specific NIFTY parquet files and explicit expiry/strike/type fields. License CC-BY-NC-4.0 restricts this to non-commercial research with attribution. |
| Automated schema/data-quality audit | RUNNING / PENDING | New workflow [#38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042); inspect sanitized artifact/report after completion. |
| Expiry/contract identity | NOT YET VERIFIED | Check filename-expiry agreement and exact `(timestamp, expiry, strike, option_type)` keys; reconcile sample dates/contracts against official NSE evidence. |
| Coverage and duplicate gates | NOT YET VERIFIED | Required >=80% eligible-date coverage and <=1% conflicting duplicate groups remain unchanged. |
| Costs, P&L, statistical validation | NOT STARTED | Do not compute or claim profitability until source, coverage, contract identity, and license gates pass. |

**Developer instruction:** verify workflow output and official-source reconciliation before moving to backtesting. **Automated quality instruction:** reject schema drift, expiry mismatches, conflicting duplicates, missing/invalid OHLC, and any contract substitution; never treat OHLC as bid/ask fills.


## HF source audit update — 2026-10-16
- Download/reuse step: **completed** in GitHub Actions run [#38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042).
- Parquet quality audit: **in progress** at latest status check; no report/artifact yet.
- Official NSE circular review: confirms expiry schedule revisions during 2025; dated contract-file evidence is required, not a weekday-only heuristic. See [free-source audit](VOL_REGIME_OPTIONS_FREE_SOURCE_AUDIT.md).
- C1 contract identity: **BLOCKED / OPEN** until the audit report and official sample contract reconciliation are complete. C2–C7 remain not started. No P&L or strategy claim.
