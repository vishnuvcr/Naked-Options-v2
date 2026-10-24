# NWCP-1.0 Test and Defect Review

Date: 24 October 2026  
Review mode: developer self-test / code review  
Status: **END-TO-END RUN COMPLETED; EMPIRICAL GATE NOT PASSED**

## Scope

Reviewed the target-construction path, expiry-calendar selection, feature timing, evolutionary candidate grammar, chronological split and test helpers. No market-performance conclusion is supported by this review.

## Findings

### CRITICAL — Fallback expiry dates could create labels

**Finding:** `get_expiry_calendar()` constructs weekday-derived fallback expiry dates when the official NSE expiry endpoint is unavailable or insufficiently complete. The pipeline previously passed the resulting list directly to `make_target_rows()`, which could accept labels whose expiry date was inferred rather than officially verified. That risks silent errors around holiday shifts and expiry-regime changes.

**Correction committed:** `expiry_calendar_is_verified()` now requires a non-empty selected calendar, zero fallback dates, provenance for every selected expiry, and `nse_expiry_api` provenance for every selected date. The main runner blocks label construction when this gate fails.

**Regression tests added:** reject fallback dates, accept complete official provenance only, reject incomplete provenance.

**Status:** code correction committed; test execution pending.

### HIGH — Target-bar rejection and provenance coverage were insufficient

**Finding:** Existing tests did not explicitly verify that missing 09:59 anchor bars and missing 15:29 expiry-close bars are rejected, or that fallback expiry provenance blocks the pipeline.

**Correction committed:** tests now cover those cases and basic Holm-adjustment monotonicity/bounds.

**Status:** tests added; test execution pending.

## Checks inspected

- **Anchor timing:** with start-labelled one-minute bars, 09:59–10:00 is used as the last completed bar at 10:00. The adapter assumes public timestamps are bar-start timestamps; that assumption still needs overlap/primary-source verification.
- **Expiry close:** 15:29–15:30 bar is used for the regular-session close. This needs exchange session/timezone verification against accepted source data.
- **Features:** current-session features are restricted to bars starting no later than 09:59; daily aggregates for prior sessions are used for lagged indicators. Point-in-time availability of any future external feature groups remains unimplemented/conditional.
- **Chronology:** current split is 50% train / 20% validation / 30% sealed test. Model selection is by validation balanced accuracy/MCC; final test block is not used for model choice.
- **Evolutionary search:** candidate fitness uses training balanced accuracy with a small complexity penalty; validation is used for selection. The candidate archive is retained in the report.
- **Statistical inference:** bootstrap is approximate and needs robustness checks for block lengths and seeds; a positive metric alone is not enough. Minimum test sample/class-count gates remain mandatory.

## Execution evidence and limitations

A local clone/test command was attempted, but the environment could not resolve `github.com`. I then triggered the repository's push workflow by committing a CI trigger to the test file (commit `48b98fd8bf6c109dc3700f877ee6aa1f68a63901`). GitHub Actions created run [#14](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40104096953), but the latest observed status is `pending` and no job records are available yet. Therefore, **no claim is made that pytest passes**. Continue to inspect this run until a terminal conclusion is available; source/data phases remain blocked meanwhile.

The source/data gates also remain unresolved:
- official expiry endpoint coverage and provenance across every selected expiry;
- public data licensing/provenance and source overlap;
- bar timestamp semantics and missing-minute audit;
- whether the available history yields at least 100 sealed test labels after warm-up;
- point-in-time verification of any additional market/derivatives/news features.

## Decision

**Do not accept a predictive result yet.** The critical label-calendar failure mode is corrected in code, but Phase 2 stays blocked until the regression suite passes and the official expiry/source checks pass. If the official expiry feed is unavailable, the correct status is `DATA-LIMITED` / blocked labels—not silently accepting weekday-generated dates.

## First GitHub Actions execution — run #14

Run [#14](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40104096953) reached the automated unit-test step and reported **13 passed in 1.38 seconds**. The full data/baseline stage then failed in `_evolve_rule` with `KeyError: 'f1'`: the generation loop carried archive wrapper records into the next generation, although prediction expects a candidate dictionary.

**Correction:** elite carry-forward now unwraps each record to its `candidate` object; mutation and crossover use those candidate dictionaries directly. Added a regression test that runs evolution across multiple generations. Defect logged as NWCP-E011. A new push-triggered workflow run is expected from the commits; end-to-end success is not yet established.



## Corrective end-to-end run #18 — 2026-10-24

[Run #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486) completed with CI conclusion **success**. All **14 tests passed in 2.12 seconds**. The full runner completed and reported `valid labels=398, features=398, decision status=OOS_GATE_NOT_PASSED_OR_INSUFFICIENT`. The evolutionary-search wrapper bug is therefore resolved for this execution. The OOS gate did not pass (or did not have sufficient evidence), so this run does not support a predictive edge or a winning method. The sanitized report artifact is [available here](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486/artifacts/12566991817). Remaining limitations include official expiry coverage, source licensing/provenance, timestamp semantics and primary-source overlap validation. Do not promote any candidate or start trading-strategy work.
