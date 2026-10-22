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
|86|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|172.38017229599004|151|10.681524600625325|-188.61601831732625|1.0|False|
|369|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|123.46452378613156|155|15.73139292495075|-182.1057851643505|1.0|False|
|238|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|116.38099963722894|151|-24.57769114506103|-214.71688893704197|1.0|False|
|13|Fixed-time long-call benchmark, 120-minute holding period, moneyness offset 1.|106.57525254987335|235|-172.2178945496195|-427.50982456455904|1.0|False|
|45|Always enter at 09:25 after the first two completed bars, buying the call or put matching the initial move; hold 120 minutes.|105.82060769479168|238|-54.76391942721513|-357.99253673083905|1.0|False|
|166|Break the first 5-minute range with a 0.25 range-width buffer; buy the directional option and hold 120 minutes.|92.3384919077037|202|-25.845337395808386|-262.2021052337448|1.0|False|
|534|An opening gap of at least 0.25% continues intraday; buy the gap-direction option after the opening bars.|61.799196125544135|108|-39.97443807948627|-239.06264742977996|1.0|False|
|173|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|59.89761905136819|158|23.670295189179782|-121.177239143178|1.0|False|
|558|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|58.12087587304165|159|70.35019741209886|-49.03199735360076|1.0|False|
|502|Break the first 30-minute range with a 0.10 range-width buffer; buy the directional option and hold 5 minutes.|56.88124227904|214|-29.035048735577263|-145.40926712063356|1.0|False|
|154|Break the first 5-minute range with a 0.40 range-width buffer; buy the directional option and hold 120 minutes.|54.23475775525579|186|11.55784975946878|-210.3739330172723|1.0|False|
|371|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|49.846110258720344|160|61.11421709087639|-69.9889279380628|1.0|False|
|15|Fixed-time long-call benchmark, 120-minute holding period, moneyness offset 1.|44.144253305060225|235|-159.30044139533948|-400.4686602661811|1.0|False|
|418|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|43.1423874246659|55|-3.0068960730938077|-89.95826727914123|1.0|False|
|103|An opening gap of at least 0.15% continues intraday; buy the gap-direction option after the opening bars.|37.25855782155749|158|-120.12117088247864|-311.9810825139981|1.0|False|
|221|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|37.20791060117068|55|-17.599196279231943|-76.99037895453077|1.0|False|
|331|An opening gap of at least 0.25% continues intraday; buy the gap-direction option after the opening bars.|36.29284210869914|116|-17.610131029463133|-106.13548790234073|1.0|False|
|457|Break the first 30-minute range with a 0.10 range-width buffer; buy the directional option and hold 5 minutes.|35.94217204822055|213|-16.0172892182246|-115.14908626581128|1.0|False|
|194|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|35.63470861795426|55|-2.969913958635987|-79.79040827600683|1.0|False|
|505|An opening gap of at least 0.50% continues intraday; buy the gap-direction option after the opening bars.|32.90362370075797|55|-11.175732746263302|-95.86321580455242|1.0|False|

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
