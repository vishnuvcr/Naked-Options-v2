# Error and defect log — QE-NOB-1.0

Only errors, source failures and protocol deviations from the fresh QE-NOB-1.0 track belong here. Historical records in other study folders are not imported as if observed in this study.

| ID | Date | Severity | Description | Root cause | Correction / test | Status |
|---|---|---|---|---|---|---|
| QE-NOB-E001 | 2026-10-22 | LOW | Existing prediction and option-validation studies have reports and caches in separate paths, creating risk of accidental evidence leakage into the new run. | One repository contains multiple distinct research tracks. | New unique report/cache namespace, independent plan/config/run IDs, and a rule forbidding old outcome reuse. | CLOSED — isolated namespace used by run #39712854501 |
| QE-NOB-E002 | 2026-10-22 | HIGH | Duplicate diagnostics initially flagged 453 conflicting groups out of 471 and dropped 906 rows. | Duplicate key omitted the rolling ATM offset, conflating distinct request-relative observations at identical timestamps/strikes. | Added `offset` to the duplicate key and a regression test with identical timestamp/strike but different offsets. Corrected run #39741806754 reports 0 duplicate groups and 0 rows dropped. | CLOSED for duplicate-key defect; exact contract identity remains covered by E003 |
| QE-NOB-E003 | 2026-10-22 | HIGH | Strict execution gate failed because historical best bid/ask/depth and exact expiry-level contract/lot-size mapping are not validated. | Dhan endpoint provides rolling ATM-relative OHLC/IV/OI/volume/spot, not verified executable historical quotes or stable contract IDs. | Obtain dated instrument/expiry mapping and executable quote data from authorized free sources where possible; keep results DATA_LIMITED until reconciled. | OPEN — blocks promotion |
| QE-NOB-E004 | 2026-10-22 | MEDIUM | Run #39712854501 failed at commit/rebase due to a concurrent `INTERACTION_LOG.md` edit. | Commit step staged overlapping status/log files. | Workflow changed to commit an explicit bounded report allowlist only; run #39730497513 and #39741806754 completed successfully. | CLOSED |
| QE-NOB-E005 | 2026-10-22 | MEDIUM | The workflow initially attempted to stage the full sanitized trade ledger (~189 MB uncompressed). | Commit step staged the entire reports directory. | Explicit allowlist now excludes the ledger from Git; the full report stays in the downloadable Actions artifact. | CLOSED |

## Handling rules
Never include credentials/tokens in logs. Record date, source endpoint, status/error class, retry, cache status and hash. Preserve failed requests. A no-data result is not a zero-price or a losing trade. Do not repair price gaps with synthetic OHLC.
