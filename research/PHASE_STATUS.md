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

## Independent audit update — 2026-10-14

Run #45 artifact was recovered and inspected. Core return/level MSE skill and QLIKE arithmetic were independently recomputed from prediction rows (max discrepancy below 3e-9 after matching the variance floor). The tester identified a confirmed defect: forward-volatility labels near the tail were computed from partial future windows because pandas standard deviation skips missing values. The developer-review branch now requires complete horizon windows and adds a unit test. Phase 5/7 remain OPEN until CI passes, the feature matrix is rebuilt, and a new run has no invalid target-date rows.
