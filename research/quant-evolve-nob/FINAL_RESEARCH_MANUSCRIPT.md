# QE-NOB-2.0: Bounded Evolutionary Discovery of Long NIFTY Options Rules Under Incomplete Execution Data

**Status:** Final bounded discovery report — DATA-LIMITED  
**Training:** 2021-10-25 to 2024-04-29 | **Validation:** 2024-04-30 to 2025-02-24 | **OOS:** 2025-02-25 to 2025-12-30  
**Branch:** `research/quant-evolve-nob-v2-discovery-developer`

## Abstract

This study assessed whether bounded evolutionary search could discover long NIFTY index-option rules with positive modeled net outcomes on a chronological out-of-sample (OOS) period. The pipeline used NIFTY 5-minute bars, rolling ATM-relative option OHLC proxies, technical features, training-only candidate fitness, validation-based finalist selection and one-time OOS inference. The search budget was 1,200; 1,185 unique candidates were archived and 20 finalists selected. Twelve passed the defined statistical gate after Holm correction. Costs included 50 basis points adverse slippage per side and ₹10 brokerage per order, plus modeled date-dependent charges. The cross-finalist mean of candidate daily net P&L was ₹982.54 under the base cost case, ₹287.39 at 100 bps per side and ₹20 brokerage, and −₹665.42 at 200 bps per side and ₹20 brokerage. These are simulation outputs, not realized or portfolio returns. Zero finalists passed the execution gate: the data do not establish stable dated exchange-contract identity, historical executable bid/ask/depth, queue position or actual broker fills. The appropriate conclusion is **DATA-LIMITED**, with no paper or live trading approval.

**Keywords:** NIFTY; index options; evolutionary search; multiple testing; block bootstrap; slippage; transaction costs; execution validity.

## 1. Introduction

Historical option backtests can overstate performance when rolling moneyness labels stand in for stable dated contracts or when OHLC touches are treated as executable fills. Spreads, market depth, queue position, latency and actual broker outcomes can materially affect short-horizon results. QE-NOB-2.0 was therefore designed as a bounded research experiment with separate statistical and execution gates.

### Research questions

1. Can a bounded evolutionary search produce diverse long-option candidate rules?
2. Do frozen candidates show positive modeled net outcomes on a later chronological OOS block?
3. How sensitive are results to higher assumed slippage and brokerage?
4. Does the data support execution-level profitability claims?
5. What data and tests would be required to proceed responsibly?

### Aim and objectives

**Aim:** Evaluate statistical promise and execution-data feasibility for evolutionary discovery of long NIFTY options rules.

Objectives were to restrict fitness to training data; select finalists on validation data; evaluate frozen candidates once OOS; use block-bootstrap inference and Holm correction; model costs and stress them; audit features and simulator behavior; and stop without trading approval if execution evidence is inadequate.

## 2. Methods

### 2.1 Chronological design

| Split | Dates | Use |
|---|---|---|
| Training | 2021-10-25–2024-04-29 | Candidate fitness and search |
| Validation | 2024-04-30–2025-02-24 | Select 20 frozen finalists |
| OOS | 2025-02-25–2025-12-30 | Final statistical evaluation only |

The run recorded 621 training, 207 validation and 208 OOS sessions. The OOS period was not used for evolution or manual selection. Search used 1,200 as the budget, 1,185 unique candidates, four islands and 20 generations.

### 2.2 Data and coverage

The active source probe supported Dhan's rolling WEEK option family. The cache audit found:

| Item | Result |
|---|---:|
| Cached files | 819 (25 underlying, 794 option) |
| Underlying rows | 92,891 |
| Option rows | 467,834 |
| Duplicate/conflicting duplicate groups | 0 / 0 |
| Option timestamp coverage | 99.9897% |
| Row-grid coverage | 100% |
| Historical bid/ask/depth verified | No |
| Stable dated contract identity verified | No |

The 366 expected source requests were recorded; 363 cache files were reused and three downloaded. These figures demonstrate cache/grid integrity, not stable contract identity or executable quotes. Open-dataset catalogue hits with unclear or non-allowlisted licenses were not accepted as usable replacements.

### 2.3 Features

The inspected feature builder defines:
- `nifty_return_1/3/6`: close-to-close percentage changes within an IST session.
- `opening_gap_pct`: signed (first session open minus previous observed session close) divided by previous close; not absolute gap magnitude.
- `opening_range_position`: close relative to the high-low range of the first three bars, available from bar four.
- `opening_range_break`: close above/below the frozen opening range.
- `ema_fast_slow_sign`: sign of EMA(8) minus EMA(21), with values −1, 0, +1.
- `time_of_day_bucket`: categorical time-of-session bucket.

VWAP distance was excluded because no usable values existed. Signals map to the next bar within the same IST session, and features use current/past rows. Timestamp units and exact bar-label semantics still need confirmation against source documentation.

### 2.4 Search and simulator

The grammar constrained instrument direction, expiry family, moneyness, holding period, entry predicates and exit rules. The active option universe was WEEK1 and ATM/OTM1, based on available rolling data. Candidate signatures—not island-local IDs—are the reliable archive join key.

The simulator repriced trades for slippage, brokerage and modeled statutory/exchange charges. Stop/target logic uses OHLC proxy ranges; stop is checked before target when both are touched. Repeated rules of the same exit kind are reduced to the minimum threshold. These are simulation conventions, not observed fills.

### 2.5 Costs and inference

Primary costs: 50 bps adverse slippage per side and ₹10 brokerage per order. Stress grid: 0, 25, 50, 100, 200 bps per side × ₹10 or ₹20 brokerage. Statutory and exchange fees were modeled using date-dependent assumptions and require official and broker-tariff reconciliation.

OOS inference used 5,000 moving-block bootstrap replicates, five-session block length, Holm correction and alpha 0.05. Multiple-testing correction does not repair contract-identity mismatch or unrealistic fills. The execution gate was separate and mandatory.

## 3. Results

### 3.1 Gate summary

| Measure | Result |
|---|---:|
| Search budget | 1,200 |
| Unique candidate signatures | 1,185 |
| Frozen finalists | 20 |
| Passed statistical gate after Holm correction | 12 |
| Passed execution gate | 0 |
| Cost stress rows | 200 |

All 20 finalist signatures resolve to exactly one archive record. An earlier missing-rule diagnosis caused by joining on island-local IDs was withdrawn and recorded in the error log.

### 3.2 Twelve statistical-gate candidates

Daily mean and confidence intervals are modeled rupees under the primary cost assumptions. All candidates still failed the execution gate.

| Candidate | Side | OOS trades | Mean daily net ₹ | 95% CI ₹ | Holm p | Mean daily at 100 bps/side, ₹20 brokerage ₹ |
|---:|---|---:|---:|---:|---:|---:|
| 1008 | CALL | 1,551 | 1,024.18 | 626.72–1,449.46 | 0.003999 | 594.86 |
| 1163 | CALL | 1,207 | 894.82 | 542.68–1,265.98 | 0.003999 | 561.48 |
| 799 | CALL | 3,399 | 1,865.98 | 1,386.36–2,508.05 | 0.003999 | 525.43 |
| 1048 | PUT | 1,077 | 734.87 | 443.61–1,074.40 | 0.003999 | 343.43 |
| 398 | CALL | 1,698 | 1,014.52 | 631.71–1,395.20 | 0.003999 | 601.40 |
| 496 | PUT | 522 | 1,450.80 | 1,024.99–1,882.39 | 0.003999 | 1,259.64 |
| 386 | CALL | 1,087 | 1,210.24 | 789.95–1,717.41 | 0.003999 | 767.82 |
| 78 | CALL | 540 | 1,150.66 | 842.13–1,548.80 | 0.003999 | 924.00 |
| 705 | CALL | 767 | 560.41 | 209.78–949.46 | 0.007598 | 233.05 |
| 264 | PUT | 260 | 1,158.22 | 924.19–1,375.79 | 0.003999 | 1,076.16 |
| 814 | CALL | 2,141 | 1,519.20 | 1,080.10–2,026.68 | 0.003999 | 989.97 |
| 936 | CALL | 1,430 | 969.69 | 590.62–1,352.98 | 0.003999 | 603.43 |

Full predicates and exits are recorded in [EXACT_FINALIST_RULES.md](EXACT_FINALIST_RULES.md). These values are simulation outputs, not realized returns.

### 3.3 Cost sensitivity

Across the 20 finalists, the mean of candidate-level daily means declined as modeled costs increased.

| Slippage per side | Brokerage/order | Mean ₹/day | Median ₹/day | Min ₹/day | Max ₹/day |
|---:|---:|---:|---:|---:|---:|
| 0 bps | ₹10 | 1,458.95 | 1,296.78 | 338.14 | 3,103.12 |
| 0 bps | ₹20 | 1,240.21 | 1,147.48 | 228.08 | 2,435.21 |
| 25 bps | ₹10 | 1,220.75 | 1,167.67 | 241.45 | 2,343.42 |
| 25 bps | ₹20 | 1,002.00 | 958.34 | 131.39 | 1,957.77 |
| 50 bps | ₹10 | 982.54 | 997.04 | 144.76 | 1,865.98 |
| 50 bps | ₹20 | 763.80 | 754.31 | 34.71 | 1,480.32 |
| 100 bps | ₹10 | 506.13 | 582.03 | −199.23 | 1,318.87 |
| 100 bps | ₹20 | 287.39 | 434.43 | −900.43 | 1,259.64 |
| 200 bps | ₹10 | −446.68 | −116.73 | −3,501.59 | 1,055.02 |
| 200 bps | ₹20 | −665.42 | −221.34 | −4,202.78 | 995.79 |

At 200 bps per side and ₹20 brokerage, 9 of 20 candidates retained positive modeled daily means. This does not validate actual execution costs. Finalist averages are descriptive summaries across alternative selected candidates, not a deployable combined portfolio estimate.

**Figure 1 — Average modeled daily mean sensitivity**

```text
0 bps / ₹10      +₹1,459  ███████████████
25 bps / ₹10     +₹1,221  ████████████
50 bps / ₹10       +₹983  ██████████
100 bps / ₹10      +₹506  █████
100 bps / ₹20      +₹287  ███
200 bps / ₹10      −₹447  ◀████
200 bps / ₹20      −₹665  ◀███████
```

### 3.4 Interpreting candidate rules

Because the gap feature is signed, `opening_gap_pct < 0.0025` includes negative gaps and positive gaps below +0.25%; it is not an absolute-gap filter. Likewise, `ema_fast_slow_sign > -1` admits neutral and positive EMA signs. Candidate 496's PUT condition after positive six-bar return is a discovered empirical pattern, not a causal explanation.

## 4. Discussion

### Supported conclusions

The bounded search produced candidates that passed the defined OOS statistical screen. Chronological splits, validation-only selection, block-bootstrap inference, Holm correction, cost stress, signature-based candidate extraction and source-level feature review are useful controls. The inspected feature formulas and next-bar mapping showed no obvious look-ahead defect, although this is not a complete independent proof.

### Unsupported conclusions

The results do not establish executable profitability. Rolling ATM-relative bars may represent different actual contracts as spot changes. Exact expiry/strike continuity, historical bid/ask/depth, queue priority, latency and broker fills were not verified. OHLC threshold touches are not guaranteed fills. The stop-first convention is conservative for overlapping stop/target bars but cannot reconstruct the true intrabar path.

Statistical significance is conditional on the simulator and data representation. It cannot correct structural proxy bias. Modeled fees and lot sizes must be reconciled against official dated contract metadata and Paytm Money's actual tariff. The discovery process also creates selection risk beyond a single final p-value; results should not be generalized to unseen regimes without a fresh untouched evaluation.

### Source feasibility

The bounded source probe confirmed that Dhan's rolling WEEK option source was accessible for this run. It did not establish that a compatible public historical source supplies stable contract IDs and executable quotes. Catalogue entries with unclear or non-allowlisted licenses were not treated as approved data. This is an unresolved feasibility result, not proof that no such source exists anywhere.

## 5. Strengths

1. Chronological training, validation and OOS partitions.
2. Finite search budget and frozen finalist list.
3. Block-bootstrap inference and Holm correction.
4. Explicit brokerage, slippage and statutory-fee assumptions.
5. Ten cost scenarios for every finalist.
6. Candidate archive, source/cache audit, sanitized trade ledger, stress grid, status and error log retained.
7. Statistical and execution gates are separate; significance alone cannot authorize trading.

## 6. Limitations

1. Rolling moneyness does not establish stable dated contract identity.
2. Historical executable bid/ask/depth, queue position and broker fills are absent.
3. OHLC fills are proxy assumptions.
4. Fees and lot-size assumptions need dated official and broker reconciliation.
5. Global leads, India VIX, verified IV surface/skew, FII/DII publication timing and timestamped events were not present in the active grammar.
6. Source timestamp and bar-label semantics remain incompletely verified.
7. Candidate selection and grammar introduce multiple-testing and specification risk.
8. No independent tester branch/report was created, per the explicit project instruction.
9. No forward or live execution study was conducted.
10. Candidate-level averages are not a combined portfolio result.

## 7. Conclusion

QE-NOB-2.0 completed bounded discovery and statistical screening. Twelve of twenty finalists passed the statistical gate after Holm correction, but none passed the execution gate. Modeled outcomes weaken under higher assumed costs, and current rolling option data do not establish stable contract identity or executable historical prices.

**Final decision: DATA-LIMITED. No candidate is approved for paper or live trading.** Retain these candidates as hypotheses only; do not claim robust or executable profitability.

## 8. Future research and stopping rule

1. Verify whether Dhan or an official/free source supplies stable instrument IDs, exact dated expiry/strike history and contemporaneous bid/ask quotes.
2. Reconcile dated lot sizes, expiry rules, exchange charges and Paytm Money fees.
3. If quote data are available, replay orders against contemporaneous bid/ask with conservative latency and marketability assumptions.
4. Require independent reproduction of extraction, formulas, costs, gates and tables before forward testing.
5. Only after data/execution gates pass, preregister a new untouched OOS or forward period. Never tune on the current OOS block.
6. Add India VIX, global leads, IV/OI, FII/DII and news/event features only when source provenance, publication timing, license and missingness are verified.
7. If contract-level executable data cannot be obtained within a predefined bounded feasibility phase, close the workstream rather than repeatedly searching or optimizing the same proxy.

## 9. Reproducibility and supplementary material

- [Exact finalist rules](EXACT_FINALIST_RULES.md)
- [Simulator and feature audit](SIMULATOR_FEATURE_AUDIT.md)
- [Artifact integrity and decision](ARTIFACT_INTEGRITY_DECISION.md)
- [Phase status](PHASE_STATUS.md)
- [Error log](ERROR_LOG.md)
- [Workflow run #39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143)
- [Workflow artifact ID 12464009881](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143/artifacts/12464009881)

The workflow artifact contains candidate archive, training/validation/OOS metrics, 200-row cost stress grid, sanitized trade ledger, feature availability, acquisition summary, source failures and run summary.

### Appendix A. Gate definitions

- **Statistical gate:** predeclared OOS inference criteria including block-bootstrap and Holm adjustment.
- **Execution gate:** data establish reliable dated contract identity and executable historical pricing. It failed for all finalists.
- **Overall decision:** execution gate is mandatory; statistical significance cannot override its failure.

### Appendix B. Simulator conventions

Entries map to the next bar within the same IST session. Long-option trades are repriced for configured slippage, brokerage and modeled statutory/exchange charges. OHLC stop/target thresholds are proxies, with stop checked before target. Duplicate exit rules of the same kind reduce to the minimum threshold. The simulator leaves execution gate false because rolling data do not prove stable contract identity.

### Appendix C. Error correction history

The initial candidate-archive diagnosis incorrectly joined on island-local candidate IDs and suggested missing finalist rules. It was withdrawn: the archive contains 1,185 unique signatures and all 20 finalists match exactly one definition by signature. See [ERROR_LOG.md](ERROR_LOG.md).

### Appendix D. Scope exclusions

This is the QE-NOB-2.0 long-option discovery study, not a NIFTY cash-index prediction study and not a trading recommendation. No result is a forecast or guarantee.
