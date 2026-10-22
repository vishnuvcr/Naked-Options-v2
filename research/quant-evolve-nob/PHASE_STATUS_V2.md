# Phase status — QE-NOB-2.0

Last updated: 2026-10-22
Governance: developer-led; user explicitly said “No tester.” No tester branch/report will be created or awaited.

| Phase | Status | Evidence / exit gate |
|---|---|---|
| 1. Protocol amendment and structural novelty specification | COMPLETE | [Open discovery plan](OPEN_STRATEGY_DISCOVERY_PLAN.md) freezes research questions, candidate budget, statistical gates and stop condition. |
| 2. Data and feature feasibility | IN PROGRESS — feature-builder unit tests pass; bounded cache acquisition still running | Static source catalogue is documented in [feature feasibility](FEATURE_FEASIBILITY_V2.md). First audit found zero local files, which is not evidence that Dhan or other public sources are unavailable. [Bounded acquisition/cache workflow](../../.github/workflows/qe-nob-v2-data-audit.yml); current run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257). Require a non-empty, quality-audited source cache or a documented source blocker before moving on. |
| 3. Typed strategy grammar and tests | IMPLEMENTED; last verified run passed | Typed predicates, numeric/categorical validation, structural signatures, novelty distance, deterministic mutation/crossover and lineage. [Grammar tests](test_strategy_grammar_v2.py), [successful CI #39802894371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894371). |
| 4. Signal timing and simulator | PARTIAL — unit tests pass; empirical validation blocked | [Signal evaluator](signal_evaluator_v2.py) maps a signal to the next actual market bar and rejects unsupported entry modes. [Option simulator](option_simulator_v2.py) pre-indexes bars, enforces no-overlap per candidate, uses modeled costs/slippage and supports only time exit / premium stop / premium target; conservative same-bar priority is stop first. [Simulator tests #39801813009](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801813009) and [signal tests #39801804759](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801804759) passed. Rolling OHLC still cannot prove exact contract identity, historical bid/ask/depth or executable fills. |
| 5. Bounded novelty-aware discovery | IMPLEMENTED; EMPIRICAL RUN BLOCKED | `run_discovery_v2.py` now wires four fixed-seed islands to training-only multi-objective fitness, validation-based finalist selection, sealed chronological OOS, block bootstrap, Holm correction and cost stresses. Feature eligibility is now frozen from training-only coverage/variation. Automated runner/statistical-utility tests passed in #39807638261 and training-fitness/candidate tests passed in #39807602936; no market-data fitness result is claimed until the acquisition/cache gate passes. [Discovery runner](run_discovery_v2.py); [candidate generator](evolve_candidates_v2.py). |
| 6. Frozen out-of-sample validation and robustness | NOT STARTED | Must use frozen chronological splits, Holm correction, session-block bootstrap, multiple slippage/brokerage stresses, regime/time-block stability and baselines. Do not tune or select against the final OOS period. |
| 7. Manuscript and bounded decision | NOT STARTED | Complete manuscript, reproducibility/supplementary outputs, tables/charts, limitations and a final GO / NO-GO / DATA-LIMITED decision. Stop after this phase; no live-trading approval. |

## Current verified checkpoint

- Grammar tests: 15 passed in combined grammar + feature-audit workflow #39802894371.
- Standalone feature-audit tests passed in #39802894311.
- Candidate generator, signal evaluator and option simulator workflows passed in #39802753682, #39801804759 and #39801813009, respectively.
- Initial cache audit artifact from run #39803204747 reported `BLOCKED_NO_LOCAL_CACHE`, zero underlying/option files, no verified exact contract IDs and no bid/ask/depth. A new bounded acquisition job was added and automatically triggered as run #39803647257; its outcome must be checked before updating the Phase 2 decision.
- No QE-NOB-2.0 candidate has been backtested for fitness or shown profitable. The old QE-NOB-1.0 no-go decision is unchanged and its fitness/OOS results are not reused.

## Mandatory constraints

- Only verified features may enter discovery; missing values are never silently fabricated.
- No short-option legs, live order placement, synthetic quotes, or OOS tuning.
- Model Paytm Money brokerage assumptions and date-effective statutory/exchange fees, plus adverse slippage; quote/fill evidence is still required for an execution pass.
- The simulator fails closed on unsupported exits. Implement and test each new entry/exit semantic before enabling it in candidates.
- No tester branch/report, per user's explicit instruction. Developer-side automated regression tests remain mandatory.
- Stop at Phase 7 or an explicit data blocker; do not run an unbounded search.


## Additional verification checkpoint — 2026-10-22 21:05 IST

- Point-in-time feature builder tests passed in run #39805843560.
- Same-session signal timing tests passed in run #39806277479; simulator same-session handling passed in run #39806376781.
- Expiry-family normalization and the focused regression test passed in simulator workflow #39806477859 (12 tests).
- Bounded source acquisition run #39803647257 remains in progress. Phase 2 stays open until its audit artifact is inspected. Phase 5 discovery stays blocked: no fitness run or candidate P&L has been verified.


## Discovery runner checkpoint — 2026-10-22 21:10 IST

- Phase 5 code path is implemented but has not been run on market data. The runner enforces training-only fitness, validation selection, and a sealed final OOS block; OOS statistical gates include a 5-session moving-block bootstrap, Holm correction, and 0/25/50/100/200 bps slippage with ₹10/₹20 brokerage stresses.
- Feature allowlist eligibility is computed on the training period only; full-sample feature coverage is diagnostic only.
- Statistical utility regression tests passed in runner workflow #39807638261; candidate/training fitness tests passed in #39807602936.
- Runtime source acquisition run #39803647257 remains in progress. Phase 2 and the empirical Phase 5 run are blocked pending its sanitized audit result.


## Automation handoff checkpoint — 2026-10-22

The bounded acquisition workflow now automatically invokes the v2 discovery runner after successful acquisition and cache audit, and uploads sanitized candidate/validation/OOS/stress reports. Workflow #39808171927 is queued behind acquisition run #39803647257, so no manual user workflow action is required. Phase 2 remains open until the acquired cache report is inspected; Phase 5 is implemented and test-verified but not yet empirically completed.


## Cache-gate regression — 2026-10-22

The discovery-runner CI passed after adding the stricter cache audit gate: [run #39808407294](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808407294). It now rejects any cache with JSON parse failures or without both underlying and option files. A later CI run #39808626484 uses a leaner dependency set to reduce unrelated installation time.


## Continuation check — 2026-10-22 21:24 IST

- Discovery-runner CI #39808626484 completed successfully; this is software-test evidence only.
- Acquisition run #39803647257 remains in progress at the source-acquisition step. Cache audit, cache save, and report upload are still pending.
- Automatic follow-up #39808171927 remains pending; no jobs or discovery results have been produced by that run yet.
- No phase gate changed: Phase 2 remains in progress, Phase 5 empirical discovery remains blocked, Phases 6–7 remain not started, and execution remains FAIL pending exact contract and executable quote/fill evidence.
