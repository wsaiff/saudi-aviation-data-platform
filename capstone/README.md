# 🇸🇦 Saudi Aviation Infrastructure & Data Platform

## 🎯 Overview
An automated data engineering and analytics platform designed to provide a single, trusted view of aviation infrastructure across the Kingdom of Saudi Arabia. The platform consolidates scattered airport data sources—including locations, runways, navaids, and communication frequencies—into unified, high-quality analytical layers to support informed planning and decision-making.

---

## 🚀 Core Objectives
* 🔗 **Unified Infrastructure View**: Combine separate dataset files (airports, runways, navaids, and frequencies) into one cohesive source of truth for Saudi aviation.
* 📊 **Data Transparency & Coverage**: Identify available infrastructure, compare regional coverage, and highlight data gaps to assist stakeholders and analysts.
* ⚙️ **Automated ELT Pipeline**: Seamlessly extract, load, and transform open-source data to feed interactive dashboards and geospatial maps.

## Dashboard
The Streamlit dashboard entry point is `capstone/dashboard/app.py`. Run it from the repository root:

```bash
streamlit run capstone/dashboard/app.py
```

The Overview, Airport explorer, Data coverage, and About & sources pages are in `capstone/dashboard/pages/`. Dashboard data is read from the dbt gold models in BigQuery (`airport_infrastructure`, `region_summary`, and `coverage_summary`); it no longer reads the live OurAirports CSV directly.

### Dashboard configuration
Configure `GCP_PROJECT_ID`, `GCP_LOCATION` (defaults to `EU`), and `GOLD_DATASET` (defaults to `gold`) as environment variables or Streamlit secrets. Local development can use Google Application Default Credentials. For Streamlit Community Cloud, add a `gcp_service_account` section to the app's secrets and provide a service account authorized to create BigQuery query jobs and read the gold dataset. Do not commit credentials or a `secrets.toml` file.

Dashboard query results are cached for 15 minutes. Re-run the dbt gold models to publish updated data; the dashboard will pick up those updates when its cache expires.
