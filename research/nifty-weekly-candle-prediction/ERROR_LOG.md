# Error and Defect Log — NWCP-1.0

This file records observed failures, incorrect assumptions, corrections and verification evidence. Do not record credentials, secrets or hidden reasoning.

| ID | Date | Severity | Defect / risk | Correction | Status |
|---|---|---|---|---|---|
| NWCP-E001 | 2026-10-24 | HIGH | Prior repository tracks target general NIFTY forecasting or option buying, so their conclusions do not establish weekly-expiry direction skill. | New isolated NWCP-1.0 namespace; prior scores and candidate fitness excluded from evidence. | Corrected in protocol |
| NWCP-E002 | 2026-10-24 | HIGH | Assuming a constant expiry weekday across historical years would mislabel endpoints after exchange changes and holidays. | Use actual expiry metadata and official circular/calendar records; audit every expiry before labels. | Open — Phase 2 gate |
| NWCP-E003 | 2026-10-24 | HIGH | Bar timestamps may identify candle start or end; selecting the 10:00 bar close could leak price after model cutoff. | Verify source timestamp semantics; use last completed bar ending <=10:00; add cutoff assertions and hand-checked fixtures. | Open — adapter test |
| NWCP-E004 | 2026-10-24 | HIGH | Evolutionary indicators can overfit when many candidates are tried and the winning one is cherry-picked. | Freeze search budget; log all candidates/seeds; training-only fitness, validation selection, sealed chronological OOS and multiplicity correction. | Mitigation specified; implementation pending |
| NWCP-E005 | 2026-10-24 | MEDIUM | Public datasets may lack license clarity, provenance or consistent timestamp conventions. | No canonical use until license/overlap/time-grid audit passes; quarantine discrepancies. | Open — Phase 1/2 |
| NWCP-E006 | 2026-10-24 | MEDIUM | FII/DII, news and option summaries may be published after 10:00 or lack point-in-time history. | Require publication-time gating; lag to prior known value or exclude. | Open — feature audit |
| NWCP-E007 | 2026-10-24 | MEDIUM | Exchange data may have use/redistribution restrictions despite being web-accessible. | Review source terms; publish only sanitized and license-safe summaries. | Open — data governance |
