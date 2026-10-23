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
