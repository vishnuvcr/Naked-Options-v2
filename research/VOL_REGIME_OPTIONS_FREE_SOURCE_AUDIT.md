# Free-source audit — VOL-REGIME-OPT continuation

**Audit date:** 2026-10-16  
**Purpose:** identify lawful/free evidence that can validate historical weekly expiry mapping and option contract identity before any P&L work.

## Sources checked

| Source | What it provides | Relevance | Current limitation / next check |
|---|---|---|---|
| [Dhan expired options API documentation](https://dhanhq.co/docs/v2/expired-options-data/) | Rolling expired options at minute intervals; OHLC, IV, volume, OI, spot; up to five years; requests up to 30 days; relative strikes such as ATM and ATM±N. | Primary candidate for historical intraday option data. | The documented endpoint describes rolling-relative strikes. Schema-valid WEEK expiryCode responses do not by themselves prove code-to-expiry-date mapping or fixed numeric strike continuity. Must query dated ranges and reconcile timestamps/strike fields against an independently verified expiry calendar. |
| [Dhan option-chain / expiry-list documentation](https://dhanhq.co/docs/v2/option-chain/) | Active expiry list for an underlying and current option-chain fields. | Can help verify endpoint semantics and current active expiry metadata. | Active expiry list does not automatically establish historical expired expiry mapping. Do not use current metadata as historical truth without proof. |
| [NSE All Reports — Derivatives](https://www.nseindia.com/all-reports-derivatives) | Official derivatives reports including UDiFF bhavcopy, contract files, settlement prices, participant statistics and FII derivatives statistics. | Free official daily contract/settlement and context data where accessible. | EOD reports are not a substitute for intraday executable quotes. Determine whether historical contract files cover the required dates and expiry identifiers. |
| [NSE historical EOD data subscription page](https://www.nse.in/static/market-data/eod-historical-data-subscription) | Describes historical end-of-day files and subscription options. | Clarifies official archive coverage and licensing. | Do not assume paid-only EOD archives are free; first exhaust public reports and Dhan entitlement. |
| [Public NSE F&O bhavcopy archive repository](https://github.com/SantoshSrinivas79/NSE-FNO-Data-bank) | Community mirror of validated daily NSE F&O bhavcopy ZIPs and format transition notes. | Possible cached source for daily contract/settlement data. | Community mirror, not authoritative; verify hashes and compare sample records to NSE originals. Does not establish intraday bid/ask. |
| [Shoonya Trader historical expired options page](https://shoonyatrader.in/free-historical-expired-options-contract-data/) | Advertises expired index-option minute data and asks users to request the full dataset. | Potential alternative lead. | Full dataset access, terms, provenance, and completeness are not publicly verified; do not treat as acquired or free until checked. |

## Findings

1. A legitimate Dhan expired-options endpoint exists and documents up to five years of rolling minute-level data. This supports continuing the source investigation, but it does not resolve the specific weekly expiry-code mapping defect.
2. NSE publishes official derivatives reports and contract files, including UDiFF bhavcopy. These are a free-source avenue for daily contract/expiry cross-checks, not proof of full intraday quote coverage.
3. Community repositories and vendor pages are leads only. No external dataset has been downloaded, licensed, or validated by this web/source audit.
4. No option P&L was calculated in the initial audit. On 2026-10-16, repository inspection of `vishnuvcr/Nifty` identified the existing HF dataset source and a new cached audit workflow was added to this continuation branch. The workflow run is being checked before any source/coverage conclusion is made.
5. Required next technical step: inspect the actual persisted Dhan source-audit artifact and the exact request/response metadata, then compare returned dated strike/timestamps to official NSE contract/expiry evidence. If stable exact contracts cannot be reconstructed, do not backtest that data as fixed-expiry positions.

## Gate status

**C1 — expiry mapping and fixed-contract continuity: OPEN / BLOCKING pending workflow audit and official-source reconciliation.**  
**C2 — full historical coverage and quality: NOT STARTED.**  
**C3–C7 — signal, P&L, costs, inference, checks, manuscript: NOT STARTED.**

No strategy has passed the required gates; no profitability conclusion is supported.


## Official expiry-rule reconciliation note (2026-10-16)

NSE's own circulars demonstrate why a weekday rule alone is insufficient for historical contract mapping: the NIFTY weekly/monthly expiry schedule was revised effective April 2025, and revised again during June 2025 for contracts from September 2025 onward. See [NSE circular 33/2025 (4 March 2025)](https://nsearchives.nseindia.com/content/circulars/FAOP66938.pdf), [NSE circular 108/2025 (23 June 2025)](https://nsearchives.nseindia.com/content/circulars/FAOP68685.pdf), and [NSE circular 111/2025 (25 June 2025)](https://nsearchives.nseindia.com/content/circulars/FAOP68747.pdf). The official [NSE NIFTY 50 F&O contract information](https://www.nseindia.com/static/products-services/equity-derivatives-nifty50) describes contract identity using underlying, expiry date, option type, and strike. Therefore expiry reconciliation must use dated contract-file evidence and applicable circulars, not a hard-coded weekday heuristic. This is a documented design constraint, not evidence that the HF files have passed reconciliation.
