# Phase Status — NWCP-1.0

Last updated: 2026-10-24 (Asia/Kolkata)  
Active branch: [research/nifty-weekly-candle-prediction-developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/nifty-weekly-candle-prediction-developer)  
Current decision: **IN PROGRESS — NO EMPIRICAL PREDICTION CLAIM**

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 0. Scope/governance | COMPLETE — protocol frozen | [Research plan](RESEARCH_PLAN.md), [questions](RESEARCH_QUESTIONS.md), [data protocol](DATA_PROTOCOL.md), [error log](ERROR_LOG.md), [interaction log](INTERACTION_LOG.md). Old prediction and option-buying results excluded. |
| 1. Literature/source audit | IN PROGRESS — PARTIAL EVIDENCE ADDED | Annotated QuantEvolve/statistical references, a TradingView Pine candidate catalogue, NSE current expiry source and official repainting guidance are recorded. Still needs dated systematic-search ledger, broader India-specific peer-reviewed coverage, and rights/provenance verification. |
| 2. Data/label construction | IMPLEMENTED IN RUNNER; NOT YET VERIFIED | Python acquisition, source-overlap audit, expiry/label construction, sanitized reports and unit-test scaffolding exist on the developer branch. Actual Actions execution, public source schema/license, Dhan security mapping, official expiry completeness and timestamp parity still must pass before accepting labels. |
| 3. Baselines/features | BLOCKED FOR EVIDENCE | Exploratory baseline and feature code is present but cannot be treated as validated until Phase 2 labels and cutoff tests pass. |
| 4. Bounded QuantEvolve discovery | CODE PRESENT; EMPIRICAL RUN BLOCKED | Bounded typed-rule evolutionary search and archive are implemented in the runner. Run only after source, labels and regression gates pass; current code has not been independently verified on real data. |
| 5. Frozen OOS validation | BLOCKED | Requires chronological folds and sealed holdout. |
| 6. Independent test/correction | NOT YET ELIGIBLE | Separate tester branch/report only after result acquisition; validate math, timing, leakage, data, statistics and reproducibility. |
| 7. Manuscript/final decision | BLOCKED | Full manuscript, figures, tables, appendices, reproducibility assets and PASS / NO-GO / DATA-LIMITED determination. |

## Governance notes
- Each phase is intended to be isolated on a separate branch as the phase is entered; promotion requires the previous gate.
- Actions workflows need manual workflow_dispatch and automatic triggers.
- No legacy score, results table or candidate fitness is imported as evidence.
- If a source or feature cannot be verified, it remains conditional or is excluded.
- The repository log contains visible instructions and research decisions, not private hidden reasoning.


## Testing update — 2026-10-24

- Added NWCP-E008 (critical): weekday-derived expiry fallback could create accepted labels. Fixed on developer branch by requiring complete official NSE provenance before target construction.
- Added NWCP-E009 (high): regression coverage did not test missing anchor/expiry bars and provenance gate. Added tests for these conditions and Holm-adjustment invariants.
- Run [#14](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40104096953) completed with **failure** after the test step passed: `13 passed in 1.38s`. The full data/baseline stage failed in `_evolve_rule` with `KeyError: 'f1'` because archive records were passed as candidates in the next generation. Fixed by unwrapping elite candidate dictionaries and correcting parent/crossover references; added a multi-generation regression test. New workflow run is pending. Phase 2 remains blocked until the full data/baseline stage and source validation complete.
- No prediction accuracy or winning rule is claimed. The current research remains blocked until the test suite runs and source/calendar validation succeeds.


## Corrective end-to-end run #18 — 2026-10-24

- [Workflow run #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486) completed successfully at the CI/job level.
- Regression suite: **14 passed in 2.12 seconds**.
- Runner reported **398 valid labels, 398 features**, with final status `OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`.
- This confirms the prior evolutionary-search crash is corrected and the bounded pipeline executes. It does **not** pass the prediction gate. Phase 2 is operational but remains scientifically conditional on public-source license/provenance, timestamp convention, official expiry-calendar completeness and source-overlap audit. Phases 3–7 remain blocked for accepted prediction claims pending detailed OOS metric/sample-size report review.


## Run #18 evidence audit — 2026-10-24

- Downloaded and inspected the sanitized artifact. Dataset: 884,552 one-minute bars / 2,362 sessions; 398 binary labels (224 UP, 174 DOWN), 10 exclusions, 28 features; final test has 120 labels (67 DOWN, 53 UP).
- Test metrics: majority balanced accuracy 0.500; logistic 0.558; Random Forest 0.542; Extra Trees 0.526; evolved rule 0.577. The evolved rule's Holm-adjusted p is 0.1159, so it does not pass 0.05. Logistic's reported Holm-adjusted p is 0.0107, but it is not accepted as a finding while source/timestamp gates are open.
- Critical unresolved audit findings: Dhan security master mapping failed and source overlap is unavailable; public source license/upstream provenance and timestamp semantics remain unverified; expiry audit reports 409 official and 402 fallback calendar dates and needs reconciliation; evolved-rule bootstrap raw p-value differs across artifact fields (0.04397 vs 0.03864).
- Added [RESULTS.md](RESULTS.md) and [MANUSCRIPT.md](MANUSCRIPT.md). Decision remains **DATA-LIMITED / NO CONFIRMATORY CLAIM**. Do not tune further on the sealed test.
