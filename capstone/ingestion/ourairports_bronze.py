"""OurAirports ingestion pipeline - Bronze layer."""

import logging
from google.cloud import bigquery

from shared.config import settings, OURAIRPORTS_DATASET_URLS
from shared.bigquery_client import get_bigquery_client
from ingestion.bigquery_loader import (
    ensure_dataset_exists,
    ingest_csv_from_url,
)

# Standard logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the OurAirports Bronze ingestion."""
    client = get_bigquery_client()
    dataset_name = settings.bronze_dataset

    logger.info("Connected to BigQuery project: %s", client.project)
    logger.info("Target dataset: %s", dataset_name)

    ensure_dataset_exists(client, dataset_name)

    failed_tables = []
    for table_name, url in OURAIRPORTS_DATASET_URLS.items():
        try:
            logger.info("Starting ingestion for table: %s", table_name)
            ingest_csv_from_url(
                client=client,
                url=url,
                dataset_name=dataset_name,
                table_name=table_name,
            )
            logger.info("Successfully ingested table: %s", table_name)
        except Exception as err:
            failed_tables.append(table_name)
            logger.error("Failed to load %s: %s", table_name, err, exc_info=True)

    if failed_tables:
        raise RuntimeError(
            f"Bronze ingestion failed for tables: {failed_tables}"
        )

    logger.info("Bronze layer ingestion completed successfully!")


if __name__ == "__main__":
    main()
