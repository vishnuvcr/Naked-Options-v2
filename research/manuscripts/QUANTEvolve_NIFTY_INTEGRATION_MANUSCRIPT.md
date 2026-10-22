# QuantEvolve Integration for NIFTY 50 Prediction and Options Strategy Discovery

**Protocol:** QE-NIFTY-1.0  
**Repository branch:** `research/quantevolve-integration`  
**Disposition date:** 2026-10-22  
**Study status:** **INCONCLUSIVE / BLOCKED AT LLM AND OPTIONS-DATA GATES**  
**Trading recommendation:** None. No options P&L was run and no trading strategy is approved.

## Abstract

This study integrated the pinned QuantEvolve evolutionary quantitative-research framework into Naked-Options-v2 while preserving the repository's prior research results and data-quality gates. The research was separated into (1) NIFTY 50 next-session return prediction and (2) NIFTY index-options strategy discovery. The prediction adapter uses a declarative, allowlisted strategy specification, point-in-time features, chronological development folds, a frozen final 20% holdout, a zero-return baseline, and a circular block-bootstrap interval for MAE improvement. Candidate source is parsed as a literal specification rather than executed as arbitrary generated Python.

The validated Dhan daily series contained 4,905 rows from 2007-01-02 through 2026-10-19. Two early bounded four-iteration controller runs saved an all-zero forecast specification, whose holdout MAE equaled the zero-return baseline (0.00580346; MAE skill 0; 95% block-bootstrap interval for MAE improvement [0, 0]). Those runs did not include provider-call telemetry, so successful LLM mutation cannot be established. A subsequent telemetry-enabled four-iteration run recorded four failed Gemini requests (three timeouts and one server error), and a one-iteration fallback using Gemini 3.6 Flash recorded one server error. Neither run generated a verified successful response; no candidate was scored in either run. Therefore, the prediction evidence is insufficient to conclude that evolutionary search itself is effective or ineffective.

For options, a bounded audit downloaded three expiry-partitioned files from the public `thetrademarkk/india-index-options-1m` dataset (986,041 rows; 8.82 MB). The sampled schema contains timestamp, OHLCV, open interest, symbol, strike, option type and expiry, but no lot-size field. A separate single-call Dhan probe returned 1,155 structurally aligned one-minute observations from 3–5 August 2026; the response had no explicit expiry or lot-size field and included six distinct strike values, consistent with rolling ATM-relative data rather than a fixed contract ledger. NSE circulars map lot sizes for the three sampled expiry cohorts (75, 50 and 65), and row-level expiry/strike/type/symbol checks passed in those three files. However, complete row-by-row official MII contract-master reconciliation and full-history lot-size mapping remain unverified. The HF dataset is CC-BY-NC-4.0, and both sources contain OHLC rather than historical executable bid/ask quotes. Coverage, conflicting duplicates and executable pricing remain unverified; the options gate stays blocked and no P&L was calculated. The result is a reproducible integration scaffold and documented inconclusive research, not a profitable strategy.

## 1. Research questions

1. Can QuantEvolve be adapted to NIFTY 50 forecasting without changing existing study outcomes, compromising the final holdout, or executing arbitrary LLM-generated code?
2. Did the bounded controller produce a verified successful Gemini mutation and a candidate that improves on the zero-return forecast?
3. Can free NIFTY option-bar data be reconciled to official contract identity, expiry, and historically applicable lot size?
4. Is there enough verified data to proceed to a realistic options backtest with transaction charges and slippage?
5. Which phases are supported by evidence, and which must remain blocked?

## 2. Aims and objectives

### Aim

Establish a safe, reproducible and finite integration of QuantEvolve for separate NIFTY prediction and NIFTY-options research tracks.

### Objectives

- Pin upstream QuantEvolve to commit `2df1e85758620e8ac0ca88ffc428b379d6cb9620`.
- Preserve the prior NIFTY-PRED and options-study results; write new results to the integration branch.
- Validate target data and retain reusable data cache with source and content hashes.
- Use a bounded evolution budget, a development-only fitness function, and an untouched final holdout.
- Record sanitized LLM attempt/success/failure counters without logging prompts, responses, API keys, or raw provider error text.
- Audit a bounded sample of free options data and preserve license/attribution constraints.
- Do not calculate options P&L until the source/contract gate passes.
- Publish manifests, results, status, errors, and a complete manuscript.

## 3. Literature and source review

This is an implementation-focused evidence review rather than a claim of exhaustive coverage of all quantitative-finance literature.

### 3.1 QuantEvolve and the upstream implementation

The public [QuantEvolve repository](https://github.com/tarsyang/quantevolve) describes an evolutionary LLM loop for quantitative strategy development. Its pinned implementation is configurable for iterations, model provider, candidate program, evaluator and output directory. Its upstream defaults and documented examples are crypto/Binance-oriented; they cannot be treated as an NSE index-options evaluator without an adapter. The integration therefore supplies a NIFTY-specific evaluator and a restricted declarative specification, and does not use the upstream evaluator unchanged.

### 3.2 NIFTY data and forecast evaluation

The existing repository's NIFTY-PRED study and its previous literature review remain the prior evidence base. The relevant statistical principles retained here are chronological splitting, point-in-time features, baseline comparison, block-bootstrap uncertainty, and separation of forecast accuracy from trading profitability. A single held-out candidate does not establish general superiority; an evolutionary search also creates a multiple-testing problem that must be controlled before confirmatory claims.

### 3.3 Options data and contract sources

The public [Hugging Face dataset card](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m) describes 1-minute index/option OHLCV data, including NIFTY options partitioned by expiry. It is licensed **CC-BY-NC-4.0**, and the card cautions that coverage is partial and should be verified against official exchange data. The sampled files contain OHLC bars but no lot-size column.

The [NSE All Reports page](https://www.nseindia.com/all-reports-derivatives) lists F&O-MII contract files and UDiFF bhavcopy reports. NSE's [NIFTY 50 F&O information](https://betanseapi.nseindia.com/static/products-services/equity-derivatives-nifty50) says permitted lot size is governed by exchange rules and points to the daily contract file. Exchange circulars also document effective-date-specific contract/lot-size changes (for example, [NSE circular FAOP70616](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf)). The reviewed NSE circulars support expiry-cohort lot sizes of 75 for 27 May 2021, 50 for 4 January 2024, and 65 for 4 August 2026, and the sampled files' dates and expiry weekdays are internally consistent. This only maps the three sampled cohorts; row-by-row official MII contract-master matching for every contract and the full historical series has not been completed.

## 4. Data

### 4.1 Prediction dataset

| Field | Verified value |
|---|---|
| Source | Dhan daily NIFTY series |
| Rows | 4,905 |
| First date | 2007-01-02 |
| Last date | 2026-10-19 |
| SHA-256 | `66e06c7fd4affcf8753e68046b311b8cfe27cb292af93691d2ee63787381629c` |
| Development portion | 3,924 rows (first 80%) |
| Final chronological holdout | 981 targets |
| Holdout target dates | 2022-11-04 to 2026-10-19 |

The final holdout was not used for candidate selection in the reports that were successfully evaluated. All feature construction is intended to use past observations only.

### 4.2 Options source audit

The bounded source audit selected the earliest, near-2024, and latest dated NIFTY option-expiry files available in the public dataset at audit time.

| Expiry partition | Rows | Download bytes | Lot size field |
|---|---:|---:|---|
| 2021-05-27 | 333,365 | 3,624,537 | Absent |
| 2024-01-04 | 650,030 | 5,139,509 | Absent |
| 2026-08-04 | 2,646 | 58,248 | Absent |
| **Total** | **986,041** | **8,822,294** | **Absent in all three** |

The timestamp type in each sampled file is `timestamp[ns, tz=+05:30]`. The union of columns is `timestamp, open, high, low, close, volume, open_interest, trading_day, symbol, strike, option_type, expiry`.

Per-file hashes and source metadata are in [options_source_audit.json](../../reports/quantevolve/options_source_audit.json). Raw licensed parquet files are cached in the workflow runtime/cache only and are not committed to the repository.

**Unverified options data requirements:** row-by-row official MII contract-master matching across the full source history; full-history lot-size/contract continuity; at least 80% eligible-date coverage; no more than 1% conflicting duplicate groups; and executable-side pricing. Circular lot-size mapping and row-level structural checks passed for only the three sampled expiry files. These limited checks do not open the gate, and thresholds were not relaxed.

## 5. Scientific methodology

### 5.1 Prediction target and candidate grammar

The prediction track targets the next-session NIFTY log return. Candidate specifications are restricted to one literal `STRATEGY_SPEC` assignment with allowlisted features, bounded coefficients/intercept, a fixed model family and a bounded output clip. The evaluator uses AST parsing and literal evaluation; it never imports or executes candidate source. Candidate evaluation strips the Google API key and acquisition secrets from child processes.

### 5.2 Development and holdout protocol

- First 80% of the daily history is the development set.
- Candidate fitness is calculated over three chronological development folds.
- The final 20% is evaluated once after candidate selection and is not used in prompts or fitness.
- The naive baseline predicts zero next-session return.
- Forecast metrics include MAE, RMSE, MAE skill against zero, directional accuracy where defined, and directional prediction coverage.
- A circular block bootstrap with block length 10 and 1,000 repetitions estimates the 95% interval for MAE improvement.
- When the candidate predicts zero for every observation, directional accuracy is reported as undefined, with 0% directional coverage—not as an artificial direction score.

The bounded run budget is at most four evolution iterations. API retries are not open-ended: the diagnostic sequence stopped after four failed calls on Gemini 3.8 Flash and one failed call on Gemini 3.6 Flash. The repository run request is now offline by default.

### 5.3 Options gate

The options track requires a provenance manifest and normalized rows with timestamp, expiry, strike, option type, OHLCV, and lot size. The gate checks source hash, official-expiry reconciliation, historical lot-size verification, license/use review, timezone, explicit pricing policy, invalid rows, duplicate conflicts, and eligible-session coverage. Passing the gate would permit only a subsequent research backtest; it would not establish profitability.

No options P&L is computed because the HF source's lot-size column is absent, Dhan's rolling response omits explicit expiry and lot-size fields, full-history official contract-master reconciliation and coverage are not verified, and OHLC bars do not establish bid/ask execution. Any later strategy study must include Paytm Money brokerage and applicable statutory/exchange charges, adverse slippage/spread sensitivity, missed fills, drawdown, tail loss, turnover, and no-trade baselines.

## 6. Results

### 6.1 Forecast report results

| Run | LLM telemetry | Selected specification | Holdout MAE | Zero baseline MAE | MAE skill | Disposition |
|---|---|---|---:|---:|---:|---|
| [39665689785](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665689785) | Not recorded | All weights/intercept zero | 0.00580346 | 0.00580346 | 0.000000 | Evaluated; no improvement |
| [39667156299](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39667156299) | Not recorded | All weights/intercept zero | 0.00580346 | 0.00580346 | 0.000000 | Evaluated; no improvement |
| [39668183031](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668183031) | 4 attempts; 0 success; 3 timeouts; 1 server error | None scored | N/A | N/A | N/A | Blocked before candidate scoring |
| [39669107291](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669107291) | 1 attempt; 0 success; 1 server error | None scored | N/A | N/A | N/A | Blocked before candidate scoring |

For the two evaluated all-zero specifications:

- Holdout sample size: 981.
- Holdout MAE: 0.005803462563991722.
- Holdout RMSE: 0.007963864496866901.
- Zero-baseline MAE: 0.005803462563991722.
- MAE skill versus baseline: 0.
- 95% circular block-bootstrap interval for MAE improvement: [0, 0].
- Directional accuracy: undefined because no non-zero direction was predicted.
- Directional prediction coverage: 0%.

The result is visually identical for candidate and baseline:

```text
Holdout MAE
All-zero specification  0.00580346
Zero-return baseline     0.00580346
MAE improvement          0.00000000
```

**Interpretation:** the saved all-zero specification did not improve on the zero-return baseline. Because provider-call telemetry was absent in the first two runs, they do not prove that a valid LLM mutation occurred. The telemetry-enabled runs subsequently established zero successful generation responses, so they provide no additional candidate performance result. It would be incorrect to attribute the first two results confidently to successful evolutionary search.

### 6.2 Options source gate

| Gate | Result |
|---|---|
| Public sample files obtained | 3 |
| Sample rows | 986,041 |
| Required option identity and OHLCV fields present | Yes in sampled schema |
| Lot-size field present in sampled HF schema | No |
| NSE circular lot-size mapping for the three sampled expiry cohorts | 75 / 50 / 65 (mapped) |
| Row-by-row official MII contract-master reconciliation for all sampled contracts | No — incomplete |
| Explicit expiry and lot-size fields in the Dhan rolling probe | No |
| Bid/ask quotes available from sample | No |
| Full eligible-date coverage measured | No |
| P&L permitted | **No** |
| Status | `BLOCKED_FULL_HISTORY_AND_OFFICIAL_CONTRACT_MASTER_RECONCILIATION` |

The Dhan probe shows that minute-level data can be retrieved, and the HF sample supports circular-backed lot sizes for three expiries. It does not identify a stable expiry-specific, lot-sized tradeable contract stream across the historical period. The options gate remains `BLOCKED_NO_VERIFIED_CONTRACT_DATA`. This is a data-readiness result, not a negative profitability test.

### 6.3 Dhan API probe and sample lot-size reconciliation

The sanitized Dhan call used `expiryFlag=WEEK`, `expiryCode=1` (Next Expiry), `strike=ATM`, `drvOptionType=CALL`, `interval=1`, and the 2026-08-03 to 2026-08-05 window. It returned HTTP 200 and 1,155 time points. Every requested field (OHLC, volume, IV, strike, OI, spot) had 1,155 values; timestamps were monotonic from 09:15 IST on 3 August to 15:39 IST on 5 August 2026. Close ranged from 9.7 to 192.5 and six strike values were present (24,450–24,750). The output saved to the repository contains aggregates only, not raw market rows or credentials.

| Dhan probe check | Result |
|---|---|
| HTTP response | 200 |
| Observations | 1,155 |
| Required array lengths aligned | Yes |
| Timestamps monotonic | Yes |
| Explicit expiry in response | No |
| Row-level lot size | No |
| Fixed-contract ledger established | No |
| P&L permitted | **No** |

NSE circular-based lot-size mapping and row-level source-file checks for the three HF expiry partitions:

| Sampled expiry | Circular-backed lot size | Row-level expiry/strike/type/symbol checks |
|---|---:|---|
| 2021-05-27 | 75 | Pass |
| 2024-01-04 | 50 | Pass |
| 2026-08-04 | 65 | Pass |

These two acquisitions are complementary, but neither yields a full point-in-time contract ledger. The HF dataset is not an executable quote feed, the Dhan ATM-relative series has no explicit expiry/lot fields, and full official MII contract-master reconciliation plus full-history coverage and duplicate checks remain outstanding.

### 6.3 Integration and automated checks

- The upstream repository is pinned to a fixed revision and is not fetched from moving `main` for the experiment.
- Automated governance tests passed after correcting the telemetry test's dependency isolation.
- A bounded options-source audit was added to the options track; it samples at most three expiry files and publishes only sanitized metadata.
- The publisher allowlist was extended to include `options_source_audit.json`; raw CC-BY-NC parquet is not published.
- Gemini telemetry stores only model identifier, attempt/success/failure counts, and exception classes; no prompts, responses, key, or raw provider error text are saved.
- The run request is `run_llm=false` by default to prevent automatic API spend.

## 7. Statistical analysis and inferences

### Prediction

For the two saved all-zero forecasts, MAE improvement over the zero-return baseline is exactly zero. The reported 95% block-bootstrap interval is [0, 0], reflecting identical predictions to the baseline, not a general statement that all possible predictors have zero skill. No adjusted significance claim is made because no valid evolutionary candidate family with verified LLM mutations was produced and evaluated. Directional accuracy is undefined at zero prediction coverage.

The study therefore cannot answer whether a functioning QuantEvolve search adds predictive value. It establishes only that the evaluated all-zero specification is no better than the naive baseline and that the current API path did not return a successful candidate-generation response in the bounded diagnostics.

### Options

No inferential P&L statistics are appropriate because the verified contract/lot-size gate did not pass. Coverage, duplicate-conflict rate, fees, slippage, drawdown, net return and confidence intervals were not estimated. Treating the OHLC sample as an executable trade ledger would be unsupported.

## 8. Discussion

The integration has made the research pipeline more reproducible and safer: upstream code is pinned, candidate source is restricted to a declarative grammar, holdout use is guarded, reports are hashed, LLM calls are counted without exposing sensitive text, and raw licensed data is kept out of public artifacts. These are infrastructure outcomes, not evidence of alpha.

Two distinct blockers remain for any strategy conclusion. First, Gemini generation calls failed in five bounded attempts across two model identifiers; the finite diagnostic stopped rather than looping or spending more quota. Second, free options data is reachable, but the HF sample has no lot-size field and only three expiry cohorts have circular-backed lot-size mappings; Dhan returned a rolling ATM-relative series with no explicit expiry or lot-size identifier. Full official contract-master matching, full-history coverage, duplicate checks and executable pricing are unverified. The existing gate appropriately prevents P&L from being calculated.

The integration should not be promoted as a usable prediction engine or trading strategy. The prior repository's historical no-go results remain unchanged and are not superseded by these integration diagnostics.

## 9. Strengths

- Existing research results and quality thresholds are preserved.
- Pinned upstream revision, bounded iteration budget, seed/config hashes, and run manifests support reproducibility.
- Chronological development folds and a frozen final holdout reduce look-ahead risk.
- Declarative AST-parsed candidate grammar avoids arbitrary generated-code execution.
- Baseline, MAE skill, block-bootstrap interval, and directional coverage are reported.
- API failures are explicitly logged and do not become fabricated performance claims.
- Raw CC-BY-NC dataset files are not committed or published.
- Options P&L is blocked until contract, lot-size, coverage, duplicate and pricing gates pass.

## 10. Limitations

- Gemini generation produced zero successful responses in the bounded diagnostics; a functioning evolutionary candidate has not been verified.
- The first two evaluated all-zero specifications lack provider telemetry and cannot be attributed confidently to successful LLM mutation.
- Only one selected declarative specification was evaluated in each of the two report-producing runs.
- The options audit samples three expiry files, not the entire source history.
- Official expiry reconciliation, historical lot size, full coverage, duplicate rate, and bid/ask/executable prices remain unverified.
- No options strategy backtest, Paytm Money charge model, or trading P&L was run.
- Dataset CC-BY-NC-4.0 limits commercial use and redistribution; license and attribution conditions must remain explicit.
- The study does not establish that all NIFTY prediction models are ineffective. The options source checks establish only a three-expiry lot-size mapping and a successful sample request to Dhan, not a valid backtest dataset.

## 11. Conclusion

**Final disposition: INCONCLUSIVE / BLOCKED; no strategy approved.**

The integration shell and automated gates are operational. The two saved all-zero forecast reports show no improvement over the zero-return baseline, but the available telemetry does not establish successful LLM mutation in those runs. Later bounded diagnostics recorded five failed generation requests and zero successes, so no verified evolutionary candidate could be scored. The options data audit confirms that useful historical NIFTY option bars exist in a free public source, but the sampled schema lacks lot size and official contract reconciliation remains incomplete. Consequently, options P&L and strategy discovery must remain blocked.

No prediction edge, profitable strategy, or live-trading readiness is claimed. Prior NIFTY-PRED and options results remain preserved.

## 12. Future research directions

1. **API availability:** when explicitly authorized, verify Google AI Studio/API project access, quota, billing and regional/service availability outside the research runner; retain sanitized HTTP status classes in telemetry if the provider exposes them. Do not retry automatically.
2. **Candidate generation:** after API access is verified, run one explicitly dispatched, capped experiment and require at least one successful response plus a valid changed candidate spec before scoring.
3. **Official contract mapping:** acquire NSE daily F&O-MII contract files and relevant circulars for representative expiry dates, parse NIFTY contracts, and reconcile expiry/strike/type/lot size against the HF sample.
4. **Data coverage:** expand from three samples to a bounded, cached history; measure eligible-date coverage, conflicting duplicates, missing bars, fixed-contract continuity, and expiry-day treatment.
5. **Execution realism:** source historical bid/ask or trades if lawfully available. If only OHLC is available, use a preregistered adverse-price proxy and mark the limitation clearly.
6. **Costs:** implement date-effective Paytm Money brokerage and applicable statutory/exchange charges, plus adverse slippage/spread scenarios before strategy search.
7. **Prediction research:** only after valid LLM mutations are verified, compare a preregistered candidate family against frozen naive and existing baselines, account for search multiplicity, and evaluate the final holdout once.
8. **Closure:** follow the finite P0-P6 plan. If the API or contract data gates cannot be passed, close the relevant phase as blocked and do not continue an unbounded search.

## Appendix A. Reproducibility manifest

- Protocol: `QE-NIFTY-1.0`
- Upstream: [tarsyang/quantevolve](https://github.com/tarsyang/quantevolve)
- Pinned upstream revision: `2df1e85758620e8ac0ca88ffc428b379d6cb9620`
- Prediction data SHA-256: `66e06c7fd4affcf8753e68046b311b8cfe27cb292af93691d2ee63787381629c`
- Options sample-hash manifest: `b8b433c5f76e62bbe262dfa39bed83d2a454f56a0152c411d8f0bd14bc1e0073`
- Options report: [options_source_audit.json](../../reports/quantevolve/options_source_audit.json)
- Options gate: [options_data_gate.json](../../reports/quantevolve/options_data_gate.json)
- Prediction reports: [run 39667156299](../../reports/quantevolve/prediction/run-39667156299/run_manifest.json)
- Failed LLM diagnostics: [run 39668183031](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668183031), [run 39669107291](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669107291)
- Phase status: [QUANTEvolve_INTEGRATION_STATUS.md](../QUANTEvolve_INTEGRATION_STATUS.md)
- Error log: [QUANTEvolve_INTEGRATION_ERROR_LOG.md](../QUANTEvolve_INTEGRATION_ERROR_LOG.md)
- Experiment log: [EXPERIMENT_LOG.md](../EXPERIMENT_LOG.md)

## Appendix B. Frozen quality gates

- Daily target history: at least 500 rows; exact data hash must match acquisition and validation manifests.
- Prediction: chronological development-only fitness; final holdout excluded from selection; directional accuracy undefined when directional coverage is zero.
- Options: at least 80% eligible-date coverage; at most 1% conflicting duplicate groups; exact expiry/strike/type/timestamp and historical lot-size mapping; source license and provenance reviewed; executable-price policy declared.
- Candidate execution: generated Python source is never executed; only validated declarative specifications are evaluated.
- API: maximum four iterations per regular experiment; bounded one-iteration fallback diagnostic completed; no further automatic API retries.
- Reporting: no P&L or profitability claims without verified contract data, realistic fees/slippage, and out-of-sample evidence.

## Appendix C. Key references

1. QuantEvolve upstream repository and license: https://github.com/tarsyang/quantevolve
2. Hugging Face dataset card and license: https://huggingface.co/datasets/thetrademarkk/india-index-options-1m
3. NSE All Reports / F&O-MII contract files: https://www.nseindia.com/all-reports-derivatives
4. NSE NIFTY 50 F&O contract information: https://betanseapi.nseindia.com/static/products-services/equity-derivatives-nifty50
5. NSE contract/lot-size circular: https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf
6. Google Gemini API model list: https://ai.google.dev/gemini-api/docs/models


## Supplemental result — Dhan expired-options API probe (bounded, 22 October 2026)

A single request to Dhan's rolling expired-options endpoint was used to test whether the existing subscription could supply a contract-identified historical series. The request returned HTTP 200 and 1,155 one-minute bars between 3 August 2026 09:15 IST and 5 August 2026 15:39 IST. The response included aligned OHLC, volume, IV, OI, strike, spot and timestamp arrays, with six distinct strikes. The sanitized report is stored at `reports/quantevolve/dhan_options_api_probe.json`.

This is a source-availability result, not a strategy result. The response did not expose a row-level expiry or lot-size field. Because the endpoint returns a rolling ATM class, continuity of a single option contract cannot be inferred. OHLC prices also do not establish executable bid/ask fills. Consequently, the options data gate remains `BLOCKED_NO_VERIFIED_CONTRACT_DATA`; no options P&L, ranking or live recommendation is reported.

The independent bounded HF source audit covers three expiry files and 986,041 rows. Those sampled files passed row-level expiry/strike/type/symbol checks and were mapped to NSE circular-backed lot sizes of 75, 50 and 65 for the sampled cohorts. This limited sample does not demonstrate full-history coverage or complete official MII contract-master reconciliation. Further research should acquire a source with stable contract identifiers and historical lot-size records, then reconcile all expiries against official exchange masters before implementing a cost- and slippage-aware backtest.
