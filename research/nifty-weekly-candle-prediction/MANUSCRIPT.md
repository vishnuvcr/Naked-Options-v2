# NIFTY Weekly Candle Prediction (NWCP-1.0): Preliminary Research Manuscript

## Abstract

This study evaluates whether information available by 10:00 IST on the first trading session after a prior NIFTY 50 weekly expiry can predict whether the index will close higher or lower on the next actual weekly expiry. A reproducible pipeline ingested a public one-minute archive, constructed expiry-anchored binary labels, generated 28 technical and hypothesis-driven features, and compared a majority baseline, logistic regression, Random Forest, Extra Trees and a bounded QuantEvolve-inspired symbolic rule search. The first end-to-end run reported 398 binary labels, with 120 in the final chronological holdout. The evolved rule achieved 0.577 holdout balanced accuracy versus 0.500 for the majority baseline, but its reported Holm-adjusted p-value was 0.116 and the research gate remained `OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`. Logistic regression achieved 0.558 balanced accuracy and a reported Holm-adjusted p-value of 0.0107, but unresolved data-source, expiry-calendar and timestamp validation limitations prevent a confirmatory claim. The study concludes that the current evidence is exploratory and insufficient to establish a reliable predictor.

## 1. Introduction

The narrow prediction target differs from generic next-day forecasting: it measures direction from the 10:00 IST anchor after one weekly expiry to the close of the following actual weekly expiry. Such multi-session outcomes may depend on momentum, realized volatility, opening-window behavior, expiry-calendar regime and market path structure. Searching a large feature/rule space creates substantial selection bias; therefore the study separates chronological training, validation and a sealed final test and applies multiplicity-aware comparisons.

## 2. Research question and hypotheses

**Primary question:** Can point-in-time information available by 10:00 IST improve out-of-sample balanced accuracy for UP/DOWN direction at the next actual weekly expiry close over a majority-class baseline?

- H0: The candidate's expected out-of-sample balanced accuracy is no better than the majority baseline.
- H1: At least one preregistered model improves balanced accuracy, with uncertainty and multiplicity controlled, while passing source, timing and data-quality gates.

The protocol excludes option P&L and trading strategy development.

## 3. Data and methods

### 3.1 Source and sample

The workflow's public manifest names `technovusin/nifty50-historical-data` as the one-minute source. The runner reported 884,552 valid bars across 2,362 sessions, from 2017-04-03 through 2026-10-23. It constructed 408 candidate intervals; 398 labels passed bar-presence and target checks, while 10 intervals were excluded. Full label counts were 224 UP and 174 DOWN. The final test block had 120 labels (67 DOWN, 53 UP), covering 2024-07-19 through 2026-10-14.

These source bars are not yet accepted as fully verified research data. Dhan lookup failed because the runner could not resolve a unique NIFTY 50 IDX_I security ID; therefore Dhan overlap was unavailable. Public-source licensing/upstream provenance and timestamp-start convention also remain unresolved. The audit reports 409 official expiries and 402 fallback calendar dates, while selected labels reportedly passed an official-only gate; that discrepancy must be independently reconciled.

### 3.2 Target construction

The intended anchor is the close of the 09:59–10:00 IST one-minute bar on the first trading session after the previous actual weekly expiry. The target is the close of the 15:29–15:30 IST bar on the next actual weekly expiry session. UP means target close exceeds anchor price; DOWN means it is lower; ties are separated from primary binary metrics. Missing or duplicate required bars and absent anchor sessions are excluded. These conventions assume source timestamps label bar starts and must be confirmed against an authoritative overlapping source.

### 3.3 Features

The 28-column set combines previous-expiry and opening-window returns/path efficiency/range, gap from previous close, ATR/RSI/EMA/MACD/Bollinger/range-position indicators, lagged returns and realized volatility, expiry weekday/regime features, and original AIA, VSRP, TCD and MHDA hypotheses. The audit reports no feature missingness above 50%. Point-in-time publication lags for external macro, FII/DII, news and options data were not included in this run and remain future extensions only after verified historical timestamps are available.

### 3.4 Models and validation

The runner compared a majority baseline, regularized logistic regression, Random Forest, Extra Trees and a bounded typed-rule evolutionary search inspired by QuantEvolve quality-diversity. The evolutionary run archived 168 candidate records over 7 generations. Training fitness included a complexity penalty and validation balanced accuracy was used for candidate selection. The final chronological quarter was held out; it was not intended for model selection.

For inference, the report used circular moving-block bootstrap with block length 4 and 1,500 valid replicates, then Holm adjustment across model comparisons. These settings are provisional: block-length/seed robustness and a formula-level review are still required. An inconsistency exists between the evolved-rule raw bootstrap p-values reported in two artifact fields (0.04397 versus 0.03864); this must be corrected before confirmatory interpretation.

## 4. Results

### 4.1 Holdout performance

| Model | Accuracy | Balanced accuracy | MCC |
|---|---:|---:|---:|
| Majority | 0.442 | 0.500 | 0.000 |
| Logistic regression | 0.508 | 0.558 | 0.207 |
| Random Forest | 0.517 | 0.542 | 0.091 |
| Extra Trees | 0.508 | 0.526 | 0.055 |
| Evolved rule | 0.600 | 0.577 | 0.168 |

The evolved rule's confusion matrix (actual DOWN/UP by predicted DOWN/UP) was [[52, 15], [33, 20]]. It identified DOWN cases more reliably than UP cases: DOWN recall 0.776, UP recall 0.377. Its validation balanced accuracy was 0.606, but that value is subject to selection optimism after a search across many candidates.

### 4.2 Statistical comparison

| Model | Difference in balanced accuracy vs majority | Bootstrap 95% interval | Holm-adjusted p |
|---|---:|---:|---:|
| Evolved rule | 0.0767 | [0.0004, 0.1658] | 0.1159 |
| Logistic regression | 0.0577 | [0.0189, 0.0971] | 0.0107 |
| Random Forest | 0.0415 | [-0.0267, 0.1066] | 0.2358 |
| Extra Trees | 0.0262 | [-0.0452, 0.0942] | 0.2518 |

The evolved rule does not pass the Holm-adjusted 0.05 threshold. Logistic regression passes the reported numeric threshold in this exploratory report, but data-source/timestamp gates and independent formula review remain open; therefore it is not accepted as a validated predictor. Model-specific score differences should not be interpreted as proof of stable economic or forecasting utility.

## 5. Discussion

The initial run shows that bounded model discovery can execute on the available cache and generate nontrivial exploratory metrics. The evolutionary rule's higher raw balanced accuracy does not survive the reported multiplicity correction. Logistic regression's reported adjusted p-value merits a predeclared replication, but not retrospective promotion, because the data source is not yet independently reconciled and the bootstrap report has an internal p-value discrepancy. The low UP recall of the evolved rule further indicates class-asymmetric behavior that overall accuracy conceals.

## 6. Strengths

- Narrow, explicit forecasting target and 10:00 IST cutoff.
- Chronological train/validation/test design rather than shuffled evaluation.
- Missing target bars excluded instead of imputed.
- Bounded evolutionary search and recorded candidate archive.
- Majority benchmark, MCC, class-specific recall and multiple-comparison adjustment reported.
- Pipeline run, regression tests and sanitized artifact are traceable.

## 7. Limitations

- Public data licensing, upstream provenance and timestamp semantics are not verified.
- Dhan source mapping failed, so no authoritative overlap check was available.
- Official/fallback expiry-calendar aggregate counts need reconciliation.
- Only 120 observations are in the final holdout; uncertainty is wide for some comparisons.
- Bootstrap inference uses one block length and seed; sensitivity analysis is incomplete.
- The raw bootstrap p-value for the evolved rule differs across artifact fields.
- FII/DII, news, options positioning, global cross-market and corporate-action features were not included due to lack of point-in-time validated data in this run.
- No independent tester report has passed the research gate.

## 8. Conclusion

The present evidence is **exploratory and insufficient** to declare a reliable NIFTY weekly direction predictor. The QuantEvolve-inspired rule achieved 0.577 balanced accuracy on 120 holdout labels, but the reported Holm-adjusted p-value was 0.116. Logistic regression achieved 0.558 balanced accuracy with a reported adjusted p-value of 0.0107; this remains a hypothesis for future replication, not an accepted finding. The pipeline's official status remains `OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`.

## 9. Future research

1. Repair Dhan security-master resolution and run source-overlap comparisons, or establish an independent authoritative public-source comparison.
2. Confirm source license and bar timestamp convention with hand-audited sessions.
3. Reconcile the expiry-calendar counts and audit selected expiry provenance row by row.
4. Fix the duplicated/inconsistent bootstrap p-value generation and add numerical tests.
5. Run block lengths and random seeds fixed in advance, with a future untouched test window.
6. Consider point-in-time options, volatility index, global market, FII/DII, news, corporate-action and sentiment features only after data timing and availability are verifiable.
7. Only after the prediction study passes its gates should a separate research protocol assess whether forecasts have any decision utility; this manuscript does not propose a trading strategy.

## Appendix A. Reproducibility

- Workflow: [NWCP-1.0 run #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486)
- Sanitized artifact: [run #18 artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486/artifacts/12566991817)
- Runner: [run_research.py](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/run_research.py)
- Tests: [test_research.py](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/test_research.py)
- Raw one-minute prices and per-expiry target rows were not included in the uploaded artifact.

## Appendix B. Decision record

Decision: **DATA-LIMITED / NO CONFIRMATORY CLAIM**. Continue only the specified remediation and replication steps. Do not promote a candidate or start strategy work from this exploratory run.
