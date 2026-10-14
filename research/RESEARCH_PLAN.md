# Research plan — NIFTY-PRED-1.0

**Scope freeze date:** 2026-10-14  
**Status:** Version 1.0; plan is locked for the nine predefined phases.  
**Decision rule:** No strategy construction, trading recommendation, or post-result expansion of the experiment universe.

## Aim

Identify whether observable information available before a forecast origin can improve forecasts of NIFTY 50 levels, returns, direction, and future volatility relative to strong simple benchmarks, with honest uncertainty estimates and evidence that generalizes to an untouched chronological holdout.

## Core principles

1. Prediction targets are not interchangeable. Price-level fit, return forecast skill, directional classification, volatility forecasts, and probability calibration are reported separately.
2. Training, model selection, and final testing are chronological. All transformations are fitted on training data only.
3. Data are point-in-time eligible only when their publication timestamp is no later than the forecast cut-off. Global market series are lagged conservatively; known release times are recorded for macro/news inputs.
4. No missing values, prices, dates, options, sentiment, or labels are fabricated. Every exclusion, fallback, source failure, and imputation is documented. Any imputation used in a model is fitted on training folds only and flagged.
5. A large price-level R-squared is not evidence of return predictability. Level forecasts must be compared with persistence; return forecasts must be compared with zero, historical mean, and simple autoregressive benchmarks.
6. The final out-of-sample period remains frozen after model selection. It cannot be used to tune parameters or choose among candidates.
7. Negative or inconclusive results count as completed research if protocols pass and the result is recorded.
8. The scope is finite: complete the nine phases once, permit only defect-driven reruns, and explicitly park unresolved work in Future Research.

## Research unit and forecast origins

- Main frequency: end-of-session daily forecasts after the NSE session close. A forecast at close t may use information publicly available by that cut-off and predicts t+1, t+5, or t+20 trading-session outcomes.
- Intraday: evaluate only if Dhan data access and historical minute coverage are verified. Do not treat an intraday workflow as completed unless the forecast timestamp, bar-availability rule and sample coverage are validated.
- Primary sample: maximum reliable common span across the chosen target and each predictor after source-availability checks. A full-sample estimate will be supplemented with subperiod/regime diagnostics.
- Core horizons: 1, 5 and 20 NSE sessions. Optional horizons can only be reported if prespecified here or marked exploratory.
- Main targets: future log return, direction, future realized volatility / volatility expansion, and closing index level. Forecasting open from prior close is a separate target when the data and time cut-offs support it.

## Fixed phases, gates and completion criteria

### Phase 1 — Repository audit and research design
Tasks: inspect repository, branch/commit history, data, source code, workflows, logs, project-library documents and previous work that is accessible; record unavailable sources; freeze this plan, hypotheses, experiment catalogue and version identifier.
Acceptance: repository and accessible-project audit recorded; no historical data or code deleted; scope / target / cut-off / split / metrics / experiment catalogue frozen; initial errors logged.
Completion: audited paths or explicit empty-repository finding and a reproducible research skeleton are committed.

### Phase 2 — Literature review and gap identification
Tasks: review India/NIFTY forecasting papers; broader financial time-series forecasting and deep learning; point-in-time information; validation, forecasting metrics, nested-model tests, calibration and multiple testing. Include uploaded project literature where accessible and label claims that come only from the source papers.
Acceptance: each relevant source has bibliographic details, URL/DOI, method, sample, evaluation design, findings, limits and relevance. Differentiate peer-reviewed papers, preprints, vendor documentation and unpublished project artifacts.
Completion: review, research-gap table and reference list committed.

### Phase 3 — Data acquisition, validation and cache
Tasks: attempt Dhan API using DHAN_ACCESS_TOKEN, official NSE data, free public data and external market context; enumerate obtainable India VIX, constituents, options/F&O, FII/DII and macro/news series; preserve source provenance and publication-time fields; build composite tables only on compatible timestamps and definitions.
Acceptance: schema tests pass, time zone/frequency is explicit, duplicate and missingness reports exist, hashes and retrieval times are recorded, token never logged, license notes recorded. External data are not merged merely because dates look similar.
Completion: at least one reproducible NIFTY index series passes validation, or the phase is marked BLOCKED with reproducible evidence and a complete source-failure report. No fabricated prices.

### Phase 4 — Baselines and benchmark establishment
Tasks: train naive level persistence; zero/mean return; historical-average direction; random-walk / drift; autoregressive / ARIMA and regularized linear benchmarks. Define target transforms and metric functions.
Acceptance: benchmark predictions are generated with strictly lagged information; metric unit tests cover zero-return forecasts, horizon overlap and sign conventions; benchmark outputs and sample counts exist.
Completion: baseline report exists and pipeline tests pass, even if baseline data are insufficient.

### Phase 5 — Systematic model experiments
Tasks: run prespecified linear/regularized, logistic, SVM, random forest, gradient boosting / XGBoost / LightGBM / CatBoost where installable, MLP and compact LSTM/GRU/TCN/Transformer variants when the data/compute gates permit; test ensembles only from validation predictions. Log model exclusions and every failed run.
Acceptance: all catalogue rows are marked PASS, FAIL, BLOCKED or NOT RUN with configuration, seed, data version, status and failure reason. No model is omitted silently.
Completion: experiment matrix and reproducible predictions exist, or each blocked family has a documented reason. Do not claim all algorithms worldwide were tested.

### Phase 6 — Feature, horizon and regime analysis
Tasks: use ablations for price/return/volatility, volume, India VIX, global indices, commodities/currency/rates, breadth, options/F&O, FII/DII and news/sentiment when valid data exist. Compare horizons and predefined regimes (e.g., volatility quantiles computed using training-only thresholds, not hindsight labels). Assess feature importance only on validation/training or by permutation on the final sample without retuning; mark that test importance is diagnostic.
Acceptance: every feature family has an availability flag, ablation comparison and sample coverage; absent data are reported absent and not given proxy labels.
Completion: feature/horizon/regime report exists; any sparse regimes are labelled underpowered.

### Phase 7 — Statistical validation and robustness
Tasks: locked final chronological holdout; expanding-window walk-forward predictions; confidence intervals by moving-block bootstrap; benchmark-relative loss tests (DM with HAC for non-nested comparisons; Clark–West where appropriate for nested forecasts); exact/binomial or block bootstrap checks for classification as appropriate; calibration and Brier/log-loss metrics; Holm correction for the predefined model-comparison family; sensitivity to training window, subperiod and regime.
Acceptance: confidence intervals, effect sizes, sample sizes and corrected p-values are reported; overlapping horizons use inference accounting for dependence; benchmark/selection data are not reused as final evidence.
Completion: gate report makes a calibrated PASS / INCONCLUSIVE / FAIL decision for predictive evidence. A strong result requires practical effect size, corrected statistical evidence and stability; otherwise report no robust skill.

### Phase 8 — Independent tester review and defect correction
Tasks: create separate developer and independent-tester branches after result acquisition; test code and formulas independently; inspect leakage, time alignment, labels, metrics, uncertainty, test reuse, provenance, multiple testing, charts and claims. Developer fixes each confirmed defect, reruns targeted checks and submits a new revision; tester reruns and records disposition.
Acceptance: all critical/high defects fixed or explicitly gate-blocking; review evidence and commit SHAs recorded; developer claims are no stronger than the tested evidence.
Completion: independent report gives PASS, CONDITIONAL PASS or REJECT. A local automated review is not represented as an independent human audit.

### Phase 9 — Manuscript and publication
Tasks: write the full manuscript; prepare plots/tables/appendices/supplementary files; update README, logs, phase status, sources and reproducibility details; add a static publication page and Actions workflow; retain results, seed, configs, hashes and source manifest.
Acceptance: manuscript includes abstract, intro, literature, questions, aims, methods, metrics, results, inferences, discussion, strengths, limitations, conclusion, future work and appendices. All numbers link to generated result artifacts.
Completion: reproducibility tests pass; publication workflow is configured and actual deployment status is verified or explicitly blocked by repository settings.

## Model selection and evaluation

- Main development region: earliest 80% of eligible observations, chronological.
- Within development: expanding-window time-series folds for model and hyperparameter selection; preprocessing and thresholds are fit only on the fold's training segment.
- Locked holdout: latest 20%, with boundaries and row hashes saved before fitting candidates. No selection/tuning on this segment.
- If the eligible sample is too small, use a 70/15/15 design only after recording the reason before any test result is inspected.
- Regression: MAE, RMSE, out-of-sample R-squared relative to target mean, benchmark-relative MSE / OOS R-squared and interval/quantile scores when supported.
- Classification: accuracy against both zero/majority baselines, balanced accuracy, precision, recall, F1, ROC-AUC, Brier score, log loss, reliability/calibration.
- Volatility: MAE/RMSE on log realized variance or volatility, QLIKE when forecast is a positive variance, Brier/AUC for predefined volatility expansion.
- Uncertainty: moving-block bootstrap with declared block length and seed; robust/HAC loss-differential inference; multiple-testing correction across the catalogue family.
- Report errors in original units and normalized/relative metrics, plus sample counts and benchmark values.

## Frozen experiment families

- E0: data schema / provenance / time-alignment controls.
- E1: level baselines: persistence, drift, linear trend, ridge.
- E2: return baselines: zero, historical mean, AR(1)/ARIMA, ridge/elastic net.
- E3: direction baselines: class-prior / majority and logistic regression.
- E4: supervised trees: Random Forest, Extra Trees, HistGradientBoosting, XGBoost, LightGBM, CatBoost (availability conditional).
- E5: SVM/SVR and MLP.
- E6: sequence models: LSTM, GRU, TCN, Transformer (compute and sample-size gate).
- E7: naive ensembles and validation-weighted ensemble (weights from validation only).
- E8: feature-family ablations and permutation importance.
- E9: horizon and fixed-regime comparisons.
- E10: statistical inference, confidence intervals, multiple testing, calibration and robustness.
- E11: final artifact consistency and independent defect review.

A full run is not permitted to exceed these catalogue families except for pre-registered defect repairs.

## Reproducibility and change control

Default seed: 20261014, recorded per model. Data raw responses or files are cached with source URL/API endpoint, retrieval UTC, source as-of timestamp if available, date span, sha256 and license/use conditions. Do not commit secrets, private chain-of-thought, copyrighted full papers or unlicensed vendor raw data. The auditable log records actions, decisions, commands/workflow run IDs where actually observed, results and errors; it never stores hidden reasoning.

The plan changes only for a genuine scope, source-access or methodological defect. Any change requires a dated plan amendment with old text, new text, reason, impact on comparability and approval/gate record. The accepted plan otherwise stays unchanged.


## Dated execution amendment — 2026-10-14 (resource-bounded screening)

**Plan version:** original NIFTY-PRED-1.0 scope retained; this dated amendment operationalizes the existing Phase 5 compute gate. It does not change targets, horizons, the chronological split or the untouched final 20% holdout.

- **Prior execution design:** fit the fixed tabular, optional boosting and sequence catalogue across every target/horizon combination with 2 walk-forward folds, then evaluate valid candidates on the holdout.
- **Amended execution design:** evaluate the full installed candidate catalogue for next-session (1-session) log return and direction, including LSTM/GRU/TCN/Transformer at three epochs. For every other target/horizon pair, the screening set is Ridge, ElasticNet, Random Forest and HistGradientBoosting for regression, or Logistic Regression, Random Forest and HistGradientBoosting for classification. Use two expanding chronological folds for selection; cap forest estimators at 60, histogram boosting at 80 iterations, optional XGBoost/LightGBM/CatBoost at 80 iterations and MLP at 80 iterations.
- **Reason:** the earlier full-grid Actions attempts remained in the model-selection step without producing reproducible result artifacts. This is a bounded compute control to finish the predefined study, not a result-driven choice of model.
- **Impact / comparability:** the full algorithm-family comparison is confirmatory only for 1-session return/direction; all other target/horizon outputs are a core-model screen and cannot establish that an omitted algorithm would underperform there. All skipped family cells must be emitted with status BLOCKED_COMPUTE_BUDGET; family-level claims must respect this distinction. The original research questions, primary targets, horizons and final holdout remain unchanged.
- **Approval/gate record:** applied under the user's explicit instruction to execute autonomously and correct recoverable workflow errors without routine confirmation. Phase 5 is not passed by this amendment. It remains open until a completed run, tests, artifacts and metric audits pass. No model winner or predictive significance is implied.
