import streamlit as st

from components.header import render_header
from data import load_airports


render_header(
    title="Airport explorer",
    subtitle="Search and filter airport records in the Saudi Arabia OurAirports snapshot.",
)

airports = load_airports()

filter_region, filter_type = st.columns(2)
with filter_region:
    regions = ["All regions", *sorted(airports["iso_region"].dropna().unique())]
    selected_region = st.selectbox("Region", regions)
with filter_type:
    types = ["All types", *sorted(airports["type"].dropna().unique())]
    selected_type = st.selectbox("Airport type", types)

search = st.text_input(
    "Search airports",
    placeholder="Search by airport name, municipality, or code",
)

filtered_airports = airports
if selected_region != "All regions":
    filtered_airports = filtered_airports.loc[
        filtered_airports["iso_region"] == selected_region
    ]
if selected_type != "All types":
    filtered_airports = filtered_airports.loc[
        filtered_airports["type"] == selected_type
    ]
if search.strip():
    searchable_columns = [
        column
        for column in ("name", "municipality", "ident", "iata_code", "gps_code")
        if column in filtered_airports.columns
    ]
    matches = (
        filtered_airports[searchable_columns]
        .fillna("")
        .astype("string")
        .apply(
            lambda column: column.str.contains(
                search.strip(), case=False, regex=False
            )
        )
        .any(axis=1)
    )
    filtered_airports = filtered_airports.loc[matches]

st.caption(f"Showing {len(filtered_airports):,} of {len(airports):,} airport records.")

display_columns = [
    column
    for column in (
        "name",
        "type",
        "iso_region",
        "municipality",
        "latitude_deg",
        "longitude_deg",
        "elevation_ft",
        "iata_code",
        "gps_code",
    )
    if column in filtered_airports.columns
]
display_data = filtered_airports[display_columns].rename(
    columns={
        "name": "Airport",
        "type": "Type",
        "iso_region": "Region",
        "municipality": "Municipality",
        "latitude_deg": "Latitude",
        "longitude_deg": "Longitude",
        "elevation_ft": "Elevation (ft)",
        "iata_code": "IATA",
        "gps_code": "GPS code",
    }
)
st.dataframe(
    display_data,
    column_config={
        "Latitude": st.column_config.NumberColumn(format="%.4f"),
        "Longitude": st.column_config.NumberColumn(format="%.4f"),
        "Elevation (ft)": st.column_config.NumberColumn(format="%d"),
    },
    hide_index=True,
    width="stretch",
)