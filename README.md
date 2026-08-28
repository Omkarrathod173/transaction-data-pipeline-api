# Transaction Data Automation & Reporting API

A portfolio-ready Python project aligned with the skills practiced during a Python Developer Internship: file-based ETL, Pandas transformations, SQLite database connectivity, Flask REST APIs, JSON, Postman, testing, and Git/GitHub.

## Internship context

**Organization:** Elevate Labs  
**Role:** Python Developer Intern  
**Period:** 22 Sep 2025 – 08 Nov 2025  
**Recognition:** Best Performer / Certificate of Completion

> This repository uses synthetic transaction data for portfolio demonstration. It does not contain or claim to contain confidential Elevate Labs data.

## Problem

Recurring transaction exports often need manual cleanup before reporting. This project automates the workflow: ingest a CSV, validate and clean records, generate KPIs, store reporting-ready data in SQLite, and expose the results through a Flask API.

## Architecture

```text
CSV source
   ↓
Extract + schema validation
   ↓
Pandas cleaning / transformation
   ↓
Data-quality report + logging
   ↓
SQLite reporting database
   ↓
KPI + regional reports
   ↓
Flask REST API
   ↓
JSON responses / Postman
```

## Technologies

Python, Pandas, NumPy, SQLite, Flask, JSON, pytest, Postman, Git, GitHub, VS Code/Jupyter.

## Run it

Use Python 3.12+.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src\run_pipeline.py
python -m pytest -q
python app\app.py
```

API endpoints:

- `GET /health`
- `GET /api/v1/kpis`
- `GET /api/v1/transactions?limit=10`
- `GET /api/v1/reports/region`

## Outputs

Running the pipeline creates:

- `data/raw/daily_transactions.csv`
- `data/processed/clean_transactions.csv`
- `data/processed/data_quality_report.json`
- `data/processed/kpi_summary.json`
- `data/processed/regional_summary.csv`
- `data/transaction_reporting.db`

## Resume-ready wording

Use only claims you can reproduce and explain:

- Automated a Python/Pandas transaction ETL workflow with schema validation, deduplication and KPI generation, persisting reporting-ready data in SQLite.
- Built reusable Python modules and a Flask REST API to expose transaction KPIs and regional reports as JSON for internal reporting workflows.
- Added data-quality checks, logging and automated tests to catch source-data issues and improve pipeline reliability.

Do not claim that the synthetic project reduced a real company’s processing time unless you measured that during the internship.
