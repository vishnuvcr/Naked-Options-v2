# QE-NOB-3.0 Research Disposition Manuscript: DATA-LIMITED

**Version:** 3.0  
**Disposition date:** 2026-10-24  
**Branch:** `research/qe-nob-v3-hypothesis-lab`  
**Status:** Bounded data-feasibility study completed; strategy performance testing not started.

## Abstract

This study assessed whether fresh and reproducible data were available to support a preregistered, bounded search for NIFTY long-option strategies. The planned research requires dated option-contract identity, timestamp integrity, sufficient historical coverage, and execution assumptions that can be defended against slippage and costs. Automated regression tests passed. A Dhan source probe returned rolling option and underlying bars, but the strict audit found no explicit stable dated contract identity or historical bid/ask fields in the rolling option payload. A bounded probe of official NSE F&O UDiFF daily bhavcopy archives successfully parsed three recent daily files, each containing date/expiry/strike/option-type/OHLC/volume/open-interest fields and 5,865–5,941 detected NIFTY option rows. These daily records do not supply intraday bid/ask, depth, or executable fills and do not independently resolve Dhan rolling-series-to-expiry mapping. Under the preregistered gate, the research therefore stops at **DATA-LIMITED**. No candidate strategies were searched, selected, backtested, or approved.

## 1. Research question

Can public NSE daily F&O archives and the available Dhan historical rolling-option endpoint be combined into a reproducible dataset that supports robust, statistically valid evaluation of NIFTY long-option strategies with realistic execution costs?

### Aims and objectives

1. Verify source access and schema using automated, reproducible checks.
2. Establish whether dated option identity, expiry, strike, option type, timestamps and required market fields are present.
3. Determine whether the data can support defensible execution prices and transaction-cost modeling.
4. Preserve fail-closed gates and stop rather than lower standards if the data are inadequate.

## 2. Methods

### 2.1 Preregistered controls

The QE-NOB-3.0 plan limits future discovery to at most 600 structurally distinct candidates, four deterministic seeds, at most 12 generations and six hypothesis families. It requires feature and simulator tests, an untouched out-of-sample period, session-level moving-block bootstrap, Holm correction, and stress tests across 0/25/50/100/200 basis points adverse slippage per side and ₹10/₹20 brokerage per order, plus date-effective statutory charges. None of those performance-search stages was started because the data gate failed.

### 2.2 Automated checks

- Regression workflow [40009667755](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40009667755): passed, including Python compilation and source/plan tests.
- Strict rolling-option gate [39933612441](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39933612441): workflow passed; research decision was `BLOCKED_DATA_LIMITED`. The small probe observed 746 underlying bars and 765 rolling-option bars. Explicit stable dated contract identity fields and bid/ask quote fields were absent.
- Official NSE archive probe [40009611140](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40009611140): passed for three recent files and uploaded schema report plus sample ZIPs as artifact [12526450061](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40009611140/artifacts/12526450061).

### 2.3 NSE daily sample

| Candidate trade date | Result | CSV rows | Detected NIFTY option rows | Required daily fields |
|---|---:|---:|---:|---|
| 2026-10-22 | PASS | 39,343 | 5,941 | Present |
| 2026-10-21 | PASS | 38,777 | 5,865 | Present |
| 2026-10-20 | NOT FOUND | — | — | Not assessed |
| 2026-10-19 | PASS | 38,485 | 5,879 | Present |

The missing 20 October archive is recorded as a source gap; it is not assumed to be a market holiday. This is a three-session schema feasibility sample, not a historical coverage study.

### 2.4 Data requirements not met

The rolling option endpoint provides ATM-relative OHLC/IV/volume/OI/spot series, but the probe does not establish a unique dated contract key for every bar. The sampled payload also lacks historical bid/ask quote fields. NSE daily bhavcopy supports daily contract-level checks, but daily OHLC/settlement cannot be substituted for five-minute fills or historical spread/depth. Joining by date, strike and call/put alone is unsafe where multiple expiries can share a strike; without verified expiry mapping, this composite is not accepted as stable contract identity.

## 3. Results

1. **Automation:** source/plan regression tests and the NSE feasibility workflow passed.
2. **Public daily source:** official NSE UDiFF archive downloads and required daily schema fields were validated on three recent sessions.
3. **Dhan rolling source:** basic API access/schema checks passed on a small sample, but stable dated identity and executable quote fields did not pass the strict gate.
4. **Coverage:** full multi-year coverage, missingness, contract transitions, corporate actions and cross-source reconciliation were not established.
5. **Strategy performance:** not measured. There are no strategy returns, significance tests, rankings or profitability claims.

## 4. Statistical analysis and inference

No strategy-level statistical analysis was run because no candidate evaluation was authorized by the preregistered data gate. It would be invalid to infer predictive edge or profitability from source availability or row counts. The correct inference is limited: a daily contract-level source is technically accessible, but the combined sources currently do not demonstrate the intraday execution fidelity required for the intended strategy study.

## 5. Discussion

The main finding is a data adequacy boundary, not a negative result about any strategy hypothesis. Public daily bhavcopy data can help verify daily contract identifiers and settlement/volume/OI history. Dhan rolling option data may be useful for some rolling-premium research if its expiry/contract semantics are independently established. However, a daily record does not reveal the price available at a particular intraday entry or exit, and a rolling strike label is not sufficient evidence of a specific expiry contract. Using either as a substitute for historical quotes would introduce avoidable contract-mapping and execution bias.

## 6. Strengths

- Preregistered a finite search and stopping rule before performance evaluation.
- Automated, branch-scoped checks with recorded workflow runs.
- Used official NSE archives for a bounded source/schema check.
- Kept the old QE-NOB-2.0 OOS period sealed from new selection.
- Did not replace missing quotes with fabricated spreads or treat daily prices as intraday fills.
- Preserved source gaps and test failures in the error log.

## 7. Limitations

- Only three recent NSE daily archives were schema-checked; full historical coverage was not audited.
- The missing candidate date was not independently classified as a holiday or archive failure.
- The probe did not reconcile every Dhan bar against a uniquely identified NSE dated contract.
- No historical bid/ask, order-book depth, or broker fill data were obtained.
- No candidate strategies or prediction models were tested, so there are no empirical performance results.
- This disposition does not establish that suitable data can never be obtained; it states that eligibility was not demonstrated within this bounded phase.

## 8. Conclusion

**Final disposition: DATA-LIMITED.** The source-feasibility phase is closed for this protocol version. Daily NSE contract data passed a small schema sample, but stable mapping of the Dhan rolling series and defensible historical intraday execution prices remain unresolved. Per the preregistered stopping rule, Phases 2–6 (feature implementation, simulator, discovery, frozen evaluation and final strategy-performance analysis) are not started. No strategy is recommended or approved for paper/live trading.

## 9. Future research

1. Obtain or collect prospectively timestamped NIFTY option-chain snapshots containing stable contract identifiers and bid/ask prices at sufficient frequency.
2. Validate contract mapping using exact expiry date, strike, option type, instrument identifier and exchange timestamp—not strike alone.
3. Run a larger, multi-year NSE archive audit with checksums, trading-calendar reconciliation, missingness and schema-version handling.
4. If an independently licensed source of historical intraday quotes/trades becomes available, rerun Phase 1 under a new protocol version before opening the search budget.
5. Only after all gates pass, implement hand-calculated fixtures, no-lookahead tests, conservative next-bar fills and dated fees, then run the preregistered candidate search and one frozen OOS evaluation.

## Appendix A. Reproducibility links

- [QE-NOB-3.0 hypothesis plan](STRATEGY_HYPOTHESIS_LAB_V3.md)
- [Phase status](PHASE_STATUS_V3.md)
- [Error log](ERROR_LOG_V3.md)
- [Alternative source audit](ALTERNATIVE_DATA_SOURCE_AUDIT_V3.md)
- [NSE probe implementation](probe_nse_bhavcopy.py)
- [Strict contract/quote audit](validate_fresh_data_gate.py)
- [NSE probe workflow](../../.github/workflows/qe-nob-v3-nse-bhavcopy.yml)
- [Regression workflow](../../.github/workflows/qe-nob-v3-hypothesis-tests.yml)

## Appendix B. Decision boundary

The word **PASS** in a workflow title or job status means the automation ran successfully. It does not mean the research data passed the strategy eligibility gate. In this study the daily NSE schema sample passed, while the overall intraday option execution-data gate failed. No trading or investment conclusion is drawn.
