# QE-NOB-3.0 phase status

Last updated: 2026-10-23  
Governance: developer-led; no independent tester branch/report per explicit user instruction.

| Phase | Status | Evidence / gate |
|---|---|---|
| 0. Hypothesis design and preregistration | COMPLETE | [STRATEGY_HYPOTHESIS_LAB_V3.md](STRATEGY_HYPOTHESIS_LAB_V3.md) |
| 1. Fresh data feasibility | BLOCKED / NOT RUN | Must validate auth, acquire fresh untouched data, verify timestamp semantics, complete underlying history and stable dated option contract identity |
| 2. Feature/grammar implementation | NOT STARTED | Requires Phase 1 pass |
| 3. Simulator and baseline tests | NOT STARTED | Requires valid data schema and fixtures |
| 4. Bounded discovery (≤600 candidates) | NOT STARTED | Requires Phases 1–3 pass |
| 5. Frozen statistical evaluation | NOT STARTED | Requires candidates frozen and untouched OOS block |
| 6. Manuscript and decision | NOT STARTED | Terminal phase; no extension without protocol version change |

## Current gate decision

No new strategy has been empirically tested. QE-NOB-2.0 OOS outcomes must not be used for new strategy selection. Fresh data and contract identity are prerequisites. If these are unavailable, close QE-NOB-3.0 as DATA-LIMITED rather than reusing the old OOS period or relaxing gates.

## Bounded plan

- Six predeclared hypothesis families, H6 disabled until exact contract/quote data exist.
- At most 600 structurally distinct candidates, four deterministic seeds, maximum 12 generations.
- Chronological train/inner validation, frozen candidates, one untouched OOS evaluation.
- Session-block bootstrap, Holm correction, 0/25/50/100/200 bps slippage per side, ₹10/₹20 brokerage assumptions, dated statutory fees.
- No live order placement, no paper-trading authorization, no tester branch.


## Implementation checkpoint — 2026-10-23

- Added two regression tests to the existing source-client test module to verify the six hypothesis families are present and that empirical testing remains blocked until the fresh-data gate passes.
- Commit: `21fd5c9d9583d0259cc1ddaf6122aeae38095768`.
- Existing GitHub Actions workflow is configured to run on pushes changing `test_run_research.py`; the workflow result has not been independently retrieved in this turn, so test pass is **not claimed**.
- Dhan auth remains a prerequisite: repository secret values are not visible through this integration. Prior QE-NOB-2.0 status says the TOTP bootstrap still requires configured `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET` plus a successful profile-validation run. Do not start a long acquisition before auth tests pass.
- Empirical strategy testing remains BLOCKED until fresh data coverage and stable contract mapping pass. Old OOS remains sealed.


## Workflow wiring checkpoint — 2026-10-23

- Added `.github/workflows/qe-nob-v3-hypothesis-tests.yml` (commit `1659953641a16d50778dfc05fedd87562e7a89d4`). It has `workflow_dispatch` and push triggers limited to this research branch and the relevant plan/test/source paths.
- This workflow runs Python compilation and the source-client pytest suite, including the two QE-NOB-3.0 plan-gate assertions.
- Workflow execution status could not be retrieved through the available GitHub integration, so passing tests are not claimed.
- Fresh data gate remains BLOCKED. No new strategy has been empirically tested; do not start acquisition until auth and source-client gates are verified.

- Added `.github/workflows/qe-nob-v3-data-probe.yml` (commit `7858c6b9b0fe0507a128989b6ff809c5e91d71a1`). It runs only the source credential/schema probe, not bulk acquisition, and uploads the sanitized probe JSON as a short-retention artifact. Secrets are passed as environment variables and must never be printed. The workflow run/result remains unverified through the current integration.


## Regression failure correction — 2026-10-23

- Reviewed user-provided GitHub Actions log: 25 tests passed and one QE-NOB-3.0 plan assertion failed because the test expected a sentence absent verbatim from the plan.
- Corrected the test to assert the exact preregistered wording already present in `STRATEGY_HYPOTHESIS_LAB_V3.md` (commit `79a81636803ba56f2aea638368a91e703504809e`). Added the event to `ERROR_LOG_V3.md` (commit `92f62c371be7f25f8497b0a8929048e62d5a058e`).
- Waiting for the branch push-triggered regression workflow to rerun; pass is not claimed until the new run is green.
- Phase 1 fresh-data feasibility remains BLOCKED / NOT RUN, independent of this test correction.


## Verified workflow results — 2026-10-23

- Regression workflow run [39913031868](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39913031868) completed SUCCESS. All compile steps and the pytest step passed after the assertion wording correction.
- Fresh-data probe workflow run [39912434371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39912434371) completed SUCCESS and uploaded sanitized artifact `qe-nob-v3-sanitized-data-probe` (artifact ID `12482469675`). Probe reported status `PASS`, one supported weekly expiry source (728 rows), and underlying probe `PASS` with 709 rows.
- Important limitation: this was only a small credential/schema probe, not full fresh historical acquisition or stable dated contract/quote validation. Therefore Phase 1 remains BLOCKED pending complete data-coverage, timestamp and contract-identity checks. No empirical strategy testing has started.


## Strict data gate result — 2026-10-23

- [Regression workflow run 39933633753](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39933633753): SUCCESS.
- [Fresh-data probe and strict audit run 39933612441](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39933612441): workflow SUCCESS; research eligibility decision **BLOCKED_DATA_LIMITED**.
- The sanitized audit reported 746 underlying probe rows and 765 rolling option probe rows. Basic endpoint/schema checks passed, but stable dated contract identity was absent and executable bid/ask quote fields were absent.
- These counts are small schema-probe samples only, not a complete historical dataset or proof of backtest eligibility. Phase 1 remains BLOCKED / NOT RUN. No strategy search or empirical evaluation was started.
- Next step: investigate lawful free/public and Dhan-supported routes for dated contract-level history with stable contract IDs and quote/fill evidence; validate provenance, completeness, timestamp integrity, and licensing before changing the gate.

- Alternative-source audit added: [ALTERNATIVE_DATA_SOURCE_AUDIT_V3.md](ALTERNATIVE_DATA_SOURCE_AUDIT_V3.md). Official NSE daily contract-wise and bhavcopy data may help establish dated daily contract identity, while Dhan rolling history may support rolling OHLC/IV/OI research. Neither is assumed to supply historical intraday executable bid/ask. Next bounded step is schema/coverage feasibility, then stop if requirements remain unmet.


## Next bounded public-source step — 2026-10-24

- Added `probe_nse_bhavcopy.py` and `.github/workflows/qe-nob-v3-nse-bhavcopy.yml`. The workflow is manual and push-triggered, samples up to three recent official NSE F&O UDiFF bhavcopy archives, caches the small public ZIP samples, and uploads a schema/coverage report.
- The probe checks dated symbol/expiry/strike/call-put/OHLC/volume/OI fields and NIFTY option row presence. It does not claim that daily data supports intraday fills.
- The regression workflow now compiles the new probe. Workflow results are pending at the time of this commit; no success is claimed until checked.
- Phase 1 remains BLOCKED pending this probe plus contract mapping and execution-data adequacy. No strategy discovery started.
