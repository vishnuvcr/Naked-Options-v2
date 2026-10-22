# Phase status — QE-NOB-2.0

Last updated: 2026-10-22  
Governance: developer-led; user explicitly said “No tester.” No tester branch/report will be created or awaited.

| Phase | Status | Exit evidence |
|---|---|---|
| 1. Protocol amendment and structural novelty specification | COMPLETE | [OPEN_STRATEGY_DISCOVERY_PLAN.md](OPEN_STRATEGY_DISCOVERY_PLAN.md); prior QE-NOB-1.0 limitations explicitly documented |
| 2. Data and feature feasibility | NOT STARTED | Feature availability matrix, source audit, coverage/missingness and timestamp provenance |
| 3. Typed strategy grammar | NOT STARTED | Typed AST, canonical fingerprints, lineage, deterministic mutations and property tests |
| 4. Simulator and baselines | NOT STARTED | Hand-calculated fixtures; next-bar execution; conservative stop/target handling; fees and slippage tests |
| 5. Bounded novelty-aware discovery | NOT STARTED | Reproducible run within 1,500 candidates / 20 generations maximum |
| 6. Frozen OOS validation | NOT STARTED | Holm correction, block bootstrap, baselines, regime stability and stress tests |
| 7. Manuscript and decision | NOT STARTED | Manuscript, artifacts, limitations, final bounded disposition; stop after this phase |

## Important distinction
The previous study tested 600 candidates within a constrained rule grammar and did not implement sufficient structural novelty or state-machine exit evolution. That run is complete and remains NO-GO. This new branch is protocol setup only; no new strategy has yet been tested or found profitable.

## Mandatory constraints
- Never reuse QE-NOB-1.0 candidate fitness or OOS outcomes as seeds/labels.
- No short-option legs, live order placement, synthetic prices or OOS tuning.
- A statistically promising result cannot pass the execution gate without credible contract identity and fill evidence.
- Keep automated developer-side tests; do not claim independent testing.
