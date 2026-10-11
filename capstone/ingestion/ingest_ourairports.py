"""
Data Ingestion Pipeline - Bronze Layer
Project: Saudi Aviation Infrastructure & Data Platform

Description:
    Downloads raw OurAirports dataset CSV files from source URLs
    and loads them directly into Google BigQuery under the 'bronze' dataset.
    Follows Medallion Architecture principles by storing unaltered raw data.
"""

import io
import requests
import pandas as pd
from google.cloud import bigquery

# ==========================================
# Configuration & Constants
# ==========================================
PROJECT_ID = "saudi-aviation-infrastructure"
DATASET_ID = "bronze"
DEFAULT_LOCATION = "EU"

# Source URLs for OurAirports reference datasets
DATASET_URLS = {
    "airports": "https://davidmegginson.github.io/ourairports-data/airports.csv",
    "runways": "https://davidmegginson.github.io/ourairports-data/runways.csv",
    "navaids": "https://davidmegginson.github.io/ourairports-data/navaids.csv",
    "frequencies": "https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv",
    "regions": "https://davidmegginson.github.io/ourairports-data/regions.csv",
    "countries": "https://davidmegginson.github.io/ourairports-data/countries.csv",
}


def get_bigquery_client() -> bigquery.Client:
    """Initializes and returns a BigQuery client using Application Default Credentials (ADC)."""
    return bigquery.Client(project=PROJECT_ID)


def ensure_dataset_exists(client: bigquery.Client, dataset_name: str, location: str = DEFAULT_LOCATION) -> None:
    """
    Checks if the target BigQuery dataset exists; if not, creates it.

    Args:
        client: Active BigQuery client instance.
        dataset_name: Name of the dataset to verify or create.
        location: Geographic location for data storage (e.g., 'EU' or 'US').
    """
    full_dataset_id = f"{client.project}.{dataset_name}"
    dataset = bigquery.Dataset(full_dataset_id)
    dataset.location = location
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f" Dataset '{dataset.dataset_id}' ready in location '{location}'.")


def load_table_from_url(client: bigquery.Client, table_name: str, url: str) -> None:
    """
    Downloads CSV data from a URL and loads it into BigQuery raw/bronze table.

    Data Ingestion Rules:
    1. keep_default_na=False: By default, pandas interprets the literal string 'NA'
       as NaN/NULL. In aviation data, 'NA' represents North America (continent code)
       and Namibia (ISO country code). Disabling this preserves valid records.
    2. na_values=['']: Only treats genuinely empty cells as NULL values.
    3. encoding='utf-8': Preserves non-Latin characters (e.g., Arabic airport names).
    4. low_memory=False: Processes files in a single pass to prevent mixed-type inference warnings.
    5. WRITE_TRUNCATE: Ensures idempotency by replacing the table on each execution.
    """
    print(f"\n Fetching '{table_name}' from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # Read raw bytes to ensure clean UTF-8 decoding and retain literal 'NA' codes
    df = pd.read_csv(
        io.BytesIO(response.content),
        low_memory=False,
        keep_default_na=False,
        na_values=[""],
        encoding="utf-8",
    )
    print(f"   Downloaded {len(df):,} rows and {len(df.columns)} columns.")

    table_id = f"{client.project}.{DATASET_ID}.{table_name}"

    # Configure job to overwrite table on each run (idempotent snapshot)
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    print(f"   Uploading to BigQuery table: {table_id} ...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Block until the BigQuery load job finishes

    # Confirm loaded row count against BigQuery metadata
    table = client.get_table(table_id)
    print(f" Loaded {table.num_rows:,} rows into {table_id}")


def main() -> None:
    """Main orchestration function for Bronze layer data ingestion."""
    client = get_bigquery_client()
    print(f"Connected to BigQuery project: {client.project}")
    print(f"Target dataset: {DATASET_ID}")

    ensure_dataset_exists(client, DATASET_ID)

    failed_tables = []
    for table_name, url in DATASET_URLS.items():
        try:
            load_table_from_url(client, table_name, url)
        except Exception as err:
            failed_tables.append(table_name)
            print(f"❌ Failed to load {table_name}: {err}")

    # Fail fast: prevent reporting a false-positive successful pipeline run
    if failed_tables:
        raise RuntimeError(f"Bronze ingestion failed for tables: {failed_tables}")

    print("\n Bronze layer ingestion completed successfully!")


if __name__ == "__main__":
    main()
