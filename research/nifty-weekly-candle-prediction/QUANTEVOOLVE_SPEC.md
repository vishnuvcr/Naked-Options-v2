# QuantEvolve-Style Discovery Specification — NWCP-1.0

## Purpose

Adapt quality-diversity and hypothesis-driven evolutionary search described in [QuantEvolve, arXiv:2510.18569](https://arxiv.org/abs/2510.18569) to binary weekly-expiry direction prediction. This is not a trading strategy or return-optimization objective.

## Safety and reproducibility

- Never execute arbitrary LLM-generated source, shell commands or evolved code with access to secrets.
- Represent candidates as typed JSON/AST expressions evaluated by a small allowlisted interpreter. Allowed operators include validated feature references, rolling transforms with minimum-history constraints, comparisons/thresholds, Boolean combinations and deterministic scores.
- No future price, target-derived feature, final-test statistic or source field published after 10:00 is accessible to candidate evaluation.
- Use fixed seeds and persist each candidate definition, parent IDs, mutation, generation, family, training/validation metrics, warnings and rejection reason.
- Deduplicate by normalized expression hash; maintain diversity across families/complexity/performance.

## Search budget

Hard upper bound: 500 distinct expressions, 20 generations, and four seeds at most (1729, 20261024, 8675309, 31415927). Stop if three generations in a row show no validation improvement. Reduce the budget if fewer than 200 valid samples or training folds are too small.

## Fitness and selection

- Training-only fitness: balanced accuracy with penalties for complexity and excessive missingness.
- Validation-only selection from fixed candidates using blocked forward splits.
- Promote only if it improves the primary metric across more than one chronological validation block; otherwise retain simple baselines.
- Access the OOS test once after selection freezes. Never mutate or retune using OOS results.
- Calibrate probabilities only within training folds or explicitly report them uncalibrated.

## Quality-diversity map

Maintain diversity on feature family, expression complexity, directional class behavior and robustness across validation blocks. The map contains price/return, technical, volatility, global, derivatives, calendar and original-indicator families. Fitness is not profitability or proof of prediction skill; evolution only proposes candidates for statistical testing.

## Required artifacts

Configuration/code/dependency versions/seeds; full candidate archive and normalized hashes; generation-level diversity history; train/validation metrics for all candidates; selected-candidate rationale; feature-family ablations; runtime/budget/failure/rejection summaries; and sealed OOS report produced only in the validation phase.
