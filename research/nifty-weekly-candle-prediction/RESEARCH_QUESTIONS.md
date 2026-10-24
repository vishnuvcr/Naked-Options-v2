# Research Questions and Preregistered Hypotheses — NWCP-1.0

## Main research question

Can information available by 10:00 IST on the first trading day after the previous actual NIFTY weekly expiry predict whether NIFTY 50 spot will close above or below that 10:00 value on the following weekly expiry?

## Confirmatory questions

**RQ1 — Predictability:** Does the best validation-selected, frozen classifier achieve balanced accuracy greater than 0.50 on the final chronological holdout and outperform the training-fold majority-class baseline?

- H0: OOS balanced accuracy is no greater than chance, or improvement over baseline is not distinguishable from zero under the preregistered block-bootstrap comparison.
- H1: Balanced accuracy exceeds 0.50 and paired improvement over baseline has a positive 95% block-bootstrap interval, subject to multiplicity correction and integrity gates.

**RQ2 — Incremental indicator value:** Do point-in-time technical indicators, including audited open-source Pine Script formula ports, improve prediction over lagged price/return/range/volatility features alone?

- H0: Technical indicators add no repeatable OOS improvement.
- H1: They add repeatable improvement under the frozen protocol and sealed OOS, after Holm correction.

**RQ3 — Evolutionary discovery:** Does bounded QuantEvolve-style hypothesis-driven search produce models/features that outperform conventional regularized models without concentrating in one fragile family or search artifact?

- H0: Evolutionary search fails to improve OOS performance over the strongest non-evolutionary baseline.
- H1: At least one evolved model improves the primary metric and survives OOS, multiplicity and integrity gates.

**RQ4 — Original indicators:** Do AIA, OWPE, MHDA, VSRP, CMRP or TCD add information beyond conventional indicator families?

- H0: No original indicator group provides robust incremental value.
- H1: At least one pre-specified original indicator has repeatable incremental value in ablations after correction.

**RQ5 — Regime stability:** Is performance stable across chronological blocks and expiry calendar regimes, including the change in weekly expiry convention?

This is descriptive unless power permits predeclared tests. No model is accepted solely because it succeeds in one regime.

## Exploratory questions

- Does point-in-time global overnight information add to Indian price features?
- Do India VIX and lagged option-derived features add value after data-quality gates?
- Are predictions differently calibrated in high/low volatility windows?
- Do holiday-shift/calendar indicators explain variation in interval length?

## Primary endpoint

Balanced accuracy on an untouched chronological test period. Secondary endpoints: MCC, accuracy, class-specific recall, ROC-AUC, Brier score and log loss. The holdout is used once after model and feature choices freeze. A positive result requires the integrity and statistical gates in RESEARCH_PLAN.md.

## Exclusions

No options P&L, options strategy, position sizing, stop/target optimization, live execution, P&L optimization, or claim that prediction accuracy implies trading profitability. Earlier repository study results are excluded from NWCP-1.0 evidence.
