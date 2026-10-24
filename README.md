# NIFTY 50 prediction — current research status

## Replacement track started — 2026-10-25

The user directed that ZigZag testing should not delay broader NIFTY prediction research. ZigZag-specific scoring is therefore parked as a non-blocking side study. A new daily next-session direction benchmark has been added using free-source daily NIFTY 50 data and leakage-controlled chronological evaluation.

- [Replacement research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Phase status](research/nifty-prediction/PHASE_STATUS.md)
- [Structured research manuscript (results pending)](research/nifty-prediction/MANUSCRIPT.md)
- [Targeted literature review](docs/research-literature/nifty_prediction_literature_review.md)
- [Repository integration plan for Quantevolve, TradingAgents, astra-quant-agent, PySR, arch, tick and MAPIE](research/nifty-prediction/REPOSITORY_INTEGRATION.md)
- [Daily data acquisition](research/nifty-prediction/acquire_daily_data.py)
- [Walk-forward model benchmark](research/nifty-prediction/evaluate_daily_models.py)
- [Two-source OHLC parity audit](research/nifty-prediction/audit_source_parity.py)
- [Benchmark tests](tests/test_nifty_prediction_benchmark.py)
- [Error log](research/nifty-prediction/ERROR_LOG.md)
- [Preliminary historical diagnostic results](reports/nifty-prediction/preliminary_historical_diagnostic.md)
- [Preliminary balanced-accuracy chart](reports/nifty-prediction/preliminary_balanced_accuracy.svg)
- [Automated workflow](.github/workflows/nifty-prediction-benchmark.yml)

Models currently specified: majority-class, previous-direction and zero-return baselines, logistic regression, random forest and histogram gradient boosting. Primary metric is balanced accuracy with chronological holdout and block-bootstrap uncertainty. ARCH/MAPIE package checks are optional workflow steps; GARCH, MAPIE, PySR and agent-framework integrations are not yet empirical results.

**Current evidence status (2026-10-25):** a preliminary historical diagnostic is now recorded for a third-party daily CSV mirror (2000–2019). On a chronological 2014–2019 holdout, custom logistic regression achieved 52.78% balanced accuracy versus 52.60% for previous-session direction; approximate block-bootstrap intervals overlap. This is not evidence of a robust edge, does not cover current market conditions, and is not the production scikit-learn benchmark. A fresh-cache check and free public-parquet fallback are now implemented for the primary workflow. Its actual run artifact remains unverified; no model winner or trading strategy is reported. See [preliminary results](reports/nifty-prediction/preliminary_historical_diagnostic.md) and [literature review](docs/research-literature/nifty_prediction_literature_review.md).

---

# ZigZag++ NIFTY 50 expiry-direction study — current status

## Latest execution status — 2026-10-25

**Scientific scoring remains blocked; no forecast observations have been scored.** A source-parity diagnostic of the previously acquired datasets found 82,451 exact five-minute timestamp overlaps. In that overlap, 94.99% of close prices differed by no more than ₹0.05, but 800 rows differed by more than ₹1 and the largest absolute close gap was ₹10.90. This is substantial agreement with material outliers, not proof that the source series are interchangeable.

A pipeline defect was found and corrected: older workflow versions reused `nifty50_5m.csv` for Dhan, Yahoo fallback, and the public archive, allowing one source to overwrite another or enter a cache under the wrong provenance. The active workflow now writes separate files for Dhan, public archive, and Yahoo fallback, quarantines the ambiguous legacy 5-minute cache with a SHA-256 record, derives 30-minute bars from a source-selected validated file, and emits [the cross-source audit](research/zigzag-expiry-direction/audit_5m_source_parity.py). A same-provider check found 6 Dhan five-minute timestamps off the expected grid and 2 OHLC mismatches among 92,696 complete aligned 1m-to-5m groups, including a 15.4-point high difference. Public archive downloads are cached and refreshed only by an explicit input. The Dhan-authentication workflow's malformed shell fragment was also repaired.

**The fixes are committed, but their new GitHub Actions run has not yet been independently inspected in this session.** Do not interpret the earlier successful acquisition run as evidence that these changes passed CI. The scientific gates remain open: exact imported `DevLucem/ZigLib/1` implementation and causal pivot timing, official date-level spot-session and weekly-expiry mapping, and vendor bar timestamp semantics. No accuracy result, winning timeframe, or strategy is claimed.

- [Cross-source parity audit](research/zigzag-expiry-direction/audit_5m_source_parity.py)
- [Legacy-cache quarantine](research/zigzag-expiry-direction/migrate_legacy_5m_cache.py)
- [Dhan source acquisition](research/zigzag-expiry-direction/acquire_dhan_timeframes.py)
- [Public archive acquisition](research/tradingagents/acquire_public_intraday_archive.py)
- [Workflow](.github/workflows/zigzag-expiry-timeframes.yml)
- [Official session and expiry protocol](research/zigzag-expiry-direction/OFFICIAL_CALENDAR_PROTOCOL.md)
- [Research manuscript](research/zigzag-expiry-direction/MANUSCRIPT.md)

- [Research plan](research/zigzag-expiry-direction/RESEARCH_PLAN.md)
- [Phase status](research/zigzag-expiry-direction/PHASE_STATUS.md)
- [Results ledger](research/zigzag-expiry-direction/RESULTS.md)
- [Error log](research/zigzag-expiry-direction/ERROR_LOG.md)
- [Interaction log](research/zigzag-expiry-direction/INTERACTION_LOG.md)

---

# ZigZag++ NIFTY 50 expiry-direction study — current status

**Updated 2026-10-25:** Data acquisition, validation, diagnostic session audit, and artifact upload succeeded in [GitHub Actions run #40128335927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927). [Artifact #12574310370](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927/artifacts/12574310370) contains 1m/5m/15m/30m/60m/daily data and validation reports. The audit found 12/5/3/0/2/0 raw OHLC anomalies by timeframe (1m through daily); raw rows were preserved. All audited files had sorted timestamps and zero duplicates. **Prediction scoring remains blocked** until official NSE session dates, Dhan bar timestamp convention, exact ZigLib v1 causal signal timing, and historical weekly expiry mapping are verified. No accuracy result exists.

- [Research plan and fixed phases](research/zigzag-expiry-direction/RESEARCH_PLAN.md)
- [Phase status and evidence](research/zigzag-expiry-direction/PHASE_STATUS.md)
- [Data acquisition and acceptance rules](research/zigzag-expiry-direction/DATA_ACQUISITION.md)
- [Timeframe sensitivity protocol](research/zigzag-expiry-direction/TIMEFRAME_SENSITIVITY.md)
- [Results ledger — no performance claim](research/zigzag-expiry-direction/RESULTS.md)
- [Error and limitation log](research/zigzag-expiry-direction/ERROR_LOG.md)
- [Interaction/decision log](research/zigzag-expiry-direction/INTERACTION_LOG.md)
- [Manuscript draft](research/zigzag-expiry-direction/MANUSCRIPT.md)
- [Latest successful data acquisition run](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927)
- [Latest acquisition artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40128335927/artifacts/12574310370)

---

# ZigZag++ NIFTY 50 expiry-direction study — current status

**Status (2026-10-25): data acquisition succeeded, but session/provenance audit and exact indicator-source verification remain incomplete. No prediction accuracy has been measured.** The acquired Dhan artifact contains 1m/5m/15m/30m/60m/daily data. An additional raw 1m audit found 511,268 rows, including 2,636 weekend-dated rows, 47,612 outside the regular session window, and 12 OHLC-inconsistent rows. These must be handled in derived data without altering the raw file. Exact DevLucem/ZigLib v1 causality and historical expiry target mapping remain hard gates; do not treat any backtest metric as valid before they pass.

- [Research plan and fixed phases](research/zigzag-expiry-direction/RESEARCH_PLAN.md)
- [Phase status and evidence](research/zigzag-expiry-direction/PHASE_STATUS.md)
- [Data acquisition and acceptance rules](research/zigzag-expiry-direction/DATA_ACQUISITION.md)
- [Timeframe sensitivity protocol](research/zigzag-expiry-direction/TIMEFRAME_SENSITIVITY.md)
- [Results ledger — no performance claim](research/zigzag-expiry-direction/RESULTS.md)
- [Error and limitation log](research/zigzag-expiry-direction/ERROR_LOG.md)
- [Interaction/decision log](research/zigzag-expiry-direction/INTERACTION_LOG.md)
- [Manuscript draft](research/zigzag-expiry-direction/MANUSCRIPT.md)
- [Successful data acquisition run](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063)
- [Acquisition artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40127255063/artifacts/12573423696)

---

# CURRENT RESEARCH TRACK — NWCP-1.0: NIFTY Weekly Candle Prediction

**Status as of 2026-10-24:** Corrective GitHub Actions [run #18](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486) completed: **14 tests passed**, 884,552 one-minute bars audited, 398 labels (224 UP / 174 DOWN), 28 features and 120 sealed test labels. The evolved rule reached 0.577 test balanced accuracy, but its reported Holm-adjusted p-value is 0.116; logistic regression reached 0.558 with a reported adjusted p-value of 0.0107. These are exploratory only: Dhan source overlap failed, expiry calendar counts require reconciliation, public-source provenance/timestamps are unverified, and an internal bootstrap p-value discrepancy must be fixed. Decision: **DATA-LIMITED / NO CONFIRMATORY CLAIM**. See [results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/RESULTS.md), [manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/MANUSCRIPT.md), [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/PHASE_STATUS.md), and [sanitized report artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40109273486/artifacts/12566991817).

This is a clean, separate study. Historical scores, candidate fitness, model selections and conclusions from the archived NIFTY forecasting or option-buying tracks below are excluded from NWCP-1.0 evidence.

**Exact question:** using only information available by 10:00 a.m. IST on the first trading session after the previous actual NIFTY 50 weekly expiry, predict whether the NIFTY 50 spot index will be above or below that next weekly expiry's regular-session close. UP / DOWN are the binary classes; ties are reported separately. This track does not develop an options strategy, optimize P&L, or recommend trades.

- **Active developer branch:** [research/nifty-weekly-candle-prediction-developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/nifty-weekly-candle-prediction-developer)
- [Research plan and fixed phases](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/RESEARCH_PLAN.md)
- [Research questions / hypotheses](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/RESEARCH_QUESTIONS.md)
- [Phase status and exit gates](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/PHASE_STATUS.md)
- [Error and defect log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/ERROR_LOG.md)
- [Developer self-test report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/TESTING_REPORT.md)
- [Phase status and exit gates](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/PHASE_STATUS.md)
- [Data and target-timing protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/DATA_PROTOCOL.md)
- [Detailed audit of the 13 supplied PDFs](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-phase-1-sources/research/nifty-weekly-candle-prediction/UPLOADED_PAPER_AUDIT.md)
- [Data/code/source catalog and acceptance checklist](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-phase-1-sources/research/nifty-weekly-candle-prediction/SOURCE_CATALOG.md)
- [Phase 1 review pull request](https://github.com/vishnuvcr/Naked-Options-v2/pull/1) — open, not merged; empirical work remains gated
- [Literature and source review](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-phase-1-sources/research/nifty-weekly-candle-prediction/LITERATURE_REVIEW.md)
- [TradingView Pine indicator catalogue](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-phase-1-sources/research/nifty-weekly-candle-prediction/PINE_INDICATOR_CATALOG.md)
- [QuantEvolve-style discovery specification](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/QUANTEVOOLVE_SPEC.md)
- [Reproducible research runner](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/run_research.py) · [Regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/test_research.py) · [Manual/automatic workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/.github/workflows/nifty-weekly-candle-prediction.yml)
- [Error and defect log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/ERROR_LOG.md) · [Visible decision log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/nifty-weekly-candle-prediction-developer/research/nifty-weekly-candle-prediction/INTERACTION_LOG.md)

**Method:** bounded QuantEvolve-inspired symbolic/rule evolution, regularized logistic regression, tree ensembles, conventional indicators and novel hypotheses (AIA, OWPE, MHDA, VSRP, CMRP and TCD). Chronological validation and a sealed final time block are mandatory. The automated initial result is exploratory only until expiry-calendar, data-provenance, look-ahead, uncertainty and independent-tester gates pass.

**Data governance:** the runner checks a public NIFTY 50 one-minute history candidate and attempts a Dhan overlap audit when DHAN_ACCESS_TOKEN is configured. Public bars are cached; Dhan raw rows are kept ephemeral in the public repository workflow until data terms are confirmed. Raw price rows and weekly target-price rows are not uploaded as public artifacts.

---

# Naked Options v2 — Research status

**Latest active track:** QE-NOB-2.0 bounded acquisition and discovery. [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Acquisition/discovery workflow #39865627143](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143) · [Sanitized reports artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39865627143/artifacts/12464009881)

**Latest status (2026-10-23): DATA-LIMITED.** TOTP-based Dhan authentication and bounded acquisition completed successfully. Cache has 819 JSON files (25 underlying, 794 option); audit read 92,891 underlying rows and 467,834 option rows, with zero duplicate groups, 99.9897% option timestamp coverage, and 100% row-grid coverage. Bounded discovery evaluated 1,185 candidates and found 12 statistical-screen candidates. This is **not** a verified profitable or executable strategy: exact exchange contract identity, historical bid/ask/depth and actual broker fills remain unverified; macro/regime and sentiment feature coverage is incomplete. Execution gate is false. Do not authorize paper/live trading from this result.

The primary cost assumptions are 50 bps adverse slippage per side and ₹10 brokerage per order, with stress cases up to 200 bps and ₹20/order. They are model assumptions, not observed fills. Review candidate-level OOS and cost-stress reports in the linked artifact before any further promotion decision. The timeout recovery is recorded as closed in the error log; execution-data limitations remain open.

---

# Fresh QuantEvolve Research: Naked NIFTY Option Buying (QE-NOB-1.0)

**Current research track:** [QE-NOB-1.0 isolated developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer) · [Research plan](research/quant-evolve-nob/RESEARCH_PLAN.md) · [Research questions](research/quant-evolve-nob/RESEARCH_QUESTIONS.md) · [Phase status](research/quant-evolve-nob/PHASE_STATUS.md) · [Literature review](research/quant-evolve-nob/LITERATURE_REVIEW.md) · [Results](research/quant-evolve-nob/RESULTS.md) · [Errors](research/quant-evolve-nob/ERROR_LOG.md)

**Scope reset on 2026-10-22:** This is a fresh study. Existing prediction/option-buying results and scores are explicitly excluded from the new study’s evidence, candidate seeding and fitness. They remain in the repository for audit history only. No strategy has yet been demonstrated profitable by QE-NOB-1.0.

The study uses bounded QuantEvolve-style candidate discovery for **long calls, long puts, long ATM straddles and long OTM strangles**, with the fresh cache under `data/cache/quant_evolve_nob_v1`, isolated from earlier caches. Only validated new-run outputs under `reports/quant_evolve_nob_v1` will count as evidence. Primary acquisition is Dhan’s rolling historical option API; official/free source checks, contract identity and data quality remain mandatory.

The protocol has eight fixed phases, up to 600 candidates and 25 generations. It requires next-bar entries, date-effective Paytm Money brokerage and charges, adverse slippage sensitivity (0/25/50/100/200 bps per side), chronological validation, block-bootstrap uncertainty and Holm correction. Rolling OHLC without historical bid/ask is not considered execution-validated. The final decision must be **PASS for paper testing only**, **NO-GO**, or **DATA-LIMITED**—never an automatic live-trading recommendation.

- [Fresh QE-NOB developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer)
- [Fresh manual/automatic workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/.github/workflows/quant-evolve-nob.yml)
- [Current workflow run](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39710205711)

**No tester branch/report is required**, per the user's instruction. No profitability claim is made until fresh data, costs, candidate results and validation gates are complete.

---

## Archived track: NIFTY-PRED-1.0 (historical; excluded from QE-NOB-1.0)

## Latest prediction audit — 2026-10-22

The prior workflow completed operationally, but its artifact contains Historical defect in run #39699761966: 798 multi-session forecasts had missing target dates due to partial forward windows. Corrective run #39704420478 completed with zero missing target dates. The pipeline is operationally corrected; scientific conclusions remain limited pending future-period replication and numerical stability checks.

- [Audit record](research/FRESH_PREDICTION_AUDIT_2026-10-22.md) · [Artifact audit utility](research/audits/audit_nifty_predictions.py) · [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/fresh-prediction-developer) · [Corrective workflow #39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478)
- Return/direction forecasts have no robust selected edge. The one-session ExtraTrees volatility-proxy result was numerically reproduced from the prior artifact, but remains a replication candidate and not a trading signal. Options P&L and strategy development remain blocked.

**Research version:** NIFTY-PRED-1.0  
**Scope:** Prediction only. No trading strategy design, optimization, or recommendation in this study.  
**Started:** 2026-10-14  
**Status:** Corrective workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478) completed; 277,633 prediction rows have zero missing target dates. Return/direction edge not established; volatility-proxy result requires untouched future replication. Developer-only process per user request; no tester gate. Artifact audit found 798 invalid missing-target-date rows in h5/h20 volatility and volatility-expansion outputs. Correction commit [e8133a5](https://github.com/vishnuvcr/Naked-Options-v2/commit/e8133a582cbe6c06ce46514f871d1393fc142f6f) is running through workflow [#39704420478](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39704420478). No strategy is approved.

## Repository audit

The repository was empty at project start: no readable README, files, branches, commits, datasets, experiment logs, or workflows. This project therefore starts a new research record without overwriting prior repository work. Relevant prior literature available in the ChatGPT Project library is cited in `research/LITERATURE_REVIEW.md`; it is not treated as this project's validated experimental output.

## Research navigation

- [Research plan](research/RESEARCH_PLAN.md)
- [Research questions and hypotheses](research/RESEARCH_QUESTIONS.md)
- [Literature review](research/LITERATURE_REVIEW.md)
- [Data catalog](research/DATA_CATALOG.md)
- [Experiment log](research/EXPERIMENT_LOG.md)
- [Results](research/RESULTS.md)
- [Phase status and gates](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Independent tester report](research/TESTER_REPORT.md)
- [Scientific manuscript](research/MANUSCRIPT.md)
- [Reproducibility guide](research/REPRODUCIBILITY.md)
- [Execution policy and phase-branch rules](research/EXECUTION_POLICY.md)

## Phase branches

Historical checkpoint branches for completed setup phases and the active model branch are available: [Phase 1](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-1-audit), [Phase 2](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-2-literature), [Phase 3](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-3-data), [Phase 4](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-4-baselines), and [Phase 5](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-models). The resource-bounded execution branch is [research/phase-5-bounded](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/phase-5-bounded). Future phase branches will be created only after their predecessor gate passes.

## Scientific integrity

No model will be declared best from training fit, shuffled validation, price-level R² alone, or a reused test set. Return, directional, volatility, and level targets will be evaluated separately with chronological walk-forward evaluation, simple benchmarks, uncertainty estimates, and multiplicity control. Results unavailable because of data, credentials, compute, or workflow restrictions will be marked **blocked/not run**, never imputed or fabricated.

## Current summary

### Active follow-on: VOL-REGIME-OPT-1.0

A separate weekly-options volatility-regime hypothesis is in protocol/source-gate work on [the developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer). A bounded Dhan probe has returned structurally valid weekly CALL/PUT arrays for candidate expiry codes 1 and 2 in a five-day January 2025 sample. Exact expiry mapping, stable contract identity, full coverage and P&L remain unverified. See the [frozen plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/VOL_REGIME_OPTIONS_PLAN.md) and [sanitized source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json). No strategy is approved.

- **Original prediction study (NIFTY-PRED-1.0): CLOSED WITH SCOPE LIMITATIONS.** Its corrected canonical run is [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128); see [results](research/RESULTS.md), [phase status](research/PHASE_STATUS.md), and [scientific manuscript](research/MANUSCRIPT.md).
- **Follow-on option-buying validation (OPT-BUY-1.0): CLOSED — NO-GO for tested candidates; broader hypothesis inconclusive.** The completed [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) and independent review found strangle quote coverage of 69.18% (<80%), conflicting duplicate groups at 1.409% (>1%), and negative net daily P&L confidence intervals for all four candidates. No paper/live strategy is approved; details are in [the option-validation results](research/option-validation/RESULTS.md) and [tester report](research/option-validation/TESTER_REPORT.md).
- Latest validated NIFTY data: 4,906 Dhan daily rows from 2007-01-02 to 2026-10-21; SHA-256 `2a76714665754ec6371e92d8b9b56565606c0d1a4a2fc9cc9013291e233b2158` (the earlier 4,901-row run remains historical).
- Data gaps remain documented: historical options features, FII/DII, PCR, breadth, point-in-time constituents/corporate actions, and timestamped news were not comprehensively verified for the original prediction study. These gaps limit the scope of inference.
- Statistical integrity: the original study found no robust return/direction edge after multiple-testing correction. The option-buying follow-on did not demonstrate profitable net option P&L after modeled costs.
- Audit trail: [error log](research/ERROR_LOG.md), [experiment log](research/EXPERIMENT_LOG.md), [interaction log](research/INTERACTION_LOG.md), [frozen option validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md), [independent tester](research/option-validation/TESTER_REPORT.md), and [developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md).

The original prediction study and follow-on option-buying study are both closed for their stated protocols. Any further work should start a separately versioned research question and preregistered protocol rather than reopen failed gates or repeat parameter loops.


## Latest correction checkpoint — 2026-10-14

The independent audit found that forward-volatility targets near the sample tail could be calculated from partial future windows. The developer branch now requires all horizon returns to be present before assigning the 5-/20-session volatility target. Workflow [#48](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38532904979) stopped at a regression-test assertion (a scalar `.notna()` call), before feature construction or model fitting. That test was corrected to `pd.notna` in commit `9b655da8d72667a6d2f15e4dad5df55a1bec2e84`; workflow [#49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) is the retest and corrected-run gate.

Until #49 completes, the run #45 model scores remain preliminary. No strategy or model is approved. Phase 5/7 remain open pending successful tests, corrected OOS predictions with complete target windows, and an independent tester report. See the [developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/ERROR_LOG.md) and [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/developer-review/research/PHASE_STATUS.md).


## Corrected run #49 — 2026-10-14

The forward-volatility target defect has been fixed and regression-tested. [Workflow #49](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38533512128) completed successfully. Artifact SHA-256: `97858125f14344520f77dd503d2c0441005e6da4cfa12fc23fe7427680f932e7`.

- [Results and evidence register](research/RESULTS.md)
- [Phase status and gate decisions](research/PHASE_STATUS.md)
- [Error log](research/ERROR_LOG.md)
- [Developer correction branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/developer-review)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md)

Preliminary results: no robust return/direction edge has been demonstrated; selected 5-/20-session global return models are worse than the zero-return baseline; volatility models do not pass adjusted QLIKE comparisons. Some volatility-expansion classifiers improve log loss, but are exploratory and not trading signals. The independent tester passed the bounded prediction-only study with scope limitations; Phase 2 literature depth and Phase 6 data/regime coverage remain partial and are documented. This is prediction research only: no options-chain strategy, transaction-cost/slippage simulation, or Paytm Money execution analysis has been completed.


## Independent review outcome — 2026-10-14

The independent tester has issued **PASS WITH SCOPE LIMITATIONS** for the bounded prediction-only research. See the [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/independent-tester/research/TESTER_REPORT.md), [results register](research/RESULTS.md), and [phase gates](research/PHASE_STATUS.md).

Conclusion: no robust return/direction edge is demonstrated. Volatility-expansion results are exploratory, and one-session probabilities are poorly calibrated. No trading strategy is approved or tested. Historical option chains, FII/DII, PCR, breadth, timestamped news, transaction costs/slippage and Paytm Money execution remain outside the verified dataset and experiments.


**Closure status:** The nine-phase research is closed for the bounded prediction-only scope, with accepted limitations. The conclusion is that this tested model/data set did not establish a robust return/direction edge. No options strategy or live execution plan is approved.


The static research status page is published through the lightweight [Pages publish workflow](https://github.com/vishnuvcr/Naked-Options-v2/actions/workflows/publish-research-status.yml). The final option-buying plan, results, manuscript, figures and independent review are now in main; this README update triggers a fresh status-page deployment.


## Follow-on study: option-buying validation — OPT-BUY-1.0

The original nine-phase NIFTY-PRED-1.0 prediction-only study remains closed and unchanged. The separate test of next-session intraday monthly-option straddles/strangles is now closed for its frozen scope.

**Final disposition: NO-GO for the tested implementations; broader hypothesis INCONCLUSIVE because the data-quality gate failed.** Final workflow [run #11](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384) completed successfully; 13 unit tests passed before and after analysis.

- [Frozen validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md)
- [Results](research/option-validation/RESULTS.md)
- [Structured manuscript](research/option-validation/MANUSCRIPT.md)
- [Net P&L comparison chart](research/option-validation/figures/net_pnl_comparison.svg)
- [Slippage sensitivity chart](research/option-validation/figures/slippage_sensitivity.svg)
- [Primary comparisons CSV](reports/option_validation/primary_comparisons.csv)
- [Results summary JSON](reports/option_validation/results_summary.json)
- [Independent tester report](research/option-validation/TESTER_REPORT.md)
- [Developer disposition](research/option-validation/DEVELOPER_DISPOSITION.md)
- [Workflow run/artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38548437384)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-developer)
- [Independent tester branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-buying-independent-tester)

At ₹10 brokerage/order and 50 bps adverse slippage per premium side, all four alert-filtered candidates had mean net daily P&L between −₹315.71 and −₹369.43 per one-lot-proxy eligible-day slot; all 95% intervals were negative. Positive paired differences versus always-buy (Holm-adjusted p=0.002) only show loss reduction relative to a worse baseline.

Frozen gates failed: strangle quote coverage 69.18% (minimum 80%) and conflicting duplicate groups 1.409% (maximum 1%). All candidates failed the 100-bps and both-half profitability gates. No paper-trading or live deployment is approved. Do not relax gates or continue optimization loops.

## OPT-BUY-2.0 — Strike-selection research (in progress)

- Protocol: [strike-selection plan](research/STRIKE_SELECTION_PLAN.md); implementation: [strike-grid code](research/option-strike-selection/strike_grid.py).
- Automated run #1 failed at the data stage: the existing 13 regression tests passed, but no usable historical option quote rows were loaded. This is a data blocker, not a profitability finding. [Run #1](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551789841).
- Diagnostic-output fix and inference-family correction are being tested in [run #2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38551939491) and [run #3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552000337). No strike winner or strategy is approved.
- Separate review branches: [developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-developer) and [independent tester](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-strike-selection-independent-tester). The tester's current report is blocked pending usable quotes.




## OPT-BUY-2.0 run #4 — results and disposition (2026-10-14)

- [Run #4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38552144097) completed successfully at workflow level; 13 pre-analysis and 13 final regression tests passed, and sanitized artifact `option-strike-selection-38552144097` was uploaded (SHA-256 `7fae1922403e398f040ee8ca3a80f607e07e0d6569c98eb35b3ae0c6f168d285`).
- Data: 1,055,699 raw rows; 1,023,541 usable rows; 452 conflicting duplicate groups out of 31,706 duplicate groups (1.4256%); no parse failures; quote dates 2022-11-01 through 2026-10-14.
- Coverage across the 980 test dates ranged from 83.27% for ATM/ATM (C0_P0) down to 16.94% for C3_P-3. Only C0_P0 cleared the 80% coverage gate. The conflict rate exceeded the 1% gate. Overall confirmatory gate failed; all candidate ranking is exploratory.
- At primary costs (50 bps adverse slippage per premium side and ₹10 per order), all 32 model-filtered candidate × horizon means were negative, with 95% block-bootstrap interval upper bounds below zero. Examples: ATM/ATM horizon 5 mean −₹315.02 per eligible date (95% CI −₹406.69 to −₹232.69; 223 alert trades); ATM/ATM horizon 20 mean −₹330.45 (95% CI −₹416.51 to −₹244.30; 259 alert trades). Across the full grid, chronological half means were negative in both halves for all model-filtered cells. Higher slippage further worsened outcomes. These are exploratory descriptive outcomes because the data gate failed.
- Defect found in run #4 artifact: all 32 primary raw/Holm p-values were blank/NaN despite nonempty ledgers. Do not treat multiplicity-adjusted inference as complete. Developer added an explicit null-centered circular block-bootstrap p-value implementation in commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9; [corrective rerun #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress. No parameter search is being expanded; this is a bounded inference correction.
- Additional scope limitation: the frozen plan calls for a common-date sensitivity, but run #4 artifact does not contain one. Do not claim cross-candidate superiority; record this as not completed under the failed quality gate.
- Decision: **NO-GO / no strike candidate approved**. The study is non-confirmatory due conflict rate and coverage failures, all measured primary model-filtered means are negative, and the p-value output defect requires the single corrective rerun. No paper or live deployment.


### Latest status

Corrective [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) is in progress on commit a543eed8059de79dbcc6b2dc53a3dd31f14298a9 to fix missing primary p-values. The run #4 result remains exploratory and no strategy is approved.


## Uploaded-PDF method audit — expanded comparison initiated

On 2026-10-14, all 13 uploaded PDFs were materialized and text-extracted for method inventory. The bounded forecasting-model comparison is running on [research/pdf-method-audit](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/pdf-method-audit). See [PDF method audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-method-audit/research/PDF_METHOD_AUDIT.md) for source-by-source methods, implemented candidates, scope exclusions, and data-dependent blockers.

- Expanded the classical registry to include Linear Regression, Lasso, SGD, KNN, Decision Tree, Gradient Boosting and AdaBoost in addition to the existing baselines, SVR, forests, MLP and optional XGBoost/LightGBM/CatBoost.
- Expanded compact CPU sequence candidates to LSTM, GRU, vanilla RNN, CNN, TCN, Transformer and four hybrids (LSTM+GRU, CNN+RNN, CNN+TCN, LSTM+TCN). These remain **pending empirical validation** until the workflow completes and artifacts are checked.
- BERT/news sentiment, fuzzy neural networks, Deep Belief Networks, wavelet preprocessing, Granger screening, and backward-elimination variants are explicitly not yet validated; some require point-in-time data or additional implementation. The three options-strategy PDFs remain outside the prediction-only scope.
- The run is a bounded screening comparison, not an exhaustive recreation of every paper's private dataset, preprocessing, or hyperparameter search. No method will be called tested without completed out-of-sample evidence.


## NIFTY prediction research — final status (2026-10-14)

The bounded prediction-only study completed on research branch `research/pdf-audit-developer` and received independent tester disposition **PASS WITH SCOPE LIMITATIONS** on `research/pdf-audit-tester-final`.

- [Final workflow #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792) — success; artifact SHA-256 `14c9d6fc1bcb0f00ff28e708cb10a6cab9b378e5e60ff31f6e66aaa5e977172b`.
- [Final research results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PDF_METHOD_AUDIT_RESULTS.md)
- [Scientific manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/MANUSCRIPT.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/PHASE_STATUS.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-developer/research/ERROR_LOG.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md)

Final artifact: 471,735 out-of-sample predictions; zero missing target dates; target-date defect resolved. Conclusion: no robust return/direction winner was established. One-session global XGBoost volatility QLIKE improvement survives the configured Holm correction; other volatility findings are metric-specific and volatility-expansion results remain exploratory. Twenty weekend-dated observations, global-market close-time alignment, and missing/unverified options/PCR, FII/DII, breadth, news and corporate-action inputs remain limitations. This is prediction-only research; no trading strategy is approved.


## OPT-BUY-2.0 strike-selection grid — final status (2026-10-14)

**Disposition: NO-GO for all tested candidates.** Frozen workflow [run #5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38562114651) succeeded; artifact SHA-256 `e727095479b645703252832956a99a2924a5b5f68c507d68ec38b66ec9bd61e5`.

- [Strike-grid results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/option-strike-selection/RESULTS.md)
- [Independent tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-independent-tester-final/research/option-strike-selection/TESTER_REPORT.md)
- [Developer error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/ERROR_LOG.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-strike-selection-developer/research/PHASE_STATUS.md)

At ₹10/order and 50 bps adverse slippage per premium side, all 32 model-filtered strike-pair × horizon cells have negative mean net P&L and 95% intervals entirely below zero; both chronological halves are negative. Mean daily net P&L ranges from −₹316.87 to −₹622.96 per eligible-date slot. Quote conflict rate is 1.4154% (frozen ceiling 1%), and only ATM/ATM clears 80% coverage. The artifact's 32 primary p-value rows are blank with zero observations; no multiplicity-adjusted significance claims are valid. Independent tester disposition: FAIL / NO-GO. Do not paper-trade or live-trade these candidates; do not relax gates or extend this grid. The original prediction-only study remains closed, and the OPT-BUY-1.0 result remains unchanged.


## OPT-BUY-3.0 — entry/exit research (in progress)

The user shifted the follow-on work from prediction to NIFTY 50 long-option entry/exit testing. Prior OPT-BUY-1.0 and OPT-BUY-2.0 no-go conclusions remain unchanged.

- [Frozen protocol and phases](research/OPTION_ENTRY_EXIT_PLAN.md)
- [Research questions](research/OPTION_ENTRY_EXIT_QUESTIONS.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/option-entry-exit-developer)
- [Implementation](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)

The first executable is only a partial time-based CALL/PUT screen with fixed-duration/EOD exits. It does not yet implement the entire registered random, rule-based, premium-barrier or trailing-stop catalogue. No empirical result or strategy is approved until the workflow output and cost formulas are independently checked. The existing 1% duplicate-conflict and 80% coverage gates remain fixed.


## OPT-BUY-3.0 — Entry/exit research (active)

The user has paused prediction research and requested a bounded NIFTY 50 long-option buying study, from random/control entries to targeted entries and varied exits. The user explicitly rejected independent reviews; **no separate tester role, tester branch, or tester-report gate will be created**. Automated tests, data checks, cost calculations, statistical corrections and robustness checks remain mandatory.

- [OPT-BUY-3.0 protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/OPTION_ENTRY_EXIT_PLAN.md)
- [Entry/exit implementation (partial)](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/entry_exit_backtest.py)
- [Entry/exit regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/test_entry_exit.py)
- [Automated workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/.github/workflows/option-entry-exit.yml)
- [Current entry/exit results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-entry-exit-developer/research/option-entry-exit/RESULTS.md)

**Current limitation:** the committed screen only covers fixed-time CALL/PUT entries and fixed holding/EOD exits; it does not yet implement the full registered entry/exit catalogue. Current branch results say BLOCKED_NO_VALID_QUOTES; no strategy result or approval is claimed. Research continues only through the predefined finite phases, and the existing failed gates from OPT-BUY-1.0/2.0 remain unchanged.


### OPT-BUY-3.0 execution update (2026-10-15)

Actions run [#3](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38620992395) completed technically and 16 tests passed, but quote acquisition yielded zero usable rows and zero candidates. A stale-manifest skip and a single-leg cost-helper mismatch were identified. Workflow/cache retry, single-leg cost accounting, expanded entries/exits, sensitivity scenarios and regression tests have been committed on the active research branch; runs [#4](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621390693) and [#5](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621455619) were triggered and are pending verification. No strategy conclusion is available yet.


**Data acquisition correction:** [Run #6](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621480232) passed tests but had no daily NIFTY cache, so the rolling-options manifest planned zero requests and no empirical result was possible. The workflow now acquires daily data before option history when the cache is missing. [Run #7](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38621701520) is pending; do not interpret the earlier blocked output as strategy performance.


### OPT-BUY-4.0 — 1,000+ unique naked-option strategy algorithms (2026-10-15)

The new study explicitly distinguishes **unique decision algorithms** from execution configurations. Strike, exit, holding-period, and cost variants do not increase the strategy count. The development branch now contains a deterministic catalogue generator, signature-based duplicate audit, registry tests, and an Actions workflow. The catalogue audit is a prerequisite only; it does not establish trading performance. Empirical option testing remains pending until the strategy catalogue is audited and usable point-in-time option data passes quality gates.

- [Research protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_PLAN.md)
- [Research questions](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/OPTION_BUYING_1000_QUESTIONS.md)
- [Unique-strategy catalogue generator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/strategy_catalogue.py)
- [Registry integrity tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/research/option-buying-1000/test_strategy_catalogue.py)
- [Automated catalogue workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/option-buying-1000-developer/.github/workflows/option-buying-1000.yml)

**Status:** implementation is underway; no new backtest results or profitable strategy are claimed. The next gates are catalogue generation/deduplication, data audit, causal backtest implementation, cost accounting, chronological holdout, multiplicity correction, and manuscript closure.


## Fresh prediction continuation audit — 2026-10-15

A continuation audit was added at [research/FRESH_PREDICTION_CONTINUATION_AUDIT.md](research/FRESH_PREDICTION_CONTINUATION_AUDIT.md). The existing bounded prediction research and expanded model workflow are already recorded as completed, but the tester branch report currently available still reports run #60 as FAIL FOR FINAL SCIENTIFIC SIGN-OFF, while this README refers to run #62 and a pass. That evidence mismatch is now logged and must be reconciled before claiming final scientific sign-off. No strategy development is included in this prediction-only continuation.


### Run #62 independent artifact review — 2026-10-15

The independent tester has now inspected [run #62](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38604064792). Target-date integrity and core MAE/RMSE/Holm arithmetic pass: 471,735 prediction rows have non-null target dates and all recorded targets align with their 1/5/20-session horizons. **Final scientific sign-off remains withheld** because some volatility QLIKE outputs are pathological (including elastic-net at horizon 5) and full HAC/block-bootstrap inference has not been independently reproduced. See the [current tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md), [ERR-019](research/ERROR_LOG.md), and [phase status](research/PHASE_STATUS.md). Only a bounded defect correction is warranted; no model-catalogue expansion or strategy development is authorized by the prediction-only scope.


### Final independent audit — run #62 (2026-10-15)

The tester has completed direct artifact review and reports **PASS WITH SCOPE LIMITATIONS**: [run #62 tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/pdf-audit-tester-final/research/PDF_METHOD_AUDIT_TESTER_REPORT.md). All 471,735 exported prediction rows have non-null target dates with offsets matching their 1/5/20-session horizons. MAE/RMSE, all 485 HAC p-values and block-bootstrap intervals, Holm corrections, and all 102 volatility QLIKE rows were independently reproduced within numerical precision. Extreme QLIKE values for some models are a large penalty for near-floor forecasts, not a confirmed calculation defect. The conclusion remains **no robust return/direction winner established**; a narrow one-session global XGBoost volatility QLIKE improvement is metric-specific, not a trading signal. Weekend-date verification and missing options/PCR, FII/DII, breadth, point-in-time news/corporate-action inputs and strict global timing remain limitations. The bounded NIFTY prediction model screen is closed; do not expand the catalogue or infer trading profitability.


## Volatility-regime weekly options hypothesis — VOL-REGIME-OPT-1.0 (2026-10-15)

A new, separate validation study was opened after user approval to test: buy an ATM NIFTY weekly straddle in a predicted high-volatility regime, and sell a weekly OTM strangle with each leg near absolute delta 0.07 in a predicted low-volatility regime. This is a hypothesis, not an approved strategy. The prior prediction-only study and prior monthly/intraday option tests remain closed and unchanged.

- [Frozen protocol and nine-phase plan](research/VOL_REGIME_OPTIONS_PLAN.md)
- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-developer)
- [Source-gate workflow](.github/workflows/vol-regime-options.yml)
- [Source probe](research/vol-regime-options/source_probe.py)
- [Source audit results](reports/vol_regime_options/source_audit.json) (created by Actions when the source probe completes)

Primary signal is the 5-session technical volatility-expansion classifier; the 20-session signal is secondary only. The protocol explicitly requires weekly-expiry and exact-contract validation, historical expiry/lot-size provenance, ≥80% quote coverage, ≤1% conflicting duplicate groups, realistic Paytm Money/statutory charges and slippage stress, risk/tail metrics, and independent tester approval. If weekly history or contract identity cannot be verified, the study stops as blocked/inconclusive. No live trading or deployment is authorized.


**Source-gate checkpoint (2026-10-15):** the first probe [run #38676211935](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676211935) exposed a workflow cache configuration issue, which was fixed. The corrected run confirmed the monthly schema control but Dhan rejected WEEK / expiryCode=0 with “expiryCode is required”. A single bounded diagnostic now tests WEEK codes 0, 1 and 2; weekly availability and expiry mapping are still unverified. No strategy results are claimed.

### VOL-REGIME-OPT-1.0 checkpoint — 2026-10-15

**Status: BLOCKED at expiry mapping / exact-contract identity; no P&L run.** Saved Dhan evidence shows schema responses for candidate weekly expiry codes 1 and 2 in a short sample, but does not establish actual expiry dates or same-contract entry/exit continuity. The saved audit predates the code-3 probe edit. The fallback dataset audit was not found and its script flags license review as required. The frozen hypothesis remains unchanged. No strategy is approved. See `research/PHASE_STATUS.md`, `research/ERROR_LOG.md`, and the source-gate disposition and independent tester report on the research branches.


## VOL-REGIME-OPT-1.0 latest source-gate checkpoint — 2026-10-15

The latest bounded Dhan probe completed its weekly schema requests in [workflow run #10](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667): candidate WEEK codes 1, 2 and 3 returned structurally valid CALL/PUT arrays in the five-day 2025-01-06 to 2025-01-10 sample (code 3 returned 357 CALL rows and 349 PUT rows). WEEK code 0 still fails. The workflow was ultimately marked failed because the runner received a shutdown signal during the Hugging Face fallback probe; the audit and later steps were skipped by that run, so the completed Dhan result has now been persisted separately. The HF fallback remains unverified.

**Decision remains BLOCKED:** schema success does not identify the actual expiry dates represented by each code or prove same-strike/same-expiry entry-to-exit continuity. No P&L, statistical strategy comparison, or profitability claim is allowed. The independent tester's report is at [tester branch](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md); see the [developer source-gate disposition](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/SOURCE_GATE_DISPOSITION.md) and [sanitized audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/reports/vol_regime_options/source_audit.json).

**Developer instruction:** do not proceed to P&L unless a verifiable source establishes expiry-code/date mapping and fixed-contract continuity. **Tester instruction:** independently check the persisted code-3 evidence and confirm the blocked disposition; do not infer profitability or loss from this data gate.

Feasibility manuscript for the closed weekly-options follow-on: [VOL-REGIME-OPT-1.0 manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-developer/research/vol-regime-options/MANUSCRIPT.md). Independent source-gate disposition: [tester report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-tester/research/vol-regime-options/TESTER_REPORT.md).


## Option-buying continuation — 2026-10-16

User requested continued bounded research toward the best evidence-supported option-buying strategy. The prior NIFTY prediction study and OPT-BUY-1.0/2.0 no-go decisions remain unchanged. A continuation branch and finite protocol were created: [VOL_REGIME_OPTIONS_CONTINUATION.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_CONTINUATION.md). The current weekly-regime hypothesis remains **BLOCKED at expiry-code/date mapping and exact-contract continuity** until a verified source establishes both. Short-window Dhan schema success is not evidence of valid historical weekly contracts or profitability. Frozen data gates remain >=80% coverage and <=1% conflicting duplicate groups; costs, taxes, slippage, chronological holdout, risk metrics and multiplicity correction are mandatory. No strategy is approved and no P&L is claimed.


### Source audit retry — 2026-10-16

The failed source-audit job has been retried as [run #38676451667, attempt 2](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38676451667). The last status check showed it in progress. This is only an acquisition/metadata retry: until the job finishes and the saved artifacts are checked, no Hugging Face data availability, license clearance, coverage, or strategy P&L is claimed. Expiry mapping and exact-contract continuity remain the blocking gates.


### Reusing the existing NIFTY options archive — 2026-10-16

Repository inspection found that [`vishnuvcr/Nifty`](https://github.com/vishnuvcr/Nifty) already uses the Hugging Face dataset [`thetrademarkk/india-index-options-1m`](https://huggingface.co/datasets/thetrademarkk/india-index-options-1m), caching `options/NIFTY/*.parquet` and index bars for expiry-exit analysis. Its dataset card lists minute OHLCV/OI, explicit expiry/strike/option-type fields, and a **CC-BY-NC-4.0** license; this is suitable only for non-commercial research with attribution and not for commercial redistribution. A new cached, sanitized source-audit workflow was added on [the continuation branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/vol-regime-options-continuation); [run #38807375042](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/38807375042) was in progress at the last check. No data-quality pass or P&L is claimed until its report is inspected and sample contracts are reconciled against official NSE evidence. The dataset contains OHLC bars, not executable bid/ask quotes.


The free-source audit also records official NSE expiry-rule changes across 2025; see the [continuation source audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/vol-regime-options-continuation/research/VOL_REGIME_OPTIONS_FREE_SOURCE_AUDIT.md). These changes mean the research must use dated contract-file evidence rather than a weekday-only expiry heuristic. The HF audit run's download step completed, but its data-quality step remained in progress at the latest check; all strategy/P&L gates remain closed pending its report and official contract reconciliation.


## Latest NIFTY prediction rerun — 2026-10-22

- [Workflow #39699761966](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39699761966) completed successfully. Artifact SHA-256: `6f2cd6bb302763e5e972fb54e447bfbd47bba0c8cd3cfe3fd024f9cf6062c8dc`.
- [Sanitized aggregate run summary](reports/nifty_prediction_run_39699761966_summary.json) · [research results](research/RESULTS.md) · [structured manuscript](research/MANUSCRIPT.md) · [phase status](research/PHASE_STATUS.md).
- Output: 647 metric rows, 299 OOS candidate comparisons, 296 CV-pass rows, 52 compute-budget-blocked rows.
- No robust selected return/direction edge was established. One selected global ExtraTrees model improved the one-session volatility-proxy QLIKE loss; Holm p=4.26e-7 across all 299 candidate comparisons. This requires independent-period replication and is not a trading signal.
- Options research remains **BLOCKED_NO_VERIFIED_CONTRACT_DATA**. No options P&L, trading recommendation, or live deployment is authorized.


## QE-NOB-1.0 — fresh QuantEvolve-inspired naked option buying (2026-10-22)

**Decision: DATA-LIMITED / NO strategy approved.** [Workflow #39712854501](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501) completed 600 candidates across 9 generations, but 0 passed the statistical gate and 0 passed the execution/promotion gate. The run acquired 92,510 underlying rows and 2,588,918 option rows from 2021-10-25 through 2026-10-21. Data quality failed because 453 of 471 duplicate groups conflicted; historical executable bid/ask/depth and exact expiry/lot-size mapping remain unverified. The strongest validation-selected opening-gap candidate's OOS mean daily net was ₹10.68 with a 95% block-bootstrap interval of -₹188.62 to ₹237.43; Holm-adjusted p=1.0, and stressed costs turned its mean daily net negative. These results do not establish profitability.

- [Fresh study branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer) · [Results report](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Workflow artifact and logs](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39712854501)
- User explicitly declined a tester; this is a developer-led analysis with automated unit checks, not an independently audited result. The first workflow's commit step failed on a documentation rebase conflict; a bounded-report allowlist was committed in workflow revision [4191d5a](https://github.com/vishnuvcr/Naked-Options-v2/commit/4191d5a0cbbbd703867d5b0f5e7474d8b13f825e). The full report remains available as the run artifact.


## QE-NOB-1.0 — fresh QuantEvolve-inspired naked option buying (2026-10-22)

Latest completed run [#39741806754](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741806754) evaluated 600 constrained candidates on 1,241 sessions (2021-10-25 to 2026-10-21). The offset-aware duplicate key corrected a diagnostic defect: 0 duplicate groups and 0 rows dropped; timestamp coverage 99.772%, row-grid coverage 100%. **No strategy passed the statistical gate**; execution quality remains unverified due to missing historical bid/ask/depth and unresolved exact expiry/contract/lot-size mapping. Decision: **NO-GO for strategy approval; no paper/live trading recommendation**.

- [Research plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PLAN.md) · [Results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Scientific manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md) · [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v1-developer)

User explicitly declined an independent tester; automated checks passed, but no independent review is claimed. Follow-up workflow [#39741823249](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39741823249) is being monitored.

## QE-NOB-1.0 latest status — 2026-10-22

The corrected duplicate-key diagnostic is valid (0 duplicate groups; 2,600,975 option rows; 99.772% timestamp coverage and 100% row-grid coverage), but prior P&L statistics are superseded: a discovered lot-size proxy bug assigned 25 units across dates before November 2024. The code now uses a sourced, expiry-family/date-based NIFTY lot proxy for WEEK1 and MONTH1. Corrected run [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) is in progress; pre-run automated tests passed.

Research will proceed using the available rolling option OHLC, modeled adverse slippage and stated cost assumptions; missing historic bid/ask/depth is not a statistical-research blocker. It remains an execution-readiness limitation, so no executable fill or deployment claim is allowed. No strategy is approved. [Plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESEARCH_PLAN.md) · [Results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md) · [Activity log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/INTERACTION_LOG.md)

Paytm Money's current [F&O FAQ](https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web) reports ₹10 per executed order; ₹20 per order remains a stress case because account-specific legacy tariffs can differ. No independent tester branch/report is created because the user explicitly declined a tester.


## QE-NOB-1.0 corrected lot-size reprice audit — 2026-10-22

The earlier P&L metrics were superseded after finding and correcting a historical NIFTY lot-size proxy defect. A saved 483,706-trade ledger has been re-priced using the official NSE transition schedule by rolling weekly/monthly series. No candidate in the frozen prior 600-candidate set met the joint daily-median, corrected-validation and cost-stress prerequisites. [Reprice audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/LOT_SIZE_REPRICE_AUDIT.md) · [Results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md). Missing historical bid/ask/depth does not stop OHLC-based research, but executable fills remain unverified. The corrected full rerun [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) was still running as a supplementary check. No strategy is approved.


## QE-NOB-1.0 final corrected result — 2026-10-22

**Final disposition: NO_STATISTICAL_CANDIDATE / NO-GO for strategy approval.** Corrected full workflow [#39774033025](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025) completed successfully. It evaluated 600 unique candidates over 4 islands and 9 generations using 1,241 sessions (2021-10-25 to 2026-10-21), 92,510 underlying rows and 2,600,975 rolling option rows. All 1,708 acquisition requests were cache hits, zero acquisition failures were recorded, and pre-run/post-run automated tests passed. Zero of 600 candidates passed the statistical gate; zero passed the execution/promotion gate. Candidate 86's corrected OOS mean daily net was about ₹6.14, with a 95% block-bootstrap lower bound about −₹195.69 and Holm p=1.0. The OHLC quality gate passed, but historical bid/ask/depth and exact exchange contract identity remain unverified, so executable profitability is not established.

- [Final results](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/RESULTS.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/PHASE_STATUS.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/ERROR_LOG.md) · [Corrected manuscript](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/MANUSCRIPT.md) · [Dated lot-size reprice audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/LOT_SIZE_REPRICE_AUDIT.md) · [Activity log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v1-developer/research/quant-evolve-nob/INTERACTION_LOG.md)
- [Sanitized run report](reports/quant_evolve_nob_v1/RESULTS.md) · [Run summary JSON](reports/quant_evolve_nob_v1/run_summary.json) · [Workflow artifact](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39774033025)

The frozen-ledger reprice audit is a separate sensitivity check, not the final evolutionary run. No strategy is approved. User explicitly declined independent testing; no tester branch/report is claimed. The bounded study is closed; do not repeat unbounded search without materially better contract/execution data.


## Follow-on research: QE-NOB-2.0 open structural discovery

The completed QE-NOB-1.0 search returned **NO-GO for the tested candidate grammar**. A new bounded protocol is being prepared to address the structural novelty limitation rather than simply increasing parameter variations.

- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer)
- [Discovery plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Feature feasibility audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)

**Status (2026-10-22):** Protocol amendment committed; feature/source runtime audit and implementation have not yet run. Fixed maximum budget: 1,500 unique structural candidates, 20 generations. Strategy novelty, evolved exit state machines, chronological holdout, multiple-testing correction, bootstrap uncertainty, fees and slippage are mandatory. No new strategy is claimed profitable. User explicitly said “No tester”; no tester branch/report will be created.


### QE-NOB-2.0 progress update — 2026-10-22

The first implementation checkpoint is now committed on the [QE-NOB-2.0 developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer). It adds a typed strategy grammar, structural fingerprints, novelty distance, deterministic mutation/crossover, parent lineage, regression tests and a dedicated automatic/manual test workflow.

- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Feature feasibility audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md)
- [Grammar source](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/strategy_grammar_v2.py)
- [Grammar tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_strategy_grammar_v2.py)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)

**Status:** test workflow is configured, but a successful CI run has not yet been verified. The grammar is not integrated with the backtester, runtime feature coverage is not fully audited, and no new strategy has been backtested or shown profitable. The next gate is automated grammar validation and feature-gated simulator integration. No tester branch/report, per user instruction.


### QE-NOB-2.0 progress — feature audit tooling

The follow-on branch now includes a cache-schema audit utility, regression tests and a dedicated manual/automatic GitHub Actions workflow. This work helps determine which market features can safely enter structural strategy search; it does not produce trading results.

- [Developer branch](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer)
- [Feature audit utility](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/feature_audit_v2.py)
- [Feature audit tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_feature_audit_v2.py)
- [Feature audit workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-feature-audit-tests.yml)
- [Updated phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Implementation error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)

**Current gate:** test workflows have been configured, but successful runs have not been verified; the feature audit has not yet run against the research cache. Backtester integration and the new discovery run remain pending. No new strategy has been shown profitable. No tester branch/report, per the user's instruction.


### QE-NOB-2.0 — implementation checkpoint 2

Added a sanitized cache/feature audit utility and regression tests; expanded the grammar CI workflow to run both test suites. Corrected a test import problem caused by the hyphenated research directory and logged the defect/correction.

- [Feature audit code](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/audit_features_v2.py)
- [Feature audit tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_audit_features_v2.py)
- [Current phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)

**Verification status:** the code and tests are committed; successful CI has not been verified in this checkpoint. The feature audit has not yet run against the prior study's cached data, and no new strategy backtest has run.


### QE-NOB-2.0 — bounded structural candidate generator

The follow-on research branch now contains a bounded candidate proposal engine with structural novelty, deterministic mutation/crossover, lineage and a fixed budget of 1,500 candidates / 20 generations. It is not yet a fitness-guided strategy search: simulator integration and CI verification remain pending, and no new strategy has been backtested or shown profitable.

- [Candidate generator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/evolve_candidates_v2.py)
- [Generator tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_evolve_candidates_v2.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-candidate-generator-tests.yml)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)


### QE-NOB-2.0 — signal evaluator checkpoint

A leakage-aware signal evaluator and regression tests have been committed to the developer branch. A sparse-signal next-bar timing defect was caught and corrected; the correction is logged. CI is configured but not verified. This is not yet an option backtester and produces no P&L result.

- [Signal evaluator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/signal_evaluator_v2.py)
- [Signal evaluator tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_signal_evaluator_v2.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-signal-evaluator-tests.yml)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)


### QE-NOB-2.0 — OHLC option simulator checkpoint

An indicative long-option simulator has been added to the developer branch. It models next-bar entries, same-strike exits, dated lot-size proxies, brokerage/statutory fees and adverse slippage, and prevents overlapping positions per candidate. The execution gate remains FAIL without exact contract identity and executable quotes. CI and historical-cache execution are not yet verified.

- [Simulator source](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/option_simulator_v2.py)
- [Simulator tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_option_simulator_v2.py)
- [Workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-option-simulator-tests.yml)
- [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)

### QE-NOB-2.0 implementation and CI checkpoint — 2026-10-22

**Status: software regression checks passing; empirical discovery still blocked pending Phase 2 runtime cache/source acquisition. No new strategy result is claimed.**

- [Bounded open structural discovery plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Feature/source feasibility](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/FEATURE_FEASIBILITY_V2.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md) · [Activity log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/INTERACTION_LOG_V2.md)
- Implemented typed predicate validation, deterministic structural mutation/crossover, and a candidate generator capped at 1,500 unique candidates / 20 generations. Only implemented signal-entry and time/premium-stop/premium-target semantics are generated; candidate generator still does not calculate fitness or P&L.
- Automated checks passed: [grammar + feature audit #39802894371](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894371) (15 tests); [standalone feature audit #39802894311](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802894311); [signal evaluator #39801804759](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801804759); [option simulator #39801813009](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39801813009); [candidate generator #39802753682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39802753682).
- The option simulator includes cost/slippage assumptions and conservative premium stop/target handling, but its execution gate intentionally remains FAIL because rolling OHLC does not confirm exact exchange contract identity, historical bid/ask/depth or actual broker fills.
- Initial runtime audit [#39803204747](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803204747) returned `BLOCKED_NO_LOCAL_CACHE` (zero files). This does not prove Dhan or any free source is unavailable; the sibling branch's Actions cache was not present in the v2 runner.
- A bounded cache-first/source-acquisition-only workflow was added: [QE-NOB v2 data-audit workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-data-audit.yml). Run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was automatically triggered; inspect its sanitized artifact before changing Phase 2 status. Raw market payloads are kept in the runner cache and are not uploaded as artifacts.
- QE-NOB-1.0 remains NO-GO and unchanged. No QE-NOB-2.0 candidate has yet been backtested for fitness or shown profitable; no tester branch/report is created, per the user's explicit instruction.


### QE-NOB-2.0 runtime checkpoint — 2026-10-22 21:05 IST

The structural-discovery branch now has tested components for typed strategy grammar, bounded candidate generation, point-in-time NIFTY OHLC features, next-bar signal timing, and an OHLC option simulator with modeled fees/slippage and same-session handling. Recent passing workflows include grammar/cache-audit #39802894371, standalone feature audit #39802894311, candidate generator #39805233976, feature builder #39805843560, signal evaluator #39806277479, and simulator #39806376781. Expiry-family normalization has been committed; its focused regression workflow #39806440507 is queued.

- [Current phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md)
- [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)
- [Interaction/activity log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/INTERACTION_LOG_V2.md)
- [Point-in-time feature builder](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/feature_builder_v2.py)
- [Option simulator](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/option_simulator_v2.py)
- [Bounded acquisition/cache audit workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-data-audit.yml) · [Current acquisition run #39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257)

**Evidence boundary:** acquisition is still running, and the runtime cache has not yet passed the current Phase 2 audit. No QE-NOB-2.0 candidate has been fitness-scored on verified market data; there is no P&L result or profitable strategy claim. The execution gate remains false because rolling OHLC does not establish exact contract identity, historical bid/ask/depth, or broker fills. Search remains capped at 1,500 unique candidates and 20 generations. No tester branch/report will be created, per the user's instruction.


### QE-NOB-2.0 test gate — 2026-10-22 21:15 IST

The bounded discovery runner now has passing automated tests for compilation, chronology/statistical utilities, candidate generation and training-only fitness: [runner tests #39807638261](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39807638261), [candidate/training fitness tests #39807602936](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39807602936). The runner separates training, validation and final OOS blocks; feature eligibility is determined from training-period coverage only; it applies block-bootstrap uncertainty, Holm correction and cost stresses to frozen finalists.

**Still blocked:** the bounded Dhan/cache acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) is still running. No real-data discovery result, OOS performance claim, or profitable strategy is available yet. Exact contract identity and executable bid/ask/depth remain unverified, so the execution gate stays FAIL.


### QE-NOB-2.0 automatic discovery handoff — 2026-10-22

The acquisition workflow is now wired to run the bounded QE-NOB-2.0 discovery/validation runner automatically after successful cache acquisition and audit; its queued follow-up is [run #39808171927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808171927). The runner rejects caches with JSON parse failures or missing underlying/option files, and its cache-gate regression passed in [run #39808407294](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808407294). A lighter CI dependency set is being applied to reduce unnecessary test setup time.

**Current evidence boundary:** source acquisition [run #39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) is still in progress. The discovery runner has passed software tests but has not produced a verified market-data result. No strategy is claimed profitable, and execution remains blocked by missing exact contract/quote/fill evidence.


### QE-NOB-2.0 continuation checkpoint — 2026-10-22 21:24 IST

The latest live workflow inspection confirms QE-NOB-2.0 is **still in progress, not complete**:

- [Acquisition/cache-audit run #39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) remains in progress at source acquisition; cache audit and sanitized result upload have not run yet.
- [Automatic follow-up #39808171927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808171927) remains pending and has produced no discovery result.
- [Discovery-runner tests #39808626484](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808626484) passed. This is software-test evidence only, not evidence of market-data sufficiency, positive OOS P&L, or executability.
- [QE-NOB-2.0 phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md), [error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md), and [activity log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/INTERACTION_LOG_V2.md) record this checkpoint.

**Current disposition:** Phase 2 remains open; empirical discovery is blocked pending cache audit; execution remains FAIL until exact contract identity and executable quote/fill evidence are verified. No QE-NOB-2.0 profitability result is currently verified. No tester branch/report will be created, per the recorded instruction. The bounded workflow remains responsible for automatic handoff; manual workflow launch is not required.


### QE-NOB-2.0 external-source audit — 2026-10-22

The Phase 2 public-source review is recorded in [SOURCE_CATALOG_V2.md](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md). Official NSE/Nifty Indices reports are candidates for daily index, India VIX and FII/DII context; Cboe/FRED are candidates for lag-aligned daily global volatility/macro context. These have not been added to candidate fitness yet.

Two public Hugging Face options datasets were found but not imported: one has a non-specific 'other' license; the other is CC BY-NC 4.0 and therefore not approved for a trading-oriented evidence pipeline without separate rights. A public GitHub NIFTY OHLC dataset is only a candidate for underlying-bar cross-check after provenance and row-level validation.

**Gate unchanged:** external-source discovery does not complete runtime acquisition. [Acquisition #39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) is still the controlling data gate; [automatic follow-up #39808171927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808171927) has no verified discovery result yet. Phase 2 remains open and execution remains FAIL.


### QE-NOB-2.0 acquisition stall remediation — 2026-10-23

The acquisition client and workflow have been hardened after the original data job remained on its source-acquisition step for multiple hours without any visible progress output.

- [Updated acquisition client](https://github.com/vishnuvcr/Naked-Options-v2/commits/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/run_research.py) now requests only the v2-supported ATM-to-OTM2 offset range (-2 through +2), writes progress lines every 25 requests, uses bounded request timeouts/retries, and halts after ten consecutive source request failures.
- Empty option payloads are not cached as valid source files. The acquisition result now requires all planned request groups, zero request failures, and at least 80% non-empty option responses; partial option or underlying acquisition exits non-zero, preventing the downstream discovery step from running.
- [Acquisition workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-data-audit.yml) now allows at most three resume passes, stops early if no cache progress is detected, applies a 160-minute acquisition-step timeout, and automatically runs when the source client or its regression tests change.
- Regression tests cover the supported offset domain, timeout/retry bounds, stop-after-consecutive-failure behavior, empty-data coverage gating, and fail-closed acquisition readiness. [Source-catalogue note](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md) has the revised estimated request count (~1,220 for two expiry families; this is not a count of completed API calls).

**Verification is pending.** The original active workflow #39803647257 was launched with the old client and cannot be patched mid-run. The queued successor #39808171927 remains the intended first run to check out the current developer branch and test the recovery changes. Until its acquisition audit succeeds, Phase 2 remains open, empirical discovery remains blocked, and execution remains FAIL. No profitable strategy result is claimed.


### QE-NOB-2.0 recovery queue update — 2026-10-23 00:13 IST

The original acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was still reported in progress at the last poll, while [the previous queued follow-up #39808171927](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39808171927) was cancelled at 18:41:39 UTC by GitHub concurrency handling as branch updates accumulated. The latest remediation commit [9ef5f663](https://github.com/vishnuvcr/Naked-Options-v2/commit/9ef5f663122a8b802445a618e3bf91f022590d65) has a pending GitHub Actions check suite with no started check runs yet. The corrected run therefore has not been tested; it is waiting for the active concurrency slot. See the [updated phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md).


### QE-NOB-2.0 recovery-code CI result — 2026-10-23 00:18 IST

- The standalone [source-client regression workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-source-client-tests.yml) passed: [check suite for commit 8241ef05](https://github.com/vishnuvcr/Naked-Options-v2/commit/8241ef05cea41a75a309f2cec979f0b69587a2e7/checks) completed successfully. This covers code compilation and unit tests, not market-data acquisition or profitability.
- At the same poll, acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was still reported in progress with no API update since 15:18:56 UTC. The corrected acquisition suite remains pending behind the concurrency group.
- Research gates remain unchanged until the source-acquisition workflow has an actual result: Phase 2 open, empirical discovery blocked, and execution FAIL.


### QE-NOB-2.0 partial-cache audit and strike-scope amendment — 2026-10-23

The stalled acquisition run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257) was cancelled through the one-time recovery handoff after exceeding the expected runtime. Its always-run audit, cache-save and artifact upload steps succeeded. Inspection of the uploaded cache audit found 716 historical weekly option files, three option probes, one underlying probe, **no historical underlying series**, and **no historical monthly option history**. A JSON-parse audit status of PASS must not be interpreted as complete market data.

Based on that observed source throughput—not any candidate performance result—the active QE-NOB-2.0 universe has been amended to ATM and one-step OTM only. OTM2 has been removed from the grammar/seeder, and source requests are now limited to offsets -1/0/+1. The amended five-year option grid is approximately 732 request groups, with around 425 expected to remain after reusable cache files, plus up to 23 underlying-history chunks and probes. See the [amended discovery plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md), [source catalogue](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md), [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md), and [error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md).

The independent source-client CI passed on the earlier timeout/progress fix. The amended grammar/data source changes have their own automatic regression checks pending. Phase 2 remains open until a **new** acquisition audit verifies actual historical underlying and option cache coverage. Empirical discovery remains blocked and the execution gate remains FAIL.


### QE-NOB-2.0 ATM/OTM1 amendment — regression checkpoint

The cached-data audit confirmed that the cancelled initial acquisition had 716 historical weekly option files but no historical underlying series and no historical monthly option history. The developer protocol was formally narrowed to ATM and one-step OTM (offsets -1/0/+1) before restarting; OTM2 is excluded from candidate generation.

- [The amended protocol](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md) and [source catalogue/cache accounting](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md) document the scope and estimated remaining request count.
- Grammar CI passed on [check suite #107968717033](https://github.com/vishnuvcr/Naked-Options-v2/commit/ada4d63039e4449465d6c7c4bb23230b844df240/checks).
- The first source-client regression check failed because the fail-fast test fixture supplied only six failing requests in one chunk, below the ten-consecutive-failure threshold. The exact log showed 17 passed and one failed; the test was corrected to provide two contiguous chunks in [commit e9982ddc](https://github.com/vishnuvcr/Naked-Options-v2/commit/e9982ddc1ee7cabb0a5aa3a581c1441df16b5cfb). Re-run source-client CI [#39836310701](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310701) passed: Python compilation and all 18 pytest tests succeeded in 1.24 seconds.
- Phase 2 remains open until the restarted run audits real historical underlying and option data. Empirical discovery is blocked, and the execution gate remains FAIL.


### QE-NOB-2.0 source-client CI diagnosis correction

Inspection of failed source-client run [#39835953946](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39835953946) showed **17 passed, 1 failed**. The failure was a test-fixture gap: a single chunk has only six requests under the ATM/OTM1 scope and cannot reach the ten-consecutive-failure stop threshold. The fixture now spans two chunks so the early-stop behavior can be verified. This was not a market-data or strategy-performance failure; the next CI run must confirm the correction.


### QE-NOB-2.0 latest recovery handoff — source-client tests passed

The corrected ATM/OTM1 source client and its regression tests now pass [workflow #39836310701](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310701): 18 tests passed in 1.24 seconds, including the cache-resume accounting and early-stop behavior. The acquisition workflow [#39836310700](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836310700) is still pending behind an older in-progress recovery run that checked out the previous scope. A one-time, message-gated workflow handoff is being used to release that slot; the next acquisition run must restore the saved partial cache and verify historical underlying and option data before discovery.


### QE-NOB-2.0 cancellation-target correction and resume

The ATM/OTM1 acquisition [#39836599391](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39836599391) reached 318/732 planned option request groups before a one-time cancellation workflow mistakenly targeted that run instead of the original stale run. The partial cache was saved and the audit artifact uploaded; logs showed 313 cached requests, one downloaded valid option file and four timeouts. No historical underlying series was acquired.

The cancellation workflow's default run ID is now corrected to the original cancelled run [#39803647257](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39803647257), and the data workflow has been retriggered from [commit e02851ad](https://github.com/vishnuvcr/Naked-Options-v2/commit/e02851ad7736c111398bb7d2903cc3f0cb9891c0). Source-client tests passed (18/18), but Phase 2 remains open until the new run proves actual historical underlying and option coverage; empirical discovery remains blocked and execution remains FAIL. Details are recorded in the [error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md), [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md), and [interaction log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/INTERACTION_LOG_V2.md).


### QE-NOB-2.0 weekly-only expiry amendment — 2026-10-23

The cache audit found no historical monthly option cache, so the bounded discovery protocol is now restricted to WEEK1 (nearest weekly expiry), with ATM/OTM1 only. MONTH1 is excluded from the config, grammar/mutation generator and acquisition source gate. This is a data-coverage amendment—not a performance-based selection—and is documented in the [updated discovery plan](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md), [source catalogue](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md), [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md), and [error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md).

Latest regression runs passed: [source client #39838112165](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838112165), [candidate generator #39838066721](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838066721), [discovery runner #39838066761](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838066761), [option simulator #39838060682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838060682), [signal evaluator #39838060728](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838060728), and [grammar validation #39838074982](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838074982). The current acquisition [#39837698610](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39837698610) started before the weekly-only amendment, so it is not eligible to pass the updated gate. The next pending workflow must use WEEK1-only scope and restore the saved cache before discovery can begin.


### QE-NOB-2.0 weekly-only recovery — 2026-10-23

The source acquisition is now being restarted against the **weekly-only, ATM/OTM1 protocol**, with a clean v2 report namespace and the partial cache retained. The previous report artifact had a stale v1 acquisition summary, so it is not accepted as completion evidence.

- [Current weekly-only bounded run #39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) has restored the existing cache and is installing dependencies before source-client and active grammar/simulator tests. It will then resume the missing WEEK1 option files and acquire historical NIFTY 5-minute underlying bars.
- Latest cache audit: 728 historical weekly option files across offsets -3..+3; 314 historical files in allowed offsets -1/0/+1; no historical underlying candles; no historical monthly-option files. Approximately 52 allowed weekly option groups and up to 23 underlying history chunks remain by file-count estimate; the new run's logs/audit determine actual counts.
- [Weekly-only protocol amendment](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/OPEN_STRATEGY_DISCOVERY_PLAN.md), [source catalogue/cache audit](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/SOURCE_CATALOG_V2.md), [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md), and [error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md) record the reasoning and prior cancelled attempts.
- The acquisition workflow now runs the source-client regression tests plus the active v2 grammar, candidate, feature-builder, simulator, and discovery test suites before attempting data acquisition. Fresh summaries are written to reports/quant_evolve_nob_v2; the legacy cache remains at data/cache/quant_evolve_nob_v1 so previously downloaded data can be reused.
- **Current research gate remains open:** Phase 2 does not close until the fresh artifact shows sufficient historical underlying and option data. Empirical discovery runs automatically only after the source client and cache audit pass. Contract identity and executable quote/fill evidence remain unresolved; execution gate stays FAIL.


### Current resume state — eligible WEEK1-only acquisition

The eligible [weekly-only acquisition workflow #39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) has passed its pre-acquisition source-client and full grammar/feature/simulator/discovery regression gates, restored the cache, and is currently in the acquisition step. Its own fresh acquisition summary and feature audit have not yet completed, so there is no data-coverage conclusion or prediction result to report yet. Phase 2 remains IN PROGRESS; Phase 5 discovery remains blocked until the fresh source gate passes. The cancelled-run summary files were identified as stale v1 outputs and are explicitly disqualified from evidence (QE-NOB2-E031).


### QE-NOB-2.0 monthly-cache evidence correction — 2026-10-23

The latest interrupted-run artifact audit refines the earlier statement that the monthly cache was empty: it actually contains **11 historical MONTH1 files, all in the first two 30-day chunks**. That is roughly 3% of the 366-file ATM/OTM1 five-year monthly grid and does not amount to usable full-period monthly coverage. The active protocol remains WEEK1-only for the bounded run, while acknowledging the partial monthly files rather than claiming none exist.

The fresh weekly-only run [#39838508682](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39838508682) has restored the saved partial cache and passed the source-client plus active v2 grammar/candidate/feature/simulator/discovery test gates. It is now running the source-acquisition step. The actual acquisition summary and fresh cache audit have not yet been produced; Phase 2 remains open, discovery remains gated, and no profitability claim is supported.


## Dhan access-token automation (QE-NOB-2.0)

The active developer branch now includes a TOTP-based Dhan token bootstrap before QE-NOB-2.0 data acquisition. It requests a fresh 24-hour token and validates it against the Dhan profile endpoint; the token is scoped to that GitHub Actions job and is not printed or committed.

- Implementation branch: [QE-NOB-2.0 developer](https://github.com/vishnuvcr/Naked-Options-v2/tree/research/quant-evolve-nob-v2-discovery-developer)
- [Token helper](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/dhan_auth.py) · [RFC regression tests](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/test_dhan_auth.py) · [Acquisition workflow](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/.github/workflows/qe-nob-v2-data-audit.yml) · [Phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS_V2.md) · [Error log](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG_V2.md)

**Required setup:** enable TOTP in Dhan Web and add GitHub Actions repository secrets `DHAN_CLIENT_ID`, `DHAN_PIN`, and `DHAN_TOTP_SECRET`. Do not paste or commit these values. The live authentication test is pending those secrets; Phase 2 data acquisition remains blocked until the token/profile and market-data gates pass.

## QE-NOB-2.0 data acquisition status — 2026-10-23

- Dhan TOTP authentication is now validated by workflow [#39844476476](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39844476476).
- Historical option acquisition remains incomplete: three bounded passes ended with 363/366 option requests recorded and transient Dhan read timeouts. The cache audit passed parsing checks, but prediction discovery correctly remained blocked.
- A bounded retry mitigation (40-second timeout, four attempts, 2/4/8-second backoff) and regression assertion updates are committed on the developer branch. See [phase status](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/PHASE_STATUS.md) and [error log QE-NOB2-E010](https://github.com/vishnuvcr/Naked-Options-v2/blob/research/quant-evolve-nob-v2-discovery-developer/research/quant-evolve-nob/ERROR_LOG.md). Do not treat cache parse success as research completion; wait for the acquisition rerun and data quality gates.


## TradingAgents benchmark feasibility (2026-10-25)

A separate feasibility review is underway on [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents), pinned to upstream commit [e8f5503](https://github.com/TauricResearch/TradingAgents/commit/e8f5503e9b86d5c2710b0c76b1f686703968c9df). Static review is complete; the pinned upstream test workflow is now configured, and no upstream test pass is claimed until its run is inspected. The framework is only a candidate benchmark, not a replacement for the preregistered ZigZag++ experiment.

- [Feasibility report](research/tradingagents/FEASIBILITY_REPORT.md)
- [Test plan and gates](research/tradingagents/TEST_PLAN.md)
- [Pinned upstream compatibility workflow](.github/workflows/tradingagents-compatibility.yml)

**Current decision:** CONDITIONAL CANDIDATE. NIFTY-specific data availability, 10:00 IST timestamp alignment, point-in-time input integrity, and a structured UP/DOWN/ABSTAIN forecast contract remain untested. No accuracy result exists.


### TradingAgents benchmark update (2026-10-25)

Pinned upstream software validation passed in [GitHub Actions run #40129883044](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40129883044): dependencies installed, unit tests passed, Ruff passed, and clean-install imports passed. This is not evidence of NIFTY prediction accuracy. A live Yahoo `^NSEI` daily/5-minute diagnostic probe has been added and awaits its next workflow run.

- [Feasibility report](research/tradingagents/FEASIBILITY_REPORT.md)
- [Staged test plan](research/tradingagents/TEST_PLAN.md)
- [NIFTY Yahoo probe](research/tradingagents/probe_nifty_yahoo.py)
- [Compatibility workflow](.github/workflows/tradingagents-compatibility.yml)

Per user instruction, no independent tester role/branch/gate is used. No NIFTY accuracy score exists.



**Latest data-probe result:** [run #40130052739](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130052739) successfully retrieved 21 daily and 375 five-minute `^NSEI` rows with timezone-aware timestamps and OHLC columns. This validates only a short live data-shape sample—not historical expiry-cutoff coverage or point-in-time correctness. TradingAgents remains a conditional benchmark candidate, with no prediction accuracy claim. See the [updated feasibility report](research/tradingagents/FEASIBILITY_REPORT.md) and [test plan](research/tradingagents/TEST_PLAN.md).



### TradingAgents forecast contract (2026-10-25)

Added a strict [forecast contract](research/tradingagents/FORECAST_CONTRACT.md), [validator](research/tradingagents/forecast_contract.py), and [unit tests](research/tradingagents/test_forecast_contract.py). The contract requires explicit timezone-aware cutoff/target times, UP/DOWN/ABSTAIN, model/prompt identity, and an input manifest hash. CI now executes the contract tests; latest result is pending. Source audit found that the standard TradingAgents Yahoo tool uses date-based windows and strips timezone information in its formatted output, so it cannot alone certify a 10:00 IST intraday cutoff. A frozen market-only adapter is required before any historical evaluation.



**Latest CI:** [Run #40130735394](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40130735394) passed forecast-contract tests, pinned TradingAgents install/tests/lint/import, and the Yahoo probe. Added [frozen market snapshot validator](research/tradingagents/market_snapshot.py), [its tests](research/tradingagents/test_market_snapshot.py), and [gate notes](research/tradingagents/MARKET_SNAPSHOT_GATE.md); CI for this newest change is pending. These checks do not yet constitute a historical forecast backtest.



**Snapshot validator CI result:** [Run #40131047411](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131047411) completed successfully with the new snapshot tests. This validates the code against synthetic cases only; historical source/session certification and model integration remain blocked. No prediction score is available.



### NIFTY data acquisition update (2026-10-25)

Data acquisition completed via the free Yahoo Finance fallback after Dhan token validation returned HTTP 401. [Successful workflow run #40131619468](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131619468) produced artifact `zigzag-nifty50-data-40131619468` (expires 2026-11-23): daily 1,235 rows (2021-10-25–2026-10-23), 1m 2,611 rows (2026-10-14–2026-10-23), 5m 4,496 rows and 15m 1,500 rows (both 2026-07-29–2026-10-23), 60m 5,075 rows (2023-11-08–2026-10-23), and 30m derived 719 rows. The intraday history is incomplete for a five-year study. Yahoo daily timestamps are midnight date labels, not certified close times; no formal prediction evaluation has been run. See the [TradingAgents feasibility report](research/tradingagents/FEASIBILITY_REPORT.md) and [test plan](research/tradingagents/TEST_PLAN.md).



### Expanded intraday data coverage (2026-10-25)

A second free-source acquisition found a public [five-year NIFTY 50 5-minute archive](https://github.com/voletiramu/nse-fno-1min-data/releases/tag/indices-v1.0.0). [Workflow run #40131891819](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40131891819) succeeded and produced artifact `zigzag-nifty50-data-40131891819` (ID 12575426805, expires 2026-11-23). The normalized 5-minute series has 92,876 rows from 2021-04-01 to 2026-04-21; derived 30-minute series has 14,849 rows. Source and normalized SHA-256 hashes are logged in the workflow output. This improves intraday coverage but remains provisional: official session completeness, source provenance and candle timestamp semantics are not yet certified, so formal model scoring remains blocked. See [detailed feasibility report](research/tradingagents/FEASIBILITY_REPORT.md) and [test plan](research/tradingagents/TEST_PLAN.md).



## Current execution status — 2026-10-25

The current developer branch continues with the acquired five-year public 5-minute archive rather than broadening data search. Artifact 12575426805 was inspected locally: 92,876 rows, 1,244 dates, sorted/unique timestamps and no invalid OHLC rows; 1,236 dates have 75 regular-clock bars. Six weekend dates and 48 out-of-clock rows need official-session classification. The existing Yahoo fallback has no timestamp overlap with this archive, so independent price parity remains untested. A reusable diagnostic script, [audit_public_5m.py](research/zigzag-expiry-direction/audit_public_5m.py), is wired into the acquisition workflow. **Prediction scoring remains blocked until official session/expiry mapping and exact ZigLib causal timing are verified; no performance result is claimed.**

## Final research disposition — 2026-10-25

The detailed audit workflow passed in [run #40132605202](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40132605202). The public five-minute archive has 92,876 structurally valid rows, but eight dates need official session classification and the combined weekend/out-of-clock diagnostic flags 315 rows (including special evening sessions). There is no timestamp overlap with the current Yahoo fallback. Most importantly, the exact imported ZigLib implementation and causal signal-availability timing could not be verified. To avoid look-ahead bias, this research run is closed as **NO-GO FOR SOURCE-FAITHFUL PREDICTION SCORING**. This is not evidence the indicator is ineffective; no predictions were scored. See [final results ledger](research/zigzag-expiry-direction/RESULTS.md), [manuscript outcome](research/zigzag-expiry-direction/MANUSCRIPT.md), and [error log](research/zigzag-expiry-direction/ERROR_LOG.md). Restart criteria are documented in the phase status and error log.

## Additional source investigation — 2026-10-25
Located a public [ZigZag++ wrapper source mirror](https://github.com/rohitbhure65/pine-scripts/blob/master/zigzag.pine). It confirms the parameters and wrapper's repaint setting, but imports rather than includes the ZigLib implementation. It therefore does not resolve causal pivot timing. Official daily historical-index pages are also confirmed ([NSE reports](https://www.nseindia.com/all-reports), [Nifty Indices reports](https://www.niftyindices.com/reports)); daily bars alone do not provide the required 10:00 intraday target. Research remains no-go for scoring until source-faithful signal timing and market-data gates pass.

## 2026-10-25 — Proceed with available data

User authorized continued work using the available dataset. Downloaded audit artifact [#12575253300](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40132605202/artifacts/12575253300) and confirmed it contains 1m/5m/15m/30m-resampled/60m/daily CSVs and diagnostic reports. Data availability enables further diagnostics but does not validate exact ZigLib v1 causal timing or the official session/expiry target table. **No source-faithful prediction metrics are claimed.** The primary protocol is unchanged; a generic ZigZag proxy must not be presented as the TradingView indicator.

- [Updated results ledger](research/zigzag-expiry-direction/RESULTS.md)
- [Updated manuscript](research/zigzag-expiry-direction/MANUSCRIPT.md)
- [Updated phase status](research/zigzag-expiry-direction/PHASE_STATUS.md)
- [Updated error log](research/zigzag-expiry-direction/ERROR_LOG.md)
- [Updated interaction log](research/zigzag-expiry-direction/INTERACTION_LOG.md)


## Workflow reliability correction — 2026-10-25

The benchmark persistence step was hardened so a non-blocking second-source parity audit cannot cause a later `git add` failure merely because its optional JSON artifact was not produced. See [error log NP-011](research/nifty-prediction/ERROR_LOG.md) and [phase status](research/nifty-prediction/PHASE_STATUS.md). The correction is committed, but Actions execution remains unverified and no new production scores are claimed.
