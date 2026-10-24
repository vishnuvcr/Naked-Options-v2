# Research Questions and Hypotheses

- **RQ1:** Does the latest confirmed ZigZag pivot class at the defined cutoff predict next-interval NIFTY 50 expiry direction?
- **RQ2:** Does it outperform the majority-class and 50% baselines on chronological out-of-sample data?
- **RQ3:** Is performance materially different for UP versus DOWN outcomes or across volatility regimes?
- **RQ4:** What fraction of intervals has a causally eligible pivot and valid target data?
- **H0:** Out-of-sample balanced accuracy is no better than the 50% baseline, subject to sampling uncertainty.
- **H1:** Out-of-sample balanced accuracy exceeds the 50% baseline and remains robust under dependence-aware uncertainty estimation.
- **Guardrail:** A positive result requires causal signal timing, source provenance, valid expiry mapping and a sealed chronological test. Otherwise report DATA-LIMITED.
