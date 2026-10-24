# NIFTY prediction research error log

## NP-001 — Daily source not exchange-certified (open)
- **Severity:** Medium/high for inference.
- **Issue:** The initial baseline uses Yahoo Finance daily NIFTY 50 data as a free source.
- **Risk:** Historical adjustments, missing sessions, or provider changes can affect labels and feature values.
- **Mitigation:** Record source manifest/hash; compare against NSE/Nifty Indices official data before stronger claims. Do not treat this as exchange-certified.

## NP-002 — New workflow run not yet verified (open)
- **Severity:** High for reporting.
- **Issue:** Benchmark and workflow files were just committed; no successful test/benchmark artifact has yet been inspected.
- **Mitigation:** Inspect actual GitHub Actions status and artifact. Do not claim scores until verified.

## NP-003 — Scope mismatch with original expiry study (open)
- **Severity:** Medium.
- **Issue:** This replacement benchmark targets next-session daily direction, not weekly-expiry interval direction.
- **Mitigation:** Clearly label scope. Build an expiry-specific target only after a verified historical calendar and exact timestamped spot dataset are available.

## NP-004 — Optional research libraries not yet integrated (open)
- **Severity:** Medium.
- **Issue:** ARCH, MAPIE, PySR, tick, Quantevolve, TradingAgents and astra-quant-agent have not all been installed or executed.
- **Mitigation:** Keep optional; validate dependency versions and contracts before integration. Baseline models must remain interpretable and independently evaluated.


## NP-005 — Workflow result not observable (open)
- **Severity:** High for result reporting.
- **Issue:** The GitHub status query returned no status entries for the benchmark workflow commits and the available commit-associated run query returned no runs.
- **Mitigation:** Treat the code as committed but unverified. Do not infer pass/fail or publish scores until the Actions run and artifact are inspected.


## NP-006 — Local execution environment cannot reach GitHub (open)
- **Severity:** Medium for verification.
- **Issue:** A direct shallow clone attempt failed because this execution environment could not resolve github.com. The available GitHub connector can read/write repository files but did not expose a workflow-dispatch action or an all-runs listing.
- **Mitigation:** Continue checking repository evidence through available GitHub endpoints. Do not claim unit tests or empirical benchmark ran until Actions artifacts/logs are accessible.


## NP-007 — Alternate historical dataset is stale (open)
- **Severity:** High for current-market generalization.
- **Issue:** The available third-party CSV mirror ends on 2019-12-02. It supports a preliminary historical diagnostic but not current-market claims.
- **Mitigation:** Keep the source and date range explicit; seek a recent daily series from Yahoo Finance and/or a free official-source dataset, then compare overlapping dates before using it for final conclusions.

## NP-008 — Preliminary diagnostic uses custom implementation (open)
- **Severity:** Medium for exact reproducibility against production pipeline.
- **Issue:** Preliminary logistic results were calculated with a custom Node.js gradient-descent implementation, not scikit-learn LogisticRegression. Random forest and gradient boosting were not included in this diagnostic.
- **Mitigation:** Treat scores as preliminary only. Verify the production Python benchmark and all planned model families before finalizing conclusions.


## NP-009 — Production workflow results still unavailable (open)
- **Severity:** High for final empirical conclusions.
- **Issue:** The available GitHub integration can read and write repository content but has not exposed a dispatch or complete workflow-run listing. No production benchmark JSON or source-parity artifact is present in the branch.
- **Mitigation:** The workflow is triggered by research-code pushes and persists outputs; continue to report execution as unverified until actual artifacts appear. Do not promote the preliminary custom diagnostic to final evidence.

## NP-010 — Second free dataset is a third-party mirror (open)
- **Severity:** Medium/high for data provenance.
- **Issue:** The new source catalog claims recent daily NIFTY 50 data through 2026-10-23, but is not exchange-certified and has not yet been parity-audited against the primary series.
- **Mitigation:** Run the cross-source OHLC audit, preserve the source hash and mismatch distribution, and seek official Nifty Indices/NSE data for final confirmation.


## NP-011 — Optional parity artifact could break result persistence (fixed in code; CI pending)
- **Severity:** Medium.
- **Issue:** The workflow allowed the second-source parity audit to fail with `continue-on-error: true`, but the persistence step staged its JSON output unconditionally. If the audit failed before writing the file, `git add` could exit nonzero and fail the otherwise usable primary benchmark job.
- **Fix:** Persistence now checks each expected output path and stages only files that exist, logging missing optional artifacts. This preserves primary benchmark output even if the independent parity audit is unavailable.
- **Verification:** Workflow YAML updated in commit `dcce2fc65ee91d45544ac3779b9c08bf100d0c13`; actual GitHub Actions execution remains unverified, so CI confirmation is still required.
