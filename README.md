# Saudi Aviation Infrastructure & Data Platform

An automated data engineering and analytics platform that brings together open aviation infrastructure data—including airports, runways, navaids, and communication frequencies—for analysis and visualization across Saudi Arabia.

The project loads raw data into BigQuery, transforms it with dbt into Silver and Gold models, and presents the Gold data in a Streamlit dashboard.

## Screenshots
### Overview page
<img width="1919" height="912" alt="Overview" src="https://github.com/user-attachments/assets/5bad34ff-8686-4874-90bd-ebca63b6788e" />

### Airport Explorer Page
<img width="1919" height="909" alt="Airport_explorer_1" src="https://github.com/user-attachments/assets/9a419c1f-b2c8-4a92-ac92-1bad8a67e3f3" />

### Data Coverage Page
<img width="1919" height="912" alt="data_coverage" src="https://github.com/user-attachments/assets/8de67fd9-f432-481b-9db2-17b433aee6ed" />

## Architecture Diagram

<img width="1280" height="720" alt="diagram" src="https://github.com/user-attachments/assets/350cdc89-707b-4770-9faa-c1bb65201fbc" />


## Requirements

- Python 3.10 or later
- A Google Cloud project with the BigQuery API enabled
- Google Cloud CLI (`gcloud`) for local Application Default Credentials (ADC)
- Docker Engine and the Docker Compose plugin (optional, for running the dashboard in a container)

## Installation

Python 3.11 or later is required. From the repository root, create and activate a virtual environment, then install the project and all of its dependencies (including dbt and Streamlit) from the single dependency manifest, [`capstone/pyproject.toml`](capstone/pyproject.toml):

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

The project also includes a Dev Container configuration for setting up a development environment in VS Code; it installs the same dependencies from `capstone/pyproject.toml`.

## BigQuery configuration and authentication

Enable the BigQuery API for your Google Cloud project and authenticate locally with ADC:

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

The ingestion pipeline reads these settings from the environment or `capstone/.env`; create the local file with `cp capstone/.env.example capstone/.env` and update its values. The dbt profile reads `GCP_PROJECT_ID` and `GCP_LOCATION` from the shell environment, so export them before running dbt. The dashboard reads its configuration from environment variables or Streamlit secrets.

The identity used for ingestion and dbt needs permission to create BigQuery query jobs and create or update tables and views in the configured datasets. The dashboard only needs permission to create query jobs and read the Gold dataset. Grant only the permissions needed for your deployment.

## Run the data pipeline

Run commands from the `capstone` directory. First load the OurAirports source files into the Bronze dataset:

```bash
cd capstone
python -m ingestion.ourairports_bronze
```

The ingestion process creates the Bronze dataset if needed and loads airports, runways, navaids, frequencies, regions, and countries. It requires network access to the OurAirports data and BigQuery write permissions.

## dbt models and tests

Run dbt from the `capstone` directory after Bronze ingestion. The dbt project and its BigQuery profile are both in `dbt/`:

```bash
dbt debug --project-dir dbt --profiles-dir dbt
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
```

The Silver models are built as views and the Gold models as tables. Gold tables used by the dashboard are `airport_infrastructure`, `region_summary`, and `coverage_summary` in the `gold` dataset. Run `dbt test` to check the configured data-quality rules; it does not rebuild models.

## Run the Streamlit dashboard

Run from the `capstone/dashboard` directory after the Gold dbt models have been built:

```bash
streamlit run app.py
```

The app opens at <http://localhost:8501>. It queries the Gold tables in BigQuery. For local use, the dashboard can use the ADC credentials configured above. Set `GCP_PROJECT_ID`, `GCP_LOCATION` (defaults to `EU`), and `GOLD_DATASET` (defaults to `gold`) in the environment or Streamlit secrets.

For Streamlit Community Cloud, configure those settings in the app's secrets and add a `gcp_service_account` section containing the service account credentials. Give that account BigQuery job-creation permission and read access to the Gold dataset. Never commit service-account credentials or `.streamlit/secrets.toml`.

Dashboard query results are cached for 15 minutes. After rebuilding the Gold models, the dashboard will display updated results when the cache expires; restarting the app also clears the cache.

## Run with Docker Compose

Docker Compose builds and runs the Streamlit dashboard container, exposing it on port 8501. Authenticate ADC on the host first:

```bash
gcloud auth application-default login
```

Before starting the container, update `GCP_PROJECT_ID` under `services.dashboard.environment` in `docker-compose.yml` to the project containing your Gold dataset. The Compose file mounts the host ADC credentials file read-only from `~/.config/gcloud/application_default_credentials.json`; make sure that file exists. Then, from the repository root, run:

```bash
docker compose up --build -d
```

Open <http://localhost:8501>. View container output or stop the service with:

```bash
docker compose logs -f dashboard
docker compose down
```

The Compose service runs the dashboard only; ingest data and run dbt separately using the local instructions above. The container uses the project ID and location configured in `docker-compose.yml`.
