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
