# Error and implementation log — QE-NOB-2.0

This log records concrete defects, workflow outcomes and protocol deviations. It is not a transcript and must not contain hidden reasoning or credentials.

| ID | Date | Severity | Issue / risk | Correction / handling | Status |
|---|---|---|---|---|---|
| QE-NOB2-E001 | 2026-10-22 | HIGH | QE-NOB-1.0's 600-candidate constrained grammar did not adequately evolve structurally different entry/exit logic; candidate count overstated diversity. | New protocol adds syntax-tree structural signatures, novelty distance, mutation/crossover, exit-state rules and a fixed maximum 1,500 unique candidates. | DESIGN CORRECTION RECORDED |
| QE-NOB2-E002 | 2026-10-22 | MEDIUM | Proposed global-lead, India VIX, FII/DII, IV-derived and event features are not all verified in the current cached feature panel. | Phase 2 feature matrix marks these conditional. Runtime field/coverage and publication-time checks must pass before the features can be enabled. | OPEN |
| QE-NOB2-E003 | 2026-10-22 | MEDIUM | New typed grammar code and tests have been committed, but automated workflow result has not yet been inspected. | Added push/manual workflows for grammar and feature-audit tests. Do not call grammar validated until a successful run is observed. | OPEN — CI RESULT PENDING |
| QE-NOB2-E004 | 2026-10-22 | HIGH | Structural grammar is not yet connected to the backtester; passing unit tests alone cannot establish market validity. | Keep Phase 4–6 blocked until feature gating, simulator integration, hand-calculated fixtures, frozen OOS and after-cost gates are implemented. | OPEN |
| QE-NOB2-E005 | 2026-10-22 | MEDIUM | Initial tests imported the research folder as an underscore-named Python package even though the on-disk folder contains hyphens. Dynamic dataclass loading also requires registering the module in `sys.modules`. | Rewrote test loading to use `importlib.util.spec_from_file_location` and register the module before execution. Workflow result still pending. | CORRECTED IN SOURCE; CI UNVERIFIED |
| QE-NOB2-E006 | 2026-10-22 | MEDIUM | The feature-audit tool can only inspect files present in the runner/cache; no local or committed raw cache has yet been audited by this new utility. | Explicitly reports `BLOCKED_NO_LOCAL_CACHE` if no files exist and documents that missing local cache is not proof of source unavailability. | OPEN — RUNTIME AUDIT PENDING |

| QE-NOB2-E007 | 2026-10-22 | HIGH | Candidate generator now creates structurally distinct candidates but has no simulator-backed fitness, so it cannot yet evolve toward profitable candidates. | Explicitly label output `CANDIDATES_GENERATED_NOT_BACKTESTED`; do not treat novelty as profitability. Phase 4 must implement a tested evaluator and only then fitness-guided evolution. | OPEN |

| QE-NOB2-E008 | 2026-10-22 | HIGH | Initial signal evaluator draft mapped sparse signals to the next signal timestamp, which can skip intervening market bars and distort entry timing. | Changed to map each signal to the next timestamp in the full sorted market-bar grid; added sparse-signal regression test. CI result pending. | CORRECTED IN SOURCE; CI UNVERIFIED |

| QE-NOB2-E009 | 2026-10-22 | HIGH | First option simulator draft did not prevent overlapping positions for a single candidate and contained redundant contract-row lookup logic. | Simplified entry lookup, enforced one open position per candidate, required same-strike legs for straddles, and added a no-overlap regression fixture. CI remains unverified. | CORRECTED IN SOURCE; CI UNVERIFIED |
