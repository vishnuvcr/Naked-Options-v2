# Phase status — QE-NOB-2.0

Last updated: 2026-10-22  
Governance: developer-led; user explicitly said “No tester.” No tester branch/report will be created or awaited.

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 1. Protocol amendment and structural novelty specification | COMPLETE | [Open discovery plan](OPEN_STRATEGY_DISCOVERY_PLAN.md) freezes budget, grammar, gates and stop condition |
| 2. Data and feature feasibility | PARTIAL — AUDIT TOOL ADDED, NOT RUN ON RESEARCH CACHE | [Feature feasibility audit](FEATURE_FEASIBILITY_V2.md), [audit utility](feature_audit_v2.py), and [audit tests](test_feature_audit_v2.py) committed. Runtime cache audit and refreshed free-source catalogue remain outstanding. |
| 3. Typed strategy grammar | IMPLEMENTED — CI RESULT NOT VERIFIED | [strategy_grammar_v2.py](strategy_grammar_v2.py) defines typed candidates, signatures, novelty distance, mutation and crossover. Tests load the hyphenated directory by file path. Dedicated [grammar test workflow](../../.github/workflows/qe-nob-v2-grammar-tests.yml) added. No successful CI result has been observed. |
| 4. Simulator and baselines | NOT STARTED | Hand-calculated fixtures; next-bar execution; conservative stop/target handling; fees/slippage tests |
| 5. Bounded novelty-aware discovery | NOT STARTED | Reproducible run, max 1,500 unique structural candidates / 20 generations |
| 6. Frozen OOS validation | NOT STARTED | Holm correction, block bootstrap, baseline comparison, regime stability and stress tests |
| 7. Manuscript and bounded decision | NOT STARTED | Manuscript, tables/figures, limitations and final decision; stop after this phase |

## Checkpoint completed
- Created new developer branch and froze a bounded open structural discovery protocol.
- Added typed strategy grammar with candidate validation, canonical signatures, novelty distance, deterministic mutation, crossover and lineage.
- Added bounded candidate generator with deterministic seed, feature allowlist, syntactic uniqueness, novelty-based environmental selection, maximum 1,500 candidate budget and 20-generation ceiling. It generates candidates only and computes no P&L.
- Added feature/cache audit utility that reports file hashes, schema fields, timestamp counts, array lengths and null counts without exposing credentials or claiming contract identity.
- Added unit tests for grammar and feature audit, plus two dedicated automatic/manual GitHub Actions workflows.
- Identified and corrected test-import defects caused by the hyphenated research directory and dynamic module loading. This was a code review correction, not evidence of passing tests.
- Added error log entries for unsupported features, pending CI and missing simulator integration.

## Important status
GitHub Actions workflows are configured to run on relevant pushes and manual dispatch, but their results have not been verified in this interaction. No test pass is claimed. The feature audit has not yet been run against the full research cache, the grammar is not integrated with the backtester, and no new strategy has been backtested or shown profitable. The prior QE-NOB-1.0 NO-GO result remains unchanged.

## Mandatory constraints
- Never reuse QE-NOB-1.0 candidate fitness or OOS outcomes as seeds/labels.
- No short-option legs, live order placement, synthetic prices or OOS tuning.
- A statistical pass cannot bypass the execution gate for credible contract identity and fill evidence.
- Keep automated developer-side tests; do not claim independent testing.
