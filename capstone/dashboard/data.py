import os

import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from streamlit.errors import StreamlitSecretNotFoundError

from shared.bigquery_client import create_bigquery_client, qualified_table_id


GOLD_TABLES = {
    "airport_infrastructure",
    "region_summary",
    "coverage_summary",
}


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

    # Service account from Streamlit secrets (Community Cloud);
    # otherwise None, which falls back to ADC (local and Docker).
    credentials = None
    service_account_info = secrets.get("gcp_service_account")
    if service_account_info:
        credentials = service_account.Credentials.from_service_account_info(
            dict(service_account_info),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    return create_bigquery_client(
        project_id=_get_setting("GCP_PROJECT_ID", secrets),
        location=_get_setting("GCP_LOCATION", secrets, "EU"),
        credentials=credentials,
    )


@st.cache_data(ttl=900)
def _load_gold_table(table_name):
    if table_name not in GOLD_TABLES:
        raise ValueError(f"Unsupported dbt gold model: {table_name}")

    client = get_bigquery_client()
    dataset = _get_setting("GOLD_DATASET", _load_secrets(), "gold")
    table_id = qualified_table_id(client.project, dataset, table_name)

    return client.query(f"SELECT * FROM {table_id}").to_dataframe()


def load_airport_infrastructure() -> pd.DataFrame:
    return _load_gold_table("airport_infrastructure")


def load_region_summary() -> pd.DataFrame:
    return _load_gold_table("region_summary")


def load_coverage_summary() -> pd.DataFrame:
    return _load_gold_table("coverage_summary")
