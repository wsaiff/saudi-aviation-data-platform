import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data import count_regions, load_airports
from components.styles import COLORS
from components.header import render_header
from components.kpi import render_kpi
from components.cards import render_insight, render_card_header


@st.cache_data
def load_region_boundaries():
    boundary_file = Path(__file__).resolve().parents[1] / "saudi_regions.geojson"
    return json.loads(boundary_file.read_text(encoding="utf-8"))


# ==========================================
# Temporary Data Loading
# ==========================================

saudi_airports = load_airports()
region_boundaries = load_region_boundaries()
region_map_data = pd.DataFrame(
    [
        {
            "iso_region": feature["properties"]["shapeISO"],
            "region_name": feature["properties"]["shapeName"],
        }
        for feature in region_boundaries["features"]
    ]
)
airport_counts = saudi_airports.groupby("iso_region").size()
region_map_data["airport_count"] = (
    region_map_data["iso_region"].map(airport_counts).fillna(0).astype(int)
)
region_map_data["region_label"] = region_map_data["region_name"].str.replace(
    " Region", "", regex=False
)
region_color_scale = [
    COLORS["card"],
    COLORS["blue"],
    COLORS["cyan"],
    COLORS["orange"],
]
region_count_range = (0, int(region_map_data["airport_count"].max()))
airport_type_labels = {
    "large_airport": "Large airport",
    "medium_airport": "Medium airport",
    "small_airport": "Small airport",
    "heliport": "Heliport",
    "seaplane_base": "Seaplane base",
    "balloonport": "Balloonport",
    "closed": "Closed",
}
type_chart_data = (
    saudi_airports["type"]
    .fillna("unknown")
    .value_counts()
    .rename_axis("airport_type")
    .reset_index(name="airport_count")
)
type_chart_data["type_label"] = type_chart_data["airport_type"].map(
    airport_type_labels
).fillna(type_chart_data["airport_type"].str.replace("_", " ").str.title())
type_chart_data = type_chart_data.sort_values("airport_count", ascending=True)
type_count_range = (0, int(type_chart_data["airport_count"].max()))

# ==========================================
# Header
# ==========================================

render_header(
    title="Saudi Arabia Aviation Overview",
    subtitle=(
        "Explore airport infrastructure, regional distribution, "
        "and data coverage from OurAirports."
    ),
)


# ==========================================
# KPIs
# ==========================================

total_airports = len(saudi_airports)

regions = count_regions(saudi_airports)


kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:
    render_kpi(
        title="Total Airports",
        value=f"{total_airports:,}",
        subtitle="in Saudi Arabia",
        icon_image="airport_icon.jpg",
    )


with kpi2:
    render_kpi(
        title="Regions Represented",
        value=f"{regions:,}",
        subtitle="administrative regions",
        icon_image="regions_icon.jpg",
    )


with kpi3:
    render_kpi(
        title="Runways",
        value="416",
        subtitle="recorded runways",
        icon_image="runway_icon.jpg",
    )


with kpi4:
    render_kpi(
        title="Navigation Aids",
        value="219",
        subtitle="recorded navaids",
        icon_image="navaids_icon.jpg",
    )


with kpi5:
    render_kpi(
        title="Frequencies",
        value="1,028",
        subtitle="recorded frequencies",
        icon_image="frequencies_icon.jpg",
    )


# ==========================================
# Filters
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

filter1, filter2, filter3, filter4 = st.columns(
    [1.1, 1.1, 1.4, 0.95]
)


with filter1:
    region = st.selectbox(
        "Region",
        ["All Regions"],
    )


with filter2:
    airport_type = st.selectbox(
        "Airport Type",
        ["All Types"],
    )


with filter3:
    data_availability = st.selectbox(
        "Data Availability",
        ["All Airports"],
    )


with filter4:
    if st.button(
        "↻ Reset Filters",
        use_container_width=True,
    ):
        st.rerun()


# ==========================================
# Main dashboard
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

map_col, region_col, type_col = st.columns(
    [1.6, 1.25, 1.0]
)
dashboard_chart_height = 640


# ------------------------------------------
# Map (TEMPORARY)
# ------------------------------------------

with map_col:
    with st.container(border=True, key="saudi-region-map-card"):
        render_card_header("Airports by Saudi Region")
        map_data = saudi_airports.dropna(
            subset=["latitude_deg", "longitude_deg"]
        )
        map_figure = px.choropleth_map(
            region_map_data,
            geojson=region_boundaries,
            locations="iso_region",
            featureidkey="properties.shapeISO",
            color="airport_count",
            color_continuous_scale=region_color_scale,
            range_color=region_count_range,
            hover_name="region_name",
            hover_data={"iso_region": True, "airport_count": True},
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
                text=map_data["name"].fillna("Airport"),
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


# ------------------------------------------
# Airports by Region (TEMPORARY)
# ------------------------------------------

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
            hover_data={"iso_region": True, "airport_count": True},
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


# ------------------------------------------
# Airport Type + Insight (TEMPORARY)
# ------------------------------------------

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
        value=f"{regions} of {len(region_map_data)} regions",
        description=(
            "have airport records in the current data snapshot."
        ),
        height=int(dashboard_chart_height * 0.25),
    )