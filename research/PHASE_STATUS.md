# Phase status and gate decisions

Last updated: 2026-10-14  
Research version: NIFTY-PRED-1.0

| Phase | Branch | Status | Gate / evidence | Next action |
|---|---|---|---|---|
| 1. Repository audit and design | research/phase-1-audit | IN PROGRESS | GitHub repo was empty: no files, branches, commits or datasets. Scope and criteria drafted. | Finish bootstrap, code, and audit summary. |
| 2. Literature review | research/phase-2-literature | IN PROGRESS | Reviewed NIFTY ML paper in Project library; official NSE / Dhan source pages and forecasting-test literature. | Finalize reference matrix and gaps. |
| 3. Data collection/validation/cache | research/phase-3-data | NOT STARTED | No data downloads or token access verified yet. | Run acquisition workflow and record hashes. |
| 4. Baselines | research/phase-4-baselines | BLOCKED | Requires validated target data. | Start after Phase 3 data gate. |
| 5. Model experiments | research/phase-5-models | BLOCKED | No fitted models / predictions verified. | Run frozen catalogue after data gate. |
| 6. Feature/horizon/regime analysis | research/phase-6-features-regimes | BLOCKED | Depends on source availability and model outputs. | Test verified feature families only. |
| 7. Statistical validation | research/phase-7-validation | BLOCKED | No locked holdout outputs. | Compute uncertainty, dependence-aware tests, multiplicity correction. |
| 8. Independent tester | research/phase-8-independent-review | BLOCKED | No empirical artifacts available. | Create developer/tester branches after results. |
| 9. Manuscript/publication | research/phase-9-publication | BLOCKED | No empirical result tables or deployment evidence. | Finish manuscript and verify Pages only after prior gates. |

## Gate rule

A phase is not PASS merely because files or workflows exist. Gates require execution artifacts and review evidence. A phase can complete with a negative result if the protocol ran and evidence is saved. If credentials or external permissions are missing, record BLOCKED and use free-source alternatives where possible. The final phase must record limitations and future directions.

## Phase 5 branch checkpoint — 2026-10-14

- Phases 1–4 have separate historical checkpoint branches; the working model pipeline is on research/phase-5-models.
- Daily target: 4,901 observations from 2007-01-02 through 2026-10-13; SHA-256 b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. The 20 weekend-dated observations are preserved and flagged for special-session/calendar cross-check; validation now passes with a warning, not deletion.
- Unit tests passed 8/8 on an earlier run; the corrected branch adds a specific benchmark-relative OOS-R-squared arithmetic test.
- Current canonical compute-bounded candidate: Actions run #34, commit d654d8f825ba19dc8dfc08f9f2e7b8f26779e7d3. At last check it was running validation/tests; model outputs not yet available.
- The candidate selection uses two chronological folds for all model families; sequence families have three epochs and are restricted to next-session return and direction. All other sequence target/horizon cells must be reported BLOCKED_COMPUTE_BUDGET.
- Final Phase 5 gate remains OPEN until Actions #34 completes and metrics/predictions plus independent checks are available.

## Phase 5 status — revised compute gate (2026-10-14)

The full grid remained active at the experiment step without producing final artifacts. A dated amendment to RESEARCH_PLAN.md now limits full catalogue comparisons to next-session return and direction and keeps core regression/classification models for all other target/horizon combinations. Excluded catalogue cells are emitted as BLOCKED_COMPUTE_BUDGET. Estimator counts are bounded. Phase 5 remains OPEN until a final workflow completes and all results/defect checks pass.

## Current execution checkpoint — 2026-10-14 (after run #41)

| Phase | Current evidence | Gate |
|---|---|---|
| 1. Repository audit | Empty initial repo documented; plan/scope and logs bootstrapped. | COMPLETE |
| 2. Literature | Uploaded NIFTY/deep-learning/sentiment/ANN papers appraised; options-strategy papers explicitly excluded; official NSE and free source families documented. | COMPLETE for first-pass review |
| 3. Data | Dhan daily target: 4,901 valid rows, 2007-01-02 to 2026-10-13, SHA b844c4847497ebf8aeb0a8f9fc64cf8c70fcf9ef7f6435f0ac3591b773706050. Seven external series passed quality checks; USD/INR, gold, crude failed and are not included. Feature matrix: 4,901 rows, 106 feature columns. | PASS for acquired series; auxiliary coverage partial |
| 4. Baselines | ARIMA(1,0,0) successfully forecast 1/5/20-session returns. Run-41 artifact showed no statistically significant gain over zero-return baseline (p=.492, .935, .842; CIs include zero). | COMPLETE provisionally; awaiting corrected merged output |
| 5. Models | Technical fit produced JSON status COMPLETE (278 experiment rows, 72,253 OOS predictions) including LSTM/GRU/TCN/Transformer comparisons for 1-session return/direction; global fit COMPLETE (210 experiment rows, 64,413 predictions). | OPEN: run #41 failed at merge; no per-model CSVs were uploaded. Corrected bounded rerun #45 must produce and upload them. |
| 6. Features/regimes | Global-market augmentation was actually run; official options, FII/DII, breadth and timestamped news remain absent. No regime-based result yet. | BLOCKED pending recovered metrics and further source gate |
| 7. Statistics/robustness | HAC tests, bootstrap intervals and Holm adjustment are implemented; QLIKE score correction now includes a unit test. | OPEN; run #45 must pass and results must be independently recomputed |
| 8. Independent review | Separate tester review not started; must follow complete result acquisition. | BLOCKED |
| 9. Manuscript/publication | Manuscript shell and Pages publisher exist; run #41 uploaded a status page with 0 merged OOS rows because merge failed. | BLOCKED pending accepted results |

## Correction and next gate
Run #41's model fitting completed, but it does not establish a best model because its merge step failed and the per-run CSVs were omitted from the artifact. The correction ensures empty CSVs do not crash merge, uploads all technical/global per-run CSVs, and scores QLIKE on a non-negative equivalent form. Do not mark Phase 5 PASS until Actions run #45 completes, artifacts are reviewed, and metric tests/checks pass.
