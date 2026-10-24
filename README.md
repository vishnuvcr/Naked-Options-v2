# NIFTY 50 prediction — current research status

## Current status — 2026-10-25

The daily next-session direction benchmark completed successfully in [GitHub Actions run #34](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/40139816710). A fixed set of momentum/reversal candidate rules has now been added to the same workflow; its new run/result is pending. No tester or tester branch is involved.

- [Research plan](research/nifty-prediction/RESEARCH_PLAN.md)
- [Phase status and verified scores](research/nifty-prediction/PHASE_STATUS.md)
- [Living research manuscript](research/nifty-prediction/MANUSCRIPT.md)
- [Repository integration ledger: all seven requested repos](research/nifty-prediction/REPOSITORY_INTEGRATION.md)
- [Targeted literature review](docs/research-literature/nifty_prediction_literature_review.md)
- [Daily data acquisition](research/nifty-prediction/acquire_daily_data.py)
- [Walk-forward model benchmark](research/nifty-prediction/evaluate_daily_models.py)
- [Candidate momentum/reversal rules](research/nifty-prediction/evaluate_candidate_rules.py)
- [Preliminary candidate-rule diagnostic](reports/nifty-prediction/candidate_rules_preliminary.json)
- [Automated candidate-rule results JSON](reports/nifty-prediction/candidate_rules.json) (pending the new Actions run)
- [Two-source OHLC parity audit](research/nifty-prediction/audit_source_parity.py)
- [Benchmark tests](tests/test_nifty_prediction_benchmark.py)
- [Error log](research/nifty-prediction/ERROR_LOG.md)
- [Daily benchmark JSON](reports/nifty-prediction/daily_benchmark.json)
- [Source parity audit JSON](reports/nifty-prediction/source_parity_audit.json)
- [Automated workflow](.github/workflows/nifty-prediction-benchmark.yml)

## Verified baseline results

The holdout contains 1,157 observations from 2022-02-14 through 2026-10-22, with 52.20% up sessions.

| Model/rule | Accuracy | Balanced accuracy |
|---|---:|---:|
| Majority-class baseline | 52.20% | 50.00% |
| Previous-session direction | 54.19% | 54.10% |
| Logistic regression | 52.46% | 52.53% |
| Random forest | 50.56% | 50.44% |
| Histogram gradient boosting | 53.15% | 52.82% |

The previous-session direction baseline has a 95% block-bootstrap balanced-accuracy interval of 51.30–56.81%. Learned models do not establish a reliable improvement over it. This is not a final no-strategy conclusion; small, hypothesis-driven rule experiments are next. Data is third-party and not exchange-certified.

## Requested repository use

All seven repository READMEs were reviewed and their intended research role and guardrails recorded in the [integration ledger](research/nifty-prediction/REPOSITORY_INTEGRATION.md): [Quantevolve](https://github.com/tarsyang/quantevolve), [TradingAgents](https://github.com/TauricResearch/TradingAgents), [astra-quant-agent](https://github.com/0xethanq/astra-quant-agent), [PySR](https://github.com/astroautomata/PySR), [arch](https://github.com/bashtage/arch), [tick](https://github.com/X-DataInitiative/tick), and [MAPIE](https://github.com/scikit-learn-contrib/MAPIE). Review is not falsely represented as full installation/execution: each repository has a specific compatibility and use gate. AstraQuant's OKX-native crypto executor and Quantevolve's Binance-oriented collector are not used as NSE data/execution connectors.

## Research safeguards

- Chronological evaluation; no random splits or look-ahead.
- No holdout tuning or unreported model selection.
- No fabricated results; failures and limitations belong in the [error log](research/nifty-prediction/ERROR_LOG.md).
- No trading strategy is called viable until net results account for slippage, brokerage, taxes/charges, turnover and execution timing (including Paytm Money costs where applicable).
- Workflow run status is verified from the actual Actions run, not inferred from a commit alone.

The older ZigZag expiry-direction study remains a separate track and does not block this daily prediction benchmark.


## Candidate-rule experiment (2026-10-25)

The existing workflow now evaluates 3-session momentum, 5-session momentum, 1-session reversal, 3-session reversal, a 20-session trend filter, and a lagged-volatility-conditioned rule. It writes a machine-readable report to `reports/nifty-prediction/candidate_rules.json`. The first verified benchmark still favors the previous-session direction baseline (54.10% balanced accuracy) over the three supervised models, none of which established a reliable improvement. Candidate results must be retrieved from an actual Actions run before a rule is selected. Gross index proxies are not net profitability; any viable candidate still needs instrument-specific execution and sourced brokerage, taxes/charges, slippage and turnover assumptions.


### Preliminary candidate outcome

A preliminary diagnostic on the same 1,157-session holdout found the 20-session trend filter at 53.90% balanced accuracy, below the previous-session-direction baseline at 54.10%. Three-session momentum scored 53.18%; five-session momentum 51.42%; one- and three-session reversal scored 45.99% and 46.82%; the volatility-conditioned rule scored 51.22%. These calculations are preliminary until confirmed by the automated Python report. Gross index proxy returns exclude trading costs and do not establish a usable strategy. The research remains active; no tester or tester branch.
