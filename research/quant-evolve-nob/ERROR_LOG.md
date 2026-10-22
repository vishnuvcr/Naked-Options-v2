# Error and defect log — QE-NOB-1.0

Only errors, source failures and protocol deviations from the fresh QE-NOB-1.0 track belong here. Historical records in other study folders are not imported as if observed in this study.

| ID | Date | Severity | Description | Root cause | Correction / test | Status |
|---|---|---|---|---|---|---|
| QE-NOB-E001 | 2026-10-22 | LOW | Existing prediction and option-validation studies have reports and caches in separate paths, creating risk of accidental evidence leakage into the new run. | One repository contains multiple distinct research tracks. | New unique report/cache namespace, independent plan/config/run IDs, and a rule forbidding old outcome reuse. Verify workflow reads only data/cache/quant_evolve_nob_v1/ and reports/quant_evolve_nob_v1/. | OPEN until workflow isolation is tested |

## Handling rules
Never include credentials/tokens in logs. Record date, source endpoint, status/error class, retry, cache status and hash. Preserve failed requests. A no-data result is not a zero-price or a losing trade. Do not repair price gaps with synthetic OHLC.
