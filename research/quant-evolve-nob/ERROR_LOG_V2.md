# Error and implementation log — QE-NOB-2.0

This log records concrete defects, workflow outcomes and protocol deviations. It is not a transcript and must not contain hidden reasoning or credentials.

| ID | Date | Severity | Issue / risk | Correction / handling | Status |
|---|---|---|---|---|---|
| QE-NOB2-E001 | 2026-10-22 | HIGH | QE-NOB-1.0's 600-candidate constrained grammar did not adequately evolve structurally different entry/exit logic; candidate count overstated diversity. | New protocol adds syntax-tree structural signatures, novelty distance, mutation/crossover, exit-state rules and a fixed maximum 1,500 unique candidates. | DESIGN CORRECTION RECORDED |
| QE-NOB2-E002 | 2026-10-22 | MEDIUM | Proposed global-lead, India VIX, FII/DII, IV-derived and event features are not all verified in the current cached feature panel. | Phase 2 feature matrix marks these conditional. Runtime field/coverage and publication-time checks must pass before the features can be enabled. | OPEN |
| QE-NOB2-E003 | 2026-10-22 | MEDIUM | New typed grammar code and tests have been committed, but automated workflow result has not yet been inspected. | Added push/manual workflow `.github/workflows/qe-nob-v2-grammar-tests.yml`; do not call grammar validated until a successful run is observed. | OPEN — CI RESULT PENDING |
| QE-NOB2-E004 | 2026-10-22 | HIGH | Structural grammar is not yet connected to the backtester; passing unit tests alone cannot establish market validity. | Keep Phase 4–6 blocked until feature gating, simulator integration, hand-calculated fixtures, frozen OOS and after-cost gates are implemented. | OPEN |
