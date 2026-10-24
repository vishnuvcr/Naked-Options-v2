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
