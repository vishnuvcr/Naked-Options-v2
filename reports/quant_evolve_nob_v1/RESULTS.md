# QE-NOB-1.0 — fresh QuantEvolve-style naked option buying

**Run status:** PASS_ANALYZED  
**Date range:** 2021-10-25 to 2026-10-21  
**Candidates tested:** 600  
**Candidates meeting statistical gate:** 0  
**Candidates meeting strict execution/promotion gate:** 0  
**Basic data quality gate:** True  
**Execution data gate:** False  
**Decision:** NO_STATISTICAL_CANDIDATE — no candidate met the preregistered after-cost statistical and baseline gates; executable profitability remains unverified.

## Important execution-quality limitation
The Dhan rolling endpoint supplies OHLC/IV/OI/volume/spot in an ATM-relative layout, not historical bid/ask depth. P&L therefore uses next-bar open with prespecified adverse slippage; this is not proof of executable fills. Historical expiry-level lot-size mapping still requires a contract-master reconciliation. The full promotion gate cannot pass until historical execution quotes and contract identity are verified. Even a future PASS only permits prospective paper testing, never automatic live trading.
## Top candidates selected on validation only

|ID|Hypothesis|Validation mean daily net (₹)|OOS trades|OOS mean daily net (₹)|OOS 95% block CI low (₹)|OOS Holm p|Statistical gate|
|---:|---|---:|---:|---:|---:|---:|---|
|86|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|116.79560009747699|151|6.144874311785659|-195.69134429024234|1.0|False|
|45|Always enter at 09:25 after the first two completed bars, buying the call or put matching the initial move; hold 120 minutes.|110.24101405512653|238|-63.1032347169017|-368.33354673065116|1.0|False|
|166|Break the first 5-minute range with a 0.25 range-width buffer; buy the directional option and hold 120 minutes.|104.14884810269764|202|-37.18457996247216|-283.63170772665825|1.0|False|
|276|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|97.68129924234587|151|-29.439443311958843|-221.93924499244707|1.0|False|
|15|Fixed-time long-call benchmark, 120-minute holding period, moneyness offset 1.|95.09977508617904|235|-163.82694661359744|-406.1437825946395|1.0|False|
|516|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|83.83139459613456|155|12.78299339816347|-183.88251267356122|1.0|False|
|154|Break the first 5-minute range with a 0.40 range-width buffer; buy the directional option and hold 120 minutes.|73.63414946685985|186|9.81890326632732|-214.39251622016354|1.0|False|
|13|Fixed-time long-call benchmark, 120-minute holding period, moneyness offset 1.|68.8583288806667|235|-179.52283326524613|-439.50263336678324|1.0|False|
|173|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|60.388564384446|158|26.20856903080113|-120.73348138191987|1.0|False|
|254|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|58.35443060895892|155|-2.073651128526989|-215.25531154350358|1.0|False|
|408|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|54.09505799320048|55|-3.0068960730938077|-89.95826727914123|1.0|False|
|533|Break the first 30-minute range with a 0.40 range-width buffer; buy the directional option and hold 120 minutes.|52.142946498950224|116|126.04836360174342|-51.04507732749753|1.0|False|
|420|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|51.680752916062595|159|70.37058696610866|-50.63569155374425|1.0|False|
|233|An opening gap of at least 0.25% continues intraday; buy the gap-direction option after the opening bars.|49.227329891331976|116|-17.995165154920347|-108.12364958695805|1.0|False|
|415|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|46.34749016314453|55|-11.175732746263302|-95.86321580455242|1.0|False|
|182|Break the first 15-minute range with a 0.00 range-width buffer; buy the directional option and hold 120 minutes.|44.46296122992856|221|-137.6609854217612|-419.51189559168967|1.0|False|
|319|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|43.89583639866767|55|-2.969913958635987|-79.79040827600683|1.0|False|
|398|An opening gap of at least 0.25% continues intraday; buy the gap-direction option after the opening bars.|43.43120638982924|116|-12.77603476997503|-92.1128934902012|1.0|False|
|441|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|42.668360436742645|55|-7.217863575656122|-98.01855665807298|1.0|False|
|221|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|40.73872914234669|55|-17.599196279231943|-76.99037895453077|1.0|False|

## Files
- source_probe.json and acquisition_summary.json: source status, range, cache and request outcomes
- candidate_results.csv: all candidates, all chronology splits, full-family Holm correction
- trade_ledger_sanitized.csv: sanitized per-trade P&L and fee decomposition
- validation_finalists_oos.csv: finalists selected on validation and evaluated on the untouched OOS block
- source_failures.csv: failed source requests; credentials are never written

## Notes
- Historical contract lot size is a date-based proxy pending exact expiry-level contract-master reconciliation.
- Rolling-option OHLC has no historical best bid/ask; slippage is stress modeled, not observed spread.
- Primary metrics use one-lot after-cost P&L, but not all execution quality can be proven with OHLC.
- Only the latest 20% chronology is reserved for final confirmation; its full candidate-family p-values are Holm-adjusted.
