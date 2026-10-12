import streamlit as st

from components.header import render_header


render_header(
    title="About & sources",
    subtitle="Project context, source data, and important interpretation notes.",
)

st.subheader("About this dashboard")
st.write(
    "This dashboard is part of the SDA Data Engineering project. It aims to unify "
    "the view of aviation infrastructure and provide clear visibility into "
    "source-data coverage gaps across Saudi Arabia."
)

st.subheader("Dataset and snapshot")
st.write(
    "Airport records are imported from OurAirports. The dataset snapshot shown "
    "in this dashboard was loaded on 11 October 2026."
)
st.markdown(
    "[OurAirports data](https://ourairports.com/data/) · "
    "[Airport data CSV](https://davidmegginson.github.io/ourairports-data/airports.csv)"
)

st.subheader("How to interpret coverage")
st.info(
    "Missing data does not always mean missing infrastructure. "
    "A coverage gap indicates that a source field is not populated in the "
    "current dataset; it is not proof that the corresponding infrastructure "
    "does not exist."
)

st.caption(
    "Administrative boundaries used in the overview map are provided by "
    "geoBoundaries (ADM1)."
)