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
