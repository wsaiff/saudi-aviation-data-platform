"""Reusable CSV-to-BigQuery ingestion functions."""

import io
import pandas as pd
import requests
from google.cloud import bigquery

from shared.config import settings
from shared.bigquery_client import get_table_id


def ensure_dataset_exists(
    client: bigquery.Client,
    dataset_name: str,
) -> None:
    """Create the BigQuery dataset if it does not exist."""
    dataset_id = f"{client.project}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = settings.gcp_location

    client.create_dataset(dataset, exists_ok=True)
    print(
        f"Dataset '{dataset_name}' ready "
        f"in location '{settings.gcp_location}'."
    )


def fetch_csv(
    url: str,
    timeout: int = 60,
) -> pd.DataFrame:
    """Download a CSV from a URL and return it as a DataFrame."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    # preserve literal 'NA' for continent and country codes
    df = pd.read_csv(
        io.BytesIO(response.content),
        low_memory=False,
        keep_default_na=False,
        na_values=[""],
        encoding="utf-8",
    )

    print(
        f"Downloaded {len(df):,} rows "
        f"and {len(df.columns)} columns."
    )
    return df


def load_dataframe_to_bigquery(
    client: bigquery.Client,
    df: pd.DataFrame,
    dataset_name: str,
    table_name: str,
    write_disposition: str = "WRITE_TRUNCATE",
) -> None:
    """Load a DataFrame into a BigQuery table."""
    table_id = get_table_id(dataset_name, table_name)

    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True,
    )

    print(f"Uploading to BigQuery table: {table_id} ...")
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )
    job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows:,} rows into {table_id}")


def ingest_csv_from_url(
    client: bigquery.Client,
    url: str,
    dataset_name: str,
    table_name: str,
) -> None:
    """Download a CSV and load it into BigQuery."""
    print(f"\nFetching '{table_name}' from: {url}")
    df = fetch_csv(url)
    load_dataframe_to_bigquery(
        client=client,
        df=df,
        dataset_name=dataset_name,
        table_name=table_name,
    )
