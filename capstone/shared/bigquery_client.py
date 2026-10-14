"""Shared BigQuery client helpers for ingestion and the dashboard."""

import re

from google.auth.credentials import Credentials
from google.cloud import bigquery

PROJECT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
NAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def create_bigquery_client(
    project_id: str,
    location: str,
    credentials: Credentials | None = None,
) -> bigquery.Client:
    """Create a BigQuery client.

    Uses Application Default Credentials when no credentials are given.
    """
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID is missing. Set it in the environment, "
            ".env file, or Streamlit secrets."
        )
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("GCP_PROJECT_ID contains invalid characters.")

    return bigquery.Client(
        project=project_id,
        location=location,
        credentials=credentials,
    )


def qualified_table_id(project_id: str, dataset: str, table: str) -> str:
    """Return a validated project.dataset.table identifier."""
    if not NAME_PATTERN.fullmatch(dataset or ""):
        raise ValueError(f"Invalid dataset name: {dataset!r}")
    if not NAME_PATTERN.fullmatch(table or ""):
        raise ValueError(f"Invalid table name: {table!r}")
    return f"{project_id}.{dataset}.{table}"


# Ingestion helpers.
# shared.config validates the environment when imported, so it is imported
# inside these functions. The dashboard can then use the helpers above
# without needing GCP_PROJECT_ID in the environment (it may come from
# Streamlit secrets instead).

def get_bigquery_client() -> bigquery.Client:
    """Create the ingestion client from shared settings."""
    from shared.config import settings

    return create_bigquery_client(
        project_id=settings.gcp_project_id,
        location=settings.gcp_location,
    )


def get_table_id(dataset: str, table: str) -> str:
    """Return a table ID restricted to the platform's datasets."""
    from shared.config import settings

    allowed_datasets = {
        settings.bronze_dataset,
        settings.silver_dataset,
        settings.gold_dataset,
    }
    if dataset not in allowed_datasets:
        raise ValueError(f"Unknown dataset: {dataset}")

    return qualified_table_id(settings.gcp_project_id, dataset, table)
