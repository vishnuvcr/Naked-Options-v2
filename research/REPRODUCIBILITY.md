# Reproducibility guide

Research version: NIFTY-PRED-1.0.

## Run the pipeline

The exact interface will be kept synchronized with committed scripts.

1. Use the Python version pinned in GitHub Actions and install requirements-research.txt.
2. Add DHAN_ACCESS_TOKEN as a GitHub Actions repository secret only. HF_TOKEN is optional and used only for an identified source in the manifest.
3. Run acquisition: python scripts/acquire_data.py --start 2007-01-01.
4. Run validation: python scripts/validate_data.py --input data/raw/nifty50_daily.csv.
5. Run experiments: python scripts/run_experiments.py.
6. Run tests: python -m pytest -q.
7. Review data/manifest.json, reports/metrics.csv, reports/predictions.csv, reports/significance.csv, reports/experiment_status.csv and figures.
8. Use the recorded Git SHA, data-source hashes, source timestamps, seed, split boundaries and package versions to reproduce outputs.

If script interfaces change, update this guide and append a reason to ERROR_LOG / interaction log. Never put credentials into shell history, logs, artifacts or commit messages. Workflow output must mask secrets.

## Expected outputs

- data/raw: validated NIFTY daily series and any permitted auxiliary source files.
- data/manifest.json: endpoint/source, timestamps, date coverage, hashes, row counts, missingness and source acquisition result.
- reports: per-origin predictions with target date, horizon, model, prediction, benchmark and observation; metrics with sample counts; statistical test outputs; catalogue status.
- figures: actual-versus-prediction diagnostics, relative errors and feature/regime plots.
- research/EXPERIMENT_LOG.md and research/ERROR_LOG.md: outcome and failure records.
- docs or GitHub Pages: publication rendering without secrets or non-redistributable raw data.

A blocked source must be documented with non-secret request metadata and a free-source alternative. Do not hand-enter missing values to make the pipeline run.
