import json
from pathlib import Path
from html import escape

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.cards import render_card_header
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
        "Explore airport infrastructure, regional distribution, and data "
        "coverage from OurAirports."
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
        "Airport Type", ["All Types", *airport_types], key="overview_airport_type"
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
    st.button("↻ Reset Filters", width="stretch", on_click=reset_overview_filters)

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
        title="Total Airports", value=f"{total_airports:,}",
        subtitle="in selected view", icon_image="airport_icon.jpg",
    )
with kpi2:
    render_kpi(
        title="Regions Represented", value=f"{regions_represented:,}",
        subtitle="administrative regions", icon_image="regions_icon.jpg",
    )
with kpi3:
    render_kpi(
        title="Runways", value=f"{total_runways:,}",
        subtitle="linked runway records", icon_image="runway_icon.jpg",
    )
with kpi4:
    render_kpi(
        title="Navigation Aids", value=f"{total_navaids:,}",
        subtitle="linked navaid records", icon_image="navaids_icon.jpg",
    )
with kpi5:
    render_kpi(
        title="Frequencies", value=f"{total_frequencies:,}",
        subtitle="linked frequency records", icon_image="frequencies_icon.jpg",
    )

# Shared dimensions keep each row aligned.
st.markdown("<br>", unsafe_allow_html=True)
TOP_CARD_HEIGHT = 430
BOTTOM_CARD_HEIGHT = 275
TOP_CHART_HEIGHT = 340

region_color_scale = [
    COLORS["card"], COLORS["blue"], COLORS["cyan"], COLORS["orange"]
]

airport_counts = (
    filtered_airports.groupby("region_code")
    .size().rename("airport_count").reset_index()
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

# ROW 1: Map and region bars
map_col, region_col = st.columns([1, 1], gap="medium")
with map_col:
    with st.container(border=True, key="saudi-region-map-card", height=TOP_CARD_HEIGHT):
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
            zoom=3.7,
            opacity=0.7,
        )
        map_figure.add_trace(
            go.Scattermap(
                lat=map_data["latitude_deg"],
                lon=map_data["longitude_deg"],
                mode="markers",
                marker={"size": 6, "color": COLORS["pink"]},
                text=map_data["airport_name"].fillna("Airport"),
                name="Airports",
                hovertemplate="%{text}<extra></extra>",
            )
        )
        map_figure.update_layout(
            map_style="carto-darkmatter",
            map_center={"lat": 24.0, "lon": 45.0},
            map_zoom=3.7,
            height=TOP_CHART_HEIGHT,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar={"title": "Airports", "thickness": 10},
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font={"color": COLORS["text"]},
        )
        st.plotly_chart(map_figure, width="stretch")
        st.caption("Administrative boundaries: geoBoundaries, ADM1.")

with region_col:
    with st.container(border=True, key="airports-by-region-card", height=TOP_CARD_HEIGHT):
        render_card_header("Airports Locations in Saudi Regions")
        region_chart_data = region_map_data.sort_values(
            "airport_count", ascending=True
        )
        # Distinct, bright categorical colors (not a numeric gradient).
        # Use descending counts for the reference palette, then retain the
        # original ascending display order for the horizontal bar chart.
        region_palette = [
            "#F59E0B",  # Orange
            "#83B879",  # Green
            "#20A8E0",  # Blue
            "#27C4D9",  # Cyan
            "#A855F7",  # Purple
            "#E85D9E",  # Pink
            "#94A3B8",  # Slate
        ]
        ranked_regions = region_chart_data.sort_values(
            ["airport_count", "region_label"], ascending=[False, True]
        )
        region_color_map = {
            str(name): region_palette[i % len(region_palette)]
            for i, name in enumerate(ranked_regions["region_label"])
        }
        region_figure = px.bar(
            region_chart_data,
            x="airport_count", y="region_label", orientation="h",
            color="region_label",
            color_discrete_map=region_color_map,
            hover_name="region_name",
            hover_data={"region_code": True, "airport_count": True},
            labels={"airport_count": "Airports", "region_label": "Region"},
        )
        region_figure.update_layout(
            height=TOP_CHART_HEIGHT,
            margin={"r": 15, "t": 5, "l": 0, "b": 10},
            showlegend=False,
            xaxis_title=None, yaxis_title=None,
            paper_bgcolor=COLORS["card"],
            plot_bgcolor=COLORS["card"],
            font={"color": COLORS["text"]},
            bargap=0.28,
        )
        region_figure.update_xaxes(
            showgrid=True, gridcolor="#1B4058",
            tickfont={"color": COLORS["muted"]},
        )
        region_figure.update_yaxes(
            showgrid=False, tickfont={"color": COLORS["text"]},
            automargin=True,
        )
        st.plotly_chart(region_figure, width="stretch")

# ROW 2: Donut with explicit type labels and regional coverage
st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
type_col, coverage_col = st.columns([1, 1], gap="medium")
type_chart_data = (
    filtered_airports["airport_type"]
    .fillna("unknown")
    .value_counts()
    .rename_axis("airport_type")
    .reset_index(name="airport_count")
)
type_chart_data["type_label"] = (
    type_chart_data["airport_type"].str.replace("_", " ").str.title()
)
type_chart_data = type_chart_data.sort_values("airport_count", ascending=False)
type_colors = [
    COLORS["cyan"], COLORS["orange"], COLORS["blue"], COLORS["pink"],
    "#A855F7", "#22C55E", "#FACC15", "#94A3B8",
]

with type_col:
    with st.container(border=True, key="airports-by-type-card", height=BOTTOM_CARD_HEIGHT):
        render_card_header("Airports by Type")
        if type_chart_data.empty:
            st.info("No airport types available for the selected filters.")
        else:
            donut_col, legend_col = st.columns(
                [1, 1.15], gap="small", vertical_alignment="center"
            )
            with donut_col:
                type_figure = go.Figure(
                    data=[
                        go.Pie(
                            labels=type_chart_data["type_label"],
                            values=type_chart_data["airport_count"],
                            hole=0.65,
                            marker={
                                "colors": type_colors,
                                "line": {"color": COLORS["card"], "width": 2},
                            },
                            sort=False,
                            textinfo="none",
                            showlegend=False,
                            hovertemplate=(
                                "%{label}<br>Airports: %{value}<br>"
                                "Share: %{percent}<extra></extra>"
                            ),
                        )
                    ]
                )
                type_figure.add_annotation(
                    text=f"<b>{total_airports:,}</b><br>Airports",
                    x=0.5, y=0.5, xref="paper", yref="paper",
                    font={"size": 17, "color": COLORS["text"]},
                    showarrow=False,
                )
                type_figure.update_layout(
                    height=190,
                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                    paper_bgcolor=COLORS["card"],
                    plot_bgcolor=COLORS["card"],
                    font={"color": COLORS["text"]},
                    showlegend=False,
                )
                st.plotly_chart(
                    type_figure, width="stretch",
                    config={"displayModeBar": False},
                )
            with legend_col:
                legend_html = ""
                for i, (_, item) in enumerate(type_chart_data.iterrows()):
                    label = escape(str(item["type_label"]))
                    count = int(item["airport_count"])
                    color = type_colors[i % len(type_colors)]
                    legend_html += f"""
                    <div style="display:flex;align-items:center;
                        justify-content:space-between;gap:8px;
                        margin-bottom:10px;color:{COLORS['text']};font-size:13px;">
                        <div style="display:flex;align-items:center;gap:8px;min-width:0;">
                            <span style="width:11px;height:11px;flex-shrink:0;
                                border-radius:50%;background:{color};"></span>
                            <span>{label}</span>
                        </div>
                        <strong>{count}</strong>
                    </div>
                    """
                st.markdown(legend_html, unsafe_allow_html=True)

with coverage_col:
    with st.container(border=True, key="regional-coverage-card", height=BOTTOM_CARD_HEIGHT):
        render_card_header("Regional Coverage")
        # Source-data coverage: count unique administrative region codes.
        total_regions = region_summary["region_code"].dropna().nunique()
        coverage_percentage = (
            regions_represented / total_regions * 100 if total_regions else 0
        )
        # Use the same image-based approach as the KPI icons above.
        icon_col, info_col = st.columns(
            [1, 6], gap="small", vertical_alignment="center"
        )
        with icon_col:
            icon_path = (
                Path(__file__).resolve().parents[1]
                / "icons"
                / "coverage_icon.jpg"
            )
            if icon_path.is_file():
                st.image(str(icon_path), width="stretch")
            else:
                st.warning("Coverage icon missing")
        with info_col:
            st.markdown(
                f"""
                <div style="display:flex;align-items:baseline;
                    flex-wrap:wrap;gap:9px;">
                    <span style="font-size:34px;font-weight:750;
                        color:{COLORS['text']};">
                        {regions_represented} of {total_regions}
                    </span>
                    <span style="font-size:12px;color:{COLORS['muted']};">
                        regions represented in the selected view.
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        bar_col, percent_col = st.columns(
            [6, 1.25], gap="small", vertical_alignment="center"
        )
        with bar_col:
            st.progress(min(1.0, max(0.0, coverage_percentage / 100)))
        with percent_col:
            st.markdown(f"**{coverage_percentage:.1f}%**")
        st.caption(
            "Coverage reflects regions with airport records in the selected "
            "view, not actual infrastructure completeness."
        )
