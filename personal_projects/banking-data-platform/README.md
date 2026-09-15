
# Banking Data Platform

Data Engineering portfolio project focused on building a banking data platform using API ingestion, AWS, S3, PySpark, Snowflake, dbt, Airflow, Docker, testing and CI/CD.

## Project Status

Phase 1 — Project setup and environment configuration.

## Project Structure

```text
banking-data-platform/
├── .github/
│   └── workflows/
│
├── dags/
│
├── dbt/
│   ├── macros/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── seeds/
│   ├── snapshots/
│   └── tests/
│
├── docs/
│   ├── architecture/
│   ├── data_dictionary/
│   └── decisions/
│
├── infrastructure/
│   └── aws/
│
├── src/
│   ├── ingestion/
│   │   ├── auth/
│   │   ├── accounts/
│   │   ├── balances/
│   │   └── transactions/
│   │
│   ├── spark/
│   │   ├── extract/
│   │   ├── transform/
│   │   ├── validation/
│   │   └── load/
│   │
│   ├── quality/
│   │   └── data_quality/
│   │
│   └── utils/
│       ├── config/
│       ├── exceptions/
│       └── logging/
│
├── tests/
│   ├── integration/
│   └── unit/
│       ├── ingestion/
│       ├── quality/
│       └── spark/
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
└── uv.lock
