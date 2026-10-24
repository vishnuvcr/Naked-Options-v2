# NWCP-1.0 — First End-to-End Results and Evidence Register

**Run:** [GitHub Actions #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486)  
**Artifact:** [Sanitized run report](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486/artifacts/12566991817)  
**Status:** EXPLORATORY ONLY — OOS GATE NOT PASSED / INSUFFICIENT

## 1. Scope and outcome

The preregistered target is whether NIFTY 50 spot at the next actual weekly expiry close is above (UP) or below (DOWN) its value at 10:00 IST on the first trading session after the preceding actual weekly expiry. Ties are separated from the binary labels. This is prediction-only research; no options strategy or P&L optimization is included.

The workflow completed and ran 14 tests successfully. The sanitized report states 884,552 canonical one-minute bars across 2,362 sessions, 398 valid binary labels, 10 excluded intervals, and 28 feature columns. The final chronological holdout contains 120 labels, spanning 2024-07-19 to 2026-10-14. The pipeline's own decision remains `OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`.

## 2. Data and label audit

| Audit item | Observed result | Interpretation |
|---|---:|---|
| Canonical one-minute bars | 884,552 | Parsed public-source history; not yet independently licensed/provenance verified |
| Sessions | 2,362 | 2017-04-03 through 2026-10-23 in the aggregate bar set |
| Candidate intervals | 408 | From expiry/anchor construction |
| Valid binary labels | 398 | Used in exploratory baseline run |
| Excluded intervals | 10 | Missing/duplicate anchor or expiry bar, or no anchor session |
| UP / DOWN labels | 224 / 174 | Class counts in the full labelled set; ties separately audited |
| Sealed test labels | 120 | 67 DOWN and 53 UP |
| Dhan overlap | NOT AVAILABLE | Dhan security master lookup failed; no source overlap validation |
| Expiry metadata | 409 official dates reported; 402 fallback calendar dates also reported | Requires reconciliation: selected labels passed the code's official-only gate, but the aggregate audit reports a substantial fallback calendar set. Do not treat this as full calendar validation. |

Primary public source recorded in the run manifest: `technovusin/nifty50-historical-data`. The runner's secondary/Dhan source comparison did not produce a usable overlap audit. Source licensing, upstream data origin, bar-start timestamp semantics and point-in-time parity remain open gates.

## 3. Frozen test-set baseline comparison

The following values are copied from the run's sanitized `data_quality_audit.json`. Balanced accuracy is the primary metric; accuracy alone is not sufficient when classes are imbalanced. The majority baseline's balanced accuracy is 0.500.

| Model (selected without test data) | Accuracy | Balanced accuracy | MCC | Test interpretation |
|---|---:|---:|---:|---|
| Majority baseline | 0.442 | 0.500 | 0.000 | Reference |
| Logistic regression | 0.508 | 0.558 | 0.207 | Some metric improvement; calibration/decision behavior needs scrutiny |
| Random forest | 0.517 | 0.542 | 0.091 | Small improvement |
| Extra Trees | 0.508 | 0.526 | 0.055 | Small improvement |
| Evolved symbolic rule | 0.600 | 0.577 | 0.168 | Highest balanced accuracy among listed models; not accepted as a predictor |

The evolved rule's test confusion matrix (rows actual DOWN/UP; columns predicted DOWN/UP) is `[[52, 15], [33, 20]]`. Its DOWN recall is 0.776 and UP recall is 0.377: it is substantially weaker at identifying UP cases. The rule has hard class outputs, so probability-based scores are not applicable.

## 4. Statistical comparison and multiplicity

The report used a circular moving-block bootstrap with block length 4 and 1,500 valid replicates. These estimates are approximate and depend on the chosen block length and implementation.

| Model | Observed balanced-accuracy difference vs majority | Bootstrap 95% CI | Raw one-sided p | Holm-adjusted p |
|---|---:|---:|---:|---:|
| Evolved rule | 0.0767 | [0.0004, 0.1658] | 0.0386 (model-comparison table) | 0.1159 |
| Logistic regression | 0.0577 | [0.0189, 0.0971] | 0.0027 (model-comparison table) | 0.0107 |
| Random forest | 0.0415 | [-0.0267, 0.1066] | 0.1179 | 0.2358 |
| Extra Trees | 0.0262 | [-0.0452, 0.0942] | 0.2358 | 0.2518 |

The evolved rule does **not** pass Holm-adjusted significance at 0.05. The logistic regression comparison is nominally significant after the reported Holm correction, but this is still not a validated research conclusion: source overlap and provenance gates are open, the holdout is limited to 120 observations, there are unverified timestamp assumptions, and the testing report has not yet been independently reviewed. The test-set winner is not to be reselected based on these figures.

**Statistical consistency note:** the artifact's evolved-rule `selected_model_bootstrap_vs_majority` reports raw bootstrap p=0.04397, whereas the multiple-comparison table reports 0.03864 for that model. The discrepancy must be reconciled in code/report generation before any confirmatory inference. Until then, use the Holm-adjusted value from the multiple-comparison table only as a provisional reported quantity, not as final evidence.

## 5. Feature and discovery summary

The audit reports 28 features, including lagged returns and realized volatility, ATR/RSI/EMA/MACD/Bollinger/range-position indicators, opening-window structure, expiry regime features, and hypothesis-driven AIA/VSRP/TCD/MHDA features. The bounded evolutionary search evaluated 168 archived candidate records over 7 generations (maximum configured budget: 500 candidates / 20 generations). The rule selected using validation balanced accuracy reached 0.606 validation balanced accuracy, but this is a selection metric and is expected to be optimistic after searching many candidates.

## 6. Decision

**NO CONFIRMATORY CLAIM.** Run #18 establishes that the end-to-end runner executes and produces a bounded exploratory report. It does not establish a reliable NIFTY weekly direction predictor.

Blocking items before any promotion:
1. Resolve the Dhan security-master mapping and obtain an independently sourced overlap audit, or formally declare Dhan unavailable and complete a valid second-public-source audit.
2. Verify public data licensing, upstream provenance, timestamp semantics and sample bars against an authoritative source.
3. Reconcile official vs fallback expiry-calendar counts and verify every labelled interval's expiry provenance.
4. Resolve the bootstrap p-value inconsistency and rerun formula-level tests.
5. Add robustness checks for block lengths/seeds and report the predeclared class-count, sample-size, uncertainty and multiplicity gates explicitly.
6. Keep the final test sealed; any corrective/model-selection changes require a new future holdout, not repeated tuning against this test.

No trading strategy, option execution, or profitability claim follows from these results.
