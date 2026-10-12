"""Validate the OurAirports Bronze layer without modifying BigQuery tables."""

"""
What this script validates
- Table existence: BigQuery must be able to retrieve each table.
- Row counts: Logs the current source and Bronze row counts. A mismatch is a warning, because the source may have changed since ingestion.
- Column names: Reports missing or unexpected columns.
- BigQuery data types: Logs the stored BigQuery types for review.

limitation: the script reports the BigQuery data types but does not yet assert that each type is correct. Also, it checks that tables are non-empty, not that the ingestion loaded every source row exactly. Those stronger checks should follow once this baseline passes.
"""

import logging
from io import StringIO

import pandas as pd
import requests

from shared.config import settings
from shared.bigquery_client import get_bigquery_client, get_table_id
from ingestion.ourairports_bronze import DATASET_URLS

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def download_source_csv(url: str) -> pd.DataFrame:
    """Download a source CSV for validation only."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text), keep_default_na=False, na_values=[""])


def validate_bronze() -> None:
    """Check Bronze table existence, row counts, columns, and BigQuery types."""
    client = get_bigquery_client()
    failures = []

    for table_name, url in DATASET_URLS.items():
        logger.info("Validating bronze.%s", table_name)

        try:
            # Read the current source snapshot; do not load it into BigQuery.
            source_df = download_source_csv(url)

            table_id = get_table_id(settings.bronze_dataset, table_name)
            table = client.get_table(table_id)

            source_columns = list(source_df.columns)
            bronze_columns = [field.name for field in table.schema]

            missing_columns = sorted(set(source_columns) - set(bronze_columns))
            extra_columns = sorted(set(bronze_columns) - set(source_columns))

            columns_match = not missing_columns and not extra_columns
            table_has_rows = table.num_rows > 0

            logger.info(
                "%s | BigQuery rows=%s | current source rows=%s",
                table_name,
                table.num_rows,
                len(source_df),
            )
            logger.info(
                "%s | BigQuery schema: %s",
                table_name,
                {field.name: field.field_type for field in table.schema},
            )
            logger.info(
                "%s | table_has_rows=%s | columns_match=%s",
                table_name,
                table_has_rows,
                columns_match,
            )

            if missing_columns:
                logger.error("Missing Bronze columns in %s: %s",
                             table_name, missing_columns)
            if extra_columns:
                logger.error("Unexpected Bronze columns in %s: %s",
                             table_name, extra_columns)

            if table.num_rows != len(source_df):
                logger.warning(
                    "%s row counts differ. The source may have changed since ingestion.",
                    table_name,
                )

            if not table_has_rows or not columns_match:
                failures.append(table_name)

        except Exception:
            logger.exception("Validation failed for %s", table_name)
            failures.append(table_name)

    if failures:
        raise RuntimeError(f"Bronze validation failed for tables: {failures}")

    logger.info("All Bronze table existence, row, and column checks passed.")


if __name__ == "__main__":
    validate_bronze()
