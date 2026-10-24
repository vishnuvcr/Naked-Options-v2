# Phase Status — NWCP-1.0

Last updated: 2026-10-24 (Asia/Kolkata)  
Active branch: [research/nifty-weekly-candle-prediction-developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/nifty-weekly-candle-prediction-developer)  
Current decision: **IN PROGRESS — NO EMPIRICAL PREDICTION CLAIM**

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 0. Scope/governance | COMPLETE — protocol frozen | [Research plan](RESEARCH_PLAN.md), [questions](RESEARCH_QUESTIONS.md), [data protocol](DATA_PROTOCOL.md), [error log](ERROR_LOG.md), [interaction log](INTERACTION_LOG.md). Old prediction and option-buying results excluded. |
| 1. Literature/source audit | IN PROGRESS | QuantEvolve and statistical references identified; NSE current expiry rule and TradingView repainting guidance identified. Need annotated Pine candidates and source/license table. |
| 2. Data/label construction | NOT STARTED — gated by Phase 1 source mapping | Validate Dhan token/instrument mapping, actual expiry calendar, timestamp semantics, source overlap and missingness before model training. |
| 3. Baselines/features | BLOCKED | Requires audited target labels and point-in-time features. |
| 4. Bounded QuantEvolve discovery | BLOCKED | Requires Phase 2 labels and Phase 3 feature/candidate regression tests. Max 500 candidates, 20 generations, four fixed seeds; reduce for small samples. |
| 5. Frozen OOS validation | BLOCKED | Requires chronological folds and sealed holdout. |
| 6. Independent test/correction | NOT YET ELIGIBLE | Separate tester branch/report only after result acquisition; validate math, timing, leakage, data, statistics and reproducibility. |
| 7. Manuscript/final decision | BLOCKED | Full manuscript, figures, tables, appendices, reproducibility assets and PASS / NO-GO / DATA-LIMITED determination. |

## Governance notes
- Each phase is intended to be isolated on a separate branch as the phase is entered; promotion requires the previous gate.
- Actions workflows need manual workflow_dispatch and automatic triggers.
- No legacy score, results table or candidate fitness is imported as evidence.
- If a source or feature cannot be verified, it remains conditional or is excluded.
- The repository log contains visible instructions and research decisions, not private hidden reasoning.
