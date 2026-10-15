# VOL-REGIME-OPT-1.0 — source-gate disposition

**Date:** 2026-10-15  
**Disposition:** BLOCKED — no P&L or strategy conclusion  
**Gate:** Phase 2b, verified expiry mapping and contract identity

## Evidence checked

- The persisted Dhan probe covers 2025-01-06 through 2025-01-10 at 5-minute resolution.
- Dhan WEEK candidate expiry codes 1 and 2 returned 375 rows each for CALL and PUT and contained timestamp, OHLC fields selected by the request, strike, spot and IV. WEEK code 0 returned HTTP 400 `DH-905: expiryCode is required`.
- The persisted audit predates the latest code-3 probe edit and therefore cannot be treated as evidence about code 3.
- The Dhan rolling response as audited does not itself provide an explicit contract expiry-date field. The sampled response is rolling strike-relative data, not a demonstrated fixed-contract entry-to-exit series.
- The repository's Hugging Face fallback script identifies a dataset with an unrecognized `other` license and provider-terms restrictions. The expected audit file was not found on the developer branch, so no successful fallback acquisition or quality result is claimed.
- Official NSE materials describe NIFTY weekly expiry rules and contract specifications, but calendar rules alone do not prove which historical expiry a Dhan rolling expiry code represents for every timestamp.

## Gate decision

Do not run P&L, infer profitability, or proceed to strategy selection until both are independently verified:
1. candidate expiry code to actual expiry date mapping across historical weekday/holiday changes; and
2. exact numeric strike and expiry continuity at entry and expiry exit, with missing contracts counted against the coverage gate.

No monthly substitution is permitted. No rupee P&L can be claimed without historical lot sizes and dated charges. The frozen strategy hypothesis and parameters remain unchanged; this is a data-feasibility blocker, not a negative profitability result.

## Bounded next action

One final bounded source check may be made by the independent tester: inspect a fresh code-3 audit if one exists, verify the Dhan annexure's expiry-code semantics and available historical contract-master/expiry calendar, and inspect the HF audit/license status. If exact expiry mapping and contract continuity remain unproven, close this study BLOCKED with no strategy recommendation. Do not relax gates or start a parameter search.
