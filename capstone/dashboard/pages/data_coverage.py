import pandas as pd
import streamlit as st

from components.header import render_header
from data import load_airports


render_header(
    title="Data coverage",
    subtitle="Review completeness across the airport attributes in the current source snapshot.",
)

airports = load_airports()

coverage_fields = {
    "Airport name": "name",
    "Airport type": "type",
    "Region code": "iso_region",
    "Municipality": "municipality",
    "Elevation": "elevation_ft",
    "IATA code": "iata_code",
    "GPS code": "gps_code",
}
coverage_rows = []
for label, column in coverage_fields.items():
    present = (
        airports[column].notna()
        & airports[column].astype("string").str.strip().ne("")
    )
    available = int(present.sum())
    coverage_rows.append(
        {
            "Attribute": label,
            "Records available": available,
            "Records missing": len(airports) - available,
            "Coverage (%)": (
                100 * available / len(airports) if len(airports) else 0
            ),
        }
    )

coordinates_present = airports["latitude_deg"].notna() & airports[
    "longitude_deg"
].notna()
coordinate_count = int(coordinates_present.sum())
coverage_rows.insert(
    4,
    {
        "Attribute": "Coordinates",
        "Records available": coordinate_count,
        "Records missing": len(airports) - coordinate_count,
        "Coverage (%)": (
            100 * coordinate_count / len(airports) if len(airports) else 0
        ),
    },
)
metric_columns = st.columns(3)
metric_columns[0].metric("Airport records", f"{len(airports):,}")
metric_columns[1].metric(
    "Records with coordinates",
    f"{coordinate_count:,}",
)
metric_columns[2].metric(
    "Records without coordinates",
    f"{len(airports) - coordinate_count:,}",
)

st.subheader("Attribute completeness")
coverage_table = pd.DataFrame(coverage_rows)
st.dataframe(
    coverage_table,
    column_config={
        "Coverage (%)": st.column_config.ProgressColumn(
            format="%.1f%%", min_value=0, max_value=100
        )
    },
    hide_index=True,
    width="stretch",
)

st.subheader("Coordinate coverage by region")
region_coverage = (
    airports.assign(
        has_coordinates=airports["latitude_deg"].notna()
        & airports["longitude_deg"].notna()
    )
    .groupby("iso_region", dropna=False)
    .agg(
        **{
            "Airport records": ("iso_region", "size"),
            "Records with coordinates": ("has_coordinates", "sum"),
        }
    )
    .reset_index()
    .rename(columns={"iso_region": "Region"})
)
region_coverage["Region"] = region_coverage["Region"].fillna("Unassigned")
region_coverage["Coordinate coverage (%)"] = (
    100
    * region_coverage["Records with coordinates"]
    / region_coverage["Airport records"]
)
st.dataframe(
    region_coverage.sort_values("Airport records", ascending=False),
    column_config={
        "Coordinate coverage (%)": st.column_config.ProgressColumn(
            format="%.1f%%", min_value=0, max_value=100
        )
    },
    hide_index=True,
    width="stretch",
)

st.info(
    "This page measures completeness in the imported airport records only. "
    "Missing data does not always mean missing infrastructure."
)