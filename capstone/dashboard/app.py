import streamlit as st

from data import load_airports


st.set_page_config(
    page_title="Saudi Aviation Infrastructure",
    page_icon="✈️",
    layout="wide",
)

st.title("Saudi Aviation Infrastructure")
st.caption(
    "A data platform for Saudi aviation infrastructure"
)

airports = load_airports()

# Filter Saudi Arabia
saudi_airports = airports[
    airports["iso_country"] == "SA"
].copy()

# KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Airports",
        len(saudi_airports),
    )

with col2:
    scheduled = (
        saudi_airports["scheduled_service"]
        .eq("yes")
        .sum()
    )
    st.metric("Scheduled Service", int(scheduled))

with col3:
    st.metric(
        "Airport Types",
        saudi_airports["type"].nunique(),
    )

st.divider()

st.subheader("Saudi Airports")

st.dataframe(
    saudi_airports[
        [
            "name",
            "municipality",
            "type",
            "iata_code",
            "icao_code",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)