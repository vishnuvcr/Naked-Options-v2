# Phase status — QE-NOB-2.0

Last updated: 2026-10-22  
Governance: developer-led; user explicitly said “No tester.” No tester branch/report will be created or awaited.

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 1. Protocol amendment and structural novelty specification | COMPLETE | [Open discovery plan](OPEN_STRATEGY_DISCOVERY_PLAN.md) freezes budget, grammar, gates and stop condition |
| 2. Data and feature feasibility | PARTIAL — STATIC AUDIT COMPLETE | [Feature feasibility audit](FEATURE_FEASIBILITY_V2.md) maps prior-pipeline fields and gaps. Runtime field-level cache audit and refreshed free-source catalogue remain outstanding; no unsupported feature may enter candidate evaluation |
| 3. Typed strategy grammar | IMPLEMENTED — AUTOMATED TEST PENDING | [strategy_grammar_v2.py](strategy_grammar_v2.py) defines typed candidates, structural signatures, novelty distance, mutation and crossover. [Test file](test_strategy_grammar_v2.py) and [manual/automatic GitHub Actions workflow](../../.github/workflows/qe-nob-v2-grammar-tests.yml) committed; no successful workflow result has yet been verified |
| 4. Simulator and baselines | NOT STARTED | Hand-calculated fixtures; next-bar execution; conservative stop/target handling; fees/slippage tests |
| 5. Bounded novelty-aware discovery | NOT STARTED | Reproducible run, max 1,500 unique structural candidates / 20 generations |
| 6. Frozen OOS validation | NOT STARTED | Holm correction, block bootstrap, baseline comparison, regime stability and stress tests |
| 7. Manuscript and bounded decision | NOT STARTED | Manuscript, tables/figures, limitations and final decision; stop after this phase |

## Work completed in this checkpoint
- Created branch `research/quant-evolve-nob-v2-discovery-developer` from QE-NOB-1.0 developer branch.
- Recorded why the previous candidate grammar did not adequately search structural novelty.
- Added typed, serializable candidate representation with entry logic, instrument, expiry/moneyness, holding horizon and up to three exit rules.
- Added canonical structural signatures that ignore hypothesis wording and parent lineage, plus Jaccard novelty distance.
- Added bounded mutation/crossover with parent lineage and feature allowlisting.
- Added regression tests for identity, exit novelty, unsupported features, invalid stop values, deterministic mutation and crossover.
- Added automatic push and manual workflow for grammar tests.

## Caveats / no overclaiming
This is not yet an integrated backtester. The grammar's feature catalogue contains conditional features; Phase 2 runtime coverage and point-in-time availability must gate them before discovery. A passing grammar test proves only representation invariants, not trading profitability or execution realism. No new strategy has been backtested or shown profitable. The prior QE-NOB-1.0 NO-GO result remains unchanged.

## Mandatory constraints
- Never reuse QE-NOB-1.0 candidate fitness or OOS outcomes as seeds/labels.
- No short-option legs, live order placement, synthetic prices or OOS tuning.
- A statistical pass cannot bypass the execution gate for credible contract identity and fill evidence.
- Keep automated developer-side tests; do not claim independent testing.
