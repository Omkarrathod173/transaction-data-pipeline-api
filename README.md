# 🚀 Transaction Data Pipeline & REST API

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

An end-to-end transaction ETL data processing pipeline and reporting microservice. It extracts raw CSV records, performs data validation and transformations via Pandas, loads clean schemas into SQLite, and exposes business metrics through Flask REST API endpoints.

---

## 🛠️ Architecture Workflow

```text
[ Raw CSV Data ] ---> [ Pandas Cleaning & Rules ] ---> [ SQLite Persistence ] ---> [ Flask REST API ] ---> [ JSON KPI Outputs ]