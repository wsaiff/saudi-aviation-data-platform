
"""Shared BigQuery client."""

from google.cloud import bigquery

from shared.config import settings


def get_bigquery_client() -> bigquery.Client:
    """Create a BigQuery client using Application Default Credentials."""
    return bigquery.Client(
        project=settings.gcp_project_id,
        location=settings.gcp_location,
    )


def get_table_id(dataset: str, table: str) -> str:
    """Return a fully qualified BigQuery table ID."""
    allowed_datasets = {
        settings.bronze_dataset,
        settings.silver_dataset,
        settings.gold_dataset,
    }

    if dataset not in allowed_datasets:
        raise ValueError(f"Unknown dataset: {dataset}")

    if not table or not table.replace("_", "").isalnum():
        raise ValueError(f"Invalid table name: {table}")

    return f"{settings.gcp_project_id}.{dataset}.{table}"
