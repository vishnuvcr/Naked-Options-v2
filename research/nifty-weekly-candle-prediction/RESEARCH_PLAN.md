# NIFTY Weekly Candle Prediction (NWCP-1.0) — Research Plan

**Protocol version:** 1.0  
**Started:** 2026-10-24  
**Status:** Phase 0 complete; source review and data feasibility beginning  
**Owner branch:** research/nifty-weekly-candle-prediction-developer  
**Scope:** Predict the direction of the NIFTY 50 spot index from a fixed 10:00 IST anchor to the next actual weekly-expiry close. No option P&L, strategy, entry/exit optimization, trade recommendations, or live execution in this study.

## 1. Frozen target definition

Let actual historical weekly NIFTY expiry dates in chronological order be E0, E1, ... Ei. Use the actual expiry calendar and contract metadata, not one weekday rule for all years.

For expiry dates E(i-1) and Ei:

1. Find Ai, the first regular NSE trading session after previous expiry E(i-1). If expiry moves because of an exchange holiday, use the next actual trading session.
2. Define P0,i as the NIFTY 50 spot index value at 10:00:00 Asia/Kolkata on Ai. Prefer an authoritative timestamped index observation. With one-minute OHLC, use the last completed bar ending at or before 10:00. Confirm whether source timestamps identify the bar start or end before constructing any labels. Never use a bar close that is only known after 10:00.
3. Define P1,i as the close of the final valid regular-session NIFTY 50 spot bar on expiry date Ei. Validate the last-bar timestamp against the official regular session close.
4. Label UP when P1,i > P0,i, DOWN when P1,i < P0,i, and TIE when equal at the source's valid precision. Ties are recorded separately and excluded from primary binary metrics; sensitivity analysis may treat them as a third class.
5. Forecast time is exactly Ai at 10:00 IST. Every predictor must have been observable by that cutoff. Lag FII/DII, news sentiment, EOD index, option OI/IV or global-market values to their true publication/availability time.

The primary outcome is direction, not price magnitude. Price change can be used for descriptive analysis only; strategy backtesting or returns-based strategy ranking is outside scope.

## 2. Research questions and hypotheses

See RESEARCH_QUESTIONS.md. Confirmatory questions are frozen before model discovery. New indicators and evolutionary search are exploratory and cannot override the confirmatory holdout.

## 3. Research phases and bounded stop rule

The project is bounded to these phases. Each phase is isolated on its own branch when entered, and each phase status is updated after a step. Progress requires the preceding exit gate. A persistent critical blocker results in DATA-LIMITED or NO-GO; do not repeat unproductive runs indefinitely.

| Phase | Work | Required exit gate |
|---|---|---|
| 0. Scope/governance | Freeze target, timestamp rules, exclusions, metrics and stop limits | This plan committed; evidence ledger and tests defined |
| 1. Literature/source audit | Review QuantEvolve, prediction literature, Pine candidates, statistics and source rights | Annotated bibliography, source catalog, feature availability table |
| 2. Data/label construction | Dhan primary source if token works; audit free/public sources; preserve provenance/cache | Data manifest, expiry/calendar audit, label audit, no leakage, missingness report |
| 3. Baselines/features | Base-rate baselines, simple classifiers, deterministic indicators and Pine formula ports | Point-in-time feature matrix, tests, chronological baseline report |
| 4. Bounded QuantEvolve discovery | Explore typed feature/indicator compositions and hypothesis-driven indicators | Candidate archive, fixed seeds, training-only fitness, hard search budget |
| 5. Validation/robustness | Walk-forward testing, class-aware metrics, blocked bootstrap, subgroup/regime diagnostics, multiplicity controls | Sealed chronological OOS report and uncertainty estimates |
| 6. Independent test/correction | After results acquisition, create a separate tester branch/report; developer fixes and resubmits | No unresolved critical math, timing, leakage, data or metric defects |
| 7. Manuscript/publication | Structured manuscript, charts, tables, appendix, reproducibility, Pages summary, bounded decision | Manuscript and supplements; final decision; stop |

Initial Phase 4 upper budget: 500 distinct candidate structures, 20 generations and up to four fixed random seeds. Stop early after three generations with no validation improvement. Reduce the budget if sample size is too small. No unbounded search or repeated OOS probing.

## 4. Primary and supporting data

### Primary source candidate
Dhan historical intraday NIFTY 50 index candles, if the repository DHAN_ACCESS_TOKEN secret works and the instrument/segment mapping is verified. Use bounded chunks and a research-specific cache namespace. Never print tokens in logs, artifacts or commits.

### Free/open cross-check candidates
- NSE official index history, exchange calendars and expiry circulars.
- Public NIFTY intraday archives in GitHub/Kaggle/Hugging Face/Zenodo only after provenance, timestamp convention, completeness, license, and Dhan-overlap checks.
- India VIX, official expiry metadata, and lagged global market, FII/DII, news/sentiment and options metrics when historic point-in-time data is actually available.

Public downloadability does not establish redistribution rights. Raw sources should be cached by source/instrument/date-range/schema. Commit compact manifests, target labels and derived tables only if their terms permit; otherwise retain raw data in Actions cache/artifacts with manifests/hashes and do not publish licensed rows to Pages.

## 5. Predictor families

Only data available by the anchor is eligible.

1. **Price/return:** lagged daily/weekly returns, realized volatility, gaps, range location, high/low counts, trend slopes.
2. **Intraday anchor:** previous expiry-to-anchor gap, 09:15–10:00 return, path efficiency, excursions, range expansion, and VWAP distance only where volume semantics are valid.
3. **TradingView Pine indicator ports:** RSI, MACD histogram, ATR-normalized trend, ADX/DMI, Supertrend state, EMA spread/slope, Bollinger/Keltner width, Donchian position, stochastic momentum and selected community scripts. Every imported/ported script requires source link, version, license, repaint/lookahead review and formula regression tests.
4. **Volatility/regime:** India VIX, rolling volatility, volatility structure when supported, trend/range regime.
5. **Derivatives:** historical option OI/IV/put-call aggregates only when coverage and point-in-time availability are audited.
6. **Cross-market/macro:** GIFT NIFTY and eligible global index/FX/commodity moves observed before 10:00 IST; FII/DII only when publication timing permits.
7. **Calendar:** actual time-to-expiry, week/holiday-shift flags, historical expiry-regime indicators and event flags known at cutoff.

### Original exploratory indicators
- **Anchor Impulse/ATR (AIA):** prior expiry close to anchor price change divided by rolling true range; tests whether post-expiry displacement is meaningful after volatility normalization.
- **Open-Window Path Efficiency (OWPE):** absolute 09:15-to-10:00 displacement divided by the sum of absolute one-minute returns; higher values mean more directional than oscillatory price action.
- **Multi-Horizon Directional Agreement (MHDA):** weighted agreement among signs of lagged 1-, 3-, 5- and 10-session returns; weights fixed or selected on training data only.
- **Volatility-Scaled Range Position (VSRP):** anchor position inside a trailing high-low channel, scaled by ATR.
- **Cross-Market Risk Pulse (CMRP):** robust median of point-in-time standardized moves across eligible global risk proxies already observable at the anchor.
- **Trend/Chop Divergence (TCD):** difference between standardized trend strength and realized path efficiency.

These are testable hypotheses, not established signals. Use ablations and retain a feature only if value persists in validation and sealed OOS.

## 6. Baselines and models

- Training-fold majority/base-rate baseline.
- Regularized logistic regression.
- Low-complexity decision tree and Random Forest/ExtraTrees.
- One gradient-boosting classifier only if sample size and dependencies justify it.
- QuantEvolve-style hypothesis-driven search over typed expressions on an allowlisted feature set, using training-only fitness and validation-only selection.
- Probability calibration only if fitted within training folds.

Given likely only a few hundred weekly samples, high-capacity deep learning is not included by default. Preprocessing, imputation, scaling, feature selection, calibration and any threshold selection must be fold-local.

## 7. Statistical design

Primary confirmatory metric: **balanced accuracy** on chronological out-of-sample observations. Also report ordinary accuracy, per-class precision/recall/F1, MCC, ROC-AUC, PR-AUC where meaningful, Brier score/log loss, calibration, confusion matrix, UP rate, baseline lift, ties and missing labels.

- Expanding-window chronological validation, with an untouched final chronological test segment (target 20% when sample size permits). Aim for at least ~50 to 100 final test labels; if unavailable, report limited power rather than silently weakening gates.
- No random shuffle split for primary claims.
- All learned preprocessing, feature filtering, calibration and candidate selection occur inside training/validation partitions.
- Moving-block bootstrap confidence intervals with primary block length of four weekly labels and sensitivity at two and eight; report exact/binomial intervals only as supplementary due to temporal dependence.
- Compare the winning model with the base-rate/majority baseline using paired block-bootstrap differences and a directional-hit test. Apply Holm correction to predeclared model/family comparisons. Exploratory candidates are not independent confirmatory tests.
- Report year/expiry-regime/VIX/trend subgroups only when sample sizes support interpretation; otherwise descriptive only.
- Track every candidate and attempted feature family in an experiment ledger to expose data snooping.

## 8. Decision criteria

A positive prediction result requires all applicable gates:
1. At least 100 sealed OOS labels where feasible; fewer means low-power/DATA-LIMITED.
2. Balanced accuracy above 0.50 and above the training-only majority baseline; 95% block-bootstrap interval for improvement does not include zero.
3. Primary comparison survives Holm correction at family-wise 5%.
4. MCC is positive; result is not explained by class imbalance or one tiny subgroup.
5. Edge persists across chronological blocks and is not exclusively tied to one expiry regime.
6. No unresolved leakage, timestamp ambiguity or critical data defect.
7. Independent tester reproduces result from a clean branch/run.

Fail a critical gate => NO-GO or DATA-LIMITED. Accuracy is not profitability. The study authorizes no trading strategy.

## 9. Data integrity and implementation rules

- Timezone-aware timestamps normalized to Asia/Kolkata for session logic.
- Deduplicate exact duplicates; quarantine conflicting duplicates and gaps instead of silently filling.
- Reconcile actual expiry dates, official holidays, special sessions and candle timestamp convention.
- Assert every feature's latest source timestamp and availability time are <= forecast cutoff.
- Log source, instrument, date range, status, response hash, row count, errors and schema.
- Bounded retry: three passes per chunk; halt after ten consecutive failures or no cache progress.
- GitHub Actions must support manual workflow_dispatch plus automatic triggers on relevant code/config changes, reuse a research-specific cache and upload sanitized audit/results even on failure.
- Secrets are environment variables only. Error log records observed defects/corrections/verification; interaction log records visible instructions and decisions, not hidden chain-of-thought.
- Existing study scores, results and candidate fitness are excluded. Prior data can be reused only after separate source/license/timestamp validation.

## 10. Required final deliverables

Protocol, annotated literature and source catalog; data dictionary/manifests, expiry and label audits; reproducible Python code/tests/dependencies; Pine source catalogue with licenses/repainting assessments; full candidate archive/seeds/budget; baselines/models/ablation/confusion/calibration/uncertainty figures; independent tester and remediation record; manuscript with Abstract, Introduction, Questions, Literature, Data/Methods, Results, Discussion, Strengths, Limitations, Conclusion, Future Research, references and appendices; GitHub Pages summary with phase states and links.

## 11. Stop boundary

Stop after Phase 7 or a verified critical blocker (legally usable target data unavailable after bounded free-source checks, target timestamp ambiguity cannot be resolved, or inadequate OOS sample). Final state is PASS FOR PREDICTION RESEARCH ONLY, NO-GO, or DATA-LIMITED. No strategy development in NWCP-1.0.
