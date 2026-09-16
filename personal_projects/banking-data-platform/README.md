# Banking Data Platform

Data Engineering portfolio project focused on building an end-to-end banking data platform.

The project demonstrates the design and implementation of a modern data pipeline, covering API ingestion, cloud infrastructure, data lake architecture, distributed processing, data warehousing, transformation, orchestration, testing, and CI/CD.

---

## Project Status

| Phase | Description | Status |
|---|---|---|
| 1 | Project Setup & Environment | ✅ Completed |
| 2 | AWS Infrastructure & Security | ✅ Completed |
| 3 | API Ingestion | ⏳ Planned |
| 4 | Bronze Layer — S3 | ⏳ Planned |
| 5 | Silver Layer — PySpark | ⏳ Planned |
| 6 | Snowflake | ⏳ Planned |
| 7 | dbt & Gold Layer | ⏳ Planned |
| 8 | Testing & Data Quality | ⏳ Planned |
| 9 | Docker | ⏳ Planned |
| 10 | Airflow | ⏳ Planned |
| 11 | Airflow on AWS | ⏳ Planned |
| 12 | CI | ⏳ Planned |
| 13 | CD | ⏳ Planned |
| 14 | Platform Maturity | ⏳ Planned |

---

## Architecture

The target architecture follows a layered data platform approach:

```text
                    ┌──────────────────────┐
                    │   GoCardless API     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Python Ingestion   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       AWS S3         │
                    │       Bronze         │
                    │   Raw JSON / History │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       PySpark        │
                    │ Extract / Transform  │
                    │      Validation      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       AWS S3         │
                    │       Silver         │
                    │       Parquet        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Snowflake       │
                    │       Staging        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │         dbt          │
                    │    Transformations   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Snowflake       │
                    │        Gold          │
                    │ Business-ready data  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    BI / Analytics    │
                    └──────────────────────┘