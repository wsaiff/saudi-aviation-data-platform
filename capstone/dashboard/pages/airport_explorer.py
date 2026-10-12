import math
from urllib.parse import urlencode

import pandas as pd
import pydeck as pdk
import streamlit as st

from components.header import render_header
from components.kpi import render_kpi
from data import load_airport_infrastructure


def clear_airport_selection():
    st.session_state.pop("airport_catalog", None)


def satellite_imagery_layer(latitude: float, longitude: float) -> pdk.Layer:
    latitude_delta = 0.035
    longitude_delta = latitude_delta * 1.6 / max(
        math.cos(math.radians(latitude)), 0.2
    )
    west = longitude - longitude_delta
    east = longitude + longitude_delta
    south = latitude - latitude_delta
    north = latitude + latitude_delta
    image_url = (
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/export?"
        + urlencode(
            {
                "bbox": f"{west},{south},{east},{north}",
                "bboxSR": 4326,
                "imageSR": 4326,
                "size": "640,400",
                "format": "jpg",
                "f": "image",
            }
        )
    )
    return pdk.Layer(
        "BitmapLayer",
        image=image_url,
        bounds=[west, south, east, north],
        pickable=False,
    )


render_header(
    title="Airport explorer",
    subtitle="Search, filter, and audit airport records from the dbt gold layer.",
)

airports = load_airport_infrastructure()
airports["data_completeness_score"] = (
    airports["data_completeness_score"].fillna(0).astype(int)
)
airports["has_runway_data"] = airports["has_runway_data"].fillna(False).astype(bool)
airports["has_frequency_data"] = (
    airports["has_frequency_data"].fillna(False).astype(bool)
)
airports["has_navaid_data"] = airports["has_navaid_data"].fillna(False).astype(bool)

kpi_slots = st.columns(3)
kpi_slots = [column.empty() for column in kpi_slots]

filter_columns = st.columns([2.2, 1.2, 1.35, 1.2, 1.0, 1.0])
with filter_columns[0]:
    search = st.text_input(
        "Search IDENT/Name",
        placeholder="Search airport identifier or name",
        key="airport_search",
        on_change=clear_airport_selection,
    )
with filter_columns[1]:
    regions = ["All regions", *sorted(airports["region_name"].dropna().unique())]
    selected_region = st.selectbox(
        "Region",
        regions,
        key="airport_region",
        on_change=clear_airport_selection,
    )
with filter_columns[2]:
    airport_types = [
        "All types",
        *sorted(airports["airport_type"].dropna().unique()),
    ]
    selected_type = st.selectbox(
        "Airport type",
        airport_types,
        key="airport_type",
        on_change=clear_airport_selection,
    )
with filter_columns[3]:
    completeness_options = ["All scores", "3/3", "<3/3"]
    selected_completeness = st.selectbox(
        "Completeness",
        completeness_options,
        key="airport_completeness",
        on_change=clear_airport_selection,
    )
with filter_columns[4]:
    core_only = st.toggle(
        "Core only",
        key="airport_core_only",
        on_change=clear_airport_selection,
    )
with filter_columns[5]:
    scheduled_only = st.toggle(
        "Scheduled",
        key="airport_scheduled_only",
        on_change=clear_airport_selection,
    )

filtered_df = airports.copy()
if search.strip():
    search_term = search.strip()
    search_matches = (
        filtered_df[["airport_ident", "airport_name"]]
        .fillna("")
        .astype("string")
        .apply(
            lambda column: column.str.contains(
                search_term, case=False, regex=False
            )
        )
        .any(axis=1)
    )
    filtered_df = filtered_df.loc[search_matches]
if selected_region != "All regions":
    filtered_df = filtered_df.loc[filtered_df["region_name"] == selected_region]
if selected_type != "All types":
    filtered_df = filtered_df.loc[filtered_df["airport_type"] == selected_type]
if selected_completeness == "3/3":
    filtered_df = filtered_df.loc[
        filtered_df["data_completeness_score"] == 3
    ]
elif selected_completeness == "<3/3":
    filtered_df = filtered_df.loc[
        filtered_df["data_completeness_score"] < 3
    ]
if core_only:
    filtered_df = filtered_df.loc[filtered_df["is_core"].fillna(False)]
if scheduled_only:
    filtered_df = filtered_df.loc[
        filtered_df["has_scheduled_service"].fillna(False)
    ]
filtered_df = filtered_df.reset_index(drop=True)

records_screened = len(filtered_df)
fully_complete = int((filtered_df["data_completeness_score"] == 3).sum())
action_required = int((filtered_df["data_completeness_score"] < 3).sum())
with kpi_slots[0].container():
    render_kpi(
        "Records Screened",
        f"{records_screened:,}",
        "filtered airports",
        centered=True,
    )
with kpi_slots[1].container():
    render_kpi(
        "Fully Complete (3/3)",
        f"{fully_complete:,}",
        "all data sources",
        centered=True,
    )
with kpi_slots[2].container():
    render_kpi(
        "Action Required (<3/3)",
        f"{action_required:,}",
        "missing source data",
        centered=True,
    )

col_table, col_profile = st.columns([2.5, 1.5])

with col_table:
    st.subheader("Airport Catalog & Completeness Audit")

    catalog = pd.DataFrame(
        {
            "Ident": filtered_df["airport_ident"].fillna("—"),
            "Airport Name": filtered_df["airport_name"].fillna("—"),
            "Region": filtered_df["region_name"].fillna("Unassigned"),
            "Type": filtered_df["airport_type"].fillna("Unknown"),
            "Runway Data": (
                "🟢 YES ("
                + filtered_df["runway_count"].fillna(0).astype(int).astype(str)
                + ")"
            ).where(filtered_df["has_runway_data"], "🔴 NO"),
            "Freq Data": (
                "🟢 YES ("
                + filtered_df["frequency_count"].fillna(0).astype(int).astype(str)
                + ")"
            ).where(filtered_df["has_frequency_data"], "🔴 NO"),
            "Navaid Data": (
                "🟢 YES ("
                + filtered_df["navaid_count"].fillna(0).astype(int).astype(str)
                + ")"
            ).where(filtered_df["has_navaid_data"], "🔴 NO"),
            "Score": filtered_df["data_completeness_score"],
        }
    )
    selection = st.dataframe(
        catalog,
        column_config={
            "Ident": st.column_config.TextColumn("Ident", width="small"),
            "Airport Name": st.column_config.TextColumn(
                "Airport Name", width="medium"
            ),
            "Region": st.column_config.TextColumn("Region", width="small"),
            "Type": st.column_config.TextColumn("Type", width="small"),
            "Runway Data": st.column_config.TextColumn(
                "Runway Data",
                help="Green indicates linked runway data; count is shown in parentheses.",
            ),
            "Freq Data": st.column_config.TextColumn(
                "Freq Data",
                help="Green indicates linked frequency data; count is shown in parentheses.",
            ),
            "Navaid Data": st.column_config.TextColumn(
                "Navaid Data",
                help="Green indicates linked navaid data; count is shown in parentheses.",
            ),
            "Score": st.column_config.NumberColumn(
                "Score", format="%d/3", width="small"
            ),
        },
        hide_index=True,
        width="stretch",
        height=520,
        key="airport_catalog",
        on_select="rerun",
        selection_mode="single-row",
        placeholder="No airports match the selected filters.",
    )

selected_rows = selection.selection.rows
with col_profile, st.container(border=True, key="airport-audit-profile"):
    st.subheader("Audit Profile")
    if selected_rows:
        airport = filtered_df.iloc[selected_rows[0]]
        airport_name = (
            str(airport["airport_name"])
            if pd.notna(airport["airport_name"])
            else "Unnamed airport"
        )
        airport_ident = (
            str(airport["airport_ident"])
            if pd.notna(airport["airport_ident"])
            else "No identifier"
        )
        st.markdown(f"### {airport_name}")
        st.caption(airport_ident)

        latitude = airport["latitude_deg"]
        longitude = airport["longitude_deg"]
        if pd.notna(latitude) and pd.notna(longitude):
            airport_point = pd.DataFrame(
                {"latitude": [latitude], "longitude": [longitude]}
            )
            satellite_map = pdk.Deck(
                layers=[
                    satellite_imagery_layer(float(latitude), float(longitude)),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=airport_point,
                        get_position="[longitude, latitude]",
                        get_fill_color=[232, 93, 158, 230],
                        get_line_color=[245, 247, 250, 255],
                        get_line_width=2,
                        line_width_min_pixels=2,
                        get_radius=350,
                        radius_min_pixels=8,
                        pickable=False,
                    )
                ],
                initial_view_state=pdk.ViewState(
                    latitude=float(latitude),
                    longitude=float(longitude),
                    zoom=11,
                    pitch=0,
                ),
                height=220,
                tooltip=False,
            )
            st.pydeck_chart(
                satellite_map,
                height=220,
                width="stretch",
                alt=f"Map location for {airport_name}",
            )
            st.caption("Satellite imagery © Esri, Maxar, Earthstar Geographics.")
        else:
            st.info("Coordinates are not available for this airport.")

        elevation = airport["elevation_ft"]
        elevation_text = f"{int(elevation):,} ft" if pd.notna(elevation) else "Not reported"
        st.write(f"**Elevation:** {elevation_text}")

        score = int(airport["data_completeness_score"])
        status = "FULLY DATA-COMPLETE" if score == 3 else "ACTION REQUIRED"
        render_kpi(
            "Data completeness",
            f"{score}/3",
            status,
            large_value=True,
        )

        runway_details = ""
        if airport["has_runway_data"]:
            runway_count = int(airport["runway_count"])
            longest_runway = airport["longest_runway_ft"]
            longest_text = (
                f", longest {int(longest_runway):,} ft"
                if pd.notna(longest_runway)
                else ""
            )
            runway_details = f" ({runway_count} runway(s){longest_text})"

        checklist = (
            ("Runway data", bool(airport["has_runway_data"]), runway_details),
            (
                "Radio frequencies data",
                bool(airport["has_frequency_data"]),
                (
                    f" ({int(airport['frequency_count'])} record(s))"
                    if airport["has_frequency_data"]
                    else ""
                ),
            ),
            (
                "Navigation aids (Navaids) data",
                bool(airport["has_navaid_data"]),
                (
                    f" ({int(airport['navaid_count'])} record(s))"
                    if airport["has_navaid_data"]
                    else ""
                ),
            ),
        )
        for label, present, details in checklist:
            icon = "✅" if present else "❌"
            st.markdown(f"- {icon} {label}{details}")
    else:
        st.info("Select an airport row to view its audit profile.")
