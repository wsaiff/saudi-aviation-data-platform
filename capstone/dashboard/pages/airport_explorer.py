from html import escape

import pandas as pd
import streamlit as st

from components.header import render_header
from data import load_airport_infrastructure


DOT_COLORS = ("#20A8E0", "#21C79A", "#8B6FF5")
STATUS_COLORS = {"available": "#27C4D9", "missing": "#9BAEC0"}


def _airport_label(airport):
    name = _text_value(airport["airport_name"], "")
    identifiers = [
        _text_value(airport[column], "")
        for column in ("iata_code", "icao_code", "airport_ident")
        if column in airport.index
    ]
    identifier = " / ".join(dict.fromkeys(value for value in identifiers if value))
    region = _text_value(airport["region_name"], "")
    parts = [value for value in (name, identifier, region) if value]
    return " · ".join(parts)


def _text_value(value, fallback="—"):
    if pd.isna(value) or not str(value).strip():
        return fallback
    return str(value)


def _formatted_number(value, unit=""):
    if pd.isna(value):
        return "—"
    number = float(value)
    formatted = f"{int(number):,}" if number.is_integer() else f"{number:,.1f}"
    return f"{formatted}{unit}"


def _airport_type_label(airport_type):
    return str(airport_type).replace("_", " ").title()


def _badge(available):
    state = bool(available) if pd.notna(available) else False
    label = "Available" if state else "Not Available"
    color = STATUS_COLORS["available"] if state else STATUS_COLORS["missing"]
    return (
        f'<span class="comparison-status" style="--status-color:{color}">'
        f"{label}</span>"
    )


def _label_icon(path):
    return (
        '<svg class="comparison-label-icon" viewBox="0 0 24 24" '
        'aria-hidden="true"><path d="'
        + path
        + '"/></svg>'
    )


def _render_comparison_table(selected_airports):
    label_rows = [
        ("Overview & Location", None, None),
        ("Region", "region_name", "M4 4h16v16H4z M8 8h8v8H8z"),
        (
            "Airport Type",
            "airport_type",
            "M3 21h18M5 21V7l7-4 7 4v14M9 9h1m4 0h1m-6 4h1m4 0h1m-5 8v-4h4v4",
        ),
        (
            "Coordinates",
            "coordinates",
            "M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Zm0-9a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z",
        ),
        (
            "Elevation",
            "elevation_ft",
            "M3 20h18M5 16l4-4 3 3 6-8 2 2",
        ),
        ("Runway Infrastructure", None, None),
        (
            "Runway Data Status",
            "has_runway_data",
            "M3 12h18M5 8h14M5 16h14M7 5v14m10-14v14",
        ),
        (
            "Total Runways",
            "runway_count",
            "M3 12h18M5 8h14M5 16h14M7 5v14m10-14v14",
        ),
        (
            "Surface Types",
            "runway_surfaces",
            "M4 7h16M4 12h16M4 17h16",
        ),
        (
            "Longest Runway",
            "longest_runway_ft",
            "M3 12h18M7 8l-4 4 4 4m10-8 4 4-4 4",
        ),
        ("Navigation & Communications", None, None),
        (
            "Navaid Data Status",
            "has_navaid_data",
            "M12 3v18m-6-3 6-15 6 15M8 13h8",
        ),
        (
            "Total Navaids",
            "navaid_count",
            "M12 3v18m-6-3 6-15 6 15M8 13h8",
        ),
        (
            "Navaid Types",
            "navaid_types",
            "M12 3v18m-6-3 6-15 6 15M8 13h8",
        ),
        (
            "Frequency Data Status",
            "has_frequency_data",
            "M4 10a8 8 0 0 1 16 0c0 5-8 11-8 11S4 15 4 10Zm5 0a3 3 0 1 0 6 0 3 3 0 0 0-6 0Z",
        ),
        (
            "Total Frequencies",
            "frequency_count",
            "M4 10a8 8 0 0 1 16 0c0 5-8 11-8 11S4 15 4 10Zm5 0a3 3 0 1 0 6 0 3 3 0 0 0-6 0Z",
        ),
        (
            "Frequency Types",
            "frequency_types",
            "M4 10a8 8 0 0 1 16 0c0 5-8 11-8 11S4 15 4 10Zm5 0a3 3 0 1 0 6 0 3 3 0 0 0-6 0Z",
        ),
        ("Data Completeness", None, None),
        (
            "Complete Data Score",
            "data_completeness_score",
            "M12 3 14.8 8.7 21 9.6l-4.5 4.4 1.1 6.2L12 17.3l-5.6 2.9 1.1-6.2L3 9.6l6.2-.9L12 3Z",
        ),
    ]

    selected_columns = "".join(
        (
            '<th scope="col"><span class="comparison-airport-heading">'
            f'<span class="comparison-dot" style="--dot-color:{DOT_COLORS[index]}">'
            "</span>"
            f'<span><strong>{escape(_text_value(airport["airport_name"], "Unnamed airport"))}</strong>'
            f'<small>{escape(_text_value(airport["municipality"], "Municipality not reported"))}'
            "</small></span></span></th>"
        )
        for index, airport in enumerate(selected_airports)
    )

    table_rows = []
    for label, field, icon_path in label_rows:
        if field is None:
            table_rows.append(
                '<tr class="comparison-section"><th colspan="'
                f'{len(selected_airports) + 1}">{escape(label)}</th></tr>'
            )
            continue

        cells = []
        for airport in selected_airports:
            if field in {
                "has_runway_data",
                "has_navaid_data",
                "has_frequency_data",
            }:
                value = _badge(airport[field])
            elif field == "coordinates":
                latitude = _text_value(airport["latitude_deg"])
                longitude = _text_value(airport["longitude_deg"])
                value = escape(f"{latitude}, {longitude}")
            elif field in {"navaid_types", "frequency_types"}:
                value = escape(
                    _text_value(
                        airport.get(field),
                        "Not available in current dataset",
                    )
                )
            elif field in {"elevation_ft", "longest_runway_ft"}:
                value = escape(_formatted_number(airport[field], " ft"))
            elif field in {"runway_count", "navaid_count", "frequency_count"}:
                value = escape(_formatted_number(airport[field]))
            elif field == "data_completeness_score":
                score = int(airport[field]) if pd.notna(airport[field]) else 0
                score_tier = "complete" if score == 3 else f"partial-{score}"
                value = (
                    f'<span class="comparison-score score-{score_tier}">'
                    f"&#10003; {score}/3 Complete</span>"
                )
            else:
                value = escape(_text_value(airport[field]))
            cells.append(f"<td>{value}</td>")

        row_class = (
            ' class="comparison-completeness"'
            if field == "data_completeness_score"
            else ""
        )
        table_rows.append(
            f"<tr{row_class}>"
            f'<th scope="row">{_label_icon(icon_path)}{escape(label)}</th>'
            + "".join(cells)
            + "</tr>"
        )

    st.html(
        """
        <style>
        .comparison-table-wrap {
            overflow-x: auto;
            border: 1px solid #1B4058;
            border-radius: 12px;
            background: #0D2940;
        }
        .comparison-table {
            width: 100%;
            min-width: 760px;
            border-collapse: separate;
            border-spacing: 0;
            color: #F5F7FA;
            font: 0.86rem Inter, Arial, sans-serif;
        }
        .comparison-table th,
        .comparison-table td {
            padding: 0.78rem 1rem;
            border-bottom: 1px solid #1B4058;
            text-align: left;
            vertical-align: middle;
        }
        .comparison-table thead th {
            position: sticky;
            top: 0;
            z-index: 2;
            background: #102B3E;
        }
        .comparison-table thead th:first-child,
        .comparison-table tbody th[scope="row"] {
            position: sticky;
            left: 0;
            z-index: 1;
            min-width: 220px;
            background: #0D2940;
        }
        .comparison-table thead th:first-child {
            z-index: 3;
            min-width: 220px;
        }
        .comparison-table tbody tr:nth-child(even):not(.comparison-section) td,
        .comparison-table tbody tr:nth-child(even):not(.comparison-section) th[scope="row"] {
            background: #102B3E;
        }
        .comparison-table tbody tr:last-child th,
        .comparison-table tbody tr:last-child td {
            border-bottom: 0;
        }
        .comparison-table th[scope="row"] {
            font-weight: 550;
            white-space: nowrap;
        }
        .comparison-table tbody td {
            min-width: 180px;
            color: #DCE7F0;
        }
        .comparison-section th {
            padding-top: 1.15rem;
            padding-bottom: 0.55rem;
            border-top: 1px solid #31536A;
            border-bottom: 1px solid #31536A;
            background: #19445D;
            color: #F5F7FA;
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .comparison-section:first-child th {
            border-top: 0;
        }
        .comparison-label-icon {
            width: 1rem;
            height: 1rem;
            margin-right: 0.55rem;
            fill: none;
            stroke: #9BAEC0;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-width: 1.7;
            vertical-align: -0.18rem;
        }
        .comparison-airport-heading {
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            min-width: 180px;
        }
        .comparison-airport-heading strong {
            display: block;
            color: #F5F7FA;
            font-size: 0.88rem;
        }
        .comparison-airport-heading small {
            display: block;
            margin-top: 0.2rem;
            color: #9BAEC0;
            font-size: 0.72rem;
            font-weight: 400;
        }
        .comparison-dot {
            display: inline-block;
            width: 0.62rem;
            height: 0.62rem;
            flex: 0 0 0.62rem;
            margin-top: 0.25rem;
            border-radius: 50%;
            background: var(--dot-color);
        }
        .comparison-status,
        .comparison-score {
            display: inline-block;
            border: 1px solid currentColor;
            border-radius: 999px;
            padding: 0.28rem 0.65rem;
            color: var(--status-color, #27C4D9);
            font-size: 0.76rem;
            font-weight: 700;
            white-space: nowrap;
        }
        .comparison-score {
            font-size: 0.82rem;
        }
        .comparison-score.score-partial-0 {
            border-color: rgba(232,93,158,0.55);
            background: rgba(232,93,158,0.16);
            color: #FF91BE;
        }
        .comparison-score.score-partial-1 {
            border-color: rgba(245,158,11,0.55);
            background: rgba(245,158,11,0.16);
            color: #FFC15C;
        }
        .comparison-score.score-partial-2 {
            border-color: rgba(139,111,245,0.6);
            background: rgba(139,111,245,0.17);
            color: #B7A4FF;
        }
        .comparison-score.score-complete {
            border-color: rgba(33,199,154,0.65);
            background: rgba(33,199,154,0.18);
            color: #55E0B6;
        }
        .comparison-completeness th,
        .comparison-completeness td {
            border-top: 2px solid #27C4D9;
            background: #12344D !important;
        }
        .comparison-empty {
            padding: 1.5rem;
            color: #9BAEC0;
            text-align: center;
        }
        </style>
        <div class="comparison-table-wrap">
          <table class="comparison-table">
            <thead>
              <tr><th scope="col">Airport properties</th>
        """
        + selected_columns
        + """
              </tr>
            </thead>
            <tbody>
        """
        + "".join(table_rows)
        + """
            </tbody>
          </table>
        </div>
        """
    )


render_header(
    title="Airport explorer",
    subtitle="Compare OurAirports records and linked infrastructure data for selected airports.",
)

airports = load_airport_infrastructure()
extended_fields = {
    "icao_code",
    "iata_code",
    "navaid_types",
    "frequency_types",
}
missing_extended_fields = extended_fields.difference(airports.columns)
if missing_extended_fields:
    st.warning(
        "The published airport infrastructure table is missing newer "
        "identifier or infrastructure-type fields. Rebuild the dbt "
        "silver airports and gold airport_infrastructure models to enable "
        "ICAO/IATA search and navigation/frequency type details."
    )
airport_index = airports.set_index("airport_id", drop=False)
selection_key = "airport_compare_selection"
if selection_key not in st.session_state:
    st.session_state[selection_key] = st.session_state.get(
        "airport_compare_ids", []
    )
valid_airport_ids = set(airport_index.index)
st.session_state[selection_key] = [
    airport_id
    for airport_id in st.session_state[selection_key]
    if airport_id in valid_airport_ids
][:3]

st.markdown("### 1. Filter Available Airports")
region_column, type_column = st.columns(2)
with region_column:
    region_options = [
        "All regions",
        *sorted(airports["region_name"].dropna().unique().tolist()),
    ]
    selected_region = st.selectbox(
        "Region",
        region_options,
        key="airport_compare_region_filter",
    )
with type_column:
    airport_types = sorted(airports["airport_type"].dropna().unique().tolist())
    selected_type = st.selectbox(
        "Airport type",
        ["All types", *airport_types],
        format_func=lambda airport_type: (
            "All types"
            if airport_type == "All types"
            else _airport_type_label(airport_type)
        ),
        key="airport_compare_type_filter",
    )

filtered_df = airports
if selected_region != "All regions":
    filtered_df = filtered_df.loc[filtered_df["region_name"] == selected_region]
if selected_type != "All types":
    filtered_df = filtered_df.loc[filtered_df["airport_type"] == selected_type]
filtered_df = filtered_df.sort_values("airport_name", na_position="last")

st.markdown("### 2. Search & Select (Up to 3)")
selected_count = len(st.session_state[selection_key])
st.markdown(
    "<div style='text-align:right;color:#9BAEC0;font-size:0.8rem;"
    f"margin-bottom:0.25rem'>{selected_count} of 3 selected</div>",
    unsafe_allow_html=True,
)
filtered_airport_ids = filtered_df["airport_id"].tolist()
selected_airport_ids_before_filter = st.session_state[selection_key]
multiselect_options = [
    *filtered_airport_ids,
    *(
        airport_id
        for airport_id in selected_airport_ids_before_filter
        if airport_id not in filtered_airport_ids
    ),
]
selected_airport_ids = st.multiselect(
    "Type an airport name or ID to search:",
    options=multiselect_options,
    format_func=lambda airport_id: _airport_label(airport_index.loc[airport_id]),
    max_selections=3,
    placeholder="Choose or search available airports",
    key=selection_key,
)
selected_airports = [
    airport_index.loc[airport_id] for airport_id in selected_airport_ids
]

st.markdown("### Airport comparison & infrastructure")
with st.container(border=True):
    if selected_airports:
        _render_comparison_table(selected_airports)
    else:
        st.info("Select up to three airports to compare their source data.")
