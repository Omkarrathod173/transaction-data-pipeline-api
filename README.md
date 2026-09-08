# Transaction Data Pipeline & Reporting API

A production-style Python data pipeline that automates transaction data cleaning, validation, transformation, KPI generation, and reporting through a Flask REST API.

## Project Overview

This project simulates a real-world transaction reporting workflow where raw CSV data needs to be cleaned, validated, transformed, and converted into reporting-ready datasets.

The pipeline processes transaction data using Python and Pandas, stores the cleaned data in SQLite, generates business KPIs and regional summaries, and exposes the results through REST API endpoints.

## Workflow

```text
Raw Transaction CSV
        ↓
Schema Validation
        ↓
Data Cleaning & Transformation
        ↓
Data Quality Checks
        ↓
SQLite Database
        ↓
KPI & Regional Reports
        ↓
Flask REST API
        ↓
JSON Responses
```

## Key Features

* Automated CSV-based transaction ETL pipeline
* Schema validation and data-quality checks
* Duplicate and invalid-record handling
* Pandas-based data cleaning and transformation
* KPI generation for transaction reporting
* Regional performance summaries
* SQLite database for structured storage
* Flask REST API for accessing processed data
* JSON-based API responses
* Logging and error handling
* Automated tests using Pytest

## Tech Stack

| Category        | Technologies         |
| --------------- | -------------------- |
| Language        | Python               |
| Data Processing | Pandas, NumPy        |
| Database        | SQLite               |
| API             | Flask, REST API      |
| Testing         | Pytest               |
| Data Format     | CSV, JSON            |
| Tools           | Git, GitHub, VS Code |

## Project Structure

```text
transaction-data-pipeline-api/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   └── run_pipeline.py
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
└── ...
```

## API Endpoints

| Endpoint                            | Purpose                              |
| ----------------------------------- | ------------------------------------ |
| `GET /health`                       | Check API status                     |
| `GET /api/v1/kpis`                  | Retrieve transaction KPIs            |
| `GET /api/v1/transactions?limit=10` | Retrieve processed transactions      |
| `GET /api/v1/reports/region`        | Retrieve regional performance report |

## Example API Response

```json
{
  "status": "success",
  "total_transactions": 1000,
  "total_revenue": 1250000
}
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Omkarrathod173/transaction-data-pipeline-api.git

cd transaction-data-pipeline-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the ETL pipeline

```bash
python src/run_pipeline.py
```

### 6. Run tests

```bash
python -m pytest -q
```

### 7. Start the API

```bash
python app/app.py
```

The API can then be tested using a browser, Postman, or another API client.

## Data Pipeline Outputs

The pipeline generates:

* Clean transaction dataset
* Data-quality report
* KPI summary
* Regional performance report
* SQLite reporting database

## Business Value

The project demonstrates how raw operational transaction data can be converted into structured, reporting-ready information through an automated ETL workflow.

It combines data engineering and analytics concepts including:

* Data cleaning
* Data validation
* ETL automation
* KPI reporting
* Database storage
* REST API development
* Automated testing

## Project Highlights

* Built a reusable Python/Pandas ETL pipeline for transaction data processing.
* Implemented data validation, cleaning, deduplication and KPI generation.
* Stored reporting-ready data in SQLite for structured analysis.
* Developed Flask REST API endpoints to expose KPIs and regional reports.
* Added data-quality checks, logging and automated tests for pipeline reliability.

## Disclaimer

This project uses synthetic transaction data created for portfolio and demonstration purposes. It does not contain confidential company data.

## Author

**Omkar Banoth**

B.Tech, IIT Madras

Aspiring Data Analyst | Python | SQL | Excel | Data Analytics
