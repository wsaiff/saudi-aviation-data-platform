"""
Data Ingestion Pipeline - Bronze Layer
Project: Saudi Aviation Infrastructure & Data Platform

Reuses shared BigQuery client and configuration settings.
"""

import io
import sys
from pathlib import Path
import requests
import pandas as pd
from google.cloud import bigquery

# Ensure the root directory is in the Python path to import from shared
sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared.config import settings
from shared.bigquery_client import get_bigquery_client, get_table_id

# Source dataset URLs
DATASET_URLS = {
    "airports": "https://davidmegginson.github.io/ourairports-data/airports.csv",
    "runways": "https://davidmegginson.github.io/ourairports-data/runways.csv",
    "navaids": "https://davidmegginson.github.io/ourairports-data/navaids.csv",
    "frequencies": "https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv",
    "regions": "https://davidmegginson.github.io/ourairports-data/regions.csv",
    "countries": "https://davidmegginson.github.io/ourairports-data/countries.csv",
}


def ensure_dataset_exists(client: bigquery.Client, dataset_name: str) -> None:
    """Ensures target BigQuery dataset exists using the configured project location."""
    dataset_ref = f"{client.project}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = settings.gcp_location
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f" Dataset '{dataset.dataset_id}' ready in location '{settings.gcp_location}'.")


def load_table_from_url(client: bigquery.Client, table_name: str, url: str) -> None:
    """Downloads CSV and loads it into BigQuery raw/bronze table."""
    print(f"\n Fetching '{table_name}' from: {url}")
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    # Preserve literal 'NA' (North America / Namibia) and keep raw data intact
    df = pd.read_csv(
        io.BytesIO(response.content),
        low_memory=False,
        keep_default_na=False,
        na_values=[""],
        encoding="utf-8",
    )
    print(f"   Downloaded {len(df):,} rows and {len(df.columns)} columns.")

    # Get verified table ID via shared helper
    table_id = get_table_id(settings.bronze_dataset, table_name)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    print(f"   Uploading to BigQuery table: {table_id} ...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    table = client.get_table(table_id)
    print(f" Loaded {table.num_rows:,} rows into {table_id}")


def main() -> None:
    """Main execution function."""
    client = get_bigquery_client()
    print(f"Connected to BigQuery project: {client.project}")
    print(f"Target dataset: {settings.bronze_dataset}")

    ensure_dataset_exists(client, settings.bronze_dataset)

    failed_tables = []
    for table_name, url in DATASET_URLS.items():
        try:
            load_table_from_url(client, table_name, url)
        except Exception as err:
            failed_tables.append(table_name)
            print(f"❌ Failed to load {table_name}: {err}")

    if failed_tables:
        raise RuntimeError(f"Bronze ingestion failed for tables: {failed_tables}")

    print("\n Bronze layer ingestion completed successfully!")


if __name__ == "__main__":
    main()
