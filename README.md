# Data Quality and Anomaly Monitoring System

## Problem
Detect broken or drifting data before it reaches dashboards and models.

## Dataset and provenance

`data/raw/sample_events.csv` is synthetic and intentionally contains a duplicate, a missing customer ID, and a negative amount. Reuse sample inputs from the other project directories or generate additional test faults; keep sensitive or large raw datasets out of Git.

### Download a Kaggle quality-check dataset

The optional downloader defaults to `uciml/adult-census-income`. Review the dataset license and terms first. Install the Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save `kaggle.json` to `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Run `python scripts/download_kaggle.py`; files go to ignored `data/external/`. The census schema differs from the event demo, so map/validate its columns before running the quality gate. Do not commit raw personal or sensitive data.

## Run the ETL quality gate

From this directory, run `python src/main.py`. It checks required columns, duplicate event IDs, missing values and negative amounts, writes accepted records to `data/gold/clean_events.csv`, routes rejected rows with reasons to `quarantine.csv`, and writes counts to `quality_report.json`. Runs replace outputs deterministically. Use `--input` and `--output-dir` to point to a different dataset. Run checks with `python -m pytest -q tests`.

## Stack
Great Expectations, Python, scheduler, Slack/email alerts

## Architecture
- Bronze / raw ingestion layer
- Silver / cleaned and validated data layer
- Gold / feature or serving layer
- Monitoring / validation and retraining feedback loop

## DE tasks
1. Ingest raw data with versioned file naming and timestamps.
2. Build idempotent and incremental transformations.
3. Add data quality checks and freshness alerts.
4. Create a reproducible run order using a Makefile or run script.
5. Store outputs in a warehouse, lake, or streaming sink with clear contracts.

## DS tasks
1. Run EDA and validate assumptions about seasonality, drift, and user behavior.
2. Benchmark a baseline model before trying a stronger approach.
3. Use proper time-based splits and avoid leakage.
4. Log experiments, tuning choices and key metrics.
5. Report limitations and next steps in a production-focused way.

## Deliverables
- Reproducible pipeline or app
- Tests for transformation and validation logic
- Dashboard, API, or report showing outputs
- Clear business summary with measurable impact

## Recommended repository structure
`	ext
data-quality-and-anomaly-monitoring/
+-- README.md
+-- requirements.txt
+-- Makefile
+-- .gitignore
+-- src/
+-- tests/
+-- notebooks/
+-- docs/
`

## Resume line
Built a data-quality and anomaly-monitoring stack that catches schema, freshness and distribution issues before they impact downstream analytics.

### Kaggle dataset download

Install Kaggle CLI with `python -m pip install kaggle`, create an API token in Kaggle account settings, and save it locally as `%USERPROFILE%\.kaggle\kaggle.json` on Windows or `~/.kaggle/kaggle.json` on macOS/Linux. Never commit or share the token. Run `python scripts/download_kaggle.py`; downloaded files go to Git-ignored `data/external/` and are not published to this repository. Review the dataset license and Kaggle terms before use; large datasets may require adapting the sample input schema.
