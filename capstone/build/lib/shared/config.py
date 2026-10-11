
"""Shared configuration for the Saudi Aviation Data Platform."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Loads a local .env file when present.
# Docker environment variables take precedence.
load_dotenv()


@dataclass(frozen=True)
class Settings:
    gcp_project_id: str
    bronze_dataset: str = "bronze"
    silver_dataset: str = "silver"
    gold_dataset: str = "gold"
    gcp_location: str = "me-central2"

    @classmethod
    def from_env(cls) -> "Settings":
        project_id = os.getenv("GCP_PROJECT_ID", "").strip()

        if not project_id:
            raise ValueError(
                "GCP_PROJECT_ID is missing. "
                "Set it in your environment or .env file."
            )

        return cls(
            gcp_project_id=project_id,
            bronze_dataset=os.getenv("BRONZE_DATASET", "bronze"),
            silver_dataset=os.getenv("SILVER_DATASET", "silver"),
            gold_dataset=os.getenv("GOLD_DATASET", "gold"),
            gcp_location=os.getenv("GCP_LOCATION", "me-central2"),
        )


settings = Settings.from_env()
