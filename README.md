# Saudi Aviation Infrastructure & Data Platform

An end-to-end data engineering and analytics platform that integrates open aviation infrastructure data—including airports, runways, navigation aids (navaids), and communication frequencies—into a unified view of Saudi Arabia's aviation infrastructure.

The platform ingests raw data into Google BigQuery, transforms it into clean and reliable Silver and Gold models using dbt, and delivers an interactive Streamlit dashboard to explore infrastructure coverage, compare regions, and identify potential data gaps.

## Problem Statement

Aviation infrastructure information is distributed across multiple datasets, making it difficult to explore and compare airports without manually combining different data sources.

For example, understanding an airport's infrastructure may require looking separately at airport details, runways, navigation aids, and communication frequencies.

This project addresses that challenge by integrating these datasets into a structured data platform, allowing users to explore available infrastructure information in one place.

## Key Features

- **Airport Explorer:** Explore airport information and associated infrastructure records through an interactive dashboard.
- **Regional Analysis:** Compare aviation infrastructure data across Saudi Arabia's regions.
- **Data Coverage Analysis:** Identify where infrastructure information is available and where source data may require further investigation.
- **Automated Data Transformation:** Transform raw data into structured analytical models using dbt.
- **Data Quality Testing:** Apply dbt tests to improve the reliability and consistency of analytical data.
- **Interactive Visualizations:** Explore the resulting Gold datasets through Streamlit.

## Screenshots

### Overview Page

<img width="1919" height="912" alt="Saudi Aviation Dashboard Overview" src="https://github.com/user-attachments/assets/5bad34ff-8686-4874-90bd-ebca63b6788e" />

### Airport Explorer Page

<img width="1919" height="909" alt="Airport Explorer Dashboard" src="https://github.com/user-attachments/assets/9a419c1f-b2c8-4a92-ac92-1bad8a67e3f3" />

### Data Coverage Page

<img width="1919" height="912" alt="Data Coverage Dashboard" src="https://github.com/user-attachments/assets/8de67fd9-f432-481b-9db2-17b433aee6ed" />

## Architecture Diagram

<img width="1280" height="720" alt="Saudi Aviation Data Platform Architecture" src="https://github.com/user-attachments/assets/350cdc89-707b-4770-9faa-c1bb65201fbc" />

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion and processing |
| Google BigQuery | Cloud data storage and analytical querying |
| dbt | Data transformation, modeling, and testing |
| Streamlit | Interactive dashboard and data visualization |
| Docker | Containerized dashboard deployment |
| GitHub | Version control and project collaboration |

## Data Pipeline Overview

The platform follows a Bronze–Silver–Gold data architecture.

### Bronze Layer — Raw Data Ingestion

Python ingests aviation infrastructure data from OurAirports into Google BigQuery.

The source datasets include:

- Airports
- Runways
- Navigation aids (navaids)
- Communication frequencies
- Regions
- Countries

This layer preserves the source data for subsequent transformation and analysis.

### Silver Layer — Data Cleaning and Transformation

dbt transforms Bronze data into cleaned and standardized Silver models.

This stage focuses on improving data consistency, preparing relationships between datasets, and creating reusable data models.

Silver models are materialized as BigQuery views.

### Gold Layer — Analytics-Ready Data

The Gold layer contains analytical tables designed to support the Streamlit dashboard.

The main Gold tables are:

| Table | Description |
|---|---|
| `airport_infrastructure` | Integrated airport and infrastructure information |
| `region_summary` | Regional aviation infrastructure summaries |
| `coverage_summary` | Data coverage information for infrastructure analysis |

Gold models are materialized as BigQuery tables.

### Visualization Layer

Streamlit queries the Gold tables to provide an interactive interface for exploring Saudi aviation infrastructure information.

Users can examine airport records, compare regional information, and investigate potential gaps in source-data coverage.

## Data Quality & Challenges

During development, several data quality and integration challenges were addressed.

| Challenge | Solution |
|---|---|
| Inconsistent runway surface names | Standardized different representations into consistent categories |
| Missing-value interpretation | Preserved valid country codes such as `NA` that could otherwise be interpreted as null values |
| Inconsistent region names | Corrected identified Saudi region name errors while preserving the original source values |
| Cloud database connectivity | Configured secure BigQuery access for the deployed Streamlit dashboard |

dbt tests are also used to validate configured data quality rules and improve confidence in the analytical models.

## Data Source & Limitations

The project uses publicly available aviation data from [OurAirports](https://ourairports.com/), focusing on Saudi Arabia.

The platform is intended for data exploration and infrastructure coverage analysis rather than operational aviation decision-making.

**Important considerations:**

- Missing infrastructure information in OurAirports does not necessarily indicate that the infrastructure does not exist in reality.
- Data completeness and accuracy depend on the available source records.
- Results reflect the source-data snapshot used during ingestion and may not represent current operational conditions.

These limitations should be considered when interpreting dashboard results.

---

## Requirements

- Python 3.11 or later
- A Google Cloud project with the BigQuery API enabled
- Google Cloud CLI (`gcloud`) for local Application Default Credentials (ADC)
- Docker Engine and the Docker Compose plugin (optional, for running the dashboard in a container)

## Installation

From the repository root, create and activate a virtual environment, then install the project and its dependencies—including dbt and Streamlit—from [`capstone/pyproject.toml`](capstone/pyproject.toml).

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ./capstone
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

The project also includes a Dev Container configuration for setting up a development environment in VS Code. It installs the same dependencies from `capstone/pyproject.toml`.

## BigQuery Configuration and Authentication

Enable the BigQuery API for your Google Cloud project and authenticate locally with Application Default Credentials (ADC):

```bash
gcloud auth application-default login
```

Set the project and dataset configuration in your shell. Replace the project ID with your Google Cloud project ID:

```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_LOCATION="EU"
export BRONZE_DATASET="bronze"
export SILVER_DATASET="silver"
export GOLD_DATASET="gold"
```

The ingestion pipeline reads these settings from the environment or `capstone/.env`.

Create the local configuration file:

```bash
cp capstone/.env.example capstone/.env
```

Then update its values as needed.

The dbt profile reads `GCP_PROJECT_ID` and `GCP_LOCATION` from the shell environment, so export them before running dbt.

The dashboard reads its configuration from environment variables or Streamlit secrets.

### BigQuery Permissions

The identity used for ingestion and dbt needs permission to create BigQuery query jobs and create or update tables and views in the configured datasets.

The dashboard only needs permission to create query jobs and read the Gold dataset.

Grant only the permissions required for your deployment.

## Run the Data Pipeline

Run commands from the `capstone` directory.

First, load the OurAirports source files into the Bronze dataset:

```bash
cd capstone
python -m ingestion.ourairports_bronze
```

The ingestion process creates the Bronze dataset if needed and loads airports, runways, navaids, frequencies, regions, and countries.

It requires network access to the OurAirports data and BigQuery write permissions.

## dbt Models and Tests

Run dbt from the `capstone` directory after Bronze ingestion.

The dbt project and its BigQuery profile are both located in `dbt/`.

```bash
dbt debug --project-dir dbt --profiles-dir dbt
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

The Silver models are built as views, while the Gold models are built as tables.

Gold tables used by the dashboard are:

- `airport_infrastructure`
- `region_summary`
- `coverage_summary`

These tables are stored in the `gold` dataset.

Run `dbt test` to check the configured data quality rules. This command validates the models but does not rebuild them.

## Run the Streamlit Dashboard

Run from the `capstone/dashboard` directory after the Gold dbt models have been built:

```bash
streamlit run app.py
```

The dashboard opens at:

http://localhost:8501

It queries the Gold tables in BigQuery.

For local use, the dashboard can use the ADC credentials configured above.

Set the following variables in the environment or Streamlit secrets:

- `GCP_PROJECT_ID`
- `GCP_LOCATION` (defaults to `EU`)
- `GOLD_DATASET` (defaults to `gold`)

### Streamlit Community Cloud Deployment

For Streamlit Community Cloud, configure the project settings in the app's secrets and add a `gcp_service_account` section containing the service account credentials.

Give that account BigQuery job-creation permission and read access to the Gold dataset.

**Security:** Never commit service-account credentials or `.streamlit/secrets.toml` to GitHub.

### Dashboard Caching

Dashboard query results are cached for 15 minutes.

After rebuilding the Gold models, the dashboard will display updated results when the cache expires. Restarting the app also clears the cache.

## Run with Docker Compose

Docker Compose builds and runs the Streamlit dashboard container, exposing it on port 8501.

First, authenticate ADC on the host:

```bash
gcloud auth application-default login
```

Before starting the container, update `GCP_PROJECT_ID` under `services.dashboard.environment` in `docker-compose.yml` to the project containing your Gold dataset.

The Compose file mounts the host ADC credentials file read-only from:

```text
~/.config/gcloud/application_default_credentials.json
```

Make sure that file exists.

Then, from the repository root, run:

```bash
docker compose up --build -d
```

Open the dashboard at:

http://localhost:8501

View container logs:

```bash
docker compose logs -f dashboard
```

Stop the service:

```bash
docker compose down
```

The Compose service runs the dashboard only. Data ingestion and dbt transformations must be executed separately using the local instructions above.

The container uses the project ID and location configured in `docker-compose.yml`.

---

## Project Summary

The Saudi Aviation Infrastructure & Data Platform demonstrates an end-to-end data engineering workflow, from ingesting and transforming open aviation datasets to building analytical models and presenting results through an interactive dashboard.

The project emphasizes data integration, quality, reusability, and accessibility while making the limitations of open-source aviation data explicit.
