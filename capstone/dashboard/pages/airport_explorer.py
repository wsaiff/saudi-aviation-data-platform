import streamlit as st

from components.header import render_header
from data import load_airport_infrastructure


render_header(
    title="Airport explorer",
    subtitle="Search and filter airport records from the dbt gold layer.",
)

airports = load_airport_infrastructure()

filter_region, filter_type = st.columns(2)
with filter_region:
    region_names = ["All regions", *sorted(airports["region_name"].dropna().unique())]
    selected_region = st.selectbox("Region", region_names)
with filter_type:
    types = ["All types", *sorted(airports["airport_type"].dropna().unique())]
    selected_type = st.selectbox("Airport type", types)

search = st.text_input(
    "Search airports",
    placeholder="Search by airport name, municipality, or identifier",
)

filtered_airports = airports
if selected_region != "All regions":
    filtered_airports = filtered_airports.loc[
        filtered_airports["region_name"] == selected_region
    ]
if selected_type != "All types":
    filtered_airports = filtered_airports.loc[
        filtered_airports["airport_type"] == selected_type
    ]
if search.strip():
    searchable_columns = [
        column
        for column in (
            "airport_name",
            "municipality",
            "airport_ident",
            "icao_code",
            "iata_code",
        )
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
        "airport_name",
        "airport_type",
        "region_name",
        "region_code",
        "municipality",
        "latitude_deg",
        "longitude_deg",
        "elevation_ft",
        "airport_ident",
        "icao_code",
        "iata_code",
        "runway_count",
        "frequency_count",
        "navaid_count",
    )
    if column in filtered_airports.columns
]
display_data = filtered_airports[display_columns].rename(
    columns={
        "airport_name": "Airport",
        "airport_type": "Type",
        "region_name": "Region",
        "region_code": "Region code",
        "municipality": "Municipality",
        "latitude_deg": "Latitude",
        "longitude_deg": "Longitude",
        "elevation_ft": "Elevation (ft)",
        "airport_ident": "Airport identifier",
        "icao_code": "ICAO",
        "iata_code": "IATA",
        "runway_count": "Runways",
        "frequency_count": "Frequencies",
        "navaid_count": "Navigation aids",
    }
)
st.dataframe(
    display_data,
    column_config={
        "Latitude": st.column_config.NumberColumn(format="%.4f"),
        "Longitude": st.column_config.NumberColumn(format="%.4f"),
        "Elevation (ft)": st.column_config.NumberColumn(format="%d"),
        "Runways": st.column_config.NumberColumn(format="%d"),
        "Frequencies": st.column_config.NumberColumn(format="%d"),
        "Navigation aids": st.column_config.NumberColumn(format="%d"),
    },
    hide_index=True,
    width="stretch",
)