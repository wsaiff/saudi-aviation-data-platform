import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.cards import render_card_header, render_insight
from components.header import render_header
from components.kpi import render_kpi
from components.styles import COLORS
from data import load_airport_infrastructure, load_region_summary


@st.cache_data
def load_region_boundaries():
    boundary_file = Path(__file__).resolve().parents[1] / "saudi_regions.geojson"
    return json.loads(boundary_file.read_text(encoding="utf-8"))


airport_data = load_airport_infrastructure()
region_summary = load_region_summary()
region_boundaries = load_region_boundaries()

render_header(
    title="Saudi Arabia Aviation Overview",
    subtitle=(
        "Explore airport infrastructure and source-data coverage "
        "from the dbt gold layer."
    ),
)

region_names = (
    region_summary[["region_code", "region_name"]]
    .dropna(subset=["region_code"])
    .drop_duplicates()
    .sort_values("region_name")
)
region_options = ["All Regions", *region_names["region_name"].dropna().tolist()]
airport_types = sorted(airport_data["airport_type"].dropna().unique().tolist())


def reset_overview_filters():
    for key in (
        "overview_region",
        "overview_airport_type",
        "overview_data_availability",
    ):
        st.session_state.pop(key, None)


filter1, filter2, filter3, filter4 = st.columns([1.1, 1.1, 1.4, 0.95])
with filter1:
    selected_region = st.selectbox("Region", region_options, key="overview_region")
with filter2:
    selected_type = st.selectbox(
        "Airport Type",
        ["All Types", *airport_types],
        key="overview_airport_type",
    )
with filter3:
    selected_availability = st.selectbox(
        "Data Availability",
        [
            "All Airports",
            "With any infrastructure data",
            "No linked infrastructure data",
        ],
        key="overview_data_availability",
    )
with filter4:
    st.button(
        "↻ Reset Filters",
        width="stretch",
        on_click=reset_overview_filters,
    )

filtered_airports = airport_data
if selected_region != "All Regions":
    selected_region_code = region_names.loc[
        region_names["region_name"] == selected_region, "region_code"
    ].iloc[0]
    filtered_airports = filtered_airports.loc[
        filtered_airports["region_code"] == selected_region_code
    ]
if selected_type != "All Types":
    filtered_airports = filtered_airports.loc[
        filtered_airports["airport_type"] == selected_type
    ]
if selected_availability != "All Airports":
    has_any_data = (
        filtered_airports["has_runway_data"]
        | filtered_airports["has_frequency_data"]
        | filtered_airports["has_navaid_data"]
    )
    if selected_availability == "With any infrastructure data":
        filtered_airports = filtered_airports.loc[has_any_data]
    else:
        filtered_airports = filtered_airports.loc[~has_any_data]

total_airports = len(filtered_airports)
regions_represented = filtered_airports["region_code"].nunique()
total_runways = int(filtered_airports["runway_count"].sum())
total_navaids = int(filtered_airports["navaid_count"].sum())
total_frequencies = int(filtered_airports["frequency_count"].sum())

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    render_kpi(
        title="Total Airports",
        value=f"{total_airports:,}",
        subtitle="in selected view",
        icon_image="airport_icon.jpg",
    )
with kpi2:
    render_kpi(
        title="Regions Represented",
        value=f"{regions_represented:,}",
        subtitle="administrative regions",
        icon_image="regions_icon.jpg",
    )
with kpi3:
    render_kpi(
        title="Runways",
        value=f"{total_runways:,}",
        subtitle="linked runway records",
        icon_image="runway_icon.jpg",
    )
with kpi4:
    render_kpi(
        title="Navigation Aids",
        value=f"{total_navaids:,}",
        subtitle="linked navaid records",
        icon_image="navaids_icon.jpg",
    )
with kpi5:
    render_kpi(
        title="Frequencies",
        value=f"{total_frequencies:,}",
        subtitle="linked frequency records",
        icon_image="frequencies_icon.jpg",
    )

st.markdown("<br>", unsafe_allow_html=True)
map_col, region_col, type_col = st.columns([1.6, 1.25, 1.0])
dashboard_chart_height = 640
region_color_scale = [
    COLORS["card"],
    COLORS["blue"],
    COLORS["cyan"],
    COLORS["orange"],
]

airport_counts = (
    filtered_airports.groupby("region_code")
    .size()
    .rename("airport_count")
    .reset_index()
)
region_map_data = (
    region_summary[["region_code", "region_name"]]
    .drop_duplicates()
    .merge(airport_counts, on="region_code", how="left")
)
region_map_data["airport_count"] = (
    region_map_data["airport_count"].fillna(0).astype(int)
)
region_map_data["region_label"] = region_map_data["region_name"].str.replace(
    " Region", "", regex=False
)
region_count_range = (0, max(1, int(region_map_data["airport_count"].max())))

with map_col:
    with st.container(border=True, key="saudi-region-map-card"):
        render_card_header("Airports by Saudi Region")
        map_data = filtered_airports.dropna(
            subset=["latitude_deg", "longitude_deg"]
        )
        map_figure = px.choropleth_map(
            region_map_data,
            geojson=region_boundaries,
            locations="region_code",
            featureidkey="properties.shapeISO",
            color="airport_count",
            color_continuous_scale=region_color_scale,
            range_color=region_count_range,
            hover_name="region_name",
            hover_data={"region_code": True, "airport_count": True},
            center={"lat": 24.0, "lon": 45.0},
            zoom=2.8,
            opacity=0.7,
        )
        map_figure.add_trace(
            go.Scattermap(
                lat=map_data["latitude_deg"],
                lon=map_data["longitude_deg"],
                mode="markers",
                marker={"size": 7, "color": COLORS["pink"]},
                text=map_data["airport_name"].fillna("Airport"),
                name="Airports",
                hovertemplate="%{text}<extra></extra>",
            )
        )
        map_figure.update_layout(
            map_style="carto-darkmatter",
            map_center={"lat": 24.0, "lon": 45.0},
            map_zoom=2.8,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=dashboard_chart_height,
            coloraxis_colorbar={"title": "Airports"},
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font={"color": COLORS["text"]},
        )
        st.plotly_chart(map_figure, width="stretch")
        st.caption("Administrative boundaries: geoBoundaries, ADM1.")

with region_col:
    with st.container(border=True, key="airports-by-region-card"):
        render_card_header("Airports Locations in Saudi Regions")
        region_chart_data = region_map_data.sort_values(
            "airport_count", ascending=True
        )
        region_figure = px.bar(
            region_chart_data,
            x="airport_count",
            y="region_label",
            orientation="h",
            color="airport_count",
            color_continuous_scale=region_color_scale,
            range_color=region_count_range,
            hover_name="region_name",
            hover_data={"region_code": True, "airport_count": True},
            labels={"airport_count": "Airports", "region_label": "Region"},
        )
        region_figure.update_layout(
            height=dashboard_chart_height,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=False,
            xaxis_title=None,
            yaxis_title=None,
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font={"color": COLORS["text"]},
        )
        region_figure.update_xaxes(
            showgrid=True,
            gridcolor="#1B4058",
            tickfont={"color": COLORS["muted"]},
        )
        region_figure.update_yaxes(
            showgrid=False,
            tickfont={"color": COLORS["text"]},
        )
        st.plotly_chart(region_figure, width="stretch")

type_chart_data = (
    filtered_airports["airport_type"]
    .fillna("unknown")
    .value_counts()
    .rename_axis("airport_type")
    .reset_index(name="airport_count")
)
type_chart_data["type_label"] = type_chart_data["airport_type"].str.replace(
    "_", " "
).str.title()
type_chart_data = type_chart_data.sort_values("airport_count", ascending=True)
type_count_range = (
    0,
    max(1, int(type_chart_data["airport_count"].max()))
    if not type_chart_data.empty
    else 1,
)

with type_col:
    with st.container(border=True, key="airports-by-type-card"):
        render_card_header("Airports by Type")
        type_figure = px.bar(
            type_chart_data,
            x="airport_count",
            y="type_label",
            orientation="h",
            color="airport_count",
            color_continuous_scale=region_color_scale,
            range_color=type_count_range,
            hover_name="type_label",
            hover_data={"airport_type": True, "airport_count": True},
            labels={"airport_count": "Airports", "type_label": "Type"},
        )
        type_figure.update_layout(
            height=dashboard_chart_height,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=False,
            xaxis_title=None,
            yaxis_title=None,
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font={"color": COLORS["text"]},
        )
        type_figure.update_xaxes(
            showgrid=True,
            gridcolor="#1B4058",
            tickfont={"color": COLORS["muted"]},
        )
        type_figure.update_yaxes(
            showgrid=False,
            tickfont={"color": COLORS["text"]},
        )
        st.plotly_chart(type_figure, width="stretch")

    render_insight(
        icon="⌁",
        value=f"{regions_represented} of {len(region_summary)} regions",
        description="have airport records in the selected view.",
        height=int(dashboard_chart_height * 0.25),
    )
