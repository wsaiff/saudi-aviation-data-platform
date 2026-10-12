from html import escape

import streamlit as st

from components.header import render_header
from data import (
    load_airport_infrastructure,
    load_coverage_summary,
    load_region_summary,
)


render_header(
    title="Data coverage",
    subtitle="Review linked infrastructure-data coverage from the dbt gold layer.",
)

coverage = load_coverage_summary()
regions = load_region_summary()
airports = load_airport_infrastructure()
overall_coverage = coverage.loc[coverage["segment_group"] == "Overall"]
all_airports_rows = overall_coverage.loc[
    overall_coverage["segment"] == "All airports"
]
if all_airports_rows.empty:
    raise ValueError("The dbt coverage_summary model has no All airports row.")
all_airports = all_airports_rows.iloc[0]
metric_columns = st.columns(3)
metric_columns[0].metric("Airport records", f"{int(all_airports['airports']):,}")
metric_columns[1].metric(
    "Airports with runway data",
    f"{int(all_airports['with_runways']):,}",
)
metric_columns[2].metric(
    "Airports with frequency data",
    f"{int(all_airports['with_frequencies']):,}",
)

complete_data = (
    airports["has_runway_data"].fillna(False).astype(bool)
    & airports["has_navaid_data"].fillna(False).astype(bool)
    & airports["has_frequency_data"].fillna(False).astype(bool)
)
complete_by_region = (
    airports.assign(complete_data=complete_data)
    .groupby("region_code", dropna=False)["complete_data"]
    .sum()
    .rename("complete_airports")
)
region_coverage = (
    regions[
        [
            "region_code",
            "region_name",
            "total_airports",
            "airports_with_runways",
            "airports_with_navaids",
            "airports_with_frequencies",
        ]
    ]
    .merge(complete_by_region, on="region_code", how="left")
    .fillna({"complete_airports": 0})
    .sort_values("total_airports", ascending=False)
)

def availability_cell(available, total, label, color):
    percentage = 100 * available / total if total else 0
    percentage = min(max(percentage, 0), 100)
    return (
        f'<div class="availability-cell">'
        f'<div class="availability-track" role="progressbar" '
        f'aria-label="{escape(label)}" aria-valuemin="0" '
        f'aria-valuemax="100" aria-valuenow="{percentage:.1f}">'
        f'<div class="availability-fill" style="width:{percentage:.1f}%;'
        f'background:{color};"></div></div>'
        f'<span class="availability-percent">{percentage:.1f}%</span>'
        f"</div>"
    )


st.subheader("Data Availability by Region")
progress_colors = {
    "runways": "linear-gradient(90deg, #20A8E0, #27C4D9)",
    "navaids": "#F59E0B",
    "frequencies": "#8B6FF5",
    "complete": "linear-gradient(90deg, #F59E0B, #FBBF24)",
}
table_rows = []
for row in region_coverage.itertuples(index=False):
    total = int(row.total_airports)
    table_rows.append(
        "<tr>"
        f'<th scope="row">{escape(str(row.region_name))}</th>'
        f'<td class="availability-count">{total:,}</td>'
        f'<td>{availability_cell(int(row.airports_with_runways), total, "Runway data", progress_colors["runways"])}</td>'
        f'<td>{availability_cell(int(row.airports_with_navaids), total, "Navaid data", progress_colors["navaids"])}</td>'
        f'<td>{availability_cell(int(row.airports_with_frequencies), total, "Frequency data", progress_colors["frequencies"])}</td>'
        f'<td>{availability_cell(int(row.complete_airports), total, "Complete data", progress_colors["complete"])}</td>'
        "</tr>"
    )

st.html(
    """
    <style>
    .availability-table-wrap {
        overflow-x: auto;
        border: 1px solid #1B4058;
        border-radius: 12px;
        background: #0D2940;
    }
    .availability-table {
        width: 100%;
        min-width: 760px;
        border-collapse: collapse;
        color: #F5F7FA;
        font: 0.85rem Inter, Arial, sans-serif;
    }
    .availability-table th,
    .availability-table td {
        padding: 0.8rem 0.9rem;
        border-bottom: 1px solid #1B4058;
        text-align: left;
    }
    .availability-table thead th {
        color: #9BAEC0;
        font-size: 0.72rem;
        font-weight: 650;
        white-space: nowrap;
    }
    .availability-table tbody tr:last-child th,
    .availability-table tbody tr:last-child td {
        border-bottom: 0;
    }
    .availability-table tbody th {
        font-weight: 550;
    }
    .availability-count {
        text-align: right !important;
        font-variant-numeric: tabular-nums;
    }
    .availability-cell {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        min-width: 145px;
    }
    .availability-track {
        height: 0.55rem;
        flex: 1;
        overflow: hidden;
        border-radius: 999px;
        background: #071827;
    }
    .availability-fill {
        height: 100%;
        border-radius: inherit;
    }
    .availability-percent {
        width: 3.4rem;
        color: #DCE7F0;
        text-align: right;
        font-variant-numeric: tabular-nums;
    }
    </style>
    <div class="availability-table-wrap">
      <table class="availability-table">
        <thead>
          <tr>
            <th scope="col">Region</th>
            <th scope="col" style="text-align:right">Airports</th>
            <th scope="col">Runway Data</th>
            <th scope="col">Navaid Data</th>
            <th scope="col">Frequency Data</th>
            <th scope="col">Complete Data</th>
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

st.subheader("Coverage by airport type")
type_coverage = coverage.loc[coverage["segment_group"] == "By type"].copy()
type_coverage = type_coverage.rename(
    columns={
        "segment": "Airport type",
        "airports": "Airports",
        "with_runways": "With runway data",
        "with_frequencies": "With frequency data",
        "with_navaids": "With navigation-aid data",
        "pct_runways": "Runway coverage (%)",
        "pct_frequencies": "Frequency coverage (%)",
        "pct_navaids": "Navigation-aid coverage (%)",
    }
)
type_coverage = type_coverage.drop(columns=["segment_group"])
st.dataframe(type_coverage, hide_index=True, width="stretch")

st.info(
    "Coverage measures whether linked runway, frequency, or navigation-aid records "
    "are present in the source data. "
    "Missing data does not always mean missing infrastructure."
)