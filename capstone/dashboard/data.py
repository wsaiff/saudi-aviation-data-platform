import os
import re

import pandas as pd
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from streamlit.errors import StreamlitSecretNotFoundError


GOLD_TABLES = {
    "airport_infrastructure",
    "region_summary",
    "coverage_summary",
}
PROJECT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
DATASET_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")


def _load_secrets():
    try:
        return dict(st.secrets)
    except StreamlitSecretNotFoundError:
        return {}


def _get_setting(name, secrets, default=None):
    value = os.getenv(name) or secrets.get(name) or default
    return str(value).strip() if value is not None else ""


@st.cache_resource
def get_bigquery_client():
    secrets = _load_secrets()
    project_id = _get_setting("GCP_PROJECT_ID", secrets)
    location = _get_setting("GCP_LOCATION", secrets, "EU")
    service_account_info = secrets.get("gcp_service_account")

    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID must be configured in the environment or "
            "Streamlit secrets before loading dbt gold data."
        )
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("GCP_PROJECT_ID contains invalid characters.")

    credentials = None
    if service_account_info:
        credentials = service_account.Credentials.from_service_account_info(
            dict(service_account_info),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    return bigquery.Client(
        project=project_id,
        location=location,
        credentials=credentials,
    )


@st.cache_data(ttl=900)
def _load_gold_table(table_name):
    if table_name not in GOLD_TABLES:
        raise ValueError(f"Unsupported dbt gold model: {table_name}")

    secrets = _load_secrets()
    project_id = _get_setting("GCP_PROJECT_ID", secrets)
    dataset = _get_setting("GOLD_DATASET", secrets, "gold")
    if not project_id:
        raise ValueError(
            "GCP_PROJECT_ID must be configured in the environment or "
            "Streamlit secrets before loading dbt gold data."
        )
    if not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("GCP_PROJECT_ID contains invalid characters.")
    if not DATASET_PATTERN.fullmatch(dataset):
        raise ValueError("GOLD_DATASET contains invalid characters.")

    table_id = f"`{project_id}.{dataset}.{table_name}`"
    return get_bigquery_client().query(
        f"SELECT * FROM {table_id}"
    ).to_dataframe()


def load_airport_infrastructure() -> pd.DataFrame:
    return _load_gold_table("airport_infrastructure")


def load_region_summary() -> pd.DataFrame:
    return _load_gold_table("region_summary")


def load_coverage_summary() -> pd.DataFrame:
    return _load_gold_table("coverage_summary")
