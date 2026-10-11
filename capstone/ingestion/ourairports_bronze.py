"""OurAirports ingestion pipeline - Bronze layer."""

from google.cloud import bigquery

from shared.config import settings
from shared.bigquery_client import get_bigquery_client
from ingestion.bigquery_loader import (
    ensure_dataset_exists,
    ingest_csv_from_url,
)

DATASET_URLS = {
    "airports": "https://davidmegginson.github.io/ourairports-data/airports.csv",
    "runways": "https://davidmegginson.github.io/ourairports-data/runways.csv",
    "navaids": "https://davidmegginson.github.io/ourairports-data/navaids.csv",
    "frequencies": "https://davidmegginson.github.io/ourairports-data/airport-frequencies.csv",
    "regions": "https://davidmegginson.github.io/ourairports-data/regions.csv",
    "countries": "https://davidmegginson.github.io/ourairports-data/countries.csv",
}


def main() -> None:
    """Run the OurAirports Bronze ingestion."""
    client = get_bigquery_client()
    dataset_name = settings.bronze_dataset

    print(f"Connected to BigQuery project: {client.project}")
    print(f"Target dataset: {dataset_name}")

    ensure_dataset_exists(client, dataset_name)

    failed_tables = []
    for table_name, url in DATASET_URLS.items():
        try:
            ingest_csv_from_url(
                client=client,
                url=url,
                dataset_name=dataset_name,
                table_name=table_name,
            )
        except Exception as err:
            failed_tables.append(table_name)
            print(f"Failed to load {table_name}: {err}")

    if failed_tables:
        raise RuntimeError(
            f"Bronze ingestion failed for tables: {failed_tables}"
        )

    print("\nBronze layer ingestion completed successfully!")


if __name__ == "__main__":
    main()
